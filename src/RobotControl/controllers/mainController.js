const motorController = require('./motorController')

const delay = duration => new Promise((resolve, reject) => {
    setTimeout(resolve, duration)
})

const testFunction = async () => {
    motorController.straightForward()
    await delay(1000);
    motorController.stop()
    await delay(1000)
    motorController.setInverted(true)
    motorController.straightForward()
    await delay(1000)
    motorController.stop()
}

module.exports = testFunction
