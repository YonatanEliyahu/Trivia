# Trivia Game

This project is a Trivia game implemented in Python using the TCP protocol.
It consists of a server and a client.
The server manages user authentication, scores, and trivia questions,
while the client provides the interface for users to interact with the game.

### Comming Up
- Using API to get more questions

## Server

### Features

- Socket-based communication
- User authentication
- Sign-up option
- Score tracking
- Trivia questions


### Technologies Used

- Python
- Threading
- Socket programming for networking
- SQLite for database storage

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/YonatanEliyahu/Trivia.git
   ```

2. Navigate to the server directory:

   ```bash
   cd Trivia/server
   ```

3. Run the server:

   ```bash
   python server_TCP.py
   ```

   The server will start listening for incoming connections.

## Communication Protocol

The Trivia application uses a custom communication protocol between the server and clients. This protocol ensures seamless interaction and data exchange during the trivia game. Below is an overview of the key messages and their meanings:
- **Login Message:**
  - *Client to Server:* Initiates the sign-up process with a new username and password.
  - *Server to Client:* Confirms successful sign-up or notifies of failure.

- **Login Message:**
  - *Client to Server:* Initiates the login process with a username and password.
  - *Server to Client:* Confirms successful login or notifies of login failure.

- **Logout Message:**
  - *Client to Server:* Signals the desire to log out from the server.

- **Get My Score Request:**
  - *Client to Server:* Requests the current user's score.
  - *Server to Client:* Responds with the user's score.

- **Highscore Request:**
  - *Client to Server:* Requests the highscore table.
  - *Server to Client:* Responds with the highscore table containing usernames and scores.

- **Logged Users Request:**
  - *Client to Server:* Requests a list of currently logged-in users.
  - *Server to Client:* Responds with a comma-separated list of usernames.

- **Get Question Message:**
  - *Client to Server:* Requests a trivia question.
  - *Server to Client:* Sends a randomly selected question for the user to answer.

- **Send Answer Message:**
  - *Client to Server:* Submits the user's answer to a trivia question.
  - *Server to Client:* Indicates whether the answer was correct or provides the correct answer in case of an error.

- **Error Message:**
  - *Server to Client:* Informs the client about an error, providing details.

Please refer to the protocol definitions in the source code (.\chatlib\chatlib_README.md)  for more technical details.


## Client

### Features

- User authentication
- Score checking
- High score viewing
- Trivia participation
- - Sign-up option

### Technologies Used

- Python
- Socket programming for networking

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/YonatanEliyahu/Trivia.git
   ```

2. Navigate to the client directory:

   ```bash
   cd Trivia/client
   ```

3. Run the client:

   ```bash
   python client_TCP.py
   ```

   Follow the on-screen instructions to log in, check scores, view high scores, and play trivia.

## Contributors

- [Yonatan Eliyahu](https://github.com/YonatanEliyahu)


## License

This project is licensed under the [MIT License](LICENSE).
