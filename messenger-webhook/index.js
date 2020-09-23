'use strict';
require('dotenv').config();
// the length of the productivity "block", in milliseconds
// const BLOCK_LENGTH = 600000;
const BLOCK_LENGTH = 10000; // just for fun (and testing,) poll me every 10 seconds
//TODO: allow user to input their own activities throught the Messenger UI (not hardcoded)
const ACTIVTIES = ['Projects', 'Social Time', 'Eating', 'Exercise', 'Misc.']
const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;
// Imports dependencies and set up http server
const
request = require('request'),
express = require('express'),
body_parser = require('body-parser'),
app = express().use(body_parser.json()); // creates express http server
const AWS = require('aws-sdk');
const ddb = new AWS.DynamoDB.DocumentClient(({apiVersion: '2012-08-10', region: 'us-east-1'}))

//TODO: support multiple users of this app 😅
let interval;
// Sets server port and logs message on success
app.listen(process.env.PORT || 1337, () => console.log('webhook is listening'));

// Accepts POST requests at /webhook endpoint
app.post('/webhook', (req, res) => {

  // Parse the request body from the POST
  let body = req.body;

  // Check the webhook event is from a Page subscription
  if (body.object === 'page') {

    body.entry.forEach(function(entry) {

      // Gets the body of the webhook event
      let webhook_event = entry.messaging[0];
      console.log(webhook_event);


      // Get the sender PSID
      let sender_psid = webhook_event.sender.id;
      console.log('Sender ID: ' + sender_psid);

      // Check if the event is a message or postback and
      // pass the event to the appropriate handler function
      if (webhook_event.message) {
        handleMessage(sender_psid, webhook_event.message);
      } else if (webhook_event.postback) {

        handlePostback(sender_psid, webhook_event.postback);
      }

    });
    // Return a '200 OK' response to all events
    res.status(200).send('EVENT_RECEIVED');

  } else {
    // Return a '404 Not Found' if event is not from a page subscription
    res.sendStatus(404);
  }

});

// Accepts GET requests at the /webhook endpoint
app.get('/webhook', (req, res) => {

  /** UPDATE YOUR VERIFY TOKEN **/
  const VERIFY_TOKEN = "rUyvRxf2R6Y";

  // Parse params from the webhook verification request
  let mode = req.query['hub.mode'];
  let token = req.query['hub.verify_token'];
  let challenge = req.query['hub.challenge'];

  // Check if a token and mode were sent
  if (mode && token) {

    // Check the mode and token sent are correct
    if (mode === 'subscribe' && token === VERIFY_TOKEN) {

      // Respond with 200 OK and challenge token from the request
      console.log('WEBHOOK_VERIFIED');
      res.status(200).send(challenge);

    } else {
      // Responds with '403 Forbidden' if verify tokens do not match
      res.sendStatus(403);
    }
  }
});

function handleMessage(sender_psid, received_message) {
  const questionResponse = {
    "text": "What are you doing?",
    "quick_replies": ACTIVTIES.map(activity => ({
      "content_type": "text",
      "title": activity,
      "payload": activity
    }))
  };
  // Checks if the message contains text
  if (received_message.quick_reply) {
    const activity = received_message.quick_reply.payload;
    addActivityToDatabase(activity);
    interval = setTimeout(() => callSendAPI(sender_psid, questionResponse), BLOCK_LENGTH)
  } else if (received_message.text) {
    // Create the payload for a basic text message, which
    // will be added to the body of our request to the Send API
    if (!interval) {
      callSendAPI(sender_psid, questionResponse)
    } else if (received_message.text === "clear") {
      interval = clearTimeout(interval);
    }
  }
}

function addActivityToDatabase(activity) {
  const timestamp = new Date().toISOString();
  var params = {
    TableName : "100-blocks-table",
    Item: {
      activity,
      timestamp
    }
  };
  ddb.put(params, function(err, data) {
    if (err) console.log(err);
    else {
      console.log('Successfully put data in DynamoDB!')
      console.log(data);
    }
  });
}

function handlePostback(sender_psid, received_postback) {
  console.log('ok')
  let response;
  // Get the payload for the postback
  let payload = received_postback.payload;

  // Set the response based on the postback payload
  response = { "text": `Got the payload ${payload} from you!` }
  // if (payload === 'yes') {
  //   response = { "text": "Thanks!" }
  // } else if (payload === 'no') {
  //   response = { "text": "Oops, try sending another image." }
  // }
  // Send the message to acknowledge the postback
  callSendAPI(sender_psid, response);
}

function callSendAPI(sender_psid, response) {
  // Construct the message body
  let request_body = {
    "recipient": {
      "id": sender_psid
    },
    "message": response
  }

  // Send the HTTP request to the Messenger Platform
  request({
    "uri": "https://graph.facebook.com/v2.6/me/messages",
    "qs": { "access_token": PAGE_ACCESS_TOKEN },
    "method": "POST",
    "json": request_body
  }, (err, res, body) => {
    if (!err) {
      console.log('message sent!')
    } else {
      console.error("Unable to send message:" + err);
    }
  });
}
