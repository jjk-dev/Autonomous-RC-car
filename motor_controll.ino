#include <SoftwareSerial.h>
#include <AFMotor.h>

# Define number and position of DC Motor
AF_DCMotor motor_L(3);              
AF_DCMotor motor_R(4);

int  i;

byte DataToRead[3];

# Initialize speed
void setup() {
  motor_L.setSpeed(200);
  motor_R.setSpeed(200);
  motor_L.run(RELEASE);
  motor_R.run(RELEASE);

  Serial.begin(9600);
}

# Get order from Raspberry Pi
void loop() {
  DataToRead[2] = '\n';
  Serial.readBytesUntil(char(13), DataToRead, 3);
  

  for (i = 0; i < 3; i++) {
    Serial.write(DataToRead[i]);
    if (DataToRead[i] == '\n') break;
  }

  switch (DataToRead[0]) {

    # Go forward
    case 'F':
      motor_L.run(FORWARD);
      motor_R.run(FORWARD);
      break;

    # Go left
    case 'L':
      motor_L.run(BACKWARD);
      motor_R.run(FORWARD);
      break;
      
      # Go right
    case 'R':
      motor_L.run(FORWARD);
      motor_R.run(BACKWARD);
      break;

    # Go backward
    case 'B':
      motor_L.run(BACKWARD);
      motor_R.run(BACKWARD);
      break;

    # Stop
    default:
      motor_L.run(RELEASE);
      motor_R.run(RELEASE);
      break;
  }

  # Initialize all
  motor_L.run(RELEASE);
  motor_R.run(RELEASE);
  Serial.write('\n');
  Serial.flush();
}

