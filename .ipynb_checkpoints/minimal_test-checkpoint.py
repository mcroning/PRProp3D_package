from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.io import output_notebook

output_notebook()

# Create a simple figure
p = figure(title="Test Plot", width=400, height=400)
p.circle([1, 2, 3], [4, 5, 6], size=10, color="blue")

# Create a button
button = Button(label="Click Me", button_type="success")

# Define button callback
def on_button_click():
    print("Button was clicked!")  # Should appear in terminal
    button.label = "Clicked!"  # Should update in UI

button.on_click(on_button_click)

# Add everything to the document
curdoc().add_root(column(button, p))

