import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.Point;
import java.awt.event.ActionEvent;
import java.util.PriorityQueue;
import java.util.Vector;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;

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
	private JPanel aPanel;
	private JTextField numIterField;
	private JTextField discountFactorField;
	private JTextField learningRateField;
	private JLabel learningRateFieldLabel;
	private JLabel discountFactorFieldLabel;
	private JLabel numIterFieldLabel;
	private JTextField colField;
	private JTextField rowField;
	private JLabel colFieldLabel;
	private JLabel rowFieldLabel;
	private boolean _initialized;
	private JTextField maxStepsField;
	private JLabel maxStepsFieldLabel;
	private JPanel panel;
	private AStarState[][] aTable;
	private PriorityQueue<AStarState> pQueue;
	
	public MyRobot() 
	{
		map = new MapGUI();
		topPanel = new JPanel();
		topPanel = new JPanel();
		panel = new JPanel();
		aPanel = new JPanel();
		frame = new JFrame();
		learningRateField = new JTextField();
		discountFactorField = new JTextField();
		numIterField = new JTextField();
		maxStepsField = new JTextField();
		rowField = new JTextField();
		colField = new JTextField();
		
		learningRateField.setText("1");
		discountFactorField.setText("0.9");
		numIterField.setText("150");
		maxStepsField.setText("500");
		
		learningRateFieldLabel = new JLabel("Learning Rate");
		discountFactorFieldLabel = new JLabel("Discount Factor");
		numIterFieldLabel = new JLabel("Number of Iterations");
		rowFieldLabel = new JLabel("Row");
		colFieldLabel = new JLabel("Column");
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
		
		topPanel.setLayout(new GridLayout(3,4));
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

		aPanel.setBorder(BorderFactory.createTitledBorder("A* Path Planning"));
		aPanel.add(aStar);
		
		panel.setLayout(new GridLayout(2,2));
		panel.add(rowFieldLabel);
		panel.add(rowField);
		panel.add(colFieldLabel);
		panel.add(colField);
		
		frame.setLayout(new BorderLayout());
		frame.add(topPanel, BorderLayout.NORTH);
		frame.add(aPanel, BorderLayout.CENTER);
		frame.add(panel, BorderLayout.SOUTH);
		
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
				Point p = new Point(j,i);
				State s = new State(p, map.isWall(i, j));
				
				qTable[i][j] = s;
			}
		}
		
		qTable[map.getGoal()[0]][map.getGoal()[1]].setGoal();
	}

	private void initialize() {
		startPoint.y = map.getRobotLocation()[0];
		startPoint.x = map.getRobotLocation()[1];
		rowField.setText(""+startPoint.y);
		colField.setText(""+startPoint.x);
		rowField.repaint();
		colField.repaint();
	}

	
	private void qLearningGreedyButtonActionPerformed(ActionEvent evt)
	{
		if(!updatelearningParameters())
			return;
		
		if(map.getMap() == null || map.getMap().length == 0)
		{
			System.out.println("Load a map first");
			return;
		}
		
		map.moveRobot(startPoint.y, startPoint.x, "N");
		
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
		if(updatelearningParameters())
			qlearning();
	}

	private boolean updatelearningParameters() {
		numIter = Integer.valueOf(numIterField.getText());
		discountFactor = Float.valueOf(discountFactorField.getText());
		learningRate = Float.valueOf(learningRateField.getText());
		maxSteps = Integer.valueOf(maxStepsField.getText());
		
		try
		{
			startPoint.y = Integer.valueOf(rowField.getText());
			startPoint.x = Integer.valueOf(colField.getText());
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
			map.moveRobot(startPoint.y, startPoint.x, "N");
			
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
		
		qTable[s.point.y][s.point.x] = s;
		map.moveRobot(next.point.y, next.point.x, angle);
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
		
		qTable[s.point.y][s.point.x] = s;
		map.moveRobot(next.point.y, next.point.x, angle);
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
		updatelearningParameters();
		
		map.moveRobot(startPoint.y, startPoint.x, "N");
		
		restartAStar();
		
		AStarState s = aTable[startPoint.y][startPoint.x];
		
		while(s != null && !s.isGoal())
		{
			System.out.println(s.point);
			s.visited = true;
			
			// CHECK UP
			if(s.point.y + 1 < aTable.length && !aTable[s.point.y + 1][s.point.x].wall && !aTable[s.point.y + 1][s.point.x].visited)
			{
				AStarState up = aTable[s.point.y + 1][s.point.x];
				
				if(up.f == 0)
				{
					computeAStarValues(up);
					up.previous = s;
					pQueue.add(up);	
				}
			}
			
			// CHECK DOWN
			if(s.point.y - 1 >= 0 && !aTable[s.point.y - 1][s.point.x].wall && !aTable[s.point.y - 1][s.point.x].visited)
			{
				AStarState down = aTable[s.point.y - 1][s.point.x];
				
				if(down.f == 0)
				{
					computeAStarValues(down);
					down.previous = s;
					pQueue.add(down);
				}
			}
			
			// CHECK LEFT
			if(s.point.x - 1 >= 0 && !aTable[s.point.y][s.point.x - 1].wall && !aTable[s.point.y][s.point.x - 1].visited)
			{
				AStarState left = aTable[s.point.y][s.point.x - 1];
				
				if(left.f == 0)
				{
					computeAStarValues(left);
					left.previous = s;
					pQueue.add(left);
				}
			}
			
			// CHECK RIGHT
			if(s.point.x + 1 < aTable[0].length && !aTable[s.point.y][s.point.x + 1].wall && !aTable[s.point.y][s.point.x + 1].visited)
			{
				AStarState right = aTable[s.point.y][s.point.x + 1];
				if(right.f == 0)
				{
					computeAStarValues(right);
					right.previous = s;
					pQueue.add(right);
				}
			}
			
			s = pQueue.poll();
		}
		
		if(s != null)
		{
			AStarState ptr = s; 
			Vector<Point> solution = new Vector<Point>();
			
			solution.add(new Point(ptr.point.x, ptr.point.y));
	
			while(ptr.previous != null)
			{
				solution.add(new Point(ptr.previous.point.x, ptr.previous.point.y));
				ptr = ptr.previous;
			}
			
			for(int i = solution.size()-1; i >= 0; i--)
			{
				try {
					Thread.sleep(1000);
					map.moveRobot(solution.get(i).y, solution.get(i).x, "N");
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				
			}
		}
		else
		{
			System.out.println("NO PATH!!!");
		}
		
	}

	private void restartAStar() 
	{
		pQueue.clear();
		for(int i = 0; i < aTable.length; i++)
		{
			for(int j = 0; j < aTable[0].length; j++)
			{
				aTable[i][j].f = 0;
				aTable[i][j].g = 0;
				aTable[i][j].h = 0;
				aTable[i][j].visited = false;
				aTable[i][j].previous = null;
			}
		}
	}
	
	private void computeAStarValues(AStarState currentState) 
	{	
		AStarState goal = aTable[map.getGoal()[0]][map.getGoal()[1]];
		
		// Computer H, G, F
		currentState.h = Math.sqrt(Math.pow(goal.point.y - currentState.point.y, 2) 
								+  Math.pow(goal.point.x - currentState.point.x, 2));
		currentState.g = currentState.previous == null ? 0 : currentState.previous.g + 1; 
		currentState.f = currentState.g + currentState.h;
	}

	private void initAStar() 
	{
		int[][] tmpMap = map.getMap();
		aTable = new AStarState[tmpMap.length][tmpMap[0].length];
		
		for(int i = 0; i < tmpMap.length; i++)
		{
			for(int j = 0; j < tmpMap[0].length; j++)
			{
				Point p = new Point(j,i);
				AStarState s = new AStarState(p, map.isWall(i, j));
				
				aTable[i][j] = s;
			}
		}
		
		aTable[map.getGoal()[0]][map.getGoal()[1]].setGoal();
		pQueue = new PriorityQueue<AStarState>();
	}

	private void refresh() 
	{
		if(map.getMap() == null || map.getMap().length == 0)
		{
			return;
		}
		
		initQTable();
		initAStar();
		initialize();
		_initialized = true;
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) 
	{
		try {
			UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
		} catch (ClassNotFoundException e1) {
			e1.printStackTrace();
		} catch (InstantiationException e1) {
			e1.printStackTrace();
		} catch (IllegalAccessException e1) {
			e1.printStackTrace();
		} catch (UnsupportedLookAndFeelException e1) {
			e1.printStackTrace();
		}
		
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
				e.printStackTrace();
			}
		}
	}

}
