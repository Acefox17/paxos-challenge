# How to run the server

run the command `python3 message-server.py`, or `python3 PATH_TO_FILE/message-server.py` if you are not in the same directory as the file.

You will need Python 3 installed to run this command

# How to send messages to the server

The server is running on 127.0.0.1:8000, or localhost:8000.

You can send a command such as
`curl -X POST -H "Content-Type: application/json" -d '{"message": "foo"}' http://localhost:8000/messages -v`
to send a message to the server and receive the SHA256 as a hexadecimal value in a JSON object at the "digest" key

You can send a command such as
`curl http://localhost:8000/messages/2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae -v`

to get the message matching the SHA256 hexadecimal value in a JSON object at the "message" key
