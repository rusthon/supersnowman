Ice shader using GPU 2D noise

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
