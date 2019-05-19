# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."


        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"

        #dictionary for all Q(s,a). Just like value-iteration, but without mdp object to keep track of R/T
        self.qVals = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.qVals[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        #check for terminal state
        if len(self.getLegalActions(state)) == 0:
            return 0

        #get all possible actions and first action/ first Q (exact same as value-iteration)
        actions = self.getLegalActions(state)
        action1 = actions[0]
        maxQ = self.getQValue(state, action1)

        #find max a' Q(s, a'), or max Q val
        for action in actions:
            currentQ = self.getQValue(state, action)
            if currentQ > maxQ:
                maxQ = currentQ
        #    elif currentQ == maxQ:
        #        maxQ = random.choice([currentQ, maxQ])
        return maxQ


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"

        #get all actions and check for terminal
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None

        #get first Q val and first action
        maxQ = self.getQValue(state, actions[0])
        bestAction = actions[0]

        #find action associated with max Q value
        for action in actions:
            currentQ = self.getQValue(state, action)
            if currentQ > maxQ:
                maxQ = currentQ
                bestAction = action

            #if potential q value is equal, decide on replacement randomly
            elif currentQ == maxQ:
                bestAction = random.choice([action, bestAction])
        return bestAction


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action

        actionList = self.getLegalActions(state)

        #returns true with self.epsilon probability
        probability = util.flipCoin(self.epsilon)

        #if true, explore
        if probability:
            return random.choice(actionList)
        #if false, do basic value-iteration
        else:
            return self.computeActionFromQValues(state)


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"

        #Q(s,a) = (1- alpha)(Q(s,a)) + alpha[reward + gamma *max a' Q(s, a'). Using averaging instead of T function
        self.qVals[(state, action)] = ((1 - self.alpha) * self.qVals[(state, action)]) + self.alpha * (reward + (self.discount * self.computeValueFromQValues(nextState)))



    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action