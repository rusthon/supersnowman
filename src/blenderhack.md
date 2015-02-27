Source Code
-------
This is a Blender Python script that gets run below by the Tornado server,
it is saved as `blenderhack.py`.  In the output tar archive.

@blenderhack.py
```python
import bpy, json, urllib.request, urllib.parse

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
	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			for reg in area.regions:
				if reg.type == 'WINDOW':
					return reg.callback_add( on_redraw, (reg,), 'POST_PIXEL' )

handle = attach_on_redraw_callback()
```
