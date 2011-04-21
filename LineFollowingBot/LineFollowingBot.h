#ifndef LINE_FOLLOWING_BOT_H
#define LINE_FOLLOWING_BOT_H

bool
	programRunning = true;
static const int
	MAX_SPEED = 255,
	NUM_LINE_SENSORS = 8;
static const unsigned long
	MESSAGE_DELAY = 1000;	//Delay in ms between times we send serial data.
static unsigned int
	lineSensor[NUM_LINE_SENSORS];
static unsigned long
	lastMessageSentTime = 0;

void initialize();
void sense();
int think();
void act(int turnRate);
void sendConstMessage(const char* message);
void sendMessage(char* message);

#endif
