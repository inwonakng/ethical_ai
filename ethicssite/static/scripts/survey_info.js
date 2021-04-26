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

    // parent.remove('a')
    // parent.parent().append('<a>'+title+'</a>')

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
            maintainAspectRatio: false
        }
    });
}

function make_subcharts(area,data){
    // first reset
    console.log(Math.ceil(data.length/2))
    area.children().remove()
    for(var i = 0; i < Math.ceil(data.length/2); i++){
        newdiv = $('<div>', {class:'charts-row'})
        
        leftdiv = $('<div>',{class:'smallchart'})
        leftdiv.append(
            $('<div>',{class:'smallframe'}).append(
                '<canvas></canvas>'
            )
        )
        // leftdiv.find('.smallframe').append('<canvas></canvas>')
        // leftdiv.append('<canvas></canvas>')
        
        newdiv.append(leftdiv)
        console.log(i)
        rightdiv = $('<div>',{class:'smallchart'})
        if(i*2+1<data.length)
            rightdiv.append($('<div>',{class:'smallframe'}).append(
                '<canvas></canvas>'
            )   
        )
            // rightdiv.find('.smallframe').append('<canvas></canvas>')    
            // rightdiv.append('<canvas></canvas>')    
        newdiv.append(rightdiv)
        area.append(newdiv)

        newdiv.find('canvas').each(function(j){
            $(this).parent().parent().prepend('<b>Option '+(i*2+j+1)+'</b>')
            make_chart(
                'pie',
                $(this).parent(),
                'Rank ',
                data[j])
        })
    }
        
}
    
function fill_charts(q_idx){
    $('.showoptions').find('.onequestion').hide()
    $('.showoptions').find('.onequestion').eq(q_idx-1).show()
    
    // ML chart
    make_chart(
        'pie',
        $('#ml-results .onechart'),
        'Option ',
        ml_output[q_idx-1])
        
        // Survey Data Chart
    make_subcharts(
        $('#survey-results .manycharts'),
        survey_output[q_idx-1])
            
}


// ========================
// ==========MAIN==========
// ========================

$(document).ready(() => {
    if (!$(".user_area .my_survey").hasClass("selected")) {
        $(".user_area .option").removeClass("selected");
        $(".user_area .my_survey").addClass("selected");
    }
    fill_charts(1)
});

// ========================
// ======INPUT EVENTS======
// ========================

$(document).on('change','select',function(){
    fill_charts($(this).val())
})
