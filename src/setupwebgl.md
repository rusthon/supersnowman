Setup Three.js
--------------

Creates camera and controls for camera, main THREE.js scene, lights, etc..
The WebGLRenderer is also created here.

```rusthon
#backend:javascript

def init_threejs( game ):
	global scene, renderer, camera, controls

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

	setup_dom_container(renderer, controls)
	setup_rendertarget(renderer, scene, camera, light)

```


WebGLRenderer
-------------

```rusthon
#backend:javascript

def setup_rendertarget(renderer, scene, camera, light):
	global composer

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

	effectFXAA.renderToScreen = true;
	composer.addPass( renderModel );
	composer.addPass( effectFXAA );

	#vblur.renderToScreen = true;
	#composer.addPass( hblur );
	#composer.addPass( vblur );

	skybox = create_skybox( scene )
	#rscene.add( skybox )

	water_mesh = create_gpu_water( renderer, camera, scene, light )
	water_mesh.position.y -= 1
	#scene.add( water_mesh )

	create_snowflakes( scene )
	generate_glaicers()

```


attach to html domElement
-------------------------
attaches to domElement #three_container
also attaches to mouse enter/leave events.

```rusthon
#backend:javascript
def setup_dom_container(renderer, controls):
	global stats

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
```



