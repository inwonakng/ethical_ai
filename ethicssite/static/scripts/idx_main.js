// $(document).ready(() => {
//
//   $('#generate_rules').on('click', event => {
//     $("#container2").hide();
//     $("#container1").show();
//     $(".custom_rules_card").hide();
//     $(".add_rules_card").show();
//
//     $("#bad_text").show();
//     $("#container4").hide();
//     $("#container3").show();
//     $(".bad_cob2").hide();
//     $(".bad_cob1").show();
//   });
//
// })

if (localStorage.getItem('cookieSeen') != 'shown') {
  $('.consent').show();
  localStorage.setItem('cookieSeen','shown')
};
