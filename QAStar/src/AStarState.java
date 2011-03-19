import java.awt.Point;


public class AStarState implements Comparable<AStarState>
{
	public double f = 0;
	public int g = 0;
	public double h = 0;
	public boolean wall = false;
	public boolean visited = false;
	
	Point point;
	private boolean goal = false;
	public AStarState previous = null;
	public AStarState next = null;
	
	public AStarState(Point p, boolean b)
	{
		this.point = p;
		wall = b;
	}

	@Override
	public int compareTo(AStarState o) {

		if(this.f < o.f)
		{
			return -1;
		}
		else if (this.f > o.f)
		{
			return 1;
		}
			
		return 0;
	}

	public void setGoal() {
		this.goal = true;
	}

	public boolean isGoal() {
		return goal;
	}
}
