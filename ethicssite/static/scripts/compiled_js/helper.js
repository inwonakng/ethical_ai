// This is the helper class for some functions that we will all have to use.
// works the same as document.getElementById
// I want to change this area here, so instead of appending it to the page, it will just add it to the page.
function addtopage(element) {
    document.getElementById("survey").append(element);
}
function make(tag, id) {
    let item = document.createElement(tag);
    item.id = id;
    return item;
}
function byid(id) {
    return document.getElementById(id);
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