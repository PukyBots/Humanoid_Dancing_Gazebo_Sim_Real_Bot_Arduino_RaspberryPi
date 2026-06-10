// --- PINS (TCE Robot Hardware) ---
const int DIR1 = 6;
const int PWM1 = 10;

const int DIR2 = 5;
const int PWM2 = 9;

const int L_ENC_A = 3;

// ---------------- SPEEDS ----------------
const int MOVE_SPEED = 90;
const int TURN_SPEED = 90;

// ----------------------------------------
volatile long left_ticks = 0;

void setup() {

  Serial.begin(9600);

  pinMode(DIR1, OUTPUT);
  pinMode(PWM1, OUTPUT);

  pinMode(DIR2, OUTPUT);
  pinMode(PWM2, OUTPUT);

  pinMode(L_ENC_A, INPUT_PULLUP);

  attachInterrupt(
    digitalPinToInterrupt(L_ENC_A),
    encoderISR,
    RISING
  );

  stopRobot();
}

void loop() {

  if (Serial.available() > 0) {

    char cmd = Serial.read();

    switch (cmd) {

      case 'f':
        moveForward();
        break;

      case 'b':
        moveBackward();
        break;

      case 'l':
        turnLeft();
        break;

      case 'r':
        turnRight();
        break;

      case 's':
        stopRobot();
        break;
    }

    // clear buffer
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}

// ========================================
// ENCODER ISR
// ========================================

void encoderISR() {
  left_ticks++;
}

// ========================================
// MOVEMENT FUNCTIONS
// ========================================

void moveForward() {

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, LOW);

  analogWrite(PWM1, MOVE_SPEED);
  analogWrite(PWM2, MOVE_SPEED);
}

void moveBackward() {

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, HIGH);

  analogWrite(PWM1, MOVE_SPEED);
  analogWrite(PWM2, MOVE_SPEED);
}

void turnLeft() {

  digitalWrite(DIR1, HIGH);
  digitalWrite(DIR2, LOW);

  analogWrite(PWM1, TURN_SPEED);
  analogWrite(PWM2, TURN_SPEED);
}

void turnRight() {

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, HIGH);

  analogWrite(PWM1, TURN_SPEED);
  analogWrite(PWM2, TURN_SPEED);
}

void stopRobot() {

  analogWrite(PWM1, 0);
  analogWrite(PWM2, 0);

  digitalWrite(DIR1, LOW);
  digitalWrite(DIR2, LOW);
}
