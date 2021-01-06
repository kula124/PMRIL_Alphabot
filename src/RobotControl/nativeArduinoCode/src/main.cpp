#include <Arduino.h>
#include <PID_v1.h>
#include <arduino-timer.h>

#define L_ENC 2
#define R_ENC 3
#define LED_PIN 13
// LEFT
#define L_D_PIN A0
#define L_CD_PIN A1
#define L_PWM_PIN 5
// RIGHT
#define R_D_PIN A2
#define R_CD_PIN A3
#define R_PWM_PIN 6

auto timer = timer_create_default();
volatile int L_Counter = 0;
volatile int R_Counter = 0;
volatile float l_rpm = 0;

volatile int L_Counter_prev = 0;
volatile int L_Current_rpm = 0;
volatile int R_Counter_prev = 0;
volatile int R_Current_rpm = 0;

void l_interupt();
void r_interupt();

const int _target_rpm = 200;

double lKp = 1.5, lKi = 2.5, lKd = 0, lSetpoint, lInput, lOutput;
PID LmyPID(&lInput, &lOutput, &lSetpoint, lKp, lKi, lKd, DIRECT);

double rKp = 1.5, rKi = 2.5, rKd = 0, rSetpoint, rInput, rOutput;
PID RmyPID(&rInput, &rOutput, &rSetpoint, rKp, rKi, rKd, DIRECT);

double LGetRpm();
double RGetRpm();
bool LSetRpm(void *args);
bool RsetRpm(void *args);

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

  LmyPID.SetMode(AUTOMATIC);
  lInput = 0;
  lSetpoint = _target_rpm;
  timer.every(200, LSetRpm);

  RmyPID.SetMode(AUTOMATIC);
  rInput = 0;
  rSetpoint = _target_rpm;
  timer.every(200, RsetRpm);

  digitalWrite(L_D_PIN, LOW);
  digitalWrite(L_CD_PIN, HIGH);

  digitalWrite(R_D_PIN, HIGH);
  digitalWrite(R_CD_PIN, LOW);

  Serial.begin(9600);
}

void loop()
{
  // Input = getRpm();
  timer.tick();
  lInput = LGetRpm();
  Serial.println(LGetRpm()); // Serial.print(',');
  LmyPID.Compute();
  analogWrite(L_PWM_PIN, lOutput);
  // Serial.println(Output);

  rInput = RGetRpm();
  // Serial.print(',');
  RmyPID.Compute();
  analogWrite(R_PWM_PIN, rOutput);
}

void l_interupt()
{
  L_Counter++;
}

void r_interupt()
{
  R_Counter++;
}

double LGetRpm()
{
  return L_Current_rpm;
}

double RGetRpm()
{
  return R_Current_rpm;
}

bool LSetRpm(void *args)
{
  float diff = L_Counter - L_Counter_prev;
  L_Counter_prev = L_Counter;
  L_Current_rpm = (diff / 20) * 5 * 60;
  return true;
}

bool RsetRpm(void *args)
{
  float diff = R_Counter - R_Counter_prev;
  R_Counter_prev = R_Counter;
  R_Current_rpm = (diff / 20) * 5 * 60;
  return true;
}