import os
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
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
    print(prdict['sigma'])
    return f"data:image/png;base64,{encoded_image}"


# Dropdown options
standard_images = ["MNIST 0", "MNIST 1", "MNIST 2", "MNIST 3", "MNIST 4", "MNIST 5", "MNIST 6", "MNIST 7", "MNIST 8", "MNIST 9", "AF Res Chart"]
xsamples = ["1024", "2048", "4096", "8192", "16384", "32768"]
ysamples = ["256", "512", "1024", "2048", "4096"]
image_types = ["real image", "phase image"]
noisetypes = ["none", "volume xy"]
time_behaviors = ["Static", "Time Dependent"]
image_on_beams = ["No Image", "Beam 1", "Beam 2", "Beams 1 & 2"]

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
        labeled_input("Wavelength:", "lm", prdict["lm"]),
        labeled_input("External Polar Angle 1:", "thout1", prdict["thout1"]),
        labeled_input("External Polar Angle 2:", "thout2", prdict["thout2"]),
        labeled_input("Azimuthal Angle 1:", "phi1", prdict["phi1"]),
        labeled_input("Azimuthal Angle 2:", "phi2", prdict["phi2"]),
        labeled_input("Beam Waist 1:", "w01", prdict["w01"]),
        labeled_input("Beam Waist 2:", "w02", prdict["w02"]),
        labeled_dropdown("Beam Image:", image_on_beams, prdict["image_on_beam"], "image_on_beam"),
    ], title="Beam Settings"),

    dbc.AccordionItem([
        labeled_dropdown("X Sampling:", xsamples, str(prdict["xsamp"]), "xsamp"),
        labeled_dropdown("Y Sampling:", ysamples, str(prdict["ysamp"]), "ysamp"),
        labeled_input("X Aperture:", "xaper", prdict["xaper"]),
        labeled_input("Y Aperture:", "yaper", prdict["yaper"]),
        labeled_input("Propagation Distance:", "rlen", prdict["rlen"]),
        labeled_input("Propagation Step:", "dz", prdict["dz"]),
    ], title="Sampling & Propagation"),

    dbc.AccordionItem([
        labeled_dropdown("Time Behavior:", time_behaviors, prdict["time_behavior"], "time_behavior"),
        labeled_input("End Time:", "tend", prdict["tend"]),
        labeled_input("Time Steps:", "tsteps", prdict["tsteps"]),
        labeled_input("Skip:", "skip", prdict["skip"]),
        labeled_checkbox("Use Consistent Time Steps:", prdict["use_cons_tsteps"], "use_cons_tsteps"),
    ], title="Time Settings"),

    dbc.AccordionItem([
        labeled_file_browser("Save Folder", "folder"),
        labeled_checkbox("Save Data", prdict["savedata"], "savedata"),
    ], title="Saving Options"),

    dbc.AccordionItem([
        labeled_input("Epsilon Relative", "epsr", prdict["epsr"]),
        labeled_input("Number Density (NT)", "NT", prdict["NT"]),
        labeled_input("Temperature (T)", "T", prdict["T"]),
        labeled_input("Refractive Index (refin)", "refin", prdict["refin"]),
        labeled_input("Dark Current (Id)", "Id", prdict["Id"]),
        labeled_input("Window Edge", "windowedge", prdict["windowedge"]),
        labeled_input("Applied Electric Field (E_app)", "E_app", prdict["E_app"]),
    ], title="Material Constants"),
], start_collapsed=True)


# Define UI Layout
app.layout = dbc.Container([
    html.H2("Dictionary Editor"),
    
    dbc.Row([
        dbc.Col([
            dbc.Button("Update Dictionary & Process Image", id="update-button", color="primary", className="mb-3"),
            html.Div(id="output-message"),
        ], width=4),
        dbc.Col([
            html.Img(id="output-image", style={"width": "400px", "display": "none"}),
        ], width=8), 
    ]),

    accordion,

    html.Br(),
    dbc.Button("Exit Application", id="exit-button", color="danger", className="mt-3"),
], fluid=True)

# Callback to update dictionary and process image
@app.callback(
    [Output("output-message", "children"), 
     Output("output-image", "src"), 
     Output("output-image", "style")],
    Input("update-button", "n_clicks"),
    [State("std_image", "value"),
     State("image_type", "value"),
     State("image_size_factor", "value"),
     State("image_invert", "value"),
     State("noisetype", "value"),
     State("sigma", "value"),
     State("xsamp", "value"),
     State("ysamp", "value")],  # Add more states as needed
    prevent_initial_call=True
)
def update_and_process(n_clicks, std_image, image_type, image_size_factor, image_invert, noisetype, sigma, xsamp, ysamp):
    # Update dictionary with new values
    prdict.update({
        "std_image": std_image,
        "image_type": image_type,
        "image_size_factor": float(image_size_factor),
        "image_invert": bool(image_invert),
        "noisetype": noisetype,
        "sigma": float(sigma),
        "xsamp": int(xsamp),
        "ysamp": int(ysamp),
    })

    output_image = process_image(prdict)
    print(prdict)
    return "Processing Complete!", output_image, {"width": "400px", "display": "block"}


  
if __name__ == "__main__":
    app.run_server(debug=True)