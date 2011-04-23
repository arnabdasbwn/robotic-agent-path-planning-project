#ifndef LINE_FOLLOWING_BOT_H
#define LINE_FOLLOWING_BOT_H

bool
	programRunning = true,
	allActivated = false,
	noneActivated = false,
	firstRun = true,
	lapStarted = false;
int
	numRuns = 0,
	numLaps = 0;

static const int
	MAX_SPEED        = 255,
	NUM_LINE_SENSORS =   8,
	LAPS_PER_RUN     =   7,
	MAX_RUNS         =   1;
static const unsigned long
	MESSAGE_DELAY = 10;	//Delay in ms between times we send serial data.
static unsigned int
	lineSensor[NUM_LINE_SENSORS];
static unsigned long
	lastMessageSentTime = 0,
	lapStartTime = 0,
	totalError[LAPS_PER_RUN],
	lapTimeTable[LAPS_PER_RUN];


void initialize();
void sense();
int think();
void act(int turnRate);
void sendConstMessage(const char* message);
void sendMessage(char* message);

#endif
