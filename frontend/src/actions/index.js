import * as types from '../constants/ActionTypes';

// Chats
const receiveChats = chats => ({
  type: types.RECIEVE_CHATS,
  chats
});

export const getChats = () => dispatch => {
  let dataRequest = new Request('/api/chats/');

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveChats(response.chats));
  });
};

// Messages
const receiveMessages = messages => ({
  type: types.RECIEVE_MESSAGES,
  messages
});

export const getMessages = (chatid) => dispatch => {
  let dataRequest = new Request('/api/chats/' + chatid);

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveMessages(response.messages));
  });
};
