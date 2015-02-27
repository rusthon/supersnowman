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


@SuperSnowmanCode
```rusthon
#backend:javascript


def create_ice_material():
	merge = [
		THREE.ShaderLib['lambert'].uniforms,
		{
			'scale' : {
				'type': "f", 
				'value': 2.0 
			}
		}
	]
	uniforms = THREE.UniformsUtils.merge( merge )
	uniforms.ambient.value.setRGB(0,0,0.5)

	shaderMaterial = new(THREE.ShaderMaterial(
		uniforms = uniforms,
		#vertexShader   = document.getElementById( 'noise_vertexshader' ).textContent,
		vertexShader   = LAMBERT_NOISE_VSHADER,
		#fragmentShader = document.getElementById( 'noise2D_lib_fragmentshader' ).textContent + document.getElementById( 'noise2D_fragmentshader' ).textContent,
		fragmentShader = LAMBERT_NOISE_FSHADER,
		transparent  =	false,
		vertexColors = THREE.VertexColors,
		lights = true
	))

	return shaderMaterial
```

custom shader for the water mesh `THREE.Water`

```rusthon
#backend:javascript

def func_scs(material):
	this.material = material
	this.material.uniforms.mirrorSampler.value = this.texture
	this.material.uniforms.textureMatrix.value = this.textureMatrix
	this.material.uniforms.alpha.value = this.alpha
	this.material.uniforms.time.value = this.time
	this.material.uniforms.normalSampler.value = this.normalSampler
	this.material.uniforms.sunColor.value = this.sunColor
	this.material.uniforms.waterColor.value = this.waterColor
	this.material.uniforms.sunDirection.value = this.sunDirection
	this.material.uniforms.distortionScale.value = this.distortionScale
	this.material.uniforms.eye.value = this.eye
	this.updateTextureMatrix()
	this.render()

THREE.Water.prototype.set_custom_shader = func_scs
```

hacked `SKUNAMI.GpuHeightFieldWater` shader

```rusthon
#backend:javascript

def func():
	merge = [
		THREE.UniformsLib['lights'],
		THREE.UniformsLib['shadowmap'],
		THREE.ShaderLib['water'].uniforms,

		{
			'uTexture' : { 
				'type': 't', 
				'value': this.__rttRenderTarget1 
			},
			'uTexelSize' : { 
				'type': 'v2', 
				'value': new(THREE.Vector2(this.__texelSizeX, this.__texelSizeY))
			},
			'uTexelWorldSize' : { 
				'type': 'v2', 
				'value': 
				new(THREE.Vector2(this.__segmentSize, this.__segmentSize))
			},
			'uHeightMultiplier' : { 
				'type': 'f', 
				'value': 1.0 
			},
			'uBaseColor' : { 
				'type': 'v3', 
				'value': new(THREE.Vector3(0.45, 0.95, 1.0))
			}
		}
	]
	this.__mesh.material = new(THREE.ShaderMaterial(
		uniforms = THREE.UniformsUtils.merge( merge ),
		vertexShader = CustomHeightMapShader,
		fragmentShader = THREE.ShaderLib['water'].fragmentShader,
		lights = false,
		depthWrite = true,
		transparent = true
	))
SKUNAMI.GpuHeightFieldWater.prototype.__setupVtf = func
```

customized height map shader

```rusthon
#backend:javascript


CustomHeightMapShader = """

    uniform mat4 textureMatrix;
    uniform float time;
    varying vec4 mirrorCoord;
    varying vec3 worldPosition;


uniform sampler2D uTexture;
uniform vec2 uTexelSize;
uniform vec2 uTexelWorldSize;
uniform float uHeightMultiplier;

varying vec3 vViewPos;
varying vec3 vViewNormal;
varying vec2 vUv;

void main() {
    vUv = uv;
    vec4 t = texture2D(uTexture, vUv) * uHeightMultiplier;
    vec3 displacedPos = vec3(position.x, t.r, position.z);

        mirrorCoord = modelMatrix * vec4( displacedPos, 1.0 );
        worldPosition = mirrorCoord.xyz;
        mirrorCoord = textureMatrix * mirrorCoord;


    vec2 du = vec2(uTexelSize.r, 0.0);
    vec2 dv = vec2(0.0, uTexelSize.g);
    vec3 vecPosU = vec3(displacedPos.x + uTexelWorldSize.r,
                        texture2D(uTexture, vUv + du).r * uHeightMultiplier,
                        displacedPos.z) - displacedPos;
    vec3 vecNegU = vec3(displacedPos.x - uTexelWorldSize.r,
                        texture2D(uTexture, vUv - du).r * uHeightMultiplier,
                        displacedPos.z) - displacedPos;
    vec3 vecPosV = vec3(displacedPos.x,
                        texture2D(uTexture, vUv + dv).r * uHeightMultiplier,
                        displacedPos.z - uTexelWorldSize.g) - displacedPos;
    vec3 vecNegV = vec3(displacedPos.x,
                        texture2D(uTexture, vUv - dv).r * uHeightMultiplier,
                        displacedPos.z + uTexelWorldSize.g) - displacedPos;
    vViewNormal = normalize(normalMatrix * 0.25 * (cross(vecPosU, vecPosV) + cross(vecPosV, vecNegU) + cross(vecNegU, vecNegV) + cross(vecNegV, vecPosU)));

    vec4 worldPosition_XXX = modelMatrix * vec4(displacedPos, 1.0);
    vec4 viewPos = modelViewMatrix * vec4(displacedPos, 1.0);
    vViewPos = viewPos.rgb;

    gl_Position = projectionMatrix * viewPos;


}"""
```

