// this is the function that will be passed along with the request. 
// Every function that goes through the 'http' function should expect one data object and one packed object of arguments it can use.
function writetopage(data:Array<JSON>,args:any){
    let question = make('div','q'+args)
    let table = maketable(data,args)
    question.appendChild(table)
    // for(let i=0;i<data.length;i++){
    //     let oneq = make('a','scenario'+i)

    //     //right now i'm just printing the json, so could use the conversion functaion to table here
    //     oneq.innerHTML = JSON.stringify(data[i]) + '<br><br>' //for viewing pleasure
    //     question.appendChild(oneq)
    // }
    addtopage(question)
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

// testing grabbing generated survey scenario
http('getscenario',writetopage,0)
//http('getscenario',writetopage,1)
