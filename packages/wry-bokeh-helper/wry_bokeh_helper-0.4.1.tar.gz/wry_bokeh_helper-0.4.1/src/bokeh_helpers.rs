use std::path::PathBuf;
use tao::{
    event::{Event, StartCause, WindowEvent},
    event_loop::{ControlFlow, EventLoopBuilder, EventLoopProxy},
    platform::run_return::EventLoopExtRunReturn,
    window::WindowBuilder,
};
use tokio::sync::broadcast::Sender;
use wry::{
    http::{self, Request},
    WebViewBuilder,
};

#[cfg(target_os = "windows")]
use wry::WebContext;

pub enum UserEvent {
    PayloadReceived(String),
}

#[derive(Clone)]
pub struct BokehCDNResource {
    pub version: String,
}

#[derive(Clone)]
pub struct BokehLocalResource {
    pub folder_uri: String,
}

#[derive(Clone)]
pub enum BokehResource {
    CDN(BokehCDNResource),
    Local(BokehLocalResource),
}

fn ipc_handler(payload: &Request<String>, event_loop_proxy: &EventLoopProxy<UserEvent>) {
    let _ = event_loop_proxy.send_event(UserEvent::PayloadReceived(payload.body().clone()));
}

fn bokeh_cdn_as_script_html(version: &str) -> String {
    format!(
        "
        <script type='text/javascript' src='https://cdn.bokeh.org/bokeh/release/bokeh-{}.min.js'></script>
        <script type='text/javascript' src='https://cdn.bokeh.org/bokeh/release/bokeh-api-{}.min.js'></script>
        <script type='text/javascript' src='https://cdn.bokeh.org/bokeh/release/bokeh-mathjax-{}.min.js'></script>
        ",
        version, version, version
    )
}

fn bokeh_resource_as_script_html(resource: Option<BokehResource>) -> String {
    match resource {
        Some(BokehResource::CDN(BokehCDNResource { version })) => {
            bokeh_cdn_as_script_html(&version)
        }
        Some(BokehResource::Local(_)) => format!(
            "
            <script type='text/javascript' src='/bokeh-resource-dir/bokeh.min.js'></script>
            <script type='text/javascript' src='/bokeh-resource-dir/bokeh-mathjax.min.js'></script>
            <script type='text/javascript' src='/bokeh-resource-dir/bokeh-api.min.js'></script>
            "
        ),
        None => bokeh_cdn_as_script_html("3.5.2"),
    }
}

