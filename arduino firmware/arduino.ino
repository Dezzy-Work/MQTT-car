#include <AFMotor.h>
#include <Servo.h>

AF_DCMotor my_motor1(1); // motor drive initialization
AF_DCMotor my_motor2(2); // motor drive initialization

Servo servo; // motor servo initialization

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(5);

  servo.attach(10);
  servo.write(90);
  
  my_motor1.setSpeed(200); // set the speed of the motors
  my_motor2.setSpeed(200); // set the speed of the motors

  my_motor1.run(RELEASE); //stop
  my_motor2.run(RELEASE); //stop 2 
}

void loop() {
  if (Serial.available()) {

    String result = Serial.readString(); // getting from serial port

    if (result.toInt() == 1){ // go FORWARD
      my_motor1.run(FORWARD);
      my_motor2.run(FORWARD);
    }
    else if (result.toInt() == 5) { // go BACKWARD
      my_motor1.run(BACKWARD);
      my_motor2.run(BACKWARD);
    }
    else if (result.toInt() == 4) { // stop
      my_motor2.run(RELEASE);
      servo.write(90);
    }
    else if (result.toInt() >= 60 and result.toInt() <= 120){ // data for servo
      servo.write(result.toInt()); // the servo sets the position according to the received data
    }
      
  }
} 
