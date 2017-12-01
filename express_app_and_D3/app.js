var express  = require('express');
var bodyParser = require('body-parser');
var path = require('path');
var delay = require('express-delay');
var pause = require('connect-pause');


var app = express();

var logger = function(req, res, next){
	console.log('logging...');
	next();
}

app.use(logger);

app.use(bodyParser.json());

app.use(bodyParser.urlencoded({ extended: false }))


//set Static path
app.use(express.static(path.join(__dirname, 'public')))

var pythonExecutable = "C:/Users/Rajat/AppData/Local/Enthought/Canopy/edm/envs/User/python.exe"

// Route handlers (middleware functions need to be before it)
app.get('/', function(req, res){
	
});


app.post('/submit', function(req, res){
	arg1 = req.body.word_input;
	const spawn = require("child_process").spawn;
	var process = spawn(pythonExecutable, ["script.py", arg1]);

	process.stdout.on('data', function (data){
	// Do something with the data returned from python script

	});
	// res.json(returned_json);
	// var arr = JSON.parse(returned_json);
	// res.json(arr);
	setTimeout((function() {res.sendFile(path.join(__dirname, 'public/submit.html'))}), 15000);
	// res.sendFile(path.join(__dirname, 'public/submit.html'));

})


app.listen(3000, function(){
	console.log("listening on 3000");
})

