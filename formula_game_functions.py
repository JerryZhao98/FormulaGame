"""
# Jerry Zhao
# Copyright Nick Cheng, 2016
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment

# Add your functions here.


def build_tree(formula):
    try:
        return build_tree_helper(formula)
    # To return a NoneType for invalid formulas
    except:
        return None


def build_tree_helper(formula):
    ''' (str) -> FormulaTree
    Takes in a string (formula) and returns the FormulaTree that represents
    formula if it is a valid formula. Otherwise None is returned
    REQ: formula must be a valid string formula
    >>> asdf = build_tree("((-x+y)*-(-y+x))")
    >>> print(asdf)
    AndTree(OrTree(NotTree(Leaf('x')), Leaf('y')),
    NotTree(OrTree(NotTree(Leaf('y')), Leaf('x'))))
    >>> asdf = build_tree("((-x+y)*-(-y+x)")
    >>> print(asdf)
    None
    >>> asdf = build_tree("(x+y")
    >>> print(asdf)
    None
    >>> asdf = build_tree("x+y")
    >>> print(asdf)
    None
    >>> asdf = build_tree("x+y)")
    >>> print(asdf)
    None
    >>> asdf = build_tree("x+y*x")
    >>> print(asdf)
    None
    >>> asdf = build_tree("x")
    >>> print(asdf)
    Leaf('x')
    >>> asdf = build_tree("-y")
    >>> print(asdf)
    NotTree(Leaf('y'))
    >>> asdf = build_tree("(x*y)")
    >>> print(asdf)
    AndTree(Leaf('x'), Leaf('y'))
    >>> asdf = build_tree("X")
    >>> print(asdf)
    None
    >>> asdf = build_tree("x*y")
    >>> print(asdf)
    None
    >>> asdf = build_tree("-(x)")
    >>> print(asdf)
    None
    >>> asdf = build_tree("(x+(y)*z)")
    >>> print(asdf)
    None
    '''
    # Checks if current character is a NOT operation
    if (formula[0] == "-"):
        # Adds a NotTree to the FormulaTree
        return NotTree(build_tree_helper(formula[1:]))
    # Checks if current character is a valid variable
    if (len(formula) == 1 and formula[0].islower()):
        # Adds a Leaf to the FormulaTree
        return Leaf(formula[0])
    # Counter for keeping track of brackets
    counter = 0
    # Keeps track of the formula(s) within the current bracket
    lastIndex = len(formula) - 1
    # Goes through each character of the current string
    for i in range(1, lastIndex):
        # Keeps track of brackets
        if (formula[i] == "("):
            counter += 1
        elif (formula[i] == ")"):
            counter -= 1
        # If it finds the current operation
        elif (counter == 0):
            # If current operation is an OR
            if (formula[i] == "+"):
                # Adds an OrTree to the FormulaTree
                return OrTree(build_tree_helper(formula[1:i]),
                              build_tree_helper(formula[i + 1: lastIndex]))
            # If current operation is an AND
            if (formula[i] == "*"):
                # Adds an AndTree to the FormulaTree
                return AndTree(build_tree_helper(formula[1:i]),
                               build_tree_helper(formula[i + 1: lastIndex]))
    # For invalid formulas so a NoneType can be returned
    raise Exception()


def draw_formula_tree(root):
    # Adds the default value for depth
    return draw_formula_tree_helper(root, "  ")


def draw_formula_tree_helper(root, depth):
    ''' (FormulaTree, str) -> str
    Takes in a FormulaTree rooted at root as well as an initial depth (depth)
    and returns the string that draws that tree.
    REQ: root is a valid FormulaTree
    REQ: depth is a valid str. Default value should be 2 spaces
    >>> asdf = build_tree("((-x+y)*-(-y+x))")
    >>> print(draw_formula_tree(asdf))
    * - + x
          - y
      + y
        - x
    '''
    # Starts off with current operation or variable
    branchStr = root.symbol
    # Checks if it is an OR/AND operation
    if (root.symbol == "+" or root.symbol == "*"):
        # Draws both branches of an OR/AND operation
        branchStr += (" " +
                      draw_formula_tree_helper(root.children[1],
                                               depth + "  ") +
                      "\n" + depth +
                      draw_formula_tree_helper(root.children[0],
                                               depth + "  "))
    # Checks if it is a NOT operation
    elif (root.symbol == "-"):
        # Draws the single branch of the NOT operation
        branchStr += (" " +
                      draw_formula_tree_helper(root.children[0], depth +
                                               "  "))
    # Returns the current branch
    return branchStr


def evaluate(root, variables, values):
    # Initialized a dictionary for storing int values
    valueDict = {}
    # Goes through all the variables
    for i in range(0, len(variables)):
        # Keys the corresponding value to the variable
        valueDict[variables[i]] = int(values[i])
    # Passes the dictionary to the helper function
    return evaluate_helper(root, valueDict)


def evaluate_helper(root, valueDict):
    ''' (FormulaTree, dict) -> int
    Takes in a formula represented by the FormulaTree rooted at root, along
    with a dictionary of integer values keyed to string variables and will
    return the truth value (1 or 0) of the formula.
    REQ: root is a valid FormulaTree
    REQ: valueDict is a valid dictionary with correct variables keyed to
    values of either 1 or 0
    >>> asdf = build_tree("((-x+y)*-(-y+x))")
    >>> print(evaluate(asdf, "xy", "00"))
    0
    >>> print(evaluate(asdf, "xy", "01"))
    1
    >>> print(evaluate(asdf, "xy", "10"))
    0
    >>> print(evaluate(asdf, "xy", "11"))
    0
    '''
    # Checks if it is an OR operation
    if (root.symbol == "+"):
        # Returns the calculated value of its branches
        return max(evaluate_helper(root.children[0], valueDict),
                   evaluate_helper(root.children[1], valueDict))
    # Checks if it is an AND operation
    if (root.symbol == "*"):
        # Returns the calculated value of its branches
        return min(evaluate_helper(root.children[0], valueDict),
                   evaluate_helper(root.children[1], valueDict))
    # Checks if it is a NOT operation
    if (root.symbol == "-"):
        # Returns the calculated value of its branch
        return 1 - evaluate_helper(root.children[0], valueDict)
    # Returns the value of the variable
    return valueDict[root.symbol]


def play2win(root, turns, variables, values):
    ''' (FormulaTree, str, str, str) -> int
    Takes the formula game configuration given by root, turns, variables,
    and values, and returns the best next move for the player whose turn is
    next. The formula part of the configuration is represented by the
    FormulaTree rooted at root. Player A will prefer 0 if there is no winning
    strategry, or if choosing 1 or 0 will result in the same outcome. The
    same goes for player E and choosing 1.
    REQ: root is a valid FormulaTree
    REQ: turns must be greater length than values. Also must only contain
    "A" or "E"
    REQ: values must only contain "1" or "0" and be shorter than turns
    REQ: variables must be the same length as turns and contain the value of
    all variables in the FormulaTree
    >>> asdf = build_tree("((x+y)*((y+z)*(-y+-z)))")
    >>> print(play2win(asdf, "EEA", "xyz", "0"))
    1
    >>> asdf = build_tree("-(x+y)")
    >>> print(play2win(asdf, "EE", "xy", ""))
    0
    '''
    # Calculates the turns left in the game
    turnsLeft = len(variables) - len(values)
    # Calculates the number of possible move variations left in the game
    possibleMoves = pow(2, turnsLeft)
    # Initialized a dictionary for the potential outcomes and possible moves
    outcomeDict = {}
    # Calculates the outcome of all the possible moves left in the game
    for i in range(0, possibleMoves):
        # Converts move to a binary number
        newValue = values + str(bin(i)[2:].zfill(turnsLeft))
        # Adds the outcome calculated with evaluate() function
        # to the dictionary
        outcomeDict[bin(i)[2:].zfill(turnsLeft)] = evaluate(root,
                                                            variables,
                                                            newValue)
    # Calculates number of future turns
    futureTurns = turns[len(values):]
    # Checks which player's turn it is
    player = futureTurns[0]
    # Calculates the player's desired outcome to win
    winningNumber = 1
    if (player == "A"):
        winningNumber = 0
    # Initializes lists to calculate best possible move
    winningMoveZero = (len(futureTurns) + 1) * [3]
    winningMoveOne = (len(futureTurns) + 1) * [3]
    # Sets both moves (0 and 1) to a non winnable move
    winningMoveZero[0] = False
    winningMoveOne[0] = False
    # Goes through each outcome and keeps track of it's data
    for i in outcomeDict:
        # Checks if the outcome of the current move set is desirable
        if (outcomeDict[i] == winningNumber):
            # Checks if player needs to play a 0
            if (i[0] == "0"):
                # Sets 0 as a winnable move
                winningMoveZero[0] = True
                # Goes through the move set
                for j in range(1, len(i)):
                    # Checks which move the opponent has to play for outcome
                    # and keeps track of it in the list
                    if (futureTurns[j] is not player):
                        # Checks if opponent has to play a 0
                        if (i[j] == "0"):
                            if (winningMoveZero[j] == 3 or
                                    winningMoveZero[j] == 0):
                                winningMoveZero[j] = 0
                            else:
                                winningMoveZero[j] = 2
                        # Checks if opponent has to play a 1
                        else:
                            if (winningMoveZero[j] == 3 or
                                    winningMoveZero[j] == 1):
                                winningMoveZero[j] = 1
                            else:
                                winningMoveZero[j] = 2
            # Checks if player needs to play a 1
            else:
                # Sets 1 as a winnable move
                winningMoveOne[0] = True
                # Goes through the move set
                for j in range(1, len(i)):
                    # Checks which move the opponent has to play for outcome
                    # and keeps track of it in the list
                    if (futureTurns[j] is not player):
                        # Checks if opponent has to play a 0
                        if (i[j] == "0"):
                            if (winningMoveOne[j] == 3 or
                                    winningMoveOne[j] == 0):
                                winningMoveOne[j] = 0
                            else:
                                winningMoveOne[j] = 2
                        # Checks if opponent has to play a 1
                        else:
                            if (winningMoveOne[j] == 3 or
                                    winningMoveOne[j] == 1):
                                winningMoveOne[j] = 1
                            else:
                                winningMoveOne[j] = 2
    # Checks if scenario suggests for either player to play a 1
    if (winningMoveOne[0]):
        if (not winningMoveZero[0]):
            return 1
        elif (0 not in winningMoveOne and 1 not in winningMoveOne and
              (0 in winningMoveZero or 1 in winningMoveZero)):
            return 1
    # Checks if scenario suggests for either player to play a 0
    if (winningMoveZero[0]):
        if (not winningMoveOne[0]):
            return 0
        elif ((0 in winningMoveOne or 1 in winningMoveOne) and
              0 not in winningMoveZero and 1 not in winningMoveZero):
            return 0
    # Else returns the player's default move
    return winningNumber