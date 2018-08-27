from flask import Flask
from flask import request, redirect
from flask import send_from_directory, render_template
from flask import jsonify

from Plugin import Plugin

import os
import time
import importlib
import sqlite3
import json
import re

#################
# CONFIGURATION #
#################
app = Flask(__name__, static_folder='static', template_folder='template')
app.url_map.strict_slashes = False


##############
# VARIABLES  #
##############
pluginInfos = []
plugins = {}

#cache for /api/plugins/ request
pluginInfosJson = []

#################
# PLUGIN LOADER #
#################
for filename in os.listdir(os.path.dirname(os.path.realpath(__file__)) + '/plugins'):
    if filename == '__init__.py' or filename[-3:] != '.py':
        continue
    
    filename = filename[0:-3] #trim file extension
    plugin = importlib.import_module('plugins.' + filename, 'plugins')
    plugin = getattr(plugin, filename)
    plugin = plugin()
    plugins[filename] = plugin
    pluginInfos.append(plugin.getPluginInfo())
    pluginInfosJson.append(plugin.getPluginInfo().toJSON())

if len(pluginInfos) == 0:
    print("You need to include at least one plugin in /plugins direcory to run this app")
    exit()

####################
# STATIC RESOURCES #
####################
@app.route('/', methods = ['GET'])
def home():
    return send_from_directory(app.static_folder, 'home.html', mimetype='text/html')

@app.route('/api', methods = ['GET'])
@app.route('/api/', methods = ['GET'])
def api_get():
    return send_from_directory(app.static_folder, 'api.html', mimetype='text/html')
    
@app.route('/favicon.ico', methods = ['GET'])
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.errorhandler(404)
def error_404(e):
    return send_from_directory(app.static_folder, '404.html', mimetype='text/html')

#############
# TEMPLATES #
#############
@app.route('/api/plugins', methods = ['GET'])
@app.route('/api/plugins/', methods = ['GET'])
def api_plugins_get():
    return render_template('available_plugins.html', plugins = pluginInfos)

@app.route('/api/plugins/<plugin_name>', methods = ['GET'])
@app.route('/api/plugins/<plugin_name>/', methods = ['GET'])
def api_plugins_plugin_get(plugin_name):
    if not plugin_name in plugins:
        return error_404(None)

    return render_template('plugin_details.html', plugin = plugins[plugin_name].getPluginInfo())
#################
# API ENDPOINTS #
#################
@app.route('/api/plugins', methods = ['POST'])
@app.route('/api/plugins/', methods = ['POST'])
def api_plugins_post():
    return jsonify(pluginInfosJson)

@app.route('/api/plugins/<plugin_name>', methods = ['POST'])
@app.route('/api/plugins/<plugin_name>/', methods = ['POST'])
def api_plugins_plugin_post(plugin_name):
    if not plugin_name in plugins:
        return jsonify({'error' : 'no such plugin: ' + plugin_name, 'streams' : None})

    #user validation
    database_tokens = sqlite3.connect('StreamChecker.db')
    database_tokens = database_tokens.cursor()
    data = request.get_json()
    
    #data validation
    if(len(data) == 2):
        try:
            auth_token = data['auth_token']
            streams = data['streams']
        except:
            return jsonify({'error' : 'bad request', 'streams' : None})
    
    database_tokens.execute('SELECT expiry_date FROM tokens WHERE auth_token=?', (auth_token,))
    result = database_tokens.fetchone()
    if(result == None):
        return jsonify({'error' : 'invalid auth_token', 'streams' : None})
    
    expiry_date = result[0]
    today = time.strftime("%Y-%m-%d")
    
    #both are in YYYY-MM-DD format, so string comparison will always work
    if(expiry_date < today):
        return jsonify({'error' : 'expired auth token; expiry date: ' + expiry_date, 'streams' : None})

        
    stream_states = plugins[plugin_name].getStreamStates(streams)
    return jsonify({'error' : None, 'stream_states' : stream_states})

@app.route('/api', methods = ['POST'])
@app.route('/api/', methods = ['POST'])
def api_auto_post():
    #user validation
    database_tokens = sqlite3.connect('StreamChecker.db')
    database_tokens = database_tokens.cursor()
    data = request.get_json()

    #data validation
    if(len(data) == 2):
        try:
            auth_token = data['auth_token']
            streams = data['streams']
        except:
            return jsonify({'error' : 'bad request', 'streams' : None})
    
    database_tokens.execute('SELECT expiry_date FROM tokens WHERE auth_token=?', (auth_token,))
    result = database_tokens.fetchone()
    if(result == None):
        return jsonify({'error' : 'invalid auth_token', 'streams' : None})
    
    expiry_date = result[0]
    today = time.strftime("%Y-%m-%d")
    
    #both are in YYYY-MM-DD format, so string comparison will always work
    if(expiry_date < today):
        return jsonify({'error' : 'expired auth token; expiry date: ' + expiry_date, 'streams' : None})

    error = {}
    stream_states = {}
    for stream in streams:
        #print("url: " + stream)
        for key, plugin in plugins.items():
            match = re.search(plugin.getPluginInfo().getSupportedUrlRegex(), stream)
            if match and match.group('username'):
                username = match.group('username')
                stream_states[stream] = plugin.getStreamState(username)
                #print(" plugin: " + plugin.getPluginInfo().getName() + "\n")
                break

        if stream not in stream_states:
            stream_states[stream] = None
            error[stream] = 'Unsupported url'
            #print(" plugin: None")

    return jsonify({'error' : (None if error == {} else error), 'stream_states' : stream_states})

########
# MAIN #
#######
if __name__ == '__main__':
    app.run(debug=True, port='1234')
