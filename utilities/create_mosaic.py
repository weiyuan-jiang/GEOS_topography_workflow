#!/usr/bin/env python3

from netCDF4 import Dataset
from netCDF4 import stringtochar
import numpy as np
import argparse


def parse_args():
   p = argparse.ArgumentParser(description='Flatten a lat-lon to 1D')
   p.add_argument('-r','--res',type=str,help='input file',default=None)
   p.add_argument('-o','--output',type=str,help='output file',default=None)
   return vars(p.parse_args())

comm_args    = parse_args()
res   = comm_args['res']
output_file  = comm_args['output']

ncfid=Dataset(output_file,mode='w',format='NETCDF4')
strdim=ncfid.createDimension('string',255)
tiledim=ncfid.createDimension('ntiles',6)
nxdim=ncfid.createDimension('nx',1120)
nydim=ncfid.createDimension('ny',1120)
gridfiles = ncfid.createVariable('gridfiles','S1',('ntiles','string'))
prefix = "C"+res+"_grid.tile"

datain = np.array([prefix+"1.nc",prefix+"2.nc",prefix+"3.nc",prefix+"4.nc",prefix+"5.nc",prefix+"6.nc"],dtype='S255')

gridfiles[:] = stringtochar(datain)


ncfid.close()


