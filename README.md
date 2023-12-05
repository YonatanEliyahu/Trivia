# Trivia Game

This project is a Trivia game implemented in Python using the TCP protocol. It consists of a server and a client. The
server manages user authentication, scores, and trivia questions, while the client provides the interface for users to
interact with the game.

## Server

### Features

- Socket-based communication
- User authentication
- Sign-up option
- Score tracking
- Trivia questions
- Dynamic question loading from an external API
- Server management commands for real-time control

### Technologies Used

- Python
- Threading
- Socket programming for networking
- SQLite for database storage
- API integration for dynamic question loading

### User Class

The `User` class represents a user in the Trivia Game. It includes attributes such as `username`, `password`, `score`, and a list of `questions_asked`. This class is designed using object-oriented principles to encapsulate user-related functionalities.



### Question Class

The `Question` class represents a trivia question in the game. It includes attributes such as `question`, `answers`, and `correct`. This class encapsulates question-related functionalities and supports the game's dynamic question loading from an external API.

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/YonatanEliyahu/Trivia.git
   ```
   
2. install requests library:

   ```bash
   pip install requests
   ```

3. Run the server:

   ```bash
   python server_TCP.py
   ```

   The server will start listening for incoming connections.

## Server Management Commands

The server includes a real-time management console for handling various operations. Here are the available commands:

- load: Load more trivia questions from an external API and add them to the database.
- kick: Kick a specific user out of the server.
- shutdown: Initiate a graceful shutdown of the server.

To use these commands, enter the desired command when prompted by
the server management console.

## Client

### Features

- User authentication
- Score checking
- High score viewing
- Trivia participation
-
    - Sign-up option

### Technologies Used

- Python
- Socket programming for networking

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/YonatanEliyahu/Trivia.git
   ```

2. Run the client:

   ```bash
   python client_TCP.py
   ```

   ## Communication Protocol

The Trivia application uses a custom communication protocol between the server and clients. This protocol ensures
seamless interaction and data exchange during the trivia game. Below is an overview of the key messages and their
meanings:

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
    - *Server to Client:* Responds with the high score table containing usernames and scores.

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

Please refer to the protocol definitions in the source code at (.\chatlib\chatlib_README.md)  for more technical details.

   Follow the on-screen instructions to log in, check scores, view high scores, and play trivia.

## Contributors

- [Yonatan Eliyahu](https://github.com/YonatanEliyahu)

## License

This project is licensed under the [MIT License](LICENSE).
