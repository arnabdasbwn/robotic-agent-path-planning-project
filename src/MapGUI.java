/*
 * MapGUI.java
 * @author Bulent TASTAN
 * Created Sep 17 2009
 * All rights reserved.
 * Copyright (c) Bulent TASTAN.
 * This java code is Introduction to Robotics (EGN 3060) use only.
 */

import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.MouseEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.PrintWriter;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileFilter;
import javax.swing.JOptionPane;
import javax.swing.filechooser.FileNameExtensionFilter;


public class MapGUI extends javax.swing.JFrame {

    
    ////////////////////////////////////////////////////////////////////////////
    /////////////////////// USEFUL FUNCTIONS ///////////////////////////////////
    ///////////////////////   AND VARIABLES  ///////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    
    
    // Map Configuration
    /** Size of each cell in map in pixels<br>(Default: 40)*/
    public int cellsize = 40;
    /** Outer wall thickness in pixels<br>(Default: 4)*/
    public int wall_thickness = 4;
    /** Goal thickness on map in pixel<br>(Default: 16)*/
    public int goal_thickness = 16;
    /** Diameter of robot figure on map in pixels<br>(Default: 32)*/
    public int robot_diameter = 32;
    /**Background color of map<br>(Default: Color.white)*/
    public Color background_color = Color.white;
    /** Color of the walls on map<br>(Default: Color.red)*/
    public Color wall_color = Color.red;
    /** Color of the goal on map<br>(Default: Color.decode("#22AA22"))*/
    public Color goal_color = Color.decode("#22AA22");
    /** Color of the robot on map<br>(Defaut: Color.green)*/
    public Color robot_color = Color.green;
    /** Color of the line that shows the direction of the robot<br>(Default: Color.black)*/
    public Color robotline_color = Color.black;
    // Map Configuration Ends
    
    
    
    
    
    /** Creates new form MapGUI. Map is placed to default location on the screen
     * Note that the initial location of the map is (0,0) which is the bottom left cell
     */
    public MapGUI() {
        this(200, 0);
    }
    
    /** Creates new MapGUI at the given location of the screen
     * Note that the initial location of the map is (0,0) which is the bottom left cell
     * @param x X coordinate on the screen from top left corner of monitor
     * @param y Y coordinate on the screen from top left corner of monitor
     */
    public MapGUI(int x, int y){
        initComponents();
        setLocation(x, y);
        setVisible(true);
    }
    
    
    
    /**
     * Changes the goal location to the given row and column.
     * The previous goal location is updated with the new one.
     * @param row Vertical coordinate. The bottom row is 0<sup>th</sup>,
     * top row is max(row)-1
     * @param column Horizontal coordinate.
     * The leftmost column is 0<sup>th</sup>, rightmost is max(column)-1
     */
    public void setGoal(int row, int column){
        if(row>=0 && row<ROW && column>=0 && column<COL){
            goal[0] = row;
            goal[1] = column;
            refresh();
        }
        else JOptionPane.showMessageDialog(this,
                    "The goal point is outside of the grid "+
                    "(check if 0<=row<"+ROW+" and 0<=column<"+COL,
                    "setGoal Function Input Error",JOptionPane.ERROR_MESSAGE);
    }
    
    
    /**
     * Returns the coordinate of the goal in an array
     * @return Goal location. The first value is row and second is column of the goal.
     */
    public int[] getGoal(){
        return goal;
    }
    
    
    /**
     * Adds a wall to the given location. If there is already a wall, it is ignored
     * @param row Vertical coordinate. The bottom row is 0<sup>th</sup>,
     * top row is max(row)-1
     * @param column Horizontal coordinate.
     * The leftmost column is 0<sup>th</sup>, rightmost is max(column)-1
     */
    public void addWall(int row, int column){
        if(row>=0 && row<ROW && column>=0 && column<COL){
            map[row][column] = 1;
            refresh();
        }
        else JOptionPane.showMessageDialog(this,
                    "The wall point is outside of the grid "+
                    "(check if 0<=row<"+ROW+" and 0<=column<"+COL,
                    "addWall Function Input Error",JOptionPane.ERROR_MESSAGE);
        
    }
    
