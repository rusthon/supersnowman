# supersnowman

<a href="http://www.youtube.com/watch?feature=player_embedded&v=walJbBM8Ams" target="_blank"><img src="http://img.youtube.com/vi/walJbBM8Ams/0.jpg" alt="IMAGE ALT TEXT HERE" width="640" height="350" border="1" /></a>

Build and Run
-------------
`rusthon.py SuperSnowman.md --run=server.py --data=./data,./libs`

Source Code
-----------
The source code is contained in a single large markdown file that contains:
html, javascript, and python.
https://github.com/rusthon/supersnowman/blob/master/SuperSnowman.md

Blender Exporter
----------------
save your blender file into `./data` as `mygame.blend`,
the exporter is hard coded to save `mygame.json` that the Tornado server uses.
```bash
cd data
blender --python=snowman_exporter.py
```