fn build_bokeh_render_html(resource: Option<BokehResource>) -> String {
    format!(
        "
        <html>
            <head>
            <style>
                html, body {{
                    box-sizing: border-box;
                    display: flow-root;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
            </style>
            {}
            <script type='text/javascript'>
                function renderBokeh(json, dpi, typ) {{
                    const data = JSON.parse(json);
                    const rootId = data['root_id'];
                    if (window.Bokeh === undefined) {{
                        throw new Error('Bokeh is not loaded');
                    }}
                    let devicePixelRatioBase = window.devicePixelRatio;
                    window.devicePixelRatio = devicePixelRatioBase * dpi / 96;
                    const container = document.getElementById('root');
                    window.Bokeh.embed.embed_item(data, container).then((viewManager) => {{
                        const view = viewManager.get_by_id(rootId);
                        const canvas = view.export().canvas;
                        const ctx = canvas.getContext('2d');
                        ctx.globalCompositeOperation = 'destination-over';
                        ctx.fillStyle = '#ffffff';
                        ctx.fillRect(0, 0, canvas.width, canvas.height);
                        container.style.width = canvas.width + 'px';
                        container.style.height = canvas.height + 'px';
                        const dataURL = canvas.toDataURL(typ, 1.0);
                        window.devicePixelRatio = devicePixelRatioBase;
                        window.ipc.postMessage(dataURL);
                    }});
                }}
            </script>
            </head>
            <body>
            <div id='root'></div>
            </body>
        </html>
        ",
        bokeh_resource_as_script_html(resource)
    )
}

fn custom_protocol_handler(
    request: Request<Vec<u8>>,
    resource: &Option<BokehResource>,
) -> Result<http::Response<Vec<u8>>, Box<dyn std::error::Error>> {
    let uri = request.uri().path();

    if uri == "/" {
        return http::Response::builder()
            .header(http::header::CONTENT_TYPE, "text/html")
            .body(build_bokeh_render_html(resource.clone()).into_bytes())
            .map_err(Into::into);
    }

    let path = PathBuf::from(uri);

    if path.parent() == Some(&PathBuf::from("/bokeh-resource-dir")) {
        match resource {
            Some(BokehResource::Local(BokehLocalResource { folder_uri })) => {
                let file_name = path.file_name().unwrap().to_str().unwrap();
                let file_path = PathBuf::from(folder_uri).join(file_name);
                let content = std::fs::read(file_path)?;
                let mimetype = mime_guess::from_path(path)
                    .first()
                    .map(|mime| mime.to_string())
                    .unwrap_or("text/plain".to_string());

                #[cfg(target_os = "windows")]
                let cors = "https://wry.render-bokeh".to_string();

                #[cfg(not(target_os = "windows"))]
                let cors = "wry://render-bokeh".to_string();

                http::Response::builder()
                    .header(http::header::CONTENT_TYPE, mimetype)
                    .header(http::header::ACCESS_CONTROL_ALLOW_ORIGIN, cors)
                    .body(content)
                    .map_err(Into::into)
            }
            _ => {
                return Err("BokehResource is not Local".into());
            }
        }
    } else {
        Err(format!("Invalid path {}", path.to_str().unwrap()).into())
    }
}

fn do_render_bokeh_in_webview(
    json_data: &str,
    dpi: u64,
    typ: &str,
    sender: Sender<String>,
    resource: Option<BokehResource>,
) {
    let mut event_loop = EventLoopBuilder::<UserEvent>::with_user_event().build();
    let event_loop_proxy = event_loop.create_proxy();
    let window = WindowBuilder::new()
        .with_decorations(false)
        .with_visible(false)
        .with_transparent(true)
        .build(&event_loop)
        .unwrap();

    #[cfg(target_os = "windows")]
    let mut web_context = WebContext::new(Some(
        (std::env::var("APPDATA")
            .map(PathBuf::from)
            .unwrap_or_else(|_| std::env::temp_dir()))
        .join("wry_bokeh_helper"),
    ));
    #[cfg(target_os = "windows")]
    let webview_builder = WebViewBuilder::with_web_context(&mut web_context);

    #[cfg(not(target_os = "windows"))]
    let webview_builder = WebViewBuilder::new();

    let webview = webview_builder
        .with_html(build_bokeh_render_html(resource.clone()))
        .with_url("wry://render-bokeh")
        .with_ipc_handler(move |payload| ipc_handler(&payload, &event_loop_proxy))
        .with_custom_protocol(
            "wry".into(),
            move |_, request| match custom_protocol_handler(request, &resource) {
                Ok(response) => response.map(Into::into),
                Err(e) => http::Response::builder()
                    .status(500)
                    .body(e.to_string().as_bytes().to_vec())
                    .unwrap()
                    .map(Into::into),
            },
        )
        .with_transparent(true)
        .build(&window)
        .unwrap();

    webview
        .evaluate_script(&format!(
            "window.onload = () => renderBokeh(`{}`, {}, `{}`)",
            json_data, dpi, typ
        ))
        .unwrap();

    let _ = event_loop.run_return(move |event, _, control_flow| {
        *control_flow = ControlFlow::Wait;

        match event {
            Event::WindowEvent {
                event: WindowEvent::CloseRequested,
                ..
            } => *control_flow = ControlFlow::Exit,
            Event::UserEvent(UserEvent::PayloadReceived(payload)) => {
                sender.send(payload).unwrap();
                *control_flow = ControlFlow::Exit;
            }
            _ => (),
        }
    });
}

pub async fn render_bokeh_in_webview(
    json_data: &str,
    dpi: u64,
    typ: &str,
    resource: Option<BokehResource>,
) -> String {
    let (tx, mut rx) = tokio::sync::broadcast::channel(1);
    do_render_bokeh_in_webview(json_data, dpi, typ, tx, resource);

    rx.recv().await.unwrap()
}
