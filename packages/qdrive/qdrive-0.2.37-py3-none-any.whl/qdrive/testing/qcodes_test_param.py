import qcodes as qc

from typing import Optional

import numpy as np

from qcodes.instrument.base import InstrumentBase
from qcodes.parameters import ArrayParameter, ManualParameter, MultiParameter, Parameter, ParameterWithSetpoints
from qcodes.instrument import DelegateParameter
from qcodes.tests.instrument_mocks import DummyInstrument
from qcodes.utils import validators

# TODO create test cases with qcodes parameters of various sizes and shapes

class MyCounter(Parameter):
    def __init__(self, name):
        super().__init__(name, label='Times this has been read',
                         vals=validators.Ints(min_value=0),
                         docstring='counts how many times get has been called '
                                   'but can be reset to any integer >= 0 by set')
        self._count = 0

    def get_raw(self):
        self._count += 1
        return self._count

    def set_raw(self, val):
        self._count = val
        return self._count

# dac = DummyInstrument('dac', gates=['ch1', 'ch2'])
# dac.ch2.set(1)
# my_delegate_param = DelegateParameter('my_delegated_parameter', dac.ch2, scale=1/1000, unit='mV')

class GeneratedSetPoints(Parameter):
    """
    A parameter that generates a setpoint array from start, stop and num points
    parameters.
    """

    def __init__(self, startparam, stopparam, numpointsparam, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._startparam = startparam
        self._stopparam = stopparam
        self._numpointsparam = numpointsparam

    def get_raw(self):
        return np.linspace(self._startparam(), self._stopparam(),
                              self._numpointsparam())

class DummyArray(ParameterWithSetpoints):

    def get_raw(self):
        npoints = self.root_instrument.n_points.get_latest()
        return np.random.rand(npoints)

from qcodes.instrument import Instrument
from qcodes.validators import Arrays, Numbers

class DummySpectrumAnalyzer(Instrument):

    def __init__(self, name, **kwargs):

        super().__init__(name, **kwargs)

        self.add_parameter('f_start',
                           initial_value=0,
                           unit='Hz',
                           label='f start',
                           vals=Numbers(0,1e3),
                           get_cmd=None,
                           set_cmd=None)

        self.add_parameter('f_stop',
				           initial_value=100,
                           unit='Hz',
                           label='f stop',
                           vals=Numbers(1,1e3),
                           get_cmd=None,
                           set_cmd=None)

        self.add_parameter('n_points',
                           unit='',
                           initial_value=10,
                           vals=Numbers(1,1e3),
                           get_cmd=None,
                           set_cmd=None)

        self.add_parameter('freq_axis',
                           unit='Hz',
                           label='Freq Axis',
                           parameter_class=GeneratedSetPoints,
                           startparam=self.f_start,
                           stopparam=self.f_stop,
                           numpointsparam=self.n_points,
                           vals=Arrays(shape=(self.n_points.get_latest,)))

        self.add_parameter('spectrum',
                   unit='dBm',
                   setpoints=(self.freq_axis,),
                   label='Spectrum',
                   parameter_class=DummyArray,
                   vals=Arrays(shape=(self.n_points.get_latest,)))


class Spectrum(ArrayParameter):
    def __init__(self, name, instrument):

        self.N = 7
        setpoints = (np.linspace(0, 1, self.N),)

        super().__init__(name=name,
                         instrument=instrument,
                         setpoints=setpoints,
                         shape=(self.N,),
                         label='Noisy spectrum',
                         unit='V/sqrt(Hz)',
                         setpoint_names=('Frequency',),
                         setpoint_labels=('Frequency',),
                         setpoint_units=('Hz',))

    def get_raw(self):
        return np.random.randn(self.N)

from qcodes.parameters import ManualParameter, MultiParameter

class SingleIQPair(MultiParameter):
    def __init__(self):
        # only name, names, and shapes are required
        # this version returns two scalars (shape = `()`)
        super().__init__('single_iq', names=('I', 'Q'), shapes=((), ()),
                         labels=('In phase amplitude', 'Quadrature amplitude'),
                         units=('V', 'V'),
                         # including these setpoints is unnecessary here, but
                         # if you have a parameter that returns a scalar alongside
                         # an array you can represent the scalar as an empty sequence.
                         setpoints=((), ()),
                         docstring='param that returns two single values, I and Q')
        self._scale_param = ManualParameter('scale', initial_value=2)

    def get_raw(self):
        scale_val = self._scale_param()
        return (scale_val, scale_val / 2)




class IQArray(MultiParameter):
    def __init__(self):
        # names, labels, and units are the same
        super().__init__('iq_array', names=('I', 'Q'), shapes=((5,), (5,)),
                         labels=('In phase amplitude', 'Quadrature amplitude'),
                         units=('V', 'V'),
                         # note that EACH item needs a sequence of setpoint arrays
                         # so a 1D item has its setpoints wrapped in a length-1 tuple
                         setpoints=(((0, 1, 2, 3, 4),), ((0, 1, 2, 3, 4),)),
                         setpoint_names=((("0, 1, 2, 3, 4"),), (("0, 1, 2, 3, 4"),)),
                         setpoint_labels=((("0, 1, 2, 3, 4"),), (("0, 1, 2, 3, 4"),)),
                         setpoint_units=((("0, 1, 2, 3, 4"),), (("0, 1, 2, 3, 4"),)),
                         docstring='param that returns two single values, I and Q')
        self._scale_param = ManualParameter('scale', initial_value=2)
        self._indices = np.array([0, 1, 2, 3, 4])

    def get_raw(self):
        scale_val = self._scale_param()
        return (self._indices * scale_val, self._indices * scale_val / 2)