Helper Functions
--------------

```rusthon
#backend:javascript

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



def toggle_camera():
	global AUTO_CAMERA
	if AUTO_CAMERA:
		AUTO_CAMERA = false
	else:
		AUTO_CAMERA = true


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