// this is the function that will be passed along with the request. 
// Every function that goes through the 'http' function should expect one data object and one packed object of arguments it can use.
function writetopage(data:Array<JSON>,args:any){
    let question = make('div','q'+args)
    let table = maketable(data,args)
    question.appendChild(table)

    addsurveytopage(question, scenarioNum)
    addsliderstopage(data.length)
}

function displayFinalPage(data:Array<JSON>, args:any){
    addSlidersToFinalPage(data);
}

function addSlidersToFinalPage(data:Array<JSON>){
    for (let key in data[0]){
        document.getElementById("features").append(makeslider(key));
    }
}

// Creates an HTML table to display the data in data.
// index: the scenario we are currently on. Used to assign id.
//        Makes data grabbing a bit easier (Plan on grabbing data
//        once the user makes final submission)
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
///  Creates a slider to represent a specific feature. 
//  index:  the scenarioNumber of people in each scenario, since 
//          we are rating on an option (person).
function makeslider(index:string){
    // Contains everything involved in creating a score.
    let scorecontainer = make('div', 'option-score-container');

    // Label for slider
    let title = make('p');
    title.className = "option-score";
    if(Number.isInteger(Number(index))){
        title.innerHTML = "Option " + index;
    }
    else{
        title.innerHTML = index;
    }

    // Container for each slider. Used only in stylings
    let slidercontainer = make('div');
    slidercontainer.className = "slidecontainer"

    // The slider itself
    var slider = document.createElement('input')
    slider.type = "range"
    if(Number.isInteger(Number(index))){
        slider.id = 'range' + index
    }
    else{
        slider.id = index;
    }
    slider.min = "0"
    slider.max="10"
    slider.value="0"
    slider.className = "slider"

    // Adding all of the elements within each other accordingly. 
    slidercontainer.appendChild(slider)
    scorecontainer.appendChild(title)
    scorecontainer.appendChild(slidercontainer)
    return scorecontainer;
}

// Monitors GUI-related changes based on given scenario.
function guicheck(){
    // Users can't go to previous scenario if there is no scenario to display
    if(scenarioNum == 0){
        document.getElementById("prev").setAttribute("disabled", "true")
    }
    else{
        document.getElementById("prev").removeAttribute("disabled")
    }
}

// Handles how the user visits the "next page". Involves generating new 
// surveys and displaying the survey-results page and the final-page.
function next(){
    clearCurrentScenario()
    scenarioNum++;

    // Has the user finished the first part of the survey?
    if(scenarioNum==maxScenarios){
        viewFinalSurveyPage();
        http('getscenario',addSlidersToFinalPage,scenarioNum)
    }
    else{
        // Assumes the person is still taking the first part of the scenario.
        // Did we already create this scenario?
        callNextScenario()
    }
    guicheck()
}

// Handles how the user visits previous pages. Includes navigating to 
// previous scenarios and previously visited pages IF ALLOWED TO.
function prev(){
    // Is the user trying to navigate back to their survey?
    if(scenarioNum == maxScenarios){
        navigateBackToSurvey()
    }
    else{
        // Assumes the person is
        // not on the final page.
        clearCurrentScenario()
    }
    scenarioNum--;
    // Displays the previous survey. Assumes the person is not on the final page.
    viewCurrentScenario()
    guicheck()
}

function assembleStars(num:number){
    
}

// TODO Megan: Store data from front-end to data structure.
function grabdata(){
}

// initial page
var scenarioNum = 0;
var maxScenarios = 10;
var data = [];
http('getscenario',writetopage,scenarioNum)

