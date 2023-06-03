
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
    
  console.log("loading..");
  clearTimeout(typingTimer);
});

//user is "finished typing," do something
function doneTyping() {
    var currentURL = window.location.href;  // Get the current page URL
    var searchURL = currentURL + '/searchUserName/';  // Construct the search URL
    $.ajax({
        type: "GET",
        url: searchURL,
        data: {
            userName: $('#search').val(),
        },
        success: function (data) {
            console.log(data);
        }
    });
}
