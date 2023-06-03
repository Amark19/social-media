
//setup before functions
var typingTimer;                //timer identifier
var doneTypingInterval = 3000;  //time in ms, 5 seconds for example
var $input = $('#search');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(typingTimer);
  typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown 
$input.on('keydown', function () {
  clearTimeout(typingTimer);
});

//user is "finished typing," do something
function doneTyping () {
  //do something
  console.log("loading..");
  make_req("GET", `searchUserName/`, {
    userName: $input.val(),
  }, (result) => {
    console.log("done");
    console.log(result);
  });
}