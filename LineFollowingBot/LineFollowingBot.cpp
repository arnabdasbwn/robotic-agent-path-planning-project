#include "stdio.h"
#include "stdlib.h"
#include "string.h"
//#include <iostream>
#include <pololu/orangutan>
#include "LineFollowingBot.h"

int main()
{
	MotorControl
		speeds;
		
	initialize();
	char
		*message = "Hello Serial!\r\n";
	OrangutanSerial::sendBlocking(message, strlen(message));
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
	OrangutanAnalog::setMode(MODE_10_BIT);//MODE_8_BIT

	//Initilize the outputs to the mux
	OrangutanDigital::setOutput(IO_B0, LOW);
	OrangutanDigital::setOutput(IO_B1, LOW);
	OrangutanDigital::setOutput(IO_B2, LOW);

	//Initialize sensor readings to zero.
	for (int i = 0; i < NUM_LINE_SENSORS; i++)
	{
		lineSensor[i] = 0;
	}
	OrangutanSerial::setBaudRate(9600);
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

	//OrangutanDigital::setOutput(IO_B0, lineSensorIndex & 1);
	//OrangutanDigital::setOutput(IO_B1, (lineSensorIndex & 2) >> 1);
	//OrangutanDigital::setOutput(IO_B2, (lineSensorIndex & 4) >> 2);

	OrangutanDigital::setOutput(IO_B0, 0);
	OrangutanDigital::setOutput(IO_B1, 0);
	OrangutanDigital::setOutput(IO_B2, 0);

	//Not sure if the mux has a response time or if it's ready imidiately
	//after switching pins so I'm adding a small delay here just in case.
	delay_ms(1000);

	//The mux controls what value is read by analogInput
	lineSensor[lineSensorIndex % 8] = OrangutanAnalog::readMillivolts(0);
	//lineSensor[lineSensorIndex % 8] = OrangutanAnalog::toMillivolts(OrangutanAnalog::read(0));
	char
		message[256];
    memset(message, 0, 256);
	sprintf (message, "Sensor %d value = %d\r\n", lineSensorIndex % 8, lineSensor[lineSensorIndex]);
	OrangutanSerial::sendBlocking(message, strlen(message));
	//Intenionally allowing "lineSensorIndex" to rollover, it should work out.
	lineSensorIndex++;
}

//Decide what to do.
MotorControl think()
{
	MotorControl
		motorControl;
	/*****Ramp Motors up and down***
	static bool
		speedUp = true;
	static int
		motorSpeed = 0;
	if (speedUp)
	{
		motorSpeed++;
	}
	else
	{
		motorSpeed--;
	}
	if (motorSpeed >= 250)
	{
		speedUp = false;
	}
	if (motorSpeed <= -250)
	{
		speedUp = true;
	}
	motorControl.leftMotorSpeed = motorSpeed;
	motorControl.rightMotorSpeed = motorSpeed;
	**********************************/
	//Temporary controls just to show that it is reading data.
	//lineSensor values range between [0,1023] but I only want
	//to send the motors [0,255] hence, the divide by 4.
	motorControl.leftMotorSpeed = lineSensor[0];// >> 2;
	motorControl.rightMotorSpeed = lineSensor[7];// >> 2;
	/************************************/
	return motorControl;
}

//Perform some action.
void act(MotorControl desiredSpeeds)
{
	static int
		leftMotorSpeed = 0,
		rightMotorSpeed = 0;

	/************Forced Ramping*************************/
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
	/*******************No Ramping***********************
	leftMotorSpeed = desiredSpeeds.leftMotorSpeed;
	rightMotorSpeed = desiredSpeeds.rightMotorSpeed;
	****************************************************/
	//motors.setSpeeds(leftMotorSpeed,rightMotorSpeed);
	//OrangutanMotors::setSpeeds(25,25);
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
