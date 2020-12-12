$(document).ready(() => {

  $('.test').show();

  $('#generate_rules').on('click', event => {
    $("#container2").hide();
    $("#container1").show();
    $(".custom_rules_card").hide();
    $(".add_rules_card").show();
    $("#final_type").val('generate') 

    $("#bad_text").show();
    $("#container4").hide();
    $("#container3").show();
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
    $("#final_type").val('custom')

    $("#bad_text").show();
    $("#container3").hide();
    $("#container4").show();
    $(".bad_cob1").hide();
  });

  $('.custom_rules_card').on('click', event => {
    idx = $('.custom_rule_card').length + 1
    var structure = $(
      `<div class = "custom_rule_card">
        <p>Question `+idx+`</p>
        <div class="input_container">
          <textarea id="custom_option" class="custom_option_card" type="text" placeholder="Custom option"></textarea>
        </div>
        <div class = "add_option custom_option_card">
          Add another option
        </div>
        <br/>
      </div>`
    );
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
})

$(document).on('click','.add_option', function(){
  var structure = $(
    '<textarea id="custom_option" class="custom_option_card" type="text" placeholder="Custom option"></textarea>'
  );
  var toAppend=$(this).parent().children().eq(1);
  toAppend.append(structure);
});

$(document).on('click','.add_rules_card', function(){
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

function parse_data() {
  // get type here
  // just gonna cover custom case for demo.
  ttype = $("#final_type")[0].value
  ttitle = byid('rule_name').value
  pprompt = byid('rule_prompt').value

  // data_tosend will be a list of list of string
  data_tosend = []
  if (ttype === 'custom'){
    for(cont of $('.custom_rule_card')){
      options = []
      // first getting the div that contains the textareas
      for (cc of $(cont).children().eq(1).children()){
        options.push(cc.value)
      }
      data_tosend.push(options)
    }
  }else{
    // one day....
  }

  // nullchecks
  if(ttitle.length==0 || data_tosend[0].length == 0){
    alert('title or survey content cannot be null!')
    return
  }

  console.log(data_tosend)

  http_post('saverule',
    {
      type:ttype,
      title:ttitle,
      prompt:pprompt,
      data:data_tosend
    }
    ,true
  )
}