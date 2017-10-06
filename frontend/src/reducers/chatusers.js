import { combineReducers } from 'redux';

import {
  RECIEVE_CHAT_USERS
} from '../constants/ActionTypes';

const initialState = {};
const defaultUser = {
  guid: 'UNKNOWN',
  name: 'Unknown'
};

const chatUsers = (state = initialState, action) => {
  switch (action.type) {
    case RECIEVE_CHAT_USERS:
      let newUsers = {};

      action.users.map((user) => {
        newUsers[user.id] = user;
      });

      return {...state, ...newUsers};
    default:
      return state;
  }
};

export default chatUsers;

export const getUser = (state, id) => {
  try {
    return state.chatusers[id] || defaultUser;
  } catch (e) {
    return defaultUser;
  }
};
