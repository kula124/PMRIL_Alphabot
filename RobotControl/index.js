require('dotenv-extended').load();
const five = require('johnny-five')

const initBoard = () => {
  const newBoard = new five.Board({
    port: process.env.CONNECTION
  })

  newBoard.on('ready', function () {
    const led = new five.Led(13)
    led.blink(500)
    require('./src/mainController')
  })
}

initBoard()
