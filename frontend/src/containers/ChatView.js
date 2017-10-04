import React, { PureComponent } from 'react';

import ReactTable from "react-table";
import { withRouter } from 'react-router';
import { connect } from 'react-redux';

import { getMessages } from '../actions';

import Message from '../components/message.js'

class ChatView extends PureComponent {
  componentWillMount() {
    this.props.getMessages(this.props.match.params.chat_id);
  }

  render() {
    if (this.props.messages.length === 0) {
      return <h1>Loading</h1>;
    }
    
    let lastSender;
    let senderChange = false;

    return (
      <div className='messages'>
        {this.props.messages.map((message) => {
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

const mapStateToProps = state => state;

export default withRouter(connect(
  mapStateToProps,
  { getMessages }
)(ChatView));
