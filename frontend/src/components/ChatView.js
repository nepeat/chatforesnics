import React from 'react';
import Message from './Message';

const ChatView = ({messages}) => {
  if (messages.length === 0) {
    return <h1>Loading</h1>;
  }

  let lastSender;
  let senderChange = false;

  return (
    <div className='messages'>
      {messages.map((message) => {
        if (lastSender !== message.from) {
          lastSender = message.from;
          senderChange = true;
        } else {
          senderChange = false;
        }

        return <Message
          key={'message_' + message.guid}
          message={message}
          lastSender={lastSender}
          senderChange={senderChange}
        />;
      })}
    </div>
  );
};

export default ChatView;
