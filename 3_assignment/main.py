from os import system, name
import time

class TicTacToeGame(object):
    def __init__(self):
        self.winOnBoxes = ([0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 4, 8], [2, 4, 6], [0, 3, 6], [1, 4, 7], [2, 5, 8])
        # refer in functions to those characters
        self.playingCharacters = {'human': 'X', 'computer' : 'O'}
        self.neutralCharacter = ' '
        self.gameBoard = [self.neutralCharacter for i in range(9)]

    def printGameBoard(self):
        delimiter = "-------------  -------------"
        print(delimiter)
        print("| ", end="")
        for i, obj in enumerate(self.gameBoard, 1):
            print(obj + " | ", end="")
            if (i % 3) == 0:
                print(" | ", end="")
                for i in range(i - 2, i + 1):
                    print(str(i) + " | ", end="")

                print()
                print(delimiter)
                if i < 9:
                    print("| ", end="")

    def freeBoxes(self):
        # find all free boxes
        possibleMoves = []
        for i, value in enumerate(self.gameBoard):
            if value == self.neutralCharacter:
                possibleMoves.append(i)
        return possibleMoves

    def finished(self):
        # end of game
        if self.neutralCharacter not in [v for v in self.gameBoard]:
            return True
        if self.findWinner() == None:
            return False
        return True

    def findWinner(self):
        for currentPlayer in self.playingCharacters:
            pos = self.getPlayerBoxes(self.playingCharacters[currentPlayer])
            for boxes in self.winOnBoxes:
                winnerFlag = True
                for winLine in boxes:
                    if winLine not in pos:
                        winnerFlag = False
                        break

                if winnerFlag:
                    return self.playingCharacters[currentPlayer]
        return None

    def getPlayerBoxes(self, currentPlayer):
        # Possible next moves for currentPlayer
        playerBoxes = []
        for i, value in enumerate(self.gameBoard):
            if value == currentPlayer:
                playerBoxes.append(i)
        return playerBoxes

    def MinimaxWithalphaBetaPrunning(self, gameState, currentPlayer, alpha, beta):
        # if gameBoard is full evaluate result
        if gameState.finished():
            if gameState.findWinner() == gameState.playingCharacters['human']:
                return -1
            elif gameState.findWinner() == gameState.playingCharacters['computer']:
                return 1
            else:
                return 0

        # recursively checking all possible moves
        for box in gameState.freeBoxes():
            gameState.gameBoard[box] = currentPlayer
            gameStateValue = self.MinimaxWithalphaBetaPrunning(gameState, self.returnOtherCharacter(currentPlayer), alpha, beta)
            gameState.gameBoard[box] = self.neutralCharacter

            if currentPlayer == gameState.playingCharacters['computer']:
                if gameStateValue > alpha:
                    alpha = gameStateValue
                if alpha >= beta:
                    return beta
                # human player's turn
            else:
                if gameStateValue < beta:
                    beta = gameStateValue
                if beta <= alpha:
                    return alpha

        if currentPlayer == gameState.playingCharacters['computer']:
            return alpha
        else:
            return beta

    def gameController(self):
        playerCharacter = self.playingCharacters['human']

        clear()
        print('Hra tic-tac-toe proti AI, začíná hráč s "X" vybráním políčka (tabulka vpravo ukazuje čísla pozic)')
        self.printGameBoard()

        while not self.finished():
            characterOnMove = playerCharacter
            playerInput = input("Jsi na tahu: ")

            try:
                # input - 1 because list with board is indexed from 0 but in-game boxes from 1
                playerInput = int(playerInput) - 1
            except:
                # if conversion from string to int fail (no other exception should occur, but in case catching all of them)
                print("\nŠpatný výběr pole. Zkus to znovu!")
                continue

            if playerInput not in self.freeBoxes():
                print("\nŠpatný výběr pole. Zkus to znovu!")
                continue

            clear()
            self.gameBoard[playerInput] = characterOnMove
            self.printGameBoard()
            print("Počítač je na tahu.")
            time.sleep(1)

            if self.finished():
                break

            clear()
            characterOnMove = self.returnOtherCharacter(characterOnMove)
            self.gameBoard[self.chooseNextBox(characterOnMove)] = characterOnMove
            self.printGameBoard()

        if self.findWinner() == self.playingCharacters['human']:
            # this if condition should never occur
            print("Vyhrál/a jsi")
        elif self.findWinner() == self.playingCharacters['computer']:
            print("Zvítězil počítač")
        else:
            print("Hra skončila remízou")


    def chooseNextBox(self, currentPlayer):
        a = -9999
        correctMoves = []
        for box in self.freeBoxes():
            self.gameBoard[box] = currentPlayer
            result = self.MinimaxWithalphaBetaPrunning(self, self.returnOtherCharacter(currentPlayer), -999, 999)
            self.gameBoard[box] = self.neutralCharacter
            if result > a:
                a = result
                correctMoves = [box]
            elif result == 2:
                correctMoves.append(box)

            # next lines print expected result by choosing those boxes as next move

            # winners = ['X vyhraje', 'skončí remízou', 'O vyhraje']
            # printing who would win on every possible move
            # print("Tah: " + str(box + 1) + " , pak: " + winners[result + 1])
        return correctMoves[0]


    def returnOtherCharacter(self, currentCharacter):
        if currentCharacter == self.playingCharacters['computer']:
            return self.playingCharacters['human']
        return self.playingCharacters['computer']


def clear():
    # clear console output
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


if __name__ == "__main__":
    TicTacToeGame().gameController()


