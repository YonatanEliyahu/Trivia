# Protocol Documentation

## Overview

The protocol operates over TCP on a specified port (choose your port; we'll use 5678).

### Message Format

```
CCCCCCCCCCCCCCCC|LLLL | MMM
```

- **C**: 16 characters representing the command type.
- **|**: Separator between message parts (required).
- **L**: A 4-character field indicating the length of the following message (M). Values range from 0000 to 9999 (negative values are invalid).
- **|**: Separator between message parts (required).
- **M**: Information represented by characters, varying based on the message.

## Messages

### Client to Server (Client -> Server)

#### LOGIN

Request for user login.

**Message Structure**: `LOGIN |UUUU#PPP`

- **UUUU**: Username.
- **#**: Separator.
- **PPP**: Password.

Example:
```plaintext
LOGIN           |0009|aaaa#bbbb
```

#### LOGOUT

Logout from the server.

**Message Structure**: `LOGOUT |0000|`

Example:
```plaintext
LOGOUT          |0000|
```

#### LOGGED

Receive a list of users currently connected to the game.

**Message Structure**: `LOGGED |0000|`

Example:
```plaintext
LOGGED          |0000|
```

#### GET_QUESTION

Request for a trivia question from the server.

**Message Structure**: `GET_QUESTION |0000|`

Example:
```plaintext
GET_QUESTION    |0000|
```

#### SEND_ANSWER

Send an answer to a trivia question.

**Message Structure**: `SEND_ANSWER |id#choice`

- **id**: Question ID.
- **#**: Separator.
- **choice**: Chosen answer (1 to 4).

Example:
```plaintext
SEND_ANSWER     |0003|2#4
```

#### MY_SCORE

Request for the current user's score.

**Message Structure**: `MY_SCORE |0000|`

Example:
```plaintext
MY_SCORE        |0000|
```

#### HIGHSCORE

Request for the highest scores table.

**Message Structure**: `HIGHSCORE |0000|`

Example:
```plaintext
HIGHSCORE       |0000|
```

### Server to Client (Server -> Client)

#### LOGIN_OK

Response to LOGIN indicating successful login.

**Message Structure**: `LOGIN_OK |0000|`

Example:
```plaintext
LOGIN_OK        |0000|
```

#### LOGGED_ANSWER

Response to LOGGED, includes a list of currently connected users.

**Message Structure**: `LOGGED_ANSWER |UUUU#UUUU`

- **UUUU**: Usernames, separated by ','.

Example:
```plaintext
LOGGED_ANSWER   |0012|user1, user2
```

#### YOUR_QUESTION

Response to GET_QUESTION, sends a trivia question to the user.

**Message Structure**: `YOUR_QUESTION |id#question#answer1#answer2#answer3#answer4`

- **id**: Question ID.
- **#**: Separator.
- **question**: Question text.
- **answer1-answer4**: Possible answers.

Example:
```plaintext
YOUR_QUESTION   |0026|2#How much is 1+1?#5#6#7#2
```

#### CORRECT_ANSWER

Response to SEND_ANSWER, indicates a correct answer.

**Message Structure**: `CORRECT_ANSWER |0000|`

Example:
```plaintext
CORRECT_ANSWER  |0000|
```

#### WRONG_ANSWER

Response to SEND_ANSWER, indicates an incorrect answer.

**Message Structure**: `WRONG_ANSWER |answer`

- **answer**: Correct answer number.

Example:
```plaintext
WRONG_ANSWER    |0001|2
```

#### YOUR_SCORE

Response to MY_SCORE, sends the current user's score.

**Message Structure**: `YOUR_SCORE |score`

- **score**: User's current score.

Example:
```plaintext
YOUR_SCORE      |0001|5
```

#### ALL_SCORE

Response to HIGHSCORE, sends a table of users with their scores.

**Message Structure**: `ALL_SCORE |...user1: score1\nuser2: score2\n`

- **user1**: Username.
- **score1**: User's score.
- **\n**: Separator between scores.

Example:
```plaintext
ALL_SCORE       |0047|bambababy: 5\nabc: 0\ntest: 0\nadmin: 0\nblabla: 0
```

#### ERROR

Error message. When received, the connection is expected to disconnect.

**Message Structure**: `ERROR |error_msg`

- **error_msg**: Description of the error.

Example:
```plaintext
ERROR           |0014|Error Occured!
```

#### NO_QUESTIONS

Response to GET_QUESTION when no more questions are available (GAME OVER).

**Message Structure**: `NO_QUESTIONS |0000|`

Example:
```plaintext
NO_QUESTIONS     |0000|
```

## Protocol States

### Disconnected

No communication between the client and server.

### Connected

Client's socket is connected to the server, but the client is not yet logged in.

- The only allowed message from the client is the LOGIN message.
- The server can respond with LOGIN_OK for successful login or ERROR for any error.

### Logged In

Client's socket is connected, and the client is logged in (LOGGED IN).

- The client can send any message except LOGIN.
- The server can send any message except LOGIN_OK.
