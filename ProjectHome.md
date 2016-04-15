# Robotic agent path planning #

In this project, we have created a two simulated robots and one real one. The first simulated robot ran in a discrete environment and the second in a continuous one.

## Robot 1: ##
Runs in the discrete 2D environment, we have set it up to do Q-Learning and A`*` path planning.

[Q-learning in Action](http://www.youtube.com/embed/n4I8ea5Dt8k)

[Q-learning Example 1 with Sensor Error](http://www.youtube.com/embed/BFYOLidqQTo)

[Q-learning Example 2 with Sensor Error](http://www.youtube.com/embed/VpWzKSG21Oc)

[Q-learning Example 1 without Sensor Error](http://www.youtube.com/watch?v=TsC6dJMnQKM)

[Q-learning Example 2 without Sensor Error](http://www.youtube.com/watch?v=Ts0CbYcviGA)

[A\* Example 1](http://www.youtube.com/watch?v=ROIjgK_cpW8)

[A\* Example 2](http://www.youtube.com/watch?v=wrVXpI0_cA8)

## Robot 2: ##
Runs in a continuous 3D environment, it uses waypoints to preform A`*` path planning.

[Continuous A\* Example 1](http://www.youtube.com/watch?v=PsfSnIXSZ_Y)

[Continuous A\* Example 2](http://www.youtube.com/watch?v=N8xtc1u3hWc)


#### Running the continuous simultion: ####
Download and install the Panda3D library
> http://www.panda3d.org/download.php
Download and install Python version 2.5
> http://www.python.org/download/
Download and install an SVN client
> http://subversion.tigris.org/
Follow instructions on the Source tab of this page
> http://code.google.com/p/aiproj09/source/checkout
In the directory where source has been downloaded type:
> `python robotworld.py`

## Line Following Robot: ##
Learning, line following robot

This physical robot uses a PID controller to navigate a course. It uses simulated annealing to learn good values for P, I, and D as it travels around the course.