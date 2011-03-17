import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.prefs.BackingStoreException;

import javax.swing.AbstractButton;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSeparator;
import javax.swing.JTextField;

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
	JButton directPathfromQTable;
	JPanel topPanel;
	JFrame frame;

	MapGUI map;
	
	private float discountFactor;
	private float learningRate;
	private int numIter;
	private int maxSteps;
	
	private State[][] qTable;
	private Point startPoint;
	private JPanel botPanel;
	private JTextField numIterField;
	private JTextField discountFactorField;
	private JTextField learningRateField;
	private JLabel learningRateFieldLabel;
	private JLabel discountFactorFieldLabel;
	private JLabel numIterFieldLabel;
	private JTextField yField;
	private JTextField xField;
	private JLabel yFieldLabel;
	private JLabel xFieldLabel;
	private boolean _initialized;
	private JTextField maxStepsField;
	private JLabel maxStepsFieldLabel;
	
	public MyRobot() 
	{
		map = new MapGUI();
		topPanel = new JPanel();
		topPanel = new JPanel();
		botPanel = new JPanel();
		frame = new JFrame();
		learningRateField = new JTextField();
		discountFactorField = new JTextField();
		numIterField = new JTextField();
		maxStepsField = new JTextField();
		xField = new JTextField();
		yField = new JTextField();
		
		learningRateField.setText("1");
		discountFactorField.setText("0.9");
		numIterField.setText("150");
		maxStepsField.setText("500");
		
		learningRateFieldLabel = new JLabel("Learning Rate");
		discountFactorFieldLabel = new JLabel("Discount Factor");
		numIterFieldLabel = new JLabel("Number of Iterations");
		xFieldLabel = new JLabel("X");
		yFieldLabel = new JLabel("Y");
		maxStepsFieldLabel = new JLabel("Max Steps per Game");
		
		qLearning = new JButton("Start");
		directPathfromQTable = new JButton("Direct Path");
		
		aStar = new JButton("Start");

		startPoint = new Point();
		
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
		
		directPathfromQTable.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                qLearningGreedyButtonActionPerformed(evt);
            }
        });
		
		topPanel.setLayout(new GridLayout(4,4));
		topPanel.setBorder(BorderFactory.createTitledBorder("Q Learning"));
		topPanel.add(qLearning);
		topPanel.add(new JLabel());
		topPanel.add(directPathfromQTable);
		topPanel.add(new JLabel());
		topPanel.add(learningRateFieldLabel);
		topPanel.add(learningRateField);
		topPanel.add(discountFactorFieldLabel);
		topPanel.add(discountFactorField);
		topPanel.add(numIterFieldLabel);
		topPanel.add(numIterField);
		topPanel.add(maxStepsFieldLabel);
		topPanel.add(maxStepsField);
		topPanel.add(xFieldLabel);
		topPanel.add(xField);
		topPanel.add(yFieldLabel);
		topPanel.add(yField);
		
		botPanel.setBorder(BorderFactory.createTitledBorder("A* Path Planning"));
		botPanel.add(aStar);
		
		frame.setLayout(new GridLayout(2,1));
		frame.add(topPanel);
		frame.add(botPanel);
		
		frame.pack();
		frame.setVisible(true);
		
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
		startPoint.x = map.getRobotLocation()[0];
		startPoint.y = map.getRobotLocation()[1];
		xField.setText(""+startPoint.x);
		yField.setText(""+startPoint.y);
		xField.repaint();
		yField.repaint();
	}

	
	private void qLearningGreedyButtonActionPerformed(ActionEvent evt)
	{
		if(!updateQlearningParameters())
			return;
		
		if(map.getMap() == null || map.getMap().length == 0)
		{
			System.out.println("Load a map first");
			return;
		}
		
		map.moveRobot(startPoint.x, startPoint.y, "N");
		
		boolean goalFound = false;
		
		while(!goalFound)
		{
			try 
			{
				Thread.sleep(1000);
			} catch (InterruptedException e) 
			{
				e.printStackTrace();
			}
			goalFound = greedy();
		}
	}
	
	private void qLearningButtonActionPerformed(ActionEvent evt)
	{
		if(updateQlearningParameters())
			qlearning();
	}

	private boolean updateQlearningParameters() {
		numIter = Integer.valueOf(numIterField.getText());
		discountFactor = Float.valueOf(discountFactorField.getText());
		learningRate = Float.valueOf(learningRateField.getText());
		maxSteps = Integer.valueOf(maxStepsField.getText());
		
		try
		{
			startPoint.x = Integer.valueOf(xField.getText());
			startPoint.y = Integer.valueOf(yField.getText());
		}
		catch(NumberFormatException ex)
		{
			System.out.println("Set the value of the start position.");
			return false;
		}
		
		return true;
	}
	
	private void qlearning()
	{	
		boolean goalFound = false;
		
		for(int i = 0; i < numIter; i++)
		{
			map.moveRobot(startPoint.x, startPoint.y, "N");
			
			goalFound = false;
			for(int j = 0; (j < maxSteps) && !goalFound; j++)
			{
				goalFound = randomWalk(false);
				if (j == maxSteps -1)
				{
					System.out.println("Max steps reached, cutting search short." + i);
				}
			}
		}
		
		printQTable();
	}

	private void printQTable() 
	{
		System.out.format("Q,up,down,left,right\n");
		
		for(int i = qTable.length - 1; i >= 0; i--)
		{
			for(int j = 0; j < qTable[0].length; j++)
			{
				System.out.println(qTable[i][j]);
			}
		}
	}
	
	private boolean greedy()
	{	
		int[] robot = map.getRobotLocation();
		
		State s = qTable[robot[0]][robot[1]];
		State next = null;
		String angle = "";
		
		boolean blocked = true;
		while(blocked)
		{	
			double maxValue = s.up;
			int maxValueIndex = 0;
			double[] dirArray = new double[4];
			dirArray[0] = s.up;
			dirArray[1] = s.down;
			dirArray[2] = s.left;
			dirArray[3] = s.right;
			
			for(int k = 0; k < 4; k++)
			{
				if(dirArray[k] > maxValue)
				{
					maxValue = dirArray[k];
					maxValueIndex = k;
				}
			}
			
			switch(maxValueIndex)
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

	private boolean takeBestPath(int numerator, int denominator)
	{
		return ((int) Math.random() * denominator) > numerator;
		
	}
	private boolean allZero(State s)
	{
		return s.up == s.down && s.down == s.left && s.left == s.right;
	}
	
	private int decideDirection(State current, int randomMove)
	{
		int direction = -1;
		if (takeBestPath(3,4) && !allZero(current))
		{
			if (current.up > Math.max(current.down, Math.max(current.left, current.right)))
			{
				direction = UP;
			}
			else if (current.down > Math.max(current.left, current.right))
			{
				direction = DOWN;
			}
			else if (current.left > current.right)
			{
				direction = LEFT;
			}
			else
			{
				direction = RIGHT;
			}
		}
		return direction;
	}
	
	private boolean randomWalk(boolean completelyRandom) 
	{
		int[] robot = map.getRobotLocation();
		
		State s = qTable[robot[0]][robot[1]];
		State next = null;
		String angle = "";
		
		boolean blocked = true;
		while(blocked)
		{
			int direction = (int) (Math.random() * 4);
			if (!completelyRandom)
			{
				int willTakeDirection = decideDirection(s, direction);
				if (willTakeDirection != -1)
				{
					direction = decideDirection(s, direction);
				}
			}
			
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
	
	private void aStarButtonActionPerformed(ActionEvent evt)
	{
		
	}
	
	private void refresh() 
	{
		if(map.getMap() == null || map.getMap().length == 0)
		{
			return;
		}
		
		initQTable();
		_initialized = true;
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) 
	{
		MyRobot robot = new MyRobot();
		
		while(true)
		{
			try {
				Thread.sleep(1000);
				
				if(!robot._initialized)
					robot.refresh();
				else
					break;
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

}
