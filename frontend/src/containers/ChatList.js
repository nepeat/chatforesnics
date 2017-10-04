import React, { PureComponent } from 'react';

import ReactTable from "react-table";
import { withRouter } from 'react-router';

class ChatList extends PureComponent {
  constructor() {
    super();

    this.state = {
      chats: []
    };
  }

  componentWillMount() {
    var dataRequest = new Request("http://localhost:5000/api/chats/", {
      mode: 'cors'
    });
    fetch(dataRequest).then((response) => {
      return response.json();
    }).then((response) => {
      this.setState({
        chats: response.chats
      });
    });
  }
  render() {
    if (this.state.chats.length === 0) {
      return <h1>Loading</h1>;
    }

    return (
      <div className='chats'>
        <ReactTable
          data={this.state.chats}
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
            }
          }}
        />;
      </div>
    );
  }
}

export default withRouter(ChatList);
