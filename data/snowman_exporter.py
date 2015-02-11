## this script is run with blender ##
'''
blender --python snowman_exporter.py

'''

GAME_BLEND  = 'mygame.blend'
JSON_OUTPUT = 'mygame.json'

import os, sys, json
import bpy, mathutils
import urllib.request, urllib.parse

def new_level( root, name=None, shared=None ):
	'''
	the game needs to know if a level flow is left to right, or right to left
	(for the simple triggers).  this assumes that player spawn points are always
	on the right or left of a level, so the level always is played the same direction.
	'''
	triggers = {}
	instances = {}
	enemies = {}
	exits = {}
	level = {
		'name' : name,
		'uid'  : root.name,
		'instances': instances,
		'triggers' : triggers,  ## fast check if player X > trigger X then fire one time
		'exits'   : exits,      ## gets a special 'EXIT' p2.js material, can be empty: cube, sphere
		'enemies' : enemies,
	}

	for ob in root.children:
		name = ob.name
		print('exporting->',name)

		pos = ob.location.copy()
		level['instances'][ob.name] = instance = {
			'name' : ob.name,
			'position':pos.to_tuple(), 
			'rotation': tuple(ob.rotation_euler),
			'scale':ob.scale.to_tuple(),
			'type':ob.type,
			'physics' : ob.game.physics_type,
			'actor' : ob.game.use_actor,
			'collision' : not ob.game.use_ghost,
			'mass' : ob.game.mass,
			'visible' : not ob.hide_render,
		}
		if ob.type == 'EMPTY':
			instances.pop( ob.name )  ## empties are not normal instances
			instance['size'] = ob.empty_draw_size
			instance['draw_type'] = ob.empty_draw_type


			if len(ob.constraints):
				targets = []       ## allow multiple exits ##
				for cns in ob.constraints:
					if cns.target:
						targets.append( cns.target )
				assert targets
				instance['targets'] = [ 
					dict(level=target.name, position=target.location.to_tuple())
					for target in targets
				]

			if ob.name=='self' or ob.name.startswith('self.'):
				triggers[ob.name] = instance
				

			elif ob.empty_draw_type == 'PLAIN_AXES':
				## chained signals can be used to spawn and then activate an enemy ##
				triggers[ ob.name ] = instance
				instance['signals'] = signals = {}  ## group name (signal name) : objects
				for group in ob.users_group:
					print('signal group->', group)
					signals[ group.name ] = []
					for child in group.objects:
						if child.name == ob.name: continue
						signals[group.name].append( child.name )

			elif ob.empty_draw_type == 'SINGLE_ARROW':
				assert len(ob.children)==1
				jumpto = ob.children[0]
				loc = jumpto.matrix_worldspace.decompose()[0]
				if loc.z not in _levels:
					print('making new level')

			else:
				enemies[ ob.name ] = instance

		elif ob.type == 'LAMP':
			instances[ob.name]['light'] = {
				'type':ob.data.type,
				'energy':ob.data.energy,
				'color':tuple(ob.data.color),
				'distance': ob.data.distance,
			}
		elif ob.type == 'CURVE' and len(ob.data.splines) == 1:
			if len(ob.data.materials):
				instances[ob.name]['material'] = ob.data.materials[0].name
			else:
				instances[ob.name]['material'] = None


			instances[ob.name]['data'] = ob.data.name
			instances[ob.name]['extrude'] = ob.data.extrude
			instances[ob.name]['bevel'] = ob.data.bevel_depth


			if ob.data.name not in shared['curves']:
				assert len(ob.data.splines) == 1

				shared['curves'][ob.data.name] = points = []
				ob.data.dimensions = '2D'
				ob.data.extrude = 0.0
				ob.data.bevel_depth = 0.0
				bpy.context.scene.update()  ## this is required to update the bounding boxes

				v1 = mathutils.Vector( tuple(ob.bound_box[0]) )


				bpy.context.scene.objects.active = ob
				ob.select = True
				bpy.ops.object.origin_set(
					type='GEOMETRY_ORIGIN', 
					center= 'BOUNDS' #'MEDIAN'
				)

				v2 = mathutils.Vector( ob.bound_box[0] )
				d = v2-v1
				if d.x or d.y or d.z:
					if ob.rotation_euler.z:
						raise RuntimeError( 'object %s with offset center can not be rotated' %ob )
					ob.location -= d

				instances[ob.name]['position'] = ob.location.to_tuple()

				mod = ob.modifiers.new(name='temp', type='DECIMATE')
				assert mod.decimate_type == 'COLLAPSE'
				mod.ratio = 0.5
				mod.show_viewport = True
				mod.show_render = True

				## poll bad context? ##
				#bpy.ops.object.convert(target='MESH', keep_original=False)
				#for vert in ob.data.vertices:
				#	points.append( vert.co.to_tuple() )

				mesh = ob.to_mesh(
					scene = bpy.context.scene, 
					apply_modifiers = True,
					settings = 'PREVIEW'
				)

				for vert in mesh.vertices:
					points.append( vert.co.to_tuple() )
				ob.select = False

		elif ob.type == 'CURVE':
			instances.pop( ob.name )

	for name in instances:
		a = instances[name]
		if 'data' in a:
			assert a['data'] in shared['curves']
			assert 'material' in a

	return level

