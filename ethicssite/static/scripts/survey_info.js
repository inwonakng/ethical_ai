function make_chart(parent,data){
    var labels = []
    var ctx = parent.find('canvas')[0].getContext('2d');
    if(parent[0].id == 'ml-results'){
        for(i = 1; i <= data.length; i++){
            labels.push('Option ' + i +' score')
        }
    }else{
        for(i = 1; i <= data.length; i++){
            labels.push('Rank '+i)
        }
    }


    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                // {{numberOfResponses|safe}},
                backgroundColor: palette('cb-Set1', data.length).map(function(hex) {
                    return '#' + hex+'80';
                }),
                borderColor: palette('cb-Set1', data.length).map(function(hex) {
                    return '#' + hex+'FF';
                }),
                borderWidth: 1
            }]
        },
    });
}

$(document).ready(() => {
    if (!$(".user_area .my_survey").hasClass("selected")) {
        $(".user_area .option").removeClass("selected");
        $(".user_area .my_survey").addClass("selected");
    }
    make_chart($('#survey-results'),survey_output[0][0])
    make_chart($('#ml-results'),ml_output[0])
});

$(document).on('change','select',function(){
    p = $(this).parent()
    pp = p.parent()
    console.log(pp)
    pp.find('canvas').remove()
    pp.append('<canvas></canvas>')

    if(this.name == 'question' && p.find('select').length > 1){
        $('.option').hide()
        $('select.option').eq($(this).val()-1).show()
    }

    q_idx = p.find('.question').val()
    o_idx = p.find('.option').val()

    title = 'Looking at distribution for Question '

    if(pp[0].id == 'survey-results'){
        data = survey_output[q_idx-1][o_idx-1]
        title+=q_idx + ' Option ' + o_idx 
    }else{
        data = pp,ml_output[q_idx-1]
        title+=q_idx
    }
    pp.find('.chart-title a').html(title)
    make_chart(pp,data)
})
