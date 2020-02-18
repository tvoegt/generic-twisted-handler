####################
# CLIENT BASE FACTORY
####################

from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twistedBase import TwistedBase
from twistedUtils import buildMessage
from const import BASE_PORT, BASE_HOST, EVENT_HANDLER_CLIENT, EnvMapping, EventTypes
import json

class ClientBase( TwistedBase ):
    ''' Generic Client Protocol '''

    def lineReceived( self, data ):
        ''' Handler for when Server receives message
        Inputs:
            data: json: message given in json format
        '''
        msg = json.loads( data )
        if isinstance( msg, bytes ):
            msg = msg.decode( 'ascii' )
        eventType = msg.get( EnvMapping.EVENT.value )
        self.handleEvent( eventType, msg )

    def handleEvent( self, event, data ):
        ''' Return the function that handles the event 
        Inputs: 
            event: str: event type to handle
        Returns:
            eventFunc: Function: function that handles the event
        '''
        eventFuncStr = self.eventHandler.get( event, '' )
        if hasattr( self, eventFuncStr ):
            eventFunc = getattr( self, eventFuncStr )
            return eventFunc( data )
        else:
            return None

    def onIndentify( self, kwargs ):
        ''' When asked to identiy yourself, return your type  '''
        msg = buildMessage( EventTypes.IDENTIFY.value,
                            kwargs = { EnvMapping.CLIENT_TYPE.value: self.factory.type }                          
                          )
        self.doSendLine( msg )

    def doSendLine( self, msg ):
        msg = json.dumps( msg ).encode( 'ascii', 'ignore' )
        self.sendLine( msg )
        
    def onRegistration( self, kwargs ):
        ''' Handles REGISRATION event on the client 
            Registers the client with after server acknowledges conneciton 
        '''
        self.factory.registered = True
        print( '{} is now registered'.format( self.factory.type ) )
        msg = buildMessage( EventTypes.REGISTERED.value )
        self.doSendLine( msg )

class ClientBaseFactory( Factory ):
    ''' Generic client factory '''

    def __init__( self ):
        self.type = 'BASE'
        self.registered = False

    def buildProtocol( self, addr ):
        return ClientBase( factory = self, eventHandler = EVENT_HANDLER_CLIENT )

    def clientConnectionFailed( self, connector, reason ):
        # todo add in better handling
        print( 'Connection Failed' )
        reactor.stop()

    def clientConnectionLost( self, connector, reason ):
        # todo add in better handling
        print( 'Connection Lost' )
        reactor.stop()

    def startedConnecting(self, connector):
        print ('Started to connect.')

reactor.connectTCP( BASE_HOST, BASE_PORT, ClientBaseFactory() )
reactor.run()
