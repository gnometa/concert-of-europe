# Religion modding

Source: https://vic2.paradoxwikis.com/Religion_modding

To add a religion, you must make changes to several files: the religion definition file, the graphics file that holds religious icons, and the graphics definition file.

### common/religion.txt

Found at `common/religion.txt`, the religions in the game are defined as religious groups and their constituent religions. Each religion has a defined `icon` and `color`. Note that the color is defined as an RGB value with values from 0 to 1, as opposed to 0 to 255. The color is used to represent said religion is pie charts.

```
pagan = {
	animist = {
		icon = 14
		color = { 0.5 0.0 0.0 }
		pagan = yes
		
	}
}
```

The `pagan = yes` is exclusive to the animist religion. It is unknown what this line does - perhaps it is just a remnant of Europa Universalis 3 code.

### Graphics

The icons are are defined in files: `gfx/interface/icon_religion.dds` and `gfx/interface/icon_religion_small.dds`. The icons are 32 x 32 in size and are defined horizontally sequentially. The `icon` number in the religion definition relates directly to the elements in the graphical file.

The graphical files are being called from two interface definition files: `interface/core.gfx` and `interface/general_gfx.gfx`. If you add more religions to the game, you must also tell these interface files that the icon graphics is longer than they expect, to do this, simply find the places where the religious icons are being loaded and specify the exact number of "frames" are in the image.

```
spriteType = {
	name = "GFX_icon_religion_small"
	texturefile = "gfx\\interface\\icon_religion_small.tga"
	noOfFrames = 13
	loadType = "INGAME"
}
```

```
spriteType = {
	name = "GFX_icon_religion"
	texturefile = "gfx\\interface\\icon_religion.tga"
	noOfFrames = 14
	norefcount = yes
}
```

The question of why `noOfFrames` is smaller in the `_small` graphics file is left as an exercise for the reader.
