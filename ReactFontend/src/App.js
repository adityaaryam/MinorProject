import React from "react";
import axios from "axios";
import { useState } from "react";
import {Buffer} from 'buffer';
import loader from '../src/loader.gif'

export default function App() {

  const [isRes,setIsRes]=useState(null);
  const [imgsrc,setImgSrc]=useState();
  function processImage(e) {

    var inputElement = document.getElementById('imageInput');
    var resultElement = document.getElementById('result');
    var file = inputElement.files[0];

    if (file) {
      setIsRes(-1);

      const form = new FormData();
      form.append('file',file);
        // console.log(file);
        axios
          .post("http://localhost:5000/process", form, { 
          headers: {
              "Content-Type": "multipart/form-data",
          },
          })
          .then((res) => {
              setIsRes(res.data.msg);
              setImgSrc("data:image/jpg;base64,"+Buffer.from(res.data.imgData).toString('base64'));         
          })
          .catch((err) => {
          if(err)console.log(err);
          });

    } else {
        resultElement.innerHTML = 'Please select an image.';
    }

  }
  return (
    <>
      <h1>{`Crowd Detection`}</h1>
      <input type="file" id="imageInput" accept="image/*"></input>
      <button  onClick={processImage}>process Image</button>
      <div id="result">
        <img className={isRes!=-1?'hide':''} src={loader} width={`400px`}></img>
        <h3 className={(isRes==null || isRes==-1)? 'hide':''}>No. of crowds = {isRes}</h3>
        <img src={imgsrc}></img>
      </div>

    </>
  );
}
