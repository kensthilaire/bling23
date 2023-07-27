#!/usr/bin/env python3

import argparse
import ntcore
import time
import logging

from enum import Enum, auto

from joystick import Joystick
from lidar import Lidar

logging.basicConfig(level=logging.INFO)

class LidarStates(Enum):
    INITIAL = auto()
    ACQUIRING = auto()
    ACQUIRED = auto()
    FOLLOWING = auto()
    TERMINATING = auto()

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
        self.lidar_state = LidarStates.INITIAL
        

    def joystick_control(self):
        for event in self.gamepad.read_loop():
            decoded_event = self.decode_event( event )
            if decoded_event['type'] == 'BUTTON' or decoded_event['type'] == 'AXIS':
                publisher = self.publishers.get(decoded_event['name'], None)
                if publisher:
                    publisher.set( decoded_event['value'] )

    def set_lidar_state(self,new_state):
        curr_state = self.lidar_state
        print( 'State Transition From %s to %s' % (curr_state.name, new_state.name) )
        if new_state == LidarStates.ACQUIRING:
            pass
        elif new_state == LidarStates.ACQUIRED:
            if self.follow_distance != 0:
                self.lidar.cancel()

        self.lidar_state = new_state

    def lidar_align(self, scan_data):
        #
        # in order to align the robot to the closest object, we will use the 'RightJoystickX' controller
        # to turn the robot left or right until the closest object is centered in the capture zone
        #
        publisher = self.publishers.get('RightJoystickX', None)

        turning_speed = 0.0
        if scan_data.get('valid', False)==True:
            if publisher:
                angle = scan_data['angle']
                if angle < 5 or angle > 355:
                    turning_speed = 0.0

                    # if the lidar is acquiring the target, then
                    # transition to the acquired state and wait 
                    # for further command
                    if self.lidar_state == LidarStates.ACQUIRING:
                        self.set_lidar_state( LidarStates.ACQUIRED )
                        
                elif angle < 20 or angle > 340:
                    turning_speed = 0.2
                elif angle < 90 or angle > 270:
                    turning_speed = 0.4
                else:
                    turning_speed = 0.6
                
                # if the angle is greater than 180, then we will turn to the left
                if angle > 180:
                    turning_speed *= -1.0

        print( 'Setting turning speed to %0.1f' % turning_speed )
        publisher.set( turning_speed )

    #
    # This function will instruct the robot to follow the closest object in the capture zone, maintaining 
    # alignment on that closest object and a minimum distance from the object.
    #
    def lidar_follow(self, scan_data):

        self.lidar_align( scan_data )

        publisher = self.publishers.get('LeftJoystickY', None)

        moving_speed = 0.0
        if scan_data.get('valid', False)==True:
            if publisher:
                distance = scan_data['distance']
                if distance <= self.follow_distance: 
                    moving_speed = 0.0
                elif distance < self.follow_distance + 12:
                    moving_speed = 0.2
                elif distance < self.follow_distance + 24:
                    moving_speed = 0.4
                else:
                    moving_speed = 0.6
                
        print( 'Setting moving speed to %0.1f' % moving_speed )
        publisher.set( moving_speed )

    #
    # Send commands to halt any movememnt of the robot
    #
    def lidar_halt(self):
        self.publishers.get('LeftJoystickY', None).set(0.0)
        self.publishers.get('RightJoystickX', None).set(0.0)


    def lidar_control(self, port='/dev/ttyUSB0', capture_distance=48, capture_zone='0-45,315-359', follow_distance=None):
        if self.lidar == None:
            self.lidar = Lidar(port)

        self.capture_distance = capture_distance
        self.follow_distance = follow_distance
        self.lidar.build_ranges(capture_zone)

        self.set_lidar_state( LidarStates.ACQUIRING )
        self.lidar.closest_in_range(ranges=None, min_distance=capture_distance, sample_interval=0.05, callback=self.lidar_align)

        if self.follow_distance != 0:
            self.set_lidar_state( LidarStates.FOLLOWING )
            self.lidar.closest_in_range(ranges=None, min_distance=self.lidar.MAX_DISTANCE, sample_interval=0.05, callback=self.lidar_follow)

        self.lidar_halt()
        self.set_lidar_state( LidarStates.TERMINATING )

if __name__ == '__main__':

    #
    # parse out the command arguments
    #
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', dest='debug', default=False)
    parser.add_argument('-j', '--joystick', action='store_true', dest='joystick', default=False)
    parser.add_argument('-l', '--lidar', action='store_true', dest='lidar', default=False)
    parser.add_argument('-c', '--capture_distance', action='store', dest='capture_distance', default='42')
    parser.add_argument('-f', '--follow_distance', action='store', dest='follow_distance', default=0)
    parser.add_argument('-r', '--range', action='store', dest='range', default='0-45,315-359')
    parser.add_argument('-p', '--port', action='store', dest='port', default='/dev/ttyUSB0')
    options = parser.parse_args()

    controller = FrcController(team_number=9999)

    try:
        if options.joystick:
            controller.joystick_control()
        elif options.lidar:
            controller.lidar_control( port=options.port,
                                      capture_zone=options.range, 
                                      capture_distance=int(options.capture_distance),
                                      follow_distance=int(options.follow_distance) )

    except KeyboardInterrupt:
        if controller.lidar:
            print( 'Terminating LIDAR Session' )
            controller.lidar.cancel()

    if controller.lidar:
        print( 'Shutting down LIDAR' )
        controller.lidar.terminate()

