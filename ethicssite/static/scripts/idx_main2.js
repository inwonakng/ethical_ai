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

	// $(".qeustion_cards").mouseover(function(){
  //   $(this).animate({height:'300px'}, 100);
  // });
  // $(".qeustion_cards").mouseout(function(){
  //   $(this).animate({height:'200px'}, 100);
  // });

})