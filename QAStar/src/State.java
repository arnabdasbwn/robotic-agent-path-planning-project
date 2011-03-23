import java.awt.Point;



public class State 
{
	public double up = 0;
	public double down = 0;
	public double left = 0;
	public double right = 0;
	
	private boolean wall = false;
	
	public Point point;
	
	private boolean goal = false;
	
	public State(Point point, boolean wall)
	{
		this.point = point;
		this.wall = wall;
	}
	
	public boolean isWall()
	{
		return wall;
	}
	
	public boolean isGoal()
	{
		return goal;
	}
	
	public void setGoal()
	{
		goal = true;
	}
	
	public String toString()
	{
		return String.format("(%1s/%2s),%3$.2f, %4$.2f, %5$.2f, %6$.2f", point.x, point.y, up, down, left, right);
	}
}
