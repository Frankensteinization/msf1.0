let shell = require("shelljs");
let code = `print('hello world')`;

let res = shell.exec(`python -c "${code}"`);
// res.stdout