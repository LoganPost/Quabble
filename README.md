# Quabble
Quirkle board game with a twist! Scrabble-like bonuses are littered across the board.

## To Play
Run `quabble` to play

Click on the player buttons and type in the names of the players. ctrl+backspace clears the name. Click "Play Game" to start pass-and-play. Pass the computer to the first player, then click on the button which says "Pass to (name)" to play the first turn. Each turn entails placing some tiles from your hand with matching shape or color in a row, then clicking the "Place Tiles" button in the top right corner. Then, pass the computer to the next player. As the game continues, the board will grow like a crossword puzzle.

Each move is scored based on the length of the vertical and horziontal lines that are connected by the newly placed tiles. The score of any potential move is shown at the top of the screen, which is the sum of all the lines. If you complete a line of six tiles in a row of the same color or shape, you get 12 points for it instead of 6.
Below are two example moves:
![Example Move](https://user-images.githubusercontent.com/95844502/148012447-4aa5d4fa-92a2-4c3d-a982-ad7497783a56.png)
This move, the green and blue diamonds, is worth 3+3+5=11 points. It is legal because although the tiles aren't touching, they are connected and matching shapes.
![Quirkle Example](https://user-images.githubusercontent.com/95844502/148012461-47f16bab-4826-44f7-a71a-8939156f61b4.png)
This move, the green circle, is 12+3=15 points. By completing the line of 6 circles, you get a 12 point bonus, in addition to the other 3.

## Things to do

### Online Play
This is deactivated because it doesn't work yet.
### Bonuses
Right now, the bonuses are implemented in the game and have been debugged. However, they are very ugly and haven't been playtested to see if they are over or underpowered.
### Graphics
The color pallate and styling is generally distasteful.
