#August Tannouri
#CS 162 f21 Section 400
#November 24th, 2021
#Description: class that allows one to play the variant 1 version of Hasami Shogi Game
#players start with 9 pieces, with the red pieces on the top and the black on the bottom
#first turn always begins with black, any pieces opposite in color to the players are "captured"
#winner removes all but one of the opponents pieces from the board
#only one class that builds the board, allows for moves and declares wins!!!!


class HasamiShogiGame():

    def __init__(self):
        """
        initializes a "game" object such that each new game has to call HasamiShogiGame()
        no return values, but makes a 2D array board through a function call
        """
        self._board = []
        self._alpha_label = ['a','b','c','d','e','f','g','h','i']
        self._num_label = [' 1 ',' 2 ',' 3 ',' 4 ',' 5 ',' 6 ',' 7 ',' 8 ', ' 9 ']
        self._counter = True            #true for black, false for red, keeps track of the turns
        self.red_capt = 0
        self.black_capt = 0
        self.make_board()

    def make_board(self):
        """
        makes a 9 x 9 grid that is full of empty places denoted by asterisks by filling up a 2D array
        no return value or parameters
        """
        for x in range(0,9):
            col = []
            for y in range(0,9):
                col.append(" * ")
            self._board.append(col)
        for y in range(0,9):
            self._board[0][y] = " R "
            self._board[8][y] = " B "
        return

    def print_board(self):
        """
        displays the pieces present on the board, uses labels to denote rows by alphabet and columns by number
        no return value or parameters
        """
        print(" ", self._num_label)
        for x in range(0,len(self._board)):
            print(self._alpha_label[x], self._board[x])
        return

    def what_square(self, square):
        """
        returns the value on the board at that particular square
        must enter an alpha num combo as parameter between a-i and 1-9
        """
        row = square[0]         #gives you the letter [row]
        for x in range(0,9):
            if row == self._alpha_label[x]:
                row = x
        column = square[1]      #give you the number[col], the index would be minus one
        column = int(column) - 1
        return self._board[row][column]

    def what_index(self, square):
        """
        returns the index on the board at that particular square
        the first return value denotes the row, the second the column
        """
        row = square[0]         #gives you the letter [row]
        for x in range(0,9):
            if row == self._alpha_label[x]:
                row = x
        column = square[1]      #give you the number[col], the index would be minus one
        column = int(column) - 1
        return row, column

    def square_to_alphacall(self, row, col):
        """
        takes the indices as parameters with row first then column
        returns the letter and number combo of a square
        """
        part_1 = self._alpha_label[row]
        part_2 = col + 1
        square = str(part_1) + str(part_2)
        return str(square)

    def remove_piece(self, row, col):
        """
        takes the indices of the square that should be removed
        removes the piece from the board
        """
        #increment captured num
        if self.get_active_player() == "RED":
            self.black_capt += 1
        else:
            self.red_capt += 1
        # replace square on board with " * "
        self._board[row][col] = " * "
        return

    def get_game_state(self):
        """
        no parameters
        checks whether the game is over (who won?) or if it ongoing
        returns UNFINISHED, RED_WON or BLACK_WON
        """
        #sift through the entire board, and add the number of reds and blacks as their own local vars
        red = 0
        black = 0
        for x in range(0,9):
            for y in range(0,9):
                if self._board[x][y] == " R ":
                    red += 1
                if self._board[x][y] == " B ":
                    black += 1
        # if either is less that one, then declare the game as won
        if red <= 1:
            return "BLACK_WON"
        if black <= 1:
            return "RED_WON"
        return "UNFINISHED"
        #could also use the number of captured to determine this!!!!

    def get_active_player(self):
        """
        no parameters
        returns whose turn it is --- "RED" or "BLACK"
        """
        if self._counter:
            return "BLACK"
        else:
            return "RED"

    def get_enemy(self):
        """
        no parameters
        returns the person whose turn it is not --- "RED" or "BLACK"
        """
        if self._counter:
            return "RED"
        else:
            return "BLACK"

    def get_num_captured_pieces(self, player_color):
        """
        parameter: the color of the player, "RED" or "BLACK"
        returns the number of pieces that have been captured for the player
        """
        if player_color == "RED":
            return self.black_capt
        else:
            return self.red_capt

    def check_sandwich(self, direction, row, col, player):
        """
        parameters: the direction where the enemy piece lays adjacent, the indices of the adjacent piece
        and the active player
        checks starting at the quadrant position(s) of the moved piece to see if an opponents
        pieces are sandwiched between the players pieces in that row/col
        no return values
        """
        stop = 0                                    #refers to the index at which the player piece sandwiches the set
        if direction == 'top' and row - 1 >= 0:
            for x in range(row - 1, -1, -1):
                if self._board[x][col] == " * ":
                    break
                if self._board[x][col] == player:
                    stop = x
                    for y in range(row, stop, -1):
                        self.remove_piece(y, col)
                    break
        if direction == 'bottom' and row + 1 <= 8:
            for x in range(row + 1, 9):
                if self._board[x][col] == " * ":
                    break
                if self._board[x][col] == player:
                    stop = x
                    for y in range(row, stop):
                        self.remove_piece(y, col)
                    break
        if direction == 'left' and col - 1 >= 0:
            for x in range(col - 1, -1, -1):
                if self._board[row][x] == " * ":
                    break
                if self._board[row][x] == player:
                    stop = x
                    for y in range(col, stop, -1):
                        self.remove_piece(row, y)
                    break
        if direction == 'right' and col + 1 <= 8:
            for x in range(col + 1, 9):
                if self._board[row][x] == " * ":
                    break
                if self._board[row][x] == player:
                    stop = x
                    for y in range(col, stop):
                        self.remove_piece(row, y)
                    break
        return

    def check_valid(self, row, column):
        """
        parameters: indices of the square where the player moved_to
        checks what positions should be looked at for a capture
        returns values for four locations that are used in the capture() method
        top, bottom, right, left
        to avoid out of bounds errors, we assign a "None" value to that direction
        """
        if row == 0 and column == 0:
            top = self._board[row - 1][column]
            right = self._board[row][column + 1]
            return top, "None", right, "None"
        if row == 0 and column == 8:
            bottom = self._board[row + 1][column]
            left = self._board[row][column - 1]
            return None, bottom, None, left
        if row == 8 and column == 8:
            top = self._board[row - 1][column]
            left = self._board[row][column - 1]
            return top, "None", "None", left
        if row == 8 and column == 0:
            top = self._board[row - 1][column]
            right = self._board[row][column + 1]
            return top, "None", right, "None"
        if row == 8:
            top = self._board[row - 1][column]
            right = self._board[row][column + 1]
            left = self._board[row][column - 1]
            return top, "None", right, left
        if row == 0:
            bottom = self._board[row + 1][column]
            right = self._board[row][column + 1]
            left = self._board[row][column - 1]
            return "None", bottom, right, left
        if column == 8:
            top = self._board[row - 1][column]
            bottom = self._board[row + 1][column]
            left = self._board[row][column - 1]
            return top, bottom, "None", left
        if column == 0:
            top = self._board[row - 1][column]
            bottom = self._board[row + 1][column]
            right = self._board[row][column + 1]
            return top, bottom, right, "None"
        else:
            top = self._board[row - 1][column]
            bottom = self._board[row + 1][column]
            right = self._board[row][column + 1]
            left = self._board[row][column - 1]
            return top, bottom, right, left

    def capture(self, pos, player):
        """
        parameters: the player whose turn it is
        updates the pieces captured and updates the board so that those positions are clear
        no return value
        """
        row = self.what_index(pos)[0]
        column = self.what_index(pos)[1]

        if player == "RED":
            enemy = " B "
            player = " R "
        else:
            enemy = " R "
            player = " B "

        #check perimeter _ what positions should be checked(top, bottom, right or left)
        top = self.check_valid(row, column)[0]
        bottom = self.check_valid(row, column)[1]
        right = self.check_valid(row, column)[2]
        left = self.check_valid(row, column)[3]

        #if the player is captured at a corner piece
        #top left quadrant
        if top == enemy and row == 1 and column == 0:
            self.remove_piece(row - 1, column)
        if left == enemy and row == 0 and column == 1:
            self.remove_piece(row, column - 1)
        #top right quadrant
        if top == enemy and row == 1 and column == 8:
            self.remove_piece(row - 1, column)
        if right == enemy and row == 0 and column == 7:
            self.remove_piece(row, column + 1)
        #bottom left quadrant
        if bottom == enemy and row == 7 and column == 0:
            self.remove_piece(row + 1, column)
        if left == enemy and row == 8 and column == 1:
            self.remove_piece(row, column - 1)
        #bottom right quadrant
        if bottom == enemy and row == 7 and column == 8:
            self.remove_piece(row + 1, column)
        if right == enemy and row == 8 and column == 7:
            self.remove_piece(row, column + 1)

        #if the move resulted in a "sandwich" that results in removal of enemy pieces
        if row - 1 >= 0 and top == enemy:
            calc_row = row - 1
            calc_column = column
            direction = 'top'
            self.check_sandwich(direction, calc_row, calc_column, player)
        if row + 1 <= 8 and bottom == enemy:
            calc_row = row + 1
            calc_column = column
            direction = 'bottom'
            self.check_sandwich(direction, calc_row, calc_column, player)
        if column + 1 <= 8 and right == enemy:
            calc_row = row
            calc_column = column + 1
            direction = 'right'
            self.check_sandwich(direction, calc_row, calc_column, player)
        if column - 1 >= 0 and left == enemy:
            calc_row = row
            calc_column = column - 1
            direction = 'left'
            self.check_sandwich(direction, calc_row, calc_column, player)
        return

    def check_jump(self, direction, ref, og, final):
        """
        parameters: the direction the player is moving in, the index that the moved_to and moved_from have in common,
        the two indices they do not have in common
        checks to see if the move is legal by making sure there are no other pieces
        in the way from the row or column that connect moved_from and moved_to
        """
        if direction == 'right':
            for x in range(og + 1, final):
                if self._board[ref][x] != " * ":
                    return False
        if direction == 'left':
            for x in reversed(range(og - 1, final + 1)):
                if self._board[ref][x] != " * ":
                    return False
        if direction == 'bottom':
            for x in range(og + 1, final):
                if self._board[x][ref] != " * ":
                    return False
        if direction == 'top':
            for x in reversed(range(og - 1, final)):
                if self._board[x][ref] != " * ":
                    return False
        else:
            return True

    def make_move(self, moved_from, moved_to):
        """
        parameters: the alpha/number combo of the position moved to and from
        allows a player to move a piece and updates the 2D array board
        returns True if a move is made, and False if not
        """
        #prelimary conditions that do not require checking the positions
        if moved_to == moved_from:
            return False
        if self.get_active_player() != self.get_square_occupant(moved_from):
            return False
        if self.get_square_occupant(moved_to) != "NONE":
            return False
        if self.get_game_state() != "UNFINISHED":
            return False

        row_1 = self.what_index(moved_from)[0]
        col_1 = self.what_index(moved_from)[1]
        row_2 = self.what_index(moved_to)[0]
        col_2 = self.what_index(moved_to)[1]

        #check if the move is legal(no jumping over pieces or diagonal moves)
        if row_1 == row_2:
            if col_1 > col_2:
                direction = "left"
            else:
                direction = "right"
            if self.check_jump(direction, row_1, col_1, col_2) is False:
                return False
        if col_1 == col_2:
            if row_1 > row_2:
                direction = 'top'
            else:
                direction = 'bottom'
            if self.check_jump(direction, col_1, row_1, row_2) is False:
                return False
        if col_1 != col_2 and row_1 != row_2:
            return False

        # update the positions on the board
        self._board[row_1][col_1] = " * "
        if self.get_active_player() == "RED":
            self._board[row_2][col_2] = " R "
        else:
            self._board[row_2][col_2] = " B "

        # remove any captured pieces from the board
        self.capture(moved_to, self.get_active_player())

        #update whose turn it is
        if self.get_active_player() == "RED":
            self._counter = True
        else:
            self._counter = False
        return True

    def get_square_occupant(self, square):
        """
        parameter: the alpha/number combo of the square
        returns the member at the location of the square
        Example: RED, BLACK, NONE
        """
        if self.what_square(square) == " R ":
            return "RED"
        if self.what_square(square) == " B ":
            return "BLACK"
        if self.what_square(square) == " * ":
            return "NONE"

