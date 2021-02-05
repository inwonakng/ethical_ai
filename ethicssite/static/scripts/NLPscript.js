// javascript doesn't have a function to remove one element from list...
function remove(arr,ele){
    idx = arr.indexOf(ele)
    arr.splice(idx,1)
    return arr
}

function scroll_to_top(){
    $('.main')[0].scrollIntoView()
}

function make_pairs(arr){
    retarr = []
    for(i=0;i<arr.length;i++){
        for(j=i+1;j<arr.length;j++){
            retarr.push([arr[i],arr[j]])
        }
    }
    return retarr
}

function make_hilight(before){
    $('#hilight').remove()

    background = $('<line/>',
                        {
                            'id':'hilight',
                            'class': 'back-hilight',
                            'x1': $(before).attr('x1'),
                            'y1': $(before).attr('y1'),
                            'x2': $(before).attr('x2'),
                            'y2': $(before).attr('y2')
                        })

    el = $('<line/>',
                    {   
                        'id': before.id,   
                        'class': $(before).attr('class'),
                        'x1': $(before).attr('x1'),
                        'y1': $(before).attr('y1'),
                        'x2': $(before).attr('x2'),
                        'y2': $(before).attr('y2')
                    })

    base = $(before).closest('#base')
    $(before).remove()
    base.append(background)
    base.append(el)
    base.html(base.html())
}

function check_input(button){
    // take the button and checks if related input is filled
    [from,to] = button.id.split('to')

    box = $(button).closest('.graph-container')
    
    // checking checkbox
    if($(box).find('#'+from+'-'+to+'-NA').attr('checked')){
        return true
    }
    // checking slider
    if($(box).find('#'+from+'-vs-'+to).val()){
        return true
    }
    return false
}

// this function sets up the each page and gets the corresponding comments/entity infos
function set_data(){
    com_idx = window.comment_idxs[window.page_index]
    dat_idx = window.dataset_idxs[window.page_index]
    
    $('#context-container').empty()

    // setting the main and original comment
    fetch(
        'https://inwonakng.github.io/survey-scripts/comments/'+dat_idx+'_comments.json'
    ).then(r=>r.json()).then( comments=>{
        $('#post-title').html(comments.title)
        $('#main-text').html(comments.comments[com_idx])
        $('#original-comment').html(comments.comments[0])

        // setting the hidden reference comments. max is 10
        fetch(
            'https://inwonakng.github.io/survey-scripts/relations/'+dat_idx+'_quote_relations.json'
        ).then(r=>r.json()).then(reftree=>{
            for(r in reftree[com_idx]){
                type = '<b class="type-tag">Previous reply to the original post</b>'
                if(reftree[com_idx][r] == "quote"){
                    type = '<b class="type-tag">Post the commenter in blue is replying to</b>'
                }
                $('#context-container').prepend(
                    '<div style = "display:none"><p class="context-block text-block">'
                    + type
                    +'<br><br>'
                    + comments.comments[r]
                    + '</p></div>'
                )
            }
        })
    })

    // emtpying the tables first
    $('#entities-labels').empty()
    $('#info-section').empty()

    // making tables from the entity info
    fetch(
        'https://inwonakng.github.io/survey-scripts/entities/'+dat_idx+'_entities.json'
    ).then(r=>r.json()).then(ent_vals=>{
        entities = ent_vals['entities']
        entity_values = ent_vals['entity_values']

        table = document.createElement('table')
        table.className = 'entities'
        header = table.insertRow()
        body = table.insertRow()
        for(ent in entities){
            th = document.createElement('th')
            th.innerHTML=ent
            header.append(th)
            body.insertCell().innerHTML=entities[ent]
        }
        $('#entities-labels').append(table)
        //finished with table here 

        // filling out the entity information table
        
        table = document.createElement('table')
        table.className = 'info-table'
        header = table.insertRow()
        header.insertCell().className = 'label'
        
        for(ent in entity_values){
            th = header.insertCell()
            th.innerHTML=ent
            th.className = 'value header'
            header.append(th)
        }
    
        for(param in entity_values[ent]){
            body = table.insertRow()
            label = body.insertCell()
            label.innerHTML=param
            label.className = 'label'
            for(ee in entity_values){
                val = body.insertCell()
                val.innerHTML = entity_values[ee][param]
                val.className = 'value'
            }
        }
        $('#info-section').append(table)
    })
}

