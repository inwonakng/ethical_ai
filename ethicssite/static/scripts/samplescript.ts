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
    slider.min = "1"
    slider.max="10"
    slider.value="5"
    slider.className = "slider"
    slidercontainer.appendChild(slider)
    scorecontainer.appendChild(title)
    scorecontainer.appendChild(slidercontainer)
    return scorecontainer;
}

function next(){
    document.getElementById("q"+num).style.display = "none"
    document.getElementById("slides" + num).style.display = "none"
    num++;

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

function prev(){
    document.getElementById("q"+num).style.display = "none"
    document.getElementById("slides" + num).style.display = "none"
    num--;
    document.getElementById("q"+num).style.display = "block"
    document.getElementById("slides" + num).style.display = "block"
}

// testing grabbing generated survey scenario
var num = 0;
http('getscenario',writetopage,num)

//http('getscenario',writetopage,1)
