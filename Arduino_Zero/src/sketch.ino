/*
* Modified Arduino Frequency Detection
* by Nicole Grimwood
*
* For more information please visit: 
* http://www.instructables.com/id/Arduino-Guitar-Tuner/
* 
* 
* Slightly edited version of:
* Arduino Frequency Detection
* created October 7, 2012
* by Amanda Ghassaei
*
* This code is in the public domain.
*/

//Setup Servo control
#include <Servo.h>
Servo servo;
int servo_outputs[6] = {3, 5, 6, 9, 10, 11};
//int servo_outputs[6] = {8, 9, 10, 11, 12, 13};
int i, j, k;
int delay_amount = 50;
int tuning;
int init_time;

int button_pin = 12;

boolean NEXT_STRING = false;

// Guitar Strings
//float tuned_strings[] = {82.41, 110.00, 146.83, 196.00, 246.94, 329.63};
float tuned_strings[] = {73.42, 98.00, 130.8, 174.6, 220.0, 293.7}; // Tuned 1 step down

int onString = 0; //E2:0, A2:1, D3:2, G3:3, B3:4, E4:5
//float freq_thresh = .02; // How in tune it should make the string //TURN THIS INTO A PERCENT OF FREQUENCY
float freq_thresh = .01; // How in tune it should make the string //TURN THIS INTO A PERCENT OF FREQUENCY
float freq_diff = 2; // How different concurrent frequencies have to be to be registered
float diff;


//clipping indicator variables
boolean clipping = 0;

//data storage variables
byte newData = 0;
byte prevData = 0;
unsigned int time = 0;//keeps time and sends vales to store in timer[] occasionally
int timer[10];//storage for timing of events
int slope[10];//storage for slope of events
unsigned int totalTimer;//used to calculate period
unsigned int period;//storage for period of wave
byte index = 0;//current storage index
float frequency;//storage for frequency calculations
float frequency_old;
float frequency_old_old;
int maxSlope = 0;//used to calculate max slope as trigger point
int newSlope;//storage for incoming slope data

//variables for decided whether you have a match
byte noMatch = 0;//counts how many non-matches you've received to reset variables if it's been too long
byte slopeTol = 3;//slope tolerance- adjust this if you need
int timerTol = 10;//timer tolerance- adjust this if you need

//variables for amp detection
unsigned int ampTimer = 0;
byte maxAmp = 0;
byte checkMaxAmp;
byte ampThreshold = 30;//raise if you have a very noisy signal

void setup(){
  
  Serial.begin(9600);
  
  pinMode(7,OUTPUT);//output pin
  pinMode(button_pin, INPUT_PULLUP);
  
  cli();//diable interrupts
  
  //set up continuous sampling of analog pin 0 at 38.5kHz
 
  //clear ADCSRA and ADCSRB registers
  ADCSRA = 0;
  ADCSRB = 0;
  
  ADMUX |= (1 << REFS0); //set reference voltage
  ADMUX |= (1 << ADLAR); //left align the ADC value- so we can read highest 8 bits from ADCH register only
  
  ADCSRA |= (1 << ADPS2) | (1 << ADPS0); //set ADC clock with 32 prescaler- 16mHz/32=500kHz
  ADCSRA |= (1 << ADATE); //enable auto trigger
  ADCSRA |= (1 << ADIE); //enable interrupts when measurement complete
  ADCSRA |= (1 << ADEN); //enable ADC
  ADCSRA |= (1 << ADSC); //start ADC measurements
  
  sei();//enable interrupts
}

