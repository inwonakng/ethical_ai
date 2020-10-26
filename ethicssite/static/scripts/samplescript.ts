// this is the function that will be passed along with the request. 
// Every function that goes through the 'http' function should expect one data object and one packed object of arguments it can use.
function writetopage(data:Array<JSON>,args:any){
    let question = make('div','q'+args)
    let table = maketable(data,args)
    question.appendChild(table)

    addsurveytopage(question, num)
    addsliderstopage(data.length)
}

function maketable(data:Array<JSON>,index:number){
    let table = make('table','table'+index) as HTMLTableElement
    // table headers
    let row = table.createTHead().insertRow()
    row.appendChild(make('th'))
    for (let i=1;i<=data.length;i++){
        let th = make('th')
        th.innerHTML = 'Option' + i
        row.appendChild(th)
    }
    // table body
    for (let key in data[0]){
        let row = table.insertRow()
        row.insertCell().innerHTML = key
        for (let d of data){
            row.insertCell().innerHTML = d[key]
        }
    }
    return table
}

function makeslider(index:string){
    let scorecontainer = make('div', 'option-score-container');
    let title = make('p');
    title.className = "option-score";
    title.innerHTML = "Option " + index;
    let slidercontainer = make('div');
    slidercontainer.className = "slidecontainer"
    var slider = document.createElement('input')
    slider.type = "range"
    slider.id = 'range' + 1;
    slider.min = "0"
    slider.max="10"
    slider.value="0"
    slider.className = "slider"
    slidercontainer.appendChild(slider)
    scorecontainer.appendChild(title)
    scorecontainer.appendChild(slidercontainer)
    return scorecontainer;
}

function guicheck(){
    if(num == 0){
        document.getElementById("prev").setAttribute("disabled", "true")
    }
    else{
        document.getElementById("prev").removeAttribute("disabled")
    }
}

function next(){
    document.getElementById("q"+num).style.display = "none"
    document.getElementById("slides" + num).style.display = "none"
    num++;

    if(num==maxScenarios){
        document.getElementById("final_page").style.display="block"
        document.getElementById("question").style.display="none"
        document.getElementById("scorecontainer").style.display="none"
    }
    else{
        // Did we already create this scenario?
        var element = document.getElementById(("q"+num))
        if(typeof(element) != "undefined" && element != null){
            // Then the scenario has already been created.
            document.getElementById("q"+num).style.display = "block"
            document.getElementById("slides" + num).style.display = "block"
        }
        else{
            http('getscenario',writetopage,num)
        }
    }
    
    guicheck()
}

function prev(){
    if(num == maxScenarios){
        document.getElementById("final_page").style.display="none"
        document.getElementById("question").style.display="block"
        document.getElementById("scorecontainer").style.display="block"
    }
    else{
        document.getElementById("q"+num).style.display = "none"
        document.getElementById("slides" + num).style.display = "none"
    }
    num--;
    document.getElementById("q"+num).style.display = "block"
    document.getElementById("slides" + num).style.display = "block"
    guicheck()
}

function grabdata(){
    for(var i=0; i < maxScenarios; i++){

    }
}

// initial page
var num = 0;
var maxScenarios = 10;
var data = [];
http('getscenario',writetopage,num)

