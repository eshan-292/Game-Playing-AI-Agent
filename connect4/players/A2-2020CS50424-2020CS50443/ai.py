import random
from tkinter import E
from xmlrpc.client import boolean
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
import sys
import copy
import time

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

        time_limit = self.time
        start_time =  time.time()
        total_states = 1
        final_move = (-1,False)      # Initialisation





        # With alpha beta pruning

        def max_value(node, depth_limit, new_node_list, player_number, alpha, beta):           
            nonlocal max_d
            nonlocal final_move

            if max_d == depth_limit:
                


                best_move = (-1,False)
                for new_node in new_node_list:
                         
                    v = value(new_node, depth_limit - 1,alpha, beta)
                    
                    
                    if v > node.value:
                        
                        best_move = new_node.action
                        
                    node.value = max(v, node.value)
                    if node.value >= beta:
                        return node.value
                    alpha = max(alpha, node.value)


                final_move = best_move             
                
                
            
            else:

                for new_node in new_node_list:
                    
                    v = value(new_node, depth_limit - 1,alpha, beta)
 
                    node.value = max(v, node.value)
                    if node.value >= beta:
                        return node.value
                    alpha = max(alpha, node.value)

                
                
                


                

            return node.value

        def min_value(node, depth_limit, new_node_list, player_number, alpha, beta):

            for new_node in new_node_list:
                v = value(new_node, depth_limit - 1,alpha, beta)
                node.value = min(v, node.value)

                if node.value <= alpha:
                    return node.value
                
                beta = min(beta, node.value)

            return node.value

        # Depth limited value
        def value(node:TreeNode, depth_limit, alpha, beta):
            nonlocal final_move
            nonlocal total_states
    

            time_remaining = time_limit - (time.time() - start_time)

            if time_remaining < 0.5:
                # breaking_time_start = time.time()
                raise Exception('Breaking from recursive calls and ending execution')

            opponent_player_number = 1

            if self.player_number == 1:
                opponent_player_number = 2
            else:
                opponent_player_number = 1

            # Setting the player number
            player_number = self.player_number
            if node.isMax == False:
                if self.player_number == 1:
                    player_number = 2
                else:
                    player_number = 1
                

            valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves

            new_node_list = []

            for move in valid_moves:
                    new_node = node.transition(move, player_number)
                    new_node.score = 1.3*get_pts(self.player_number, new_node.state[0]) - get_pts(opponent_player_number, new_node.state[0])
                    
                    new_node_list.append(new_node)


            


            total_states = total_states+ len(valid_moves)

            node.numChildren += len(valid_moves)        # Incrementing no of children of node
        
            # Leaf State
            if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                node.value = 1.3*get_pts(self.player_number, node.state[0]) - get_pts(opponent_player_number, node.state[0])
                return node.value
                
            else:
                
                # Non Leaf State


                if node.isMax:
                    
                    new_node_list.sort(key = lambda x : x.score, reverse = True)
                    return max_value(node, depth_limit, new_node_list, player_number, alpha, beta)
                else:
                    
                    new_node_list.sort(key = lambda x : x.score, reverse = False)
                    return min_value(node, depth_limit, new_node_list, player_number, alpha, beta)

        valid_moves = get_valid_actions(self.player_number, state)     # List of valid moves
        b = len(valid_moves)
   


        depth_limit = 3
        
        while (True):
            
            max_d = depth_limit
            root_node = TreeNode(state=state, value= -sys.maxsize, isMax=True, parent= None, action=(-1,False), numChildren=0, score = 0)            

            try :
                
                value(root_node, depth_limit, -sys.maxsize, sys.maxsize)
            except : 

            

                    
                break 
            else :
                

                depth_limit = depth_limit + 1


        return final_move
        #raise NotImplementedError('Whoops I don\'t know what to do')

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

        time_limit = self.time
        start_time =  time.time()
        total_states = 1
        final_move = (-1,False)      # Initialisation
        

    


        def max_value(node, depth_limit, valid_moves, player_number):
            best_move = (-1,False)
            for move in valid_moves:
                new_node = node.transition(move, player_number)
                v = value(new_node, depth_limit - 1)
                if v > node.value:
                    best_move = move
                node.value = max(v, node.value)
            nonlocal max_d
            nonlocal final_move
            if max_d == depth_limit:
                final_move = best_move             
            return node.value

        def expected_value(node, depth_limit, valid_moves, player_number):
            node.value = 0
            for move in valid_moves:
                new_node = node.transition(move, player_number)
                v = value(new_node, depth_limit - 1)
                
                node.value += v/node.numChildren
            
            return node.value

        # Depth limited value
        def value(node:TreeNode, depth_limit):
            nonlocal final_move
            nonlocal total_states

            time_remaining = time_limit - (time.time() - start_time)            

            if time_remaining < 0.5:
                raise Exception('Breaking from recursive calls and ending execution')            

            opponent_player_number = 1

            if self.player_number == 1:
                opponent_player_number = 2
            else:
                opponent_player_number = 1

            # Setting the player number
            player_number = self.player_number
            if node.isMax == False:
                if self.player_number==1:
                    player_number = 2
                else:
                    player_number = 1
                
            
            valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves
            total_states = total_states + len(valid_moves)

            node.numChildren = len(valid_moves)        # Incrementing no of children of node

        
            # Leaf State
            if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                node.value = get_pts(self.player_number, node.state[0]) - get_pts(opponent_player_number, node.state[0]) 
                return node.value
                
            else:
                
                # Non Leaf State



                if node.isMax:
                    return max_value(node, depth_limit, valid_moves, player_number)
                else:
                    return expected_value(node, depth_limit, valid_moves, player_number)

        valid_moves = get_valid_actions(self.player_number, state)     # List of valid moves
        b = len(valid_moves)

        depth_limit = 1
        

        
        while (True):
            
            max_d = depth_limit
            root_node = TreeNode(state=state, value= -sys.maxsize, isMax=True, parent= None, action=(-1,False), numChildren=0, score = 0)
            
            
            try :
                value(root_node, depth_limit)
            except :
                break 
            else :

                depth_limit = depth_limit + 1
 


        return final_move        
        #raise NotImplementedError('Whoops I don\'t know what to do')


        
class TreeNode:
    def __init__(self, state: Tuple[np.array, Dict[int, Integer]], value: float, isMax: bool, parent, action:Tuple[int, bool], numChildren:int, score:float):
        self.state = state
        self.value = value
        self.isMax = isMax
        self.parent = parent
        self.action = action
        self.numChildren = numChildren
        self.score = score
        
    def transition(self, action:Tuple[int, bool], player_number:int):
        board = copy.deepcopy(self.state[0])
        popout_dict = copy.deepcopy(self.state[1])
        col, isPopout = action
        r = board.shape[0]     # No of Rows in board array
        if isPopout == True:     # Pop out move - we need to change the pop out dictionary as well as the state table
            popout_dict[player_number].decrement()
            temp = [0]
            temp.extend(board[:,col][:-1])
            board[:,col] = temp       # Update the board state
            
        else:       # Normal move
            for row in range(r-1,-1,-1):
                if board[row][col] == 0: # Adding player token in bottomost unfilled row
                    board[row][col] = player_number
                    break
        new_s = (board, popout_dict)      

        new_value = - sys.maxsize
        if(self.isMax): 
            new_value = sys.maxsize
        next_node = TreeNode(state=new_s, value = new_value, isMax= not self.isMax, parent= self, action= action, numChildren=0, score = 0) 

        return next_node    
