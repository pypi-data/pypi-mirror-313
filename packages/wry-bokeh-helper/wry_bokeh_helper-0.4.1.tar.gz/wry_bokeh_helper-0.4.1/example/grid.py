import numpy as np
from bokeh.plotting import figure, gridplot

from wry_bokeh_helper import bokeh_to_image

if __name__ == "__main__":
    p = figure()
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.sin(x)
    p.line(x, y, line_color="#1f77b4")

    p2 = figure()
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.cos(x)
    p2.line(x, y, line_color="#ff7f0e")

    p3 = figure()
    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)
    p3.line(x, y, line_color="#2ca02c")

    p4 = figure()
    x = np.linspace(0, 4 * np.pi, 100)
    y = np.cos(x)
    p4.line(x, y, line_color="#d62728")

    gp = gridplot([[p, p2], [p3, p4]])

    bokeh_to_image(
        gp,
        "grid.png",
        typ="image/png",
        dpi=300,
    )
