use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

mod bokeh_helpers;

#[pyfunction]
#[pyo3(signature = (json_data, dpi=300, typ="image/png", resource=None))]
fn render_bokeh(
    json_data: &str,
    dpi: u64,
    typ: &str,
    resource: Option<[String; 2]>,
) -> PyResult<String> {
    let resource = match resource {
        Some(resource) => {
            let variant = &resource[0];
            let value = (&resource[1]).clone();

            if value == "" {
                return Err(PyValueError::new_err("Resource value cannot be empty"));
            }

            match variant.as_str() {
                "cdn" => Some(bokeh_helpers::BokehResource::CDN(
                    bokeh_helpers::BokehCDNResource { version: value },
                )),
                "local" => Some(bokeh_helpers::BokehResource::Local(
                    bokeh_helpers::BokehLocalResource { folder_uri: value },
                )),
                _ => {
                    return Err(PyValueError::new_err(format!(
                        "Invalid resource variant: {}",
                        variant
                    )))
                }
            }
        }
        None => None,
    };

    Ok(tokio::runtime::Runtime::new()
        .unwrap()
        .block_on(bokeh_helpers::render_bokeh_in_webview(
            json_data, dpi, typ, resource,
        )))
}

/// A Python module implemented in Rust.
#[pymodule]
fn wry_bokeh_helper(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(render_bokeh, m)?)?;
    Ok(())
}
