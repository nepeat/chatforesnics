import { combineReducers } from 'redux';

import {
  RECIEVE_CHATS,
  UPDATE_CHAT_DATA
} from '../constants/ActionTypes';

const defaultChat = {
  id: 'UNKNOWN',
  name: 'UNKNOWN',
  date: 'UNKNOWN',
  messages: 0
};

const chats = (state = {}, action) => {
  let stateDelta = {};

  switch (action.type) {
    case RECIEVE_CHATS:
      Object.keys(action.chats).map((key, index) => {
        let chatID = action.chats[key].id;
        stateDelta[chatID] = {...state[chatID], ...action.chats[key]};
      });

      return {...state, ...stateDelta};
    case UPDATE_CHAT_DATA:
      stateDelta[action.chatid] = {...state[action.chatid], ...action.data};
      return {...state, ...stateDelta};
    default:
      return state;
  }
};

export default chats;

export const getChat = (state, id) => {
  try {
    return state.chats[id] || defaultChat;
  } catch (e) {
    return defaultChat;
  }
};


export const getChatsById = (state) => {
  return state.chats;
};

export const getChatsByList = (state) => {
  var chatList = [];
  Object.keys(state.chats).map((key, index) => {
    chatList.push(state.chats[key]);
  });
  return chatList;
};
