import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';

import ChatListContainer from './containers/ChatListContainer.js';
import ChatViewContainer from './containers/ChatViewContainer.js';

import 'purecss';
import 'react-table/react-table.css';
import 'react-vis/dist/style.css';
import './App.css';

class App extends Component {
  render () {
    return (
      <Router>
        <div className="app">
          <h1 className="d-inline"><Link to="/">viewapp</Link></h1>
          <input className="float-right" type="text" placeholder="Shame yourself..."/>
          <Route exact path="/" component={ChatListContainer}/>
          <Route exact path="/chat/:chat_id" component={ChatViewContainer}/>
        </div>
      </Router>
    );
  }
}

export default App;
