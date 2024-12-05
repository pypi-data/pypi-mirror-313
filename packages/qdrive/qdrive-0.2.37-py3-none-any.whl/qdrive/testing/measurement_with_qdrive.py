from qdrive.measurement.data_collector import data_collector, from_QCoDeS_parameter
from qdrive.dataset.dataset import dataset
from qdrive.testing.qcodes_test_param import MyCounter

from qcodes.tests.instrument_mocks import DummyInstrument

import time

dac = DummyInstrument('dac', gates=['ch1', 'ch2'])
param = MyCounter("counter")

name = '1D_test'

ds = dataset.create(name)

dc = data_collector(ds)

dc += from_QCoDeS_parameter(param, [dac.ch1], dc)

print(dc.h5_file.filename)
for i in range(50):
    dac.ch1.set(i)
    dc.add_data({param : param.get(), dac.ch1 : dac.ch1.get()})
    time.sleep(0.1)
    
dc.complete()
print(ds)