    /**
     * Returns the whole map as double array. The initial position of the map is
     * bottom left cell. It goes vertically up and right.
     * @return Map as double integer array. In the map 0 means empty,
     * 1 means there is wall, 2 means there is goal.<br><b>Note:</b>
     * You can loop in the map array as follows:<br>
     * <p>int[][] map = mapGUI.getMap();<br>
     * for(int i=0; i&lemap.length; i++)<br>
     * &nbsp&nbsp&nbsp for(int j=0; j&lemap[i].length; j++)<br>
     * &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<i>...process...</i> map[i][j]
     * </p>
     */
    public int[][] getMap(){
        return map;
    }
    
    /**
     * Check whether the given location has wall or not
     * @param row Vertical coordinate. The bottom row is 0<sup>th</sup>,
     * top row is max(row)-1
     * @param column Horizontal coordinate.
     * The leftmost column is 0<sup>th</sup>, rightmost is max(column)-1
     * @return True if location has wall, False otherwise
     */
    public boolean isWall(int row, int column){
        if(row>=0 && row<ROW && column>=0 && column<COL){
            return (map[row][column]==1? true : false);
        }
        else JOptionPane.showMessageDialog(this,
                    "The wall point is outside of the grid "+
                    "(check if 0<=row<"+ROW+" and 0<=column<"+COL,
                    "isWall Function Input Error",JOptionPane.ERROR_MESSAGE);
        return false;
    }
      
    /**
     * Moves the robot on the map. You can use it to only rotate or both rotate
     * and change the location of the robot on the map.
     * @param row New vertical coordinate of robot. The bottom row is 0<sup>th</sup>,
     * top row is max(row)-1
     * @param column New horizontal coordinate of robot.
     * The leftmost column is 0<sup>th</sup>, rightmost is max(column)-1
     * @param angle New angle in degrees (ie: 30&deg;) of robot
     */
    public void moveRobot(int row, int column, int angle){
        if(row>=0 && row<ROW && column>=0 && column<COL){
            robot[0] = row;
            robot[1] = column;
            robotangle = (angle+360)%360;
            refresh();
        }
        else JOptionPane.showMessageDialog(this,
                    "The point is outside of the grid "+
                    "(check if 0<=row<"+ROW+" and 0<=column<"+COL,
                    "moveRobot Function Input Error",JOptionPane.ERROR_MESSAGE);
        
    }
    
    /**
     * Moves the robot on the map. You can use it to only rotate, move or both rotate
     * and change the location of the robot on the map.
     * @param row Vertical coordinate. The bottom row is 0<sup>th</sup>,
     * top row is max(row)-1
     * @param column Horizontal coordinate.
     * The leftmost column is 0<sup>th</sup>, rightmost is max(column)-1
     * @param direction New cardinal direction (E,NE,N,NW,W,SW,S,SE) of robot
     */
    public void moveRobot(int row, int column, String direction){
        if(row>=0 && row<ROW && column>=0 && column<COL){
            robot[0] = row;
            robot[1] = column;
            if(direction.equals("E")) robotangle = 0;
            else if(direction.equals("NE")) robotangle = 45;
            else if(direction.equals("N")) robotangle = 90;
            else if(direction.equals("NW")) robotangle = 135;
            else if(direction.equals("W")) robotangle = 180;
            else if(direction.equals("SW")) robotangle = 225;
            else if(direction.equals("S")) robotangle = 270;
            else if(direction.equals("SE")) robotangle = 315;
            else 
                JOptionPane.showMessageDialog(this,
                        "Wrong Direction Given (Use: E,NE,N,NW,W,SW,S,SE or ANGLE",
                        "Error while moving Robot",JOptionPane.ERROR_MESSAGE);
            refresh();
        }
        else JOptionPane.showMessageDialog(this,
                    "The point is outside of the grid "+
                    "(check if 0<=row<"+ROW+" and 0<=column<"+COL,
                    "moveRobot Function Input Error",JOptionPane.ERROR_MESSAGE);
    }
    
