# Checksum

Source: https://vic2.paradoxwikis.com/Checksum

A **checksum** is a means by which a computer confirms the contents of a file. If, when the computer runs the checksum test over the file, it comes to a different checksum value than what is suspected, it lets the computer know that the file is modified in some way from what is expected. (Such mismatches in a checksum could be due to corruption of the file or even computer viruses.)

In the case of Victoria 2, Paradox uses checksums to let players know their games have been installed correctly, and also as a way to ensure players are using compatible versions when playing in multiplayer games.

### Finding the checksum

The checksum will appear in the lower left corner of the main screen next to the version number.

### Usage in installation

Players can check the checksum to ensure their games were installed correctly. If, after launching the game, a different checksum is shown compared to what is expected, the player knows that their copy of the game may be missing key components or is corrupted in some way. The player may need to reinstall the game in order to achieve the correct checksum.

### Use in multiplayer

Players using the multiplayer game features need to compare their games to make sure that all players share the same checksum. If any of the players have a different checksum, their games are incompatible and the multiplayer game cannot be started.

 ''The quickest way to verify that you are both using a compatible version is to consult the “checksum,” that four letter code following the version number at the bottom left of the main screen. If your opponent’s checksum matches yours, then you are ready to play.

### What affects the checksum?

The checksum is created by Victoria 2 looking at certain files in its file-structure, and generating a unique key for the contents of those files. However, some files and folders are ignored by the checksum generator, which allows us to tinker with certain aspects of the game in mods, via the *mod* folder system.

Following files are used for the checksum calculation:
- **common**:
  - including sub directories
  - all .txt and .lua files
- **events**:
  - including sub directories
  - all .txt files
- **missions**:
  - including sub directories
  - all .txt files
- **decisions**
  - including sub directories
  - all .txt files
- **history**:
  - including sub directories
  - all .txt files
- **map**:
  - all .txt, .map,.csv and .bmp files
  - all .lua files in **map/random**
