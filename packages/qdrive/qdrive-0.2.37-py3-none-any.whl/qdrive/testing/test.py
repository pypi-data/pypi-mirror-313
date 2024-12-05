from qdrive.measurement.dataset_core import dataset
import numpy as np
import xarray as xr
import h5py, netCDF4, os

ds = dataset.create("my_test_dataset")

#####################################
# manually adding measurement files #
#####################################
os.remove("data1.h5")

xarray_ds_2 = xr.Dataset({"Readout Signal fit (mV)": (["vP1 (mV)"], np.random.random(100)),},
    coords={ "vP1 (mV)":np.linspace(0,99,100)})
xarray_ds_2.to_netcdf('data1.h5')


rootgrp = netCDF4.Dataset('data1.h5', "a", format="NETCDF4")
key = rootgrp.createGroup("key")


lat = key.createDimension("time", 100)
lon = key.createDimension("level", 100)

times = key.createVariable("time","f8",("time",))
levels = key.createVariable("level","f8",("time",))

times[:] = np.random.random([100])
levels[:] = np.random.random([100])

rootgrp.close()

# test 2
xarray_ds_test = xr.Dataset({"Readout Signal fit (mV)": (["vP1 (mV)"], np.random.random(100)),},
    coords={ "vP1 (mV)":np.linspace(0,99,100)})
xarray_ds_test.to_netcdf('data.h5')

group_name = "test"

insert_file = h5py.File("data.h5",'r')
full_file   = h5py.File('data1.h5','a')



full_file.create_group(group_name)
grp = full_file[group_name]

for item in insert_file.keys():
	h5py.h5o.copy(insert_file.id, item.encode('utf-8'), grp.id, item.encode('utf-8'))

def list_groups:
	
print(full_file.keys())

insert_file.close()
full_file.close()

# ds = xr.open_dataset('data1.h5')
# ds2 = xr.open_dataset('data1.h5', group="key")
# ds3 = xr.open_dataset('data1.h5', group=group_name)
# print("\n\n")
# print(ds)
# print("\n\n\n\n")
# print(ds2)
# print("\n\n\n\n")
# print(ds3)

# # loading a hdf5 files (read only): #note that a file has to be netcdf4 compatible to be table to export it to xarray, pandas or netcdf
# hdf5_file = ds['my_analysis'].hdf5
# print(hdf5_file)

# if you were to update your analysis you could add new version to it by : 
# xarray_ds_2 = xr.Dataset({"Readout Signal fit (mV)": (["vP1 (mV)"], np.random.random(100)),},
#     coords={ "vP1 (mV)":np.linspace(0,99,100)})
# # for example :
# ds['my_analysis']["test_ds"] = xarray_ds_2 # one of the formats outlined above.

# print(ds["my_analysis"].xarray)