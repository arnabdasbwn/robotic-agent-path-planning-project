#include <pololu/orangutan>
#include "LineFollowingBot.h"

int main()
{
	MotorControl
		speeds;
	//programRunning will always be true... I just hate while(1)'s.
	while (programRunning)
	{
		sense();
		speeds = think();
		act(speeds);
	}
	return 0;
}

//Initialize board.
void initialize()
{
	//Initilize the outputs to the mux
	muxSelector.setOutput(IO_B0, LOW);
	muxSelector.setOutput(IO_B1, LOW);
	muxSelector.setOutput(IO_B2, LOW);

	//Initialize sensor readings to zero.
	for (int i = 0; i < NUM_LINE_SENSORS; i++)
	{
		lineSensor[i] = 0;
	}
	//serialDebug.setBaudRate(115200);
}

//Grab sensor data.
void sense()
{
	static unsigned char
		lineSensorIndex = 0;

	//Set mux inputs for which pin to read from
	//This should work because it looks at the first
	//three bits and each output to the mux is a mask looking
	//at one of each of the three bits. The result is shifted
	//over to the ones place where neccicary incase of the
	//unknown result of sending something other than 0 or 1
	//to setOutput()
	muxSelector.setOutput(IO_B0, lineSensorIndex & 1);
	muxSelector.setOutput(IO_B1, (lineSensorIndex & 2) >> 1);
	muxSelector.setOutput(IO_B2, (lineSensorIndex & 4) >> 2);

	//Not sure if the mux has a response time or if it's ready imidiately
	//after switching pins so I'm adding a small delay here just in case.
	delay_ms(5);

	//The mux controls what value is read by analogInput
	lineSensor[lineSensorIndex % 8] = analogInput.readMillivolts(0);

	//Intenionally allowing "lineSensorIndex" to rollover, it should work out.
	lineSensorIndex++;
}

//Decide what to do.
MotorControl think()
{
	MotorControl
		motorControl;
	//Temporary controls just to show that it is reading data.
	//lineSensor values range between [0,1023] but I only want
	//to send the motors [0,255] hence, the divide by 4.
	motorControl.leftMotorSpeed = lineSensor[0] >> 2;
	motorControl.rightMotorSpeed = lineSensor[7] >> 2;
	return motorControl;
}

//Perform some action.
void act(MotorControl desiredSpeeds)
{
	static int
		leftMotorSpeed = 0,
		rightMotorSpeed = 0;

	//Temporarily force ramping.
	if (desiredSpeeds.leftMotorSpeed > leftMotorSpeed)
	{
		leftMotorSpeed++;
	}
	else if(desiredSpeeds.leftMotorSpeed < leftMotorSpeed)
	{
		leftMotorSpeed--;
	}

	if (desiredSpeeds.rightMotorSpeed > rightMotorSpeed)
	{
		rightMotorSpeed++;
	}
	else if(desiredSpeeds.rightMotorSpeed < rightMotorSpeed)
	{
		rightMotorSpeed--;
	}
	//motors.setSpeeds(leftMotorSpeed,rightMotorSpeed);
}
