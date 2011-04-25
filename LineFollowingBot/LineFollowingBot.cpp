#include "stdio.h"
#include "math.h"
#include "stdlib.h"
#include "string.h"
//#include <cmath>
#include <stdlib.h>

#include <pololu/orangutan>
#include "LineFollowingBot.h"

int main()
{
	initialize();
	int
		turn = 0;
	char
		message[128];

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
	   	
		//sprintf (message, "I'm still alive! %u\r\n", OrangutanTime::ms());
		//sendMessage(message);

	}
	programRunning = true;
	while(programRunning)
	{
		sendMessage("Printing gathered data\r\n");
		OrangutanTime::delayMilliseconds(10);
		memset(message, 0, 256);
		sprintf(message, "Num Laps = %d\r\n", numLaps);
		sendMessage(message);
		OrangutanTime::delayMilliseconds(10);
		for (unsigned char i = 0; i < LAPS_PER_RUN; i++)
		{
			sendMessage("------------------------------\r\n");
			OrangutanTime::delayMilliseconds(10);
			memset(message, 0, 256);
			sprintf(message, "Run %d stats:\r\n", i);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(10);
			memset(message, 0, 256);
			sprintf(message, "P = %f, I = %f, D = %f\r\n",
				runStatHistory[i].P, runStatHistory[i].I, runStatHistory[i].D);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(10);
			memset(message, 0, 256);
			sprintf(message, "Time for Lap %d is %u\r\n", i, runStatHistory[i].lapTime);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(10);
			memset(message, 0, 256);
			sprintf(message, "Error for lap %d is %u\r\n", i, runStatHistory[i].totalError);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(10);
			
			memset(message, 0, 256);
			sprintf(message, "Best Run So Far (%.2f, %.2f, %.2f) time = %lu error = %lu\r\n",
				runStatHistory[i].bestP,
				runStatHistory[i].bestI,
				runStatHistory[i].bestD,
				runStatHistory[i].bestTime,
				runStatHistory[i].bestError);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(10);
		}
		sendMessage("Program has run to completion.\r\n");
		OrangutanTime::delayMilliseconds(10000);
	}

	return 0;
}

//Initialize board.
void initialize()
{
	OrangutanAnalog::setMode(MODE_10_BIT);//MODE_8_BIT
	OrangutanSerial::setBaudRate(9600);
	OrangutanTime::reset();
	//OrangutanMotors::setSpeeds(0,0);

	//Initialize sensor readings and random seed..
	for (int i = 0; i < NUM_LINE_SENSORS; i++)
	{
		lineSensor[i] = OrangutanAnalog::read(i);
		randNum += lineSensor[i];
	}
	seedRand(randNum);

	//Initialize first run statistics
	bestRunStat.P          = 60.0;
	bestRunStat.I          =  0.1;
	bestRunStat.D          = 10.0;
	bestRunStat.lapTime    = 9999;
	bestRunStat.totalError = 9999;

	currentRunStat.P          = 60.0;
	currentRunStat.I          =  0.1;
	currentRunStat.D          = 10.0;
	currentRunStat.lapTime    =  0;
	currentRunStat.totalError =  0;

	for (int i = 5; i > 0; i--)
	{
		char
			message[64];
		sprintf(message, "Program will start in %d\r\n", i);
		sendMessage(message);
		OrangutanTime::delayMilliseconds(1000);
	}
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
	}
}

