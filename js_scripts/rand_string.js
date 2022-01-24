var alhpabet = "~!+_)({}":?><@#$%^&*1234567890abcdefgh";
var randomString = "";
while (randomString.length < 6) {
  randomString += alhpabet[Math.floor(Math.random() * alhpabet.length)]; 
}
