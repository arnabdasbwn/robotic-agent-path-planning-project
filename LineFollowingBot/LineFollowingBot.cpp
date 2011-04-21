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
		*message = "Hello Serial!             \r\n";
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

	
	   	
		sprintf (message, "I'm still alive! %u\r\n", OrangutanTime::ms());
		sendMessage(message);

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
		//char
		//	message[256];
	    //memset(message, 0, 256);
		//sprintf (message, "Sensor %d value = %d\r\n", i, lineSensor[i]);
		//OrangutanSerial::sendBlocking(message, strlen(message));
	}
}

//Decide what to do.
int think()
{
	static const float
		P = 25,
		I = 0.0,
		D = 15;
	static int
		sumError = 0;
	static int
		oldError = 0;
	int
		dError   = 0;
	int
		actual   = 0,
		desired  = 0,
		error    = 0;
	static unsigned long
		lastFrameTime = 0;
	
	char
		message[256];

	//Calculate Error
	for (unsigned char i = 0; i < 8; i++)
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

	//The P multiplicand
	error = desired - actual;

	//The D multiplicand
	dError = (error - oldError) / (long)((OrangutanTime::ms() - lastFrameTime));
	

	//sendMessage(message);

	OrangutanTime::delayMicroseconds(100);
	//The I multiplicand
	sumError += error * (OrangutanTime::ms() - lastFrameTime);


	//Set old error to current
	oldError = error;

	lastFrameTime = OrangutanTime::ms();


    //memset(message, 0, 256);
	//sprintf (message, "P = %d, I = %d, D = %d \r\n turnRate = %d \r\n",
	//		 P*error, I*sumError, D*dError, P*error+I*sumError+D*dError);
	//sendMessage(message);

	//Turn rate
	return P * error + I * sumError + D * dError;
}

//Perform some action.
void act(int turnRate)
{
	static const int
		forward = 500;
		//ramp = 2;
	//static int
	//	leftMotorSpeed = 0,
	//	rightMotorSpeed = 0;
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

	/************Forced Ramping*************************/
	//if (desiredLeftMotorSpeed > leftMotorSpeed)
	//{
	//	leftMotorSpeed += ramp;
	//}
	//else if(desiredLeftMotorSpeed < leftMotorSpeed)
	//{
	//	leftMotorSpeed -= ramp;
	//}

	//if (desiredRightMotorSpeed > rightMotorSpeed)
	//{
	//	rightMotorSpeed += ramp;
	//}
	//else if(desiredRightMotorSpeed < rightMotorSpeed)
	//{
	//	rightMotorSpeed -= ramp;
	//}
	/*******************No Ramping***********************/
	//leftMotorSpeed = desiredSpeeds.leftMotorSpeed;
	//rightMotorSpeed = desiredSpeeds.rightMotorSpeed;
	/****************************************************/

	//char
	//	message[256];
    //memset(message, 0, 256);
	//sprintf (message, "MotorSpeeds (%d, %d)\r\n", desiredLeftMotorSpeed, desiredRightMotorSpeed);
	//OrangutanSerial::sendBlocking(message, strlen(message));


	OrangutanMotors::setSpeeds(desiredLeftMotorSpeed, desiredRightMotorSpeed);
	//OrangutanMotors::setSpeeds(0,0);
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
void sendMessage(char* message)
{
	unsigned long
		currentTime = OrangutanTime::ms();
	/**********************************************
	char
		message2[256];

	memset(message2, 0, 256);
	sprintf (message2, "lastMessageSentTime + MESSAGE_DELAY > currentTime\r\n");
	OrangutanSerial::sendBlocking(message2, strlen(message2));

	memset(message2, 0, 256);
	sprintf (message2, "%lu + %u > %lu\r\n", lastMessageSentTime, 10000, currentTime);
	OrangutanSerial::sendBlocking(message2, strlen(message2));
	****** *********************************************/
	if (lastMessageSentTime + MESSAGE_DELAY > currentTime)
	{
		//OrangutanSerial::sendBlocking(message, strlen(message));
		//OrangutanTime::delayMilliseconds(1000);
		//OrangutanSerial::sendBlocking("TRUE\r\n", strlen("TRUE\r\n"));
	}
	else
	{
		OrangutanSerial::sendBlocking(message, strlen(message));
		//OrangutanTime::delayMilliseconds(100);
		lastMessageSentTime = currentTime;
		/************************************************/
		//OrangutanSerial::sendBlocking("FALSE\r\n", strlen("FALSE\r\n"));
		//OrangutanTime::delayMilliseconds(1000);
	}

}
