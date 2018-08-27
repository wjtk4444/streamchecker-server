# StreamChecker server
StreamChecker application server

StreamChecker is an application made to provide an easy way to deliver notifications about online streams to users. It's main feature is a plugin system that helps to ensure compatibility with virtually any streaming service.

StreamChecker server is the core part of the application - it gathers data about live streams and normalizes them to a way clients can use. As an user You're probably more interested in StreamChecker clients.

Available clients:
- There are no clients yet. Both Windows and Linux clients are under construction now.

# Repository contents:
- Full source code of streamchecker-server and all plugins
    - The project is currently under heavy development and everything is a subject to change. API keys exposed in plugins will be deactivated and a license will be added when the first public release comes out.
- Two example clients (written in Python) using two different API endpoints.
- Example database containing 3 different access tokens. (Futher explanation in clients' source codes)
- StreamChecker project website (Currently it's just a mere dummy)

# Requirements:
Python 3.7.0+
Flask 1.0.2+
