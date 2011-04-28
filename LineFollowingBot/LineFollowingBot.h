#ifndef LINE_FOLLOWING_BOT_H
#define LINE_FOLLOWING_BOT_H

#include "stdio.h"
#include "math.h"
#include "stdlib.h"
#include "string.h"
//#include <cmath>
#include <stdlib.h>

// If you want to do more than 20 runs or so, you will have to comment this next line out
// The microcontroller has limited memory and cannot store history for an arbitrary number of runs.
#define KEEP_STAT_HISTORY

struct RunStat
{
	// Using floats on a micro-controller is bad since there usually isn't any hardware support
	// for them and have to be calculated in software. For better performance, it would probably
	// be better if I multiplied values by some number to keep them all in the integer range.
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

static const int
	MAX_SPEED        =  255,
	NUM_LINE_SENSORS =    8,
	NUM_LAPS         =   20,
	MAX_PRIME        = 1303,
	MID_PRIME        = 1301;

int
	numLaps           = 0,
	annealNumerator   = NUM_LAPS,
	annealDenominator = NUM_LAPS,
	randNum           = 0;


static const unsigned long
	MESSAGE_DELAY = 10;	//Delay in ms between times we send serial data.
static unsigned int
	lineSensor[NUM_LINE_SENSORS];
static unsigned long
	lastMessageSentTime = 0,
	lapStartTime = 0;

struct RunStat
#ifdef KEEP_STAT_HISTORY
	runStatHistory[NUM_LAPS],
#endif
	runStat;

float
	annealStepP = 20.00,
	annealStepI =  0.05,
	annealStepD =  5.00;
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
#endif
