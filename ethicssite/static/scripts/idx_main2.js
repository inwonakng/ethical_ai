var getCookie = function (name) {
	var value = "; " + document.cookie;
	var parts = value.split("; " + name + "=");
	if (parts.length == 2) return parts.pop().split(";").shift();
};

function WriteCookie() {
   document.cookie= "consent=Shown";
}

$(document).ready(() => {
	$('.question_nav .filter').on('click', event => {
    $('.question_nav .filter_options').toggle("10")
		
  });

})
