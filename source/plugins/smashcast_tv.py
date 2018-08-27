from PluginInfo import PluginInfo
from Plugin import Plugin

import urllib.request
import json

class smashcast_tv(Plugin):
    def __init__(self):
        self._pluginInfo = PluginInfo(
            'smashcast_tv',
            'https://www.smashcast.tv/',
            'Smashcast',
            'smashcast.tv/(?P<username>([^/]+))',
            'https://www.smashcast.tv/favicon.ico'
        )
    
    def _getStreamState(self, username):
        url = 'https://api.smashcast.tv/media/channel/' + username + '.json'

        try:
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
        except:
            return None
        
        if 'livestream' in response:
            livestream = response['livestream'][0]
            if 'media_is_live' in livestream and livestream['media_is_live'] != '0':
                return {
                    'url' : 'https://www.smashcast.tv/' + username,
                    'game' : livestream['category_name'],
                    'title' : livestream['media_status'],
                    'viewers' : livestream['media_views'],
                    'previews' : {
                        'medium' : livestream['media_thumbnail'],
                        'large' : livestream['media_thumbnail_large'] 
                    }
                }
        
        return None
