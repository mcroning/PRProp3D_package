import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import dash.exceptions
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend
import matplotlib.pyplot as plt
import io
import base64

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Predefined dictionary
prdict = {
    "std_image": "MNIST 0",
    "external_image": "",
    "image_type": "real image",
    "image_size_factor": 1,
    "image_invert": False,
    "noisetype": "none",
    "sigma": 0.4,
    "image_on_beam": "No Image",
    "xaper": 1000,
    "yaper": 1000,
    "w01": 100,
    "w02": 100,
    "thout1": 0.16,
    "thout2": -0.16,
    "phi1": 0,
    "phi2": 0,
    "xsamp": 4096,
    "ysamp": 512,
    "rlen": 4000,
    "dz": 20,
    "lm": 0.633,
    "backpropagate": False,
    "time_behavior": "Static",
    "tend": 1,
    "tsteps": 12,
    "use_cons_tsteps": False,
    "batchnum_spec": 1,
    "fanning_study": False,
    "use_old_seeds": False,
    "folder": "",
    "savedata": False,
    "epsr": 2500,
    "NT": 6.4e22,
    "T": 293,
    "refin": 2.4,
    "Id": 0.01,
    "windowedge": 0.1,
    "E_app": 0,
    "skip": 4,
    "arrin": [],
    "planewave": False,
}

# Function to generate an image
def process_image(prdict):
    image = np.random.rand(100, 100)  # Placeholder image (replace with actual processing)
    
    fig, ax = plt.subplots()
    ax.imshow(image, cmap="gray")
    ax.set_title("Processed Image")

    # Convert plot to image
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded_image = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)
    
    return f"data:image/png;base64,{encoded_image}"

# Dropdown options
standard_images = ["MNIST 0", "MNIST 1", "MNIST 2", "MNIST 3", "MNIST 4", "MNIST 5", "MNIST 6", "MNIST 7", "MNIST 8", "MNIST 9", "AF Res Chart"]
xsamples = ["1024", "2048", "4096", "8192", "16384", "32768"]
ysamples = ["256", "512", "1024", "2048", "4096"]
image_types = ["real image", "phase image"]
noisetypes = ["none", "volume xy"]
time_behaviors = ["Static", "Time Dependent"]
image_on_beams = ["No Image", "Beam 1", "Beam 2", "Beams 1 & 2"]

# Function to create vertically stacked elements with labels
# Function to create labeled dropdowns
# Function to create labeled dropdowns
def labeled_dropdown(label, options, value, id):
    return dbc.Row([
        dbc.Col(html.Label(label, htmlFor=id), width=4),
        dbc.Col(dcc.Dropdown(
            options=[{"label": option, "value": option} for option in options], 
            value=value, 
            id=id
        ), width=8),
    ], className="mb-2")

# Function to create labeled numeric inputs
def labeled_input(label, id, value, input_type="number"):
    return dbc.Row([
        dbc.Col(html.Label(label, htmlFor=id), width=4),
        dbc.Col(dcc.Input(value=value, id=id, type=input_type), width=8),
    ], className="mb-2")

# Function to create labeled file browser inputs
def labeled_file_browser(label, id):
    return dbc.Row([
        dbc.Col(html.Label(label, htmlFor=id), width=4),
        dbc.Col(dcc.Upload(id=id, children=html.Button("Browse"), multiple=False), width=8),
    ], className="mb-2")

# Function to create labeled checkboxes
def labeled_checkbox(label, value, id):
    return dbc.Row([
        dbc.Col(html.Label(label, htmlFor=id), width=4),
        dbc.Col(dcc.Checklist(
            options=[{"label": "", "value": True}], 
            value=[True] if value else [], 
            id=id
        ), width=8),
    ], className="mb-2")

