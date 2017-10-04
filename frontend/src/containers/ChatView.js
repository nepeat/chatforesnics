import React, { PureComponent } from 'react';

import ReactTable from "react-table";
import { withRouter } from 'react-router';

import Message from '../components/message.js'

class ChatView extends PureComponent {
  constructor() {
    super();

    this.state = {
      data: []
    };
  }

  componentWillMount() {
    var dataRequest = new Request("http://localhost:5000/api/chats/" + this.props.match.params.chat_id, {
      mode: 'cors'
    });
    fetch(dataRequest).then((response) => {
      return response.json();
    }).then((response) => {
      if (!response.messages) {
        console.error("Could not fetch messages?");
        console.error(response);
        return;
      }

      this.setState({
        data: response.messages
      });
    });
  }
  render() {
    if (this.state.data.length === 0) {
      return <h1>Loading</h1>;
    }
    
    let lastSender;
    let senderChange = false;

    return (
      <div className='messages'>
        {this.state.data.map((message) => {
          if (lastSender !== message.from) {
            lastSender = message.from;
            senderChange = true;
          } else {
            senderChange = false;
          }

          return <Message
            key={'message_pg1_' + message.created + message.content}
            message={message}
            lastSender={lastSender}
            senderChange={senderChange}
          />;
        })}
      </div>
    );
  }
}

export default ChatView;
