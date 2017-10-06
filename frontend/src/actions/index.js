import * as types from '../constants/ActionTypes';

// Chats
const receiveChats = chats => ({
  type: types.RECIEVE_CHATS,
  chats
});

const receiveChatData = (chatid, data) => ({
  type: types.UPDATE_CHAT_DATA,
  chatid: chatid,
  data: data
});

export const getChats = () => dispatch => {
  let dataRequest = new Request('/api/chats/');

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveChats(response.chats));
  });
};

export const getChatMeta = (chatid) => dispatch => {
  let dataRequest = new Request('/api/chats/' + chatid + '/daily');

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveChatData(chatid, {
      daily: response.data
    }));
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

// Users
const receiveUsers = users => ({
  type: types.RECIEVE_CHAT_USERS,
  users
});

export const getUsers = (chatid) => dispatch => {
  let dataRequest = new Request('/api/chats/' + chatid + '/users');

  fetch(dataRequest).then((response) => {
    return response.json();
  }).then((response) => {
    dispatch(receiveUsers(response.users));
  });
};
