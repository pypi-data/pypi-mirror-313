from etiket_client.python_api.dataset_model.dataset import dataset_model
from etiket_client.python_api.dataset import dataset_read_raw, dataset_create_raw, DatasetCreate
from etiket_client.python_api.scopes import get_scopes
from etiket_client.python_api.dataset_model.files import FileStatusLocal

from etiket_client.settings.user_settings import user_settings

from qdrive.dataset.file_manager import file_manager
from qdrive.dataset.files.file_mgr_single import file_mgr_single

import uuid, datetime, typing


class dataset(dataset_model):
    def __init__(self, ds_uuid : 'uuid.UUID | str', scope : "uuid.UUID | str | None" = None):
        '''
        Initialize a dataset instance.

        Args:
            ds_uuid (uuid.UUID | str): The UUID of the dataset.
            scope (uuid.UUID | str, optional): The scope UUID or name. Defaults to None.
        '''
        if scope is not None:
            scope_uuid = get_scope_uuid(scope)
        else:
            scope_uuid = None
        l_ds, r_ds = dataset_read_raw(ds_uuid, scope_uuid=scope_uuid)
        super().__init__(l_ds, r_ds, user_settings.verbose)
        self.__files = file_manager(self, self.files)
    
    @classmethod
    def init_raw(cls, local_ds, remote_ds):
        '''
        Initialize a dataset instance from raw local and remote datasets.
        Used for internal purposes only.

        Args:
            local_ds: The local dataset object.
            remote_ds: The remote dataset object.

        Returns:
            dataset: An instance of the dataset class.
        '''
        ds = cls.__new__(cls)
        super(cls, ds).__init__(local_ds, remote_ds, user_settings.verbose)
        ds.__files = file_manager(ds, ds.files)
        return ds

    @classmethod
    def create(cls, name : str,
                    description  : typing.Optional[str] = None,
                    scope_name : typing.Optional[str] = None,
                    alt_uid : typing.Optional[str] = None) -> 'dataset':
        '''
        Create a new dataset.

        Args:
            name (str): The name of the dataset.
            description (str, optional): Description of the dataset.
            scope_name (str, optional): The name of the scope.
            alt_uid: Alternative user ID.

        Raises:
            ValueError: If no scope is provided and no default scope is set.
            ValueError: If the specified scope does not exist.

        Returns:
            dataset: An instance of the newly created dataset.
        '''
        if scope_name is None:
            user_settings.load()
            if user_settings.current_scope is None:
                raise ValueError("No scope provided and no default scope set. Please provide a scope.")
            scope_uuid=uuid.UUID(user_settings.current_scope)
        else:
            scope_uuid = None
            scopes = get_scopes()
            for scope in scopes:
                if scope.name == scope_name:
                    scope_uuid = scope.uuid
            if scope_uuid is None:
                raise ValueError(f"Scope '{scope_name}' does not exist ): .")
        
        datasetCreate = DatasetCreate(uuid=uuid.uuid4(), collected=datetime.datetime.now(),
                                      name=name, creator=user_settings.user_sub, alt_uid=alt_uid,
                                      description=description, keywords=[],
                                      ranking= 0, synchronized=False,
                                      scope_uuid=scope_uuid)
        l_ds = dataset_create_raw(datasetCreate)
        ds = cls.__new__(cls)
        super(cls, ds).__init__(l_ds, None, user_settings.verbose)
        ds.__files = file_manager(ds, ds.files)
        return ds
    
    def __iter__(self):
        return iter(self.__files)
        
    def __getitem__(self, item) -> typing.Type[file_mgr_single]:
        return self.__files[item]
    
    def __setitem__(self, item, value):
        self.__files[item] = value
    
    def add_new_file(self,name, destination, file_type, generator, status = FileStatusLocal.complete):
        self.__files._add_new_file(name, destination, file_type, generator, status)
    
def get_scope_uuid(scope_like_input : 'uuid.UUID | str'):
    if isinstance(scope_like_input, uuid.UUID):
        return scope_like_input
    elif isinstance(scope_like_input, str):
        scopes = get_scopes()
        for scope in scopes:
            if scope.name == scope_like_input:
                return scope.uuid
            if str(scope.uuid) == scope_like_input:
                return scope.uuid
        raise ValueError(f"Scope '{scope_like_input}' does not exist ): .")
    else:
        raise ValueError(f"Scope '{scope_like_input}' is not a valid input type. Please provide a scope name or uuid.")
