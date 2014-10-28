MarcoPygame
===========

#IMPORTANT:
Using Python 3.3 with pygame 1.9.2a0

Windows 8.1

IDE: Pycharm (which is why there are a bunch of files that seem like giberish and not related to Python)

# Game idea has now changed!
I started as wanting to play around with a top down grid system but now I've decided to turn the game into a platform fighting game.  

#ALREADY IMPLIMENTED
+ Basic Drawings Placeholders
+ Main Loop
+ Basic Movement and Controls
+ Display of player off screen
+ Basic collision detection for world objects (slight bug where bottom and right clipping of player is off)
+ Basic Platform system
+ Damage and Healing system
+ 60 fps ticks (Pygame feature, hopefully I'm using it correctly and no issues pop up for lower FPS such as the game running in slow motion)
+ Platform collision detection
+ Solid and Oneway platforms acting as they should (being able to go through bottom of one way plats and falling through them)
+ Ledge system
+ Human and CPU controls base
+ Double Jump
+ Physics system including jump heights, acceleration, velocity, gravity
+ Basic character system, starting with prototype character (child of Players class)

#GOING TO IMPLIMENT
- Multiplayer (hopefully)
- CPU players
- Win screen and Statistics
- Character select
- Different characters
- attacks
- partical system


#CONTROLS (will change)
+ "wasd" movement
+ "q/e" hurt/heal
+ "space" jump
+ "f" debug mode for collision

#NOTES
I've tried to set things up so that the basic features can easily be built into bigger features
