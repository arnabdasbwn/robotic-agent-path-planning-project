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
		act(turn);
	}
	programRunning = true;
	while(programRunning)
	{
		sendMessage("Printing gathered data\r\n");
		OrangutanTime::delayMilliseconds(100);
		memset(message, 0, 256);
		sprintf(message, "Will run for %d laps = %d\r\n", LAPS_PER_RUN);
		sendMessage(message);
		OrangutanTime::delayMilliseconds(100);
		memset(message, 0, 256);
		sprintf(message, "Using anneal values (%f, %f, %f)\r\n", annealStepP, annealStepI, annealStepD);
		sendMessage(message);
		OrangutanTime::delayMilliseconds(100);
		for (unsigned char i = 0; i < LAPS_PER_RUN; i++)
		{
			sendMessage("\r\n------------------------------\r\n");
			OrangutanTime::delayMilliseconds(100);
			memset(message, 0, 256);
			sprintf(message, "Run %d stats:\r\n", i + 1);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(100);
			memset(message, 0, 256);
			sprintf(message, "P = %f, I = %f, D = %f\r\n",
				runStatHistory[i].P, runStatHistory[i].I, runStatHistory[i].D);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(100);
			memset(message, 0, 256);
			sprintf(message, "Time for Lap %d is %u\r\n", i + 1, runStatHistory[i].lapTime);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(100);
			memset(message, 0, 256);
			sprintf(message, "Error for lap %d is %u\r\n", i + 1, runStatHistory[i].totalError);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(100);
			
			memset(message, 0, 256);
			sprintf(message, "Best Run So Far (%.2f, %.2f, %.2f) time = %lu error = %lu\r\n",
				runStatHistory[i].bestP,
				runStatHistory[i].bestI,
				runStatHistory[i].bestD,
				runStatHistory[i].bestTime,
				runStatHistory[i].bestError);
			sendMessage(message);
			OrangutanTime::delayMilliseconds(100);
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
	runStat.P          = 60.0;
	runStat.I          =  0.1;
	runStat.D          = 10.0;
	runStat.lapTime    = 	0;
	runStat.totalError = 	0;

	runStat.bestP      = 50.0;
	runStat.bestI      =  0.1;
	runStat.bestD      = 10.0;
	runStat.bestTime   = 9999;
	runStat.bestError  = 9999;

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
			runStat.lapTime = OrangutanTime::ms() - lapStartTime;
						
			/*memset(message, 0, 128);
			sprintf (message, "bestRunStat(%u) > currentRunStat(%u) == %d\r\n",
				bestRunStat.lapTime + bestRunStat.totalError, currentRunStat.lapTime + currentRunStat.totalError,
				(bestRunStat.lapTime + bestRunStat.totalError > currentRunStat.lapTime + currentRunStat.totalError));
			sendMessage(message);*/

			//Update current run in history regardless of whether it's a winner.
			runStatHistory[numLaps].P = runStat.P;
			runStatHistory[numLaps].I = runStat.I;
			runStatHistory[numLaps].D = runStat.D;
			runStatHistory[numLaps].lapTime    = runStat.lapTime;
			runStatHistory[numLaps].totalError = runStat.totalError;

			//If current run is better than any previous found.
			//(First run is usually bad, so we will always say second was worse to re-run it.)
			if((runStat.bestTime + runStat.bestError > runStat.lapTime + runStat.totalError
				&& numLaps != 0 && runStat.lapTime > 7000)
				|| runStat.bestP == 0)
			{
				//memset(message, 0, 128);
				sendMessage("New Best Found!\r\n");
				runStat.bestP          = runStat.P;
				runStat.bestI          = runStat.I;
				runStat.bestD          = runStat.D;
				runStat.bestTime       = runStat.lapTime;
				runStat.bestError      = runStat.totalError;
				runStatHistory[numLaps].bestP     = runStat.P;
				runStatHistory[numLaps].bestI     = runStat.I;
				runStatHistory[numLaps].bestD     = runStat.D;
				runStatHistory[numLaps].bestTime  = runStat.lapTime;
				runStatHistory[numLaps].bestError = runStat.totalError;
			}
			else
			{
				runStatHistory[numLaps].bestP = runStat.bestP;
				runStatHistory[numLaps].bestI = runStat.bestI;
				runStatHistory[numLaps].bestD = runStat.bestD;
				runStatHistory[numLaps].bestTime = runStat.bestTime;
				runStatHistory[numLaps].bestError = runStat.bestError;
			}

			numLaps++;

			//Calculate new P, I, D values
			do
				runStat.P = runStat.bestP + (float)annealNumerator/(float)annealDenominator * randFloatRange(-annealStepP, annealStepP);
			while (runStat.P < 0 || runStat.P > runStat.bestP + annealStepP || runStat.P < runStat.bestP - annealStepP);
			
			do
				runStat.I = runStat.bestI + (float)annealNumerator/(float)annealDenominator * randFloatRange(-annealStepI, annealStepI);
			while (runStat.I < 0 || runStat.I > runStat.bestI + annealStepI || runStat.I < runStat.bestI - annealStepI);
			
			do
				runStat.D = runStat.bestD + (float)annealNumerator/(float)annealDenominator * randFloatRange(-annealStepD, annealStepD);
			while (runStat.D < 0 || runStat.D > runStat.bestD + annealStepD || runStat.D < runStat.bestD - annealStepD);

			annealNumerator--;

			//Reset Runtime and error
			runStat.lapTime    = 0;
			runStat.totalError = 0;

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

	runStat.totalError += abs(error);
	
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
	return runStat.P * error + runStat.I * sumError + runStat.D * dError;
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
		runStat.totalError += 100;
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
		OrangutanSerial::send(message, strlen(message));
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

