
//setup before functions
var typingTimer;                //timer identifier
var doneTypingInterval = 1000;  //time in ms, 5 seconds for example
var $input = $('#search');

//on keyup, start the countdown
$input.on('keyup', function () {
  clearTimeout(typingTimer);
  handleText();
  typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

document.getElementById("search").addEventListener("search", function(event) {
  handleText();
});

function handleText(){
  if ($('#search').val() != "") {
    $('.search-results').css('display', 'flex');
    $('.search-results').empty();
    $('.search-results').html("Loading...")
  }
  else {

    $('.search-results').css('display', 'none');
    $('.search-results').empty();
  }
}

//on keydown, clear the countdown 
$input.on('keydown', function () {
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
    error: function (response) {
      $('.search-results').empty();
      $('.search-results').html('<p class="text-center my-2">There is some issue while processing your request.</p>');
    },
    success: function (data) {
      if (data == "LessChar") {
        $('.search-results').empty();
        $('.search-results').html('<p class="text-center my-2">Enter atleast 4 characters</p>');
      }
      else if (data == "NoUserFound") {
        $('.search-results').html('Sorry, no user found :(');
      }
      else {
        $('.search-results').empty();
        console.log(data);
        data.map((user, index) => {
          $('.search-results').append
            (`
            <div id="result-${index}" class="results rounded" onclick="location.href='/' + '${user.user_name}' + '/'">

              <div class="d-flex flex-row align-items-center mx-2">
                <div class="p-1 rounded-circle border-1 border border-secondary">
                  <img class="rounded-circle " width="32" height="32px" src="${user.user_pic != "False" ?  user.user_pic : '/static/avatar.png'}" alt="avatar"
                    style="object-fit: cover;" />
                </div>
                <div class="d-flex flex-column my-1 mb-2">
                  <p  class="medium  fw-bold mx-3 mb-1" style="color:#2d8291">${user.user_name}</p>
                  <small class="mx-3 ">${user.name}</small>
                </div>
              </div>
            </div>
            
            ${index != data.length - 1 ? '<hr class="bg-secondary">' : ''}
          `)
        });
      }
    }
  });
}