    /**
     * Returns the location of the robot as integer array.
     * @return Robot location in integer array. The first value of array is the
     * row and second is column on the map
     */
    public int[] getRobotLocation(){
        return robot;
    }
    
    /**
     * Returns the angle of the robot in degrees (ie: 30&deg)
     * @return Angle of the robot on the map as int
     */
    public int getRobotAngle(){
        return robotangle;
    }
    
    /**
     * Returns the cardinal direction of the robot (E,NE,N,NW,W,SW,S,SE).
     * If the robot is not directly on one of 8 cardinal directions (ie: 15%deg)
     * it's rounded to the closest cardinal direction (ie: E)
     * @return Cardinal direction of the robot on the map as String
     */
    public String getRobotDirection(){
        if(robotangle>337.5 || robotangle<22.5) return "E";
        else if(robotangle>22.5 && robotangle<67.5) return "NE";
        else if(robotangle>67.5 && robotangle<112.5) return "N";
        else if(robotangle>112.5 && robotangle<157.5) return "NW";
        else if(robotangle>157.5 && robotangle<202.5) return "W";
        else if(robotangle>202.5 && robotangle<247.5) return "SW";
        else if(robotangle>247.5 && robotangle<292.5) return "S";
        else if(robotangle>292.5 && robotangle<337.5) return "SE";
        else{
            JOptionPane.showMessageDialog(this,
                    "Error in retrieving robot direction "+
                    "(The error occurs when somehow the robot angle becomes negative)",
                    "getRobotDirection Function Output Error",JOptionPane.ERROR_MESSAGE);
            return "Unknown";
        }
    }
    
    
    
    
    ///////////////////////     END OF       ///////////////////////////////////
    /////////////////////// USEFUL FUNCTIONS ///////////////////////////////////
    ///////////////////////   AND VARIABLES  ///////////////////////////////////
    /////////////// DON'T BOTHER WITH THE REST OF CODE /////////////////////////
    
    
    
    
    

