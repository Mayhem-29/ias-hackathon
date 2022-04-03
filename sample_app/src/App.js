import './App.css';
import React, {Component} from 'react';
import axios from 'axios';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      createdAt:"",
      success: false,
      fetched:false,
      loading : false
    }
    this.click = this.click.bind(this);
  }
  componentDidMount(){
    setInterval(() => this.click(),5000);
  }
  
  click() {
    // e.preventDefault();
    const str = "ting ting ting";
    this.setState({loading:true})
    // console.log(str)
    axios.post("https://reqres.in/api/users/", {name:str})
    .then(res => {
        console.log(res.data.createdAt);
        // alert(res.data.createdAt);
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
        <p>{this.state.createdAt}</p>
            
          {/* <button onClick = {this.click}>Learn React</button> */}
        </header>
      </div>
    );
  }
}

// export default App;
