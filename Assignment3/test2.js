var http = require("http");
function handleRequest(request, response){
	console.log("request object received");
	response.writeHead(200, {"content-type": "text/plain"});
	response.write("Hello SYDE 322 Students!");
	response.end();
}

http.createServer(handleRequest).listen(8080);
console.log("Node.js server is running at localhost:8080");
