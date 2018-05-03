import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import matplotlib.pyplot as plt

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.q = {}
        self.epsilon = 0.1
        self.alpha = 0.2
        self.gamma = 0.9
        self.actions = self.env.valid_actions
        self.newState = None
        self.invalidMoves = 0
        self.validMoves = 0
        #self.invalidRatio = []
        self.reached = 0
        self.accList =[]

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
#        self.invalidMoves = 0
#        self.validMoves = 0
        self.state = None
        self.newState = None
        
    def chooseRandomAction(self, state):
        return random.choice(self.actions)
        
    def chooseAction(self, state):
        if random.random() < self.epsilon:
            action = random.choice(self.actions)
        else:
            q = [self.getQ(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = random.choice(best)
            else:
                i = q.index(maxQ)
            action = self.actions[i]
        return action
        
    def getQ(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        oldv = self.q.get((state, action), None)
        if oldv is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = oldv + self.alpha * (value - oldv)
            
    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.getQ(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)
    
    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        
        # TODO: Update state
        self.state = inputs + (self.next_waypoint,) 
        # TODO: Select action according to your policy        
        action = self.chooseAction(self.state)
        # Execute action and get reward
        reward = self.env.act(self, action)
        if reward < -0.5:
            self.invalidMoves += 1
        else:
            self.validMoves +=1
        
        # TODO: Learn policy based on state, action, reward
        self.newState = self.env.sense(self) + (self.planner.next_waypoint(),)
        self.learn(self.state, action, reward, self.newState)
        

        print "LearningAgent.update(): deadline = {}, oldstate = {}, newstate = {}, action = {}, reward = {}".format(deadline, self.state, self.newState, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline= True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.0001)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    print sum(sim.env.primary_agent.accList)
    print sum(sim.env.primary_agent.accList[70:100])/float(30)
#    for qkey in sim.env.primary_agent.q:
#        print qkey, sim.env.primary_agent.q[qkey]
if __name__ == '__main__':
    run()
