#include "Wire.h"
#include <ArduinoJson.h>

#define DS3231_I2C_ADDRESS 0x68

#include <dht.h>

dht DHT;

#define DHT11_PIN 7

// Convert decimal number to binary
byte decToBcd(byte val) {
  return ((val / 10 * 16) + (val % 10));
}

// Convert binary number to decimal
byte bcdToDec(byte val) {
  return ((val / 16 * 10) + (val % 16));
}

// For the initial setup of the time on the clock
// dayofweek is a number from 1 - 7 - not currently being used
// year is a 2 digit number (assumed prefix is 20)
void setTime(byte second, byte minute, byte hour, byte dayofweek, byte day, byte month, byte year) {
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  Wire.write(0);
  Wire.write(decToBcd(second));
  Wire.write(decToBcd(minute));
  Wire.write(decToBcd(hour));
  Wire.write(decToBcd(dayofweek));
  Wire.write(decToBcd(day));
  Wire.write(decToBcd(month));
  Wire.write(decToBcd(year));
  Wire.endTransmission();
}

// Read the current time from the clock
void readTime(byte *second, byte *minute, byte *hour, byte *dayofweek, byte *day, byte *month, byte *year) {
  Wire.beginTransmission(DS3231_I2C_ADDRESS);
  // set DS3231 register pointer to 00h
  Wire.write(0);
  Wire.endTransmission();
  Wire.requestFrom(DS3231_I2C_ADDRESS, 7);
  // request seven bytes of data from DS3231 starting from register 00h
  *second = bcdToDec(Wire.read() & 0x7f);
  *minute = bcdToDec(Wire.read());
  *hour = bcdToDec(Wire.read() & 0x3f);
  *dayofweek = bcdToDec(Wire.read());
  *day = bcdToDec(Wire.read());
  *month = bcdToDec(Wire.read());
  *year = bcdToDec(Wire.read());
}

// Get the datetime as a String - format is YYYYMMDDHHMMSS
String getDateTime() {
  byte second, minute, hour, day, dayofweek, month, year;
  // retrieve data from DS3231
  readTime(&second, &minute, &hour, &dayofweek, &day, &month, &year);
  // Build up the datetime string
  String datetime = "20" + String(year, DEC);
  if (month < 10) {
    datetime += "0";
  }
  datetime += String(month, DEC);
  if (day < 10) {
    datetime += "0";
  }
  datetime += String(day, DEC);
  if (hour < 10) {
    datetime += "0";
  }
  datetime += String(hour, DEC);
  if (minute < 10) {
    datetime += "0";
  }
  datetime += String(minute, DEC);
  if (second < 10) {
    datetime += "0";
  }
  datetime += String(second, DEC);
  return datetime;
}

void sendjson(float Temp, float hum){//, String time){
  StaticJsonDocument<200> doc;
  doc["int_temp"] = Temp;
  doc["rel_hum"] = hum;
 // doc["Temp"] = Temp;
  Serial.println();
  serializeJson(doc, Serial);
}


void setup() {
  Wire.begin();
  Serial.begin(9600);
  // set the initial time here
}

void loop() { //Run Forever
  int chk = DHT.read11(DHT11_PIN);
  sendjson(DHT.temperature,DHT.humidity);//,getDateTime());
  delay(1000);  // every second
}
