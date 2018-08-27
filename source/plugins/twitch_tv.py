from PluginInfo import PluginInfo
from Plugin import Plugin

import urllib.request
import json

class twitch_tv(Plugin):
    _CLIENT_ID = 'ewvlchtxgqq88ru9gmfp1gmyt6h2b93'
    
    def __init__(self):
        self._pluginInfo = PluginInfo(
            'twitch_tv',
            'https://www.twitch.tv/',
            'Twitch',
            'twitch.tv/(?P<username>([^/]+))',
            'https://www.twitch.tv/favicon.ico'
        )
    
    def _getStreamState(self, username):
        url = 'https://api.twitch.tv/kraken/streams/' + username + '?client_id=' + self._CLIENT_ID

        try:
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
        except:
            return None
        
        if 'stream' in response:
            stream = response['stream']
            if stream != None and stream['stream_type'] == 'live': # ignore VOD
                return {
                    'url' : stream['channel']['url'],
                    'game' : stream['channel']['game'],
                    'title' : stream['channel']['status'],
                    'viewers' : stream['viewers'],
                    'previews' : stream['preview']
                }
        
        return None
