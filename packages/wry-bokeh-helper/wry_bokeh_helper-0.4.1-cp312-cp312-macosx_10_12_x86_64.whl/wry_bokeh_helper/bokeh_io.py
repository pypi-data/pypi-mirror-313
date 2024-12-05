from __future__ import annotations

import io
import json
import os
import pathlib
import sys
import urllib.request
from typing import TYPE_CHECKING, Any, overload

from PIL import Image

from wry_bokeh_helper._wry_bokeh_helper import render_bokeh

if TYPE_CHECKING:
    from multiprocessing import Queue

    from wry_bokeh_helper._wry_bokeh_helper import ResourceType

    try:
        from bokeh.embed.standalone import StandaloneEmbedJson
        from bokeh.models import Model

    except ImportError:
        Model = Any
        StandaloneEmbedJson = dict[str, Any]

    BokehFigureOrStandaloneJson = Model | StandaloneEmbedJson


def _render_bokeh(
    bokeh_json_item: dict[str, Any],
    dpi: int,
    typ: str,
    resource: tuple[ResourceType, str] | None,
) -> str:
    try:
        return render_bokeh(
            json_data=json.dumps(bokeh_json_item),
            dpi=dpi,
            typ=typ,
            resource=resource,
        )
    except BaseException as e:
        raise e


def _run_in_process(
    queue: Queue,
    bokeh_json_item: dict[str, Any],
    dpi: int,
    typ: str,
    resource: tuple[ResourceType, str] | None,
):
    try:
        data_url = _render_bokeh(
            bokeh_json_item,
            dpi,
            typ,
            resource,
        )
        queue.put(data_url)
    except BaseException as e:
        queue.put(e)


def _get_img_data_url_in_subprocess(
    bokeh_json_item: dict[str, Any],
    dpi: int,
    typ: str,
    resource: tuple[ResourceType, str] | None,
) -> str:
    from multiprocessing import Process, Queue, freeze_support
    from multiprocessing.process import current_process
    from queue import Empty

    if getattr(current_process(), "_inheriting", False):
        freeze_support()
    queue: Queue[str | BaseException] = Queue()
    process = Process(
        target=_run_in_process,
        args=(
            queue,
            bokeh_json_item,
            dpi,
            typ,
            resource,
        ),
    )
    process.start()

    try:
        result = queue.get(timeout=60)
    except Empty:
        raise TimeoutError("The process took too long to complete.")
    if isinstance(result, BaseException):
        raise result
    return result


@overload
def bokeh_to_image(
    bokeh_figure_or_bokeh_standalone_json: BokehFigureOrStandaloneJson,
    *,
    dpi: int = 300,
    typ: str = "image/png",
    resource: tuple[ResourceType, str] | None = None,
) -> Image.Image:
    """
    Converts a Bokeh figure or standalone JSON to an image.

    Args:
        bokeh_figure_or_bokeh_standalone_json (BokehFigureOrStandaloneJson):
            The Bokeh figure or standalone JSON to convert.
        dpi (int, optional):
            The resolution of the image in dots per inch. Default is 300.
        resource (tuple[ResourceType, str] | None, optional):
            Additional resources required for the conversion. Defaults to None.
    Returns:
        Image.Image: The resulting image.
    """
    ...


@overload
def bokeh_to_image(
    bokeh_figure_or_bokeh_standalone_json: BokehFigureOrStandaloneJson,
    filepath: os.PathLike[str] | str,
    *,
    dpi: int = 300,
    typ: str = "image/png",
    resource: tuple[ResourceType, str] | None = None,
) -> None:
    """
    Save a Bokeh plot to a specified file path.

    Parameters:
        bokeh_figure_or_bokeh_standalone_json (BokehFigureOrStandaloneJson):
            The Bokeh figure or standalone JSON to be saved as an image.
        filepath (os.PathLike[str] | str):
            The file path where the image will be saved.
        dpi (int, optional):
            The resolution of the saved image in dots per inch. Default is 300.
        resource (tuple[ResourceType, str] | None, optional):
            Additional resources required for saving the image. Default is None.

    Returns:
        None
    """
    ...


def bokeh_to_image(
    bokeh_figure_or_bokeh_standalone_json: BokehFigureOrStandaloneJson,
    filepath: os.PathLike[str] | str | None = None,
    *,
    dpi: int = 300,
    typ: str = "image/png",
    resource: tuple[ResourceType, str] | None = None,
) -> Image.Image | None:
    if typ not in ["image/jpeg", "image/png", "image/webp"]:
        raise ValueError(
            "Invalid `toDataURL` type value. See https://developer.mozilla.org/en-US/docs/Web/API/HTMLCanvasElement/toDataURL for more details."
        )
    if isinstance(bokeh_figure_or_bokeh_standalone_json, dict):
        bokeh_json_item = bokeh_figure_or_bokeh_standalone_json

    else:
        try:
            from bokeh.embed.standalone import json_item
            from bokeh.models import Model
        except ImportError:
            raise ImportError("bokeh is not installed.")
        if not isinstance(bokeh_figure_or_bokeh_standalone_json, Model):
            raise TypeError(
                "bokeh_figure_or_bokeh_standalone_json must be a Bokeh Model."
            )
        bokeh_json_item = json_item(bokeh_figure_or_bokeh_standalone_json)
    is_MacOS = sys.platform == "darwin"
    if is_MacOS:
        img_data_url = _get_img_data_url_in_subprocess(
            {**bokeh_json_item}, dpi, typ, resource
        )
    else:
        img_data_url = _render_bokeh({**bokeh_json_item}, dpi, typ, resource)
    response = urllib.request.urlopen(img_data_url)
    img = Image.open(io.BytesIO(response.read()))

    if filepath:
        # if want jpg, convert RGBA to RGB
        filepath = pathlib.Path(filepath)
        if typ == "image/png" and (
            filepath.suffix == ".jpg" or filepath.suffix == ".jpeg"
        ):
            img = img.convert("RGB")
        return img.save(filepath, dpi=(dpi, dpi))
    return img
