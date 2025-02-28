import json
import base64
import os
from tornado.ioloop import IOLoop
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Button, Div, FileInput, Slider, TextInput, CheckboxGroup, ColumnDataSource

import numpy as np
from bokeh.plotting import figure

# ----------------------
# INITIAL DICTIONARY
# ----------------------
data_dict = {
    "gl": -3, "rat": 1, "image_on_beam": "No Image", "image_type": "real image",
    "image_size_factor": 1, "external_image": "", "std_image": "MNIST 0",
    "image_invert": False, "noisetype": "none", "sigma": 0.4, "eps": 0.02,
}

# ----------------------
# UI ELEMENTS
# ----------------------
dropdowns = {
    "std_image": Select(title="Standard Image", value=data_dict["std_image"], options=["MNIST 0", "MNIST 1", "MNIST 2"]),
    "image_type": Select(title="Image Type", value=data_dict["image_type"], options=["real image", "phase image"]),
    "noisetype": Select(title="Noise Type", value=data_dict["noisetype"], options=["none", "volume xy"]),
}

sliders = {
    "sigma": Slider(title="Sigma", value=data_dict["sigma"], start=0, end=1, step=0.05),
    "eps": Slider(title="Epsilon", value=data_dict["eps"], start=0, end=0.1, step=0.01),
}

checkboxes = {
    "image_invert": CheckboxGroup(labels=["Invert Image"], active=[0] if data_dict["image_invert"] else []),
}

text_inputs = {
    "external_image": TextInput(title="External Image", value=data_dict["external_image"]),
}

file_input_json = FileInput(accept=".json")
status_div = Div(text="<b>Upload a JSON file to load parameters.</b>", width=400)
dict_display = Div(text=f"<pre>{json.dumps(data_dict, indent=2)}</pre>", width=500, height=400)

# ----------------------
# SAMPLE IMAGE (Left Panel)
# ----------------------
image = np.ones((200, 200), dtype=np.uint8) * 255  # White image
image = np.dstack([image, image, image, np.full_like(image, 255)])  # Convert to RGBA format
img_source = ColumnDataSource(data=dict(image=[image], x=[0], y=[0], dw=[200], dh=[200]))

# Input Image Figure
input_plot = figure(title="Input Image", x_range=(0, 200), y_range=(0, 200), width=400, height=400)
input_plot.image_rgba(image="image", x="x", y="y", dw="dw", dh="dh", source=img_source)

# ----------------------
# OUTPUT IMAGE (Right Panel)
# ----------------------
output_source = ColumnDataSource(data=dict(image=[image], x=[0], y=[0], dw=[200], dh=[200]))

output_plot = figure(title="Output Image", x_range=(0, 200), y_range=(0, 200), width=400, height=400)
output_plot.image_rgba(image="image", x="x", y="y", dw="dw", dh="dh", source=output_source)

# ----------------------
# CALLBACK FUNCTIONS
# ----------------------
def update_dict():
    """ Updates the dictionary with current UI values. """
    for key, dropdown in dropdowns.items():
        data_dict[key] = dropdown.value
    for key, slider in sliders.items():
        data_dict[key] = slider.value
    for key, text_input in text_inputs.items():
        data_dict[key] = text_input.value
    for key, checkbox in checkboxes.items():
        data_dict[key] = bool(checkbox.active)

    dict_display.text = f"<pre>{json.dumps(data_dict, indent=2)}</pre>"
    status_div.text = "<b>Dictionary updated.</b>"

def load_json(attr, old, new):
    """ Loads parameters from a JSON file. """
    try:
        json_content = base64.b64decode(new).decode("utf-8")
        loaded_data = json.loads(json_content)
        data_dict.update(loaded_data)
        status_div.text = "<b>JSON file loaded successfully.</b>"
        update_dict()
    except Exception as e:
        status_div.text = f"<b>Error loading JSON:</b> {str(e)}"

def save_json():
    """ Saves the current dictionary to a JSON file. """
    with open("saved_params.json", "w") as json_file:
        json.dump(data_dict, json_file, indent=4)
    status_div.text = "<b>Dictionary saved as 'saved_params.json'.</b>"

def run_image_processing():
    """ Simulated function for processing images based on dictionary parameters. """
    output_text.text = "<b>Processing images...</b>"
    output_status.text = "<b>Image processing completed.</b>"

    # Simulated new image processing result
    new_image = np.zeros((200, 200), dtype=np.uint8)  # Black image
    new_image = np.dstack([new_image, new_image, new_image, np.full_like(new_image, 255)])  # Convert to RGBA format

    # Update the ColumnDataSource for the output image
    output_source.data = dict(image=[new_image], x=[0], y=[0], dw=[200], dh=[200])

def exit_app():
    """ Gracefully exits the Bokeh application. """
    IOLoop.current().stop()

# ----------------------
# BUTTONS
# ----------------------
update_button = Button(label="Update Dictionary", button_type="primary")
update_button.on_click(update_dict)

process_button = Button(label="Run Image Processing", button_type="success")
process_button.on_click(run_image_processing)

save_button = Button(label="Save Dictionary", button_type="success")
save_button.on_click(save_json)

exit_button = Button(label="Exit", button_type="danger")
exit_button.on_click(exit_app)

# ----------------------
# LAYOUT
# ----------------------
layout = column(
    row(update_button, save_button, file_input_json),
    row(*dropdowns.values(), *sliders.values()),
    status_div, dict_display,
    process_button, 
    exit_button
)

curdoc().add_root(layout)
curdoc().title = "Enhanced Bokeh Dictionary Editor"
