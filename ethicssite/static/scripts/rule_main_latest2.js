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
    var structure = $('<div class = "rule_card card"><label>Rule name:</label><input type="text" id="attribute_name" placeholder="Rule name"><br><label>Rule type:</label><input type="text" id="attribute_type" placeholder="Rule type"><div id="slider"><div id="custom-handle1" class="ui-slider-handle"></div><div id="custom-handle2" class="ui-slider-handle"></div></div></div>');
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
    var structure = $('<div class = "custom_rule_card"><p>Scenario</p><div class = "custom_option_container"><div class = "custom_option_card"><textarea id="custom_rule" name = "custom" placeholder="Custom option"></textarea></div></div><div class = "add_option custom_option_card"><p class="p_card_custom_option">Add more options</p></div><br/></div>');
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

  // $('.add_option').on('click', event => {
  //   var structure = $('<div class = "custom_option_card"><textarea id="custom_rule" name = "custom" placeholder="Custom option"></textarea></div>');
  //   $(".custom_option_container").append(structure);
  // });

  // $('.add_option').live('click',function() {
  //   var structure = $('<div class = "custom_option_card"><textarea id="custom_rule" name = "custom" placeholder="Custom option"></textarea></div>');
  //   $(".custom_option_container").append(structure);
  // });

})

$(document).on('click','.add_option', function(){
  var structure = $('<div class = "custom_option_card"><textarea id="custom_rule" name = "custom" placeholder="Custom option"></textarea></div>');
  var toAppend=$(this).parent().children().eq(1);
  toAppend.append(structure);
});

$(document).on('click','.add_rules_card', function(){
  console.log("here");
  var handle1 = $( "#custom-handle1" );
  var handle2 = $( "#custom-handle2" );
  $( "#slider" ).slider({
    range: true,
    min: 0,
    max: 500,
    values: [ 75, 300 ],
    create: function() {
      handle1.text( $( this ).slider( "values",0 ) );
      handle2.text( $( this ).slider( "values",1 ) );
    },
    slide: function( event, ui ) {
      handle1.text( ui.values[0] );
      handle2.text( ui.values[1] );
    }

  });
});


$( function() {
    var handle1 = $( "#custom-handle1" );
    var handle2 = $( "#custom-handle2" );
    $( "#slider" ).slider({
      range: true,
      min: 0,
      max: 500,
      values: [ 75, 300 ],
      create: function() {
        handle1.text( $( this ).slider( "values",0 ) );
        handle2.text( $( this ).slider( "values",1 ) );
      },
      slide: function( event, ui ) {
        handle1.text( ui.values[0] );
        handle2.text( ui.values[1] );
      }

    });
  });
