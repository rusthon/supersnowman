Player Class
------------


```rusthon
#backend:javascript


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
			size  = 15, 
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
			size  = 10, 
			color = 0xffff44,
			map   = snowball_sprite,
			depthTest = false,
			#transparent = true
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
			mass=50.0,
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
			position = [x,y+1.5],
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
			print 'shot self'
			return

		print 'missle hit something'
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
			THREE.MarchingCubes(24, blobMaterial, True, True )
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
			print missle.vertex
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
			self.head.position.y = height*0.8
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

		else:
			blob.addBall(0.25, (ay*0.01)+0.5, z+0.05, strength*3, 0.001)
			blob.addBall(0.75, (ay*0.01)+0.5, z+0.05, strength*3, 0.001)
			blob.addBall(0.35, 0.45, z-0.1, strength*3, 0.001)
			blob.addBall(0.65, 0.45, z-0.1, strength*3, 0.001)


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

```