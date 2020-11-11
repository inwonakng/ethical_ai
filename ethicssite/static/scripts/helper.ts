// This is the helper class for some functions that we will all have to use.
// works the same as byid
// I want to change this area here, so instead of appending it to the page, it will just add it to the page.

// Creates a 'tag' element with the id provided.
function make( tag:string, id?:string){
    let item = document.createElement(tag)
    item.id = id
    return item
}

// An intuitive way to grab an element by the id given
function byid( id:string ){ 
    return document.getElementById( id )
}

// method for interacting with the python server.
// args should look like this: (fill in as we go)
function http_get(endpoint:string,func:any,args:any){
    let reply = []
    var resp =  fetch(endpoint)
                .then(r => r.json())
                .then(rd=>func(rd,args))
                // .then(rr=> reply = rr)
    // console.log(reply)
    return reply
}

// Forms a POST request. Used to transfer data from front-end 
// to the endpoint specifiec in the back-end using the provided
// models.
function http_post(endpoint:string,data:any,redirect:boolean){
    let reply = []
    let fn = function(r){}
    if(redirect){
        fn = function(r){
            // just in case make sure there is an endpoint to redirect to
            if(r.redirected){
                window.location.href = r.url
            }
        }
    }
    var resp =  fetch(endpoint,{
                    method:'POST',
                    body:JSON.stringify(data),
                    headers:{'Content-Type':'application/json',
                    "X-CSRFToken": get_csrf()},
                }).then(r => fn(r)
            )
}

// Gets the value of the token csrf.
function get_csrf(){
    return (document.getElementsByName('csrfmiddlewaretoken')[0] as HTMLInputElement).value
}
