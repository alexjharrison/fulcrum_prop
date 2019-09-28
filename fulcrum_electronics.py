from adafruit_bno055 import BNO055
from adafruit_pca9685 import PCA9685
import statistics
from time import sleep
import time

class Sensor(BNO055):
    def __init__(self, i2c):
        super().__init__(i2c)
        self.calibratedAngle = 0
        
        
    def calibrate(self, sampleFreq:float):
        print('CALIBRATION: Let rod hang down, perpendicular to the floor')
        input('Press return to continue...')
        print('CALIBRATION: Now calibrating BNO055 IMU - Angle Sensor')
        timedCalibration = 0
        t0 = time.time()
        angleList = []
        while timedCalibration < 5:
            angleList.append(self.euler[2])
            sleep(sampleFreq)
            timedCalibration = time.time() - t0
        avgAngle = statistics.mean(angleList)
        self.calibratedAngle = 0 - avgAngle
        print('Average sensed angle was: {}'.format(avgAngle))
        print('Now put back in safety position.')
        input('Press return to continue...')
        pass
    
    def sensedAngle(self):
        return self.euler[2] + self.calibratedAngle
    
    def sensedRate(self):
        return self.euler[3]

class MotorController(PCA9685):
    def __init__(self, i2c, motorChannel:int, pwmFrequency:int):
        super().__init__(i2c)
        self.motorChannel = motorChannel
        self.frequency = pwmFrequency
        
        
    def startup(self, sampleFreq:float, startupValue:int):
        for x in range(100):
            value = round(x/100 * startupValue)
            self.channels[self.motorChannel].duty_cycle = value
            print(value)
            sleep(sampleFreq)
        while True:
            self.channels[self.motorChannel].duty_cycle = startupValue
            sleep(sampleFreq)

    def setThrottle(self, value:int):
        self.channels[self.motorChannel].duty_cycle = value

    def setThrottleRange(self):
        print('SET THROTTLE RANGE: ESC must be de-energized.')
        upperValue = input('SET THROTTLE RANGE: Enter upper value: ')
        self.setThrottle(int(upperValue))
        input('SET THROTTLE RANGE: Now energize the ESC and wait for beep.')
        lowerValue = input('SET THROTTLE RANGE: Enter lower value: ')
        self.setThrottle(int(lowerValue))
        

            