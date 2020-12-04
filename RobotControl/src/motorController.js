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
const _leftCalibration = process.env.CALIBRATION_LEFT
const _rightCalibration = process.env.CALIBRATION_RIGHT

const leftDefaultSpeed = parseInt(_defaultSpeed) + parseInt(_leftCalibration)
const rightDefaultSpeed = parseInt(_defaultSpeed) + parseInt(_rightCalibration)

let isInverted = false;

const straightForward = () => {
  console.log(leftDefaultSpeed, rightDefaultSpeed)
  if (isInverted) {
    motorRight.reverse(rightDefaultSpeed)
    motorLeft.reverse(leftDefaultSpeed)
  } else {
    motorRight.forward(rightDefaultSpeed)
    motorLeft.forward(leftDefaultSpeed)
  }
}

const stop = () => motorLeft.stop() | motorRight.stop()

const steerLeft = diffAngle => {
  // mapping logics here
  const mappedValue = 10; // example only
  // TODO: actually implement mapping
  if (isInverted) {
    motorRight.reverse(rightDefaultSpeed + mappedValue)
    motorLeft.reverse(leftDefaultSpeed)
  } else {
    motorRight.forward(rightDefaultSpeed + mappedValue)
    motorLeft.forward(leftDefaultSpeed)
  }
}

const steerRight = diffAngle => {
  // mapping logics here
  const mappedValue = 10; // example only
  // TODO: actually implement mapping
  if (isInverted) {
    motorLeft.reverse(leftDefaultSpeed + mappedValue)
    motorRight.reverse(rightDefaultSpeed)
  } else {
    motorLeft.forward(leftDefaultSpeed + mappedValue)
    motorRight.forward(rightDefaultSpeed)
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