globals for screen size and water size.

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

enemy_kill_sound = Sound('hit-noise.mp3')
Enemies = []
class Enemy:
	def __init__(self, x=-40, y=10, z=0, radius=1, segments=16, rings=8):
		Enemies.append( self )

		self.active = false
		self.destroyed = false
		self.hit = false
		self.health = 10.0
		geometry = new(THREE.SphereGeometry( radius, segments, rings ))

		self.material = create_enemy_material()
		acolors = self.material.attributes.ca.value

		for i in range( geometry.vertices.length ):
			color = new(THREE.Color(0xff0000))
			acolors.push( color )
			self.material.attributes.size.value.push( 10 )

		self.sphere = new(THREE.ParticleSystem( geometry, self.material ))
		self.sphere.dynamic = true
		self.sphere.sortParticles = true
		self.sphere.renderDepth = -1
		self.sphere.position.set(x,y,z)


		scene.add( self.sphere )

		self.body = new(p2.Body(
			position=[x,y], 
			mass=2.0,
			fixedRotation = true
		))
		self.body.enemy = self
		self.body.motionState = p2.Body.DYNAMIC
		self.body.gravityScale = 0.0

		shape = new(p2.Circle(radius))
		shape.material = PhysicsMaterials['enemy']
		self.body.addShape( shape )
		world.addBody( self.body )

	def update_ai(self):
		self.avoid = false
		#self.body.updateAABB()
		for mesh in SyncMeshes:
			if mesh._body.motionState == p2.Body.DYNAMIC:
				body = mesh._body
				#print p2.vec2.distance(self.body.position, body.position)
				if p2.vec2.distance(self.body.position, body.position) < 4.0:
					self.avoid = body
					break



	def update(self, time):
		self.update_ai()

		if self.hit:
			self.hit -= 1
			self.material.uniforms.color.value.setRGB(1,1,1)
		else:
			self.material.uniforms.color.value.setRGB(0,0,0)

		self.material.uniforms.color.needsUpdate = true

		asizes = self.material.attributes.size.value
		for i in range( asizes.length ):
			asizes[i] = Math.sin(0.1*i*time) *1.4
		self.material.attributes.size.needsUpdate = true

		if self.hit:
			pass

		elif not self.active:
			self.body.velocity[0] = Math.sin(time) * 3.0
			#if Math.random() > 0.5:
			#else:
			#	self.body.velocity[0] = 3

			self.sphere.rotation.y += 0.02
			self.sphere.rotation.z += 0.02

			self.sphere.position.x = self.body.position[0]
			self.sphere.position.y = self.body.position[1]


		elif self.avoid:
			if Math.random() > 0.5:
				if self.body.position[0] < self.avoid.position[0]:
					self.body.velocity[0] = -2
				else:
					self.body.velocity[0] = 2

			self.sphere.position.x = self.body.position[0]
			self.sphere.position.y = self.body.position[1]
			self.sphere.rotation.y += 0.1
			self.sphere.rotation.z += 0.1

		elif self.health > 0.0:
			self.sphere.rotation.y += 0.02
			self.sphere.rotation.z += 0.02

			self.sphere.position.x = self.body.position[0]
			self.sphere.position.y = self.body.position[1]

			if Math.random() > 0.5:
				px = player.center.position[0]
				py = player.center.position[1]
				x = self.sphere.position.x
				y = self.sphere.position.y
				if x < px and Math.random() > 0.5:
					self.body.velocity[0] = 10
					self.body.velocity[1] = 0

				elif x > px and Math.random() > 0.5:
					self.body.velocity[0] = -10
					self.body.velocity[1] = 0

				elif y < py and Math.random() > 0.5:
					self.body.velocity[1] = 5
					self.body.velocity[0] = 0
				elif y > py and Math.random() > 0.5:
					self.body.velocity[1] = -5
					self.body.velocity[0] = 0
		elif self.health <= 0.0:
			if self.destroyed: self.destroy()
			self.sphere.scale.z *= 0.7
			self.sphere.scale.x = Math.random()
			if self.sphere.scale.z < 0.001:
				scene.remove(self.sphere)
				Enemies.remove( self )
		else:
			self.sphere.position.x = self.body.position[0]
			self.sphere.position.y = self.body.position[1]

	def destroy(self):
		self.destroyed = true
		enemy_kill_sound.play()
		world.removeBody(self.body)


	def on_touch(self, body, shape):
		if body.motionState == p2.Body.DYNAMIC:
			if hasattr(body,'player'):
				return
			a = p2.vec2.distance(self.body.velocity, body.velocity)
			if a > 10.0:
				self.hit += 5
				self.health = 0.0
				self.body.velocity[0] = body.velocity[0] * 3
				self.body.velocity[1] = body.velocity[1]
			elif a > 5.0:
				self.hit += 4
				self.health -= 4
				self.body.velocity[0] = body.velocity[0] * 2
				self.body.velocity[1] = body.velocity[1]


