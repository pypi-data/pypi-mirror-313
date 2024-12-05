from etiket_client.sync.backends.quantify.live_sync import XArrayReplicator, check_live_dataset
from etiket_client.sync.base.sync_source_abstract import SyncSourceDatabaseBase, SyncSourceFileBase
from etiket_client.sync.base.sync_utilities import file_info, sync_utilities,\
    dataset_info, sync_item
from etiket_client.remote.endpoints.models.types import FileType
from etiket_client.sync.backends.quantify.quantify_config_class import QuantifyConfigData

from datetime import datetime, timedelta

import os, pathlib, xarray, re, typing

class QuantifySync(SyncSourceFileBase):
    SyncAgentName = "Quantify"
    ConfigDataClass = QuantifyConfigData
    MapToASingleScope = True
    LiveSyncImplemented = True
    level = 2
    
    @staticmethod
    def rootPath(configData: QuantifyConfigData) -> pathlib.Path:
        return pathlib.Path(configData.quantify_directory)

    @staticmethod
    def checkLiveDataset(configData: QuantifyConfigData, syncIdentifier: sync_item, maxPriority: bool) -> bool:
        if not maxPriority:
            return False
        
        # check the last time the file is modified:
        dir_content = os.listdir(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier))
        m_files = [content for content in dir_content if content.endswith(".hdf5") or content.endswith(".h5")]
        
        if len(m_files) == 0:
            return False

        m_file = max(m_files, key=lambda f: os.path.getmtime(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, f)))
        path = os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, m_file)
        mod_time = pathlib.Path(path).stat().st_mtime
        return datetime.now() - datetime.fromtimestamp(mod_time) < timedelta(minutes=2)
    
    @staticmethod
    def syncDatasetNormal(configData: QuantifyConfigData, syncIdentifier: sync_item):
        create_ds_from_quantify(configData, syncIdentifier, False)
        dataset_path = pathlib.Path(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier))
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if not (file.endswith(".hdf5") or file.endswith(".h5")):
                    name, file_path = process_file_name(root, file, dataset_path)
                    if name is None:
                        continue

                    f_type = FileType.UNKNOWN
                    if file.endswith(".json"):
                        f_type = FileType.JSON
                    if file.endswith(".txt"):
                        f_type = FileType.TEXT
                        
                    f_info = file_info(name = name, fileName = file,
                        created = datetime.fromtimestamp(pathlib.Path(os.path.join(root, file)).stat().st_mtime),
                        fileType = f_type, file_generator = "Quantify")
                    
                    sync_utilities.upload_file(file_path, syncIdentifier, f_info)

        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.endswith(".hdf5") or file.endswith(".h5"):
                    name, file_path = process_file_name(root, file, dataset_path)
                    if name is None:
                        continue
                
                    if check_live_dataset(file_path):
                        replicator = XArrayReplicator(name, file_path, syncIdentifier.datasetUUID)
                        replicator.sync()
                    else:
                        f_info = file_info(name = name, fileName = file,
                                            created = datetime.fromtimestamp(pathlib.Path(os.path.join(root, file)).stat().st_mtime),
                                            fileType = FileType.HDF5_NETCDF, file_generator = "Quantify")
                        ds = xarray.load_dataset(file_path, engine='h5netcdf')
                        
                        # check if fields in the datasets are standard deviations and mark them as such -- this is useful for plotting
                        data_vars = list(ds)
                        for var_name in data_vars:
                            if var_name.endswith("_u") and var_name[:-2] in data_vars:
                                ds[var_name[:-2]].attrs['__std'] = var_name
                                ds[var_name].attrs['__is_std'] = 1
                                                    
                        sync_utilities.upload_xarray(ds, syncIdentifier, f_info)
                    
    
    @staticmethod
    def syncDatasetLive(configData: QuantifyConfigData, syncIdentifier: sync_item):
        # there is a live check in the normal sync, so we can just call that.
        QuantifySync.syncDatasetNormal(configData, syncIdentifier)


def process_file_name(file_dir : str, file_name : str, dataset_path : str) -> typing.Tuple[str, pathlib.Path]:
    if file_name.startswith("."):
        return None, None

    relative_path = os.path.relpath(os.path.join(file_dir, file_name), start=dataset_path)
    name_parts = [re.sub(r"\d{8}-\d{6}-\d{3}-[a-z0-9]{6}-", "", part)
                  for part in pathlib.Path(relative_path).parts]
    reformatted_file_name = ".".join(name_parts)
    file_path = pathlib.Path(os.path.join(file_dir, file_name))
    return reformatted_file_name, file_path

def create_ds_from_quantify(configData: QuantifyConfigData, syncIdentifier: sync_item, live : bool):
    tuid = syncIdentifier.dataIdentifier.split('/')[1][:26]
    name = syncIdentifier.dataIdentifier.split('/')[1][27:]
    created = datetime.strptime(tuid[:18], "%Y%m%d-%H%M%S-%f")
    
    # get variable names in the dataset, this is handy for searching!
    keywords = set()
    
    # loop through all datasets in the folder os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier) (not recursive) and get the keywords
    for file in os.listdir(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier)):
        try:
            if file.endswith(".hdf5") or file.endswith(".h5"):
                with xarray.load_dataset(os.path.join(configData.quantify_directory, syncIdentifier.dataIdentifier, file), engine='h5netcdf') as xr_ds:
                    for key in xr_ds.keys():
                        if 'long_name' in xr_ds[key].attrs.keys():
                            keywords.add(xr_ds[key].attrs['long_name'])
                            continue
                        if 'name' in xr_ds[key].attrs.keys():
                            keywords.add(xr_ds[key].attrs['name'])

                    for key in xr_ds.coords:
                        if 'long_name' in xr_ds[key].attrs.keys():
                            keywords.add(xr_ds[key].attrs['long_name'])
                            continue
                        if 'name' in xr_ds[key].attrs.keys():
                            keywords.add(xr_ds[key].attrs['name'])  
        except Exception as e:
            print(f"Error loading dataset: {e}")
    
    ds_info = dataset_info(name = name, datasetUUID = syncIdentifier.datasetUUID,
                alt_uid = tuid, scopeUUID = syncIdentifier.scopeUUID,
                created = created, keywords = list(keywords), 
                attributes = {"set-up" : configData.set_up})
    sync_utilities.create_ds(live, syncIdentifier, ds_info)
    