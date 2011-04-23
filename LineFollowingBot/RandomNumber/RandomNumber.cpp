#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include <pololu/orangutan>

int
	seed = 7;
unsigned long
	maxPrime = 1303,
	midPrime = 1301;
	
int randInt();
int randIntRange(int min, int max);
float randFloat();
float randFloatRange(float min, float max);

int main()
{
	char
		message[64];
	
	OrangutanAnalog::setMode(MODE_10_BIT);//MODE_8_BIT
	OrangutanSerial::setBaudRate(9600);

	while(true)
	{
		memset(message, 0, 64);
		sprintf(message, "%d\r\n", randInt());
		OrangutanSerial::sendBlocking(message, strlen(message));
		OrangutanTime::delayMilliseconds(1000);
	}
}

int randInt()
{
	seed = seed * midPrime % maxPrime;
	return seed;
}

int randIntRange(int minVal, int maxVal)
{
	return (maxVal - minVal) * randFloat() + minVal;
}

float randFloat()
{
	return (float)randInt()/(float)maxPrime;
}

float randFloatRange(float minVal, float maxVal)
{
	return (randFloat() * (maxVal - minVal) + minVal); 
}
