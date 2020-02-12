const baseTime = 1000; // time base image is shown at start
const scoreTime = 2000; // time each score is shown
const minRestTime = 1000; // rest time between each score
const restNum = 5; // num of scores to rest after - should be 5
const numScores = 11; // num of hard and easy scores to show - should be 11
const baseImage = "/static/images/Black_Cross.png"; // base & rest image
const skip = true; // to skip through scores for testing

var scores = null;
var e = 0, h = 0, counter = 0, trialNum = 0;
var timer = null;
var easyScoreShowing = null;

/* Socket connection with Flask application */
var socket = io.connect('127.0.0.1:5000');
socket.on('connect', function(){
  socket.send('Connected to application!');

  // Turn on start button
  start_btn = document.getElementById("start_btn");
  start_btn.disabled = false;
  start_btn.innerText = "Start";
});

function createMarker(label){
  marker = String(trialNum + ";" + label + ";" + Date.now());
  return marker;
}

/* Rest until user presses spacebar */
function restPeriod(){
  document.getElementById("message").innerHTML = "Press the spacebar when you are ready to continue.";

  document.body.onkeyup = function(e){
    if(e.keyCode == 32)
      contMusicTask();
  }
  counter = 0;
  console.log("Rest some...");
  document.getElementById("skip_btn").style.display = "none";
  document.getElementById("main_image").src = baseImage;
}

function miniRest(){
  // Turn off skipping
  document.body.onkeyup = function(e){
    if(e.keyCode == 32)
      return;
  }

  console.log("Mini rest")
  document.getElementById("skip_btn").style.display = "none";
  document.getElementById("main_image").src = baseImage;
  timer = window.setTimeout(musicTask, minRestTime);
}

function easyScore(){
  easyScoreShowing = true;
  console.log("Easy score");
  main_image.src = scores.easy[e++];
  socket.emit('marker', createMarker('easystart'));
  counter++;

  timer = window.setTimeout(function(){
    socket.emit('marker', createMarker('easyend'));
  }, scoreTime);
}

function hardScore(){
  easyScoreShowing = false;
  console.log("Hard score");
  main_image.src = scores.hard[h++];
  socket.emit('marker', createMarker('hardstart'));
  counter++;

  timer = window.setTimeout(function(){
    socket.emit('marker', createMarker('hardend'));
  }, scoreTime);
}

function musicTask(){

  var main_image = document.getElementById("main_image");

  if(e == numScores && h == numScores){
    socket.emit('marker', 100 + ';experimentfinished;' + Date.now());
    socket.close();
    console.log("Finished with scores.")
    document.getElementById("message").innerHTML = "Part One Finished";
    return;
  }

  if(skip){
    document.body.onkeyup = function(e){
      if(e.keyCode == 32)
        skipScore();
    }
  }

  trialNum += 1;

  /* Pick score */
  if(e == numScores) // easy is done
    hardScore();
  else if(h == numScores) // hard is done
    easyScore();
  else // pick by random
    Math.round(Math.random()) == 0 ? easyScore() : hardScore();

  /* Pick rest */
  // TODO: use trialNum instead
  counter == restNum ? timer = window.setTimeout(restPeriod, scoreTime) : timer = window.setTimeout(miniRest, scoreTime);
}

function startMusicTask(scoresJSON){
  socket.emit('marker', '0;baselinestart;' + Date.now());
  scores = JSON.parse(scoresJSON);
  document.getElementById("start_btn").style.display = "none";
  setTimeout(function(){
    socket.emit('marker', '0;baselineend;' + Date.now());
  }, baseTime);
  timer = setTimeout(musicTask, baseTime);
}

function contMusicTask(){
  /* Turn off spacebar click */
  document.body.onkeyup = function(e){
    if(e.keyCode == 32)
      return;
  }

  document.getElementById("message").innerHTML = "";
  document.getElementById("cont_btn").style.display = "none";
  musicTask();
}

function skipScore(){
  console.log("Skipping score");

  // clear ALL timeoutes
  while(timer)
    window.clearTimeout(timer--);

  if(easyScoreShowing)
    socket.emit('marker', createMarker('easyend'));
  else
    socket.emit('marker', createMarker('hardend'));

  counter == restNum ? restPeriod() : miniRest();
}
