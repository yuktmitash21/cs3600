# inference.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import itertools
import util
import random
import busters
import game

class InferenceModule:
    """
    An inference module tracks a belief distribution over a ghost's location.
    This is an abstract class, which you should not modify.
    """

    ############################################
    # Useful methods for all inference modules #
    ############################################

    def __init__(self, ghostAgent):
        "Sets the ghost agent for later access"
        self.ghostAgent = ghostAgent
        self.index = ghostAgent.index
        self.obs = [] # most recent observation position

    def getJailPosition(self):
        return (2 * self.ghostAgent.index - 1, 1)

    def getPositionDistribution(self, gameState):
        """
        Returns a distribution over successor positions of the ghost from the given gameState.

        You must first place the ghost in the gameState, using setGhostPosition below.
        """
        ghostPosition = gameState.getGhostPosition(self.index) # The position you set
        actionDist = self.ghostAgent.getDistribution(gameState)
        dist = util.Counter()
        for action, prob in actionDist.items():
            successorPosition = game.Actions.getSuccessor(ghostPosition, action)
            dist[successorPosition] = prob
        return dist

    def setGhostPosition(self, gameState, ghostPosition):
        """
        Sets the position of the ghost for this inference module to the specified
        position in the supplied gameState.

        Note that calling setGhostPosition does not change the position of the
        ghost in the GameState object used for tracking the true progression of
        the game.  The code in inference.py only ever receives a deep copy of the
        GameState object which is responsible for maintaining game state, not a
        reference to the original object.  Note also that the ghost distance
        observations are stored at the time the GameState object is created, so
        changing the position of the ghost will not affect the functioning of
        observeState.
        """
        conf = game.Configuration(ghostPosition, game.Directions.STOP)
        gameState.data.agentStates[self.index] = game.AgentState(conf, False)
        return gameState

    def observeState(self, gameState):
        "Collects the relevant noisy distance observation and pass it along."
        distances = gameState.getNoisyGhostDistances()
        if len(distances) >= self.index: # Check for missing observations
            obs = distances[self.index - 1]
            self.obs = obs
            self.observe(obs, gameState)

    def initialize(self, gameState):
        "Initializes beliefs to a uniform distribution over all positions."
        # The legal positions do not include the ghost prison cells in the bottom left.
        self.legalPositions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        self.initializeUniformly(gameState)

    ######################################
    # Methods that need to be overridden #
    ######################################

    def initializeUniformly(self, gameState):
        "Sets the belief state to a uniform prior belief over all positions."
        pass

    def observe(self, observation, gameState):
        "Updates beliefs based on the given distance observation and gameState."

        pass

    def elapseTime(self, gameState):
        "Updates beliefs for a time step elapsing from a gameState."
        pass

    def getBeliefDistribution(self):
        """
        Returns the agent's current belief state, a distribution over
        ghost locations conditioned on all evidence so far.
        """
        pass