ISR(ADC_vect) {//when new ADC value ready
  
  PORTB &= B11101111;//set pin 12 low
  prevData = newData;//store previous value
  newData = ADCH;//get value from A0
  if (prevData < 127 && newData >=127){//if increasing and crossing midpoint
    newSlope = newData - prevData;//calculate slope
    if (abs(newSlope-maxSlope)<slopeTol){//if slopes are ==
      //record new data and reset time
      slope[index] = newSlope;
      timer[index] = time;
      time = 0;
      if (index == 0){//new max slope just reset
        PORTB |= B00010000;//set pin 12 high
        noMatch = 0;
        index++;//increment index
      }
      else if (abs(timer[0]-timer[index])<timerTol && abs(slope[0]-newSlope)<slopeTol){//if timer duration and slopes match
        //sum timer values
        totalTimer = 0;
        for (byte i=0;i<index;i++){
          totalTimer+=timer[i];
        }
        period = totalTimer;//set period
        //reset new zero index values to compare with
        timer[0] = timer[index];
        slope[0] = slope[index];
        index = 1;//set index to 1
        PORTB |= B00010000;//set pin 12 high
        noMatch = 0;
      }
      else{//crossing midpoint but not match
        index++;//increment index
        if (index > 9){
          reset();
        }
      }
    }
    else if (newSlope>maxSlope){//if new slope is much larger than max slope
      maxSlope = newSlope;
      time = 0;//reset clock
      noMatch = 0;
      index = 0;//reset index
    }
    else{//slope not steep enough
      noMatch++;//increment no match counter
      if (noMatch>9){
        reset();
      }
    }
  }
    
  /*
  if (newData == 0 || newData == 1023){//if clipping
    clipping = 1;//currently clipping
    //Serial.println("clipping");
  }
  */
  
  time++;//increment timer at rate of 38.5kHz
  
  ampTimer++;//increment amplitude timer
  if (abs(127-ADCH)>maxAmp){
    maxAmp = abs(127-ADCH);
  }
  if (ampTimer==1000){
    ampTimer = 0;
    checkMaxAmp = maxAmp;
    maxAmp = 0;
  }
  
}

void reset(){//clean out some variables
  index = 0;//reset index
  noMatch = 0;//reset match couner
  maxSlope = 0;//reset slope
}


void checkClipping(){//manage clipping indication
  if (clipping){//if currently clipping
    clipping = 0;
    Serial.println("clipping");
  }
}


void loop(){
  
  checkClipping();
  
  if (checkMaxAmp>ampThreshold){
    frequency = 38462/float(period);//calculate frequency timer rate/period
    Serial.println(frequency);
    if (frequency < 350 && frequency > 40 && NEXT_STRING == false){
      diff = frequency - frequency_old;
      if ( -freq_diff < diff && diff < freq_diff ){
        //cli();
        Serial.print(frequency);
        Serial.print("  ");
        Serial.println(onString);
        turn_servo();
      }
      frequency_old = frequency;
      //sei();
    }
  }else{
    delay(1000);
    NEXT_STRING = false;
    digitalWrite(7,NEXT_STRING);
  }

  if ( digitalRead(button_pin) == LOW){ 
    for( i = 0; i < 6; i++){
      servo.attach(servo_outputs[i]);
      servo.write(80);
      delay(1500);
    }
  }
  
  //delay(100);
}

void turn_servo(){

  //Check to see if string is in tune
  if ( (tuned_strings[onString] - tuned_strings[onString]*freq_thresh) < frequency &&
        frequency < (tuned_strings[onString] + tuned_strings[onString]*freq_thresh) ){
    Serial.println("IN TUNE");
    servo.detach();
    onString++; 
    NEXT_STRING = true;
    digitalWrite(7, NEXT_STRING);
    return;
  }

  //Servos[onString].attach(servo_outputs[onString]);
  servo.attach(servo_outputs[onString]);

  if ( frequency > (tuned_strings[onString] + tuned_strings[onString]*freq_thresh) ){
    servo.write(80);
  }else{
    servo.write(100);
  }
/*
  delay_amount = abs(frequency - tuned_strings[onString])*200;
  
  delay(delay_amount < 500 ? delay_amount : 500);
*/
  if ( abs(frequency - tuned_strings[onString]) < 5){
    delay(200);
  }else{
    delay(500);
  }
  servo.detach();
  return;
}
