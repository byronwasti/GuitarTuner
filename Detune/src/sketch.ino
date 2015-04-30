#include <Servo.h>
Servo servo;
int servo_outputs[6] = {3, 5, 6, 9, 10, 11};
int i, j, k, on_string = 0;
uint8_t done = 0;

void setup()
{
}

void loop()
{
  if( !done ){
    servo.attach(servo_outputs[on_string]);
    servo.write( on_string%2 == 0 ? 100 : 80);
    delay(500);
    servo.detach();
    on_string++;
    if (on_string > 5) done = 1;
  }
}
