#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <ArduinoJson.h>
#include <MPU6050.h>

const char* WIFI_NAME="YOUR_WIFI";
const char* WIFI_PASSWORD="YOUR_PASSWORD";

const char* API=
"https://arise-soccertracker.onrender.com/sensor-data";

MPU6050 mpu;

int session_id=1;

void setup() {

Serial.begin(115200);

Wire.begin();

WiFi.begin(
WIFI_NAME,
WIFI_PASSWORD
);

while(
WiFi.status()!=WL_CONNECTED
){
delay(500);
Serial.print(".");
}

Serial.println();
Serial.println("Connected");

mpu.initialize();

if(
!mpu.testConnection()
){

Serial.println(
"MPU6050 failed"
);

while(true);

}

Serial.println(
"MPU6050 Ready"
);

}

void loop() {

int16_t ax;
int16_t ay;
int16_t az;

int16_t gx;
int16_t gy;
int16_t gz;

mpu.getMotion6(
&ax,
&ay,
&az,
&gx,
&gy,
&gz
);

float accel_x=ax/16384.0;
float accel_y=ay/16384.0;
float accel_z=az/16384.0;

float gyro_x=gx/131.0;
float gyro_y=gy/131.0;
float gyro_z=gz/131.0;

sendData(
accel_x,
accel_y,
accel_z,
gyro_x,
gyro_y,
gyro_z
);

delay(2000);

}

void sendData(
float ax,
float ay,
float az,
float gx,
float gy,
float gz
){

if(
WiFi.status()==WL_CONNECTED
){

HTTPClient http;

http.begin(API);

http.addHeader(
"Content-Type",
"application/json"
);

StaticJsonDocument<256> doc;

doc["session_id"]=session_id;

doc["accel_x"]=ax;
doc["accel_y"]=ay;
doc["accel_z"]=az;

doc["gyro_x"]=gx;
doc["gyro_y"]=gy;
doc["gyro_z"]=gz;

String body;

serializeJson(
doc,
body
);

int code=
http.POST(body);

Serial.print(
"HTTP:"
);

Serial.println(
code
);

Serial.println(
http.getString()
);

http.end();

}

}