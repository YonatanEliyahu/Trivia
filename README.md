# Trivia Game

This project is a Trivia game implemented in Python using the TCP protocol.
It consists of a server and a client.
The server manages user authentication, scores, and trivia questions,
while the client provides the interface for users to interact with the game.

## Server

### Features

- Socket-based communication
- User authentication
- Score tracking
- Trivia questions

### Technologies Used

- Python
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

## Client

### Features

- User authentication
- Score checking
- High score viewing
- Trivia participation

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