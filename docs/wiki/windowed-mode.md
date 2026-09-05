# Windowed mode

Source: https://vic2.paradoxwikis.com/Windowed_mode

Many players wish to play in **windowed mode** (that is, the game is not maximized in the screen). This can have various advantages, namely that the player can continue to do other tasks while his game is running without having to minimize. This can be especially useful to modders. 

To play the game in windowed mode instead of full screen, access the hard drive that you installed Victoria II to. Navigate to Program Files, then to "Paradox Games," "Paradox Interactive," or to whatever similarly named folder contains your Paradox selections. Access Victoria 2, then find the "settings.txt" file. This should be in the base Victoria 2 folder, somewhere near the bottom. 

Open the settings file, and you should see a variety of settings, but nestled somewhere near the top should be:

```
fullScreen=yes
```

Change this to:

```
fullScreen=no
```

Your game will now operate in windowed mode. Enjoy!

### (Pseudo) Fullscreen Borderless Windowed Mode

To play the game in a pseudo-fullscreen borderless window, set the *settings.txt* as above, but keep the size exactly the same as your desktop display size. Once you do this the game will be awkwardly positioned, but a utility such as [Gamers Window Relocator](http://gwr.orekaria.com/) will automatically move the game window to the correct position and over the taskbar, giving you a fullscreen borderless window effect. This will allow you to play the game in fullscreen, but still retaining the ease and functionality of Alt-Tab.