//Decide what to do.
int think()
{
	static int
		sumError      = 0;
	static int
		oldError      = 0;
	int
		dError        = 0;
	int
		actual        = 0,
		desired       = 0,
		error         = 0,
		numActivated  = 0;
	static unsigned long
		lastFrameTime = 0;
	
	char
		message[256];

	//Calculate Error
	for (unsigned char i = 0; i < NUM_LINE_SENSORS; i++)
	{
		if (lineSensor[i] > 400)
		{
			numActivated++;
			if (i < 4) //NUM_LINE_SENSORS/2
			{
				actual -= (4 - i); //actual -= 2 * (NUM_LINE_SENSORS/2 - i)
			}
			else
			{
				actual += (i - 3); //actual += 2 * (i - NUM_LINE_SENSORS/2 - 1)
			}
		}
	}

	//We went off track.
	if (numActivated == 0)
	{
		noneActivated = true;
		allActivated  = false;
		lapStarted = false;
	}
	//We've completed a lap.
	else if (numActivated == NUM_LINE_SENSORS)
	{

		//If we just completed a lap
		if (lapStarted)
		{
			//Record lap time
			currentRunStat.lapTime = OrangutanTime::ms() - lapStartTime;
			
			runStatHistory[numLaps].P = currentRunStat.P;
			runStatHistory[numLaps].I = currentRunStat.I;
			runStatHistory[numLaps].D = currentRunStat.D;
			runStatHistory[numLaps].lapTime = currentRunStat.lapTime;
			runStatHistory[numLaps].totalError = currentRunStat.totalError;

						
			/*memset(message, 0, 128);
			sprintf (message, "bestRunStat(%u) > currentRunStat(%u) == %d\r\n",
				bestRunStat.lapTime + bestRunStat.totalError, currentRunStat.lapTime + currentRunStat.totalError,
				(bestRunStat.lapTime + bestRunStat.totalError > currentRunStat.lapTime + currentRunStat.totalError));
			sendMessage(message);*/

			//If current run is better than any previous found.
			//(First run is usually bad, so we will always say second was worse to re-run it.)
			if((bestRunStat.lapTime + bestRunStat.totalError > currentRunStat.lapTime + currentRunStat.totalError
				&& numLaps != 0 && currentRunStat.lapTime > 7000)
				|| bestRunStat.P == 0)
			{
				//memset(message, 0, 128);
				sendMessage("New Best Found!\r\n");
				bestRunStat.P          = currentRunStat.P;
				bestRunStat.I          = currentRunStat.I;
				bestRunStat.D          = currentRunStat.D;
				bestRunStat.lapTime    = currentRunStat.lapTime;
				bestRunStat.totalError = currentRunStat.totalError;
				runStatHistory[numLaps].bestP = currentRunStat.P;
				runStatHistory[numLaps].bestI = currentRunStat.I;
				runStatHistory[numLaps].bestD = currentRunStat.D;
				runStatHistory[numLaps].bestTime = currentRunStat.lapTime;
				runStatHistory[numLaps].bestError = currentRunStat.totalError;
			}
			else
			{
				runStatHistory[numLaps].P = currentRunStat.P;
				runStatHistory[numLaps].I = currentRunStat.I;
				runStatHistory[numLaps].D = currentRunStat.D;
				runStatHistory[numLaps].lapTime = currentRunStat.lapTime;
				runStatHistory[numLaps].totalError = currentRunStat.totalError;
				runStatHistory[numLaps].bestP = bestRunStat.P;
				runStatHistory[numLaps].bestI = bestRunStat.I;
				runStatHistory[numLaps].bestD = bestRunStat.D;
				runStatHistory[numLaps].bestTime = bestRunStat.bestTime;
				runStatHistory[numLaps].bestError = bestRunStat.bestError;
			}

			sendMessage("Got here\r\n");
			/*memset(message, 0, 128);
			sprintf(message, "(%.1f %.1f %.1f)\r\n",
					currentRunStat.P, currentRunStat.I, currentRunStat.D);
			sendMessage(message);*/
			/*memset(message, 0, 128);
			sprintf(message, "(%.1f %.1f %.1f) Best (%.1f %.1f %.1f)\r\n",
					currentRunStat.P, currentRunStat.I, currentRunStat.D,
					bestRunStat.P, bestRunStat.I, bestRunStat.D);
			sendMessage(message);*/

			numLaps++;

			//Calculate new P, I, D values
			do
				currentRunStat.P = bestRunStat.P + (float)annealNumerator/(float)annealDenominator * randFloatRange(-annealStepP, annealStepP);
			while (currentRunStat.P < 0 || currentRunStat.P > bestRunStat.P + annealStepP || currentRunStat.P < bestRunStat.P - annealStepP);
			
			do
			currentRunStat.I = bestRunStat.I + (float)annealNumerator/(float)annealDenominator * randFloatRange(-annealStepI, annealStepI);
			while (currentRunStat.I < 0 || currentRunStat.I > bestRunStat.I + annealStepI || currentRunStat.I < bestRunStat.I - annealStepI);
			
			do
			currentRunStat.D = bestRunStat.D + (float)annealNumerator/(float)annealDenominator * randFloatRange(-annealStepD, annealStepD);
			while (currentRunStat.D < 0 || currentRunStat.D > bestRunStat.D + annealStepD || currentRunStat.D < bestRunStat.D - annealStepD);

			annealNumerator--;

			//Reset Runtime and error
			currentRunStat.lapTime    = 0;
			currentRunStat.totalError = 0;

			//Print new P, I, D values
			/*
			memset(message, 0, 128);
			sprintf (message, "CurrentBest = (%.2f, %.2f, %.2f), with time = %u and error = %u \r\n Starting P = %.2f, I = %.2f, D = %.2f\r\n",
				bestRunStat.P, bestRunStat.I, bestRunStat.D, bestRunStat.lapTime, bestRunStat.totalError,
				currentRunStat.P, currentRunStat.I, currentRunStat.D);
			sendMessage(message);*/

			if (numLaps == LAPS_PER_RUN)
			{
				programRunning = false;
			}
		}
		noneActivated = false;
		allActivated  = true;
		lapStarted    = false;
	}
	//We are trying to follow the line.
	else
	{
		//If we just left the line
		if (allActivated)
		{
			lapStarted = true;
			lapStartTime = OrangutanTime::ms();

		}
		noneActivated = false;
		allActivated  = false;
		sumError = 0;
	}


	//The P multiplicand
	error = desired - actual;

	currentRunStat.totalError += abs(error);
	
	//The D multiplicand
	dError = (2 * error - oldError) / (long)((OrangutanTime::ms() - lastFrameTime));
	

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
	return currentRunStat.P * error + currentRunStat.I * sumError + currentRunStat.D * dError;
}

