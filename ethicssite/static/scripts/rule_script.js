$(document).ready(() => {

  // $('.add_rules_card').hide()
  // $('.custom_rules_card').hide()

  // $('#generate_rules').on('click', event => {
  //   $("#container2").hide();
  //   $("#container1").show();
  //   $(".custom_rules_card").hide();
  //   $(".add_rules_card").show();
  //   $("#final_type").val('generate') 

  //   $("#bad_text").show();
  //   $("#container4").hide();
  //   $("#container3").show();
  //   $(".bad_cob1").show();
  // });

  // $('#set_rules').on('click', event => {
  $("#container1").hide();
  $("#container2").show();
  $(".add_rules_card").hide();
  $(".custom_rules_card").show();
  $("#final_type").val('custom')

  $("#bad_text").show();
  $("#container3").hide();
  $("#container4").show();
  $(".bad_cob1").hide();
  // });

  $('.custom_rules_card').on('click', event => {
    idx = $('.custom_rule_card').length + 1
    var structure = $(
      `<div class = "custom_rule_card">
        <textarea id="custom_option" class="custom_option_card" type="text" 
            placeholder="Question ex) Rank the options by score, higher the better"></textarea>
        <div class="input_container">
          <textarea id="custom_option" class="custom_option_card" type="text" placeholder="Option 1"></textarea>
        </div>
        <div class = "add_option custom_option_card">
          Add another option
        </div>
        <br/>
      </div>`
    );
    $("#container2").append(structure);
  });

  // on file select
  // $('#rule_file').change(function(){
  //   console.log('file detected!!')
  //   fname = $('#rule_file').val().toString().split('\\')
  //   $('#filename').html(fname[fname.length-1])
  //   const reader = new FileReader()
  //   reader.onload = function(event){
  //     // var jsonVal = JSON.parse(event.target.result)
  //     $('#hiddenjson').val(event.target.result)
  //   }
  //   reader.readAsText($('#rule_file')[0].files[0])
  // })

})

$(document).on('click','.add_option', function(){
  index = $(this).parent().find('.input_container textarea').length + 1
  var structure = $(
    '<textarea id="custom_option" class="custom_option_card" type="text" placeholder="Option '+index+'"></textarea>'
  );
  var toAppend=$(this).parent().children().eq(1);
  toAppend.append(structure);
});

function parse_data() {
  // get type here
  // just gonna cover custom case for demo.
  // ttype = 'custom'
  ttitle = byid('rule_name').value
  pprompt = byid('rule_prompt').value

  // data_tosend will be a list of list of string
  data_tosend = []
  // if (ttype === 'custom'){
    for(cont of $('.custom_rule_card')){
      question = $(cont).children().eq(0)[0].value
      options = []
      // first getting the div that contains the textareas
      for (cc of $(cont).children().eq(1).children()){
        options.push(cc.value)
      }
      data_tosend.push({  'question': question,
                          'options':  options})
    }
  // }else{
  //   uploaded = $('#rule_file')[0].files
  //   if(uploaded.length == 0){
  //     alert('Input file must be present!')
  //     return
  //   }
    
  //   console.log('okayyy')
  //   data_tosend = JSON.parse($('#hiddenjson').val())
  //   console.log(data_tosend)
  //   // one day....
  // }

  // nullchecks
  if(ttitle.length==0 || Object.keys(data_tosend).length == 0){
    alert('title or survey content cannot be null!')
    return
  }

  console.log(data_tosend)

  http_post('saverule',
    {
      title:ttitle,
      prompt:pprompt,
      data:data_tosend
    }
    ,true
  )
}