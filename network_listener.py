#!/usr/bin/env python3

import ntcore
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def event_callback( event ):
    command_str = event.data.value.getString()
    print( 'Command Received: %s' % command_str )
    tokens=command_str.split(',')
    for token in tokens:
        key,token_value=token.split('=')
        print( '    token=%s value=%s' % (key,token_value) )

if __name__ == "__main__":
    inst = ntcore.NetworkTableInstance.getDefault()
    inst.startClient4('Test client')
    inst.setServerTeam(9999) # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
    table = inst.getTable("Bling")

    cmdSub = table.getStringTopic('command').subscribe('Uninitialized')

    inst.addListener( cmdSub, ntcore.EventFlags.kValueAll, event_callback )

    while True:
        time.sleep(1)

