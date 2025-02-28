import json
import base64
import os
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Select, Button, Div, FileInput, Slider, TextInput, CheckboxGroup, ColumnDataSource, Tabs, Panel
from bokeh.plotting import figure

# ----------------------
# INITIAL DICTIONARY
# ----------------------
data_dict = {
    'gl': -3, 'rat': 1, 'image_on_beam': 'No Image', 'image_type': 'real image',
    'image_size_factor': 1, 'external_image': '', 'std_image': 'MNIST 0',
    'image_invert': False, 'noisetype': 'none', 'sigma': 0.4, 'eps': 0.02,
    'kt': 0, 'xaper': 1000, 'yaper': 1000, 'xsamp': 4096, 'ysamp': 512,
    'rlen': 4000, 'dz': 20, 'lm': 0.633, 'w01': 100, 'w02': 100,
    'thout1': 0.16, 'thout2': -0.16, 'phi1': 0, 'phi2': 0, 'backpropagate': False,
    'time_behavior': 'Static', 'tend': 1, 'tsteps': 12, 'use_cons_tsteps': False,
    'batchnum_spec': 1, 'fanning_study': False, 'use_old_seeds': False,
    'folder': '', 'savedata': False, 'epsr': 2500, 'NT': 6.4e22, 'T': 293,
    'refin': 2.4, 'Id': 0.01, 'windowedge': 0.1, 'E_app': 0, 'skip': 4,
    'arrin': [], 'planewave': False
}

# ----------------------
# UI ELEMENTS
# ----------------------
dropdowns = {
    "std_image": Select(title="Standard Image", value=data_dict["std_image"], options=[
        "MNIST 0", "MNIST 1", "MNIST 2", "MNIST 3", "MNIST 4",
        "MNIST 5", "MNIST 6", "MNIST 7", "MNIST 8", "MNIST 9", "AF Res Chart"
    ]),
    "image_type": Select(title="Image Type", value=data_dict["image_type"], options=["real image", "phase image"]),
    "noisetype": Select(title="Noise Type", value=data_dict["noisetype"], options=["none", "volume xy"]),
    "time_behavior": Select(title="Time Behavior", value=data_dict["time_behavior"], options=["Static", "Time Dependent"]),
    "image_on_beam": Select(title="Image on Beam", value=data_dict["image_on_beam"], options=["No Image", "Beam 1", "Beam 2", "Beams 1 & 2"]),
}

sliders = {
    "sigma": Slider(title="Sigma", value=data_dict["sigma"], start=0, end=1, step=0.05),
    "eps": Slider(title="Epsilon", value=data_dict["eps"], start=0, end=0.1, step=0.01),
    "xaper": Slider(title="X Aperture", value=data_dict["xaper"], start=100, end=5000, step=100),
    "yaper": Slider(title="Y Aperture", value=data_dict["yaper"], start=100, end=5000, step=100),
}

checkboxes = {
    "image_invert": CheckboxGroup(labels=["Invert Image"], active=[0] if data_dict["image_invert"] else []),
    "backpropagate": CheckboxGroup(labels=["Backpropagate"], active=[0] if data_dict["backpropagate"] else []),
    "savedata": CheckboxGroup(labels=["Save Data"], active=[0] if data_dict["savedata"] else []),
}

text_inputs = {
    "external_image": TextInput(title="External Image", value=data_dict["external_image"]),
    "folder": TextInput(title="Folder", value=data_dict["folder"]),
}

file_input_json = FileInput(accept=".json")
status_div = Div(text="<b>Upload a JSON file to load parameters.</b>", width=400)
dict_display = Div(text=f"<pre>{json.dumps(data_dict, indent=2)}</pre>", width=500, height=400)

# ----------------------
# IMAGE DISPLAY
# ----------------------
image = np.ones((200, 200), dtype=np.uint8) * 255
image = np.dstack([image, image, image, np.full_like(image, 255)])
img_source = ColumnDataSource(data=dict(image=[image], x=[0], y=[0], dw=[200], dh=[200]))

input_plot = figure(title="Input Image", x_range=(0, 200), y_range=(0, 200), width=400, height=400)
input_plot.image_rgba(image='image', x='x', y='y', dw='dw', dh='dh', source=img_source)

output_source = ColumnDataSource(data=dict(image=[image], x=[0], y=[0], dw=[200], dh=[200]))
output_plot = figure(title="Output Image", x_range=(0, 200), y_range=(0, 200), width=400, height=400)
output_plot.image_rgba(image='image', x='x', y='y', dw='dw', dh='dh', source=output_source)

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

def run_image_processing():
    """ Simulated function for processing images based on dictionary parameters. """
    output_source.data = dict(image=[image], x=[0], y=[0], dw=[200], dh=[200])
    status_div.text = "<b>Processing completed.</b>"

# ----------------------
# ORGANIZING UI INTO TABS
# ----------------------
image_settings = Panel(title="Image Settings", child=column(*dropdowns.values(), *checkboxes.values()))
processing_settings = Panel(title="Processing Parameters", child=column(*sliders.values()))
file_settings = Panel(title="File Settings", child=column(file_input_json, text_inputs["folder"]))

tabs = Tabs(tabs=[image_settings, processing_settings, file_settings])

# ----------------------
# BUTTONS
# ----------------------
update_button = Button(label="Update Dictionary", button_type="primary")
update_button.on_click(update_dict)

process_button = Button(label="Run Image Processing", button_type="success")
process_button.on_click(run_image_processing)

exit_button = Button(label="Exit", button_type="danger")
exit_button.on_click(lambda: os._exit(0))

# ----------------------
# FINAL LAYOUT
# ----------------------
controls_and_status = column(tabs, update_button, process_button, status_div, dict_display)
image_panel = row(input_plot, output_plot)
layout = row(controls_and_status, image_panel)

curdoc().add_root(layout)
curdoc().title = "Structured Bokeh Dictionary Editor"
