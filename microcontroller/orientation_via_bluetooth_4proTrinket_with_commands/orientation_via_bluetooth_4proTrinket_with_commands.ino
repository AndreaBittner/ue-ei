#include <Arduino.h>
#include <SPI.h>
//#if not defined (_VARIANT_ARDUINO_DUE_X_) && not defined (_VARIANT_ARDUINO_ZERO_)
//  #include <SoftwareSerial.h>
//#endif

/* SENSORS */
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM303_U.h>
#include <Adafruit_L3GD20_U.h>
#include <Adafruit_9DOF.h>
/* Assign a unique ID to the sensors */
Adafruit_9DOF                dof   = Adafruit_9DOF();
Adafruit_LSM303_Accel_Unified accel = Adafruit_LSM303_Accel_Unified(30301);
Adafruit_LSM303_Mag_Unified   mag   = Adafruit_LSM303_Mag_Unified(30302);
/* Update this with the correct SLP for accurate altitude measurements */
float seaLevelPressure = SENSORS_PRESSURE_SEALEVELHPA;

/* BLUETOOTH */
#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_SPI.h"
#include "Adafruit_BluefruitLE_UART.h"
#include "BluefruitConfig.h"

/*=========================================================================
    APPLICATION SETTINGS:
   - FACTORYRESET_ENABLE       Perform a factory reset when running this sketch
   - MINIMUM_FIRMWARE_VERSION  Minimum firmware version to have some new features
   - MODE_LED_BEHAVIOUR        LED activity, valid options are
                              "DISABLE" or "MODE" or "BLEUART" or
                              "HWUART"  or "SPI"  or "MANUAL"
    -----------------------------------------------------------------------*/
    #define FACTORYRESET_ENABLE         1
    #define MINIMUM_FIRMWARE_VERSION    "0.6.6"
    #define MODE_LED_BEHAVIOUR          "MODE"
/*=========================================================================*/

/*
SoftwareSerial bluefruitSS = SoftwareSerial(BLUEFRUIT_SWUART_TXD_PIN, BLUEFRUIT_SWUART_RXD_PIN);

Adafruit_BluefruitLE_UART ble(bluefruitSS, BLUEFRUIT_UART_MODE_PIN,
                      BLUEFRUIT_UART_CTS_PIN, BLUEFRUIT_UART_RTS_PIN);
*/

/* ...or hardware serial, which does not need the RTS/CTS pins. Uncomment this line */
// Adafruit_BluefruitLE_UART ble(Serial1, BLUEFRUIT_UART_MODE_PIN);

/* ...hardware SPI, using SCK/MOSI/MISO hardware SPI pins and then user selected CS/IRQ/RST */
/* PRO TRINKET */
// Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

/* ...software SPI, using SCK/MOSI/MISO user-defined SPI pins and then user selected CS/IRQ/RST */
/* UNO */
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_SCK, BLUEFRUIT_SPI_MISO,
                             BLUEFRUIT_SPI_MOSI, BLUEFRUIT_SPI_CS,
                             BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST); 

// A small helper
void error(const __FlashStringHelper*err) {
 // Serial.println(err);
  while (1);
}

// Counter
int loopnr =0;
bool sending = false;

/**************************************************************************/
/* Initialises all the sensors */
/**************************************************************************/
void initSensors()
{
  if(!accel.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
 //   Serial.println(F("Ooops, no LSM303 detected ... Check your wiring!"));
    while(1);
  }  
  if(!mag.begin())
  {
    /* There was a problem detecting the LSM303 ... check your connections */
//    Serial.println("Ooops, no LSM303 detected ... Check your wiring!");
    while(1);
  }
}

/**************************************************************************/
/* Sets up the HW an the BLE module */
/**************************************************************************/
void setup(void)
{
//  while (!Serial);  // required for Flora & Micro
//  delay(500);
  Serial.begin(115200);

  /* Initialise the module */
 // Serial.print(F("Initialising the Bluefruit LE module: "));
  if ( !ble.begin(VERBOSE_MODE) )
  {
    error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
  }
 // Serial.println( F("OK!") );

  if ( FACTORYRESET_ENABLE )
  {
    /* Perform a factory reset to make sure everything is in a known state */
//    Serial.println(F("Performing a factory reset: "));
    if ( ! ble.factoryReset() ){
      error(F("Couldn't factory reset"));
    }
  }
  /* Disable command echo from Bluefruit */
  ble.echo(false);

//  Serial.println("Requesting Bluefruit info:");
  ble.info();
//  Serial.println(F("Use Adafruit Bluefruit LE app to connect in UART mode"));
//  Serial.println();

  ble.verbose(false);  // debug info 

  /* Wait for connection */
  while (! ble.isConnected()) {
      delay(500);
  }

  // LED Activity command is only supported from 0.6.6
  if ( ble.isVersionAtLeast(MINIMUM_FIRMWARE_VERSION) )
  {
    // Change Mode LED Activity
 //   Serial.println(F("******************************"));
 //   Serial.println(F("Change LED activity to " MODE_LED_BEHAVIOUR));
    ble.sendCommandCheckOK("AT+HWModeLED=" MODE_LED_BEHAVIOUR);
 //   Serial.println(F("******************************"));
  }

//  Serial.println(F("Adafruit 9 DOF Pitch/Roll/Heading ")); Serial.println("");
  initSensors();
}

/**************************************************************************/
/* Constantly poll for new command or response data */
/**************************************************************************/
void loop(void)
{
  if(ble.isConnected()){
    
    // Check incomming Commands
    ble.println("AT+BLEUARTRX");
    if (ble.readline()) {
      /*private static class  microCommand {
            public static int START    = 1;
            public static int STOP     = 2;
            public static int RESET    = 3;
        }*/
     // Serial.println(ble.buffer);
    
      if ( strcmp(ble.buffer, "1") == 0) { 
          //START
          sending = true;
          ble.print("ble: start");
        } else if ( strcmp(ble.buffer, "2") == 0) {
          //STOP
          sending = false;
        } else if ( strcmp(ble.buffer, "3") == 0) {
          //RESET
          sending = false;
          loopnr = 0;
          ble.factoryReset();
          ble.echo(false);
          while (! ble.isConnected()) {
            delay(500);
          }
       }
    }
 
  delay(60);
  if (sending) 
  {
    sensors_event_t accel_event;
    sensors_event_t mag_event;
    sensors_vec_t   orientation;
  
    /* Calculate pitch and roll from the raw accelerometer data */
    accel.getEvent(&accel_event);
    if (dof.accelGetOrientation(&accel_event, &orientation))
    {
    Serial.println(loopnr);
       
     /* OUTPUT FORMAT BLE {[loopnr, time, roll, pitch, yaw, (accel) x, y z],..}  */
      ble.print("AT+BLEUARTTX=");
      ble.print("{");
      ble.print(loopnr);
      ble.print(",");
      ble.print(millis());
      ble.print(",");
      ble.print(orientation.roll);
      ble.print(",");
      ble.print(orientation.pitch);
      ble.print(",");
      
      /* Calculate the heading using the magnetometer */
      mag.getEvent(&mag_event);
      if (dof.magGetOrientation(SENSOR_AXIS_Z, &mag_event, &orientation)){
          ble.print(orientation.heading);
          ble.print(",");  
      }
        
      ble.print(accel_event.acceleration.x);
      ble.print(",");
      ble.print(accel_event.acceleration.y);
      ble.print(",");
      ble.print(accel_event.acceleration.z);
      ble.println("},");
     loopnr++;
    }
      
    ble.waitForOK();
    
 } else {
    delay(1000);
   }
 }
}
