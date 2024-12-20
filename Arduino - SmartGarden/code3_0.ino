// C++ code
//

#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>
#include <Base64.h>
#include <Arduino_MKRIoTCarrier.h>

//Server details MUUTA VASTAAMAAN TODELLISIA ARVOJA
String server = "1.1.1.1";
int port = 8080;
char* username = "USERNAME";
char* pass = "PASSWORD";

//Wifi details MUUTA TIEDOT
char* ssid = "SSID";
char* password = "PASSWORD";

//Alustetaan pinnit ja tarvittavat muuttujat
MKRIoTCarrier carrier;
int moisture = 0;
int lightAmount = 0;
int outputLight = 0;
const int valoPin = A0;
const int moistureSensorPin = A6;
unsigned long time;
unsigned long timeSince;
const unsigned long period = 30000;

//Tieto palvelimelta
String GLOBALMINUTES = "";

//Luodaan wifi olio
WiFiClient wifiClient;
//Luodaan http olio
HttpClient client(wifiClient, server.c_str(), port);

void setup()
{
  time = millis(); //Tallenna aika

  // pinMode (A2, INPUT); //PhotoDiode IN
  // pinMode (13, OUTPUT); //Photodiode output to LED
  // pinMode(A0, OUTPUT); //Moisture sensor OUT
  // pinMode(A1, INPUT); //Moisture sensor IN

  carrier.withCase();
  carrier.begin();

  Serial.begin(9600); 

//Yritetään muodostaa yhteys 
    Serial.print("Connecting to WiFi..");
  if (WiFi.begin(ssid, password) != WL_CONNECTED) {
    Serial.println("Failed to connect to Wi-Fi"); //Jos yhteyden muodostus epäonnistuu, tulostetaan viesti
    while (true);
  }
  Serial.println("Connected successfully to Wi-Fi");
  Serial.println(WiFi.localIP());
}
//Mitataan valo
void measureLight()
{
  lightAmount = analogRead(valoPin);
  lightAmount = map(lightAmount, 0, 800, 0, 10);
  delay(2); // Wait for 2 millisecond(s)
}
//Mitataan kosteus
void measureMoisture(){
  moisture = analogRead(moistureSensorPin);
  moisture = map(moisture, 1023, 0, 0, 100);
}

//Funktio, joka hoitaa yhteyden serverille
void networking()
{
    //Yritetään muodostaa yhteys palvelimeen
    if(wifiClient.connect(server.c_str(), port)) {
    Serial.println("Connected to server, sending POST request...");

    //Luodaan tunnukset ja kryptataan
    char auth[100];
    snprintf(auth, sizeof(auth), "%s:%s", username, pass);
    int authLength = strlen(auth);
    int encodedLength = Base64.encodedLength(authLength);
    char encodedAuth[encodedLength + 1];
    Base64.encode(encodedAuth, auth, authLength);
    

    //Luodaan json body jossa mitatut arvot
    StaticJsonDocument<512> jsonDoc;

    jsonDoc["moistlvl"] = moisture;
    jsonDoc["lightlvl"] = lightAmount;
    
    String jsonData;
    serializeJson(jsonDoc, jsonData);

    //Aloitetaan POST pyyntö
    client.beginRequest();
    client.post("/data");

    //Lähetetään headerit
    client.sendHeader("Authorization", String("Basic ") + encodedAuth);
    client.sendHeader("Content-Type", "application/json");
    client.sendHeader("Content-Length", jsonData.length());
    client.sendHeader("Connection", "close");
    client.endRequest();

    //Lähetetään mittaustulokset
    client.print(jsonData);

    //Tarkistetaan palvelimen vastaus
    if (client.responseStatusCode() == 201)
    {
        //Luetaan vastauksen mukana tullut tieto
        String responseBody = client.responseBody();
        StaticJsonDocument<512> responseDoc;

        DeserializationError error = deserializeJson(responseDoc, responseBody);
        if (!error) {
            //Tallennetaan vastuksena tullut aikatieto globaaliin muuttujaan että se on käytettävissä funktion ulkopuolella
            GLOBALMINUTES = responseDoc["initialMinutes"].as<String>();
            String waterResponse = responseDoc["watering"];  
            Serial.println("Server response for minutes: " + GLOBALMINUTES);
            Serial.println("Server response for watering: " + waterResponse);
        }
        else {
            Serial.println("Failed to parse JSON response");
            }     
    }
    else {
        Serial.println("Error: " + client.responseStatusCode());
    }
    //Suljetaan yhteys
    client.stop();
    Serial.println("POST request sent with JSON payload");
  
  } else {
    Serial.println("Connection to server failed");
  }

}

void loop()
{
  //Tallennetaan aika
  timeSince = millis();
  
  //Mitataan valo
  measureLight();
  //Mitataan kosteus
  measureMoisture();
  
  //Tarkistetaan että on aika lähettää tiedot serverille. PERIOD = 3000
  if (timeSince - time >= period){
    Serial.println("Contacting server...");
    networking();
    Serial.print("{lightlvl: ");
    Serial.print(lightAmount);
    Serial.print(", moisture: ");
    Serial.print(moisture);
    Serial.println(" }");
    time = timeSince;

  }

  
  delay(100); // Wait for 100 millisecond(s)
}