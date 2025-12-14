#include <Servo.h>
Servo servoMotor;

const int trigPin = 9;
const int echoPin = 10;
const int servoPin = 6;

const int MIN_ANGLE = 0;
const int MAX_ANGLE = 180;
const int STEP_ANGLE = 2; // scan speed

const unsigned long ECHO_TIMEOUT_US = 30000; // aprox 5ms in aer
const float SPEED_OF_SOUND_CM_PER_US = 0.0343; // 343 m/s = 0.0343 cm/us

long readDistanceCM() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long duration = pulseIn(echoPin, HIGH, ECHO_TIMEOUT_US);

  if (duration == 0) {
    return -1; 
  }

  // dist = (t * v) / 2
  float cm = (duration * SPEED_OF_SOUND_CM_PER_US) / 2.0;
  return (long)(cm + 0.5); // rotunjire
}

int angle = MIN_ANGLE;
int dir = STEP_ANGLE;

void setup() {
  Serial.begin(115200);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  servoMotor.attach(servoPin);
  servoMotor.write(angle);
  delay(300);
}

void loop() {
  servoMotor.write(angle);
  delay(20);

  long dist = readDistanceCM();

  //"angle,distance" - csv format
  Serial.print(angle);
  Serial.print(",");
  Serial.println(dist);

  angle += dir;
  if (angle >= MAX_ANGLE) {
    angle = MAX_ANGLE;
    dir = -STEP_ANGLE;
  } else if (angle <= MIN_ANGLE) {
    angle = MIN_ANGLE;
    dir = STEP_ANGLE;
  }

  delay(25);
}
