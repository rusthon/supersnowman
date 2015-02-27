SuperSnowman Demo
-----------------
Requires:
* Blender
* Python2
* Python3

On most linux systems you will only need to run:
`sudo apt-get install blender python3`

Running:
`./rusthon.py SuperSnowman.md --run=server.py --data=./data,./libs`
The command above will rebuild and run this project.

Markdown Imports
---------------
* [@import blenderhack.md](src/blenderhack.md)
* [@import server.md](src/server.md)
* [@import mainhtml.md](src/mainhtml.md)


Main Source Code
-----------
The Python code below is translated to JavaScript and inserted at the tag `<@SuperSnowmanCode>` marker in [mainhtml.md](src/mainhtml.md)
Main globals for screen size, water size, etc..

@SuperSnowmanCode
```rusthon
#backend:javascript

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

WATER_SIZE = [100,25];
WATER_RES = [256,32];
#WATER_GRID_SIZE = WATER_SIZE / WATER_RES;
MEAN_WATER_HEIGHT = 0.0;
WATER_FLOOD_RATE = 0.0;
WATER_SOURCE_AMOUNT = 0.2;
WATER_SOURCE_RADIUS = 0.7;
WATER_SINK_AMOUNT = 0.5;
WATER_SINK_RADIUS = 0.7;

demo = None
world = None
Blobs = []
blob = None

uvGenerator = new(THREE.UVsUtils.CylinderUVGenerator())

```

Extra Markdown Imports
----------------------
* [@import iceshader.md](src/iceshader.md)
* [@import watershader.md](src/watershader.md)
* [@import hmapshader.md](src/hmapshader.md)
* [@import sound.md](src/sound.md)
* [@import enemy.md](src/enemy.md)
* [@import player.md](src/player.md)



