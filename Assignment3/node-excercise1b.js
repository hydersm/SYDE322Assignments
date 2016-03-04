var fs = require("fs");

fs.readFile(process.argv[2], function(err, data) {
	if (err) throw err;
	var stringed = data.toString();
	var newLineArray = stringed.split("\n");
	var num = newLineArray.length-1;
	process.stdout.write(num.toString());
});
