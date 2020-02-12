var nextImage = null;
var timer = null;

function startTest(){
  document.getElementById("start_btn").style.display = "none";

  window.setTimeout(function(){
      nextImage = "./static/images/Scores/Easy/BohemianLullabyA.png";
  }, 2000);

  timer = window.setTimeout(function(){
    console.log("Changing image to " + nextImage);
    document.getElementById("main_image").src = nextImage;
  }, 5000);
}
