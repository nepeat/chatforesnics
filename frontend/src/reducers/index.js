import { combineReducers } from 'redux';
import chats, * as fromChats from './chats';
import chatusers, * as fromChatUsers from './chatusers';
import messages, * as fromMessages from './messages';

export default combineReducers({
  chats,
  chatusers,
  messages
});
