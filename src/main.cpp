/**
 * Project: Array of LDRs
 * Board: Arduino Nano
 * IC: 74HC4052N, 74HC595
 * 
 * Copyright 2020 Tauno Erik
 * 
 * https://microcontrollerslab.com/cd4052-mux-demux-pinout-examples-applications-datasheet/
 * http://tok.hakynda.com/article/detail/146/cd4053be-cmos-analog-multiplexersdemultiplexers-with-logic-level-conversion-analog-input
 * https://learn.sparkfun.com/tutorials/multiplexer-breakout-hookup-guide/
 * 
 */
#include <Arduino.h>

/* Enable debug info Serial print */
#define DEBUG
#ifdef DEBUG
  #define DEBUG_PRINT(x)  Serial.print(x)
  #define DEBUG_PRINTLN(x)  Serial.println(x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif

/* Define Pins */
const int INPUT_Y_PIN = A0;  // 74HC4052N
const int INPUT_X_PIN = A1;  // 74HC4052N
const int SELECT_A_PIN = 4;  // 74HC4052N
const int SELECT_B_PIN = 2;  // 74HC4052N

const int DATA_PIN = 11;     // 74HC595
const int LATCH_PIN = 8;     // 74HC595
const int CLOCK_PIN = 12;    // 74HC595

const int LED_PIN = 3;

/* Config */
const int WRITE_A[8] = {1, 0, 0, 1, 1, 0, 1, 0};
const int WRITE_B[8] = {0, 1, 0, 1, 1, 1, 0, 0};
const int READ_PINS[8] = {
  INPUT_X_PIN, INPUT_X_PIN, INPUT_X_PIN, INPUT_X_PIN,
  INPUT_Y_PIN, INPUT_Y_PIN, INPUT_Y_PIN, INPUT_Y_PIN
};

const int COLUMNS = 6;
const int ITEMS_IN_COLUMN = 8;

const int INTERVAL = 1000;

// https://www.tutorialspoint.com/cplusplus/cpp_return_arrays_from_functions.htm

int * get_data() {
  static int data[COLUMNS * ITEMS_IN_COLUMN];  // 8*6
  int step = 0;

  // Select column
  for (int i = 0; i < COLUMNS; i++) {
    int column = 0b00000010 << i;
    digitalWrite(LATCH_PIN, LOW);
    shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, column);
    digitalWrite(LATCH_PIN, HIGH);

    // Read a column
    for (int j = 0; j < ITEMS_IN_COLUMN; j++) {
      digitalWrite(SELECT_B_PIN, WRITE_B[j]);
      digitalWrite(SELECT_A_PIN, WRITE_A[j]);
      int value = analogRead(READ_PINS[j]);
      data[step] = value;
      step++;
    }
  }
  return data;
}


void setup() {
  Serial.begin(115200);

  pinMode(SELECT_A_PIN, OUTPUT);
  pinMode(SELECT_B_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    int in_byte = Serial.read();
    DEBUG_PRINT("I received: ");
    DEBUG_PRINTLN(in_byte);  // , DEC

    if (in_byte == 97) {  // 97 == a
      digitalWrite(LED_PIN, HIGH);
      int *table;  // a pointer to an int array
      table = get_data();
      digitalWrite(LED_PIN, LOW);

      for (int i = 0; i < COLUMNS * ITEMS_IN_COLUMN; i++) {
        Serial.print(" ");
        Serial.print(table[i]);
      }
      Serial.println();
    }
  }
}
