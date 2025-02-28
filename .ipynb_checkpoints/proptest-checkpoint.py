from PRProp3D import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import torch

prdict={
'gl':-3, 
'rat':6.67,
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
'rlen':400,
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

if  prdict['w01'] < 0 or prdict['w02'] < 0: #we are using plane waves, so force periodic conditions

  fc=prdict['xsamp']*prdict['lm']/2/prdict['xaper']
  prdict['thout1']=np.arcsin(fc/(2**round(np.log(
    fc/np.sin(abs(prdict['thout1'])))/np.log(2))))*np.sign(prdict['thout1'])
  prdict['thout2']=-prdict['thout1']
  prdict['windowedge']=0


# call propagator to popagate input
amp,derived,output=propagate(prdict=prdict,outputs=['ampxz','dnxz'])

print('calculated gain',output.gain)
imoutp=np.rot90(abs(output.amps[0])**2,k=3)
imoutm=np.rot90(abs(output.amps[1])**2,k=3)

iminp=np.rot90(abs(output.amps[2])**2,k=3)
iminm=np.rot90(abs(output.amps[3])**2,k=3)

xaper=prdict['xaper']
yaper=prdict['yaper']
xsamp=prdict['xsamp']
ysamp=prdict['ysamp']

fig1,ax1 = plt.subplots(1,2)
ax1[0].set_title('Beam 1 in')
ax1[0].set_xlabel(r'x ($\mu$m)')
ax1[0].set_ylabel(r'y ($\mu$m)')
                  
im=ax1[0].imshow(iminp,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
fig1.colorbar(im,ax=ax1[0],shrink=0.5)  
ax1[1].set_title('Beam 2 in')  
ax1[1].set_xlabel(r'x ($\mu$m)')
ax1[1].set_ylabel(r'y ($\mu$m)')
im=ax1[1].imshow(iminm,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2]) 
fig1.colorbar(im,ax=ax1[1],shrink=0.5)
fig1.tight_layout()

fig2,ax2 = plt.subplots(1,2)
ax2[0].set_title('Beam 1 out')
ax2[0].set_xlabel(r'x ($\mu$m)')
ax2[0].set_ylabel(r'y ($\mu$m)')
im=ax2[0].imshow(imoutp,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2])
fig2.colorbar(im,ax=ax2[0],shrink=0.5)  
ax2[1].set_title('Beam 2 out') 
ax2[1].set_xlabel(r'x ($\mu$m)')
ax2[1].set_ylabel(r'y ($\mu$m)')
im=ax2[1].imshow(imoutm,extent=[-xaper//2,xaper//2,-yaper//2,yaper//2]) 
fig2.colorbar(im,ax=ax2[1],shrink=0.5)
fig2.tight_layout()

fig3,ax3 = plt.subplots()
ax3.plot(derived.x,iminp[ysamp//2,:])
ax3.plot(derived.x,iminm[ysamp//2,:])
ax3.set_xlabel('transverse x microns')
ax3.set_ylabel('normalized intensity')
ax3.legend(['beam1', 'beam2'])
ax3.set_ylim(0,1)
ax3.set_title('input')

fig4,ax4 = plt.subplots()
ax4.plot(derived.x,imoutp[ysamp//2,:])
ax4.plot(derived.x,imoutm[ysamp//2,:])
ax4.set_xlabel('transverse x microns')
ax4.set_ylabel('normalized intensity')
ax4.legend(['beam 1', 'beam2'])
ax4.set_title('output')

plt.show()