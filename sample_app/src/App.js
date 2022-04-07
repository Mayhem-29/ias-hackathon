import './App.css';
import React, {Component} from 'react';
import axios from 'axios';

import {imageData} from "./data" 
export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      createdAt: "",
      success: false,
      fetched:false,
      loading: false,
      img_no: "0.jpg",
    }
    this.click = this.click.bind(this);
  }
  componentDidMount(){
    setInterval(() => this.click(),2000);
  }
  
  click() {
    const str = "ting ting ting";
    this.setState({loading:true})

    axios.post("https://reqres.in/api/users/", {name:str})
    .then(res => {
        // console.log(res.data.id);
        // alert(res.data.createdAt);
        
        this.setState({img_no:(res.data.id%10)});
        console.log(this.state.img_no);
        this.setState({success:true,createdAt:res.data.createdAt});
    })
    .catch((error) => {
        console.log(error);
    });

    this.setState({loading:false})
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          {/* <img src={logo} className="App-logo" alt="logo" /> */
          /* <p>
            Edit <code>src/App.js</code> and save to reload.
          </p> */}
        {/* <p>{this.state.createdAt}</p> */}
        <p>{this.state.img_path}</p>
        <img src={imageData[this.state.img_no]} alt={"alt"}/>
            
          {/* <button onClick = {this.click}>Learn React</button> */}
        </header>
      </div>
    );
  }
}

// export default App;
