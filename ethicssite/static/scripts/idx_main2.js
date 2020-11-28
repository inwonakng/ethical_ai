var getCookie = function (name) {
	var value = "; " + document.cookie;
	var parts = value.split("; " + name + "=");
	if (parts.length == 2) return parts.pop().split(";").shift();
};

function WriteCookie() {
   document.cookie= "consent=Shown";
}

$(document).ready(() => {
  console.log(document.cookie);

  // $(".consent").show();
  // $(".consent_background").show();
  if (typeof getCookie('consent') == 'undefined') {
    $(".consent").show();
    $(".consent_background").show();
  }

  $('.consent_input').on('click', event => {
    $(".consent").hide();
    $(".consent_background").hide();
  });

	$('.question_nav .filter').on('click', event => {
    $('.question_nav .filter_options').toggle("10")
		
  });

})
