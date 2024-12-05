from qdrive.dataset.dataset import dataset
import numpy as np
import xarray as xr
import h5py

ds = dataset.create("my_test_dataset")

#####################################
# manually adding measurement files #
#####################################

# create hdf5 file
hf = h5py.File('data.h5', 'w')
hf.create_dataset('dataset_1', data=np.zeros([100,100]))

# add HDF5 file : 
ds["my_analysis"] = hf

# loading a hdf5 files (read only): #note that a file has to be netcdf4 compatible to be table to export it to xarray, pandas or netcdf
hdf5_file = ds['my_analysis'].hdf5
print(hdf5_file)


# example : add xarray dataset to dataset
temp = 15 + 8 * np.random.randn(2, 2, 3)
precip = 10 * np.random.rand(2, 2, 3)
lon = [[-99.83, -99.32], [-99.79, -99.23]]
lat = [[42.25, 42.21], [42.63, 42.59]]

xarray_ds = xr.Dataset({"Readout Signal fit (mV)": (["vP1 (mV)"], np.random.random(100)),},
    coords={ "vP1 (mV)":np.linspace(0,99,100)})

ds["my_analysis"] = xarray_ds
print(ds["my_analysis"].hdf5)
print(ds["my_analysis"].xarray)
print(ds["my_analysis"].netcdf4) #convert to netcdf4
print(ds["my_analysis"].pandas) #convert to pandas

# if you were to update your analysis you could add new version to it by : 
xarray_ds_2 = xr.Dataset({"Readout Signal fit (mV)": (["vP1 (mV)"], np.random.random(100)),},
    coords={ "vP1 (mV)":np.linspace(0,99,100)})
# for example :
ds['my_analysis'] = xarray_ds_2 # one of the formats outlined above.

# This generates two versions : 
print(f"file has the following versionss {ds['my_analysis'].versions}\nversion 0\n\n")
print(ds['my_analysis'].version(0).xarray)
print("\nversion 1\n\n")
print(ds['my_analysis'].version(1).xarray)
print("\nversion 2\n\n")
print(ds['my_analysis'].version(2).xarray)

#####################################
# creating json files               #
#####################################

# add json style parameters (standard response on assigning python data types)
ds['snapshot'] = {'paramn_name' : "somether_param"}
# modify and update of the snapshot file
ds['snapshot']['new_param'] = {'1235' : "685"}
print(ds['snapshot'])
ds['snapshot']['new_param']['1235'] = [1,2,3]
print(ds['snapshot'])
ds['snapshot']['new_param']['1235'] = 15
print(ds['snapshot'])

# when assigning like this, the file is not updated, but a new version is made 
ds['snapshot'] = "test"

print("version 0")
print(ds['snapshot'].version(0))
print("version 1")
print(ds['snapshot'].version(1))

# show files we have created until now
print(ds.files)

# utility functions (+ switch version):
ds["snapshot"].version(0)
for k,v in ds["snapshot"].items():
	print(k, v)
for k in ds["snapshot"].keys():
	print(k)
for v in ds["snapshot"].values():
	print(v)

# create another new version
ds["snapshot"] = [1,2,3,4,5]
for i in range(len(ds["snapshot"])):
	ds["snapshot"][i] = "blah"

##########################################
# adding raw numpy files to your dataset #
##########################################

# assign numpy array
ds['new_data'] = np.zeros([100,100])
numpy_array = ds['new_data'].raw #access raw numpy array
print(type(ds['new_data']))
print(type(numpy_array))

ds['new_data'] = np.ones([100,100]) #array gets now overwirtten 

# more options of providing numpy arrays
ds['new_data'] = [np.ones([100,100]), np.zeros([100,100])]
print(ds['new_data'].raw)
ds['new_data'] = { "x" : np.ones([100,100]),
				   "y" : np.zeros([100,100]),
				   "z" : np.zeros([100,100])}
print(ds['new_data'].raw["x"])

###################
# general utility #
###################

# supports iteration
for file in ds:
    print(file)

# export file to hard drive :
ds['new_data'].export("./", "my_filename.npz")

###############################
# data files :: edit at will! #
###############################

'''
In addition to creating new files, 
it is also possible to data to an existing one.

This can be done by making an additional group in the HDF5 file.

One could imagine this being handy if you want both analysis and raw data to reside in the same file.
Or if you have an analysis file and you just want to add things to it.
'''

# Example usage case : create normal data file, then augment with more data
xarray_ds = xr.Dataset({"Readout Signal fit (mV)": (["vP1 (mV)"], np.random.random(100)),},
    coords={ "vP1 (mV)":np.linspace(0,99,100)})

ds["meaurement"] = xarray_ds

# then add more to it : 
analysis_1 = xr.Dataset({"Power Spectra density (FFT base)": (["Frequency (Hz)"], np.random.random(100)),},
    coords={ "Frequency (Hz)":np.linspace(0,99,100)})
analysis_2 = xr.Dataset({"Power Spectra density (powel)": (["Frequency (Hz)"], np.random.random(100)),},
    coords={ "Frequency (Hz)":np.linspace(0,99,100)})

ds["meaurement"]["PSD (FFT)"] = analysis_1
ds["meaurement"]["PSD (POWEL)"] = analysis_2

print(ds["meaurement"].keys())
print(ds["meaurement"])

# get getting the data out : 
print(ds["meaurement"].xarray)
print(ds["meaurement"]["PSD (FFT)"].xarray)
print(ds["meaurement"]["PSD (FFT)"].pandas)

# note that calling hdf5/netcdf4 call do not give a different result as ds["analysis"], since they already suport 

'''
Note that structure is not yet officially supported by xarray, therefore some additional functionality is added to our libs

There is however already a beta of xarray stuff that supports groups (as it is part of the netcdf4 standard).
For now this method will have to do.

Irrgular datasets will also come in their own groups.
# TODO what to do with datasets that are non netcdf4 compliant -- how to check?
'''

################
# adding files #
################
# Add this file : 
ds["my_analysis_script"] = __file__ #some path of a file.
print(ds["my_analysis_script"])


######################
# Features to add    #
######################

# # easy expansion of datasets ?
# ds["my_data"].add_lineplot(name=name, x = np.random.random(20), x_name = "blah1", x_unit = "mV",
#                                       y = np.random.random(20), y_name = "blah2", y_unit = "mV",)
# ds["my_data"].add_heatmap(name=name, x = np.random.random(20),      x_name = "blah1", x_unit = "mV",
#                                      y = np.random.random(20),      y_name = "blah2", y_unit = "mV",
#                                      z = np.random.random([20,20]), z_name = "blah3", z_unit = "mV",)

