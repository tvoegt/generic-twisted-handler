#########################
# utils func for Twisted Client and Server handlers
#########################

from const import BASE_MESSAGE, EnvMapping
import json
import copy

def buildMessage( event, kwargs = None ):
    ''' Builds a JSON message between Clients and Servers 
    Inputs:
        event: str: type of event you are sending
        kwargs: dict: anything of interest you with to send on 
    Returns:
        json: message to transfer between client and server
    '''
    kwargs = kwargs or {} 
    msgDict = copy.deepcopy( BASE_MESSAGE )
    msgDict[ EnvMapping.EVENT.value ] = event
    msgDict.update( kwargs )
    return msgDict
