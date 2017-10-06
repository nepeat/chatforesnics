import React from 'react';

import { withRouter } from 'react-router';
import { connect } from 'react-redux';

import { getChatsByList } from '../reducers/chats';

import ChatList from '../components/ChatList';

const ChatListContainer = ({ chats }) => {
  return <ChatList chats={chats}/>;
};

const mapStateToProps = state => ({
  chats: getChatsByList(state)
});

export default withRouter(connect(
  mapStateToProps
)(ChatListContainer));
