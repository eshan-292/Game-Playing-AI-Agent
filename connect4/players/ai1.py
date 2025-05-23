# TODO:
# ++ 1. Implement alpha beta pruning 
# ++ 2. Maximise the diff btw scores instead of just maximising the current player's score
# 3. Build a clever heuristic function to greedily prune the search tree (smthng like local beam search)
# ++ 4. Find a good approximation for the scores of virtual leaf nodes
# ~~ 5. Reduce the no of backtracking operations 
#̶ ̶-̶-̶ ̶6̶.̶ ̶T̶r̶y̶ ̶t̶o̶ ̶i̶m̶p̶l̶e̶m̶e̶n̶t̶ ̶m̶e̶m̶o̶i̶s̶a̶t̶i̶o̶n
# ~~ 7. Try to make the depth limit dynamic (based on the conditions - board size, no of popout moves, etc)~~ 
# 8. Use iterative deepening
# ~~ 9. Sort nodes in descending order to max pruning
# 10. Modify eval fn - weights of features 
# 11. Toggle algo depending on whether player 1 or 2
# 12. Test against naive minimax with pruning
# 

import random
from tkinter import E
from xmlrpc.client import boolean
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
import sys
import copy
import time

class AIPlayer1:
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

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) :
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
        

        # final_move = (0,False)      # Initialisation


        # # Without alpha beta pruning


        # def max_value(node, depth_limit, valid_moves, player_number):
        #     best_move = (-1,False)
        #     for move in valid_moves:
        #         new_node = node.transition(move, player_number)
        #         v = value(new_node, depth_limit - 1)
        #         if v > node.value:
        #             best_move = move
        #         node.value = max(v, node.value)
        #     nonlocal max_d
        #     nonlocal final_move
        #     if max_d == depth_limit:
        #         final_move = best_move             
        #     return node.value

        # def min_value(node, depth_limit, valid_moves, player_number):
        #     for move in valid_moves:
        #         new_node = node.transition(move, player_number)
        #         v = value(new_node, depth_limit - 1)
        #         node.value = min(v, node.value)
        #     return node.value

        # # Depth limited value
        # def value(node:TreeNode, depth_limit):
        #     nonlocal final_move
        #     nonlocal total_states
            

        #     opponent_player_number = 1

        #     if self.player_number == 1:
        #         opponent_player_number = 2
        #     else:
        #         opponent_player_number = 1

            
        #     # Setting the player number
        #     player_number = self.player_number
        #     if node.isMax == False:
        #         if self.player_number==1:
        #             player_number = 2
        #         else:
        #             player_number = 1
                
        #     #print("Player Number : ", player_number)
        #     #print("IsMax : ", node.isMax)
        #     valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves
        #     total_states = total_states + len(valid_moves)

        #     node.numChildren += len(valid_moves)        # Incrementing no of children of node
        
        #     # Leaf State
        #     if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
        #         node.value = get_pts(self.player_number, node.state[0]) - get_pts(opponent_player_number, node.state[0]) 
        #         return node.value
                
        #     else:
                
        #         # Non Leaf State

        #         # # new_node_list = []
        #         # for move in valid_moves:
        #         #     new_node = node.transition(move, player_number)
        #         #     value(new_node, depth_limit - 1)


        #         if node.isMax:
        #             return max_value(node, depth_limit, valid_moves, player_number)
        #         else:
        #             return min_value(node, depth_limit, valid_moves, player_number)







        # With alpha beta pruning
        def max_value(node, depth_limit, new_node_list, player_number, alpha, beta):           
            nonlocal max_d
            nonlocal final_move

            if max_d == depth_limit:
                


                best_move = (-1,False)
                for new_node in new_node_list:
                    # new_node = node.transition(move, player_number)
                    # try:
                    #     v = value(new_node, depth_limit - 1,alpha, beta)
                    # except:
                    #     raise Exception('Time Limit Exceeded')
                         
                    v = value(new_node, depth_limit - 1,alpha, beta)
                    
                    # print("Child Value: ", v)
                    if v > node.value:
                        
                        # best_move = move
                        best_move = new_node.action
                        # print("Best Move: ", best_move)
                    node.value = max(v, node.value)
                    if node.value >= beta:
                        return node.value
                    alpha = max(alpha, node.value)


                final_move = best_move             
                
                # print("Final Move: ", final_move)
            
            else:

                for new_node in new_node_list:
                    # new_node = node.transition(move, player_number)
                    v = value(new_node, depth_limit - 1,alpha, beta)
                    # if v > node.value:
                        # best_move = move
                        #print("Best Move: ", best_move)
                    node.value = max(v, node.value)
                    if node.value >= beta:
                        return node.value
                    alpha = max(alpha, node.value)

                
                # print("Best Move: ", best_move)
                


                

            return node.value

        def min_value(node, depth_limit, new_node_list, player_number, alpha, beta):

            for new_node in new_node_list:
                # new_node = node.transition(move, player_number)
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
                
            #print("Player Number : ", player_number)
            #print("IsMax : ", node.isMax)
            valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves

            new_node_list = []

            for move in valid_moves:
                    new_node = node.transition(move, player_number)
                    new_node.score = 2*get_pts(self.player_number, new_node.state[0]) - get_pts(opponent_player_number, new_node.state[0])
                    # move_node_dict[new_node] = move
                    new_node_list.append(new_node)


            # new_node_list.sort(key = lambda x : x.score, reverse = True)


            total_states = total_states+ len(valid_moves)

            node.numChildren += len(valid_moves)        # Incrementing no of children of node
        
            # Leaf State
            if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                node.value = 2*get_pts(self.player_number, node.state[0]) - get_pts(opponent_player_number, node.state[0])
                return node.value
                
            else:
                
                # Non Leaf State

                # # new_node_list = []
                # for move in valid_moves:
                #     new_node = node.transition(move, player_number)
                #     value(new_node, depth_limit - 1)


                if node.isMax:
                    #total_states = total_states + len(valid_moves)
                    new_node_list.sort(key = lambda x : x.score, reverse = True)
                    return max_value(node, depth_limit, new_node_list, player_number, alpha, beta)
                else:
                    #total_states = total_states + len(valid_moves)
                    new_node_list.sort(key = lambda x : x.score, reverse = False)
                    return min_value(node, depth_limit, new_node_list, player_number, alpha, beta)

        valid_moves = get_valid_actions(self.player_number, state)     # List of valid moves
        b = len(valid_moves)
        print('branching factor = ', b)

        # if (b > 15) :
        #     depth_limit = 3 + 2
        # elif (b == 15) :
        #     depth_limit = 4+ 2
        # elif (b == 14) :
        #     depth_limit = 4 + 2
        # elif (b == 13) :
        #     depth_limit = 4 + 2
        # elif (b == 12) :
        #     depth_limit = 4 + 2          
        # elif (b == 11) :
        #     depth_limit = 5 + 2
        # elif (b == 10) :
        #     depth_limit = 5 + 2
        # elif (b == 9) :
        #     depth_limit = 6 + 2
        # elif (b == 8) :
        #     depth_limit = 6 + 2  
        # elif (b == 7) :
        #     depth_limit = 7 + 2
        # elif (b == 6) :
        #     depth_limit = 7 + 2
        # elif (b == 5) :
        #     depth_limit = 9 + 2
        # elif (b == 4) :
        #     depth_limit = 9 + 2
        # elif (b == 3) :
        #     depth_limit = 16 + 2
        # elif (b == 2) :
        #     depth_limit = 16 + 2          
        # else :
        #     depth_limit = 20 + 2   


        depth_limit = 3
        # iteration_time = 0
        # time_remaining = time_limit - (time.time() - start_time)

        # while (iteration_time < time_remaining/b):
        while (True):
            # iteration_time = - time.time()
            max_d = depth_limit
            root_node = TreeNode(state=state, value= -sys.maxsize, isMax=True, parent= None, action=(-1,False), numChildren=0, score = 0)            
            print('depth limit = ', depth_limit)

            try :
                # value(root_node, depth_limit)
                value(root_node, depth_limit, -sys.maxsize, sys.maxsize)
            except : 
                print('final_move = ', final_move)
                
    

                    
                break 
            else :
                # print('Total no of visited states: ', total_states)
                print('final_move = ', final_move)

                depth_limit = depth_limit + 1
                # iteration_time += time.time()
                # time_remaining = time_limit - (time.time() - start_time)
                
                # print('iteration_time = ', iteration_time)
                # print('time_remaining = ', time_remaining)

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
        # final_move = (0,False)      # Initialisation

        # Without alpha beta pruning


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
                # node.value = min(v, node.value)
                node.value += v/node.numChildren
            # node.value = (node.value/node.numChildren)
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
                
            #print("Player Number : ", player_number)
            #print("IsMax : ", node.isMax)
            valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves
            total_states = total_states + len(valid_moves)

            node.numChildren = len(valid_moves)        # Incrementing no of children of node

            # print("Number of children : ", node.numChildren)
        
            # Leaf State
            if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                node.value = 2*get_pts(self.player_number, node.state[0]) - get_pts(opponent_player_number, node.state[0]) 
                return node.value
                
            else:
                
                # Non Leaf State

                # # new_node_list = []
                # for move in valid_moves:
                #     new_node = node.transition(move, player_number)
                #     value(new_node, depth_limit - 1)


                if node.isMax:
                    return max_value(node, depth_limit, valid_moves, player_number)
                else:
                    return expected_value(node, depth_limit, valid_moves, player_number)

        valid_moves = get_valid_actions(self.player_number, state)     # List of valid moves
        b = len(valid_moves)
        print('branching factor = ', b)

        # if (b > 15) :
        #     depth_limit = 3
        # elif (b == 15) :
        #     depth_limit = 3
        # elif (b == 14) :
        #     depth_limit = 3
        # elif (b == 13) :
        #     depth_limit = 3
        # elif (b == 12) :
        #     depth_limit = 3          
        # elif (b == 11) :
        #     depth_limit = 3
        # elif (b == 10) :
        #     depth_limit = 3
        # elif (b == 9) :
        #     depth_limit = 4
        # elif (b == 8) :
        #     depth_limit = 4  
        # elif (b == 7) :
        #     depth_limit = 4
        # elif (b == 6) :
        #     depth_limit = 5
        # elif (b == 5) :
        #     depth_limit = 5
        # elif (b == 4) :
        #     depth_limit = 6
        # elif (b == 3) :
        #     depth_limit = 8
        # elif (b == 2) :
        #     depth_limit = 8       
        # else :
        #     depth_limit = 10

        # max_d = depth_limit
        # root_node = TreeNode(state=state, value= - sys.maxsize, isMax=True, parent= None, action=(-1,False), numChildren=0, score = 0)
        # value(root_node, depth_limit)

        # #value(root_node, depth_limit, -sys.maxsize, sys.maxsize)

        # print('Total no of visited states: ', total_states)
        # # print('best_move = ', final_move)
        # return final_move

        depth_limit = 3
        # iteration_time = 0
        # time_remaining = time_limit - (time.time() - start_time)

        # while (iteration_time < time_remaining/b):
        while (True):
            # iteration_time = - time.time()
            max_d = depth_limit
            root_node = TreeNode(state=state, value= -sys.maxsize, isMax=True, parent= None, action=(-1,False), numChildren=0, score = 0)
            print('depth limit = ', depth_limit)
            
            try :
                value(root_node, depth_limit)
                # value(root_node, depth_limit, -sys.maxsize, sys.maxsize)
            except : 
                print('final_move = ', final_move)
                break 
            else :
                # print('Total no of visited states: ', total_states)
                print('final_move = ', final_move)

                depth_limit = depth_limit + 1
                # iteration_time += time.time()
                # time_remaining = time_limit - (time.time() - start_time)
                
                # print('iteration_time = ', iteration_time)
                # print('time_remaining = ', time_remaining)


        return final_move        
        #raise NotImplementedError('Whoops I don\'t know what to do')


        # Do the rest of your implementation here

        
        # total_states = 1
        # final_move = (-1,False)      # Initialisation
        # # final_move = (0,False)      # Initialisation

        # # Depth limited DFS
        # def dfs(node:TreeNode, depth_limit):
        #     nonlocal total_states
        #     nonlocal final_move
        #     # final_move = (-1,False)
        #     # nonlocal root_node
        #     # print("Root state: ", root_node.state[0])
            
        #     opponent_player_number = 1

        #     if self.player_number == 1:
        #         opponent_player_number = 2
        #     else:
        #         opponent_player_number = 1

        #     # Setting the player number
        #     player_number = self.player_number
        #     if node.isMax == False:
        #         if self.player_number==1:
        #             player_number = 2
        #         else:
        #             player_number = 1
                
        #     #print("Player Number : ", player_number)
        #     #print("IsMax : ", node.isMax)
        #     valid_moves = get_valid_actions(player_number, node.state)     # List of valid moves
        #     total_states = total_states+ len(valid_moves)

        #     node.numChildren += len(valid_moves)        # Incrementing no of children of node
        
        #     # Leaf State
        #     if depth_limit == 0 or len(valid_moves) == 0:                       # If depth limit reached or no valid moves
                
                
        #         # curr_player_number = player_number
        #         child_score = get_pts(self.player_number, node.state[0]) - get_pts(opponent_player_number, node.state[0])
        #         curr = node.parent
        #         prev_child = node

                
        #         # Backtrack to update scores for each parent
        #         while curr is not None:
        #             #print("child score is = ", child_score)
        #             # print("Depth: ", depth_limit)      
        #             # print("Current player number: ", curr_player_number)
        #             # print("Child Score: ", child_score)
        #             # print("Prev Child: ", prev_child)      


        #             if curr.isMax == False:
        #                 print('expected curr value = ', curr.value)  
        #                 # curr.value = min(curr.value, child_score)
        #                 curr.value += (child_score/curr.numChildren)
        #             else :
        #                 #print('max curr value = ', curr.value)                            
        #                 if (curr.parent == None) and child_score > curr.value:
        #                     final_move = prev_child.action
        #                     print("Final Move updated to : ", final_move)
        #                 curr.value = max(curr.value, child_score)

        #             # # Updating the player number
        #             # if curr_player_number==1:
        #             #     curr_player_number = 2
        #             # else:
        #             #     curr_player_number = 1

        #             # Updating the child and curr parameters
                    
        #             #child_score = get_pts(self.player_number, curr.state[0])
        #             child_score = curr.value
        #             #print('curr state board = ', curr.state[0])
        #             prev_child = curr
        #             curr  = curr.parent
                
        #         #print('modified final_move = ', final_move)
                
        #     else:
                
        #         # Non Leaf State

        #         # new_node_list = []
        #         for move in valid_moves:
        #             new_node = node.transition(move, player_number)
        #             dfs(new_node, depth_limit - 1)                 

        #             # try:
        #             #     new_node = node.transition(move, player_number)
        #             #     dfs(new_node, depth_limit - 1)
        #             # except: 
        #             #     print('move : ', move)
        #             #     print('player_number = ', player_number)
        #             #     raise Exception
        #             # finally: 
        #             #     pass

        # depth_limit = 4
        # root_node = TreeNode(state=state, value= 0, isMax=True, parent= None, action=(-1,False), numChildren=0)
        
        # dfs(root_node, depth_limit)

        # print('Total no of visited states: ', total_states)
        # # print('best_move = ', final_move)
        # return final_move
        # #raise NotImplementedError('Whoops I don\'t know what to do')
        
        