```rusthon
#backend:javascript

PhysicsMaterials = {
	'default' : new(p2.Material()),
	'water' : new(p2.Material()),
	'missle' : new(p2.Material()),
	'player' : new(p2.Material()),
	'player-skin' : new(p2.Material()),
	'player-head' : new(p2.Material()),
	'enemy' : new(p2.Material()),
	'trigger' : new(p2.Material()),
	'exit' : new(p2.Material()),
}

def init( game ):
	global plane, demo, world, player


	bp = new( p2.SAPBroadphase() )

	world = new(
		p2.World(
			doProfiling=false,
			gravity = [0, -10],
			broadphase = bp
		)
	)
	world.solver.useGlobalEquationParameters = false  ## for custom soft collisions

	init_threejs( game )

	x,y,z = game.data.player.position
	player = new Player(x,y,z)

	planeShape = new( p2.Plane() )
	planeShape.material = PhysicsMaterials['water']

	wall = new(p2.Body(
		position=[-50, 0],
		angle = -Math.PI/2
	))
	wall.addShape( planeShape )
	world.addBody( wall )

	wall = new(p2.Body(
		position=[50, 0],
		angle = Math.PI/2
	))
	wall.addShape( planeShape )
	world.addBody( wall )


	plane = new( p2.Body(position=[0,-0.5], mass=1.0) )
	plane.addShape( planeShape )
	plane.motionState = p2.Body.DYNAMIC
	world.addBody( plane )

	dummy = new( p2.Body(position=[0,0.5], mass=0.0) )
	dummy.motionState = p2.Body.STATIC

	spring = new(p2.Spring(
		dummy,plane,
		stiffness=10000,
		restLength=0.75
	))
	world.addSpring(spring)


	a = PhysicsMaterials['water']
	b = PhysicsMaterials['default']
	cm = new(p2.ContactMaterial(
		a, b,
		restitution = 0,
		stiffness = 0.01,
		relaxation = 10000
	))
	world.addContactMaterial( cm )

	a = PhysicsMaterials['water']
	b = PhysicsMaterials['missle']
	cm = new(p2.ContactMaterial(
		a, b,
		restitution = 1,
	))
	world.addContactMaterial( cm )

	a = PhysicsMaterials['default']
	b = PhysicsMaterials['missle']
	cm = new(p2.ContactMaterial(
		a, b,
		restitution = 1,
	))
	world.addContactMaterial( cm )



	################################################
	global demo
	demo = new(PixiDemo(world, width=1200,height=540, run=false))
	demo.setState(Demo.DRAWPOLYGON)

	def on_add_body(evt):
		print('on_add_body')
		return
		print(evt.body)
		evt.body.setDensity(10)
		evt.body.gravityScale = 1.0
		if evt.body.concavePath:
			for shape in evt.body.shapes:
				print(shape)
				shape.material = PhysicsMaterials['default']
			mesh = add_shape( evt.body.concavePath, evt.body._sprite_color )
			print(evt.body)
			mesh.position.x = evt.body.position[0]
			mesh.position.y = evt.body.position[1]
			mesh._body = evt.body
			SyncMeshes.append( mesh )

	world.on("addBody",on_add_body)


	def on_impact(evt):
		materialA = None
		materialB = None
		if hasattr(evt.shapeA, 'material'):
			materialA = evt.shapeA.material
		if hasattr(evt.shapeB, 'material'):
			materialB = evt.shapeB.material

		if materialA == PhysicsMaterials['missle']:
			evt.bodyA.on_missle_contact( evt.bodyA, evt.bodyB, evt.shapeB )
		elif materialB == PhysicsMaterials['missle']:
			evt.bodyB.on_missle_contact( evt.bodyB, evt.bodyA, evt.shapeA )

		elif evt.shapeA is planeShape:
			if instanceof(evt.shapeB, p2.Particle):
				pass
			else:
				x = evt.bodyB.position[0]
				s = evt.bodyB.velocity[1] *0.1
				WaterHF.disturb( {'x':x,'z':0.0}, -s, 2)

				if evt.bodyB is player.center:
					player.splash( evt.bodyB.velocity )
		elif evt.shapeB is planeShape:
			if instanceof(evt.shapeA, p2.Particle):
				pass
			else:
				x = evt.bodyA.position[0]
				s = evt.bodyA.velocity[1] *0.1
				WaterHF.disturb( {'x':x,'z':0.0}, -s, 2)

				if evt.bodyA is player.center:
					player.splash( evt.bodyA.velocity )

		elif evt.bodyA is player.center:
			player.on_touch( evt.bodyB, evt.shapeB )
		elif evt.bodyB is player.center:
			player.on_touch( evt.bodyA, evt.shapeA )

		elif materialA == PhysicsMaterials['player-skin']:
			player.on_touch( evt.bodyB, evt.shapeB )
		elif materialB == PhysicsMaterials['player-skin']:
			player.on_touch( evt.bodyA, evt.shapeA )

		elif materialA == PhysicsMaterials['enemy']:
			evt.bodyA.enemy.on_touch( evt.bodyB, evt.shapeB )
		elif materialB == PhysicsMaterials['enemy']:
			evt.bodyB.enemy.on_touch( evt.bodyA, evt.shapeA )


	world.on('impact', on_impact)


scene = None
renderer = None
camera = None
SyncMeshes = []

def add_shape( points, extrude=0.5, bevel=0.0, color=0xffffff, smooth=false, ice=true, material=None ):
	arr = [] #[new(THREE.Vector2(x,y)) for x,y in points]
	for p in points:
		arr.append(
			new(THREE.Vector2(p[0],p[1]))
		)
	shape = new(THREE.Shape(arr))

	if ice:
		geometry = new(THREE.ExtrudeGeometry(
			shape, 
			amount=extrude,
			bevelEnabled=True,
			bevelSegments=2,
			bevelSize=0.1,
			bevelThickness=0.5,
			steps=1,
			uvGenerator = uvGenerator
		))
	else:
		geometry = new(THREE.ExtrudeGeometry(
			shape, 
			amount=extrude,
			bevelEnabled = bevel > 0.0,
			bevelSize = bevel,
			bevelThickness=bevel
		))

	#geometry.computeVertexNormals()
	#geometry.computeFaceNormals()
	for vert in geometry.vertices:
		vert.z -= extrude * 0.5

	if ice:
		modifier = new(THREE.SubdivisionModifier(1))
		#modifier.useOldVertexColors = true ## deprecated?
		modifier.modify( geometry )
		for vertex in geometry.vertices:
			vertex.x += Math.random()*Math.random()*0.3
			vertex.y += Math.random()*Math.random()*0.3
			vertex.z += Math.random()*Math.random()*0.3


		if smooth:
			modifier.modify( geometry )

		s = 0.96
		for vertex in geometry.vertices:
			r = Math.random()*Math.random() *0.2
			g = Math.random()*Math.random() *0.25
			b = Math.random()*Math.random() *0.35
			vertex.color = [r+s, g+s, b+s]

		for face in geometry.faces:
			verts = [face.a, face.b, face.c]
			for index in verts:
				v = geometry.vertices[index]
				vc = new(THREE.Color(0xff0000))
				vc.setRGB( v.color[0], v.color[1], v.color[2] )
				face.vertexColors.append(vc)



		mat = create_ice_material()

	elif material:
		mat = material

	else:
		mat = new(THREE.MeshLambertMaterial(
			color=0xffffff, 
			ambient=0x000000,
			wireframe = false,
		))

	mesh = new(THREE.Mesh(geometry, mat))
	mesh.castShadow = True
	mesh.receiveShadow = True
	scene.add( mesh )
	return mesh

def init_threejs( game ):
	global scene, renderer, camera, controls, composer, stats

	camera = new(THREE.PerspectiveCamera( 50, SCREEN_WIDTH / SCREEN_HEIGHT, 1, 300000 ))
	x,y,z = game.data.player.position
	camera.position.set( x, y+3, 20 )
	camera.target = new(THREE.Vector3(x,y+1,0))

	controls = new(THREE.TrackballControls(camera))
	controls.enabled = False
	controls.rotateSpeed = 1.0
	controls.zoomSpeed = 1.2
	controls.panSpeed = 0.8
	controls.noZoom = False
	controls.noPan = False
	controls.staticMoving = True
	controls.dynamicDampingFactor = 0.3
	controls.keys = [ 65, 83, 68 ]


	scene = new(THREE.Scene())
	rscene = new(THREE.Scene())  ## scene for reflections


	ambient = new(THREE.AmbientLight( 0x4444ff ))
	scene.add( ambient );


	pointLight = new(THREE.PointLight( 0x0044ff ))
	pointLight.position.set( 0, -50, 50 );
	scene.add( pointLight );

	light = new(
		THREE.SpotLight( 0xffffff, 1, 0, Math.PI / 2, 1 )
	)
	light.position.set( 0, 500, 100 )
	light.target.position.set( 0, 0, 0 )

	light.castShadow = True
	light.shadowCameraNear = 400
	light.shadowCameraFar = 550
	light.shadowCameraFov = 24
	#light.shadowCameraVisible = True

	light.shadowBias = 0.0001
	light.shadowDarkness = 0.4

	light.shadowMapWidth = 512
	light.shadowMapHeight = 512

	scene.add( light );

	renderer = new(THREE.WebGLRenderer( antialias=false ))
	renderer.setSize( SCREEN_WIDTH, SCREEN_HEIGHT )
	renderer.setClearColor( 0xffffff, 1 )
	renderer.shadowMapEnabled = True
	renderer.shadowMapType = THREE.PCFSoftShadowMap #THREE.PCFSoftShadowMap
	renderer.shadowMapSoft = true
	#renderer.gammaInput = true  ## vcolor*vcolor
	#renderer.gammaOutput = true
	container = document.getElementById('three_container') 
	container.appendChild( renderer.domElement )

	stats = new(Stats());
	stats.domElement.style.position = 'absolute';
	stats.domElement.style.top = '550px';
	stats.domElement.style.right = '10px';
	container.appendChild( stats.domElement );

	def on_enter(e):
		controls.enabled = True
	def on_leave(e):
		controls.enabled = False

	container.addEventListener('mouseenter', on_enter)
	container.addEventListener('mouseleave', on_leave)




	renderer.autoClear = false

	renderTargetParameters = {  };
	renderTarget = new(
		THREE.WebGLRenderTarget(
			SCREEN_WIDTH, 
			SCREEN_HEIGHT, 
			minFilter = THREE.LinearFilter, 
			magFilter = THREE.LinearFilter, 
			format = THREE.RGBFormat,
			stencilBuffer = false
	))

	effectFXAA = new(THREE.ShaderPass( THREE.FXAAShader ))

	hblur = new(THREE.ShaderPass( THREE.HorizontalTiltShiftShader ))
	vblur = new(THREE.ShaderPass( THREE.VerticalTiltShiftShader ))

	bluriness = 3;
	hblur.uniforms[ 'h' ].value = bluriness / SCREEN_WIDTH;
	vblur.uniforms[ 'v' ].value = bluriness / SCREEN_HEIGHT;

	hblur.uniforms[ 'r' ].value = 0.5
	vblur.uniforms[ 'r' ].value = 0.65

	effectFXAA.uniforms[ 'resolution' ].value.set( 1 / SCREEN_WIDTH, 1 / SCREEN_HEIGHT );

	composer = new(THREE.EffectComposer( renderer, renderTarget ))

	renderModel = new(THREE.RenderPass( scene, camera ))

	vblur.renderToScreen = true;


	composer.addPass( renderModel );
	composer.addPass( effectFXAA );
	composer.addPass( hblur );
	composer.addPass( vblur );

	skybox = create_skybox( scene )
	#rscene.add( skybox )

	water_mesh = create_gpu_water( renderer, camera, scene, light )
	#scene.add( water_mesh )

	create_snowflakes( scene )
	init_godrays()
	generate_glaicers()

Glaicers = []
def generate_glaicers():
	arr = []
	for j in range(100):
		arr.append(
			[Math.random()+j, (Math.random()*Math.random())+1]
		)
	arr.append( [100,0] )
	arr.append( [0,0] )

	bg = add_shape( arr )
	bg.position.x = -50
	bg.position.y = -4
	bg.position.z = -50
	bg.scale.x = 1
	bg.scale.y = 3
	bg.scale.z = 10
	Glaicers.append( bg )

	arr = []
	for j in range(50):
		arr.append(
			[Math.random()+j, (Math.random()*Math.random())+1]
		)
	arr.append( [100,0] )
	arr.append( [0,0] )

	bg = add_shape( arr )
	bg.position.x = -40
	bg.position.y = -4
	bg.position.z = -150
	bg.scale.x = 2
	bg.scale.y = 10
	bg.scale.z = 50
	bg.rotation.z = -Math.PI / 32
	Glaicers.append( bg )

	arr = []
	for j in range(30):
		arr.append(
			[Math.random()+j, (Math.random()*Math.random())+1]
		)
	arr.append( [100,0] )
	arr.append( [0,0] )

	bg = add_shape( arr, smooth=true )
	bg.position.x = -80
	bg.position.y = -10
	bg.position.z = 50
	bg.scale.x = 4
	bg.scale.y = 15
	bg.scale.z = 20
	bg.rotation.y = Math.PI / 2
	Glaicers.append( bg )

	arr = []
	for j in range(30):
		arr.append(
			[Math.random()+j, (Math.random()*Math.random())+1]
		)
	arr.append( [100,0] )
	arr.append( [0,0] )

	bg = add_shape( arr, smooth=true )
	bg.position.x = 60
	bg.position.y = -5
	bg.position.z = 50
	bg.scale.x = 4
	bg.scale.y = 10
	bg.scale.z = 20
	bg.rotation.y = Math.PI / 2
	Glaicers.append( bg )

def create_skybox(scene):
	global skyBox
	cubeMap = new(THREE.Texture( [] ))
	cubeMap.format = THREE.RGBFormat;
	cubeMap.flipY = false;

	loader = new(THREE.ImageLoader())
	def callback( image ):

		def getSide( x, y ):
			size = 1024;
			canvas = document.createElement( 'canvas' );
			canvas.width = size;
			canvas.height = size;
			context = canvas.getContext( '2d' );
			context.drawImage( image, - x * size, - y * size );
			return canvas

		cubeMap.image[ 0 ] = getSide( 2, 1 ); # px
		cubeMap.image[ 1 ] = getSide( 0, 1 ); # nx
		cubeMap.image[ 2 ] = getSide( 1, 0 ); # py
		cubeMap.image[ 3 ] = getSide( 1, 2 ); # ny
		cubeMap.image[ 4 ] = getSide( 1, 1 ); # pz
		cubeMap.image[ 5 ] = getSide( 3, 1 ); # nz
		cubeMap.needsUpdate = true;


	loader.load( 'skyboxsun25degtest.png', callback )

	cubeShader = THREE.ShaderLib['cube']
	cubeShader.uniforms['tCube'].value = cubeMap

	skyBoxMaterial = new(THREE.ShaderMaterial(
		fragmentShader = cubeShader.fragmentShader,
		vertexShader = cubeShader.vertexShader,
		uniforms = cubeShader.uniforms,
		depthWrite = false,
		side = THREE.BackSide
	))

	skyBox = new(THREE.Mesh(
		new(THREE.BoxGeometry( 100000, 100000, 100000 )),
		skyBoxMaterial
	))
	
	scene.add( skyBox )
	return skyBox


AUTO_CAMERA = True
def toggle_camera():
	global AUTO_CAMERA
	if AUTO_CAMERA:
		AUTO_CAMERA = false
	else:
		AUTO_CAMERA = true

SPAWN_ENEMIES = false
USE_POSTPROC = True
clock = new(THREE.Clock())
time = 0.0


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

			d = (y - camera.position.y) * 0.1
			camera.position.y += d

			#elif camera.position.y > 3:
			#	camera.position.y *= 0.9

			#camera.position.z = y+10
			#y += 40.0
			d = (y - camera.target.y) * 0.1
			camera.target.y += d

			d = (x - camera.target.x) * 0.1
			camera.target.x+=d
			camera.lookAt( {'x':camera.target.x, 'y':camera.target.y, 'z':0.0} )

			d = (x - camera.position.x) * 0.01
			camera.position.x += d


		#if camera.position.y < 0:
		#	renderer.setClearColor( 0x0000ff, 1 )
		#	skyBox.visible = False
		#	renderer.clear()
		#	render_godrays( true )
		#else:
		renderer.setClearColor( 0xffffff, 1 )
		skyBox.visible = True

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






USE_PIXI = true
def toggle_pixi(b):
	global USE_PIXI
	USE_PIXI = b
	a = document.getElementById('demo_container')
	a.hidden = not b

def open_blender():
	req = new(XMLHttpRequest())
	req.open('GET', 'open-blender', true)
	req.send(null)


def init_websocket(on_open, on_message):
	addr = 'ws://localhost:8080/websocket'
	print 'websocket test connecting to:', addr
	ws = new( WebSocket(addr) )
	#ws.binaryType = 'arraybuffer'
	ws.onmessage = on_message
	ws.onopen = on_open
	#ws.onclose = on_close
	return ws
```

main entry point
----------------
create a Game instance and run it.

```rusthon
#backend:javascript
def main():
	print 'enter main'
	g = Game()
	print 'animate game'
	g.animate()


```