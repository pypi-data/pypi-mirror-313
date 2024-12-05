from typing import Literal

ResourceType = Literal["cdn", "local"]

def render_bokeh(
    json_data: str,
    dpi: int = 300,
    typ: str = "image/png",
    resource: tuple[ResourceType, str] | None = None,
) -> str:
    """Render Bokeh JSON to a image URL."""
    ...
