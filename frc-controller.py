#!/usr/bin/env python3

import argparse
import ntcore
import time
import logging

from joystick import Joystick
from lidar import Lidar

logging.basicConfig(level=logging.INFO)

class FrcController(Joystick):
    def __init__(self, path=None, team_number=9999):
        super().__init__(path)

        self.inst = ntcore.NetworkTableInstance.getDefault()
        self.inst.startClient4('Test client')
        self.inst.setServerTeam(team_number) 

        self.table = self.inst.getTable("RobotRemoteControl")
        self.publishers = {}
        for button in list(self.BUTTONS.values()):
            self.publishers[button['name']] = self.table.getIntegerTopic(button['name']).publish()
        for axis in list(self.AXIS_TYPES.values()):
            self.publishers[axis['name']] = self.table.getDoubleTopic(axis['name']).publish()

        self.lidar = None
        

    def joystick_control(self):
        for event in self.gamepad.read_loop():
            decoded_event = self.decode_event( event )
            if decoded_event['type'] == 'BUTTON' or decoded_event['type'] == 'AXIS':
                publisher = self.publishers.get(decoded_event['name'], None)
                if publisher:
                    publisher.set( decoded_event['value'] )

    def lidar_align(self, scan_data):
        #
        # in order to align the robot to the closest object, we will use the 'RightJoystickX' controller
        # to turn the robot left or right until the closest object is centered in the capture zone
        #
        publisher = self.publishers.get('RightJoystickX', None)

        speed = 0.0
        if scan_data.get('valid', False)==True:
            if publisher:
                angle = scan_data['angle']
                if angle < 5 or angle > 355:
                    speed = 0.0
                elif angle < 20 or angle > 340:
                    speed = 0.2
                elif angle < 90 or angle > 270:
                    speed = 0.4
                else:
                    speed = 0.6
                
                # if the angle is greater than 180, then we will turn to the left
                if angle > 180:
                    speed *= -1.0

        print( 'Setting speed to %0.1f' % speed )
        publisher.set( speed )

    def lidar_control(self, port='/dev/ttyUSB0', capture_distance=48, capture_zone='0-45,315-359', min_distance=24):
        if self.lidar == None:
            self.lidar = Lidar(port)

        self.lidar.build_ranges(capture_zone)
        self.lidar.closest_in_range(ranges=None, min_distance=capture_distance, sample_interval=0.05, callback=self.lidar_align)

if __name__ == '__main__':

    #
    # parse out the command arguments
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', dest='debug', default=False)
    parser.add_argument('-j', '--joystick', action='store_true', dest='joystick', default=False)
    parser.add_argument('-l', '--lidar', action='store_true', dest='lidar', default=False)
    parser.add_argument('-d', '--distance', action='store', dest='distance', default='42')
    parser.add_argument('-r', '--range', action='store', dest='range', default='0-359')
    parser.add_argument('-p', '--port', action='store', dest='port', default='/dev/ttyUSB0')
    options = parser.parse_args()

    controller = FrcController(team_number=9999)

    try:
        if options.joystick:
            controller.joystick_control()
        elif options.lidar:
            controller.lidar_control( port=options.port, capture_zone=options.range, capture_distance=int(options.distance) )

    except KeyboardInterrupt:
        if controller.lidar:
            print( 'Terminating LIDAR Session' )
            controller.lidar.cancel()

    if controller.lidar:
        print( 'Shutting down LIDAR' )
        controller.lidar.terminate()

