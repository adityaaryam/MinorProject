const express = require("express");
const cors = require("cors");
const app = express();
const socket = require("socket.io");
const sharp=require('sharp');
const multer = require('multer');
var fs=require('fs');
const FormData = require('form-data');


app.use(cors());
app.use(express.json());
var bodyParser = require('body-parser');
app.use(bodyParser.json({limit: '50mb'}));

app.use(
  bodyParser.urlencoded({
    extended: true,
    limit: '50mb',
    parameterLimit: 70000,
  }),
);
let {PythonShell} = require('python-shell');


const storage = multer.memoryStorage();
const upload = multer({ storage: storage });


const server = app.listen(process.env.PORT || 5000, () =>
  console.log(`Server started on ${process.env.PORT!=undefined? process.env.PORT: 5000}`)
);


app.post("/process", upload.single('file'),function(req,res){
  
  let temp=req.file.buffer;
  temp=Buffer.from(temp);
  fs.writeFile("./0000085_00001_d_0000008.jpg",temp,(err)=>{
        if(err)console.log(err);
  })
  PythonShell.run('crowdDetectionScript.py', null).then(messages=>{

    let dataRet={
      msg:messages[0],
      imgData:fs.readFileSync('./result.jpg')
    }
    res.send(dataRet)
  });

  
  
})