def break_apart_curve(ob):
	bpy.context.scene.objects.active = ob
	ob.select = True
	bpy.ops.object.mode_set( mode='EDIT' )
	for spline in ob.data.splines:
		for bez in spline.bezier_points:
			bez.select_control_point = False
	#for i in range( len(ob.data.splines)-1 ):
	#	spline = ob.data.splines[0]
	while len(ob.data.splines) > 1:
		spline = ob.data.splines[0]
		spline.bezier_points[0].select_control_point = True
		bpy.ops.curve.separate()
	bpy.ops.object.mode_set( mode='OBJECT' )

def export():
	## shared level data ##
	materials = {}

	dump = {
		'curves' : {},
		'materials' : materials,
		'player'    : None,
		'blend_file': os.path.abspath(bpy.context.blend_data.filepath)
	}

	dump['levels'] = levels = {
		'main' : [None]*10,
		'secrets' : {}
	}


	bpy.context.scene.update()

	for m in bpy.data.materials:
		materials[ m.name ] = {
			'name' : m.name,
			'diffuse' : tuple(m.diffuse_color)
		}


	roots = set()
	for ob in bpy.data.objects:
		ob.select = False
		if ob.empty_draw_type == 'CONE':
			player = {
				'position' : ob.location.to_tuple()
			}
			dump['player'] = player
		elif ob.type == 'EMPTY' and not ob.parent:
			roots.add( ob )


	for root in roots:
		for ob in root.children:
			#if ob.type == 'CURVE' and len(ob.data.splines) > 1:
			#	break_apart_curve()
			## TODO reprent the new objects to the root ##
			pass

	bpy.context.scene.update()  ## this is required to update the bounding boxes
	for ob in bpy.data.objects:
		ob.select = False


	for root in roots:
		if root.name.startswith('level.'):
			postfix = root.name.split('.')[-1]
			if postfix.isnumeric():
				levels['main'][ int(postfix) ] = new_level( root, name=postfix, shared=dump )
			else:
				levels['secrets'][ root.name ] = new_level( root, name=postfix, shared=dump )

	assert levels['main'][0]
	assert dump['player']
	open( JSON_OUTPUT, 'wb' ).write( json.dumps( dump, indent=2, separators=(',', ': ') ).encode('utf-8') )
	bpy.ops.wm.save_as_mainfile(
		filepath = 'debug-mygame.blend',
		check_existing = False
	)
	return True



def on_redraw(reg):
	ob = bpy.context.active_object
	if not ob: return
	msg = {
		'name':ob.name,
		'position': ob.location.to_tuple(),
		'scale': ob.scale.to_tuple(),
		'rotation': tuple(ob.rotation_euler)
	}
	urllib.request.urlopen(
		'http://localhost:8080/blenderhack', 
		data=urllib.parse.urlencode( {'message':json.dumps(msg)}).encode('utf-8')
	)


def attach_on_redraw_callback():
	bpy.context.scene.update()

	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			for reg in area.regions:
				if reg.type == 'WINDOW':
					return reg.callback_add( on_redraw, (reg,), 'POST_PIXEL' )


## load game blend and export ##

handle = attach_on_redraw_callback()
assert handle


bpy.ops.wm.open_mainfile(
	filepath = GAME_BLEND,
	load_ui=False,
)

assert export()

#bpy.ops.wm.quit_blender()


