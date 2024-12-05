# wry-bokeh-helper

Bokeh is a great library for creating interactive plots in Python. However, it can be a bit verbose to use, especially when you want to export a plot to a standalone image file (which is fairly common in scientific publications). This library provides a simple wrapper around Bokeh that makes it easier to export them to image files.

## Installation

```bash
pip install wry-bokeh-helper
```

## Usage

```python
from bokeh.plotting import figure, show
from wry_bokeh_helper import bokeh_to_image

# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# create a new plot with a title and axis labels
p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")

# add a line renderer with legend and line thickness
p.line(x, y, legend_label="Temp.", line_width=2)


# Export the plot to an image file
img = bokeh_to_image(plot, dpi=600)
img.show()

bokeh_to_image(plot, dpi=300, filename="plot.png")
```