class ExactInference(InferenceModule):
    """
    The exact dynamic inference module should use forward-algorithm
    updates to compute the exact belief function at each time step.
    """

    def initializeUniformly(self, gameState):
        "Begin with a uniform distribution over ghost positions."
        self.beliefs = util.Counter()
        for p in self.legalPositions: self.beliefs[p] = 1.0
        self.beliefs.normalize()

    def observe(self, observation, gameState):
        """
        Updates beliefs based on the distance observation and Pacman's position.

        The noisyDistance is the estimated manhattan distance to the ghost you are tracking.

        The emissionModel below stores the probability of the noisyDistance for any true
        distance you supply.  That is, it stores P(noisyDistance | TrueDistance).

        self.legalPositions is a list of the possible ghost positions (you
        should only consider positions that are in self.legalPositions).

        A correct implementation will handle the following special case:
          *  When a ghost is captured by Pacman, all beliefs should be updated so
             that the ghost appears in its prison cell, position self.getJailPosition()

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).

        """
        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        print(self.beliefs)
        pacmanPosition = gameState.getPacmanPosition()

        "*** YOUR CODE HERE ***"



        # Replace this code with a correct observation update
        # Be sure to handle the "jail" edge case where the ghost is eaten
        # and noisyDistance is None
        allPossible = util.Counter()

        #loop through all possible positions
        for p in self.legalPositions:

            #if noisy distance is valid recalculate the belief distribution for the current position
            if noisyDistance != None:
                trueDistance = util.manhattanDistance(p, pacmanPosition)

                #multiple the observation distributions value for trueDistance by the current belief distriubution p-val
                allPossible[p] = emissionModel[trueDistance] * self.beliefs.get(p)
            else:

                #otherwise set the jail position to 100%
                allPossible[self.getJailPosition()] = 1

        "*** END YOUR CODE HERE ***"

        allPossible.normalize()
        self.beliefs = allPossible

    def elapseTime(self, gameState):
        """
        Update self.beliefs in response to a time step passing from the current state.

        The transition model is not entirely stationary: it may depend on Pacman's
        current position (e.g., for DirectionalGhost).  However, this is not a problem,
        as Pacman's current position is known.

        In order to obtain the distribution over new positions for the
        ghost, given its previous position (oldPos) as well as Pacman's
        current position, use this line of code:

          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

        Note that you may need to replace "oldPos" with the correct name
        of the variable that you have used to refer to the previous ghost
        position for which you are computing this distribution. You will need to compute
        multiple position distributions for a single update.

        newPosDist is a util.Counter object, where for each position p in self.legalPositions,

        newPostDist[p] = Pr( ghost is at position p at time t + 1 | ghost is at position oldPos at time t )

        (and also given Pacman's current position).  You may also find it useful to loop over key, value pairs
        in newPosDist, like:

          for newPos, prob in newPosDist.items():
            ...

        *** GORY DETAIL AHEAD ***

        As an implementation detail (with which you need not concern
        yourself), the line of code at the top of this comment block for obtaining newPosDist makes
        use of two helper methods provided in InferenceModule above:

          1) self.setGhostPosition(gameState, ghostPosition)
              This method alters the gameState by placing the ghost we're tracking
              in a particular position.  This altered gameState can be used to query
              what the ghost would do in this position.

          2) self.getPositionDistribution(gameState)
              This method uses the ghost agent to determine what positions the ghost
              will move to from the provided gameState.  The ghost must be placed
              in the gameState with a call to self.setGhostPosition above.

        It is worthwhile, however, to understand why these two helper methods are used and how they
        combine to give us a belief distribution over new positions after a time update from a particular position
        """

        "*** YOUR CODE HERE ***"


        i = 0
        beliefDistribution = util.Counter()


        while i < len(self.legalPositions):

            currentPosition = self.legalPositions[i]

            #distribution for predictiogn the bext position
            newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, currentPosition))

            #loop through all positions at time t
            for keys in newPosDist.keys():

                #the belief for each position at time t + 1 is sum of the beliefs of the corresponding at t
                #times the newPostDist belief in the transition to t+ 1 given t
                if (self.beliefs.get(currentPosition) != None):
                    beliefDistribution[keys] = beliefDistribution[keys] + (self.beliefs.get(currentPosition) * newPosDist[keys])
            i += 1

        #resetting belief distribution
        self.beliefs = beliefDistribution

           # pacmanPosition = gameState.getPacmanPosition()
           # trueDistance = util.manhattanDistance(p, pacmanPosition)
           # allPossible[p] = newPosDist[trueDistance] * self.beliefs.get(p)


        #self.beliefs = allPossible

    def getBeliefDistribution(self):
        return self.beliefs

