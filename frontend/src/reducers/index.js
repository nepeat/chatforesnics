import { combineReducers } from 'redux';
import chats, * as fromChats from './chats';
import messages, * as fromMessages from './messages';

export default combineReducers({
  chats,
  messages
});
