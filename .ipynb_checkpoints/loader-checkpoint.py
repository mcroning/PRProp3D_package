import torch
import numpy as np
#import cupy as cp

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython import display as ipydisplay
from IPython.display import display
import json
from pathlib import Path
from PIL import Image, ImageChops
import ipywidgets as widgets
from ipywidgets import interact, interactive, fixed
from scipy.ndimage import zoom, gaussian_filter
import subprocess

#default parameters
prdict={
'gl':-3,
'rat':1,
'image_on_beam':'No Image',
'image_type':'real image',
'image_size_factor':1,
'external_image':'',
'std_image':'MNIST 0',
'image_invert':False,
'noisetype':'none',
'sigma':0.4,
'eps':0.02,
'kt':0,
'xaper':1000,
'yaper':1000,
'xsamp':4096,
'ysamp':512,
'rlen':4000,
'dz':20,
'lm':0.633,
'w01':100,
'w02':100,
'thout1':0.16,
'thout2':-0.16,
'phi1':0,
'phi2':0,
'backpropagate':False,
'time_behavior':'Static',
'tend':1,
'tsteps':12,
'use_cons_tsteps':False,
'batchnum_spec':1,
'fanning_study':False,
'use_old_seeds':False,
'folder':'',
'savedata':False,
'epsr':2500,
'NT':6.4e22,
'T':293,
'refin':2.4,
'Id':0.01,
'windowedge':0.1,
'E_app':0,
'skip':4,
'arrin':[],
'planewave':False          
}
p = prdict #shorthand for dictionary

print(prdict)

if not Path("./sample_images").exists():
  process = subprocess.run(['git clone https://github.com/mcroning/sample_images'],shell=True)

#prdata={} # parameter dictionary
data_file_name=""
first_run=True
if first_run:
  #prdata_d={} # parameter dictionary
  load_existing=input("Do you want to load existing parameters from Google Drive \n \
   if no, defaults will be used: y or n:")
else:
  load_existing=input("Do you want to load existing parameters from Google Drive \n \
   if no, values in widgets will be used: y or n:")

load_success=False
if load_existing in ("y","Y","Yes","YES"):
  from google.colab import drive
  drive.mount('/content/drive')
  data_file_name=input("enter starting parameter file (json or npz): ")
  print('dfn',data_file_name)
# Load parameters from npz file if needed

  if data_file_name != "":
    if Path(data_file_name).suffix==".npz":
      prdict=np.load(data_file_name,allow_pickle=True)["arr_0"].item()
      load_success=True
      first_run=False
    elif Path(data_file_name).suffix==".json":
      with open(data_file_name) as f:
        prdict=json.load(f)
      load_success=True
      first_run=False
      print(prdict)
    else:
      print("unknown file type")
      load_existing=False

p=prdict

# initialize parameters:
#set up input widgets
standard_images=["MNIST 0", "MNIST 1", "MNIST 2", "MNIST 3", "MNIST 4", "MNIST 5", "MNIST 6", "MNIST 7", "MNIST 8", "MNIST 9", "AF Res Chart"]
xsamples=["1024", "2048", "4096", "8192", "16384","32768"]
ysamples=["256", "512", "1024", "2048","4096"]

#Dropdowns
im_type=widgets.Dropdown(options=['real image', 'phase image'],value=p['image_type'],description='image type',disabled=False)
std_im=widgets.Dropdown(options=standard_images,value=p['std_image'],description='standard image',disabled=False)
noisetype_=widgets.Dropdown(options=["none","volume xy"],value="none",description=p['noisetype'],disabled=False)
xsamp_=widgets.Dropdown(options=xsamples,value=str(p['xsamp']),description='x samples',disabled=False)
ysamp_=widgets.Dropdown(options=ysamples,value=str(p['ysamp']),description='y_samples',disabled=False)
t_beh=widgets.Dropdown(options=["Static", "Time Dependent"],value=p['time_behavior'],description='time behavior',disabled=False)
im_on_beam=widgets.Dropdown(options=['No Image','Beam 1','Beam 2','Beams 1 & 2'],value=p['image_on_beam'],description='image on beam',disabled=False)

