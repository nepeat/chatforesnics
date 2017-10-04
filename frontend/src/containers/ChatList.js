import React, { PureComponent } from 'react';

import ReactTable from 'react-table';
import { withRouter } from 'react-router';
import { connect } from 'react-redux';

import { getChats } from '../actions';

class ChatList extends PureComponent {
  componentWillMount () {
    if (this.props.chats.length === 0) {
      this.props.getChats();
    }
  }

  render () {
    if (this.props.chats.length === 0) {
      return <h1>Loading</h1>;
    }

    return (
      <div className='chats'>
        <ReactTable
          data={this.props.chats}
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
                this.props.history.push('/chat/' + rowInfo.original.id);
              }
            };
          }}
        />;
      </div>
    );
  }
}

const mapStateToProps = state => state;

export default withRouter(connect(
  mapStateToProps,
  { getChats }
)(ChatList));
