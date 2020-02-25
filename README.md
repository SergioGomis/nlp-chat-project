# Natural Language Processing

<img src="https://github.com/SergioGomis/nlp-chat-project/blob/master/images/chat.png" width="300">

This repo is a project for developing skills at the Data Analytics bootcamp of Ironhack Madrid by building an API in python with Flask that allows anyone to store and query conversations, messages and users, and analyze their positivity/negativity.


### Requirements and deployment

The project is already deployed at [HEROKU](https://flask-nlp-project.herokuapp.com/) and the data will be stored on my own MongoDB cloud storage.

A step-to-step instructions for the deploy will be given soon.

### Usage API Endpoints

* /user/create/(username)
  * Creates a user
* /users/rand/(qty)
  * Returns a list of <qty> random users from DB
* /chat/create
  * Creates a chat with some users (see examples)
* /chat/(idchat)/adduser
  * Adds an user to a chat
* /chat/(idchat)/addmessage
  * Adds a message to a chat (see examples)
* /chat/(idchat)/list
  * Lists the messages from a chat
* /chat/(idchat)/changename/(newname)
  * Changes the name of an existing chat
* /chat/(idchat)/sentiment
  * Returns sentiment analysis from a chat
* /user/(username)/recommend
  * Recommends the top-3 users to a given user

### Examples

Some examples are provided as Jupyter Notebooks.

Also, the format of the documents in the MongoDB database looks as follows:

<img src="https://github.com/SergioGomis/nlp-chat-project/blob/master/images/user_example.png" width="300">
(user)
<br>
<img src="https://github.com/SergioGomis/nlp-chat-project/blob/master/images/chat_example.png" width="300">
(conversation)





