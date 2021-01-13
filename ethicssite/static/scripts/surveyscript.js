// this is the function that will be passed along with the request. 
// Every function that goes through the 'http' function should expect one data object and one packed object of arguments it can use.
function writetopage(data, args) {
    totalData.push(data);
    let question = make('div', 'q' + args);
    if(isgen){
        let table = maketable(data, args);
        question.appendChild(table);
    }
    // super hardcoding time...
    // html_text = ''

    var outli = make('table','listq'+args)
    var dd;
    for(dd of data){
        var inli = make('tr','')
        inli.innerHTML = dd
        inli.style.fontSize='large'
        outli.appendChild(inli)
    }
    outli.style.borderColor = 'white'
    console.log(data)
    question.appendChild(outli)
    addsurveytopage(question, scenarioNum);
    addsliderstopage(scenarioNum, data.length);
}
// adds the generated scenario to the front-end web page.
function addsurveytopage(element, index) {
    byid("survey").append(element);
}
// Dynamically adds the sliders for the user to choose from,
// given the scenario number (to mark the id of the sliders)
// and the specific slider number (to mark the option that the
// slider is measuring the preference for).
function addsliderstopage(scen_idx, i) {
    var element = document.createElement('div');
    element.id = "slides" + scenarioNum;
    for (var j = 0; j < i; j++) {
        element.append(makeslider(String(scen_idx), String((j))));
    }
    byid("scorecontainer").append(element);
}
// Delete the scenario currently being displayed.
function clearCurrentScenario() {
    byid("q" + scenarioNum).style.display = "none";
    byid("slides" + scenarioNum).style.display = "none";
}
// View the final page of the survey (the page before the survey results)
function viewFinalSurveyPage() {
    byid("final_page").style.display = "block";
    byid("question").style.display = "none";
    byid("scorecontainer").style.display = "none";
    byid("next").style.display = "none";
    byid('go-to-review').style.display = 'inline';
}
// Delete the scenario currently being displayed.
function viewCurrentScenario() {
    byid("q" + scenarioNum).style.display = "block";
    byid("slides" + scenarioNum).style.display = "block";
}
// Reveals the scenario after the current one being displayed. Either
// creates a new scenario or makes one visible if it has already been 
// created. 
function callNextScenario() {
    var element = byid(("q" + scenarioNum));
    if (typeof (element) != "undefined" && element != null) {
        // Then the scenario has already been created.
        viewCurrentScenario();
    }
    else {
        console.log(scenarioNum)
        // Create a new scenario if one is needed.
        http_get('/oldget/' + parent_id +'/'+scenarioNum ,writetopage, scenarioNum);
    }
}
// Changes the page from the final survey page to the initial surveys
// involving the different scenarios.
function navigateBackToSurvey() {
    byid("final_page").style.display = "none";
    byid("question").style.display = "block";
    byid("scorecontainer").style.display = "block";
    byid("next").innerHTML = "Next";
    byid("next").style.display = "inline";
    byid("go-to-review").style.display = "none";
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
// Creates the final page of the scenario. 
function makeFinalPage(data) {
    var element = byid("final_page");
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
// Completely clears the page, leaving the submit button (which submits
// the POST request)
function clearPage() {
    byid("final_page").style.display = "none";
    byid("prev").style.display = "none";
    byid("go-to-review").style.display = "none";
    byid("question").style.display = "none";
    byid("scorecontainer").style.display = "none";
    byid("submit").style.display = "inline";
    for (let i = 0; i < maxScenarios; i++) {
        byid("q" + i).style.display = "none";
        byid("slides" + i).style.display = "none";
        byid("scorecontainer").style.display = "none";
    }
}
function viewReviewPage() {
    clearPage();
    let element = byid("review_page");
    element.style.display = 'block';
    if (byid("review0") != null) {
        for (let i = 0; i < maxScenarios; i++) {
            element.removeChild(byid("review" + i));
        }
    }
    sortFeatures();
    for (let i = 0; i < maxScenarios; i++) {
        let currentQuestion = totalData[i];
        let div = make("div", "review" + i);
        div.className = "review_div";
        let p = make("p", "prompt");
        div.appendChild(p);
        p.innerHTML = "Prompt: " + byid('rule_prompt').innerHTML;
        
        if(isgen){
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
        } else {
            let table = make('table', 'q' + i + "review");
            headrow = table.createTHead().insertRow()
            headrow.insertCell().innerHTML = 'Options'
            headrow.insertCell().innerHTML = 'Scores'
            scos = grabscores()
            for(j=0;j<totalData[i].length;j++){
                let row = table.insertRow();
                row.insertCell().innerHTML = totalData[i][j]
                row.insertCell().innerHTML = scos[i][j]
            }
            div.appendChild(table)
        }


        let button_div = make("div");
        button_div.className = "review_button";
        let button = make("button", i + "review_button");
        button.innerHTML = "Modify Anwser";
        button.className = 'action-btn'
        button.onclick = function (i) {
            backToPage(parseInt(i.target.id));
        };
        button_div.appendChild(button);
        div.appendChild(button_div);
        element.appendChild(div);
    }
    featuresAsString();
    console.log(dataFeatures);
}
function backToPage(pageNum) {
    byid("review_page").style.display = "none";
    byid("submit").style.display = "none";
    byid("go-to-review").style.display = "inline";
    byid("question").style.display = "block";
    byid("q" + pageNum).style.display = "block";
    byid("slides" + pageNum).style.display = "block";
    byid("scorecontainer").style.display = "block";
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
        byid("prev").setAttribute("disabled", "true");
    }
    else {
        byid("prev").removeAttribute("disabled");
    }
}
// Handles how the user visits the "next page". Involves generating new 
// surveys and displaying the survey-results page and the final-page.
function next() {
    clearCurrentScenario();
    scenarioNum++;
    // Has the user finished the first part of the survey?
    if (scenarioNum == maxScenarios) {
        if(isgen){
            viewFinalSurveyPage();
        }else{
            viewReviewPage();
            byid("next").style.display = "none";
        }
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
// Grabs the user's scores from the survey scenarios.
function grabscores() {
    let scores = [];
    for (let s in totalData) {
        let one_scen = [];
        for (let j of totalData[s].keys()) {
            var sco = byid('q' + s + 'range' + j).value;
            // console.log(sco)
            one_scen.push(sco);
        }
        scores.push(one_scen);
    }
    return scores;
}
// Submits the original scenarios, the user's option 
// scores for each scenario, and the user's scores 
// for each feature. 
function submitResult() {
    var scores = grabscores();
    http_post('submitsurvey', 
                {'survey_data':totalData, 'scores':scores,'parent_id':parent_id}, 
                true);
}
function printstuff(dat, arg) {
    console.log(dat);
}
function featuresAsString() {
    console.log(dataFeatures[i].key);
    for (var i = 0; i < dataFeatures.length; i++) {
        dataFeatures[i].value = dataFeatures[i].value.toString();
    }
}
// initial Take Survey Page
var scenarioNum = 0;
var maxScenarios = Number(byid('maxlen').innerHTML)
var data = [];
var dataFeatures = [];
var totalData = [];
var parent_id = byid('parent_id').innerHTML;
var isgen = byid('is_gen').innerHTML === "True"
http_get('/oldget/' + parent_id+'/0', writetopage, scenarioNum);
//# sourceMappingURL=surveyscript.js.map