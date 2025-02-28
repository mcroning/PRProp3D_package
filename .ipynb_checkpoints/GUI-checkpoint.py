import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Dictionary to populate
data_dict = {
    'gl': -3, 'rat': 1, 'image_on_beam': 'No Image', 'image_type': 'real image',
    'image_size_factor': 1, 'external_image': '', 'std_image': 'MNIST 0', 'image_invert': False,
    'noisetype': 'none', 'sigma': 0.4, 'eps': 0.02, 'kt': 0, 'xaper': 1000, 'yaper': 1000,
    'xsamp': 4096, 'ysamp': 512, 'rlen': 4000, 'dz': 20, 'lm': 0.633, 'w01': 100, 'w02': 100,
    'thout1': 0.16, 'thout2': -0.16, 'phi1': 0, 'phi2': 0, 'backpropagate': False,
    'time_behavior': 'Static', 'tend': 1, 'tsteps': 12, 'use_cons_tsteps': False,
    'batchnum_spec': 1, 'fanning_study': False, 'use_old_seeds': False, 'folder': '',
    'savedata': False, 'epsr': 2500, 'NT': 6.4e22, 'T': 293, 'refin': 2.4, 'Id': 0.01,
    'windowedge': 0.1, 'E_app': 0, 'skip': 4, 'arrin': [], 'planewave': False
}

# Dropdown options
std_image_options = ["MNIST 0", "MNIST 1", "MNIST 2", "MNIST 3", "MNIST 4",
                     "MNIST 5", "MNIST 6", "MNIST 7", "MNIST 8", "MNIST 9", "AF Res Chart"]
xsamples = ["1024", "2048", "4096", "8192", "16384", "32768"]
ysamples = ["256", "512", "1024", "2048", "4096"]
image_type_options = ["real image", "phase image"]
noisetype_options = ["none", "volume xy"]
time_behavior_options = ["Static", "Time Dependent"]
image_on_beam_options = ["No Image", "Beam 1", "Beam 2", "Beams 1 & 2"]

# Function to update dictionary when a selection is made
def on_dropdown_select(event, key):
    data_dict[key] = event.widget.get()
    print(f"Updated: {key} -> {data_dict[key]}")  # Debugging

# Function to update dictionary values
def update_dict():
    for key, entry in entries.items():
        try:
            if isinstance(data_dict[key], bool):
                data_dict[key] = bool(entry_var[key].get())
            elif key in ['xsamp', 'ysamp']:  # Dropdown selections
                data_dict[key] = int(entry_var[key].get())
            elif isinstance(data_dict[key], int):
                data_dict[key] = int(entry.get())
            elif isinstance(data_dict[key], float):
                data_dict[key] = float(entry.get())
            elif isinstance(data_dict[key], list):
                data_dict[key] = entry.get().split(',')
            else:
                data_dict[key] = entry.get()
        except ValueError:
            messagebox.showerror("Input Error", f"Invalid input for {key}")
    messagebox.showinfo("Success", "Dictionary Updated Successfully")

# Function to select a folder
def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_var['folder'].set(folder_selected)
        data_dict['folder'] = folder_selected

# Create main window
root = tk.Tk()
root.title("Dictionary Populator")
root.geometry("600x600")  # Set an initial size for the window
root.minsize(500, 500)  # Minimum size for usability

# Create a canvas with a scrollbar
canvas = tk.Canvas(root)
scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)

entries = {}
entry_var = {}

for idx, (key, value) in enumerate(data_dict.items()):
    ttk.Label(frame, text=key).grid(row=idx, column=0, padx=5, pady=2, sticky="w")

    entry_var[key] = tk.StringVar(value=str(value))

    if isinstance(value, bool):
        cb = ttk.Checkbutton(frame, variable=entry_var[key], onvalue="True", offvalue="False")
        cb.grid(row=idx, column=1, padx=5, pady=2, sticky="w")
    elif key == 'folder':
        entry = ttk.Entry(frame, textvariable=entry_var[key], width=30)
        entry.grid(row=idx, column=1, padx=5, pady=2)
        ttk.Button(frame, text="Browse", command=select_folder).grid(row=idx, column=2, padx=5, pady=2)
    elif key in ['std_image', 'xsamp', 'ysamp', 'image_type', 'noisetype', 'time_behavior', 'image_on_beam']:
        # Dropdowns that update instantly on selection
        options = {
            'std_image': std_image_options,
            'xsamp': xsamples,
            'ysamp': ysamples,
            'image_type': image_type_options,
            'noisetype': noisetype_options,
            'time_behavior': time_behavior_options,
            'image_on_beam': image_on_beam_options
        }
        entry = ttk.Combobox(frame, textvariable=entry_var[key], values=options[key], state="readonly", width=20)
        entry.grid(row=idx, column=1, padx=5, pady=2)
        
        # Bind selection event to update immediately
        entry.bind("<<ComboboxSelected>>", lambda event, k=key: on_dropdown_select(event, k))
    else:
        entry = ttk.Entry(frame, textvariable=entry_var[key], width=20)
        entry.grid(row=idx, column=1, padx=5, pady=2)

    entries[key] = entry

ttk.Button(frame, text="Update Dictionary", command=update_dict).grid(columnspan=3, pady=10)

# Configure canvas and scrolling
canvas.create_window((0, 0), window=frame, anchor="nw")
frame.update_idletasks()
canvas.configure(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

# Packing layout
canvas.pack(fill="both", expand=True, side="left")
scroll_y.pack(fill="y", side="right")

# Run the application
root.mainloop()
