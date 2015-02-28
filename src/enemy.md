Enemy Class
-----------


```rusthon
#backend:javascript

enemy_kill_sound = Sound('hit-noise.mp3')
Enemies = []
class Enemy:
	def __init__(self, x=-40, y=10, z=0, radius=2, segments=16, rings=8):
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

```
