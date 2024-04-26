112 Project Option 3 4/26/24
By: Adam Kollgaard

---------------
File structure:
main.py - This is the main file! Run the game from here. Make sure cmu_graphics is
in the same directory.

Graphics.py - This is all the stuff that creates a graphics engine. I choose to make
it into a class because I can create multiple graphics engines to run multiple scenes
at the same time or at different moments. This is why the beginning animation is possible

Object.py - This contains all the parent classes for most of the shape data. Sorry for
naming confusing, but I mix and match shape/object a little. A shape/object is anything
that gets rendering in the game.

Model.py - This contains all the data for creating arbitray shapes, ships, enemies,
buildings and other stuff.

test.py - Random stuff to test python things

Engine.py - An old version of the graphics engine. It is not used; deprecated :(
---------------

For my project, I created a game that is essientally very similiar to the game starfox.
It is a endless version of the game that is more of a snippet to the actual game.
Think of it like a demo or something similar. The main goal of the project was to
use 3D graphics to draw everything. 

The 3D graphics engine uses a Perspective Projection Matrix, however I have not
implemented any lighting/shadows/anything super complicated. Each shape is made
of multiple polygons that are of any 2D shape which are represented by vertices
in 3D space. Then those vertices are taken a vectors from some arbitrary origin point. 
The graphics engine converts these 3D points to 2D points that can then be represented
on the screen. At the end, I simply use drawPolygon to create the shapes. Then some
list sorting can be done to figure out which object is closer to the camera to find
what objects need to be drawn first. It is a relatively simple engine that uses a 
lot information from the following sources:
https://en.wikipedia.org/wiki/3D_projection
https://www.3dgep.com/understanding-the-view-matrix/
https://www.youtube.com/watch?v=EqNcqBdrNyI&ab_channel=pikuma

After hitting the play button, the game starts a little animation and then you enter
the actually playing part. The playing part uses WASD as the controls, space to shoot,
F to boost forward, then press H to change to first-person point of view. In this view
you can use the mouse to control the ship where the center of the screen centers the view
of the ship. You can not use WASD in first person mode! All other commands still work.
Try not to get hit by the other enemies and avoid the obstacles. The buildings to the left
and right are the bounds; do not leave! If you hit the ground or go to high you will also lose.
The bar in the bottom left corner shows your health in red and then the boost in blue.
You can also hit z for extra camera data in the top left corner, but this is mostly for 
debugging purposes.

GRADING SHORTCUTS:
You can press r at any moment to enter the actual playing part of the game. This works for any
screen. Mostly if you want to skip the beginning animation.
You can also press m while playing to enter back into the menu screen.