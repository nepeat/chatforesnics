import { combineReducers } from 'redux';

import {
  RECIEVE_CHATS
} from '../constants/ActionTypes'

const initialState = [];

const chats = (state = initialState, action) => {
  switch (action.type) {
    case RECIEVE_CHATS:
      console.log(action);
      return action.chats;
    default:
      return state;
  }
}

export default chats;
