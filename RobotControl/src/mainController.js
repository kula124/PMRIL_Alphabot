const motorController = require('./motorController')

const delay = duration => new Promise((resolve, reject) => {
    setTimeout(resolve, duration)
})

const testFunction = async () => {
    motorController.straightForward(200)
    await delay(2000);
    motorController.stop()
    motorController.setInverted(true)
    motorController.straightForward(200)
    await delay(2000)
    motorController.stop()
}

module.exports = testFunction
