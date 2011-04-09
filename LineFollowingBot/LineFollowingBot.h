#ifndef LINE_FOLLOWING_BOT_H
#define LINE_FOLLOWING_BOT_H

bool
	programRunning = true;
static const int
	MAX_SPEED = 255,
	NUM_LINE_SENSORS = 8;
static char
	lineSensor[NUM_LINE_SENSORS];
//OrangutanMotors
//	motors;
//OrangutanDigital
//	muxSelector;
//OrangutanAnalog
//	analogInput;
//OrangutanSerial
//	serialDebug;

struct MotorControl
{
	int
		leftMotorSpeed,
		rightMotorSpeed;
};

void initialize();
void sense();
MotorControl think();
void act(MotorControl desiredSpeeds);
void sendConstMessage(const char* message);

#endif