def main():
    game = HasamiShogiGame()
    game.make_move()

    game.print_board()

if __name__ == "__main__":
    main()

#"DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS"
#(1)Determining how to store the board
    #Make a 2D array in a make_board() method that is called by the init method such that a game object can
    #be made in main and moves can immediately be taken. Initial positions are labeled with an asteriks, indicating
    #they are empty, and a print_board() method easily displays the board with alpha and num labels.

#(2)Initializing the board
        #Use main to create a game object. This allows for each object to represent a new round where moves can be kept track of.
    #As stated in question 1, the initialization of the object will automatically call the make_board() method.

#(3)Determining how to track which player's turn it is to play right now
        #I used a global variable for the class that was initialized in the init method called self._counter. It will only be called
    #directly in the HasamiShogiGame() class. When this boolean value is set as True, then we know that it is the black opponent's
    #turn. Otherwise, false denotes the red opponent's turn. One can check whose turn it is by get_active_player() method.
    #However, it should be noted that whose turn it is is a condition checked by the make_move() method so that pieces of the
    #opponent are not accidently moved.

#Determining how to validate piece movement
    #Here, we check for three things . . .
    #1. if there are any other pieces in the way from point A to point B (i.e. no jumping over pieces)
    #2. that the move being made is either horizontal or vertical (no diagonal movement)
        #to check this we ensure that either the row or col remain the same in the moved_from and moved_to positions
    #3. That the turn of the player and the piece being moved are the same.
    #4. That the game is not finished.
    #5. That the piece is being moved to a new location on the board, such that moved_from and moved_to are not equivalent.

