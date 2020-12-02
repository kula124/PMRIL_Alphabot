const five = require('johnny-five')
// two motors
const motorLeft = new five.Motor({
    pins: {
      pwm: process.env.MOTOR_L_PWM,
      dir: process.env.MOTOR_L_DIR,
      cdir: process.env.MOTOR_L_CDIR,
    }
  });

const motorRight = new five.Motor({
  pins: {
    pwm: process.env.MOTOR_R_PWM,
    dir: process.env.MOTOR_R_DIR,
    cdir: process.env.MOTOR_R_CDIR,
  }
});

const _defaultSpeed = process.env.DEFAULT_SPEED

let isInverted = false;

const straightForward = () => {
  console.log(_defaultSpeed)
  if (isInverted) {
    motorRight.reverse(_defaultSpeed)
    motorLeft.reverse(_defaultSpeed)
  } else {
    motorRight.forward(_defaultSpeed)
    motorLeft.forward(_defaultSpeed)
  }
}

const stop = () => motorLeft.stop() | motorRight.stop()

const steerLeft = diffAngle => {
  // mapping logics here
  const mappedValue = 10; // example only
  // TODO: actually implement mapping
  if (isInverted) {
    motorRight.reverse(_defaultSpeed + mappedValue)
    motorLeft.reverse(_defaultSpeed)
  } else {
    motorRight.forward(_defaultSpeed + mappedValue)
    motorLeft.forward(_defaultSpeed)
  }
}

const steerRight = diffAngle => {
  // mapping logics here
  const mappedValue = 10; // example only
  // TODO: actually implement mapping
  if (isInverted) {
    motorLeft.reverse(_defaultSpeed + mappedValue)
    motorRight.reverse(_defaultSpeed)
  } else {
    motorLeft.forward(_defaultSpeed + mappedValue)
    motorRight.forward(_defaultSpeed)
  }
}

const setInverted = value =>  isInverted = value

module.exports = {
  straightForward,
  steerRight,
  steerLeft,
  setInverted,
  stop
}