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

SCREEN_WIDTH = 760
SCREEN_HEIGHT = 500

WATER_SIZE = [100,100];
WATER_RES = [256,256];
#WATER_GRID_SIZE = WATER_SIZE / WATER_RES;
MEAN_WATER_HEIGHT = 0.0;
WATER_FLOOD_RATE = 0.0;
WATER_SOURCE_AMOUNT = 0.2;
WATER_SOURCE_RADIUS = 0.7;
WATER_SINK_AMOUNT = 0.5;
WATER_SINK_RADIUS = 0.7;

AUTO_CAMERA = True
SPAWN_ENEMIES = false
USE_POSTPROC = True
clock = new(THREE.Clock())
time = 0.0


demo = None
world = None
Blobs = []
blob = None

scene = None
renderer = None
camera = None
SyncMeshes = []
Glaicers = []
WaterHF = None
USE_PIXI = true

uvGenerator = new(THREE.UVsUtils.CylinderUVGenerator())

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

```

Extra Markdown Imports
----------------------
* [@import iceshader.md](src/iceshader.md)
* [@import watershader.md](src/watershader.md)
* [@import hmapshader.md](src/hmapshader.md)
* [@import sound.md](src/sound.md)
* [@import enemy.md](src/enemy.md)
* [@import player.md](src/player.md)
* [@import helperfuncs.md](src/helperfuncs.md)
* [@import setupwebgl.md](src/setupwebgl.md)
* [@import gameengine.md](src/gameengine.md)



```rusthon
#backend:javascript

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


	demo = new(PixiDemo(world, width=320,height=440, lineWidth=2.0, scrollFactor=0.01, pixelsPerLengthUnit=32, run=false))
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