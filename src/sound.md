Sound Class
-----------
html5 audio wrapper

```rusthon
#backend:javascript

class Sound:
	def __init__(self, url, loop=false):
		self.audio = document.createElement('audio')
		self.audio.loop = loop
		self.source = document.createElement('source')
		self.source.src = url
		self.audio.appendChild( self.source )
		self.audio.addEventListener('loaded')

	def play(self):
		self.audio.currentTime = 0
		self.audio.play()

	def stop(self):
		self.audio.repeat = false
		self.audio.pause()

#bgmusic = Sound('ocean.mp3', loop=true)
#def play_bgmusic():
#	bgmusic.play()
#window.setTimeout(play_bgmusic, 5000)

```