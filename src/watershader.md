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
