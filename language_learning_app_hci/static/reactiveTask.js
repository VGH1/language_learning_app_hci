var trialNum = 0;
var scores = null;
var i = 0;

/* Socket connection with Flask application */
var socket = io.connect('127.0.0.1:5000');
socket.on('connect', function(){
  socket.send('Connected to application!');

  /* Turn on start button */
  start_btn = document.getElementById("start_btn");
  start_btn.disabled = false;
  start_btn.innerText = "Start";
});

function createMarker(label1, label2, label3){
  return String(label1 + ";" + label2 + ";" + label3);
}

function createLevelMarker(lvl, label){
  return createMarker(String(1000 + lvl), String("level" + lvl + label), String(Date.now()));
}

function showScore(i) {
  if (i > 0)
    socket.emit("marker", createLevelMarker(i-1, "end"));

  main_image = document.getElementById('main_image');

  if(i >= scores.length){
    console.log('Finished!');
    // TODO: Let Flask know tests are finished
    socket.emit("reactiveTaskDone");
    socket.close();
    main_image.src = "";
    document.getElementById('message').innerHTML = "Test completed.";
    return null;
  }
  socket.emit("marker", createLevelMarker(i, "start"));
  main_image.src = scores[i];
}

// Used to pass scores over and set up test
function startReactiveTask(scoresArr){
  scores = scoresArr

  socket.emit("reactiveTaskStart")
  start_btn = document.getElementById('start_btn');
  start_btn.style.display = "none";

  // socket.emit("marker", createLevelMarker(i, "start"));
  showScore(i);
}

// Show next score
function levelUp(){
  console.log('Increasing difficulty');
  showScore(++i);
}

// Event triggered from Flask to increase difficulty
socket.on('levelUp', function(){levelUp()});
