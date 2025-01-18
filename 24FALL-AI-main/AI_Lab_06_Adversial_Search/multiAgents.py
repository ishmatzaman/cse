from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function returns the score of the state.
    The score is accessed directly from the GameState object.
    """
    return currentGameState.getScore()

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.
    """

    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) 
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()

        # Distance to the closest food
        foodList = newFood.asList()
        foodDistances = [manhattanDistance(newPos, food) for food in foodList]
        closestFoodDist = min(foodDistances) if foodDistances else 0

        # Distance to ghosts
        ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
        closestGhostDist = min(ghostDistances) if ghostDistances else float('inf')

        # Calculate score considering food an - closestFoodDist
        if closestGhostDist < 2:  # Avoid ghosts
            score -= 10
        return score

class MultiAgentSearchAgent(Agent):
    """
      Common elements for all multi-agent searchers.
    """
    def __init__(self, evalFn='scoreEvaluationFunction', depth='4'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Implements the Minimax algorithm.
    """

    def getAction(self, gameState):
        action, score = self.minimax(0, 0, gameState)
        return action

    def minimax(self, curr_depth, agent_index, gameState):
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
            curr_depth += 1
        if curr_depth == self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)
        
        if agent_index == 0:  # Maximizing player (Pacman)
            best_score = float('-inf')
            best_action = None
            for action in gameState.getLegalActions(agent_index):
                next_game_state = gameState.generateSuccessor(agent_index, action)
                _, score = self.minimax(curr_depth, agent_index + 1, next_game_state)
                if score > best_score:
                    best_score = score
                    best_action = action
            return best_action, best_score
        else:  # Minimizing player (Ghosts)
            best_score = float('inf')
            best_action = None
            for action in gameState.getLegalActions(agent_index):
                next_game_state = gameState.generateSuccessor(agent_index, action)
                _, score = self.minimax(curr_depth, agent_index + 1, next_game_state)
                if score < best_score:
                    best_score = score
                    best_action = action
            return best_action, best_score

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Implements Alpha-Beta Pruning.
    """

    def getAction(self, gameState):
        action, score = self.alphabeta(0, 0, gameState, float('-inf'), float('inf'))
        return action

    def alphabeta(self, curr_depth, agent_index, gameState, alpha, beta):
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
            curr_depth += 1
        if curr_depth == self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)
        
        if agent_index == 0:  # Maximizing player (Pacman)
            best_score = float('-inf')
            best_action = None
            for action in gameState.getLegalActions(agent_index):
                next_game_state = gameState.generateSuccessor(agent_index, action)
                _, score = self.alphabeta(curr_depth, agent_index + 1, next_game_state, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_action = action
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_action, best_score
        else:  # Minimizing player (Ghosts)
            best_score = float('inf')
            best_action = None
            for action in gameState.getLegalActions(agent_index):
                next_game_state = gameState.generateSuccessor(agent_index, action)
                _, score = self.alphabeta(curr_depth, agent_index + 1, next_game_state, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_action = action
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_action, best_score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Implements Expectimax search.
    """

    def getAction(self, gameState):
        action, score = self.expectimax(0, 0, gameState)
        return action

    def expectimax(self, curr_depth, agent_index, gameState):
        if agent_index >= gameState.getNumAgents():
            agent_index = 0
            curr_depth += 1
        if curr_depth == self.depth or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)
        
        if agent_index == 0:  # Maximizing player (Pacman)
            best_score = float('-inf')
            best_action = None
            for action in gameState.getLegalActions(agent_index):
                next_game_state = gameState.generateSuccessor(agent_index, action)
                _, score = self.expectimax(curr_depth, agent_index + 1, next_game_state)
                if score > best_score:
                    best_score = score
                    best_action = action
            return best_action, best_score
        else:  # Chance node (Ghosts)
            scores = []
            for action in gameState.getLegalActions(agent_index):
                next_game_state = gameState.generateSuccessor(agent_index, action)
                _, score = self.expectimax(curr_depth, agent_index + 1, next_game_state)
                scores.append(score)
            avg_score = sum(scores) / len(scores) if scores else 0
            return None, avg_score

def betterEvaluationFunction(currentGameState):
    """
      Improved evaluation function for Pacman.
    """
    position = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    score = currentGameState.getScore()

    foodDistances = [manhattanDistance(position, foodPos) for foodPos in food.asList()]
    closestFoodDist = min(foodDistances) if foodDistances else 1

    ghostDistances = [manhattanDistance(position, ghost.getPosition()) for ghost in ghostStates]
    closestGhostDist = min(ghostDistances) if ghostDistances else float('inf')

    score += max(1 / closestFoodDist, 0.5) - max(2 / (closestGhostDist + 1), 0.2)
    return score

# Abbreviation
better = betterEvaluationFunction
