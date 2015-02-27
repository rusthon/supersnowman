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


```
