Game Engine
-----------

```rusthon
#backend:javascript

class Game:
	def __init__(self):
		print('new game...')
		req = new(XMLHttpRequest())
		req.open('GET', 'mygame.json', false)  ## false means sync
		req.send(null)
		self.data = JSON.parse( req.responseText )

		init( self )
		self.ws = init_websocket( self.on_ws_open.bind(this), self.on_ws_message.bind(this) )
		self.load_game( self.data )

	def load_game(self, game):
		print('loading game..')
		self.materials = {}
		for name in game.materials:
			m = game.materials[ name ]
			mat = new(THREE.MeshLambertMaterial(
				color=0xffffff, 
				ambient=0x000000,
				wireframe = false,
			))
			mat.color.setRGB( m.diffuse[0], m.diffuse[1], m.diffuse[2] )
			mat.ambient.setRGB( m.diffuse[0], m.diffuse[1], m.diffuse[2] )
			self.materials[ name ] = mat

		self.body_instances = {}
		self.mesh_instances = {}
		self.enemies = {}
		## simple triggers if player passes point x, simple action api.
		self.triggers = {}
		## empty with a child that marks the jump/spawn point for the player
		self.level_jump_triggers = {}
		self.level = None
		self.level_index = 0
		self.levels = game.levels.main
		self.secret_levels = game.levels.secrets
		self.load_level( game.levels.main[0] )


	def load_level(self, level):
		print('load level.')
		self.triggers.update( level.triggers )
		self.level = level
		self.level_index = self.levels.index(level)

		for name in level['instances']:
			ob = level['instances'][name]
			print( ob )
			if ob.type == 'CURVE':
				material = None
				ice = false
				if ob.material == 'ICE':
					ice = true
				elif ob.material:
					material = self.materials[ ob.material ]

				data_name = ob.data
				print( 'curve data_name:', data_name)
				points = self.data['curves'][ data_name ]

				if ob.position[2] == 0.0:
					b = new(p2.Body(
						mass=0, 
						position=ob.position,
						angle=ob.rotation[2]
					))
					b.fromPolygon( points, removeCollinearPoints=0.01)
					world.addBody(b)
					mesh = add_shape(
						b.concavePath, 
						extrude=ob.extrude*2, 
						bevel=ob.bevel,
						ice=ice, 
						material=material 
					)

					if ob.physics == 'DYNAMIC':
						b.setDensity(1.0 * ob.mass )
						b.motionState = p2.Body.DYNAMIC
					mesh._body = b
					SyncMeshes.append( mesh )
					self.body_instances[ ob.name ] = b

				else:
					mesh = add_shape(
						points, 
						extrude=ob.extrude*2, 
						bevel=ob.bevel, 
						ice=ice, 
						material=material
					)
					self.mesh_instances[ ob.name ] = mesh

				x,y,z = ob.position
				mesh.position.set(x,y,z)
				x,y,z = ob.rotation
				mesh.rotation.set(x,y,z)
				x,y,z = ob.scale
				mesh.scale.set(x,y,z)



	def spawn_enemy(self, name):
		print('spawn enemy', name)
		ob = self.level.enemies[ name ]
		x,y,z = ob.position
		e = Enemy(x=x, y=y, z=z)
		self.enemies[ name ] = e
		return e

	def trigger(self, t):
		print('trigger',t)
		for name in t.signals:
			print('signal:'+name)
			if name.startswith('spawn'):
				for n in t.signals[name]:
					self.spawn_enemy( n )
			elif name.startswith('activate'):
				for n in t.signals[name]:
					self.enemies[ n ].active = true

			else:
				print('unknown signal:', name)


	def animate(self, *args):
		global time
		requestAnimationFrame( self.animate.bind(this) )

		delta = clock.getDelta()
		time += delta
		world.step(1/60, delta, 3)

		if USE_PIXI:
			demo.render()

		if SPAWN_ENEMIES:
			if Math.random()>0.99 and Enemies.length < 8:
				if Math.random() > 0.5:
					e = Enemy(x=-40)
				else:
					e = Enemy(x=40)

		for enemy in Enemies:
			enemy.update(time)

		controls.update()
		waterMesh.material.uniforms.time.value = time

		for mesh in Glaicers:
			mesh.position.y += Math.sin( time )*0.01

		for mesh in SyncMeshes:
			mesh.position.x = mesh._body.position[0]
			mesh.position.y = mesh._body.position[1]
			mesh.rotation.z = mesh._body.angle

		for i,flake in enumerate(SnowFlakes):
			m = i+1
			if i > 4: m = -m
			flake.rotation.y = time * m


		simulate(time)

		x,y = player.update(time, delta)
		for name in self.triggers:
			t = self.triggers[name]
			if x > t.position[0]:
				self.trigger( t )
				self.triggers.pop( name )

		if AUTO_CAMERA:
			#if y > 0.0:

			d = (y - camera.position.y) * 0.01
			camera.position.y += d

			#elif camera.position.y > 3:
			#	camera.position.y *= 0.9

			camera.position.z = y+10
			#y += 40.0
			d = (y - camera.target.y) * 0.1
			camera.target.y += d

			d = (x - camera.target.x) * 0.1
			camera.target.x+=d
			camera.lookAt( {'x':camera.target.x, 'y':camera.target.y, 'z':0.0} )

			d = (x - camera.position.x) * 0.01
			camera.position.x += d


		if camera.position.y < 10:
			camera.position.y += 0.1

		renderer.setClearColor( 0xffffff, 1 )
		renderer.clear()

		WaterHF.update(delta)
		water.render()

		if USE_POSTPROC:
			composer.render(scene, camera)
		else:
			renderer.render(scene, camera)
		#WaterHF.flood( delta )

		stats.update()

	def on_ws_open(self):
		self.ws.send('hello server')

	def on_ws_message(self, event):
		print 'on ws message', event
		if instanceof(event.data, ArrayBuffer):
			print 'got binary bytes', event.data.byteLength
			arr = new(Uint8Array(event.data))
		else:
			ob = JSON.parse(event.data)
			if ob.name in self.body_instances:
				body = self.body_instances[ ob.name ]
				body.position[0] = ob.position[0]
				body.position[1] = ob.position[1]
				body.angle = ob.rotation[2]
			elif ob.name in self.mesh_instances:
				mesh = self.mesh_instances[ ob.name ]
				x,y,z = ob.position
				mesh.position.set(x,y,z)
				x,y,z = ob.scale
				mesh.scale.set(x,y,z)
				x,y,z = ob.rotation
				mesh.rotation.set(x,y,z)

```