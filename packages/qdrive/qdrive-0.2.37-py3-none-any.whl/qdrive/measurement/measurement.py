'''
Wrapper that allows for an interface that reproduces core tools behavior
'''
from qdrive.measurement.data_collector import data_collector, from_QCoDeS_parameter
from qdrive import dataset

from qcodes.utils.json_utils import NumpyJSONEncoder

import logging, json

logger = logging.getLogger(__name__)


class Measurement:
    def __init__(self, name, scope_name = None, silent=False):
        self.silent = silent

        self.ds = dataset.create(name, scope_name=scope_name)
        self.data_collector = data_collector(self.ds)
    
    def register_get_parameter(self, parameter, *setpoints):
        '''
        register parameters that you want to get in a measurement
        '''
        self.data_collector += from_QCoDeS_parameter(parameter, setpoints, self.data_collector)

    def add_snapshot(self, snapshot : dict):
        self.data_collector.set_attr('snapshot', json.dumps(snapshot, cls=NumpyJSONEncoder))
        
    def add_attribute(self, name : str, value):
        self.data_collector.set_attr(name, value)
    
    def add_attributes(self, attributes : dict):
        for name, value in attributes.items():
            self.add_attribute(name, value)
        
    def add_result(self, args):
        '''
        add results to the data_set

        Args:
            args : tuples of the parameter object submitted to the register parameter object and the get value.
        '''
        
        self.data_collector.add_data(args)
        
    def __enter__(self):
        if not self.silent:
            print(f'\nStarting measurement with uuid : {self.ds.uuid} - {self.ds.name}', flush=True)

        return self

    def  __exit__(self, exc_type, exc_value, exc_traceback):
        self.data_collector.complete()
            
        if exc_type is None:
            return True
        if exc_type == KeyboardInterrupt:
            print('\nMeasurement aborted with keyboard interrupt. Data has been saved.')
            return False

        return False