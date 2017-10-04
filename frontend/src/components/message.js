import React from 'react';

import './message.css';

export default (props) => {
  let prependedExtras = [];

  if (props.senderChange) {
    prependedExtras.push(<h1 className='sender'>{props.lastSender}</h1>)
  }

  return <div className='message'>
    {prependedExtras}
    <span className='created'>{props.message.created}</span>
    <span className='content'>{props.message.content}</span>
  </div>;
}
