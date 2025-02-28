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
from PRProp3D import *
import time

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Predefined dictionary
prdict = {
    "gl":-3,
    "rat":1,
    "std_image": "MNIST 0",
    "external_image": "",
    "image_type": "real image",
    "image_size_factor": 1,
    "image_invert": False,
    "noisetype": "none",
    "sigma": 0.4,
    "eps": 0.02,
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
    "time_behavior": "Time Dependent",
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
    "arrin":[],
    "planewave": False
}

# Function to generate an image
def process_image(prdict):
    amp=[]
    derived=[]
    output=[]
    xaper=float(prdict['xaper'])
    yaper=float(prdict['yaper'])
    tic=time.time()
    #image = np.random.rand(100, 100)  # Placeholder image (replace with actual processing)
    amp,derived,output=propagate(prdict=prdict,outputs=['ampxz','dnxz'])
    toc=time.time()
    print('elapsed time',toc-tic)
    image=abs(amp)**2
    image=np.rot90(image,k=3)
    #image=np.rot90(abs(output.amps[0])**2,k=3)
    fig, ax = plt.subplots()
    ax.imshow(image, cmap="gray",extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
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

# Function to create labeled upload
def labeled_upload(label, id):
    return dbc.Row([
        dbc.Col(html.Label(label, htmlFor=id), width=4),
        dbc.Col(dcc.Upload(id=id, children=html.Button("Upload File"), multiple=False), width=8),
    ], className="mb-2")


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

# Function to create labeled text inputs
def labeled_text_input(label, id, value=""):
    return dbc.Row([
        dbc.Col(html.Label(label, htmlFor=id), width=4),
        dbc.Col(dcc.Input(value=value, id=id, type="text"), width=8),
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
        labeled_input("Sigma:", "sigma", prdict["sigma"]),
        labeled_input("Scattering strength:", "eps", prdict["eps"]), 
    ], title="Image Settings"),

    dbc.AccordionItem([
        labeled_input("Gain:", "gl", prdict["gl"]),
        labeled_input("Beam Ratio 2_1:", "rat", prdict["rat"]),
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
        labeled_checkbox("Planewave?:", prdict["planewave"], "planewave"),
        labeled_dropdown("Noise Type:", noisetypes, prdict["noisetype"], "noisetype"),
        labeled_checkbox("Use old noise seeds?:", prdict["use_old_seeds"], "use_old_seeds"),
        labeled_checkbox("Fanning study?:", prdict["fanning_study"], "fanning_study"),
        labeled_checkbox("Backpropagate?:", prdict["backpropagate"], "backpropagate")
    ], title="Sampling & Propagation"),

    dbc.AccordionItem([
        labeled_dropdown("Time Behavior:", time_behaviors, prdict["time_behavior"], "time_behavior"),
        labeled_input("End Time:", "tend", prdict["tend"]),
        labeled_input("Time Steps:", "tsteps", prdict["tsteps"]),
        labeled_input("Skip:", "skip", prdict["skip"]),
        labeled_checkbox("Use Consistent Time Steps:", prdict["use_cons_tsteps"], "use_cons_tsteps"),
        labeled_input("Number of Batches", "batchnum_spec", prdict["batchnum_spec"]),
    ], title="Time Settings"),

    dbc.AccordionItem([
        labeled_text_input("Save Folder:", "folder", prdict["folder"]),

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

from dash import ctx  # To track which component triggered the callback




# Callback to update dictionary and process image
@app.callback(
    [Output("output-message", "children"), 
     Output("output-image", "src"), 
     Output("output-image", "style")],
    Input("update-button", "n_clicks"),
    [State("gl","value"),
    State("rat","value"),
    State("std_image","value"),
    State("external_image","contents"),
    State(    "image_type","value"),
    State(    "image_size_factor","value"),
    State(    "image_invert","value"),
    State(    "noisetype","value"),
    State(    "sigma","value"),
    State(    "eps","value"),
    State(    "image_on_beam","value"),
    State(    "xaper","value"),
    State(    "yaper","value"),
    State(    "w01","value"),
    State(    "w02","value"),
    State(    "thout1","value"),
    State(    "thout2","value"),
    State(    "phi1","value"),
    State(    "phi2","value"),
    State(    "xsamp","value"),
    State(    "ysamp","value"),
    State(    "rlen","value"),
    State(    "dz","value"),
    State(    "lm","value"),
    State(    "backpropagate","value"),
    State(    "time_behavior","value"),
    State(    "tend","value"),
    State(    "tsteps","value"),
    State(    "use_cons_tsteps","value"),
    State(    "batchnum_spec","value"),
    State(    "fanning_study","value"),
    State(    "use_old_seeds","value"),
    State(    "folder","value"),
    State(    "savedata","value"),
    State(    "epsr","value"),
    State(    "NT","value"),
    State(    "T","value"),
    State(    "refin","value"),
    State(    "Id","value"),
    State(    "windowedge","value"),
    State(    "E_app","value"),
    State(    "skip","value"),
    
    State(    "planewave","value")],  # Add more states as needed
    prevent_initial_call=True
)



def update_and_process(n_clicks, *args):
    state_keys = [
      "gl", "rat", "std_image", "external_image", "image_type", "image_size_factor",
      "image_invert", "noisetype", "sigma","eps", "image_on_beam", "xaper", "yaper",
      "w01", "w02", "thout1", "thout2", "phi1", "phi2", "xsamp", "ysamp", "rlen",
      "dz", "lm", "backpropagate", "time_behavior", "tend", "tsteps", "use_cons_tsteps",
      "batchnum_spec", "fanning_study", "use_old_seeds", "folder", "savedata", "epsr",
      "NT", "T", "refin", "Id", "windowedge", "E_app", "skip", "planewave"
    ]

      
    # Convert args to a dictionary for easy use
    prdict = {key: value for key, value in zip(state_keys, args)}

    
    # ✅ Convert necessary numeric values to float or int
    int_keys = ["xsamp", "ysamp", "tsteps", "skip", "batchnum_spec"]
    float_keys = ["sigma","eps", "xaper", "yaper", "w01", "w02", "thout1", "thout2", "phi1", "phi2", 
                  "rlen", "dz", "lm", "tend", "epsr", "T", "refin", "Id", "windowedge", "E_app", "NT" ]

    for key in int_keys:
        if key in prdict and prdict[key] is not None:
            try:
                prdict[key] = int(prdict[key])
            except ValueError:
                return f"Invalid integer value for {key}: {prdict[key]}", "", {}

    for key in float_keys:
        if key in prdict and prdict[key] is not None:
            try:
                prdict[key] = float(prdict[key])
            except ValueError:
                return f"Invalid float value for {key}: {prdict[key]}", "", {}
    
    
    if prdict["external_image"] is None:
      prdict["external_image"] = ""
    
    # Ensure folder is valid (should be a text input, not dcc.Upload)
    if prdict["folder"] is None:
        prdict["folder"] = ""
    prdict["arrin"] = []  #temporary
    # Update dictionary with new values
    prdict.update()
    print('entering propagation')
    output_image = process_image(prdict)
    print(prdict)
    return "Processing Complete!", output_image, {"width": "400px", "display": "block"}


  
if __name__ == "__main__":
    app.run_server(debug=True)