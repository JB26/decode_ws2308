#include <Wire.h>
#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp;


#include "DHT.h"

#define DHTPIN 12     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

DHT dht(DHTPIN, DHTTYPE);


int incomingByte = 0;   // for incoming serial data

void setup() {
        Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
        dht.begin();
        bmp.begin();
}

void loop() {

        // send data only when you receive data:
        if (Serial.available() > 0) {
                // read the incoming byte:
                incomingByte = Serial.read();
                
                if (incomingByte == 116) { // Temperatur
                  int t1 = dht.readTemperature()*10;
                  int t2 = bmp.readTemperature()*10;
                  int t = (t1 + t2)/2;
                  Serial.print(t/10);
                  Serial.print(".");
                  Serial.print(t % 10);
                  Serial.print("\n");
                }
                
                if (incomingByte == 104) { // Luftfeuchte
                  Serial.print(dht.readHumidity());
                  Serial.print("\n");
                }
                
                if (incomingByte == 112) { // Druck
                  Serial.print(bmp.readPressure());
                  Serial.print("\n");
                }

        }
}
