import React, { Component } from 'react';
import {
  BrowserRouter as Router,
  Route,
  Link
} from 'react-router-dom';

import ChatList from './containers/ChatList.js';
import ChatView from './containers/ChatView.js';

import 'react-table/react-table.css';
import './App.css';

class App extends Component {
  render () {
    return (
      <Router>
        <div className="app">
          <h1>viewapp</h1>
          <Route exact path="/" component={ChatList}/>
          <Route exact path="/chat/:chat_id" component={ChatView}/>
        </div>
      </Router>
    );
  }
}

export default App;
