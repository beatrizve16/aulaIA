# seuPacManAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
 
from util import manhattanDistance
from game import Directions
import random, util
 
from game import Agent
from pacman import GameState
from multiAgents import MultiAgentSearchAgent
 
 
class MinimaxAgent(MultiAgentSearchAgent):
 
    def getAction(self, gameState: GameState):
 
        def minimax(agentIndex=0, depth=0, state=gameState):
         
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None
 
            numAgents   = state.getNumAgents()
            isLastAgent = (agentIndex == numAgents - 1)
            nextAgent   = 0          if isLastAgent else agentIndex + 1
            nextDepth   = depth + 1  if isLastAgent else depth
 
         
            scores_and_actions = []
            for action in state.getLegalActions(agentIndex):
                successor = state.generateSuccessor(agentIndex, action)
                score, _  = minimax(nextAgent, nextDepth, successor)
                scores_and_actions.append((score, action))
       
 
    
            if agentIndex == 0:  
                return max(scores_and_actions, key=lambda x: x[0])
            else:                 
                return min(scores_and_actions, key=lambda x: x[0])
      
 

        _, best_action = minimax()
        return best_action
 
 
 
def betterEvaluationFunction(currentGameState: GameState):

    pos         = currentGameState.getPacmanPosition()
    food        = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
 

    foodDistances    = [manhattanDistance(pos, f) for f in food]
    minFoodDistance  = min(foodDistances) if foodDistances else 0
 

    ghostDistances   = [manhattanDistance(pos, g.getPosition()) for g in ghostStates]
    minGhostDistance = min(ghostDistances) if ghostDistances else 1
 

    scaredTimes = [g.scaredTimer for g in ghostStates]
    if min(scaredTimes) > 0:
        minGhostDistance = float('inf')
 
    score  = currentGameState.getScore()
    score -= 1.5 / (minFoodDistance  + 1)   
    score += 2.0 / (minGhostDistance + 1)  
 
    return score
 
 

better = betterEvaluationFunction
