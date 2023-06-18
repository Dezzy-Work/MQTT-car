#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char *ssid =  "";  // WiFi name
const char *pass =  ""; // WiFi space

const char *mqtt_server = ""; // MQTT broker
const int mqtt_port = 99999; // MQTT port
const char *mqtt_user = ""; // MQTT login
const char *mqtt_pass = ""; // MQTT password

#define BUFFER_SIZE 100

bool LedState = false;
int tm=300;
int temp=0;

void callback(const MQTT::Publish& pub) // receiving from the MQTT
{
  String payload = pub.payload_string();

  // checking data from topic

  if(String(pub.topic()) == "robot/forward")
  {
    if (payload == "1"){
      Serial.println("1");
    }
          
  }
  if(String(pub.topic()) == "robot/stop")
  {
    if (payload == "1");{
      Serial.println("4");
    }
  }
  if(String(pub.topic()) == "robot/backward")
  {
    if (payload == "1");{
      Serial.println("5");
    }
  }
  if(String(pub.topic()) == "robot/rotate")
  {
    Serial.println(payload.toFloat());
  }
}



WiFiClient wclient;      
PubSubClient client(wclient, mqtt_server, mqtt_port); // Connecting to MQTT broker

void setup() {
  Serial.begin(115200);

  Serial.println();
}

void loop() {
  // connecting to wi-fi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.print("Connecting to ");
    Serial.print(ssid);
    Serial.println("...");
    WiFi.begin(ssid, pass);
    
    if (WiFi.waitForConnectResult() != WL_CONNECTED)
        return;

    Serial.println("WiFi connected");
  }
  
  // connect to MQTT server
  if (WiFi.status() == WL_CONNECTED) {
    if (!client.connected()) {
      Serial.println("Connecting to MQTT server");

      if (client.connect(MQTT::Connect("arduinoClient2").set_auth(mqtt_user, mqtt_pass))) {
        Serial.println("Connected to MQTT server");
        client.set_callback(callback);

        // subscription to the topic
        client.subscribe("robot/forward");
        client.subscribe("robot/stop");
        client.subscribe("robot/rotate");
        client.subscribe("robot/backward");      
      }
      else {
        Serial.println("Could not connect to MQTT server");   
      }

    }
      
    if (client.connected()){
        client.loop();
    }
  }
}
