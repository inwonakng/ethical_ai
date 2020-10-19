// This is the helper class for some functions that we will all have to use.
export class helper {
    // works the same as document.getElementById
    static byid(id) {
        return document.getElementById(id);
    }
    // method for interacting with the python server.
    // args should look like this: (fill in as we go)
    // args = {
    //  endpoint = 'somethingsomething' 
    // }
    static post(args) {
        return fetch(args.endpoint).then(res => res.json());
    }
}
//# sourceMappingURL=helper.js.map