const axios = require('axios');

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method Not Allowed' }),
    };
  }

  try {
    const { url, name } = JSON.parse(event.body);

    await axios.post('https://hooks.slack.com/services/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', {
      text: `${url} is requested to be scraped by ${name}`,
      blocks: [
        {
          type: "section",
          text: {
            type: "mrkdwn",
            text: `*New Scraping Request*\n\n*URL:* ${url}\n*Requested by:* ${name}`
          }
        }
      ]
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true }),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Slack notification failed',
        details: error.message
      }),
    };
  }
};
