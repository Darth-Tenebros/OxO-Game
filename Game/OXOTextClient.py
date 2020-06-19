from GameClient import *

class OXOTextClient(GameClient):

    def __init__(self):
        GameClient.__init__(self)
        self.board = [' '] * BOARD_SIZE
        self.shape = None
        
    def clear_board(self):
        self.board = [' '] * BOARD_SIZE
        
    def input_server(self):
        return input('enter server:')
     
    def input_move(self):
        return input('enter move(0-8):')
     
    def input_play_again(self):
        return input('play again(y/n):')

    def display_board(self):
        """display a 3x3 grid with empty slots at first
            -to be filled out as the game progresses."""
        print("__________________________________") #34 underscores
        print()
        count = 0
        for i in range(3):
            print("|   ", end="")
            for j in range(3):
                print("   "+self.board[count]+"   |   ", end="")  #3 spaces before and after game symbol
                count+=1

            print()
            print("__________________________________")
            print()


    # “new game,S” – indicates a new game is about to start, S indicates what this client’s shape is,  X or O.

    # “your move” – indicating it is this client’s turn to move

    # “opponents move” – indicating it is the turn of the opponent

    # “valid move,S,P” – indicating a valid move, where S is the shape P and is the position

    # “invalid move” – indicating the position chosen is invalid. client will have to replay the move.

    # “game over,W” – indicates game is over with winner W, where W is either X or O, or T for a tie

    # “play again” – indicating that the game is over and the client will have to see if the user wants to play again.

    # “exit game” – someone has decided to exit the game

    def handle_message(self,msg):
        # the message might/will be comma separated(multiple components)
        # split it into an array so as to individualise each component for later use----.split(",")
        # remove any trailing or leading white space
        message = msg.lower().strip().split(",")
        # lenghtOfMessage = len(message)
        # print(message)

        if(message[0] == "new game"):
            self.display_board()
            self.shape = message[1]
            print("The game has started, your character is " + message[1])

        # The board should only display at the start of a new game
        # or when it is a player's turn to play.
        # there is no reason for the player to see the board when it's the opponents turn to play.
        elif(message[0] == "your move"):
            self.display_board()
            self.yourMove = self.input_move()
            self.send_message(self.yourMove)
        
        elif(message[0] == "opponents move"):
            print("opponent's move")
            #print(message[0])
        
        # when a player makes a valid move at position n, their given charecter should
        # be added to the board array at index n
        elif(message[0] == "valid move"):
            self.shape = message[1]
            self.chosenPosition = message[2]
            self.chosenPosition = int(self.chosenPosition)
            self.board[self.chosenPosition] = self.shape
            print("{} played at position {}".format(self.shape.upper(), str(self.chosenPosition)))
            return "valid move"
        
        elif(message[0] == "invalid move"):
            print(message[0])
        
        # when it's the game ends, displays the final game board and announces the winner
        elif(message[0] == "game over"):
            print("Final game Board.")
            self.display_board()
            if(message[1] == "T"):
                print("It's a tie")
            else: print("Game over, the winner is player {}".format(message[1].upper()))
            return "game over"
        
        elif(message[0] == "play again"):
            self.reply = self.input_play_again()
            if self.reply == 'y': 
                self.clear_board()
            self.send_message(self.reply)
            
        elif(message[0] == "exit game"):
            print("Game ended")
            print("G.G") # "Good Game"----gamer tings



    def play_loop(self):
        while True:
            msg = self.receive_message()
            if len(msg): self.handle_message(msg)
            else: break
            
def main():
    otc = OXOTextClient()
    while True:
        try:
            otc.connect_to_server(otc.input_server())
            break
        except:
            print('Error connecting to server!')
    otc.play_loop()
    input('Press click to exit.')
        
main()
