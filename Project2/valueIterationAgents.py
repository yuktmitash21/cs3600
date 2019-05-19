# valueIterationAgents.py
# -----------------------
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


import mdp, util, random

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        start = 0

        while start < iterations:
            #substitute dictionary
            substitute = util.Counter()
            index = 0
            biggestQ = 0

            #loop through all states
            for state in self.mdp.getStates():


                #if the state is terminal, do not loop through
                if self.mdp.isTerminal(state) == False:
                    actionArr = self.mdp.getPossibleActions(state)

                    #copute Q(s,a) for first action
                    biggestQ = self.computeQValueFromValues(state, actionArr[0])

                    #loop through all actions to find maximum Q(state, action)
                    for action in actionArr:
                        possibleQ = self.computeQValueFromValues(state, action)
                        if (possibleQ > biggestQ):
                            biggestQ = possibleQ
                            #self.values[state] = biggestQ
                    substitute[state] = biggestQ
                    #self.values[state] = biggestQ
                index = index + 1
                #self.values[state] = biggestQ

                #if all states have been checked transfer values to actual dictionary
                if index == len(self.mdp.getStates()):
                    for key in substitute.keys():
                        self.values[key] = substitute[key]


            start = start + 1




    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        #get all possible actions from current state
        possibleActions = self.mdp.getPossibleActions(state)

        #if action is illegal return 0
        if action in possibleActions:
            transitions = self.mdp.getTransitionStatesAndProbs(state, action)
            returnVal = 0
            index = 0

            #loop through all trainsitions/probabilities
            while index < len(transitions):
                #This returns s' and T(s, a, s')
                (nextState, prob) = transitions[index]


                #This returns R(s,a,s')
                rewardVal = self.mdp.getReward(state, action, nextState)

                #This is gamma * V(s')
                lastPartOfEquation = self.values[nextState] *self.discount

                #This is T(s, a, s')[R(s, a, s') + gamma * V(s'). Bellman equation
                returnVal = returnVal + prob * (rewardVal + lastPartOfEquation)
                index = index + 1

            return returnVal
        else:
            return 0

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"



        #check if teminal
        if self.mdp.isTerminal(state):
            return None
        else:
            # get all actions for state
            actionArr = self.mdp.getPossibleActions(state)

            #Q val and action at index 0 of action Array
            currentQ = self.computeQValueFromValues(state, actionArr[0])
            currentAction = actionArr[0]

            #loop through action Array
            for action in actionArr:
                #compute q at each index
                possibleQ = self.computeQValueFromValues(state, action)

                if (possibleQ == currentQ):
                   currentAction = random.choice([currentAction, action])


                elif (possibleQ > currentQ):
                    # want to return action for greatest Q value
                    currentAction = action
                    # update Q to keep track of corresponding value
                    currentQ = possibleQ




            return currentAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
