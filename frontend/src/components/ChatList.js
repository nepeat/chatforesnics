import React, { PureComponent } from 'react';

import ReactTable from 'react-table';
import { withRouter } from 'react-router';

const ChatList = ({ chats, history }) => {
  if (!chats || chats.length === 0) {
    return <h1>Loading</h1>;
  }

  return (
    <div className='chats'>
      <ReactTable
        data={chats}
        columns={[
          {
            Header: 'ID',
            accessor: 'id'
          },
          {
            Header: 'Name',
            accessor: 'name'
          },
          {
            Header: 'Messages',
            accessor: 'messages'
          },
          {
            Header: 'Created',
            accessor: 'created'
          }
        ]}
        getTrProps={(state, rowInfo, column, instance) => {
          return {
            onClick: (e, handleOriginal) => {
              if (handleOriginal) {
                return handleOriginal();
              }
              history.push('/chat/' + rowInfo.original.id);
            }
          };
        }}
      />;
    </div>
  );
};

export default withRouter(ChatList);
