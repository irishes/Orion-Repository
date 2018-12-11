var express = require('express');
var app = express();
var path = require("path");
var fs = require("fs");
var serv = require('http').Server(app);
const spawn = require("child_process").spawn;

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

    socket.on('add', function(data){
        console.log(data.number1);
        console.log(data.number2);
        var answer = data.number1 + data.number2;
        console.log(answer);
       /* 
        const pythonProcess = spawn('python', ['is.py', data.number1, data.number2]);
        pythonProcess.stdout.on('data', (data) => {
            console.log("hello");
        });
        */
        socket.emit('serverMsg', {
            msg: answer
        });
    });
});

const multer = require("multer");

const handleError = (err, res) => {
      res
        .status(500)
        .contentType("text/plain")
        .end("Oops! Something went wrong!");
};

const upload = multer({
    dest: "Capstone_Repo/uploads"
});
