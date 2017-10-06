import React from 'react';

import MessageSender from './MessageSender';

import './Message.css';

const Message = ({ message, senderChange, lastSender, _key, dispatch }) => {
  let prependedExtras = [];

  if (senderChange) {
    prependedExtras.push(<MessageSender key={'sender_' + lastSender} lastSender={lastSender}/>);
  }

  return <div className='message' key={_key}>
    {prependedExtras}
    <span className='created'>{message.created}</span>
    <span className='content'>{message.content}</span>
  </div>;
};

export default Message;
