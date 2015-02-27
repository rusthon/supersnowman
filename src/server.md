Server Script
-------
The script below `server.py` is written in Python3 and requires Tornado.

@server.py
```python
#!/usr/bin/env python3

try:
	import tornado
except ImportError:
	print('ERROR: Tornado is not installed')
	print('download Tornado from - http://www.tornadoweb.org/en/stable/')
	raise SystemExit

import tornado.ioloop
import tornado.web
import tornado.websocket
import os, sys, subprocess, datetime, json

ResourcePaths = ['./data/']
assert os.path.isdir(ResourcePaths[0])

def open_blender():
	cmd = [
		'blender',
		'./data/level.blend',
		'--window-geometry', '700','0','640','480', '-noaudio', 
		'--python',  './blenderhack.py',
	]
	proc = subprocess.Popen( cmd )



class MainHandler( tornado.web.RequestHandler ):
	def get(self, path=None):
		print('path', path)

		if not path:
			self.write( open('./main.html','rb').read() )

		elif path == 'open-blender':
			open_blender()
			server.write('OK')

		else:
			local_path = path
			if os.path.isfile( local_path ):
				data = open(local_path, 'rb').read()
				self.set_header("Content-Length", len(data))
				self.write( data )

			else:
				found = False
				for root in ResourcePaths:
					local_path = os.path.join( root, path )
					if os.path.isfile(local_path):
						data = open(local_path, 'rb').read()
						self.set_header("Content-Length", len(data))
						self.write( data )
						found = True
						break

				if not found:
					print( 'FILE NOT FOUND', path)

class WebSocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print( self.request.connection )

	def on_message(self, msg):
		print('on json message', msg)
		self.write_message('"hello client"')

	def on_close(self):
		print('websocket closed')
		if self.ws_connection:
			self.close()


Handlers = [
	(r'/websocket', WebSocketHandler),
	(r'/(.*)', MainHandler),  ## order is important, this comes last.
]

if __name__ == '__main__':
	print('running server...')
	print('http://localhost:8080')
	os.system('google-chrome --app=http://localhost:8080 &')
	app = tornado.web.Application(Handlers)
	app.listen( 8080 )
	tornado.ioloop.IOLoop.instance().start()

```
