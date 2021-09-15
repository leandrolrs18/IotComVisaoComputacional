#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <PubSubClient.h>
#include <auth.h>

WiFiClient espClient;
PubSubClient client(espClient); //lib required for mqtt

int LED = 2;
void callback(char* topic, byte* payload, unsigned int length) {   //callback includes topic and payload ( from which (topic) the payload is comming)
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
  if ((char)payload[0] == 'O' && (char)payload[1] == 'N') //ON
  {
    digitalWrite(LED, HIGH);
    Serial.println("ON");
  }
  else if ((char)payload[0] == 'O' && (char)payload[1] == 'F' && (char)payload[2] == 'F') //OFF
  {
    digitalWrite(LED, LOW);
    Serial.println(" OFF");
  }
  Serial.println();
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect("clientId-dZHZ88maBh1")) {
      Serial.println("connected");
      client.subscribe("esp∕exercicio/led");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void connectmqtt()
{
  client.connect("clientId-dZHZ88maBh1");  // ESP will connect to mqtt broker with clientID
  {
    Serial.println("connected to MQTT");
    client.subscribe("esp∕exercicio/led"); //topic=Demo
    if (!client.connected())
    {
      reconnect();
    }
  }
}

void setup()
{
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  WiFi.begin(ssid, password);
  Serial.println("connected");
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  connectmqtt();
}

void loop()
{
  // put your main code here, to run repeatedly:
  if (!client.connected())
  {
    reconnect();
  }

  client.loop();
}
