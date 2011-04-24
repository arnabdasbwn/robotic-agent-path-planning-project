#ifndef LINE_FOLLOWING_BOT_H
#define LINE_FOLLOWING_BOT_H

#include "stdio.h"
#include "math.h"
#include "stdlib.h"
#include "string.h"
//#include <cmath>
#include <stdlib.h>

unsigned const int size = 10;
char q[128][size];
unsigned int qIndex = 0,
			 lastIndex = 0;



struct RunStat
{
	float
		P,
		I,
		D,
		bestP,
		bestI,
		bestD;
	unsigned long
		totalError,
		lapTime,
		bestError,
		bestTime;
};

bool
	programRunning = true,
	allActivated = false,
	noneActivated = false,
	firstRun = true,
	lapStarted = false,
	empty = true;

int
	numLaps           = 0,
	annealNumerator   = 100,
	annealDenominator = 100,
	randNum           = 0;

static const int
	MAX_SPEED        =  255,
	NUM_LINE_SENSORS =    8,
	LAPS_PER_RUN     =    7,
	MAX_RUNS         =    1,
	MAX_PRIME        = 1303,
	MID_PRIME        = 1301;

static const unsigned long
	MESSAGE_DELAY = 10;	//Delay in ms between times we send serial data.
static unsigned int
	lineSensor[NUM_LINE_SENSORS];
static unsigned long
	lastMessageSentTime = 0,
	lapStartTime = 0;

struct RunStat
	bestRunStat,
	currentRunStat,
	runStatHistory[LAPS_PER_RUN];

float
	annealStepP = 10.0,
	annealStepI =  0.0,
	annealStepD =  0.0;
/*double
	annealStepP =  1.0,
	annealStepI =  0.0,
	annealStepD =  0.0;*/

void initialize();
void sense();
int think();
void act(int turnRate);
void sendConstMessage(const char* message);
void sendMessage(char* message);
void seedRand(int seed);
int randInt();
int randIntRange(int min, int max);
float randFloat();
float randFloatRange(float min, float max);
void enqueue(char* message);
void dequeue();

#endif
