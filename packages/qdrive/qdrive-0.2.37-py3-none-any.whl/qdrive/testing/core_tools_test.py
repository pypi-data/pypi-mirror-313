from qdrive.measurement.data_collector import data_collector

from qcodes_test_param import MyCounter
from qcodes.tests.instrument_mocks import DummyInstrument
from qcodes.instrument import DelegateParameter

from qdrive.testing.qcodes_test_param import SingleIQPair, IQArray

from core_tools.data.measurement import Measurement
from core_tools.data.SQL.connect import SQL_conn_info_local, sample_info

IQ = IQArray()

SQL_conn_info_local("localhost", 5432, 'stephan',
                        '', 'core_tools', False)
sample_info("test", "test", "test")

dac = DummyInstrument('dac', gates=['ch1', 'ch2'])
dac.ch2.set(1)
my_delegate_param = DelegateParameter('my_delegated_parameter', dac.ch2, scale=1/1000, unit='mV')

param = MyCounter("counter")

param = IQ
meas = Measurement("test_measurement")
meas.register_set_parameter(dac.ch2, 50)
meas.register_set_parameter(dac.ch1, 50)
meas.register_get_parameter(param, dac.ch1, dac.ch2)

with meas as m:
	for i in range(50):
		for j in range(50):
			dac.ch1.set(j/10)
			dac.ch2.set(i/10)
			meas.add_result((param, param.get()), (dac.ch2, dac.ch2.get()),  (dac.ch1, dac.ch1.get()))

print(meas)
# print(meas.ds)
# print(meas.ds.files)

# print(meas.ds["snapshot"])
# print(meas.ds["Measurement"])

# from qdrive.measurement.core_tools.sweeps.sweeps import do1D

# data = do1D(dac.ch1, 0,100,50,0, param, name="test ds")

# from qdrive.measurement.core_tools.sweeps.scans import Scan, Getter, sweep
# import numpy as np

# s = sweep(dac.ch1, np.linspace(0,50,100))
# g = Getter(param)

# data = Scan(s,g, name = "scan function test")
# print(data)