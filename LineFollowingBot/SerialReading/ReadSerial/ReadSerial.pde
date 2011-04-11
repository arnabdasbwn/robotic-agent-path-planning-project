
void setup()
{
	Serial.begin(9600);	// opens serial port, sets data rate to 9600 bps
        Serial1.begin(9600);
}

void loop()
{
  if (Serial1.available())
  {
    Serial.print(Serial1.read(), BYTE);
  }
}

