function stringGenerator(length) {
    let result           = '';
    const characters       = '~!+_)({}:?><@#$%^&*1234567890abcdefgh';
    const charactersLength = characters.length;
    
    for (var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
   
   return result;
}

const divContainer = document.querySelector('#time');


function run(stringLength, iterationTimeMs, colorText) {
  setInterval(() => {
    divContainer.innerHTML = stringGenerator(stringLength)
    
    if (colorText) {
        divContainer.style.color = colorText;
    }
    
  }, iterationTimeMs)
}

run(10, 1000, 'green');