from PluginInfo import PluginInfo
from Plugin import Plugin

import urllib.request
import json

class picarto_tv(Plugin):
    def __init__(self):
        self._pluginInfo = PluginInfo(
            'picarto_tv',
            'https://picarto.tv/',
            'Creative live streaming service - Picarto',
            'picarto.tv/(?P<username>([^/]+))',
            'https://www.picarto.tv/favicon.ico'
        )
    
    def _getStreamState(self, username):
        url = 'https://api.picarto.tv/v1/channel/name/' + username

        try:
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
        except:
            return None
        
        if 'online' in response and response['online'] != False:
            #if len(response['description_panels']) > 0:
            #    description = response['description_panels'][0]['title'] + ' ' +\
            #        response['description_panels'][0]['body']
            #else:
            #    description = 'No description'
            
            return {
                'url' : 'https://picarto.tv/' + username,
                'title' : response['title'],
            #    'description': description,
                'viewers' : response['viewers'],
                'previews' : response['thumbnails']
            }
        
        return None