    private void initMaze(File mapFile) {
        try {
            /* 6 8          row column
             * 00000000     grid data
             * 00000000     0 empty cell
             * 00001100     1 cell has wall
             * 00001100
             * 00011000
             * 00010002
             * 2 1 N        robot coordinate and angle or direction
             * robot angle 0East 45NE 90N 135NW 180W 225SW S270 SE315
             */
            BufferedReader reader = new BufferedReader(new FileReader(mapFile));
            String[] mazeSize = reader.readLine().split(" ");
            ROW = Integer.parseInt(mazeSize[0]);
            COL = Integer.parseInt(mazeSize[1]);
            setSizeLabel(ROW, COL);
            Ymargin = YBase + seperator.getY();

            //myMaze = new MazeGraphics(this, WIDTH, HEIGHT, Xmargin, Ymargin);

            map = new int[ROW][COL];
            setSize(2 * Xmargin + COL * cellsize, Ymargin + Xmargin + ROW * cellsize);

            for(int i=ROW-1; i>=0; i--){
                String line = reader.readLine();
                for(int j=0; j<COL; j++){
                    if(line.charAt(j) == '0'){
                        map[i][j] = 0;
                    }
                    else if(line.charAt(j) == '1'){
                        map[i][j] = 1;
                    }
                    else if(line.charAt(j) == '2'){
                        goal[0] = i;
                        goal[1] = j;
                     //   MyFirstCreate.goal = new Point(j, i);   <-----
                        setGoalLabel(i, j);
                    }
                    else{
                        JOptionPane.showMessageDialog(this,
                        "Unknown grid number in the map file, please check your map file",
                        "Map File Error",JOptionPane.ERROR_MESSAGE);
                    }
                }
            }
            
            String[] robData = reader.readLine().split(" ");
            robot[0] = Integer.parseInt(robData[0]);
            robot[1] = Integer.parseInt(robData[1]);
            try{
                robotangle = Integer.parseInt(robData[2]);
            } catch(Exception ex){
                if(robData[2].equals("E")) robotangle = 0;
                else if(robData[2].equals("NE")) robotangle = 45;
                else if(robData[2].equals("N")) robotangle = 90;
                else if(robData[2].equals("NW")) robotangle = 135;
                else if(robData[2].equals("W")) robotangle = 180;
                else if(robData[2].equals("SW")) robotangle = 225;
                else if(robData[2].equals("S")) robotangle = 270;
                else if(robData[2].equals("SE")) robotangle = 315;
            }

            refresh();
            
            reader.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
    
    
    private void saveMap(File mapFile){
        try{
            int[][] mymap = map;
            mymap[goal[0]][goal[1]] = 2;
            PrintWriter pw = new PrintWriter(new FileWriter(mapFile));
            pw.println(""+ROW+" "+COL);

            for(int i=ROW-1; i>=0; i--){
                for(int j=0; j<COL; j++)
                    pw.print(""+mymap[i][j]);
                pw.println();
            }
            pw.println(""+robot[0]+" "+robot[1]+" "+robotangle);
            pw.close();
        } catch (Exception ex) {
            System.err.println("CHECK IF THE MAP IS LOADED FIRST BEFORE SAVING");
            ex.printStackTrace();
        }
    }

    
    
    
    
    ////////////////////  GRAPHICS  /////////////////////
    
    private void refresh(){
        wipeGrid();
        drawBorder();
        drawGrid();
        drawWalls();
        drawGoal();
        drawRobot();
    }
    
    // translates from cell,cell to x,y //
    private int xCell2Pixel(int cell)
    {
        return (int)(cell * cellsize);
    }
    private int yCell2Pixel(int cell)
    {
        return (int) ((ROW-cell-1) * cellsize);
    }
    
    // this draws a line and does thickness symmetrically //
    private void drawHorizontalLine(int x1, int x2,int y, int thickness)
    {
        Graphics g = getGraphics();
        g.setColor(wall_color);
        int start_y = y - (int)((float)(thickness)/2.0);
        for (int i=0; i<thickness; i++) {
            g.drawLine(Xmargin+x1,Ymargin+start_y+i,Xmargin+x2,Ymargin+start_y+i);
        }
        g.dispose();
    }

    // this draws a line and does thickness symmetrically //
    private void drawVerticalLine(int x, int y1,int y2, int thickness)
    {
        Graphics g = getGraphics();
        g.setColor(wall_color);
        int start_x = x - (int)((float)(thickness)/2.0);
        for (int i=0; i<thickness; i++) {
            g.drawLine(Xmargin+start_x+i,Ymargin+y1,Xmargin+start_x+i,Ymargin+y2);
        }
        g.dispose();
    }
    
    
    private void wipeGrid()
    {
        Graphics g = getGraphics();
        g.setColor(background_color);
        g.fillRect(Xmargin-wall_thickness,Ymargin-wall_thickness,
                   COL*cellsize + 2*wall_thickness, ROW*cellsize + 2*wall_thickness);
        g.dispose();
    }
    
    // draws the outside wall border of the maze //
    private void drawBorder()
    {
        drawHorizontalLine(0,cellsize*COL,0,wall_thickness);
        drawHorizontalLine(0,cellsize*COL,cellsize*ROW,wall_thickness);
        drawVerticalLine(0,0,cellsize*ROW,wall_thickness);
        drawVerticalLine(cellsize*COL,0,cellsize*ROW,wall_thickness);

    }
    
    // draws the interior grid of the maze -- 1 pixel thick //
    private boolean drawGrid()
    {
        for (int i=1; i < ROW; i++) {
            drawHorizontalLine(0,COL*cellsize,i*cellsize,1);
        }
        for (int i=1; i < COL; i++) {
            drawVerticalLine(i*cellsize,0,ROW*cellsize,1);
        }

        return(true);
    }
    
    private void drawRobot(){
        int x = xCell2Pixel(robot[1]);
        int y = yCell2Pixel(robot[0]);

        Graphics g = getGraphics();
        g.setColor(robot_color);
        int tl_x, tl_y;
        tl_x = x + Xmargin;
        tl_y = y + Ymargin;
        tl_x = tl_x + (cellsize-robot_diameter)/2;
        tl_y = tl_y + (cellsize-robot_diameter)/2;
        int diam = robot_diameter;
        int radius = (int)((float)diam / 2.0);

        g.fillOval(tl_x, tl_y, diam, diam);
        
        g.setColor(robotline_color);
        g.drawLine(tl_x + radius, tl_y + radius,
                (int)(tl_x+radius+radius*Math.cos(robotangle*Math.PI/180.0)), 
                (int)(tl_y+radius-radius*Math.sin(robotangle*Math.PI/180.0)));

        g.dispose();
    }
    private void drawWalls(){
        Graphics g = getGraphics();
        g.setColor(wall_color);
        for(int i=0; i<ROW; i++)
            for(int j=0; j<COL; j++)
                if(map[i][j]==1){
                    int x = Xmargin + xCell2Pixel(j);
                    int y = Ymargin + yCell2Pixel(i);
                    g.fillRect(x, y, cellsize, cellsize);
                }
        g.dispose();
    }
    private void drawGoal(){
        int x = xCell2Pixel(goal[1]);
        int y = yCell2Pixel(goal[0]);
        Graphics g = this.getGraphics();
        g.setColor(goal_color);
        int tl_x, tl_y;
        
        tl_x = x + Xmargin + (cellsize-goal_thickness)/2;
        tl_y = y + Ymargin + (cellsize-goal_thickness)/2;
        g.fillRect(tl_x, tl_y, goal_thickness,goal_thickness);
        g.dispose();
    }
    
    
    

    @Override
    public void paint(Graphics g) {
        super.paint(g);
        refresh();
    }

    
    private void testMapClass(){
        System.out.println("----TESTING GOAL----");
        setGoal(2,5);
        int g[]=getGoal();
        System.out.println("GOAL: "+g[0]+" "+g[1]);
        System.out.println("----TESTING WALL----");
        addWall(2, 6);
        try{
            Thread.sleep(1000);
        }catch(Exception ex){ex.printStackTrace();}
        addWall(4, 2);
        int mymap[][]=getMap();
        for(int i=ROW-1; i>=0; i--){
            for(int j=0; j<COL; j++)
                System.out.print(mymap[i][j]);
            System.out.println();
        }
        System.out.println("location 4,6 is wall: "+isWall(4,6));
        System.out.println("location 1,3 is wall: "+isWall(1,3));
        System.out.println("----TESTING ROBOT----");
        moveRobot(2,1,180);
            try{
                Thread.sleep(1000);
            }catch(Exception ex){ex.printStackTrace();}
        moveRobot(1,0,-265);
        int robotpos[] = getRobotLocation();
        System.out.println("Robot is at: "+robotpos[0]+" "+robotpos[1]);
        System.out.println("Robot Angle: "+getRobotAngle());
        System.out.println("Robot Direction: "+getRobotDirection());
    }


    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        mapFileChooser = new javax.swing.JFileChooser();
        rightClickMenu = new javax.swing.JPopupMenu();
        addWaypointItem = new javax.swing.JMenuItem();
        sizeLabel = new javax.swing.JLabel();
        goalLabel = new javax.swing.JLabel();
        loadButton = new javax.swing.JButton();
        seperator = new javax.swing.JSeparator();
        saveButton = new javax.swing.JButton();

        mapFileChooser.setFileFilter(mapFileFilter);

        addWaypointItem.setText("Set Goal");
        addWaypointItem.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                addWaypointItemActionPerformed(evt);
            }
        });
        rightClickMenu.add(addWaypointItem);

        setDefaultCloseOperation(javax.swing.WindowConstants.DO_NOTHING_ON_CLOSE);
        setTitle("Map");
        addMouseListener(new java.awt.event.MouseAdapter() {
            public void mousePressed(java.awt.event.MouseEvent evt) {
                formMousePressed(evt);
            }
        });

        sizeLabel.setBackground(new java.awt.Color(153, 240, 240));
        sizeLabel.setFont(new java.awt.Font("Tahoma", 0, 10)); // NOI18N
        sizeLabel.setForeground(new java.awt.Color(102, 102, 102));
        sizeLabel.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        sizeLabel.setText("Size: <not set>");
        sizeLabel.setPreferredSize(new java.awt.Dimension(48, 18));

        goalLabel.setBackground(new java.awt.Color(153, 240, 240));
        goalLabel.setFont(new java.awt.Font("Tahoma", 0, 10)); // NOI18N
        goalLabel.setForeground(new java.awt.Color(102, 102, 102));
        goalLabel.setHorizontalAlignment(javax.swing.SwingConstants.CENTER);
        goalLabel.setText("Goal: <empty>");
        goalLabel.setPreferredSize(new java.awt.Dimension(48, 18));

        loadButton.setText("Load");
        loadButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                loadButtonActionPerformed(evt);
            }
        });

        saveButton.setText("Save");
        saveButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                saveButtonActionPerformed(evt);
            }
        });

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addComponent(seperator, javax.swing.GroupLayout.DEFAULT_SIZE, 444, Short.MAX_VALUE)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(loadButton, javax.swing.GroupLayout.DEFAULT_SIZE, 71, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(saveButton, javax.swing.GroupLayout.DEFAULT_SIZE, 72, Short.MAX_VALUE)
                .addGap(43, 43, 43)
                .addComponent(sizeLabel, javax.swing.GroupLayout.DEFAULT_SIZE, 76, Short.MAX_VALUE)
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(goalLabel, javax.swing.GroupLayout.DEFAULT_SIZE, 69, Short.MAX_VALUE)
                .addGap(91, 91, 91))
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.BASELINE)
                        .addComponent(loadButton, javax.swing.GroupLayout.PREFERRED_SIZE, 23, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(saveButton, javax.swing.GroupLayout.PREFERRED_SIZE, 23, javax.swing.GroupLayout.PREFERRED_SIZE))
                    .addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.CENTER)
                        .addComponent(sizeLabel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                        .addComponent(goalLabel, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)))
                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(seperator, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(386, Short.MAX_VALUE))
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents

    

