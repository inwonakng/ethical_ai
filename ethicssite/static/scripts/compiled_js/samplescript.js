// this is the function that will be passed along with the request. 
// Every function that goes through the 'http' function should expect one data object and one packed object of arguments it can use.
function writetopage(data, args) {
    totalData.push(data);
    let question = make('div', 'q' + args);
    let table = maketable(data, args);
    question.appendChild(table);
    addsurveytopage(question, scenarioNum);
    addsliderstopage(scenarioNum, data.length);
}
// Creates an HTML table to display the data in data.
// index: the scenario we are currently on. Used to assign id.
//        Makes data grabbing a bit easier (Plan on grabbing data
//        once the user makes final submission)
function maketable(data, index) {
    if (index == maxScenarios - 1) {
        makeFinalPage(data);
    }
    console.log(data);
    let table = make('table', 'table' + index);
    // table headers
    let row = table.createTHead().insertRow();
    row.appendChild(make('th'));
    for (let i = 1; i <= data.length; i++) {
        let th = make('th');
        th.innerHTML = 'Option' + i;
        row.appendChild(th);
    }
    // table body
    for (let key in data[0]) {
        let row = table.insertRow();
        row.insertCell().innerHTML = key;
        for (let d of data) {
            row.insertCell().innerHTML = d[key];
        }
    }
    return table;
}
function makeFinalPage(data) {
    var element = document.getElementById("final_page");
    for (let key in data[0]) {
        dataFeatures.push({ "key": key, "value": 0 });
        let div = make('div');
        let p = make('p');
        p.className = "feature";
        p.innerHTML = key;
        let slidercontainer = make('div');
        slidercontainer.className = "slidecontainer";
        // The slider itself
        var slider = document.createElement('input');
        slider.type = "range";
        slider.id = 'score-' + key;
        slider.min = "0";
        slider.max = "10";
        slider.value = "0";
        slider.className = "slider";
        slidercontainer.appendChild(slider);
        div.appendChild(p);
        div.appendChild(slidercontainer);
        element.appendChild(div);
    }
    var p2 = make("p", "explain-followup");
    p2.innerHTML = "Please write more than 20 words to explain how you made your choices";
    var textarea = make("textarea", "textarea");
    element.appendChild(p2);
    element.appendChild(textarea);
}
function clearPage() {
    document.getElementById("final_page").style.display = "none";
    document.getElementById("prev").style.display = "none";
    document.getElementById("go-to-review").style.display = "none";
    document.getElementById("question").style.display = "none";
    document.getElementById("scorecontainer").style.display = "none";
    document.getElementById("submit").style.display = "inline";
    for (let i = 0; i < maxScenarios; i++) {
        document.getElementById("q" + i).style.display = "none";
        document.getElementById("slides" + i).style.display = "none";
        document.getElementById("scorecontainer").style.display = "none";
    }
}
function viewReviewPage() {
    clearPage();
    let element = document.getElementById("review_page");
    element.style.display = 'block';
    // if (isNaN( document.getElementById("review0") )) {
    //     for(let i = 0; i < maxScenarios; i++) {
    //         element.removeChild(document.getElementById("review" + i));
    //     }
    // }
    sortFeatures();
    for (let i = 0; i < maxScenarios; i++) {
        let currentQuestion = totalData[i];
        let div = make("div", "review" + i);
        div.className = "review_div";
        let p = make("p", "prompt");
        div.appendChild(p);
        p.innerHTML = "Prompt";
        let table = make('table', 'q' + i + "review");
        // table headers
        let row = table.createTHead().insertRow();
        row.appendChild(make('th'));
        for (let j = 0; j < 3; j++) {
            let th = make('th');
            th.innerHTML = dataFeatures[j]["key"];
            row.appendChild(th);
        }
        let th = make('th');
        th.innerHTML = "Your Choices";
        console.log('current question: ', currentQuestion);
        row.appendChild(th);
        // table body
        for (let j = 0; j < currentQuestion.length; j++) {
            let row = table.insertRow();
            row.insertCell().innerHTML = "Option " + j;
            for (let k = 0; k < 3; k++) {
                let currentFeauture = dataFeatures[k]["key"];
                row.insertCell().innerHTML = currentQuestion[j][currentFeauture];
            }
            let sliderIndex = j;
            console.log("q" + i + "range" + sliderIndex);
            let value = byid("q" + i + "range" + sliderIndex).value;
            row.insertCell().innerHTML = value;
        }
        div.appendChild(table);
        let button_div = make("div");
        button_div.className = "review_button";
        let button = make("button", i + "review_button");
        button.innerHTML = "Modify Anwser";
        button.onclick = function (i) {
            backToPage(parseInt(i.target.id));
        };
        button_div.appendChild(button);
        div.appendChild(button_div);
        element.appendChild(div);
    }
}
function backToPage(pageNum) {
    document.getElementById("review_page").style.display = "none";
    document.getElementById("submit").style.display = "none";
    document.getElementById("go-to-review").style.display = "inline";
    document.getElementById("question").style.display = "block";
    document.getElementById("q" + pageNum).style.display = "block";
    document.getElementById("slides" + pageNum).style.display = "block";
    document.getElementById("scorecontainer").style.display = "block";
}
function sortFeatures() {
    for (let i in dataFeatures) {
        let scoreId = "score-" + dataFeatures[i]["key"];
        dataFeatures[i]["value"] = Number(byid(scoreId).value);
    }
    dataFeatures = dataFeatures.sort(compare);
}
function compare(a, b) {
    return b["value"] - a["value"];
}
//  Creates a slider to represent a specific feature. 
//  index:  the scenarioNumber of people in each scenario, since 
//          we are rating on an option (person).
function makeslider(scen_idx, index) {
    // Contains everything involved in creating a score.
    let scorecontainer = make('div', 'option-score-container');
    // Label for slider
    let title = make('p');
    title.className = "option-score";
    title.innerHTML = "Option " + index;
    // Container for each slider. Used only in stylings
    let slidercontainer = make('div');
    slidercontainer.className = "slidecontainer";
    // The slider itself
    var slider = document.createElement('input');
    slider.type = "range";
    slider.id = 'q' + scen_idx + 'range' + index;
    slider.min = "0";
    slider.max = "10";
    slider.value = "0";
    slider.className = "slider";
    // Adding all of the elements within each other accordingly. 
    slidercontainer.appendChild(slider);
    scorecontainer.appendChild(title);
    scorecontainer.appendChild(slidercontainer);
    return scorecontainer;
}
// Monitors GUI-related changes based on given scenario.
function guicheck() {
    // Users can't go to previous scenario if there is no scenario to display
    if (scenarioNum == 0) {
        document.getElementById("prev").setAttribute("disabled", "true");
    }
    else {
        document.getElementById("prev").removeAttribute("disabled");
    }
}
// Handles how the user visits the "next page". Involves generating new 
// surveys and displaying the survey-results page and the final-page.
function next() {
    clearCurrentScenario();
    scenarioNum++;
    // Has the user finished the first part of the survey?
    if (scenarioNum == maxScenarios) {
        viewFinalSurveyPage();
    }
    else {
        // Assumes the person is still taking the first part of the scenario.
        // Did we already create this scenario?
        callNextScenario();
    }
    guicheck();
}
// Handles how the user visits previous pages. Includes navigating to 
// previous scenarios and previously visited pages IF ALLOWED TO.
function prev() {
    // Is the user trying to navigate back to their survey?
    if (scenarioNum == maxScenarios) {
        navigateBackToSurvey();
    }
    else {
        // Assumes the person is
        // not on the final page.
        clearCurrentScenario();
    }
    scenarioNum--;
    // Displays the previous survey. Assumes the person is not on the final page.
    viewCurrentScenario();
    guicheck();
}
// TODO Megan: Store data from front-end to data structure.
function grabdata() {
    for (let i of Array(maxScenarios).keys()) {
        byid('q');
    }
}
function submitResult() {
    alert('hey');
}
// initial page
var scenarioNum = 0;
var maxScenarios = 10;
var data = [];
var dataFeatures = [];
var totalData = [];
http('getscenario', writetopage, scenarioNum);
//# sourceMappingURL=samplescript.js.map