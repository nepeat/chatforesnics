import React from 'react';
import ReactHighstock from 'react-highcharts/ReactHighstock.src';
import HighchartsMore from 'highcharts-more';
import HighchatsExporting from 'highcharts-exporting';

// Modules
HighchartsMore(ReactHighstock.Highcharts);
HighchatsExporting(ReactHighstock.Highcharts);

const ChatMeta = ({ chat }) => {
  if (!chat.daily) {
    return null;
  }

  let dailyData = [];
  for (let point of chat.daily) {
    dailyData.push([point.time * 1000, point.count]);
  }

  const chartOptions = {
    xAxis: {
      type: 'datetime'
    },
    yAxis: {
      title: {
        text: 'Messages'
      }
    },
    title: {
      text: 'Messages'
    },
    series: [{
      name: 'Messages',
      data: dailyData
    }]
  };

  return (
    <div className='chatmeta'>
      <ReactHighstock config={chartOptions}/>
    </div>
  );
};

export default ChatMeta;