pins = [0, cloth.w]
ballSize = 20
ballPosition.set(0,-20,5)

Splashes = [
	new Sound('splash-drop.wav'),
	new Sound('splash-drift.wav'),
	new Sound('splash-tiny.wav'),
	new Sound('splash-thud.wav'),
	new Sound('splash-big.wav')
]

class Player:
	GRAB_KEYS = [20,65,83,68,70,71,72,74,75,76,186,222,13]
	ALT_MOVE_KEYS = [65, 68]

	def on_post_broadphase(self, pairs):
		rem = []
		for i in range(0,pairs.length, 2):
			a = pairs[i]
			b = pairs[i+1]


	def __init__(self, x=0.0, y=0.0, z=0.0):
		self.spawn_point = [x,y,z]
		self.foot_step_rate = 0.045
		self.left_foot = 0.0
		self.right_foot = 0.0

		self.sounds = {
			'jump'  :       new Sound('catlike.mp3'),
			'shoot' :       new Sound('hit-machine.mp3'),
			'bounce' :      new Sound('aping.mp3'),
			'damage' :      new Sound('aping.mp3'),
			'missle-hit' :  new Sound('reverse-blip.mp3'),
			'missle-hit-enemy' : new Sound('hit-club.mp3'),
		}
		self.root = new(THREE.Object3D())
		self.root.position.set(x,y,0.5)
		scene.add( self.root )

		self.reset(x=x, y=y, N=5, M=5, k=500)

		window.addEventListener('keydown', self.on_key_down.bind(this), false)
		window.addEventListener('keyup', self.on_key_up.bind(this), false)

		#world.on('postBroadphase', self.on_post_broadphase)

		clothMaterial = new(THREE.MeshLambertMaterial(
			color = 0xff0000,
			side  = THREE.DoubleSide
		))

		global clothGeometry
		clothGeometry = new(THREE.ParametricGeometry( clothFunction, cloth.w, cloth.h ))
		clothGeometry.dynamic = true
		clothGeometry.computeFaceNormals()

		object = new(THREE.Mesh( clothGeometry, clothMaterial ))
		object.rotation.x = Math.PI / 4
		object.scale.set(0.05, 0.05, 0.05)
		object.castShadow = true
		object.receiveShadow = true
		self.root.add( object )
		self.cape = object

		self.throwing = None
		self.grab = false
		self.holding = None
		self.damage = 0.0
		self.head_attached = true
		self.flexing = false
		self.powerup = 0.0
		self.jump_pull = 0.0
		self._shoot = 0.0
		self.moving = false
		self.aim = 'FORWARD'
		self.projectiles = []
		self._pvert_index = 0
		self._pvert_max = 100
		self.ax = 0.0
		self.ay = 0.0
		self.spinning = false
		self.head_radius = 0.5

		self.constraints = []

		geom = new(THREE.Geometry())
		geom.vertices.append( new(THREE.Vector3()) )
		self.glow_material = 	new(THREE.ParticleSystemMaterial(
			size  = 20, 
			color = 0xffff44,
			map   = snowball_sprite,
			depthTest = false,
			depthWrite = false,
			transparent = true,
			opacity = 0.4
		))
		self.glow = new(THREE.ParticleSystem(
			geom, 
			self.glow_material
		))
		self.root.add( self.glow )
		self.glow.visible = false

		mat = new(THREE.MeshLambertMaterial(color=0xffffff))
		geom = new(THREE.ParametricGeometries.SphereGeometry(self.head_radius, 12, 12))
		geom.mergeVertices()
		geom.computeVertexNormals()
		#geom.vertices[0].z=0  ## mouth hole

		self.head = new(THREE.Mesh(geom, mat))
		self.head.position.z = 0.5
		self.head.scale.y = 0.8
		self.root.add( self.head )

		mat = new(THREE.MeshBasicMaterial(color=0x000000))
		geom = new(THREE.ParametricGeometries.SphereGeometry(0.1, 8, 8))
		self.left_eye = new(THREE.Mesh(geom, mat))
		self.head.add( self.left_eye )
		self.left_eye.position.z=0.6
		self.left_eye.position.x=-0.12
		self.left_eye.position.y = 0.3

		geom = new(THREE.ParametricGeometries.SphereGeometry(0.09, 8, 8))
		self.right_eye = new(THREE.Mesh(geom, mat))
		self.head.add( self.right_eye )
		self.right_eye.position.z=0.6
		self.right_eye.position.x=0.12
		self.right_eye.position.y = 0.32

		geom = new(THREE.ParametricGeometries.SphereGeometry(0.2, 8, 8))
		self.mouth = new(THREE.Mesh(geom, mat))
		self.mouth.scale.z = 0.6
		self.head.add( self.mouth )



		self.missle_material = 	new(THREE.ParticleSystemMaterial(
			size  = 5, 
			color = 0xffff44,
			map   = snowball_sprite,
			depthTest = false,
			transparent = true
		))


		geom = new(THREE.Geometry())
		for i in range(self._pvert_max):
			v = new(THREE.Vector3(-1000,-1000,0))
			geom.vertices.push( v )
		self.particles = new(THREE.ParticleSystem(
			geom, 
			self.missle_material
		))
		self.particles.dynamic = True
		scene.add( self.particles )

		x = self.spawn_point[0]-0.25
		y = self.spawn_point[1]-0.25
		self.center = new(p2.Body(
			position=[x,y], 
			mass=100.0,
			fixedRotation = true
		))
		self.center.player = self
		self.center.motionState = p2.Body.DYNAMIC	#KINEMATIC
		self.center.gravityScale = 2.25

		shape = new(p2.Circle(0.4))
		shape.material = PhysicsMaterials['player']
		self.center.addShape( shape )
		world.addBody( self.center )

		for body in self.bodies:
			spring = new(p2.Spring(
				self.center,body,
				stiffness=100,
				restLength=p2.vec2.distance(self.center.position, body.position),
				damping=10
			))
			world.addSpring(spring)
			self.springs.append( spring )

			cns = new(p2.LockConstraint(
				self.center,
				body,
				localOffsetB=body.position,
				localAngleB=0,
				maxForce=0.5
			))
			world.addConstraint( cns )
			self.constraints.append( cns )


	def move_to(self, x,y,z):
		self.center.position[0] = x
		self.center.position[1] = y
		self.root.position.set(x,y,z)

	def splash(self, vel):
		try:
			if vel[1] < -10:
				Splashes[4].play()
			elif vel[1] < -6:
				Splashes[3].play()
			elif vel[1] < -4:
				Splashes[2].play()
			elif vel[1] < -2:
				Splashes[1].play()
			elif vel[1] < -1:
				Splashes[0].play()

		except:
			pass

	def update_move(self):
		if self.moving == 'BACKWARDS':
			self.head.rotation.y = -Math.PI / 3
			self.head.rotation.x = 0
			self.center.position[0] -= 0.3
			self.center.velocity[0] = -10
		elif self.moving == 'FORWARD':
			self.head.rotation.y = Math.PI / 3
			self.head.rotation.x = 0
			self.center.position[0] += 0.3
			self.center.velocity[0] = 10

		elif self.moving == 'UP':
			self.head.rotation.y = 0.0
			self.head.rotation.x = -Math.PI / 6
			if self.flexing is false:
				self.flexing = true
				self.center.position[1] -= 0.3
				self.center.velocity[1] -= 4
		elif self.moving == 'DOWN':
			self.head.rotation.y = 0.0


	def on_key_up(self, evt):
		#evt.preventDefault()

		key = evt.keyCode

		if key == 65: ## alt-left
			for b in self.bodies:
				b.velocity[0] -= 2
				b.position[0] -= 1

		#elif key == 87: ## alt-up
		#	self.center.velocity[1] += 1
		#elif key == 83: ## alt-down
		#	self.center.velocity[1] -= 1
		elif key == 68: ## alt-right
			for b in self.bodies:
				b.velocity[0] += 2
				b.position[0] += 1


		elif key == 37:  ## left
			self.moving = false
			self.center.velocity[0] = 1
		elif key == 39:  ## right
			self.moving = false
			self.center.velocity[0] = -1
		elif key == 38: ## up
			self.moving = false
			self.flexing = false

			self.grab = false
			if self.holding:
				print('throwing')
				world.removeConstraint( self.holding_cns )
				self.center.motionState = p2.Body.STATIC
				#self.holding.motionState = p2.Body.KINEMATIC
				self.static = 30  ## frames
				if self.ax < self.holding.position[0]:
					print('throw forward')
					self.holding.velocity[0] = 50
					self.throw_vector = [50,0]
				else:
					print('throw backwards')
					self.holding.velocity[0] = -50
					self.throw_vector = [-50,0]

				#self.holding.velocity[0] = self.center.velocity[0] * 20
				#self.holding.velocity[1] = self.center.velocity[1]
				#self.center.velocity[0] = -self.center.velocity[0] * 20
				#self.center.velocity[1] = -self.center.velocity[1]

				#if self.aim == 'FORWARD':
				#	print('throwing forward')
				#	self.holding.velocity[0] += 50.0
				#elif self.aim == 'BACKWARDS':
				#	print('throwing backward')
				#	self.holding.velocity[0] -= 50.0
				#else:
				#	'wrong aim'

				self.throwing = self.holding
				self.throw_ticks = 30
				self.holding = None

		elif key == 40: ## down
			self.moving = false
			self.center.position[1] -= 0.1
			self.center.velocity[1] = -2

		elif key == 32 or key == 20 or key == 83:  ## spacebar or capslock, or "s"
			self._shoot = 0.0
			self.powerup = 0.0

		else:
			self.sounds['jump'].play()
			self.jump_pull = 0.15
			if self.center.position[1] < 15:
				self.center.position[1] += 2
				self.center.velocity[1] = 12
				for body in self.bodies:
					body.position[1] += 1.5
					body.velocity[1] = 8


	def on_key_down(self, evt):
		#evt.preventDefault()

		if self.center.motionState != p2.Body.DYNAMIC:
			self.center.motionState = p2.Body.DYNAMIC
			self.static = 0

		key = evt.keyCode
		print(key)
		#if key in self.GRAB_KEYS:
		#	print('grab on')
		#	self.grab = true

		if key in Player.ALT_MOVE_KEYS:  ## self.ALT_MOVE_KEYS is broken
			pass

		elif key == 37:
			self.aim = self.moving = 'BACKWARDS'

		elif key == 39:
			self.aim = self.moving = 'FORWARD'

		elif key == 38:
			self.aim = self.moving = 'UP'
			self.grab = true

		elif key == 40:
			self.aim = self.moving = 'DOWN'

		elif key == 32 or key == 20 or key == 83:  ## space, capslock, or "s"
			self.sounds['shoot'].play()
			self.powerup += 0.1
			self.shoot()

		else:  ## jump
			self.center.velocity[1] -= 1

	def shoot(self):
		x = self.ax
		y = self.ay

		self._shoot = 0.1
		if self.aim == 'FORWARD':
			vel = [50,0]
			x += 1
		elif self.aim == 'BACKWARDS':
			vel = [-50,0]
			x -= 1
		elif self.aim == 'UP':
			vel = [0,50]
			y += 1
		elif self.aim == 'DOWN':
			vel = [0,-50]
			y -= 1

		self.missle_material.size = (Math.random()*5) + self.powerup + 3.0

		shape = new(p2.Particle())
		shape.material = PhysicsMaterials['missle']
		#x,y = self.center.position
		missle = new(p2.Body(
			position = [x,y+0.5],
			mass = 0.00001,
			velocity = vel
		))
		missle.on_missle_contact = self.on_missle_contact.bind(this)
		missle.addShape( shape )
		missle.shape = shape
		world.addBody( missle )
		self.projectiles.append( missle )

		vert = self.particles.geometry.vertices[ self._pvert_index ]
		self._pvert_index += 1
		if self._pvert_index >= self._pvert_max:
			self._pvert_index = 0
		missle.vertex = vert
		#self.particles.geometry.vertices.push( vert )

	def on_missle_contact(self, missle, body, shape):
		if shape.material == PhysicsMaterials['player']:
			return

		self.sounds['missle-hit'].play()

		missle.vertex.x = -1000
		missle.vertex.y = -1000

		self.projectiles.remove( missle )
		body.velocity[0] = 0
		body.velocity[1] = 0
		body.angularVelocity *= 0.1
		if missle.world:
			world.removeBody( missle )

		if hasattr(body,'enemy'):
			enemy = body.enemy
			enemy.hit = 2
			enemy.health -= 1.0

	def on_touch(self, body, shape):
		#print('on-touch', body)
		if hasattr(body, 'enemy'):
			print('hit enemy')
			if self.spin_attack:
				body.enemy.hit = 4
				body.enemy.health -= 2.0
				body.velocity[0] = self.center.velocity[0]*8
				if enemy.health <= 0.0:
					body.enemy.destroy()
			if self.center.position[1] > body.position[1]:
				pass
			else:

				if self.springs:
					print('removing springs!')
					for spring in self.springs:
						#spring = self.springs.pop()
						self.dead_springs.append( spring )
						world.removeSpring( spring )
					self.springs = []

					for cns in self.constraints:
						world.removeConstraint( cns )
					self.constraints = []

				else:
					print('ssnowman is springless')

				self.sounds['damage'].play()
				self.damage += 0.25

				self.mouth.position.z = 0.4
				self.mouth.scale.y = 1.0 + (Math.random()*Math.random())

				self.head.rotation.y = -(Math.PI / 6) * Math.random()
				self.head.rotation.x = -(Math.PI / 4) * Math.random()

				if body.velocity[0] < 0.0:
					push = -20
				else:
					push = 20

				for b in self.bodies:
					b.velocity[0] += (Math.random()-0.5)*100
					b.velocity[1] += (Math.random()-0.5)*20

				if self.damage > 10.0 and self.head_attached:
					self.detach_head()
					push *= 5

				self.center.velocity[0] = push

		elif shape.material is PhysicsMaterials['player-head'] and self.damage < 0.9:
			self.reattach_head()

		elif body.motionState == p2.Body.DYNAMIC:
			if shape.material == PhysicsMaterials['player-skin'] or shape.material == PhysicsMaterials['player']:
				pass

			elif self.grab and not self.holding:
				self.holding = body
				self.holding_cns = new(p2.LockConstraint(
					self.center,
					body,
					localOffset = p2.vec2.distance(self.center.position, body.position),
					localAngleB = 0.0
				))
				world.addConstraint( self.holding_cns )



	def reattach_head(self):
		self.head.position.x = 0.0
		scene.remove( self.head )
		self.root.add( self.head )
		self.head_attached = true
		try:
			world.removeBody( self.head_body )
		except:
			pass

	def detach_head(self):
		self.head_attached = false

		self.head_body = new(p2.Body(
			position=[self.head.position.x, self.head.position.y], 
			mass=20.0,
		))
		self.head_body.player = self
		self.head_body.motionState = p2.Body.DYNAMIC	#KINEMATIC
		self.head_body.gravityScale = 2.25
		self.head_body.velocity[1] = -10

		shape = new(p2.Circle( self.head_radius ))
		shape.material = PhysicsMaterials['player-head']
		self.head_body.addShape( shape )
		world.addBody( self.head_body )

		self.root.remove( self.head )
		scene.add( self.head )


	def reset(self, x=0.0, y=0.0, N=5, M=5, k=1000, d=10, l=0.35, m=1):
		self.bodies = []
		self.springs = []
		self.dead_springs = []
		self.N = N
		self.M = M
		bodies = []

		#// Create particle bodies
		particleShape = new(p2.Particle())
		particleShape.material = PhysicsMaterials['player-skin']
		for i in range(N):
			bodies.push([])
			for j in range(M):
				p = new(p2.Body(
					mass=m,
					position=[
						(i-N/2)*l*1.05+x, 
						((j-M/2)*l*1.05)+y
					]
				))
				p.addShape(particleShape)
				bodies[i].push(p)
				world.addBody(p)
				self.bodies.append(p)
				p.player = self

		#// Vertical springs
		for i in range(N):
			for j in range(M-1):
				bodyA = bodies[i][j];
				bodyB = bodies[i][j+1];
				spring = new(p2.Spring(
					bodyA,bodyB,
					stiffness=k,
					restLength=l,
					damping=d
				))
				world.addSpring(spring)
				self.springs.append( spring )

		#// Horizontal springs
		for i in range(N-1):
			for j in range(M):
				bodyA = bodies[i][j];
				bodyB = bodies[i+1][j];
				spring = new( p2.Spring(
					bodyA,bodyB,
					stiffness=k,
					restLength=l,
					damping=d
				))
				world.addSpring(spring)
				self.springs.append( spring )

		#// Diagonal right/down springs
		for i in range(N-1):
			for j in range(M-1):
				a = bodies[i][j]
				b = bodies[i+1][j+1]
				spring = new(p2.Spring(
					a,b,
					stiffness=k,
					restLength=Math.sqrt(l*l + l*l)
				))
				world.addSpring(spring)
				self.springs.append( spring )

		#// Diagonal left/down springs
		for i in range(N-1):
			for j in range(M-1):
				a = bodies[i+1][j]
				b = bodies[i][j+1]
				spring = new(p2.Spring(
					a,b,
					stiffness=k,
					restLength=Math.sqrt(l*l + l*l)
				))
				world.addSpring(spring)
				self.springs.append( spring )


		self.material = blobMaterial = new(
			THREE.MeshPhongMaterial( color=0xffff00 )
		)

		self.marching_cubes = blob = new(
			THREE.MarchingCubes(16, blobMaterial, True, True )
		)
		blob.position.set( 0, 0, 1 )
		blob.scale.set( 2.5, 2.5, 4 )
		blob.enableUvs = False
		blob.enableColors = False
		blob.castShadow = true
		blob.receiveShadow = true

		self.root.add( blob )

	def update(self, time, delta):

		if self.throwing:
			self.throwing.velocity[0] = self.throw_vector[0]
			self.throwing.velocity[1] = self.throw_vector[1]

			self.throw_ticks -= 1
			if not self.throw_ticks:
				self.throwing = None


		if self.center.motionState != p2.Body.DYNAMIC:
			if self.static: self.static -= 1
			if not self.static:
				self.center.motionState = p2.Body.DYNAMIC


		self.damage *= 0.9
		if self.damage < 0.1:
			self.mouth.position.z = 0

		vx = self.center.velocity[0]
		vy = self.center.velocity[1]
		windForce.set(-vx*25, -vy*10, -vy)

		particles = cloth.particles
		geom = self.cape.geometry
		for i in range(particles.length):
			geom.vertices[ i ].copy( particles[i].position )

		geom.vertices[ 0 ].x = -5
		geom.vertices[ 5 ].x = 5

		geom.computeFaceNormals()
		geom.computeVertexNormals()
		geom.normalsNeedUpdate = true
		geom.verticesNeedUpdate = true


		if self.moving:
			self.update_move()

		for missle in self.projectiles:
			missle.vertex.x = missle.position[0]
			missle.vertex.y = missle.position[1]
		self.particles.geometry.verticesNeedUpdate = true

		if self.jump_pull == 0.0:
			pass
		elif self.jump_pull > 0.00001:
			if self.jump_pull > 0.01 and abs(self.center.velocity[0]) > 2:
				if self.center.velocity[0] < 0.0:
					self.center.velocity[0] -= 5
				else:
					self.center.velocity[0] += 5
				self.spinning = true
				print('spin')

			self.jump_pull *= 0.5
			self.center.velocity[1] -= 1
			print('jump pull')

		if abs(self.center.velocity[0]) < 1 and self.spinning:
			self.spinning = false
			#self.cape.rotation.z = 0.0
			#self.cape.rotation.x = Math.PI / 4

		if self.spinning and abs(self.center.velocity[0]) > 10.0:
			self.root.rotation.x += time * 0.03
			self.spin_attack = true
			self.glow.visible = true
		else:
			self.root.rotation.x = 0.0
			self.spin_attack = false
			self.glow.visible = false

		blob = self.marching_cubes
		blob.reset()

		ax = 0.0
		ay = 0.0
		heights = []
		widths = []

		numblobs = self.N * self.M
		for body in self.bodies:
			ax += body.position[0]
			ay += body.position[1]
			heights.append( body.position[1] )
			widths.append( body.position[0] )
		ax /= numblobs
		ay /= numblobs
		self.ax = ax
		self.ay = ay

		self.root.position.x = ax
		self.root.position.y = ay
		#self.cape.position.set( ax, ay, 0 )

		top = max(heights)
		bottom = min(heights)
		height = top - bottom
		xmin = min(widths)
		xmax = max(widths)

		if self.head_attached:
			#self.head.position.x = ax
			self.head.position.y = height*0.7
		else:
			self.head.position.x = self.head_body.position[0]
			self.head.position.y = self.head_body.position[1]


		if Math.random() > 0.93:
			self.left_eye.scale.y = 0.1
			self.right_eye.scale.y = 0.1
		elif self.jump_pull:
			self.left_eye.scale.y = 1.5
			self.right_eye.scale.y = 1.5
		elif self._shoot:
			self.left_eye.scale.y = 0.5
			self.right_eye.scale.y = 0.5
		else:
			self.left_eye.scale.y = 1
			self.right_eye.scale.y = 1

		if Math.random() > 0.98:
			if self.aim == 'FORWARD':
				self.head.rotation.y = Math.PI / 4
			elif self.aim == 'BACKWARDS':
				self.head.rotation.y = -Math.PI / 4
			elif Math.random() > 0.5:
				self.head.rotation.y = -Math.random() * Math.random() * 0.5
			else:
				self.head.rotation.y = Math.random() * Math.random() * 0.5

		elif Math.random() > 0.99:
			if self.aim == 'FORWARD':
				self.head.rotation.y = Math.PI / 3
			elif self.aim == 'BACKWARDS':
				self.head.rotation.y = -Math.PI / 3
			else:
				self.head.rotation.y = 0

		height += 2.0
		scale = (10 / height) + 2
		blob.scale.z = 4
		blob.position.z = 0.5

		z = 0.5
		strength = 0.05
		for i,body in enumerate(self.bodies):
			x = body.position[0] - ax
			y = body.position[1] - ay
			x *= 0.2
			y *= 0.2
			#if i == 0 or i == self.N:
			#	blob.addBall(x+0.5,y+0.5,z, strength*3, 0.001)
			#else:
			blob.addBall(x+0.5,y+0.5,z, strength, 0.001)

		if self.flexing:
			pass

		if self._shoot > 0.0001:
			self._shoot *= 0.5
			xmin = -ax
			xmin *= 0.2
			xmin += 0.5

			xmax = -ax
			xmax *= 0.2
			xmax += 0.5

			if self.aim == 'FORWARD':
				blob.addBall(0.7, 0.6, z, strength*5, 0.001)
				blob.addBall(0.8, 0.6, z, strength*3, 0.001)


			elif self.aim == 'UP':
				blob.addBall(0.3, 0.8, z, strength*3, 0.001)
				blob.addBall(0.7, 0.8, z, strength*3, 0.001)

				blob.addBall(0.3, 0.7, z, strength*5, 0.001)
				blob.addBall(0.7, 0.7, z, strength*5, 0.001)

			elif self.aim == 'DOWN':
				blob.addBall(0.2, 0.4, z, strength*3, 0.001)
				blob.addBall(0.8, 0.4, z, strength*3, 0.001)

				blob.addBall(0.3, 0.5, z, strength*5, 0.001)
				blob.addBall(0.7, 0.5, z, strength*5, 0.001)


			else:
				blob.addBall(0.3, 0.6, z, strength*5, 0.001)
				blob.addBall(0.2, 0.6, z, strength*3, 0.001)

		y = (bottom-ay) * 0.2
		if self.moving == 'FORWARD' or self.moving == 'BACKWARDS':
			#self.left_foot = Math.sin(time)*0.1
			#self.right_foot = Math.sin(time+0.5)*0.1
			self.left_foot -= self.foot_step_rate
			self.right_foot += self.foot_step_rate
			if self.left_foot < -0.15 or self.right_foot < -0.15:
				self.foot_step_rate = -self.foot_step_rate

			blob.addBall(self.left_foot+0.5,y+0.4,z+0.05, 0.2, 0.001)
			blob.addBall(self.right_foot+0.5,y+0.4,z-0.05, 0.2, 0.001)
		elif self.moving == 'UP':
			blob.addBall(0.45,y+0.4,z+0.05, 0.1, 0.001)
			blob.addBall(0.55,y+0.4,z-0.05, 0.1, 0.001)
		else:
			blob.addBall(0.55,y+0.4,z+0.05, 0.1, 0.001)
			blob.addBall(0.45,y+0.4,z-0.05, 0.1, 0.001)

		return [ax,ay]

