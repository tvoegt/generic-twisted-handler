###########################
# SERVER BASE FACTORY
###########################

from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Factory 
from twistedBase import TwistedBase
from const import EventTypes, EnvMapping, EVENT_HANDLER_SERVER, BASE_PORT
from twistedUtils import buildMessage
import json 

class ServerBase( TwistedBase ):
    ''' Server Base Protocol Handler '''

    def __init__( self, factory, eventHandler ):
        '''Init func to the Server Base class
        Inputs:
            factory: FactoryClass: twisted protocol factory class
            eventHandler: dict: dict that maps all events to server side funcs 
         '''
        super( ServerBase, self ).__init__( factory, eventHandler )
        self.clientName = None
        self.state = EnvMapping.UNREGISTERED_STATE.value

    def connectionMade( self ):
        ''' Handler for initial client connection to server '''
        print( '>>> Server has received connection request | Identifying' )
        msg = dict( { EnvMapping.EVENT.value: EventTypes.IDENTIFY.value } )
        self.doSendLine( msg )

    def handleEvent( self, event, data ):
        ''' Return the function that handles the event 
        Inputs: 
            event: str: event type to handle
            data: dict: data to be passed onto the event 
        Returns:
            eventFunc: Function: function that handles the event
        '''
        eventFuncStr = self.eventHandler.get( event, '' )
        if hasattr( self, eventFuncStr ):
            eventFunc = getattr( self, eventFuncStr )
            return eventFunc( data )
        else:
            return None

    def doSendLine( self, data ):
        ''' Encode all messages to fall in line with twisted convention
        Inputs:
            data: dict: raw data to pass onto the client
        '''
        data = json.dumps( data ).encode( 'ascii', 'ignore' )
        self.sendLine( data )

    def updateClients( self, msg ):
        ''' Handler for IDENTIFY event on the server. 
            Looks to update the existing client mapping with new conneciton
        Inputs:
            msg: dict: message received from IDENTIFY event
        '''
        self.clientName = msg.get( EnvMapping.CLIENT_TYPE.value, None )
        if self.clientName:
            self.factory.clients[ self.clientName + '_{}'.format( self.factory.numConnections ) ] = self
            self.factory.numConnections += 1
            print( '{} Clients Currently being held: {}'.format( self.factory.numConnections, self.factory.clients ) )
            msg = buildMessage( event = EventTypes.REGISTERED.value )
            self.doSendLine( msg )
        else:
            # todo if no clientName is provided, disconnect that client with failure to
            # authenticate message
            pass

    def lineReceived( self, data ):
        ''' Handler for when Server receives message
        Inputs:
            data: json: message given in json format
        '''
        msg = json.loads( data )
        # There are instances where data is returned in bytes
        # decode this if that happens 
        if isinstance( msg, bytes ):
            msg = msg.decode( 'ascii' )
        eventType = msg.get( EnvMapping.EVENT.value )
        self.handleEvent( eventType, msg )
    
class ServerBaseFactory( Factory ):
    ''' Server Base Factory '''

    def __init__( self ):
        self.clients = {}
        self.numConnections = 0

    def buildProtocol( self, addr ):
        return ServerBase( factory = self, eventHandler = EVENT_HANDLER_SERVER )

reactor.listenTCP( BASE_PORT, ServerBaseFactory() )
reactor.run()