# Accordion with properly structured sections
accordion = dbc.Accordion([
    dbc.AccordionItem([
        labeled_dropdown("Standard Image:", standard_images, prdict["std_image"], "std_image"),
        labeled_file_browser("External Image Path:", "external_image"),
        labeled_dropdown("Image Type:", image_types, prdict["image_type"], "image_type"),
        labeled_input("Image Size Factor:", "image_size_factor", prdict["image_size_factor"]),
        labeled_checkbox("Invert Image:", prdict["image_invert"], "image_invert"),
        labeled_dropdown("Noise Type:", noisetypes, prdict["noisetype"], "noisetype"),
        labeled_input("Sigma:", "sigma", prdict["sigma"]),
    ], title="Image Settings"),



    dbc.AccordionItem([
        labeled_input("Wavelength:", dcc.Input(value=prdict["lm"], id="lm", type="number")),
        labeled_input("External Polar angle 1",dcc.Input(value=prdict["thout1"], id="thout1", type="number")),
        labeled_input("External Polar angle 2",dcc.Input(value=prdict["thout2"], id="thout2", type="number")),      
        labeled_input("Azimuthal Angle 1", dcc.Input(value=prdict["phi1"], id="phi1", type="number")),
        labeled_input("Azimuthal Angle 2", dcc.Input(value=prdict["phi2"], id="phi2", type="number")),
        labeled_input("Beam Waist 1", dcc.Input(value=prdict["w01"], id="w01", type="number")),
        labeled_input("Beam Waist 2", dcc.Input(value=prdict["w02"], id="w02", type="number")),
        labeled_input("Beam Image:", dcc.Dropdown(image_on_beams, prdict["image_on_beam"], id="image_on_beam")),
                      
    ], title="Beam Settings"),

    dbc.AccordionItem([
        labeled_input("X Sampling:", dcc.Dropdown(xsamples, str(prdict["xsamp"]), id="xsamp")),
        labeled_input("Y Sampling:", dcc.Dropdown(ysamples, str(prdict["ysamp"]), id="ysamp")),
        labeled_input("X Aperture:", dcc.Input(value=prdict["xaper"], id="xaper", type="number")),
        labeled_input("Y Aperture:", dcc.Input(value=prdict["yaper"], id="yaper", type="number")),      
        labeled_input("Propagation Distance:", dcc.Input(value=prdict["rlen"], id="rlen", type="number")),
        labeled_input("Propagation Step:", dcc.Input(value=prdict["dz"], id="dz", type="number")),
        
    ], title="Sampling & Propagation"),

    dbc.AccordionItem([
        labeled_input("Time Behavior:", dcc.Dropdown(time_behaviors, prdict["time_behavior"], id="time_behavior")),
        labeled_input("End Time:", dcc.Input(value=prdict["tend"], id="tend", type="number")),
        labeled_input("Time Steps:", dcc.Input(value=prdict["tsteps"], id="tsteps", type="number")),
        labeled_input("Skip:", dcc.Input(value=prdict["skip"], id="skip", type="number")),
        labeled_input("Use Consistent Time Steps:", dcc.Checklist([{"label": "", "value": True}], value=[prdict["use_cons_tsteps"]] if prdict["use_cons_tsteps"] else [], id="use_cons_tsteps")),
      
      
    dbc.AccordionItem([
        labeled_file_browser("Save Folder", "folder"),
        labeled_checkbox("Save Data", prdict["savedata"], "savedata"),
    ], title="Saving Options"),

    dbc.AccordionItem([
        labeled_input("Epsilon Relative", dcc.Input(value=prdict["epsr"], id="epsr", type="number"), "epsr"),
        labeled_input("Number Density (NT)", dcc.Input(value=prdict["NT"], id="NT", type="number"), "NT"),
        labeled_input("Temperature (T)", dcc.Input(value=prdict["T"], id="T", type="number"), "T"),
        labeled_input("Refractive Index (refin)", dcc.Input(value=prdict["refin"], id="refin", type="number"), "refin"),
        labeled_input("Dark Current (Id)", dcc.Input(value=prdict["Id"], id="Id", type="number"), "Id"),
        labeled_input("Window Edge", dcc.Input(value=prdict["windowedge"], id="windowedge", type="number"), "windowedge"),
        labeled_input("Applied Electric Field (E_app)", dcc.Input(value=prdict["E_app"], id="E_app", type="number"), "E_app"),
    ], title="Material Constants"),

      
      
    ], title="Time Settings"),
], start_collapsed=True)

# UI Layout
app.layout = dbc.Container([
    html.H2("Dictionary Editor"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("Update Dictionary & Process Image", id="update-button", color="primary", className="mb-3"),
            html.Div(id="output-message"),
            html.Pre(id="updated-dictionary", style={"whiteSpace": "pre-wrap", "border": "1px solid #ccc", "padding": "10px"}),
        ], width=6),
        dbc.Col([
            html.Img(id="output-image", style={"width": "400px", "display": "none"}),
        ], width=6), 
    ]),

    html.Br(),
    dbc.Button("Exit Application", id="exit-button", color="danger", className="mt-3"),
], fluid=True)

# Callback to update dictionary and process image
@app.callback(
    [Output("output-message", "children"), Output("output-image", "src"), Output("output-image", "style"), Output("updated-dictionary", "children")],
    Input("update-button", "n_clicks"),
    prevent_initial_call=True
)
def update_and_process(n_clicks):
    global prdict  # Ensure we modify the global dictionary
    updated_dict = json.dumps(prdict, indent=2)  # Convert to JSON for display
    output_image = process_image(prdict)
    print(prdict)
    return "Processing Complete!", output_image, {"width": "400px", "display": "block"}, updated_dict

# Callback to print dictionary and exit application
@app.callback(
    Input("exit-button", "n_clicks"),
    prevent_initial_call=True
)
def exit_application(n_clicks):
    print("\nFinal Dictionary:\n", json.dumps(prdict, indent=2))  # Print dictionary
    os._exit(0)  # Force quit without errors

if __name__ == "__main__":
    app.run_server(debug=True)
