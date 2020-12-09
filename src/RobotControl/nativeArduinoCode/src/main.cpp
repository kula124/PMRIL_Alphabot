#include <Arduino.h>
#include <PID_v1.h>
#include <arduino-timer.h>

#define L_ENC 2
#define R_ENC 3
#define LED_PIN 13

#define L_D_PIN A0
#define L_CD_PIN A1
#define L_PWM_PIN 5

auto timer = timer_create_default();
volatile int L_Counter = 0;
volatile int R_Counter = 0;
volatile float l_rpm = 0;

volatile int L_Counter_prev = 0;
volatile int L_Current_rpm = 0;

void l_interupt();
void r_interupt();

const int target_rpm = 170;

double Kp = 1.5, Ki = 2.5, Kd = 0, Setpoint, Input, Output;
PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

double getRpm();
bool setRpm(void *args);

void setup()
{
  // put your setup code here, to run once:
  pinMode(L_D_PIN, OUTPUT);
  pinMode(L_CD_PIN, OUTPUT);
  pinMode(L_PWM_PIN, OUTPUT);

  pinMode(L_ENC, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(L_ENC), l_interupt, FALLING);
  pinMode(L_ENC, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(R_ENC), r_interupt, FALLING);

  myPID.SetMode(AUTOMATIC);
  Input = 0;
  Setpoint = target_rpm;
  timer.every(200, setRpm);
  Serial.begin(115200);
}

void loop()
{
  // Input = getRpm();
  timer.tick();
  digitalWrite(L_D_PIN, LOW);
  digitalWrite(L_CD_PIN, HIGH);
  Input = getRpm();
  Serial.println(getRpm());
  // Serial.print(',');
  myPID.Compute();
  analogWrite(L_PWM_PIN, Output);
  // Serial.println(Output);
}

void l_interupt()
{
  L_Counter++;
}

void r_interupt()
{
  R_Counter++;
}

double getRpm()
{
  return L_Current_rpm;
}

bool setRpm(void *args)
{
  float diff = L_Counter - L_Counter_prev;
  L_Counter_prev = L_Counter;
  L_Current_rpm = (diff / 20) * 5 * 60;
  return true;
}