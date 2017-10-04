import React from 'react';

import './message.css';

export default ({ message, senderChange, lastSender }) => {
  let prependedExtras = [];

  if (senderChange) {
    prependedExtras.push(<h1 className='sender'>{lastSender}</h1>);
  }

  return <div className='message'>
    {prependedExtras}
    <span className='created'>{message.created}</span>
    <span className='content'>{message.content}</span>
  </div>;
};
