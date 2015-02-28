HTML
-------

@main.html
```html
<html>
<head>
<link href="libs/css/bootstrap.css" rel="stylesheet"/>
<link href="libs/css/darkstrap.css" rel="stylesheet"/>

<script src="libs/pythonjs.js"></script>

<script src="libs/p2.js/p2.min.js"></script>
<script src="libs/p2.js/p2.extras.js"></script>
<script src="libs/pixi.js/pixi.dev.js"></script>

<script src="libs/jquery/jquery-latest.js"></script>
<script src="libs/bootstrap/bootstrap.min.js"></script>

<script src="libs/p2.js/Demo.js"></script>
<script src="libs/p2.js/PixiDemo.js"></script>

<script src="libs/three.js/three.min.js"></script>
<script src="libs/three.js/controls/TrackballControls.js"></script>

<script src="libs/three.js/shaders/CopyShader.js"></script>
<script src="libs/three.js/shaders/FXAAShader.js"></script>
<script src="libs/three.js/shaders/HorizontalTiltShiftShader.js"></script>
<script src="libs/three.js/shaders/VerticalTiltShiftShader.js"></script>

<script src="libs/three.js/postprocessing/EffectComposer.js"></script>
<script src="libs/three.js/postprocessing/RenderPass.js"></script>
<script src="libs/three.js/postprocessing/BloomPass.js"></script>
<script src="libs/three.js/postprocessing/ShaderPass.js"></script>
<script src="libs/three.js/postprocessing/MaskPass.js"></script>
<script src="libs/three.js/postprocessing/SavePass.js"></script>

<script src="libs/three.js/MarchingCubes.js"></script>
<script src="libs/three.js/Mirror.js"></script>
<script src="libs/three.js/WaterShader.js"></script>
<script src="libs/three.js/ShaderGodRays.js"></script>

<script type="text/javascript" src="libs/skparallelreduce/skparallelreduce.js"></script>
<script type="text/javascript" src="libs/skunami.js/skunami.min.js"></script>


<script src="libs/three.js/UVsUtils.js"></script>

<script src="libs/three.js/ParametricGeometries.js"></script>
<script src="libs/three.js/modifiers/SubdivisionModifier.js"></script>
<script src="libs/three.js/Cloth.js"></script>

<script src="libs/three.js/stats.min.js"></script>

<script id="noise_vertexshader" type="x-shader/x-vertex">

#ifdef USE_COLOR
	varying vec3 vColor;
#endif

	varying vec3 vUv;
	uniform float scale;

	void main( void ) {

		#ifdef USE_COLOR
			#ifdef GAMMA_INPUT
				vColor = color * color;
			#else
				vColor = color;
			#endif
		#endif

		vUv = position*scale;
		gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );

	}

</script>


<script type="x-shader/x-fragment" id="noise2D_lib_fragmentshader">
//
// Description : Array and textureless GLSL 2D simplex noise function.
//      Author : Ian McEwan, Ashima Arts.
//  Maintainer : ijm
//     Lastmod : 20110822 (ijm)
//     License : Copyright (C) 2011 Ashima Arts. All rights reserved.
//               Distributed under the MIT License. See LICENSE file.
//               https://github.com/ashima/webgl-noise
// 

varying vec3 vUv;

vec3 mod289(vec3 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec2 mod289(vec2 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec3 permute(vec3 x) {
  return mod289(((x*34.0)+1.0)*x);
}

float snoise(vec2 v)
  {
  const vec4 C = vec4(0.211324865405187,  // (3.0-sqrt(3.0))/6.0
                      0.366025403784439,  // 0.5*(sqrt(3.0)-1.0)
                     -0.577350269189626,  // -1.0 + 2.0 * C.x
                      0.024390243902439); // 1.0 / 41.0
// First corner
  vec2 i  = floor(v + dot(v, C.yy) );
  vec2 x0 = v -   i + dot(i, C.xx);

// Other corners
  vec2 i1;
  //i1.x = step( x0.y, x0.x ); // x0.x > x0.y ? 1.0 : 0.0
  //i1.y = 1.0 - i1.x;
  i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
  // x0 = x0 - 0.0 + 0.0 * C.xx ;
  // x1 = x0 - i1 + 1.0 * C.xx ;
  // x2 = x0 - 1.0 + 2.0 * C.xx ;
  vec4 x12 = x0.xyxy + C.xxzz;
  x12.xy -= i1;

// Permutations
  i = mod289(i); // Avoid truncation effects in permutation
  vec3 p = permute( permute( i.y + vec3(0.0, i1.y, 1.0 ))
		+ i.x + vec3(0.0, i1.x, 1.0 ));

  vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy), dot(x12.zw,x12.zw)), 0.0);
  m = m*m ;
  m = m*m ;

// Gradients: 41 points uniformly over a line, mapped onto a diamond.
// The ring size 17*17 = 289 is close to a multiple of 41 (41*7 = 287)

  vec3 x = 2.0 * fract(p * C.www) - 1.0;
  vec3 h = abs(x) - 0.5;
  vec3 ox = floor(x + 0.5);
  vec3 a0 = x - ox;

// Normalise gradients implicitly by scaling m
// Approximation of: m *= inversesqrt( a0*a0 + h*h );
  m *= 1.79284291400159 - 0.85373472095314 * ( a0*a0 + h*h );

// Compute final noise value at P
  vec3 g;
  g.x  = a0.x  * x0.x  + h.x  * x0.y;
  g.yz = a0.yz * x12.xz + h.yz * x12.yw;
  return 130.0 * dot(m, g);
}
</script>

<script type="x-shader/x-fragment" id="noise2D_fragmentshader">

#ifdef USE_COLOR
	varying vec3 vColor;
#endif


void main( void ) {
	float n = snoise(vUv.xy)*0.05;
	vec3 h = vUv*12.0;
	n += snoise( h.xy )*0.05;
	gl_FragColor = vec4( vec3( vColor.x+n, vColor.y+n, vColor.z ), 1.0 );// + vec4( vColor, 1.0 );

}
</script>


<script type="x-shader/x-fragment" id="noise3D_fragmentshader">
//
// Description : Array and textureless GLSL 2D/3D/4D simplex 
//               noise functions.
//      Author : Ian McEwan, Ashima Arts.
//  Maintainer : ijm
//     Lastmod : 20110822 (ijm)
//     License : Copyright (C) 2011 Ashima Arts. All rights reserved.
//               Distributed under the MIT License. See LICENSE file.
//               https://github.com/ashima/webgl-noise
// 

vec3 mod289(vec3 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 mod289(vec4 x) {
  return x - floor(x * (1.0 / 289.0)) * 289.0;
}

vec4 permute(vec4 x) {
     return mod289(((x*34.0)+1.0)*x);
}

vec4 taylorInvSqrt(vec4 r)
{
  return 1.79284291400159 - 0.85373472095314 * r;
}

float snoise(vec3 v)
  { 
  const vec2  C = vec2(1.0/6.0, 1.0/3.0) ;
  const vec4  D = vec4(0.0, 0.5, 1.0, 2.0);

// First corner
  vec3 i  = floor(v + dot(v, C.yyy) );
  vec3 x0 =   v - i + dot(i, C.xxx) ;

// Other corners
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min( g.xyz, l.zxy );
  vec3 i2 = max( g.xyz, l.zxy );

  //   x0 = x0 - 0.0 + 0.0 * C.xxx;
  //   x1 = x0 - i1  + 1.0 * C.xxx;
  //   x2 = x0 - i2  + 2.0 * C.xxx;
  //   x3 = x0 - 1.0 + 3.0 * C.xxx;
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy; // 2.0*C.x = 1/3 = C.y
  vec3 x3 = x0 - D.yyy;      // -1.0+3.0*C.x = -0.5 = -D.y

// Permutations
  i = mod289(i); 
  vec4 p = permute( permute( permute( 
             i.z + vec4(0.0, i1.z, i2.z, 1.0 ))
           + i.y + vec4(0.0, i1.y, i2.y, 1.0 )) 
           + i.x + vec4(0.0, i1.x, i2.x, 1.0 ));

// Gradients: 7x7 points over a square, mapped onto an octahedron.
// The ring size 17*17 = 289 is close to a multiple of 49 (49*6 = 294)
  float n_ = 0.142857142857; // 1.0/7.0
  vec3  ns = n_ * D.wyz - D.xzx;

  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);  //  mod(p,7*7)

  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_ );    // mod(j,N)

  vec4 x = x_ *ns.x + ns.yyyy;
  vec4 y = y_ *ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);

  vec4 b0 = vec4( x.xy, y.xy );
  vec4 b1 = vec4( x.zw, y.zw );

  //vec4 s0 = vec4(lessThan(b0,0.0))*2.0 - 1.0;
  //vec4 s1 = vec4(lessThan(b1,0.0))*2.0 - 1.0;
  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));

  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy ;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww ;

  vec3 p0 = vec3(a0.xy,h.x);
  vec3 p1 = vec3(a0.zw,h.y);
  vec3 p2 = vec3(a1.xy,h.z);
  vec3 p3 = vec3(a1.zw,h.w);

//Normalise gradients
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2, p2), dot(p3,p3)));
  p0 *= norm.x;
  p1 *= norm.y;
  p2 *= norm.z;
  p3 *= norm.w;

// Mix final noise value
  vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot( m*m, vec4( dot(p0,x0), dot(p1,x1), 
                                dot(p2,x2), dot(p3,x3) ) );
  }

float surface( vec3 coord ) {

	float n = 0.0;

	n += 0.5 * abs( snoise( coord ) );
	//n += 0.5 * abs( snoise( coord * 8.0 ) );
	//n += 0.5 * abs( snoise( coord * 16.0 ) );
	n += 0.5 * abs( snoise( coord * 32.0 ) );

	return n;

}

varying vec3 vUv;
void main( void ) {

	//float n = surface( vUv );
	float n = snoise(vUv);
	gl_FragColor = vec4( vec3( 1.0, n,n ), 1.0 );

}

</script>


<script type="x-shader/x-vertex" id="vertexshader">

	attribute float size;
	attribute vec3 ca;

	varying vec3 vColor;

	void main() {

		vColor = ca;
		vec4 mvPosition = modelViewMatrix * vec4( position, 1.0 );
		gl_PointSize = size * ( 300.0 / length( mvPosition.xyz ) );
		gl_Position = projectionMatrix * mvPosition;

	}

</script>

<script type="x-shader/x-fragment" id="fragmentshader">

	uniform vec3 color;
	uniform sampler2D texture;

	varying vec3 vColor;

	void main() {

		gl_FragColor = vec4( color * vColor, 1.0 );
		gl_FragColor = gl_FragColor * texture2D( texture, gl_PointCoord );

	}
</script>

<script type="text/javascript">


var sunPosition = new THREE.Vector3( 0, 1000, -1000 );
var screenSpacePosition = new THREE.Vector3();
var postprocessing = {};
var bgColor = 0x0000ff;
var sunColor = 0x0000ff;
var materialDepth;
var projector = new THREE.Projector();
var SnowFlakes = [];


var sprite1 = THREE.ImageUtils.loadTexture( "snowflake1.png" );
var sprite2 = THREE.ImageUtils.loadTexture( "snowflake2.png" );
var sprite3 = THREE.ImageUtils.loadTexture( "snowflake3.png" );
var sprite4 = THREE.ImageUtils.loadTexture( "snowflake4.png" );
var sprite5 = THREE.ImageUtils.loadTexture( "snowflake5.png" );

var snowball_sprite = THREE.ImageUtils.loadTexture( "snowball.png" );

function create_snowflakes( scene ) {
	geometry = new THREE.Geometry();


	for ( i = 0; i < 3000; i ++ ) {

		var vertex = new THREE.Vector3();
		vertex.x = Math.random() * 2000 - 1000;
		vertex.y = Math.random() * 2000 - 1000;
		vertex.z = Math.random() * 2000 - 1000;

		geometry.vertices.push( vertex );

	}

	parameters = [ [ [1.0, 0.2, 0.5], sprite2, 20 ],
				   [ [0.95, 0.1, 0.5], sprite3, 15 ],
				   [ [0.90, 0.05, 0.5], sprite1, 10 ],
				   [ [0.85, 0, 0.5], sprite5, 8 ],
				   [ [0.80, 0, 0.5], sprite4, 5 ],
				   ];

	var materials = [];
	for ( i = 0; i < parameters.length; i ++ ) {

		color  = parameters[i][0];
		sprite = parameters[i][1];
		size   = parameters[i][2];

		materials[i] = new THREE.ParticleSystemMaterial( { size: size, map: sprite, blending: THREE.AdditiveBlending, depthTest: false, transparent : true } );
		materials[i].color.setHSL( color[0], color[1], color[2] );

		particles = new THREE.ParticleSystem( geometry, materials[i] );

		particles.rotation.x = Math.random() * 6;
		particles.rotation.y = Math.random() * 6;
		particles.rotation.z = Math.random() * 6;

		scene.add( particles );
		SnowFlakes.push( particles );

	}

}

function init_godrays() {
	materialDepth = new THREE.MeshDepthMaterial();

	postprocessing.scene = new THREE.Scene();

	postprocessing.camera = new THREE.OrthographicCamera( SCREEN_WIDTH / - 2, SCREEN_WIDTH / 2,  SCREEN_HEIGHT / 2, SCREEN_HEIGHT / - 2, -10000, 10000 );
	postprocessing.camera.position.z = 100;

	postprocessing.scene.add( postprocessing.camera );

	var pars = { minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter, format: THREE.RGBFormat };
	postprocessing.rtTextureColors = new THREE.WebGLRenderTarget( SCREEN_WIDTH, SCREEN_HEIGHT, pars );

	// Switching the depth formats to luminance from rgb doesn't seem to work. I didn't
	// investigate further for now.
	// pars.format = THREE.LuminanceFormat;

	// I would have this quarter size and use it as one of the ping-pong render
	// targets but the aliasing causes some temporal flickering

	postprocessing.rtTextureDepth = new THREE.WebGLRenderTarget( SCREEN_WIDTH, SCREEN_HEIGHT, pars );

	// Aggressive downsize god-ray ping-pong render targets to minimize cost

	var w = SCREEN_WIDTH / 4.0;
	var h = SCREEN_HEIGHT / 4.0;
	postprocessing.rtTextureGodRays1 = new THREE.WebGLRenderTarget( w, h, pars );
	postprocessing.rtTextureGodRays2 = new THREE.WebGLRenderTarget( w, h, pars );

	// god-ray shaders

	var godraysGenShader = THREE.ShaderGodRays[ "godrays_generate" ];
	postprocessing.godrayGenUniforms = THREE.UniformsUtils.clone( godraysGenShader.uniforms );
	postprocessing.materialGodraysGenerate = new THREE.ShaderMaterial( {

		uniforms: postprocessing.godrayGenUniforms,
		vertexShader: godraysGenShader.vertexShader,
		fragmentShader: godraysGenShader.fragmentShader

	} );

	var godraysCombineShader = THREE.ShaderGodRays[ "godrays_combine" ];
	postprocessing.godrayCombineUniforms = THREE.UniformsUtils.clone( godraysCombineShader.uniforms );
	postprocessing.materialGodraysCombine = new THREE.ShaderMaterial( {

		uniforms: postprocessing.godrayCombineUniforms,
		vertexShader: godraysCombineShader.vertexShader,
		fragmentShader: godraysCombineShader.fragmentShader

	} );

	var godraysFakeSunShader = THREE.ShaderGodRays[ "godrays_fake_sun" ];
	postprocessing.godraysFakeSunUniforms = THREE.UniformsUtils.clone( godraysFakeSunShader.uniforms );
	postprocessing.materialGodraysFakeSun = new THREE.ShaderMaterial( {

		uniforms: postprocessing.godraysFakeSunUniforms,
		vertexShader: godraysFakeSunShader.vertexShader,
		fragmentShader: godraysFakeSunShader.fragmentShader

	} );

	postprocessing.godraysFakeSunUniforms.bgColor.value.setHex( bgColor );
	postprocessing.godraysFakeSunUniforms.sunColor.value.setHex( sunColor );

	postprocessing.godrayCombineUniforms.fGodRayIntensity.value = 0.5;

	postprocessing.quad = new THREE.Mesh( new THREE.PlaneGeometry( SCREEN_WIDTH, SCREEN_HEIGHT ), postprocessing.materialGodraysGenerate );
	postprocessing.quad.position.z = -9900;
	postprocessing.scene.add( postprocessing.quad );


}

function render_godrays( clear_target ) {

	// Find the screenspace position of the sun

	screenSpacePosition.copy( sunPosition );
	projector.projectVector( screenSpacePosition, camera );

	screenSpacePosition.x = ( screenSpacePosition.x + 1 ) / 2;
	screenSpacePosition.y = ( screenSpacePosition.y + 1 ) / 2;

	// Give it to the god-ray and sun shaders

	postprocessing.godrayGenUniforms[ "vSunPositionScreenSpace" ].value.x = screenSpacePosition.x;
	postprocessing.godrayGenUniforms[ "vSunPositionScreenSpace" ].value.y = screenSpacePosition.y;

	postprocessing.godraysFakeSunUniforms[ "vSunPositionScreenSpace" ].value.x = screenSpacePosition.x;
	postprocessing.godraysFakeSunUniforms[ "vSunPositionScreenSpace" ].value.y = screenSpacePosition.y;

	// -- Draw sky and sun --

	// Clear colors and depths, will clear to sky color

	if (clear_target) {
		renderer.clearTarget( postprocessing.rtTextureColors, true, true, false );
	} else {
		renderer.clearDepth();
		//renderer.clearStencil();
	}

	// Sun render. Runs a shader that gives a brightness based on the screen
	// space distance to the sun. Not very efficient, so i make a scissor
	// rectangle around the suns position to avoid rendering surrounding pixels.

	var sunsqH = 0.74 * SCREEN_HEIGHT; // 0.74 depends on extent of sun from shader
	var sunsqW = 0.74 * SCREEN_HEIGHT; // both depend on height because sun is aspect-corrected

	screenSpacePosition.x *= SCREEN_WIDTH;
	screenSpacePosition.y *= SCREEN_HEIGHT;

	renderer.setScissor( screenSpacePosition.x - sunsqW / 2, screenSpacePosition.y - sunsqH / 2, sunsqW, sunsqH );
	renderer.enableScissorTest( true );

	postprocessing.godraysFakeSunUniforms[ "fAspect" ].value = SCREEN_WIDTH / SCREEN_HEIGHT;

	postprocessing.scene.overrideMaterial = postprocessing.materialGodraysFakeSun;
	renderer.render( postprocessing.scene, postprocessing.camera, postprocessing.rtTextureColors );

	renderer.enableScissorTest( false );

	// -- Draw scene objects --

	// Colors

	scene.overrideMaterial = null;
	renderer.render( scene, camera, postprocessing.rtTextureColors );

	// Depth

	scene.overrideMaterial = materialDepth;
	renderer.render( scene, camera, postprocessing.rtTextureDepth, true );

	// -- Render god-rays --

	// Maximum length of god-rays (in texture space [0,1]X[0,1])

	var filterLen = 1.0;

	// Samples taken by filter

	var TAPS_PER_PASS = 6.0;

	// Pass order could equivalently be 3,2,1 (instead of 1,2,3), which
	// would start with a small filter support and grow to large. however
	// the large-to-small order produces less objectionable aliasing artifacts that
	// appear as a glimmer along the length of the beams

	// pass 1 - render into first ping-pong target

	var pass = 1.0;
	var stepLen = filterLen * Math.pow( TAPS_PER_PASS, -pass );

	postprocessing.godrayGenUniforms[ "fStepSize" ].value = stepLen;
	postprocessing.godrayGenUniforms[ "tInput" ].value = postprocessing.rtTextureDepth;

	postprocessing.scene.overrideMaterial = postprocessing.materialGodraysGenerate;

	renderer.render( postprocessing.scene, postprocessing.camera, postprocessing.rtTextureGodRays2 );

	// pass 2 - render into second ping-pong target

	pass = 2.0;
	stepLen = filterLen * Math.pow( TAPS_PER_PASS, -pass );

	postprocessing.godrayGenUniforms[ "fStepSize" ].value = stepLen;
	postprocessing.godrayGenUniforms[ "tInput" ].value = postprocessing.rtTextureGodRays2;

	renderer.render( postprocessing.scene, postprocessing.camera, postprocessing.rtTextureGodRays1  );

	// pass 3 - 1st RT

	pass = 3.0;
	stepLen = filterLen * Math.pow( TAPS_PER_PASS, -pass );

	postprocessing.godrayGenUniforms[ "fStepSize" ].value = stepLen;
	postprocessing.godrayGenUniforms[ "tInput" ].value = postprocessing.rtTextureGodRays1;

	renderer.render( postprocessing.scene, postprocessing.camera , postprocessing.rtTextureGodRays2  );

	// final pass - composite god-rays onto colors

	postprocessing.godrayCombineUniforms["tColors"].value = postprocessing.rtTextureColors;
	postprocessing.godrayCombineUniforms["tGodRays"].value = postprocessing.rtTextureGodRays2;

	postprocessing.scene.overrideMaterial = postprocessing.materialGodraysCombine;

	renderer.render( postprocessing.scene, postprocessing.camera );
	postprocessing.scene.overrideMaterial = null;


}



function create_enemy_material() {
	var attributes = {

		size: {	type: 'f', value: [] },
		ca:   {	type: 'c', value: [] }

	};

	var uniforms = {

		amplitude: { type: "f", value: 1.0 },
		color:     { type: "c", value: new THREE.Color( 0x0000ff ) },
		texture:   { type: "t", value: THREE.ImageUtils.loadTexture( "disc.png" ) },

	};

	uniforms.texture.value.wrapS = uniforms.texture.value.wrapT = THREE.RepeatWrapping;

	var shaderMaterial = new THREE.ShaderMaterial( {

		uniforms: 		uniforms,
		attributes:     attributes,
		vertexShader:   document.getElementById( 'vertexshader' ).textContent,
		fragmentShader: document.getElementById( 'fragmentshader' ).textContent,
		transparent:	true

	});

	return shaderMaterial;
}


var LAMBERT_NOISE_VSHADER = [
	'varying vec3 vUv;',
	'uniform float scale;',

	"#define LAMBERT",

	"varying vec3 vLightFront;",

	"#ifdef DOUBLE_SIDED",

		"varying vec3 vLightBack;",

	"#endif",

	THREE.ShaderChunk[ "map_pars_vertex" ],
	THREE.ShaderChunk[ "lightmap_pars_vertex" ],
	THREE.ShaderChunk[ "envmap_pars_vertex" ],
	THREE.ShaderChunk[ "lights_lambert_pars_vertex" ],
	THREE.ShaderChunk[ "color_pars_vertex" ],
	THREE.ShaderChunk[ "morphtarget_pars_vertex" ],
	THREE.ShaderChunk[ "skinning_pars_vertex" ],
	THREE.ShaderChunk[ "shadowmap_pars_vertex" ],

	"void main() {",

		THREE.ShaderChunk[ "map_vertex" ],
		THREE.ShaderChunk[ "lightmap_vertex" ],
		THREE.ShaderChunk[ "color_vertex" ],

		THREE.ShaderChunk[ "morphnormal_vertex" ],
		THREE.ShaderChunk[ "skinbase_vertex" ],
		THREE.ShaderChunk[ "skinnormal_vertex" ],
		THREE.ShaderChunk[ "defaultnormal_vertex" ],

		THREE.ShaderChunk[ "morphtarget_vertex" ],
		THREE.ShaderChunk[ "skinning_vertex" ],
		THREE.ShaderChunk[ "default_vertex" ],

		THREE.ShaderChunk[ "worldpos_vertex" ],
		THREE.ShaderChunk[ "envmap_vertex" ],
		THREE.ShaderChunk[ "lights_lambert_vertex" ],
		THREE.ShaderChunk[ "shadowmap_vertex" ],

		'vUv = position*scale;',
		//'vUv.y *= 0.1;'
	"}"

].join("\n");

var LAMBERT_NOISE_FSHADER = [
	document.getElementById( 'noise2D_lib_fragmentshader' ).textContent,

	"uniform float opacity;",

	"varying vec3 vLightFront;",

	"#ifdef DOUBLE_SIDED",

		"varying vec3 vLightBack;",

	"#endif",

	THREE.ShaderChunk[ "color_pars_fragment" ],
	THREE.ShaderChunk[ "map_pars_fragment" ],
	THREE.ShaderChunk[ "lightmap_pars_fragment" ],
	THREE.ShaderChunk[ "envmap_pars_fragment" ],
	THREE.ShaderChunk[ "fog_pars_fragment" ],
	THREE.ShaderChunk[ "shadowmap_pars_fragment" ],
	THREE.ShaderChunk[ "specularmap_pars_fragment" ],

	"void main() {",

		"gl_FragColor = vec4( vec3 ( 1.0 ), opacity );",

		THREE.ShaderChunk[ "map_fragment" ],
		THREE.ShaderChunk[ "alphatest_fragment" ],
		THREE.ShaderChunk[ "specularmap_fragment" ],

		"#ifdef DOUBLE_SIDED",

			"if ( gl_FrontFacing )",
				"gl_FragColor.xyz *= vLightFront;",
			"else",
				"gl_FragColor.xyz *= vLightBack;",

		"#else",

			"gl_FragColor.xyz *= vLightFront;",

		"#endif",

		THREE.ShaderChunk[ "lightmap_fragment" ],
		THREE.ShaderChunk[ "color_fragment" ],
		THREE.ShaderChunk[ "envmap_fragment" ],
		THREE.ShaderChunk[ "shadowmap_fragment" ],

		THREE.ShaderChunk[ "linear_to_gamma_fragment" ],

		THREE.ShaderChunk[ "fog_fragment" ],

		'float n = snoise(vUv.xy)*0.2;',
		'vec3 h = vUv*12.0;',
		'n += snoise( h.xy )*0.1;',
		'gl_FragColor *= vec4( vec3( vColor.x+n, vColor.y+n, (n*0.5)+vColor.z ), 1.0 );',

	"}"

].join("\n");

</script>

<@SuperSnowmanCode>

</head>
<body onload="javascript:main()">

<div class="well span" id="three_container"></div>
<div class="well" id="demo_container"></div>

<p>
<div class="navbar">
	<button class="btn btn-warning" onclick="javascript:demo.setState(Demo.DEFAULT)">move</button>
	<button class="btn" onclick="javascript:demo.setState(Demo.DRAWPOLYGON)">draw shape</button>
	<button class="btn" onclick="javascript:toggle_camera()">camera</button>
	<button class="btn" onclick="javascript:open_blender()">blender</button>
	<input type="checkbox" checked="true" onclick="javascript:toggle_pixi(this.checked)">2D View</input>
	<input type="checkbox" onclick="javascript:SPAWN_ENEMIES=this.checked">spawn enemies</input>

</div>
<p/>


</body>
</html>
```
