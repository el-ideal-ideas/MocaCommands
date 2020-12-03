// *** This script will be reload automatically. So you can change your response dynamically.***
// *** dynamic-js-route is too slow. dynamic-python-route is fast.***
// the value at the end of this file will be return to client as a response.


const data = 'This is a sample data';
const end = ['!', '?', '.', '!!', '!?'];

// This value will be return as response.
// response type can be number, string, array, dictionary, boolean.
const response = {
    // type: 'number',
    // data: Math.random(),

    type: 'string',
    data: data + end[Math.floor(Math.random() * end.length)],

    // type: 'array',
    // data: end,

    // type: 'dictionary',
    // data: {a: 1, b: 2, c: 3, d: [1,2,3,4]},

    // type: 'boolean',
    // data: false,
}