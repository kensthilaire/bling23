#!/usr/bin/env python3

import ntcore
import time
import logging

from joystick import Joystick

logging.basicConfig(level=logging.DEBUG)

class FrcController( Joystick ):
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

    def read(self):
        for event in self.gamepad.read_loop():
            decoded_event = self.decode_event( event )
            if decoded_event['type'] == 'BUTTON' or decoded_event['type'] == 'AXIS':
                publisher = self.publishers.get(decoded_event['name'], None)
                if publisher:
                    publisher.set( decoded_event['value'] )

if __name__ == '__main__':

    controller = FrcController(team_number=9999)

    try:
        controller.read()
    except KeyboardInterrupt:
        print( 'Terminating Joystick Session' )


