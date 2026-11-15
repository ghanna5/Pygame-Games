
# Tic Tac Toe

The objectives of this exercise are:

* Write a game that is single player and turn based
* Use a rule set
* Learn to use Pygame for a single view game
* Improving our programming practices

We shall all write the card game named [Tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe). Tic-tac-toe is paper and pencil game for two players who take turns marking a 3 x 3 grid. One player marks the grid with Xs and the other player marks the gird with Os. A player wins when three spaces in a row, column or diagonal of the 3 x 3 grid contains their marks.

In your [recommended reading](https://docs.google.com/document/d/184U-IQ0DrmlVlPMySjKaYxq2M-ScNvgX8NRa1Kkuk9Q/edit), the book [_Luck, logic, and white lies : the mathematics of games_](https://csu-fullerton.primo.exlibrisgroup.com/permalink/01CALS_FUL/10o4t9/alma991013418479202908) offers a brief analysis of Tic-tac-toe in Chapter 19. You are strongly encouraged to read this chapter. Additionally, Wikipedia's article on [Tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe) provides a summary of [Newell](https://en.wikipedia.org/wiki/Allen_Newell) & [Simon's](https://en.wikipedia.org/wiki/Herbert_A._Simon) Tic-tac-toe strategy from their seminal text [Human Problem Solving](https://csu-fullerton.primo.exlibrisgroup.com/permalink/01CALS_FUL/pav3bs/alma991003548419702908.

In our version of Tic-tac-toe, the paper and pencil is replaced by the computer and your code. The game shall be two player, however one of the players shall be a human and the other player shall be a robot. The human always plays first and uses Xs. The robot plays second and uses Os.

The human is presented with an easy to understand user interface and uses the computer's mouse to point and click, thus selecting which grid cell they're playing their X. The robot player use's some set of heuristics to select which grid cell they shall play. Players may not select in a previously selected grid cell. In other words, a player may not overwrite a grid cell played by themself or their opponent. A turn isn't completed until an empty grid cell is selected.

The game continues, turn by turn, until either one of the two players win or the game comes to a draw. When a player wins the game stops immediately. When all grid cells are filled and no player wins, then the game is considered a draw. 

When a game concludes (win or draw), the human player can opt to play again or exit the game.

## Rules

* There are always two players; a human player who inputs moves using a mouse and a robot player who communicates directly to the game.
* The game is turn based. The human player plays first and uses the X symbol. The robot player plays second and uses the O symbol.
* A turn is concluded once an empty grid cell is selected.
* Grid cells that have already been selected, may not be selected again.
* When the program starts, the game begins. The game does not end until someone wins or there is a draw.
* When a game ends (win or draw), the player who won is identified or the user interface communicates that the game is a draw.
* The human player has the option to start a new game or exit the game at the end of each game.
* The human player may not exit a game once the game begins.
* The robot player must use some heuristics which attempt to play the game competitively.

## Requirements

The requirements of the program are that the game must play according to the rules given above. If there is any ambiguity of the rules, the the student should discuss the rules with the instructor to clarify the rules.

The game must be written in Python 3 and Pygame. You may use other libraries to complete this project.

The human player must use the mouse to select the grid space they desire to select. Clicking in the grid cell selects the cell.

After each turn or starting after the third turn, the game checks the board to see who is the winner. If no winner is identified, the game play continues. If a winner is identified, then game play stops and the winner is identified.

The robot player must use some heuristics which attempt to play the game competitively. At a minimum, the robot player must analyze the Tic-tac-toe board to weigh the choices and determine a good choice. Ideally, the robot player plays with a perfect strategy.

The game must have a soundtrack and it must have at least two auditory or visual cues. For example, play a sound effect when a turn is completed or a mouse button is clicked.

To run the game, the command must be `./tictactoe.py`. This means that the file `tictactoe.py` must have a shebang and call the main game loop. This file contains only a call to the game's main loop which is defined in the `videogame` package.

The game's logic must be defined in a package named `videogame`. This means there must be a directory named `videogame` which contains all the Python source code for the project. At a minimum, the following files must be included in the `videogame` package:
* `__init__.py`
* `game.py`
* `scene.py`

The file `__init__.py` can be a very simple file which defines an `__all__` variable for the package. See the documentation about [Python modules](https://docs.python.org/3/tutorial/modules.html), specifically [Section 6.4.1. Importing * From a Package](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package).

Place all your media files and other assets in the data directory found in the `videogame` directory. Do not hard code paths to files. Use the example asset as a starting point for your own asset mananger.

## Suggestions

Write a bot such that you can automate the gameplay. This will help you test the game without having to interact with the game. Make the bot scriptable or predictable so you can observe how your game behaves.

Write tests for your project. A small investment in writing tests will improve the quality of your work as well as teach you a very valuable skill. Python has a framework aptly named [`unittest`](https://docs.python.org/3/library/unittest.html). The documentation is very good and it is easy to get started.

### AUTHORS.md File
The file `AUTHORS.md` is empty. You must fill in the file with your name, email, and GitHub user name.

Let's imagine your name is Tuffy Titan. Tuffy's email address is tuffy@csu.fullerton.edu. Tuffy's GitHub user name is `tuffytitan`. With this information, the contents of the `AUTHORS.md` file will look like the following example:

```
Tuffy Titan
tuffy@csu.fullerton.edu
@tuffytitan
```

The order matters and it is part of your grade. Please make your `AUTHORS.md` file match the same pattern as the one given here.

## Don't Forget

Please remember that:
* Fill in the `AUTHORS.md` file.
* You need to follow [PEP-8](https://www.python.org/dev/peps/pep-0008/); use linters and style checkers such as `pycodestyle`, `pylint`, and `black`.
* You need to test your program. If it does not run correctly or if it unplayable then your project will receive poor marks.

# Rubric

This exercise is worth 15 points. Your program must not have any syntax errors before it is graded. Submissions that have a syntax error or throw an uncaught exception will be assigned a score of 0.

* Functionality (approximately 9 points): Your submission shall be assessed for the appropriate constructs and strategies to address the exercise. A program the passes the instructor's tests completely receives full marks for this dimension. A program that partially passes the instructors tests receives partial-marks. A program that fails the majority or all the tests receives no marks.

* Format & Readability (approximately 6 points): Your submission shall be assessed by checking whether your code passess the style and format check, as well as how well it follows the proper naming conventions, and internal documentation guidelines. Git log messages are an integral part of how readable your project is. _Failure to include or complete an AUTHORS.md file forfeits all marks._