class TreeNode:
    def __init__(self, state: Tuple[np.array, Dict[int, Integer]], value: int, isMax: bool, parent, action:Tuple[int, bool], numChildren:int, score:int):
        self.state = state
        self.value = value
        self.isMax = isMax
        self.parent = parent
        self.action = action
        self.numChildren = numChildren
        self.score = score
        # self.alpha = -sys.maxsize
        # self.beta = sys.maxsize
        
    def transition(self, action:Tuple[int, bool], player_number:int):
        board = copy.deepcopy(self.state[0])
        popout_dict = copy.deepcopy(self.state[1])
        #print('init board = ', board)
        col, isPopout = action
        r = board.shape[0]     # No of Rows in board array
        #c = board.shape[1]     # No of Columns in board array
        if isPopout == True:     # Pop out move - we need to change the pop out dictionary as well as the state table
            # print('popouts remaining before = ', popout_dict[player_number].get_int())
            popout_dict[player_number].decrement()
            # print('popouts remaining after = ', popout_dict[player_number].get_int())
            # print('popouts remaining original = ', self.state[1][player_number].get_int())

            # print('[].extend(board[:,col][:-1] = ', [0].append(board[:,col][:-1]))
            temp = [0]
            temp.extend(board[:,col][:-1])
            board[:,col] = temp       # Update the board state
            # print('board[:,col] = ', board[:,col])
            
        else:       # Normal move
            for row in range(r-1,-1,-1):
                if board[row][col] == 0: # Adding player token in bottomost unfilled row
                    board[row][col] = player_number
                    break
        new_s = (board, popout_dict)      

        new_value = - sys.maxsize
        if(self.isMax): 
            new_value = sys.maxsize
        # else:
        #     new_value = 0
        next_node = TreeNode(state=new_s, value = new_value, isMax= not self.isMax, parent= self, action= action, numChildren=0, score = 0) 
        #print('final board = ', next_node.state[0])

        return next_node    

    # def copy(self):
    #     state_dup = (self.state[0].copy(), self.state[1].copy())
    #     parent_dup = None
    #     node_dup = TreeNode(state=state_dup,value=self.value,isMax=self.isMax, parent=parent_dup, action=self.action,numChildren=self.numChildren)
    #     return node_dup