import time
from PluginInfo import PluginInfo

class Plugin():
    #stream => (timestamp, StreamState)
    _timeout = 120
    _CACHED_STREAM_STATES = {}

    def __init__(self):
        self._pluginInfo = None #pluginInfo
 
    def getPluginInfo(self):
        return self._pluginInfo

    def _getCachedStreamState(self, stream):
        if not stream in self._CACHED_STREAM_STATES:
            return (None, None)
        
        return self._CACHED_STREAM_STATES[stream]
    
    def getStreamStates(self, usernames):
        streamStates = {}
        for username in usernames:
            timestamp, streamState = self._getCachedStreamState(username)
            
            # state not in cache or state too old
            if timestamp == None or timestamp + self._timeout < int(time.time()):
                streamState = self._getStreamState(username)
                timestamp = int(time.time())
                self._CACHED_STREAM_STATES[username] = (timestamp, streamState)

            streamStates[username] = streamState    

        return streamStates

    def getStreamState(self, username):
        timestamp, streamState = self._getCachedStreamState(username)
        
        # state not in cache or state too old
        if timestamp == None or timestamp + self._timeout < int(time.time()):
            streamState = self._getStreamState(username)
            timestamp = int(time.time())
            self._CACHED_STREAM_STATES[username] = (timestamp, streamState)

        return streamState    

