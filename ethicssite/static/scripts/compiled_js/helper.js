// This is the helper class for some functions that we will all have to use.
// works the same as document.getElementById
// I want to change this area here, so instead of appending it to the page, it will just add it to the page.
function addsurveytopage(element, index) {
    document.getElementById("survey").append(element);
}
function addsliderstopage(i) {
    var element = document.createElement('div');
    element.id = "slides" + scenarioNum;
    for (var j = 0; j < i; j++) {
        element.append(makeslider(String((j + 1))));
    }
    document.getElementById("scorecontainer").append(element);
}
function make(tag, id) {
    let item = document.createElement(tag);
    item.id = id;
    return item;
}
function byid(id) {
    return document.getElementById(id);
}
// Delete the scenario currently being displayed.
function clearCurrentScenario() {
    document.getElementById("q" + scenarioNum).style.display = "none";
    document.getElementById("slides" + scenarioNum).style.display = "none";
}
// View the final page of the survey (the page before the survey results)
function viewFinalSurveyPage() {
    document.getElementById("final_page").style.display = "block";
    document.getElementById("question").style.display = "none";
    document.getElementById("scorecontainer").style.display = "none";
    document.getElementById("next").style.display = "none";
    document.getElementById("go-to-review").style.display = "inline";
}

// Delete the scenario currently being displayed.
function viewCurrentScenario() {
    document.getElementById("q" + scenarioNum).style.display = "block";
    document.getElementById("slides" + scenarioNum).style.display = "block";
}
// Reveals the scenario after the current one being displayed. Either
// creates a new scenario or makes one visible if it has already been 
// created. 
function callNextScenario() {
    var element = document.getElementById(("q" + scenarioNum));
    if (typeof (element) != "undefined" && element != null) {
        // Then the scenario has already been created.
        viewCurrentScenario();
    }
    else {
        // Create a new scenario if one is needed.
        http('getscenario', writetopage, scenarioNum);
    }
}
// Changes the page from the final survey page to the initial surveys
// involving the different scenarios.
function navigateBackToSurvey() {
    document.getElementById("final_page").style.display = "none";
    document.getElementById("question").style.display = "block";
    document.getElementById("scorecontainer").style.display = "block";
    document.getElementById("next").innerHTML = "Next";
    document.getElementById("next").style.display = "inline";
    document.getElementById("go-to-review").style.display = "none";
}
// method for interacting with the python server.
// args should look like this: (fill in as we go)
function http(endpoint, func, args) {
    let reply = [];
    var resp = fetch(endpoint)
        .then(r => r.json())
        .then(rd => func(rd, args));
    // .then(rr=> reply = rr)
    // console.log(reply)
    return reply;
}
//# sourceMappingURL=helper.js.map