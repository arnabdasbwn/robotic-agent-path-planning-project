import java.awt.event.ActionEvent;

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

	JButton qLearning;
	JButton aStar;
	JPanel panel;
	JFrame frame;

	MapGUI map;
	
	private float discountFactor;
	private float learningRate;
	private double[] qTable; 
	
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
		
	}
	
	private void qlearning()
	{
		
	}
	
	private void aStarButtonActionPerformed(ActionEvent evt)
	{
		
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		MyRobot robot = new MyRobot();
		

	}

}
