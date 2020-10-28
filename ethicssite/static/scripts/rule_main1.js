$(document).ready(() => {

  $('.test').show();

  $('#generate_rules').on('click', event => {
    $("#container2").hide();
    $("#container1").show();
    $(".add_your_rules").hide();
    $(".add_rules").show();

    $("#bad_text").show();
    $("#container4").hide();
    $("#container3").show();
    $(".add_bad2").hide();
    $(".add_bad1").show();
  });

  $('.add_rules').on('click', event => {
    var structure = $('<label for="attribute_name">Attribute name:</label><input type="text" id="attribute_name"><br><label for="attribute_value">Attribute value:</label><select name="cars" id="cars"><option value="1">1. _______________</option><option value="2">2. _______________</option><option value="3">3. _______________</option><option value="4">4. _______________</option></select><br><br>');
    $("#container1").append(structure);
  });

  $('#set_rules').on('click', event => {
    $("#container1").hide();
    $("#container2").show();
    $(".add_rules").hide();
    $(".add_your_rules").show();

    $("#bad_text").show();
    $("#container3").hide();
    $("#container4").show();
    $(".add_bad1").hide();
    $(".add_bad2").show();
  });

  $('.add_your_rules').on('click', event => {
    var structure = $('<label for="your_option">Your option:</label><input type="text" id="your_option"><br><br>');
    $("#container2").append(structure);
  });

  $('.add_bad1').on('click', event => {
    var structure = $('<label for="bad_attribute">Bad attribute:</label><input type="text" id="bad_attribute"><br><label for="bad_values">Bad values:</label><select name="values" id="values"><option value="1">1. _______________</option><option value="2">2. _______________</option><option value="3">3. _______________</option><option value="4">4. _______________</option></select><br><br>');
    $("#container3").append(structure);
  });

  $('.add_bad2').on('click', event => {
    var structure = $('<label for="bad_attribute">Bad attribute:</label><input type="text" id="bad_attribute"><br><label for="bad_values">Bad values:</label><select name="values" id="values"><option value="1">1. _______________</option><option value="2">2. _______________</option><option value="3">3. _______________</option><option value="4">4. _______________</option></select><br><br>');
    $("#container4").append(structure);
  });

  $('.add_one').on('click', event => {
    var structure = $('<input type="text" name="rule_name" placeholder="Your rules"><input type="text" name="rule_type" placeholder="Type of your rule"><br>');
    $(".rule_form").append(structure);
  });

})