class ParticleFilter(InferenceModule):
    """
    A particle filter for approximately tracking a single ghost.

    Useful helper functions will include random.choice, which chooses
    an element from a list uniformly at random, and util.sample, which
    samples a key from a Counter by treating its values as probabilities.
    """


    def __init__(self, ghostAgent, numParticles=300):
        InferenceModule.__init__(self, ghostAgent)
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles


    def initializeUniformly(self, gameState):
        """
          Initializes a list of particles. Use self.numParticles for the number of particles.
          Use self.legalPositions for the legal board positions where a particle could be located.
          Particles should be evenly (not randomly) distributed across positions in order to
          ensure a uniform prior.

          ** NOTE **
            the variable you store your particles in must be a list; a list is simply a collection
            of unweighted variables (positions in this case). Storing your particles as a Counter or
            dictionary (where there could be an associated weight with each position) is incorrect
            and will produce errors
        """
        "*** YOUR CODE HERE ***"
        #empty list
        self.list = []

        #the available number divided by the number of legal positions yields the particles per position
        particlesPerPosition = int(self.numParticles / len(self.legalPositions))

        #loop through all positions
        for position in self.legalPositions:
            i = 0

            #at each position append the right number of particles
            while i < particlesPerPosition:
                self.list.append(position)
                i = i + 1



    def observe(self, observation, gameState):
        """
        Update beliefs based on the given distance observation. Make
        sure to handle the special case where all particles have weight
        0 after reweighting based on observation. If this happens,
        recreate particles uniformly from the prior distribution by
        calling initializeUniformly.

        A correct implementation will handle two special cases:
          1) When a ghost is captured by Pacman, **all** particles should be updated so
             that the ghost appears in its prison cell, self.getJailPosition()

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).

          2) When all particles receive 0 weight, they should be recreated from the
             prior distribution by calling initializeUniformly. The total weight
             for a belief distribution can be found by calling totalCount on
             a Counter object

        util.sample(Counter object) is a helper method to generate a sample from
        a belief distribution

        You may also want to use util.manhattanDistance to calculate the distance
        between a particle and pacman's position.
        """

        noisyDistance = observation
        emissionModel = busters.getObservationDistribution(noisyDistance)
        pacmanPosition = gameState.getPacmanPosition()
        #emission model maps dist to probability
        distributionOfBeliefs = util.Counter()
        "*** YOUR CODE HERE ***"

        #checking if ghost is in jail
        if noisyDistance is None:

            #empty list
            newList = []

            #sunce there is only one ghost we can place all particles in jail upon capture
            for i in range(self.numParticles):

                #adding jail particle
                newList.append(self.getJailPosition())

            #resetting list
            self.list = newList
            return
        else:

            #loop through all particles
            for loc in self.list:

                #the distribution will be resampled so set (arbitrary value * numberOfOccurence) for each element in particle
                distributionOfBeliefs[loc] += 68

            #loop through all distances in keyset
            for distance in distributionOfBeliefs.keys():

                #determine ghosts distance from pacman
                truedistance = util.manhattanDistance(pacmanPosition, distance)
                # previousProb = 0
                #  if distributionOfBeliefs[distance] == 0:
                #      previousProb = 1
                #  else:
                #      previousProb = distributionOfBeliefs[distance]

                #current probability of this location based on current sampling
                previousProb = distributionOfBeliefs[distance]

                #multiply this by the emissionModels belief of the distnance of the particle
                probability = emissionModel[truedistance] * previousProb

                #reset distruibution value
                distributionOfBeliefs[distance] = probability



       # print "sampling"
       # print util.sample(distributionOfBeliefs)


            #sum of all beliefs
            sum1 = sum(distributionOfBeliefs.values())

            #in the event of 0 probabilty totalm resample
            if sum1 == 0:
                self.initializeUniformly(gameState)
            else:
                newList = []

                #otherwise loop through list and resample everything based on the distribution
                for i in range(len(self.list)):
                    self.list[i] = util.sample(distributionOfBeliefs)
                    #newList.append(util.sample(distributionOfBeliefs))
                #self.list = newList





    def elapseTime(self, gameState):
        """
        Update beliefs for a time step elapsing.

        As in the elapseTime method of ExactInference, you should use:

          newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, oldPos))

        to obtain the distribution over new positions for the ghost, given
        its previous position (oldPos) as well as Pacman's current
        position.

        util.sample(Counter object) is a helper method to generate a sample from a
        belief distribution
        """

        #allPossible = util.Counter()
        #for p in self.legalPositions:
        #    newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, p))
        #
         #   for keys in newPosDist.keys():
          #      if (self.beliefs.get(p) != None):
          #          allPossible[keys] = allPossible[keys] + (self.beliefs.get(p) * newPosDist[keys])
        #self.beliefs = allPossible
        "*** YOUR CODE HERE ***"
      #  print "NEWPOSTDIST"
      #  print self.getPositionDistribution(self.setGhostPosition(gameState, self.list[0]))

        #since this updating the list instead of the dictionary we can just sample based on likely next positions
        i = 0

        #loop through all legal positions
        for pos in self.list:

            #based on these generate a distribution for likely next position
            newPosDist = self.getPositionDistribution(self.setGhostPosition(gameState, pos))

            #sample from it
            random = util.sample(newPosDist)

            #update list
            self.list[i] = random

            #update index
            i += 1




       # util.raiseNotDefined()

    def getBeliefDistribution(self):
        """
          Return the agent's current belief state, a distribution over
          ghost locations conditioned on all evidence and time passage. This method
          essentially converts a list of particles into a belief distribution (a Counter object)
        """
        "*** YOUR CODE HERE ***"




        #get current list
        # turn list to counter
        list = self.list
        beliefDist = util.Counter()

        #come up with weight for each particle
        adding = 1.0 / self.numParticles
       # print "adding"
        #print adding

        #loop through list
        for particle in list:

            #for each particle set its belief do n * adding, where n is the number of occurences of the particle
            beliefDist[particle] += adding


        return beliefDist

