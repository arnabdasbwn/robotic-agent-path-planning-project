import java.awt.Point;
import java.awt.event.ActionEvent;
import java.util.ArrayList;
import java.util.HashMap;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

/**
 * 
 */

/**
 * @author Frank
 *
 */
public class MyRobot {

	public static final int UP = 0;
	public static final int DOWN = 1;
	public static final int LEFT = 2;
	public static final int RIGHT = 3;
		
	
	JButton qLearning;
	JButton aStar;
	JPanel panel;
	JFrame frame;

	MapGUI map;
	
	private final float discountFactor = 0.9f;
	private final float learningRate = 1;
	private final int numIter = 100;
	
	private State[][] qTable;
	
	public MyRobot() {
		qLearning = new JButton("Q Learning");
		aStar = new JButton("A* planning");
		
		aStar.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                aStarButtonActionPerformed(evt);
            }
        });
		
		qLearning.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                qLearningButtonActionPerformed(evt);
            }
        });
		
		map = new MapGUI();
		panel = new JPanel();
		frame = new JFrame();
		panel.add(qLearning);
		panel.add(aStar);
		frame.add(panel);
		frame.pack();
		frame.setVisible(true);
//		map.getContentPane().add(panel);
	}
	
	private void qLearningButtonActionPerformed(ActionEvent evt)
	{
		qlearning();
	}
	
	private void qlearning()
	{
		if(map.getMap() == null || map.getMap().length == 0)
		{
			System.out.println("Load a map first");
			return;
		}
		
		initQTable();
		
		for(int i = 0; i < numIter; i++)
		{
			boolean goalFound = false;
			while(!goalFound)
			{
				goalFound = randomWalk();
			}
		}
		
		printQTable();
	}

	private void printQTable() 
	{
		System.out.format("|  Q  |  up  |  down  |  left  | right |\n");
		
		for(int i = qTable.length - 1; i >= 0; i--)
		{
			for(int j = 0; j < qTable[0].length; j++)
			{
				System.out.println(qTable[i][j]);
			}
		}
	}

	private boolean randomWalk() 
	{
		int[] robot = map.getRobotLocation();
		
		State s = qTable[robot[0]][robot[1]];
		State next = null;
		String angle = "";
		
		boolean blocked = true;
		while(blocked)
		{
			int direction = (int) (Math.random() * 4);
			
			switch(direction)
			{
				case UP:
					if(robot[0] < qTable.length - 1 && !qTable[robot[0]+1][robot[1]].isWall())
					{
//								System.out.format("Robot (%1$d, %2$d) moving to (%3$d, %4$d)", robot[0], robot[1], robot[0]+1, robot[1]);
//								System.out.println("Moving UP");
						next = qTable[robot[0]+1][robot[1]];
						angle = "N";
						s.up = update(s, next, s.up);
						blocked = false;
					}
					break;
				case DOWN:
					if(robot[0] > 0 && !qTable[robot[0]-1][robot[1]].isWall())
					{
//								System.out.format("Robot (%1$d, %2$d) moving to (%3$d, %4$d)", robot[0], robot[1], robot[0]-1, robot[1]);
//								System.out.println("Moving DOWN");
						next = qTable[robot[0]-1][robot[1]];
						angle = "S";
						s.down = update(s, next, s.down);
						blocked = false;
					}
					break;
				case LEFT:
					if(robot[1] > 0 && !qTable[robot[0]][robot[1]-1].isWall())
					{
//								System.out.format("Robot (%1$d, %2$d) moving to (%3$d, %4$d)", robot[0], robot[1], robot[0], robot[1]-1);
//								System.out.println("Moving LEFT");
						next = qTable[robot[0]][robot[1]-1];
						angle = "W";
						s.left = update(s, next, s.left);
						blocked = false;
					}
					break;
				case RIGHT:
					if(robot[1] < qTable[0].length - 1 && !qTable[robot[0]][robot[1]+1].isWall())
					{
//								System.out.format("Robot (%1$d, %2$d) moving to (%3$d, %4$d)", robot[0], robot[1], robot[0], robot[1]+1);
//								System.out.println("Moving RIGHT");
						angle = "E";
						next = qTable[robot[0]][robot[1]+1];
						s.right = update(s, next, s.right);
						blocked = false;
					}
				default:
					
					break;
			}
		}
		
		qTable[s.point.x][s.point.y] = s;
		map.moveRobot(next.point.x, next.point.y, angle);
		return next.isGoal();
	}
	
	private double update(State current, State next, double oldValue) 
	{
		int reward = 0;
		
		if(next.isGoal())
		{
			reward = 100;
		}
		
		double qValue = 0;
		
		qValue = oldValue + learningRate * (reward + discountFactor * Math.max(next.down, Math.max(next.up, Math.max(next.left, next.right))) - oldValue);
		
		return qValue;
	}

	private void initQTable()
	{
		int[][] tmpMap = map.getMap();
		qTable = new State[tmpMap.length][tmpMap[0].length];
		
		for(int i = 0; i < tmpMap.length; i++)
		{
			for(int j = 0; j < tmpMap[0].length; j++)
			{
				Point p = new Point(i,j);
				State s = new State(p, map.isWall(i, j));
				
				qTable[i][j] = s;
			}
		}
		
		qTable[map.getGoal()[0]][map.getGoal()[1]].setGoal();
	}
	
	private void aStarButtonActionPerformed(ActionEvent evt)
	{
		
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		MyRobot robot = new MyRobot();
		
	}

}
