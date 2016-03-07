var http = require("http");
var url = require("url");
var server = http.createServer(function(req, res) {
	var requrl = url.parse(req.url, true);
	var jsonres = {};
	var date = new Date(requrl.query.iso);
	if (requrl.pathname === '/api/parsetime') {
		jsonres.hour = date.getHours();
		jsonres.minute = date.getMinutes();
		jsonres.second = date.getSeconds();

	} else if (requrl.pathname === '/api/unixtime') {
		jsonres.unixtime = date.getTime();
	}
	res.writeHead(200, {'Content-Type': 'application/json'});
	return res.end(JSON.stringify(jsonres));
	
});

server.listen(process.argv[2]);