var fs = require("fs");

var buffer = fs.readFileSync(process.argv[2]);
var stringed = buffer.toString();
var newLineArray = stringed.split("\n");
var num = newLineArray.length-1;
process.stdout.write(num.toString());