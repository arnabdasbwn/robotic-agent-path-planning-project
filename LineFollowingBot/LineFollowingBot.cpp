#include "stdio.h"
#include "math.h"
#include "stdlib.h"
#include "string.h"
//#include <cmath>
#include <stdlib.h>
//#include <iostream>
#include <pololu/orangutan>
#include "LineFollowingBot.h"

int main()
{
	initialize();
	int
		turn = 0;
	char
		*message = "Hello Serial!\r\n";
	OrangutanSerial::sendBlocking(message, strlen(message));
	//programRunning will always be true... I just hate while(1)'s.
	while (programRunning)
	{
		sense();
		turn = think();

		/*char
			message[256];
	    memset(message, 0, 256);
		sprintf (message, "turn = %d\r\n", turn);
		OrangutanSerial::sendBlocking(message, strlen(message));*/

		act(turn);
		//OrangutanMotors::setSpeeds(-50,0);

	}
	return 0;
}

//Initialize board.
void initialize()
{
	OrangutanAnalog::setMode(MODE_10_BIT);//MODE_8_BIT

	//Initialize sensor readings to zero.
	for (int i = 0; i < NUM_LINE_SENSORS; i++)
	{
		lineSensor[i] = 0;
	}
	OrangutanSerial::setBaudRate(9600);
	OrangutanTime::reset();

}

//Grab sensor data.
void sense()
{
	float
		filterStrength = 0.1f; //Larger number means less responsive to change.

	//The mux controls what value is read by analogInput
	for (unsigned char i = 0; i < 8; i++)
	{
		lineSensor[i] = (1-filterStrength) * OrangutanAnalog::read(i) 
						+ filterStrength * lineSensor[i];
		/*char
			message[256];
	    memset(message, 0, 256);
		sprintf (message, "Sensor %d value = %d\r\n", i, lineSensor[i]);
		OrangutanSerial::sendBlocking(message, strlen(message));*/
	}
}

//Decide what to do.
int think()
{
	static const int
		P = 35,
		I = 0,
		D = 0;
	static int
		sumError = 0,
		oldError = 0;
	int
		actual   = 0,
		desired  = 0,
		error    = 0,
		dError   = 0;
	static unsigned long
		lastFrameTime = OrangutanTime::us();
	
	//Calculate Error
	for (unsigned char i = 1; i < 7; i++)
	{
		if (i < 4)
		{
			if (lineSensor[i] > 400)
			{
				actual -= 2 * (4 - i);//lineSensor[i];
			}
		}
		else
		{
			if (lineSensor[i] > 400)
			{
				actual += 2 * (i - 3);//lineSensor[i];
			}
		}
	}

	/*char
		message[256];
    memset(message, 0, 256);
	sprintf (message, "actual difference = %d\r\n", actual);
	OrangutanSerial::sendBlocking(message, strlen(message));*/

	//The P multiplicand
	error = desired - actual;

	//The D multiplicand
	dError = (error - oldError) / (OrangutanTime::ms() - lastFrameTime);
	/*
	char
		message[256];
    memset(message, 0, 256);
	sprintf (message, "dError = %d -", dError);
	OrangutanSerial::sendBlocking(message, strlen(message));
	memset(message, 0, 256);
	sprintf (message, "deltaT = %d\r\n", dError);
	OrangutanSerial::sendBlocking(message, OrangutanTime::ms() - lastFrameTime);
*/
	//The I multiplicand
	sumError += error * (OrangutanTime::ms() - lastFrameTime);

	//Set old error to current
	oldError = error;

	lastFrameTime = OrangutanTime::ms();

	//Turn rate
	return P * error + I * sumError + D * dError;
}

//Perform some action.
void act(int turnRate)
{
	static const int
		forward = 180,
		ramp = 2;
	static int
		leftMotorSpeed = 0,
		rightMotorSpeed = 0;
	int
		desiredLeftMotorSpeed = 0,
		desiredRightMotorSpeed = 0,
		forwardComponent = forward / 2,
		turnComponent = turnRate / 2;

		//Retain full ability to turn even when speed is maxxed.
		if (forwardComponent + abs(turnComponent) > 255)
		{
			forwardComponent = 255 - abs(turnComponent);
		}

		desiredLeftMotorSpeed = forwardComponent + turnComponent;
		desiredRightMotorSpeed = forwardComponent - turnComponent;

	/************Forced Ramping*************************
	if (desiredLeftMotorSpeed > leftMotorSpeed)
	{
		leftMotorSpeed += ramp;
	}
	else if(desiredLeftMotorSpeed < leftMotorSpeed)
	{
		leftMotorSpeed -= ramp;
	}

	if (desiredRightMotorSpeed > rightMotorSpeed)
	{
		rightMotorSpeed += ramp;
	}
	else if(desiredRightMotorSpeed < rightMotorSpeed)
	{
		rightMotorSpeed -= ramp;
	}
	/*******************No Ramping***********************
	leftMotorSpeed = desiredSpeeds.leftMotorSpeed;
	rightMotorSpeed = desiredSpeeds.rightMotorSpeed;
	****************************************************/

	//char
	//	message[256];
    //memset(message, 0, 256);
	//sprintf (message, "MotorSpeeds (%d, %d)\r\n", desiredLeftMotorSpeed, desiredRightMotorSpeed);
	//OrangutanSerial::sendBlocking(message, strlen(message));


	OrangutanMotors::setSpeeds(desiredLeftMotorSpeed,desiredRightMotorSpeed);
	//OrangutanMotors::setSpeeds(leftMotorSpeed,rightMotorSpeed);
}

// Failed attempt to create a function that can send a const
// with no compile warnings.
void sendConstMessage(const char* message)
{
	char
		*data = static_cast<char*>(malloc(sizeof(char) * strlen(message)));
	OrangutanSerial::sendBlocking(data, strlen(data));
	free(data);
}