private void readMapFile(JFileChooser fileChooser){
    if(fileChooser.getDialogType() == JFileChooser.OPEN_DIALOG){
        File mapFile = fileChooser.getSelectedFile();

        if (!mapFile.canRead()) {
            JOptionPane.showMessageDialog(this, fileChooser.getSelectedFile().toString() +
                    " cannot be read", "Map Loading Error", JOptionPane.ERROR_MESSAGE);
        } else if (!mapFile.isFile()) {
            JOptionPane.showMessageDialog(this, fileChooser.getSelectedFile().toString() +
                    " is not a file", "Map Loading Error", JOptionPane.ERROR_MESSAGE);
        } else if (!mapFile.toString().endsWith(".map") && !mapFile.toString().endsWith(".txt")) {
            JOptionPane.showMessageDialog(this, fileChooser.getSelectedFile().toString() +
                    ", file extension is incorrect", "Map Loading Error", JOptionPane.ERROR_MESSAGE);
        } else {
            initMaze(mapFile);
        }
    }
}

private void saveMapFile(JFileChooser fileChooser){
    if(fileChooser.getDialogType() == JFileChooser.SAVE_DIALOG){
        
        String filename = fileChooser.getSelectedFile().toString();
        if(!filename.endsWith(".txt") && !filename.endsWith(".map")){
            filename += ".txt";
        }

        if(fileChooser.getSelectedFile().exists()){
            int option = JOptionPane.showConfirmDialog(this, 
                    "Map file already exists, do you want to overwrite?","Overwrite",
                    JOptionPane.YES_NO_OPTION);
            if(option == JOptionPane.YES_OPTION){
                saveMap(new File(filename));
            }
        }
        else{
            saveMap(new File(filename));
        }
    }
}

