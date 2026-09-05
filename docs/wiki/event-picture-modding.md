# Event picture modding

Source: https://vic2.paradoxwikis.com/Event_picture_modding

This is a method for creating quick and dirty event pictures using the free utility, [Paint.NET](http://www.getpaint.net/) that look reasonably good next to the Paradox pictures. (If you own a more advanced graphics program you'll be able to create even better pictures, with nice airbrushing and fading effects that Paint.NET doesn't feature.)

### Find an appropriate picture

Naturally, a good source of pictures for both PI and modders is [Wikipedia](http://wikipedia.org) and its sister site [Wikimedia Commons](http://commons.wikimedia.org). 

#### Good places to find pictures

- Archival sites
  - [U.S. National Archives](http://archives.gov/)
  - [British National Archives](http://www.nationalarchives.gov.uk/)
  - [Archives Canada](http://www.archivescanada.ca/)
  - [National Archives of Australia](http://naa.gov.au/)
- School library websites
- Other student resources - schools and universities also often have access to digital archive services where you can find pictures

#### Tips for choosing a picture

- Generally Paradox Interactive seems to prefer **line drawings, cartoons and paintings** to photographs.
- Look for **long and thin landscape pictures** wherever possible, and go for the **highest resolution** you can find (they're easier to resize). All event pictures are sized **521 pixels by 203 pixels**. If your picture is too small you may have to copy in another image to fill in the space.
- If your picture has a plain white background, such as a poster or other document, try overlaying it over the image **gfx\interface\event_country_background.dds** (which is the parchment-like background texture of the event screen)
- Choose something appropriate to the pre-1936 period of course. :P
- If you have mad photoshop skills, you can get creative with tricks such as adding text next to a person's portrait which PI used for some of the author events, see e.g. *Emerson.tga* and *Tocqueville.tga* in the Victoria 2\gfx\pictures\events folder.

This tutorial will be using Henry Arthur McArdle's painting, [*The Battle of San Jacinto*](http://en.wikipedia.org/wiki/File:The_Battle_of_San_Jacinto_(1895).jpg).

### Get your pic into Paint.NET and recolor it

Save the picture and open it in Paint.NET. 

If you keep the event picture the same colour as the original source, it'll stick out like a sore thumb next to the sepia-toned vanilla pictures. A neat trick here is to find your game folder (for example, C:\Program Files\Paradox Interactive\Victoria 2\) and browse to the gfx\pictures\events folder. Open one of the images in Paint.NET, which supports TGA files. Find the **Color Picker** tool (the eyedropper icon, shortcut: K) and choose a fairly dark brown portion of the image.

Next, use these menu options to re-colour your image.
1. Adjustments > Black and White (shortcut Ctrl+Shift+G): this is so the color is washed out.
1. Effects > Color > Color Filter: Click the box with the active foreground color, to the left of the color wheel, and the settings will be automatically applied.

Now you have a nice sepia-toned picture. If you're doing many pictures at once, you can use the Ctrl+F shortcut or 'Repeat Color Filter' under the Effects menu to speed the process up.

### Resize your picture to 521x203

Try changing the size to 521 pixels wide (Image > Resize or Ctrl+R), then use Rectangle Select (the dotted square tool, shortcut S) to measure out a box that is 203 pixels tall - the size of the rectangle is indicated in the status bar. You can then use the Move Selection tools or drag the mouse to adjust the selection. Finally, go to Image > Crop to Selection (Ctrl+Shift+X). Voila, a 521x203 image!

### Add the border as a new layer

Save the above PNG file somewhere on your computer where you can drag it straight into Paint.NET over your source image. A Drag and Drop dialog box will appear. Choose "Add layer".

As you will see, the border isn't pretty and the edges need extra retouching (see below). Try using Filters > Blurs > True Blur to soften the sharp edges of the frame. Since the BlankEventFrame layer should still be selected by default, only the border will blur; if it doesn't, look in the Layers window to ensure that "Background" is not the active layer.

### Save your image

Event pictures go in the **Victoria 2\gfx\pictures\events** directory. Save the image as a TGA file (use the dropdown in the Save box) - the default format settings are OK. You'll be prompted to "flatten" the image from two layers to one: go ahead and do it. Now you're done!

### Use your image in an event

It couldn't be easier to use your new image: when writing events, use the line **picture = "xxx"** where xxx is the filename of your TGA file. For example, **picture = "SanJacinto"**

<gallery caption="Making event pictures: a gallery" widths="200px" heights="200px">
File:The Battle of San Jacinto (1895).jpg|The source image.
File:Event pictures open file.jpg|How it looks when open in Paint.NET.
File:Event pictures eyedropper.jpg|Here I have opened "VictoriaWedding.tga" and used the color picker on the part of the background highlighted by red. In the Colors box you can see the corresponding RGB values, which you can enter directly if you want to skip this step.
File:Event pictures Color Filter dialog.jpg|Using the Color Filter window.
File:Event pictures Resize dialog.jpg|Resizing the image before cropping it.
File:Event pictures Drag and drop dialog.jpg|Choose "Add Layer" and the border will frame your image.
File:Event pictures rough borders.jpg|The edges look rough. Just a few more steps!
File:Event pictures Finished.jpg|The finished product
</gallery>
