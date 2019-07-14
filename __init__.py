import time

from modules.core.props import Property, StepProperty
from modules.core.step import StepBase
from modules import cbpi

@cbpi.step
class KettleVolumeStep(StepBase):
    '''
    Just put the decorator @cbpi.step on top of a method. The class name must be unique in the system
    '''
    # Properties
    temp = Property.Number("Temperature", configurable=True)
    kettle = StepProperty.Kettle("Kettle")
    timer = Property.Number("Timer in Minutes", configurable=True)
    sensor = StepProperty.Sensor("Sensor")
    volume = Property.Number("Volume", configurable=True)

    def init(self):
        '''
        Initialize Step. This method is called once at the beginning of the step
        :return: 
        '''
        # set target tep
        #self.set_target_temp(self.temp, self.kettle)

    def finish(self):
        self.set_target_temp(0, self.kettle)

    def execute(self):
        '''
        This method is execute in an interval
        :return: 
        '''
        for key, value in cbpi.cache.get("sensors").iteritems():
            if key == int(self.sensor):
                sensorValue = value.instance.last_value

        # Check if timer finished and go to next step
        if float(sensorValue) <= float(self.volume):
            self.set_target_temp(self.temp, self.kettle)
            if self.is_timer_finished() is None:
                self.start_timer(int(self.timer) * 60)
            
        if self.is_timer_finished() == True:
            self.notify("Mash-in Complete!", "Starting the next step.", timeout=None)
            self.next()