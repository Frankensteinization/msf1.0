let express = require("express");
let app = express();
let fs = require("fs");

const { spawn } = require("child_process");

let http = require("http").createServer(app);
let io = require("socket.io")(http);

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});

io.on("connection", function(socket) {
    console.log("a user connected");
    try {
        socket.on("disconnect", function() {
            console.log("user disconnected");
        });
    
        // 运行传回的代码
        let subProcess;
        socket.on("run code", function(msg) {
            subProcess = runPython(socket, msg);
        });
    
        socket.on("code input", function(msg) {
            subProcess.stdin.write(msg + "\n");
        });
    }catch(e){
        console.log(e)
    }
    
});

http.listen(3000, function() {
    console.log("listening on *:3000");
});

function runPython(socket, code) {
    let fileName = "main.py"; // todo 换成随机文件名
    fs.writeFileSync(fileName, code, "utf8");

    let subProcess = spawn("python", [fileName], { cmd: __dirname });

    // 监听子进程是否运行完毕
    subProcess.on("close", code => {
        console.log("Python程序已结束");
    });

    subProcess.stdout.on("data", onData);
    subProcess.stderr.on("data", onData);

    function onData(data) {
        socket.emit("stdout", data.toString());
    }

    // 接收前端发送的输入，并将输入发送给Python子进程
    socket.on("input", function(input) {
        subProcess.stdin.write(input + "\n");
    });

    return subProcess;
}
