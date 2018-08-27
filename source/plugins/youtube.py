from PluginInfo import PluginInfo
from Plugin import Plugin

import urllib.request
import json

class youtube(Plugin):
    _API_KEY = "AIzaSyBpW1Q7OKWJsUDwqakpFRIbrJ5leWtFGrc"
    _CACHED_YOUTUBE_IDS = {}

    def __init__(self):
        self._pluginInfo = PluginInfo(
            'youtube',
            'https://www.youtube.com/',
            'YouTube',
            'youtube.com/user/(?P<username>([^/]+))',
            'https://www.youtube.com/favicon.ico'
        )
   
    def _obtainChannelId(self, username):
        if username in self._CACHED_YOUTUBE_IDS:
            return self._CACHED_YOUTUBE_IDS[username]

        url = "https://www.googleapis.com/youtube/v3/channels?key=" + self._API_KEY +\
        "&forUsername=" + username + "&part=id"

        try:
            response = urllib.request.urlopen(url).read()
            response = json.loads(response.decode('utf-8'))
        except:
            return None

        youtube_id = None
        if 'items' in response and len(response['items']) > 0:
            youtube_id = response['items'][0]['id']

        self._CACHED_YOUTUBE_IDS[username] = youtube_id
        return youtube_id

    def _getStreamState(self, username):
        youtube_id = self._obtainChannelId(username)
        if youtube_id == None:
            return None

        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=" + youtube_id +\
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
