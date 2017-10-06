import React, { PureComponent } from 'react';

import { withRouter } from 'react-router';
import { connect } from 'react-redux';

import { getMessages, getUsers, getChatMeta } from '../actions';
import { getMessagesState } from '../reducers/messages';
import { getChat } from '../reducers/chats';

import ChatMeta from '../components/ChatMeta';
import ChatView from '../components/ChatView';

class ChatViewContainer extends PureComponent {
  componentWillMount () {
    this.props.getUsers(this.props.match.params.chat_id);
    this.props.getMessages(this.props.match.params.chat_id);
    this.props.getChatMeta(this.props.match.params.chat_id);
  }

  render () {
    return (
      <div>
        <ChatMeta chat={this.props.chat}/>
        <ChatView messages={this.props.messages}/>
      </div>
    );
  }
}

const mapStateToProps = (state, ownProps) => ({
  chat: getChat(state, ownProps.match.params.chat_id),
  messages: getMessagesState(state)
});

export default withRouter(connect(
  mapStateToProps,
  { getMessages, getUsers, getChatMeta }
)(ChatViewContainer));