private void setSizeLabel(int x, int y){
    sizeLabel.setText("Size: "+x+"x"+y);
}

private void setGoalLabel(int x, int y){
    goalLabel.setText("Goal: "+x+"x"+y);
}

private int clickedR, clickedC;
private void addWaypointItemActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_addWaypointItemActionPerformed
    setGoalLabel(clickedR, clickedC);
    setGoal(clickedR, clickedC);
    rightClickMenu.setVisible(false);
}//GEN-LAST:event_addWaypointItemActionPerformed

private void formMousePressed(java.awt.event.MouseEvent evt) {//GEN-FIRST:event_formMousePressed
    if (evt.getButton() == MouseEvent.BUTTON3 &&
            evt.getX() > Xmargin && evt.getX() < (Xmargin + cellsize * COL) &&
            evt.getY() > Ymargin && evt.getY() < (Ymargin + cellsize * ROW)) {
        rightClickMenu.setVisible(true);
        rightClickMenu.setLocation(evt.getX() + this.getLocation().x, evt.getY() + this.getLocation().y);
        clickedR = ROW - 1 - (evt.getY() - Ymargin) / cellsize;
        clickedC = (evt.getX() - Xmargin) / cellsize;
    } else {
        rightClickMenu.setVisible(false);
    }
}//GEN-LAST:event_formMousePressed


