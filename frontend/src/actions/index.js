import * as types from '../constants/ActionTypes'

// Chats
const receiveChats = chats => ({
  type: types.RECIEVE_CHATS,
  chats
});

export const getChats = () => dispatch => {
  let dataRequest = new Request("http://localhost:5000/api/chats/", {
    mode: 'cors'
  });

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveChats(response.chats));
  });
}

// Messages
const receiveMessages = messages => ({
  type: types.RECIEVE_MESSAGES,
  messages
});

export const getMessages = (chat_id) => dispatch => {
  let dataRequest = new Request("http://localhost:5000/api/chats/" + chat_id, {
    mode: 'cors'
  });

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveMessages(response.messages));
  });
}
