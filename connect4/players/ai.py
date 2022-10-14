# TODO:
# 1. Implement alpha beta pruning 
# 2. Maximise the diff btw scores instead of just maximising the current player's score
# 3. Build a clever heuristic function to greedily prune the search tree (smthng like local beam search)
# 4. Find a good approximation for the scores of virtual leaf nodes
# 5. Reduce the no of backtracking operations 




import random
from xmlrpc.client import boolean
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
import sys



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

        
        total_states = 1
        final_move = (-1,False)      # Initialisation
        # final_move = (0,False)      # Initialisation

        # Depth limited DFS
        def dfs(node:TreeNode, depth_limit):
            nonlocal total_states
            nonlocal final_move
            # final_move = (-1,False)
            # nonlocal root_node
            # print("Root state: ", root_node.state[0])
            
            # Setting the player number
            player_number = self.player_number
            if node.isMax == False:
                if self.player_number==1:
                    player_number = 2
                else:
                    player_number = 1
                
            #print("Player Number : ", player_number)
            #print("IsMax : ", node.isMax)
            valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves
            total_states = total_states+ len(valid_moves)

            node.numChildren += len(valid_moves)        # Incrementing no of children of node
        
            # Leaf State
            if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                
                # Backtrack to update scores for each parent
                curr_player_number = player_number
                child_score = get_pts(curr_player_number, node.state[0])
                curr = node.parent
                prev_child = node
                
                while curr is not None:
                    #print("child score is = ", child_score)
                          
                    if curr.isMax == False:
                        #print('min curr value = ', curr.value)  
                        curr.value = min(curr.value, child_score)
                        # curr.value += (child_score/curr.numChildren)
                    else :
                        #print('max curr value = ', curr.value)                            
                        if (curr.parent == None) and child_score > curr.value:
                            final_move = prev_child.action
                            print("Final Move updated to : ", final_move)
                        curr.value = max(curr.value, child_score)

                    # Updating the player number
                    if curr_player_number==1:
                        curr_player_number = 2
                    else:
                        curr_player_number = 1

                    #Updating the child and curr parameters
                    child_score = get_pts(curr_player_number, curr.state[0])
                    #print('curr state board = ', curr.state[0])
                    prev_child = curr
                    curr  = curr.parent
                
                #print('modified final_move = ', final_move)
                
            else:
                
                # Non Leaf State

                # new_node_list = []
                for move in valid_moves:
                    new_node = node.transition(move, player_number)
                    dfs(new_node, depth_limit - 1)


        depth_limit = 10
        root_node = TreeNode(state=state, value= 0, isMax=True, parent= None, action=(-1,False), numChildren=0)
        
        dfs(root_node, depth_limit)

        # print('Total no of visited states: ', total_states)
        # print('best_move = ', final_move)
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

        
       
        total_states = 1
        final_move = (-1,False)      # Initialisation
        # final_move = (0,False)      # Initialisation

        # Depth limited DFS
        def dfs(node:TreeNode, depth_limit):
            nonlocal total_states
            nonlocal final_move
            # final_move = (-1,False)
            # nonlocal root_node
            # print("Root state: ", root_node.state[0])
            
            # Setting the player number
            player_number = self.player_number
            if node.isMax == False:
                if self.player_number==1:
                    player_number = 2
                else:
                    player_number = 1
                
            print("Player Number : ", player_number)
            print("IsMax : ", node.isMax)
            valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves
            total_states = total_states+ len(valid_moves)

            node.numChildren += len(valid_moves)        # Incrementing no of children of node
        
            # Leaf State
            if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                
                # Backtrack to update scores for each parent
                curr_player_number = player_number
                child_score = get_pts(curr_player_number, node.state[0])
                curr = node.parent
                prev_child = node
                
                while curr is not None:
                    print("child score is = ", child_score)
                          
                    if curr.isMax == False:
                        print('min curr value = ', curr.value)  
                        curr.value = min(curr.value, child_score)
                        # curr.value += (child_score/curr.numChildren)
                    else :
                        print('max curr value = ', curr.value)                            
                        if (curr.parent == None) and child_score > curr.value:
                            final_move = prev_child.action
                            print("Final Move updated to : ", final_move)
                        curr.value = max(curr.value, child_score)

                    # Updating the player number
                    if curr_player_number==1:
                        curr_player_number = 2
                    else:
                        curr_player_number = 1

                    #Updating the child and curr parameters
                    child_score = get_pts(curr_player_number, curr.state[0])
                    print('curr state board = ', curr.state[0])
                    prev_child = curr
                    curr  = curr.parent
                
                print('modified final_move = ', final_move)
                
            else:
                
                # Non Leaf State

                # new_node_list = []
                for move in valid_moves:
                    new_node = node.transition(move, player_number)
                    dfs(new_node, depth_limit - 1)


        depth_limit = 3
        root_node = TreeNode(state=state, value= 0, isMax=True, parent= None, action=(-1,False), numChildren=0)
        
        dfs(root_node, depth_limit)

        print('Total no of visited states: ', total_states)
        print('best_move = ', final_move)
        return final_move
        #raise NotImplementedError('Whoops I don\'t know what to do')
        
class TreeNode:
    def __init__(self, state: Tuple[np.array, Dict[int, Integer]], value: int, isMax: bool, parent, action:Tuple[int, bool], numChildren:int):
        self.state = state
        self.value = value
        self.isMax = isMax
        self.parent = parent
        self.action = action
        self.numChildren = numChildren
        
    def transition(self, action:Tuple[int, bool], player_number:int):
        board = self.state[0].copy()
        popout_dict = self.state[1].copy()
        #print('init board = ', board)
        col, isPopout = action
        r = board.shape[0]     # No of Rows in board array
        #c = board.shape[1]     # No of Columns in board array
        if isPopout == True:     # Pop out move - we need to change the pop out dictionary as well as the state table
            popout_dict[player_number].decrement()
            board[:,col] = [0].extend(board[:,col][:-1])        # Update the board state
            
        else:       # Normal move
            for row in range(r-1,-1,-1):
                if board[row][col] == 0: # Adding player token in bottomost unfilled row
                    board[row][col] = player_number
                    break
        new_s = (board, popout_dict)      

        new_value = 0
        if(self.isMax): 
            new_value = - sys.maxsize
        # else:
        #     new_value = 0
        next_node = TreeNode(state=new_s, value = new_value, isMax= not self.isMax, parent= self, action= action, numChildren=0) 
        #print('final board = ', next_node.state[0])

        return next_node    

    def copy(self):
        state_dup = (self.state[0].copy(), self.state[1].copy())
        parent_dup = None
        node_dup = TreeNode(state=state_dup,value=self.value,isMax=self.isMax, parent=parent_dup, action=self.action,numChildren=self.numChildren)
        return node_dup