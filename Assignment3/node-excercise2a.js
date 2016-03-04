var http = require("http");
var len = 0;
var string = "";
var req = http.get(process.argv[2], function(res) {
	res.on('data', function(chunk) {
		len += chunk.length;
		string += chunk;
	});
	res.on('end', function(){
		process.stdout.write(len.toString() + "\n");
		process.stdout.write(string+ "\n");
	});
});
req.end();