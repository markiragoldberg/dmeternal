dmeternal
=========

Dungeon Monkey Eternal- Third game in the dungeon monkey series, first written in Python.

Requires Python 2 and PyGame.

![Screenshot](image/screenshot.png)

INSTALLATION
============

This game requires Python 2.6 or 2.7 and PyGame to be installed on your system.
Do that first.

Unzip the game files and put them in a convenient folder. 

HOW TO PLAY
===========

There's not much to play at the moment, but you can do a bit...

Run chargen.py to make some characters. From the command line type:

  python chargen.py

Or maybe just double click chargen.py, which should work. Or right click and
select "Open with Python". You'll find a way.

If updating from a previous version, old characters may no longer be compatible.
Sorry. You can delete them from the "dmeternal" folder in your home directory.

After that, you can load up to four characters in campaign.py:

  python campaign.py

You will find your party on a mostly empty map. Here are the things you can do:
- Talk to the NPCs, though they don't have much to say right now.
- Check out the big treasure chest. There may be magic items!
- See if there's anything useful lying on the ground.
- There are some monsters on the other side of the river.
- The door in the building leads to the Edge of Civilization map, containing
  another chest, another fight, and a deserted city.
- The stairs going down lead to a dungeon, containing yet another chest, another
  fight, and a locked door which can be opened.
- Use the bookshelf to change your characters' prepared spells
- Press "s" to access the debugging store at any time. Useful for identifying
  potentially magic items.

New! You can check out the current progress on the random story/world builder
by running tp.py:

    python tp.py

Right now, it generates a scene kind of like campaign.py's edge of civ map,
but without any monsters or treasure. Take a look in the narrator package to
see what's going on under the hood. Maybe try adding some content of your own?


COMMANDS
========

Left click: Move to spot/Pick up items

Right click: Open popup menu

1-4: View party member/inventory screen

c: Center the screen on the party/active character

Q: Quit the game. There is no saving because there is no point.

s: Open the store. This cheat code is there for testing purposes, since
   there is currently no other way to access store functionality.


