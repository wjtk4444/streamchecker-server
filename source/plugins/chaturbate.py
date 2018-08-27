from PluginInfo import PluginInfo
from Plugin import Plugin

import urllib.request
import json
import re

class chaturbate(Plugin):
    def __init__(self):
        self._pluginInfo = PluginInfo(
            'chaturbate',
            'https://chaturbate.com/',
            'Chaturbate - Free Adult Live Webcams!',
            'chaturbate.com/(?P<username>([^/]+))',
            'https://www.chaturbate.com/favicon.ico'
        )
    
    def _getStreamState(self, username):
        url = 'https://chaturbate.com/' + username

        try:
            response = urllib.request.urlopen(url).read().decode('utf-8')
        except:
            return None
        
        if 'Room is currently offline' not in response:
            match = re.search('default_subject: "(.+?)"', response)
            if match:
                title = match.group(1)
            else:
                title = 'no title'
            
            panelurl = 'https://chaturbate.com/api/panel/' + username
            try:
                response = urllib.request.urlopen(panelurl).read().decode('utf-8')
            except:
                response = None

            status = None
            if response == None:
                status = None
            elif '<strong>' in response and 'Remaining' in response:
                match = re.search('<strong>(.+?)</strong>', response)
                if match:
                    status = match.group(1)
            elif 'class="counter_label_green' in response:
                match = re.search('<div class="counter_label_green">(.+?)</div>', response)
                if match:
                    status = match.group(1)
                    match = re.search('<td class="data">(.+?)</td>', response)
                    if match:
                        status += ' ' + match.group(1)
                        match = re.search('<div class="counter_label">(.+?)</div>', response)
                        if match:
                            status += "\n" + match.group(1)
                            match = re.search('<td class="data">(.+?)</td>', response)
                            if match:
                                status += ' ' + match.group(1)
            
            return {
                'url' : url,
                'title' : title,
                'status' : status,
                'previews' : {
                    'small' : 'https://roomimg.stream.highwebmedia.com/ri/' + username + '.jpg'
                }
            }
        
        return None
