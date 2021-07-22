/* LIBRARIES */
#include <ArduinoJson.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

RF24 radio(7, 8);
const byte address[6] = "00001";

struct Data_Package {
  int module;
  float T1;
  float T2;
  float T3;
  float T4;
  float T5;
  float T6;
  bool overheat;
};

Data_Package data;

void setup() {
    Serial.begin(9600);

    radio.begin();
    radio.openReadingPipe(0, address);
    radio.setDataRate(RF24_250KBPS);
    radio.setPALevel(RF24_PA_MIN);
    radio.startListening();
    Serial.println("Got here");
}


void loop() {
  if (radio.available()) {

    radio.read(&data, sizeof(Data_Package));
    Serial.print("Module: ");
    Serial.println(data.module);
    Serial.println(data.T1);
    Serial.println(data.T2);
    Serial.println(data.T3);
//    Serial.println(data.T4);
//    Serial.println(data.T5);
//    Serial.println(data.T6);
    Serial.println(data.overheat);
    Serial.println("------------------------");
  
  }
}