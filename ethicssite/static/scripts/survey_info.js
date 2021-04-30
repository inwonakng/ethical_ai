function get_color(pal,len,alpha){
    return palette(pal, len).map(function(hex) {
        return '#' + hex+alpha;
    })
}

function make_chart(chart_type,parent,col_prefix,data){
    // prep what to show on chart
    var labels = []    
    for(var i = 1; i <= data.length; i++){
        labels.push(col_prefix + i)
    }

    // reset canvase
    parent.find('canvas').remove()
    parent.append('<canvas style="width:100%"></canvas>')
    ctx = parent.find('canvas')[0].getContext('2d');
        
    // prepare each dataset
    prepped = [{
            data:data,
            backgroundColor: get_color('cb-Set1',data.length,'80'),
            borderColor: get_color('cb-Set1',data.length,'FF'),
            borderWidth: 1
        }]

    // make the chart
    new Chart(ctx, {
        type: chart_type,
        data: {
            labels: labels,
            datasets: prepped
        },
        options: {
            responsive: true, 
            maintainAspectRatio: false,
            legend: {display: false},

            plugins: {
                datalabels: {
                    color:'#000',
                    display:true,
                    anchor: 'end',
                    align: 'start',
                    formatter: function(value){return Math.round(value)+'%'},
                    offset: 2,
                    font: {
                        weight: 'bold',
                        size: 18,
                    }
                }
            }
        }
    });
}

function show_votes(area,data){
    area.children().remove()

    table = $('<table>')

    table.append(show_votingrule(data, 'Borda'))
    table.append(show_votingrule(data, 'Plurality'))
    table.append(show_votingrule(data, 'Maximin'))
    area.append(table)
}

function show_votingrule(data, type){
    // area.children().remove()
    slot = $('<tr>')
    slot.append(
        $('<td>').html(type)
        ).append(
            $('<td>').html('<b>'+data[type.toLowerCase()].join(' > ')+'</b>')
        )

    return slot
}
    
function fill_charts(q_idx){
    $('.showoptions').find('.onequestion').hide()
    $('.showoptions').find('.onequestion').eq(q_idx-1).show()
    
    $('#survey-results select').hide()
    $('#survey-results select').eq(q_idx-1).show()    

    shared_legend(ml_output[q_idx-1].length)

    // ML chart
    make_chart(
        'pie',
        $('#ml-results .onechart'),
        'Option ',
        ml_output[q_idx-1])

    make_chart(
        'pie',
        $('#survey-results .onechart'),
        'Option ',
        survey_output[q_idx-1][0]
    )
}

function shared_legend(len){
    labels = []
    data = []
    for(i = 0; i < len; i++){
        labels.push('Option '+(i+1))
        data.push('')
    }

    ctx = $('.shared-legend canvas')[0].getContext('2d')
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data:data,
                backgroundColor: get_color('cb-Set1',len,'80'),
                borderColor: get_color('cb-Set1',len,'FF'),
                borderWidth: 1,
                hidden:true
            }]
        },
        options:{
            maintainAspectRatio: false,
        }
    });
}

// ========================
// ==========MAIN==========
// ========================

$(document).ready(() => {
    if (!$(".user_area .my_survey").hasClass("selected")){
        $(".user_area .option").removeClass("selected");
        $(".user_area .my_survey").addClass("selected"); }
    fill_charts(1)
    show_votes($('#show-votes .raw-data'),survey_voting_results[0])
    show_votes($('#show-votes .ml-data'),pl_voting_results[0])
});

// ========================
// ======INPUT EVENTS======
// ========================
$(document).on('change','select.question',function(){
    fill_charts($(this).val())
})

$(document).on('change','select.option',function(){
    make_chart(
        'pie',
        $('#survey-results .onechart'),
        'Option ',
        survey_output[$('select.question').val()-1][$(this).val()-1]
    )
})

$(document).on('change','select.voting-rule',function(){
    idx = $('select.question').val()-1
    show_votes($('#show-votes'),survey_voting_results[idx])
    show_votes($('#show-votes .ml-data'),pl_voting_results[idx])
})