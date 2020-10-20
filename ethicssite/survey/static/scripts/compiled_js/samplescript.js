// this is the function that will be passed along with the request. 
// Every function that goes through the 'http' function should expect one data object.
function writetopage(data) {
    let question = make('div', 'q0');
    for (let i = 0; i < data.length; i++) {
        let oneq = make('a', 'scenario' + i);
        //right now i'm just printing the json, so could use the conversion functaion to table here
        oneq.innerHTML = JSON.stringify(data[i]) + '<br><br>'; //for viewing pleasure
        question.appendChild(oneq);
    }
    addtopage(question);
}
// testing grabbing generated survey scenario
http('getscenario', writetopage);
//# sourceMappingURL=samplescript.js.map