function prepare(comments,datasets,entities){
    // these values here are basically global scope. Do not need to re-read
    window.comment_idxs = comments
    window.dataset_idxs = datasets
    window.num_entities = entities
    window.page_index = 'Sample'
    // var alph = ['A','B','C','D','E','F']
    base_length = 150
    verti = ((base_length/3)**2)**.5
    ori_x=130,ori_y = 25
    offset_x = 40
    offset_y = 10


    // ====== making the input UI here! ======
    
    num_entities.forEach((value,index,arr)=>{
        // if number of entities is 3
        if(value == 3){
            coords = {
                // top,left
                'A': [ori_y,ori_x],
                'B': [ori_y + verti,ori_x+base_length/2],
                'C': [ori_y + verti,ori_x-base_length/2]
            }
        }else{
            // if only two give some(25) more y offset to bring down.
            coords = {
                'A': [ori_y+25,ori_x-base_length/2],
                'B': [ori_y+25,ori_x+base_length/2]
            }
        }

        // drawing the lines inside base before attaching
        base = $('<svg/>',{'id':'base'})
        for([from,to] of make_pairs(Object.keys(coords))){
            base.append(
                $('<line/>',{
                        'id': from+'to'+to,
                        'class':'trig-button',
                        'x1': coords[from][1],
                        'y1': coords[from][0],
                        'x2': coords[to][1],
                        'y2': coords[to][0]
                    }
                )
            )
        }

        diagram = $('<div/>',{'class':'diagram flex-left-input'})
        for(c in coords){
            [y,x] = coords[c]
            diagram.append(
                $('<a/>',{'class':'entity','id':'entity'+c,'html':'Entity '+c })
                    .css('top',y-offset_y)
                    .css('left',x-offset_x)
            )
        }
        
        scores_area = $('<div/>',{'class':'scores-area flex-right-input'})
        for([fir,sec] of make_pairs(Object.keys(coords))){
            scores_area.append(
                $('<div/>', {'class':'select-score','id':'input-'+fir+'to'+sec})
                    .append(
                        $('<b/>',{'class':'score-title'}).html(fir+' vs '+sec)
                    ).append(
                        $('<div/>',{'class':'slider-box'})
                        .append($('<a/>').html(fir+' preferred'))
                        .append($('<crowd-slider/>',{'name':fir+'-vs-'+sec,'id':fir+'-vs-'+sec,'min':-5,'max':5,'pin':'','required':''}))
                        .append($('<a/>').html(sec+' preferred'))
                    ).append(
                        $('<crowd-checkbox/>',{'name':fir+'-'+sec+'-NA','id':fir+'-'+sec+'-NA'}).html('No preference expressed')
                    )
                .hide()
            )
        }


        // putting together the whole div for each page
        $('#all-inputs')
            .append(
                $('<div/>',{'id':'graphspot'+index,'class':'flex-container graph-container'}
                ).append(
                    diagram.append(base)
                ).append(scores_area).hide()
            )
    })

    // gotta refresh the page for svg to work
    $("#reloadhere").html($("#reloadhere").html())

    // ====== Done with the input UI ======

    
    // reset the buttons here
    $('#nextbtn').prop('disabled',false)
    $('#prevbtn').prop('disabled',true)

}

// ====== Button actions below! ======

//CONTINUE button 

$(document).on('click','#user-continue',function(){
    $('#turk_id').hide()
    username = $('#mturk-user').val()
    $('#startloading').show()
    fetch(
        'http://127.0.0.1:8000/api/NLPsurvey_setup',
        {   
            method:'POST',
            body:username
        }
    ).then(
        r=>r.json()
    ).then(r=>{
        prepare(r['comments'],r['datasets'],r['entities'])
        $('#startloading').hide()
        

        $('#practice').show()
    })

})

$(document).on('click','#continue',function(){
    $('#practice').hide()
    $('.one-comment').css('display','block')
    
    $('#scenario-index').html('1/'+window.comment_idxs.length)
    $('#prevbtn').prop('disabled',true)
    window.page_index = 0
    set_data()
    this.style.display = 'none'
    
    $('#all-inputs')
        .children().first().show()
        .find('.trig-button').first().trigger('click')
    scroll_to_top()
})

// NEXT button
// also checks if all the inputs are filled out
$(document).on('click','#nextbtn',function(){
    buttons = $('#graphspot'+window.page_index).find('.trig-button')
    for(b of buttons){
        if(!check_input(b)){
            alert('Please respond to all the questions before moving on!')
            return
        }
    }

    window.page_index += 1
    window.page_index = window.page_index
    $('#scenario-index').html((window.page_index+1)+'/'+window.comment_idxs.length)

    $('#all-inputs').children().hide()
    $('#graphspot'+(window.page_index)).show().find('.trig-button').first().trigger('click')
    
    set_data()
    if(window.page_index == window.comment_idxs.length-1){ $(this).prop('disabled',true) }
    $('#prevbtn').prop('disabled',false)
    
    scroll_to_top()
})

// PREV button
$(document).on('click','#prevbtn',function(){
    window.page_index -= 1
    $('#page-index').val(window.page_index)

    $('#all-inputs').children().hide()
    $('#graphspot'+(window.page_index)).show().find('.trig-button').first().trigger('click')

    $('#scenario-index').html((window.page_index+1)+'/'+window.comment_idxs.length)
    set_data()
    if(window.page_index == 0){ $(this).prop('disabled',true) }
    $('#nextbtn').prop('disabled',false)

    scroll_to_top()
})

// Show MORE comments
$(document).on('click','#show-more',function(){
    boxes = $('#context-container').children().toArray().reverse()
    for([i,c] of boxes.entries()){
        if($(c).css('display') == 'none'){
            $(c).slideToggle("fast","linear")
            scroll_to_top()
            break
        }
    }
    if(i == boxes.length-1){
        this.disabled = true
    }
    $('#show-less').prop('disabled',false)
})

// Show LESS comments
$(document).on('click','#show-less',function(){
    boxes = $('#context-container').children().toArray()
    for([i,c] of boxes.entries()){
        if($(c).css('display') == 'block'){
            $(c).slideToggle("fast","linear")
            scroll_to_top()
            break
        }
    }

    // if no more to hide
    if(i == boxes.length-1){
        this.disabled=true
    }
    $('#show-more').prop('disabled',false)
})

// Clicking the pair link 
$(document).on('click','.trig-button',function(){
    [from,to] = this.id.split('to')
    
    scoresarea = $(this).closest('.graph-container').find('.scores-area')

    for(c of scoresarea.children()){
        $(c).hide()
    }
    scoresarea.find("#input-"+from+'to'+to).show()

    // re-color buttons if inpute satisfied
    // base = $(this).closest('#base')
    
    // put hilight in background

    base = $(this).closest('#base')

    make_hilight(this)
    
    for(b of base.find('.trig-button')){
        if(check_input(b)){
            $(b).addClass('button-filled')
        }else{
            $(b).removeClass('button-filled')
        }
    }
})

// ====== Done with button actions ======
