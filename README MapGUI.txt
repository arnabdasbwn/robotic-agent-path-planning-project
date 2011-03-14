Purpose of this README file is to be able to use grid based map user interface for your projects. Please read it till end.


Contents
- Installation
- Usage
- Documentation



- INSTALLATION
In order to install the MapGUI add the MapGUI.java file into the terk-client-MyFirstRobot folder where MyFirstCreate.java file stays.




- USAGE
To view and access the map gui call once:

MapGUI map = new MapGUI();

in your program before creating robot object. You can also use MapGUI map = new MapGUI(x_pos, y_pos); to change the location of the gui on your monitor. The x_pos and y_pos inputs are integers in pixels that are used to change the location of the map gui starting from top left corner. Quick note, the X button on top right corner of map gui is disabled. So the only way to close the map is to close your robot program. You can not only view the map, but also retrieve the information from the map gui. The following functions are defined in order to retrieve and change robot, wall and goal information on the map.

map.setGoal(row, column);
map.getGoal();
map.addWall(row, column);
map.getMap();
map.isWall();
map.moveRobot(row, column, angle);
map.moveRobot(row, column, direction);
map.getRobotLocation();
map.getRobotAngle();
map.getRobotDirection();

Look into the documentation for more details about the functions.

The map user interface is pretty flexible. You can change certain things about the way the user interface looks. The following variables let you change the way map looks. If you don't touch any of these variables, the default values will be used.

map.background_color
map.cellsize
map.goal_color
map.goal_thickness
map.robot_color
map.robot_diameter
map.robotline_color
map.wall_color
map.wall_thickness

For more details check the documentation.


When the map gui shows up, you need to load map from a file. You can do this by clicking the load button above the map and select the file. A sample map file and map file structure is described below:

6 8
00100010
00000000
00000100
01101100
00011000
10010002
2 1 120

The first line shows the number of rows and columns on the map grid.
Then the following lines show the actual grid data, 1 means the cell has wall, 0 means empty cell.
The last line shows the position of robot (row:2 and column:1) and angle of the robot 120 degrees. Instead of angle you can give cardinal direction as E,NE,N,NW,W,SW,S,SE where East is 0 degrees and North is 90 degrees.

IMPORTANT NOTE: The 0x0 location on the map is the bottom left cell. For example the cell 3X1 is the 4th row from bottom and 2nd column from left. The reason why map starts from 0x0 is because this is going to be easier for you to use it in a for loop

When you change the map, you can also save it using the gui by clicking the save button above the map. Map files can only have the extension .txt or .map . I recommend you to use .txt extension, because you can also see the map data using basic text editor.



- DOCUMENTATION
MapGUI.html is the javadoc for the MapGUI.java file. All of the variables and functions that you need have descriptions inside the documentation. If you have any question about how a function works, what inputs it takes or what it returns please refer to the documentation. It is very explanatory.