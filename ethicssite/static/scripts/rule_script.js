$(document).ready(() => {
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