# Battleship Game

## Table of Contents
- [Purpose](#purpose)
- [User Stories](#user-stories)
- [Design and UX](#design-and-ux)
- [Notepad planning](#notepad-planning)
- [Features](#features)
- [Technologies](#technologies)
- [Testing](#testing)
  - [Code Validation](#code-validation)
  - [Browser Compatibility](#browser-compatibility)
  - [Performance Testing](#performance-testing)
  - [Manual Testing](#manual-testing)
  - [User Testing](#user-testing)
- [Debugging and Known Bugs](#debugging-and-known-bugs)
- [Deployment](#deployment)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)

## Purpose
The Battleship Game is a text-based Python game where players try to sink their opponent’s fleet of ships before their own fleet is sunk. It’s a strategy-based game where each player places their ships on a grid and then takes turns guessing the coordinates of the opponent’s ships to attack. The game ends when one player's fleet is completely destroyed.

[Live link: Battleship Game](https://battleship03-58560e78b929.herokuapp.com/)

## User Stories
### A first-time player:
- I want to understand the rules and how to play the game easily.
- I want the game to provide feedback after each move.
- I want to be able to see the state of the game clearly.

### A returning player:
- I want to replay the game with new challenges each time.
- I want to be able to toggle difficulty levels (e.g., AI strategies).
- I want to play quickly without rereading instructions every time.

### As the owner of the game:
- I want to provide users with an intuitive and engaging experience.
- I want the game to handle invalid input effectively.
- I want the game to track player progress and display useful results.

## Design and UX
### Notepad planning
The game follows a simple flow:
1. **Game Start:** Instructions are displayed, ships are placed.
2. **Player Turns:** Players take turns guessing coordinates to attack.
3. **Feedback:** Each turn provides feedback (hit or miss).
4. **Game End:** The game concludes when a player's ships are all sunk.

### Notepad Image:
![planning](/assets/images/planning.1.JPG)
![planning.2](/assets/images/Capture.JPG)

## Features
### Existing Features:
- **Grid Display:** Shows the game grid and updates it after each move.
  - *Example: Displays player’s and computer’s grids with current status.*
  - ![grid](/assets/images/grid.JPG)
  
- **Ship Placement:** Players ships are placed randomly.
  - *Example: Players see their ships and guess coordinates for the opponent's ships.*
  - ![player-ship](/assets/images/player-ship.JPG)
  
- **Hit and Miss Feedback:** The game provides real-time feedback on attacks.
  - *Example: “Hit!” or “Miss!” messages after each attack.*
  - ![feedback](/assets/images/hit-miss.JPG)
  
- **Victory Conditions:** The game announces a winner once all ships of one player are destroyed.
  - *Example: Displaying a message of congratulations or defeat.*
  - ![victory-conditions](/assets/images/victory-condition.JPG)

- **Input Validation:** The game handles invalid inputs (e.g., out-of-bound coordinates) gracefully.
    - ![input-validation](/assets/images/input-validation.JPG)

### Future Features:
- **Difficulty Levels:** Introduce multiple difficulty levels with varying AI Behaviour.
- **Multiplayer Support:** Implement an online mode to allow multiplayer games.
- **Save/Load Game:** Allow players to save and load game progress.
- **Timed Rounds:** Add a timer to limit the time a player can take for their turn.
- **Custom Ship Layouts:** Let players design their fleet layouts.

## Technologies
- **Python 3:** Core language for the game's logic.
- **GitHub:** For version control and hosting the project repository.

## Testing
### Code Validation
- **Python Validation:** The code was tested using PEP8 Online and passed with no major issues.

### Browser Compatibility
- Since this is a console-based Python game, it doesn’t require browser testing.

### Performance Testing
- The game was tested for performance by running multiple rounds, ensuring that it handled turns efficiently without noticeable lag. ![testing](/assets/images/testing.JPG)

### Manual Testing
- Manual testing was done by running the game on various operating systems (Windows, macOS, and Linux) to ensure compatibility.

### User Testing
- **A first-time user looking to play the game:**
  - The instructions were clear and easy to follow.
  - The game grid was easy to understand and interact with.
  - Feedback after each move kept the game engaging.
  
- **A returning user looking to play the game again:**
  - The game provided fresh challenges each time due to the randomized ship placement.
  - The overall flow was smooth, and repeated instructions could be skipped.

## Debugging and Known Bugs
- **Issue:** Initially, input validation allowed negative coordinates, which led to an index error.
  - **Solution:** Added checks to ensure input stays within grid bounds.

- **Issue:** The grid display sometimes didn’t update correctly after a hit.
  - **Solution:** The grid update function was debugged to ensure all coordinates were updated properly.

- **Remaining Bugs:** Currently, no major known bugs remain. The game is fully functional.

## Deployment
The game was deployed using the following steps:
- Fork or clone this repository
- Create a new Heroku app
- Set the buildbacks to Python and NodeJS in that order
- Link the Heroku app to the repository
- Click on **Deploy**

## Credits
- **Python Docs:** For Python language references and syntax.
- **Battleship Strategy Guides:** For game logic inspirations.
- **README.md example:** I used this [example](https://github.com/keelback-code/the-rhubarb-witch) project to help with the README.md

## Acknowledgements
Special thanks to my mentor for guidance and support throughout the project development. Many thanks to friends and family who provided feedback and helped with testing.