//Perform some action.
void act(int turnRate)
{
	static const int
		forward = 1000;
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

 	if (!( -255 < desiredLeftMotorSpeed  || desiredLeftMotorSpeed  < 255
 		|| -255 < desiredRightMotorSpeed || desiredRightMotorSpeed < 255))
	{
		char
			message[256];
	    memset(message, 0, 256);
		sprintf (message, "Overspeed! Turn Rate %d\r\n", turnRate);
		sendMessage(message);
	}

	if (!programRunning)
	{
		OrangutanMotors::setSpeeds(0,0);
	}
	else if (noneActivated) 
	{
		//We went off track..
		OrangutanMotors::setSpeeds(0,0);
		currentRunStat.totalError += 100;
	}
	else
	{
		OrangutanMotors::setSpeeds(desiredLeftMotorSpeed, desiredRightMotorSpeed);
	}
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

void seedRand(int seed)
{
	randNum = seed % MAX_PRIME;
}

int randInt()
{
	randNum = randNum * MID_PRIME % MAX_PRIME;
	return randNum;
}

int randIntRange(int minVal, int maxVal)
{
	return (maxVal - minVal) * randInt() + minVal;
}

float randFloat()
{
	return (float)randInt()/(float)MAX_PRIME;
}

float randFloatRange(float minVal, float maxVal)
{
	return randFloat() * (maxVal - minVal) + minVal; 
}

