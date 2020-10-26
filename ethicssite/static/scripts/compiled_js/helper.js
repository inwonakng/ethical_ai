// This is the helper class for some functions that we will all have to use.
// works the same as document.getElementById
function addtopage(element) {
    document.body.append(element);
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