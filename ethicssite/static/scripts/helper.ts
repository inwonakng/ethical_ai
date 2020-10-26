// This is the helper class for some functions that we will all have to use.
// works the same as document.getElementById
// I want to change this area here, so instead of appending it to the page, it will just add it to the page.
function addsurveytopage(element:any){
    document.getElementById("survey").append(element)
}

function addsliderstopage(i:number){
    for(var j=0; j < i; j++){
        document.getElementById("scorecontainer").append(makeslider(String((j+1))));
    }
    
}

function make( tag:string, id?:string){
    let item = document.createElement(tag)
    item.id = id
    return item
}

function byid( id:string ){ 
    return document.getElementById( id )
}

// method for interacting with the python server.
// args should look like this: (fill in as we go)
function http(endpoint:string,func:any,args:any){
    let reply = []
    var resp =  fetch(endpoint)
                .then(r => r.json())
                .then(rd=>func(rd,args))
                // .then(rr=> reply = rr)
    // console.log(reply)
    return reply
}