class PluginInfo():
    def __init__(self, name, url, description, supportedUrlRegex, iconUrl):
        self._name = name
        self._url = url
        self._description = description
        self._supportedUrlRegex = supportedUrlRegex
        self._iconUrl = iconUrl


    def getName(self):
        return self._name

    def getUrl(self):
        return self._url
    
    def getDescription(self):
        return self._description

    def getSupportedUrlRegex(self):
        return self._supportedUrlRegex

    def getIconUrl(self):
        return self._iconUrl


    def toJSON(self):
        return '''{{
            "name":"{}",
            "url":"{}",
            "description":"{}",
            "supportedUrlRegex":"{}",
            "iconUrl":"{}"
        }}'''.format(
            self._name,
            self._url,
            self._description,
            self._supportedUrlRegex,
            self._iconUrl
        )
