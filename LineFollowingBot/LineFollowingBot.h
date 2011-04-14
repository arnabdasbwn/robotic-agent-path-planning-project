#ifndef LINE_FOLLOWING_BOT_H
#define LINE_FOLLOWING_BOT_H

bool
	programRunning = true;
static const int
	MAX_SPEED = 255,
	NUM_LINE_SENSORS = 8;
static unsigned int
	lineSensor[NUM_LINE_SENSORS];

void initialize();
void sense();
int think();
void act(int turnRate);
void sendConstMessage(const char* message);

#endif