#Checkboxes
im_invert=widgets.Checkbox(value=p['image_invert'],description='invert image',disabled=False)
#plane_model=widgets.Checkbox(value=False,description='use plane wave space charge model if appropriate',disabled=False)
bkp=widgets.Checkbox(value=p['backpropagate'],description='backpropagate output image',disabled=False)
use_cons_tsteps_=widgets.Checkbox(value=p['use_cons_tsteps'],description='use conservative time steps',disabled=False)
fanning_study_=widgets.Checkbox(value=p['fanning_study'],description='fanning study',disabled=False)
use_old_seeds_=widgets.Checkbox(value=p['use_old_seeds'],description='use old seeds',disabled=False)
save_output=widgets.Checkbox(value=p['savedata'],description='save output',disabled=False)

#FloatTexts
gl_=widgets.FloatText(value=p['gl'],description='gain length product',disabled=False)
rat_=widgets.FloatText(value=p['rat'],description='beam ratio',disabled=False)
im_size_norm=widgets.FloatText(value=p['image_size_factor'],description='image size norm by waist',disable=False)
sigma_=widgets.FloatText(value=p['sigma'],description='scattering correlation length',disabled=False)
volnoise=widgets.FloatText(value=p['eps'],description='volume noise parameter',disabled=False)
eapp=widgets.FloatText(value=p['E_app'],description='applied electic field kV/cm',disabled=False)
kerr_coeff=widgets.FloatText(value=p['kt'],description='Kerr coefficient',disabled=False)
xaper_=widgets.FloatText(value=p['xaper'],description='x aperture um',disabled=False)
yaper_=widgets.FloatText(value=p['yaper'],description='y aperture um',disabled=False)
int_len=widgets.FloatText(value=p['rlen'],description='interaction length',disabled=False)
dz_=widgets.FloatText(value=p['dz'],description='z step size um',disabled=False)
lm_=widgets.FloatText(value=p['lm'],description='wavelength um',disabled=False)
w1=widgets.FloatText(value=p['w01'],description='waist 1',disabled=False)
w2=widgets.FloatText(value=p['w02'],description='waist 2',disabled=False)
th1=widgets.FloatText(value=p['thout1'],description='beam 1 polar angle',disabled=False)
th2=widgets.FloatText(value=p['thout2'],description='beam 2 polar angle',disabled=False)
az1=widgets.FloatText(value=p['phi1'],description='azimuth 1',disabled=False)
az2=widgets.FloatText(value=p['phi2'],description='azimuth 2',disabled=False)
end_time=widgets.FloatText(value=p['tend'],description='end time (t0)',disabled=False)
epsr_=widgets.FloatText(value=p['epsr'],description='relative dielectric constant',disabled=False)
charge_dens=widgets.FloatText(value=p['NT'],description='mobile charge density',disabled=False)
temperature=widgets.FloatText(value=p['T'],description='temperature K',disabled=False)
index=widgets.FloatText(value=p['refin'],description='refractive index',disabled=False)
dark_intensity=widgets.FloatText(value=p['Id'],description='dark intensity',disabled=False)
windowedge_=widgets.FloatText(value=p['windowedge'],description='Tukey window edge',disabled=False)

# IntTexts
tsteps_=widgets.IntText(value=p['tsteps'],description='time steps',disabled=False)
numbatch_=widgets.IntText(value=p['batchnum_spec'],description='number of batches',disabled=False)

#Texts
gdrive_folder=widgets.Text(value=p['folder'],placeholder='Insert text here',description='Google drive folder',disabled=False)
external_im=widgets.Text(value=p['external_image'],placeholder='Insert text here',description='external image file',disabled=False)

#set Box layout

vbox_left=widgets.VBox([gl_,rat_,im_on_beam,im_type,im_size_norm,external_im,
                        std_im,im_invert,noisetype_,sigma_,volnoise,eapp,kerr_coeff,
                        xaper_,yaper_,xsamp_,ysamp_,int_len,dz_,lm_,w1,w2
                        ])
vbox_right=widgets.VBox([th1,th2,az1,az2,bkp,t_beh,end_time,tsteps_,
                        use_cons_tsteps_,numbatch_,fanning_study_,
                        use_old_seeds_,gdrive_folder,save_output,epsr_,charge_dens,
                        temperature,index,dark_intensity,windowedge_])
hbox=widgets.HBox([vbox_left,vbox_right])
display(hbox)