##################################################
# Const file for twisted Client and Server classes
##################################################

import enum

class EnvMapping( enum.Enum ):
    EVENT = 'event'
    CLIENT_TYPE = 'clientType'
    UNREGISTERED_STATE  = 'UNREGISTERED'

class EventTypes( enum.Enum ):
    IDENTIFY = 'IDENTIFY'
    REGISTERED = 'REGISTERED'

# Handlers for Client Side events
EVENT_HANDLER_CLIENT = { 
    EventTypes.IDENTIFY.value: 'onIndentify',
    EventTypes.REGISTERED.value: 'onRegistration',
 }

 # Handler for Server Side events
EVENT_HANDLER_SERVER = {
    EventTypes.IDENTIFY.value: 'updateClients',
 }

# All base messages between Clients and Servers must contain an event handle
BASE_MESSAGE = { EnvMapping.EVENT.value: '' }

BASE_PORT = 8000
BASE_HOST = 'localhost'
REGISTERED_STATE = 'REGISTERED'
UNREGISTERED_STATE = 'UNREGISTERED'


