$(document).ready(() => {

  $('.test').show();

  $('#generate_rules').on('click', event => {
    $("#container2").hide();
    $("#container1").show();
    $(".custom_rules_card").hide();
    $(".add_rules_card").show();

    $("#bad_text").show();
    $("#container4").hide();
    $("#container3").show();
    $(".bad_cob2").hide();
    $(".bad_cob1").show();
  });

  $('.add_rules_card').on('click', event => {
    var structure = $('<div class = "rule_card card"><label>Rule name:</label><input type="text" id="attribute_name" placeholder="Rule name"><br><label>Rule type:</label><input type="text" id="attribute_type" placeholder="Rule type"></div>');
    $("#container1").append(structure);
  });

  $('#set_rules').on('click', event => {
    $("#container1").hide();
    $("#container2").show();
    $(".add_rules_card").hide();
    $(".custom_rules_card").show();

    $("#bad_text").show();
    $("#container3").hide();
    $("#container4").show();
    $(".bad_cob1").hide();
    $(".bad_cob2").show();
  });

  $('.custom_rules_card').on('click', event => {
    var structure = $('<div class = "rule_card card"><textarea id="custom_rule" placeholder="Custom rule"></textarea></div>');
    $("#container2").append(structure);
  });

  $('.bad_cob1').on('click', event => {
    var structure = $('<div class = "card"><label>Rule:</label><input type="text" id="attribute_name" placeholder="Rule name"><br><label>Bad value:</label><input type="text" id="attribute_type" placeholder="Bad value"></div>');
    $("#container3").append(structure);
  });

  $('.bad_cob2').on('click', event => {
    var structure = $('<div class = "card"><label>Rule:</label><input type="text" id="attribute_name" placeholder="Rule name"><br><label>Bad value:</label><input type="text" id="attribute_type" placeholder="Bad value"></div>');
    $("#container4").append(structure);
  });

  $('.add_one').on('click', event => {
    var structure = $('<input type="text" name="rule_name" placeholder="Your rules"><input type="text" name="rule_type" placeholder="Type of your rule"><br>');
    $(".rule_form").append(structure);
  });

})
