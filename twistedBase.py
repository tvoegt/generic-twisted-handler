##############################
# Base class for Client and Server Protocols
##############################

from twisted.protocols.basic import LineReceiver

class TwistedBase( LineReceiver ):
    ''' Twisted Base Clasee for Client and Server Protocols '''

    def __init__( self, factory, eventHandler ):
        ''' init func for Twisted Base
        Inputs:
            factory: FactoryClass: twisted protocol factory class
            eventHandler: dict: dict that maps all events on Protocol Factory to a function
        '''
        self.factory = factory
        self.eventHandler = eventHandler