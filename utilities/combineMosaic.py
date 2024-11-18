#!/usr/bin/env python3

#-------------
# Load modules
#-------------
from netCDF4 import Dataset
import numpy  as np
import argparse

def parse_args():
    p = argparse.ArgumentParser(description='Flatten a lat-lon to 1D')
    p.add_argument('-i','--input',type=str,help='input file',default=None)
    p.add_argument('-o','--output',type=str,help='output file',default=None)
    return vars(p.parse_args())

#------------------
# Opening the file
#------------------
comm_args    = parse_args()
Input_prefix   = comm_args['input']
Output_file  = comm_args['output']

#---------------------
# Extracting variables
#---------------------


input_file=Input_prefix+".tile"+str(1)+".nc"
ncFid=Dataset(input_file,mode='r')
cRes = len(ncFid.dimensions['nx'])
ncFid.close()

fout = Dataset(Output_file,mode='w', format='NETCDF4')
ncol = fout.createDimension('ncol',cRes*cRes*6)
orog = fout.createVariable('PHIS','f8',('ncol'))

orog_np = np.zeros([6,cRes,cRes],dtype=np.double)

for i in range(6):
   input_file=Input_prefix+".tile"+str(i+1)+".nc"
   ncFid=Dataset(input_file,mode='r')

   temp=ncFid.variables['orog_filt'][:]
   orog_np[i,:,:]=temp

   ncFid.close()

orog_1d = np.reshape(orog_np,cRes*cRes*6)
orog[:]=orog_1d
fout.close()