#Determining when pieces have been captured

        #To determine which pieces have been captured we have to determine whose turn it is (refer to #3's method), the pieces
    #surrounding the piece that was just moved (whether or not they are opponents and/or are orthogonal), and how to remove them
    #from the board.
        #To do this, in my make_move() method I call the capture() method. The capture method looks at the positions to the top,right,
    #left, and bottom at the position where the piece was just moved to. It will only call the remove_piece method if the piece is
    #identified to be an enemy piece and is at the corner of the board. For all other captures another function, the check_sandwich()
    #method, is called. This method checks where the next player piece is in a line such that a sandwich forms and removes all the
    #opponent pieces in the line.
    #Please note that the code above still has bugs in it but if clarification is needed it is a good resource to turn to.
    #are enemy pieces.
        #My first solution was to come up with a recursive call, however this will not work as it would also remove orthoganol pieces
    #which is not desired. So, I have edited my code to call a separate capture function that is split in four.
    #The first half would only check vertical positions and the second horizontal positions. This means that for the first capture call,
    #if a piece was found to be on top of the top piece, the only adjacent pieces it would be allowed to check are to the top or bottom of it.

#Determining when the game has ended
        #I have written a method called get_game_state() that counts the number of red and black pieces on the board and
    #call the game if the opponent's pieces left are one or zero. This is because the last move could wipe out all pieces from
    #the board, but only one piece has to remain on the board in order to win. This method is used as a condition for the make_move()
    #method to ensure that the pieces are not able to be moved after a game has been declared.
        #I may use another apporach that uses the number of captured pieces as opposed to counting all the pieces on the board.
