# Flask Chatbot App for Zoom

This is a sample Chatbot app using the [Zoom Chatbot Flask App click here for flask installation](https://flask.palletsprojects.com/en/1.1.x/installation/).


To run the completed Chatbot code locally or deploy it to a live server, continue reading below.

## Local/Development Setup

To run the completed Chatbot locally, follow these steps,

1. In terminal:

   `$ git clone https://github.com/saurabhguptaoodles/zoom_chatbot_app.git`

   `$ cd zoom_chatbot_app`

   `$ export FLASK_ENV=development`

   `$ export FLASK_APP=app.py`



2. Add this code to your `.env` file, replacing the `Required` text with your respective [**Development** Zoom Chatbot API credentials](https://marketplace.zoom.us/docs/guides/getting-started/app-types/create-chatbot-app#register).

   ```
   client_id=Required
   client_secret=Required
   zoom_bot_jid=Required
   mongo_url=Required  => To create connection with mongo DB
   ```

3. In terminal:

   `$ flask run` to start the flask App

   `$ ngrok http 5000` ([ngrok turns localhost into live server](https://ngrok.com/) so slash commands and user actions can be sent to your app)

5. Open your ngrok https url in a browser, you should see this,

   `Welcome to the Zoom App....`

6. On your App Marketplace Dashboard, add your ngrok https url to your Whitelist URLs (App Credentials Page), **Development** Redirect URL for OAuth (App Credentials Page), and **Development** Bot Endpoint URL (Features Page). Make sure to match the path after your ngrok https url with the express routes in index.js.

   > In order to click the **Save** button on the Features page when adding a Slash Command and Development Bot Endpoint URL, you have to provide a Production Bot Endpoint URL. Feel free to use https://zoom.us as a placeholder.

   After that, your app is ready to be installed!

7. On your App Marketplace Dashboard, go to the **Local Test** page and click **Install**. After you click the **Authorize** button, you should be taken to your redirect url and see this,

   `Thanks for installing the Vote Chatbot for Zoom!`


8. Now that your Chatbot is installed on your Zoom account, go to a Zoom Chat channel and type,

   `/skeleton set 123456`
   `/skeleton get`
