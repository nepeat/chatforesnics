import React from 'react';

import { withRouter } from 'react-router';
import { connect } from 'react-redux';

import { getUser } from '../reducers/chatusers';

const MessageSender = ({ lastSender, chatuser }) => {
  return <p className='sender' key={'sender_' + lastSender}>{chatuser.name}</p>;
};

const mapStateToProps = (state, ownProps) => ({
  chatuser: getUser(state, ownProps.lastSender)
});

export default withRouter(connect(
  mapStateToProps
)(MessageSender));