class MarginalInference(InferenceModule):
    "A wrapper around the JointInference module that returns marginal beliefs about ghosts."

    def initializeUniformly(self, gameState):
        "Set the belief state to an initial, prior value."
        if self.index == 1: jointInference.initialize(gameState, self.legalPositions)
        jointInference.addGhostAgent(self.ghostAgent)

    def observeState(self, gameState):
        "Update beliefs based on the given distance observation and gameState."
        if self.index == 1: jointInference.observeState(gameState)

    def elapseTime(self, gameState):
        "Update beliefs for a time step elapsing from a gameState."
        if self.index == 1: jointInference.elapseTime(gameState)

    def getBeliefDistribution(self):
        "Returns the marginal belief over a particular ghost by summing out the others."
        jointDistribution = jointInference.getBeliefDistribution()
        dist = util.Counter()
        for t, prob in jointDistribution.items():
            dist[t[self.index - 1]] += prob
        return dist

class JointParticleFilter:
    "JointParticleFilter tracks a joint distribution over tuples of all ghost positions."

    def __init__(self, numParticles=600):
        self.setNumParticles(numParticles)

    def setNumParticles(self, numParticles):
        self.numParticles = numParticles

    def initialize(self, gameState, legalPositions):
        "Stores information about the game, then initializes particles."
        self.numGhosts = gameState.getNumAgents() - 1
        self.ghostAgents = []
        self.legalPositions = legalPositions
        self.initializeParticles()

    def initializeParticles(self):
        """
        Initialize particles to be consistent with a uniform prior.

        Each particle is a tuple of ghost positions. Use self.numParticles for
        the number of particles. You may find the python package 'itertools' helpful.
        Specifically, you will need to think about permutations of legal ghost
        positions, with the additional understanding that ghosts may occupy the
        same space. Look at the 'product' function in itertools to get an
        implementation of the Cartesian product. Note: If you use
        itertools, keep in mind that permutations are not returned in a random order;
        you must shuffle the list of permutations in order to ensure even placement
        of particles across the board. Use self.legalPositions to obtain a list of
        positions a ghost may occupy.

          ** NOTE **
            the variable you store your particles in must be a list; a list is simply a collection
            of unweighted variables (positions in this case). Storing your particles as a Counter or
            dictionary (where there could be an associated weight with each position) is incorrect
            and will produce errors


        """
        "*** YOUR CODE HERE ***"
        #particlesPerPosition = int(self.numParticles / len(self.legalPositions))

        #initialize a list of all possible permutations of size numGhosts
        ghosts = []

        #randommize it
        ghosts = list(itertools.permutations(self.legalPositions, self.numGhosts))
        random.shuffle(ghosts)

        #initialize list
        self.list = []

        #loop through range of numParticles
        for i in range(self.numParticles):

            #append onto list i % permutation list length of permutation list
            self.list.append(ghosts[i % len(ghosts)])
        #print "ghosts"
        #print self.list




    def addGhostAgent(self, agent):
        "Each ghost agent is registered separately and stored (in case they are different)."
        self.ghostAgents.append(agent)

    def getJailPosition(self, i):
        return (2 * i + 1, 1)

    def observeState(self, gameState):
        """
        Resamples the set of particles using the likelihood of the noisy observations.

        To loop over the ghosts, use:

          for i in range(self.numGhosts):
            ...

        A correct implementation will handle two special cases:
          1) When a ghost is captured by Pacman, all particles should be updated so
             that the ghost appears in its prison cell, position self.getJailPosition(i)
             where "i" is the index of the ghost.

             You can check if a ghost has been captured by Pacman by
             checking if it has a noisyDistance of None (a noisy distance
             of None will be returned if, and only if, the ghost is
             captured).

          2) When all particles receive 0 weight, they should be recreated from the
              prior distribution by calling initializeParticles. After all particles
              are generated randomly, any ghosts that are eaten (have noisyDistance of None)
              must be changed to the jail Position. This will involve changing each
              particle if a ghost has been eaten.

        ** Remember ** We store particles as tuples, but to edit a specific particle,
        it must be converted to a list, edited, and then converted back to a tuple. Since
        this is a common operation when placing a ghost in the jail for a particle, we have
        provided a helper method named self.getParticleWithGhostInJail(particle, ghostIndex)
        that performs these three operations for you.

        """
        pacmanPosition = gameState.getPacmanPosition()
        noisyDistances = gameState.getNoisyGhostDistances()
        if len(noisyDistances) < self.numGhosts: return
        emissionModels = [busters.getObservationDistribution(dist) for dist in noisyDistances]
        beliefDist = util.Counter()

        "*** YOUR CODE HERE ***"

        #loop through all locations in list
        for location in self.list:


            i = 0

            #initialize a float probability of 1.0
            previousProb = 1.0

            #then loop through all ghosts by index
            for j in range(0, self.numGhosts):

                #initialize boolean to false. This is true when noisyDistances[j] i reached
                reachedNone = False

                #if ghost j is in jail
                if noisyDistances[j] is None:
                    #reachedNone = True

                    #turn the tuple to a list
                    newList = list(location)

                    #change the tuple at index j of list to the jail position
                    newList[j] = self.getJailPosition(j)

                    #convert back to tuple
                    newLoc = tuple(newList)
                    location = newLoc
                else:

                    #set reachedNone to False because the last condition was not jail
                    reachedNone = False

                    #manhattan distance
                    distance = util.manhattanDistance(pacmanPosition, location[j])

                    #modify previous probability exactly the same as we have always done.
                    #only difference if we need to index on of the distributions in
                    #emissionsModels based on current ghost
                    previousProb = float(previousProb * emissionModels[j][distance])

            #id the last thing modified was the jail location we need to modify that key
            if reachedNone:
                beliefDist[newLoc] = beliefDist[newLoc] + previousProb


            #otherwise we modify the default key
            else:
                beliefDist[location] = beliefDist[location] + previousProb


        #check if all probabilities are 0
        if sum(beliefDist.values()) == 0:

            #initialize particles
            self.initializeParticles()

            #loop through noisy distances
            ii = 0
            for distance in noisyDistances:

                #if this ghost is in jail, update the tuple accordinglt
                if noisyDistances is None:
                    for i in range(0, len(self.list)):
                        currentParticle = self.list[i]
                        asList = list(currentParticle)
                        asList[ii] = self.getJailPosition(ii)
                        self.list[i] = tuple(asList)
            ii += 1

        #otherwise normalize the distribution
        else:

            #this is total probability
            totalWeight = float(sum(beliefDist.values()))

            #loop through all tuple keys and set their beleief to currentBelief/ total probability
            for key in beliefDist.keys():
                beliefDist[key] = float(beliefDist[key] / totalWeight)

            #make new List
            newList = []

            #loop through whole list
            for i in range (0, self.numParticles):

                #rebuild list by resampling
                newList.append(util.sample(beliefDist))

            #remake list
            self.list = newList





    def getParticleWithGhostInJail(self, particle, ghostIndex):
        particle = list(particle)
        particle[ghostIndex] = self.getJailPosition(ghostIndex)
        return tuple(particle)

    def elapseTime(self, gameState):
        """
        Samples each particle's next state based on its current state and the gameState.

        To loop over the ghosts, use:

          for i in range(self.numGhosts):
            ...

        Then, assuming that "i" refers to the index of the
        ghost, to obtain the distributions over new positions for that
        single ghost, given the list (prevGhostPositions) of previous
        positions of ALL of the ghosts, use this line of code:

          newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, prevGhostPositions),
                                                       i, self.ghostAgents[i])

        **Note** that you may need to replace "prevGhostPositions" with the
        correct name of the variable that you have used to refer to the
        list of the previous positions of all of the ghosts, and you may
        need to replace "i" with the variable you have used to refer to
        the index of the ghost for which you are computing the new
        position distribution.

        As an implementation detail (with which you need not concern
        yourself), the line of code above for obtaining newPosDist makes
        use of two helper functions defined below in this file:

          1) setGhostPositions(gameState, ghostPositions)
              This method alters the gameState by placing the ghosts in the supplied positions.

          2) getPositionDistributionForGhost(gameState, ghostIndex, agent)
              This method uses the supplied ghost agent to determine what positions
              a ghost (ghostIndex) controlled by a particular agent (ghostAgent)
              will move to in the supplied gameState.  All ghosts
              must first be placed in the gameState using setGhostPositions above.

              The ghost agent you are meant to supply is self.ghostAgents[ghostIndex-1],
              but in this project all ghost agents are always the same.
        """
        newParticles = []
        for oldParticle in self.list:
            newParticle = list(oldParticle) # A list of ghost positions

            # now loop through and update each entry in newParticle...
            "*** YOUR CODE HERE ***"

            #loop through every particle
            i = 0

            while i < len(newParticle):

                #create distribution exactly as told except pass in newParticle because that is essentially a list of previous ghost positions
                newPosDist = getPositionDistributionForGhost(setGhostPositions(gameState, newParticle),
                                                             i, self.ghostAgents[i])

                #resamole to determine next ghost positions
                newParticle[i] = util.sample(newPosDist)

                i += 1



            "*** END YOUR CODE HERE ***"
            newParticles.append(tuple(newParticle))
        self.list = newParticles

    def getBeliefDistribution(self):
        "*** YOUR CODE HERE ***"

        #very similar to previous beliefDistribution methods
        beliefDist = util.Counter()
        list = self.list

        #create a weight for each particle
        adding = 1.0 / self.numParticles
        # print "adding"
        # print adding

        #loop through all particles
        for particle in list:

            #set each particle weight to adding * n where n is the number of that specific particle
            beliefDist[particle] += adding
        return beliefDist

# One JointInference module is shared globally across instances of MarginalInference
jointInference = JointParticleFilter()

def getPositionDistributionForGhost(gameState, ghostIndex, agent):
    """
    Returns the distribution over positions for a ghost, using the supplied gameState.
    """

    # index 0 is pacman, but the students think that index 0 is the first ghost.
    ghostPosition = gameState.getGhostPosition(ghostIndex+1)
    actionDist = agent.getDistribution(gameState)
    dist = util.Counter()
    for action, prob in actionDist.items():
        successorPosition = game.Actions.getSuccessor(ghostPosition, action)
        dist[successorPosition] = prob
    return dist

def setGhostPositions(gameState, ghostPositions):
    "Sets the position of all ghosts to the values in ghostPositionTuple."
    for index, pos in enumerate(ghostPositions):
        conf = game.Configuration(pos, game.Directions.STOP)
        gameState.data.agentStates[index + 1] = game.AgentState(conf, False)
    return gameState

