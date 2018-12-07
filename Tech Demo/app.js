var express = require('express');
var app = express();
var serv = require('http').Server(app);

app.get('/', function(req, res){
    res.sendFile(__dirname + '/client/index.html');
});
app.use('/client', express.static(__dirname + '/client'));

var port = 8080;
serv.listen(port);
console.log("Server is running on port: " + port);

var io = require('socket.io')(serv, {});
io.sockets.on('connection', function(socket){
    console.log("New Connection");

    socket.on('happy', function(data){
        console.log(data.reason);
    });
});
