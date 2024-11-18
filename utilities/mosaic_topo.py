#!/usr/bin/env python3

from yaml import safe_load, load, dump
from netCDF4 import Dataset
import numpy as np
from scipy.io import FortranFile
import argparse


def parse_args():
    p = argparse.ArgumentParser(description='Flatten a lat-lon to 1D')
    p.add_argument('-i','--input',type=str,help='input file',default=None)
    p.add_argument('-o','--output',type=str,help='output file',default=None)
    p.add_argument('-c','--csize',type=str,help='cube size',default=None)
    return vars(p.parse_args())

comm_args    = parse_args()
binfile   = comm_args['input']
Output_prefix = comm_args['output']

f = FortranFile(binfile,'r')
rec = f.read_reals(dtype=np.float32)

im=int(comm_args['csize'])
topo=np.zeros([6,im,im])

icnt=0
for n in range(6):
    for j in range(im):
        for i in range(im):
           topo[n,j,i]=rec[icnt]
           icnt=icnt+1

for n in range(6):
   output_file=Output_prefix+".tile"+str(n+1)+".nc"
   ncfid=Dataset(output_file,mode='w',format='NETCDF4')

   xdim=ncfid.createDimension('nx',im)
   ydim=ncfid.createDimension('ny',im)

   orog = ncfid.createVariable('orog_filt','f4',('nx','ny'))
   mask = ncfid.createVariable('land_frac','f4',('nx','ny'))
   orog[:,:]=topo[n,:,:]
   #orog[:,:]=topo[n,:,:]*9.80665
   mask[:,:]=1
   ncfid.close()