WaterHF = None
def create_gpu_water(renderer, camera, scene, light):
	global WaterHF, waterMesh, water

	waterGeom = new(THREE.PlaneGeometry(WATER_SIZE[0], WATER_SIZE[1], WATER_RES[0] - 1, WATER_RES[1] - 1))
	waterGeom.applyMatrix(new(THREE.Matrix4()).makeRotationX(-Math.PI / 2))
	waterMesh = new(THREE.Mesh(waterGeom, null))
	scene.add(waterMesh)


	gpuXWater = new(SKUNAMI.GpuXWater(
		renderer = renderer,
		scene = scene,
		mesh = waterMesh,  ## sets material on mesh ##
		size = WATER_SIZE,
		res = WATER_RES,
		dampingFactor = 0.95,
		multisteps = 2,
		meanHeight = MEAN_WATER_HEIGHT
	))

	waterNormals = new(
		THREE.ImageUtils.loadTexture( 'waternormals.jpg' )
	)
	waterNormals.wrapS = waterNormals.wrapT = THREE.RepeatWrapping

	## texture size must be square for custom shader to work ##
	water = new(THREE.Water(
		renderer, 
		camera, 
		scene, 
		textureWidth=512, 
		textureHeight=512,
		waterNormals=waterNormals,
		alpha=0.9,
		sunDirection=light.position.clone().normalize(),
		sunColor=0xffffff,
		waterColor=0x001e0f,
		distortionScale=5.0
	))

	water.set_custom_shader( waterMesh.material )
	waterMesh.add( water )

	WaterHF = gpuXWater  ## TODO test other gpu water types, collision objects, etc.
	#WaterHF.reset()
	#WaterHF.setShouldDisplayWaterTexture(true)
	return waterMesh



############################################################################
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

def main():
	print 'enter main'
	g = Game()
	print 'animate game'
	g.animate()


```