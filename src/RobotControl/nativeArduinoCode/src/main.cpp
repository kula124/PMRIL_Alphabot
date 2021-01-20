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

volatile double l_target_rpm = 0;
volatile double r_target_rpm = 0;

double lKp = 1.5, lKi = 2.0, lKd = 0, lInput, lOutput;
PID LmyPID(&lInput, &lOutput, &l_target_rpm, lKp, lKi, lKd, DIRECT);

double rKp = 1.5, rKi = 2.0, rKd = 0, rSetpoint, rInput, rOutput;
PID RmyPID(&rInput, &rOutput, &r_target_rpm, rKp, rKi, rKd, DIRECT);

double LGetRpm();
double RGetRpm();
bool LSetRpm(void *args);
bool RsetRpm(void *args);
bool LDIR, RDIR;

const double _base_speed = 150;
const double L = 0.15;

double abs_v(float f);

class Communicator
{
public:
  int didReadData()
  {
    return Serial.available();
  }
  void updateRpms()
  {
    float v, w;
    if (Serial.available() != 0 && Serial.available() % (2 * sizeof(float)) == 0)
    {
      Serial.readBytes((char *)&v, sizeof(float));
      Serial.readBytes((char *)&w, sizeof(float));

      double diff = w;
      /*Serial.println(diff);
      Serial.println(w);
      Serial.println("---------");*/
      // r_target_rpm = v;
      if (v == 0)
      {
        r_target_rpm = 0;
        l_target_rpm = 0;
        return;
      }
      r_target_rpm = _base_speed + diff;
      l_target_rpm = _base_speed - diff;
    };
  }
};

Communicator comms;

void setup()
{
  // put your setup code here, to run once:
  pinMode(L_D_PIN, OUTPUT);
  pinMode(L_CD_PIN, OUTPUT);
  pinMode(L_PWM_PIN, OUTPUT);

  pinMode(R_D_PIN, OUTPUT);
  pinMode(R_CD_PIN, OUTPUT);
  pinMode(R_PWM_PIN, OUTPUT);

  pinMode(L_ENC, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(L_ENC), l_interupt, FALLING);
  pinMode(L_ENC, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(R_ENC), r_interupt, FALLING);

  LmyPID.SetMode(AUTOMATIC);
  lInput = 0;
  timer.every(200, LSetRpm);

  RmyPID.SetMode(AUTOMATIC);
  rInput = 0;
  timer.every(200, RsetRpm);

  digitalWrite(L_D_PIN, LOW);
  digitalWrite(L_CD_PIN, HIGH);

  digitalWrite(R_D_PIN, HIGH);
  digitalWrite(R_CD_PIN, LOW);

  Serial.begin(57600);
  // Serial.begin(9600);
  Serial.setTimeout(100);
}

void loop()
{
  // Input = getRpm();
  timer.tick();
  // Serial.println(LGetRpm()); // Serial.print(',');
  comms.updateRpms();
  lInput = LGetRpm();
  rInput = RGetRpm();

  LmyPID.Compute();
  analogWrite(L_PWM_PIN, lOutput);

  // Serial.print(',');
  RmyPID.Compute();
  analogWrite(R_PWM_PIN, rOutput);
  /*Serial.println(lOutput);
  Serial.println(rOutput);
  Serial.println("-----");*/
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

double abs_v(float f)
{
  return f > 0 ? (double)f : (double)-f;
};