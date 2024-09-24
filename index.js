const express = require("express")
const app = express()
const path = require("path");
const ejsMate = require("ejs-mate")

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.urlencoded({ extended: true }));

app.engine("ejs", ejsMate)
app.use(express.static(path.join(__dirname, "/public")))


const { spawn } = require('child_process');


const port = 8080;


app.get("/",(req,res)=>{
    let url = "";
    res.render("index.ejs",{url})
})
app.post("/generateQR",async(req,res)=>{
    let url = req.body.url
    const pythonProcess = await spawn('python', ['generator.py', "http://"+url]);
    await pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
    });

    await pythonProcess.stderr.on('data', (data) => {
    console.error(data.toString());
    });

    await pythonProcess.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    });

    url = "https://qr-code-generator1.s3.eu-north-1.amazonaws.com/"+url+".png"
    console.log(url)
    res.render("index.ejs",{url});

})
app.listen(port,()=>{
    console.log("server");
})

