// This is the helper class for some functions that we will all have to use.
// works the same as byid
// I want to change this area here, so instead of appending it to the page, it will just add it to the page.
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
function http_get(endpoint, func, args) {
    let reply = [];
    var resp = fetch(endpoint)
        .then(r => r.json())
        .then(rd => func(rd, args));
    // .then(rr=> reply = rr)
    // console.log(reply)
    return reply;
}
function http_post(endpoint, data, redirect) {
    let reply = [];
    let fn = function (r) { };
    if (redirect) {
        fn = function (r) {
            // just in case make sure there is an endpoint to redirect to
            if (r.redirected) {
                window.location.href = r.url;
            }
        };
    }
    var resp = fetch(endpoint, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: { 'Content-Type': 'application/json',
            "X-CSRFToken": get_csrf() },
    }).then(r => fn(r));
}
function get_csrf() {
    return document.getElementsByName('csrfmiddlewaretoken')[0].value;
}
//# sourceMappingURL=helper.js.map