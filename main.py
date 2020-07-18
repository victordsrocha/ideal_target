from simulation.simulation import Simulation
from agent.agent import Agent

agent = Agent()

simulation = Simulation(agent)

simulation.run(10)
