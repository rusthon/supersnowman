# supersnowman

<a href="http://www.youtube.com/watch?feature=player_embedded&v=walJbBM8Ams" target="_blank"><img src="http://img.youtube.com/vi/walJbBM8Ams/0.jpg" alt="IMAGE ALT TEXT HERE" width="640" height="350" border="1" /></a>

Build and Run
-------------
`rusthon.py SuperSnowman.md --run=server.py --data=./data,./libs`


Blender Exporter
----------------
save your blender file into `./data` as `mygame.blend`,
the exporter is hard coded to save `mygame.json` that the Tornado server uses.
```bash
cd data
blender --python=snowman_exporter.py
```

Source Code
-----------
The source code is in several markdown modules, the toplevel markdown that imports them is:
[SuperSnowman.md](https://github.com/rusthon/supersnowman/blob/master/SuperSnowman.md)

Modules
-------
* [blenderhack.md](src/blenderhack.md)
* [server.md](src/server.md)
* [mainhtml.md](src/mainhtml.md)
* [iceshader.md](src/iceshader.md)
* [watershader.md](src/watershader.md)
* [hmapshader.md](src/hmapshader.md)
* [sound.md](src/sound.md)
* [enemy.md](src/enemy.md)
* [player.md](src/player.md)
* [helperfuncs.md](src/helperfuncs.md)
* [setupwebgl.md](src/setupwebgl.md)
* [gameengine.md](src/gameengine.md)

