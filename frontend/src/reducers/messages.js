import { combineReducers } from 'redux';

import {
  RECIEVE_MESSAGES
} from '../constants/ActionTypes'

const initialState = [];

const messages = (state = initialState, action) => {
  switch (action.type) {
    case RECIEVE_MESSAGES:
      return action.messages;
    default:
      return state;
  }
}

export default messages;
