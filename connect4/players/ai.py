import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer


class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        raise NotImplementedError('Whoops I don\'t know what to do')

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here

        parent_dict = {}            # Dictionary for maintaininng parents of each state
        values_dict = {}            # Dictionary for maintaining utilities of each state
        minmax_dict = {}            # Dicitonary for deciding min (false) or max (true) node
        state_action_dict = {}      # Dictionary which maps a state to the corresponding action from the root state

        final_move = (-1,False)      # Initialisation

        def dfs(s):
            valid_moves = get_valid_actions(self.player_number, s)     # List of valid moves
            
            if len(valid_moves) == 0:       # Leaf State
                
                # Backtrack to update scores for each parent
                child_score = get_pts(self.player_number, s[0])
                
                curr = parent_dict[s]

                prev_child = s

                
                
                while curr != None:

                    if minmax_dict[curr] == False:
                        values_dict[curr] = min(values_dict[curr], child_score)
                    else :
                        if (parent_dict[curr] == None) and (child_score > values_dict[curr]):
                            #global final_state
                            global final_move
                            #final_state = prev_child
                            final_move = state_action_dict[prev_child]
                        values_dict[curr] = max(values_dict[curr], child_score)


                    
                        
                    child_score = get_pts(self.player_number, curr[0])
                    
                    prev_child = curr

                    curr  = parent_dict[curr]
                
            else:
                
                # Non Leaf State

                new_state_list = []
                for move in valid_moves:
                    new_s = s       # New state generated after valid move
                    board, popout_dict = s
                    col, isPopout = move
                    r = board.shape[0]     # No of Rows in board array
                    c = board.shape[1]     # No of Columns in board array

                    if isPopout == True:     # Pop out move - we need to change the pop out dictionary as well as the state table
                        popout_dict[self.player_number].decrement()

                        board[:,col] = [0].extend(board[:,col][:-1])        # Update the board state
                        
                        
                        


                        
                    else:       # Normal move
                        for row in range(r-1,-1,-1):
                            if board[row][col] == 0: # Adding player token in bottomost unfilled row
                                board[row][col] = self.player_number
                                break

                    new_s = (board, popout_dict)
                    minmax_dict[new_s] = not minmax_dict[s]     # Change the minmax value for the new state
                    parent_dict[new_s] = s                      # Update the parent of the new state



                    if parent_dict[s] == None:      # Checking if we are at the root state
                        state_action_dict[new_s] = move
                    
                    new_state_list.append(new_s)

                
                # Recursively run DFS on the new states
                
                for new_state in new_state_list:
                    dfs(new_state) 




        parent_dict[state] = None
        dfs(state)


        #raise NotImplementedError('Whoops I don\'t know what to do')
