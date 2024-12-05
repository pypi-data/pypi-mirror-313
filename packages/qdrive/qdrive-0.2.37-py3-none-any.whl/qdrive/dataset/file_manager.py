from qdrive.dataset.files.utility import is_scalar, is_iterable

from qdrive.dataset.files.HDF5 import HDF5_file, xarray_dataset_attr_formatter_to_json, xarray_dataArray_attr_formatter_json
from qdrive.dataset.files.json import JSON_file
from qdrive.dataset.files.numpy import numpy_file, is_numpy_array, is_numpy_dict
from qdrive.dataset.files.file import file_file

from etiket_client.settings.folders import create_file_dir
from etiket_client.python_api.dataset_model.files import file_manager as file_manager_etiket,\
    file_object, FileType, generate_version_id, FileStatusLocal
import h5py, json, numpy, xarray, os, shutil, warnings, uuid, pathlib, h5netcdf.legacyapi as netcdf4, contextlib



# TODO add method to load csv files and save them as HDF5

class file_manager():
    def __init__(self, dataset, file_mgr_core : file_manager_etiket):
        self.ds = dataset
        self.file_obj = {}
        self.file_mgr_core = file_mgr_core
        
        for file in file_mgr_core.values():
            self.__load_file(file)
        
    def __getitem__(self, item):
        return self.file_obj[item]
        
    def __setitem__(self, item_name, value):
        self.ds._create_local()
        if item_name not in self.keys():
            
            fpath = create_file_dir(self.ds.scope.name, self.ds.uuid, uuid.uuid4(), generate_version_id())

            file_type = FileType.UNKNOWN
            generator = "unknown"
            if isinstance(value, numpy.ndarray) or is_numpy_dict(value) or is_numpy_array(value):
                fname = f'{item_name}.npz'
                destination = fpath + fname
                if isinstance(value, numpy.ndarray):
                    numpy.savez_compressed(destination, value)
                elif is_numpy_array(value):
                    numpy.savez_compressed(destination, *value)
                elif is_numpy_dict(value):
                    numpy.savez_compressed(destination, **value)
                file_type = FileType.NDARRAY
                generator = f"numpy.{numpy.__version__}"
            elif isinstance(value, pathlib.Path):
                if not value.exists():
                    raise ValueError(f"Path {value} does not exist.")
                fname =  os.path.basename(value)
                destination = fpath + fname
                
                if value.suffix in {".hdf5", ".h5", ".nc"}:
                    file_type = FileType.HDF5
                    with contextlib.suppress(Exception):
                        with netcdf4.Dataset(value):
                            file_type = FileType.HDF5_NETCDF
                if value.suffix == ".json":
                    with contextlib.suppress(Exception):
                        json.load(value.open())
                        file_type = FileType.JSON
                
                shutil.copyfile(value, destination)
            elif is_scalar(value) or is_iterable(value):
                fname = f'{item_name}.json'
                destination = fpath + fname
                with open(destination, "w") as outfile:
                    json.dump(value, outfile)
                file_type = FileType.JSON
                generator = f"json.{json.__version__}"
            elif isinstance(value, h5py.File):
                fname = f'{item_name}.hdf5'
                destination = fpath + fname
                
                ori_filename = (value.file.filename)
                value.file.close()
                shutil.copyfile(ori_filename, destination)
                file_type = FileType.HDF5
                generator = f"h5py.{h5py.__version__}"
            elif isinstance(value, (xarray.Dataset, xarray.DataArray)):
                fname = f'{item_name}.hdf5'
                destination = fpath + fname
                if isinstance(value, xarray.Dataset):
                    value = xarray_dataset_attr_formatter_to_json(value)
                elif isinstance(value, xarray.DataArray):
                    value = xarray_dataArray_attr_formatter_json(value)
                comp = {"zlib": True, "complevel": 3}
                encoding = {var: comp for var in list(value.data_vars)+list(value.coords)}
                value.to_netcdf(destination, engine='h5netcdf', invalid_netcdf=True, encoding=encoding)
                file_type = FileType.HDF5_NETCDF
                generator = f"xarray.{xarray.__version__}"
            else: 
                raise ValueError(f"Assignment of the type {type(value)} is not supported.")
            
            self._add_new_file(item_name, destination, file_type, generator)
        else:
            self.file_obj[item_name].update(value)
    
    def __load_file(self, file : file_object):
        if file.current.type is FileType.HDF5_NETCDF or file.current.type is FileType.HDF5_CACHE:
            file_modifier = HDF5_file(file)
        elif file.current.type is FileType.HDF5:
            file_modifier = HDF5_file(file)
        elif file.current.type is FileType.JSON:
            file_modifier = JSON_file(file)
        elif file.current.type is FileType.NDARRAY:
            file_modifier = numpy_file(file)
        elif file.current.type is FileType.TEXT:
            file_modifier = file_file(file)
        elif file.current.type is FileType.UNKNOWN:
            file_modifier = file_file(file)
        else:
            raise ValueError("Unrecognized file type. Contact support.")
        
        if file_modifier.name not in self.file_obj:
            self.file_obj[file.name] = file_modifier
        else:
            self.file_obj[file.name] += file_modifier
    
    def _add_new_file(self, name, file_path, file_type, generator, file_Status = FileStatusLocal.complete ):
        file = self.file_mgr_core.add_new_file(name, file_path, file_type, file_Status, generator)
        self.__load_file(file)
        if len(self.file_mgr_core) > 50:
            message = f"Many files are present in the dataset ({len(self.file_mgr_core)}). Is this necessary?"
            warnings.warn(message)

    def __len__(self):
        return len(self.file_obj)
    
    def __iter__(self):
        return iter(self.file_obj.values())
    
    def keys(self):
        return list(self.file_obj.keys())
