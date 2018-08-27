from PluginInfo import PluginInfo
from Plugin import Plugin

import urllib.request
import json

class youtube_id(Plugin):
    _API_KEY = "AIzaSyBpW1Q7OKWJsUDwqakpFRIbrJ5leWtFGrc"
    
    def __init__(self):
        self._pluginInfo = PluginInfo(
            'youtube_id',
            'https://www.youtube.com/',
            'YouTube',
            'youtube.com/channel/(?P<username>([^/]+))',
            'https://www.youtube.com/favicon.ico'
        )
    
    def _getStreamState(self, username):
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + username +\
        "&type=video&eventType=live&key=" + self._API_KEY

        try:
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
        except:
            return None
        
        if 'items' in response and len(response['items']) > 0:
            stream = response['items'][0]
            return {
                'url' : 'https://www.youtube.com/watch?v=' + stream['id']['videoId'],
                'title' : stream['snippet']['title'],
                #'description' : stream['snippet']['description'],
                'previews' : {
                    'small' : stream['snippet']['thumbnails']['default']['url'],
                    'medium' : stream['snippet']['thumbnails']['medium']['url'],
                    'large' : stream['snippet']['thumbnails']['high']['url'],
                }
            }
        
        return None