private void loadButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_loadButtonActionPerformed
    int option = mapFileChooser.showOpenDialog(this);
    if(option == JFileChooser.APPROVE_OPTION){
        readMapFile(mapFileChooser);
    }
}//GEN-LAST:event_loadButtonActionPerformed

private void saveButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_saveButtonActionPerformed
    int option = mapFileChooser.showSaveDialog(this);
    if(option == JFileChooser.APPROVE_OPTION){
        saveMapFile(mapFileChooser);
    }
}//GEN-LAST:event_saveButtonActionPerformed



    /**
     * The main function allows the MapGUI run standalone
     * @param args the command line arguments
     */
    public static void main(String args[]) {
        java.awt.EventQueue.invokeLater(new Runnable() {

            public void run() {
                new MapGUI().setVisible(true);
            }
        });
    }

    
    
    
    
    private FileFilter mapFileFilter = new FileNameExtensionFilter("Map File", "txt", "map");
    
    private int ROW = 0, COL = 0;    //row and column sizes of maze
    private int map[][];
    private int robot[] = new int[2];
    private int robotangle = 0;
    private int goal[] = new int[2];
    private int Xmargin = 30, Ymargin = 0, YBase = 48;
    
    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JMenuItem addWaypointItem;
    private javax.swing.JLabel goalLabel;
    private javax.swing.JButton loadButton;
    private javax.swing.JFileChooser mapFileChooser;
    private javax.swing.JPopupMenu rightClickMenu;
    private javax.swing.JButton saveButton;
    private javax.swing.JSeparator seperator;
    private javax.swing.JLabel sizeLabel;
    // End of variables declaration//GEN-END:variables
}
