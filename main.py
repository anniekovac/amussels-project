import numpy
from pprint import pprint as pp


def observation_function(sigma, delta):
	"""
	Calculating observation function for values of sigma and delta.
	Observation function will be calculated only for agents that communicate.
	:param sigma: float
	:param delta: float
	:return: float
	"""
	# ako je delta veci obzervacijska funkcija ce biti sve manja (bliza nuli)
	result = numpy.exp(-(numpy.square(delta) / numpy.square(sigma)))
	return result


def initialize(n, all_communicating=True):
	"""
	Initializing beginning values for trust matrix zeta and
	confidence matrix (sigma).
	:param n: int (number of agents) 
	:param all_communicating: boolean (True if all agents are communicating)
	:return: numpy.array, numpy.array, numpy.array 
	"""
	# zeta = numpy.random.uniform(low=0, high=1, size=(n, n))
	zeta = numpy.array([[1.0, 0.1, 0, 0, 0],
						[0.1, 1.0, 0.1, 0, 0.1],
						[0, 0.1, 1.0, 0.1, 0.1],
						[0, 0, 0.1, 1.0, 0],
						[0, 0.1, 0.1, 0, 1]])
	sigma = numpy.random.uniform(low=0.1, high=0.8, size=(n, n))
	# sigma = numpy.array([[0, 0.7, 0, 0, 0],
	# 					 [1, 0, 1, 0, 1],
	# 					 [0, 0.5, 0, 0.4, 1],
	# 					 [0, 0, 1, 0, 0],
	# 					 [0, 0.4, 1, 0, 0]])
	#
	# A = numpy.array([[0, 1, 0, 0, 0],
	# 				 [1, 0, 1, 0, 1],
	# 				 [0, 1, 0, 1, 1],
	# 				 [0, 0, 1, 0, 0],
	# 				 [0, 1, 1, 0, 0]])

	delta = numpy.array([[0, 0.2, 0, 0, 0],
						  [0.8, 0, 0.4, 0, 1],
						  [0, 0.2, 0, 0.6, 1],
						  [0, 0, 0.4, 0, 0],
						  [0, 0.2, 0.4, 0, 0]])

	A = numpy.ones((n, n))
	for i in range(n):
		A[i, i] = 0  # agent can't communicate to itself
	return (A, zeta, sigma, delta)


def convergence_zeta(zeta, x, A, sigma, number_of_iterations=1000, epsilon=0.01, plot=False):
	"""
	Function for calculating covergence of consensus by trust between mussels.
	It will run number_of_iterations given in the arguments.
	:param zeta: numpy.array of floats (trust between agents)
	:param x: numpy.array of floats or ints (measurement)
	:param A: numpy.array of ints (0 and 1) - communication matrix
	:param sigma: numpy.array of floats
	:param number_of_iterations: int
	:param epsilon: float
	:param plot: boolean (if you want function to plot or not)
	:return: 
	"""
	agent1 = []
	agent2 = []
	agent3 = []
	agent4 = []
	agent5 = []
	iterations = []
	for iteration in range(number_of_iterations):
		zeta = update_zeta(zeta, x, A, sigma, iteration=iteration)
		if plot:
			agent1.append(zeta[0][4])
			agent2.append(zeta[1][4])
			agent3.append(zeta[2][4])
			agent4.append(zeta[3][4])
			agent5.append(zeta[4][4])
			iterations.append(iteration)

	numpy.set_printoptions(suppress=True)
	for row in zeta:
		print(row)
	mean = numpy.mean(zeta, axis=0)
	# print("mean", mean)

	if plot:
		agent1 = numpy.array(agent1)
		agent2 = numpy.array(agent2)
		agent3 = numpy.array(agent3)
		agent4 = numpy.array(agent4)
		agent5 = numpy.array(agent5)
		iterations = numpy.array(iterations)
		plot_zeta(agent1, agent2, agent3, agent4, agent5, iterations)


def plot_zeta(agent1, agent2, agent3, agent4, agent5, iterations):
	import matplotlib.pyplot as plt
	plt.title('Povjerenja agenataprema agentu 5 (agent koji krivo mjeri)')
	plt.ylabel('Povjerenje')
	plt.xlabel('Iteracije')
	plt.plot(iterations, agent5, label="Agent 5")
	plt.plot(iterations, agent1, label="Agent 1")
	plt.plot(iterations, agent2, label="Agent 2")
	plt.plot(iterations, agent3, label="Agent 3")
	plt.plot(iterations, agent4, label="Agent 4")
	plt.grid()
	plt.legend()
	plt.show()


def update_zeta(zeta, x, A, sigma, epsilon=0.01, iteration=None):
	"""
	Function created for updating values of zeta (trust
	matrix).
	:param zeta: numpy.array
	:param x: numpy.array
	:param epsilon: float
	:param A: numpy.array
	:return: 
	"""
	K = 0.02
	allowed_error = 0.02
	all_inside_lines = False

	if all_inside_lines:
		print("ALL INSIDE LINES AT ITERATION {}".format(iteration))
		return zeta
	for i, row in enumerate(zeta):  # iterating over row in matrix zeta (agent i)
		for j, trust in enumerate(row):  # iterating over agent j
			a = A[i, j]  # a tells us if agent i and j are communicating

			# trust regarding neighbours:
			# this trust is calculted even if agents i and j
			# do NOT communicate, and it is dependent on neighbours of
			# i
			sum_of_neighbours_trust = 0
			for k, k_trust in enumerate(row):
				if i != k:
					if A[i, k]:  # if i and k agents communicate
						# zeta[i, k] - povjerenje od agenta koji racuna povjerenje prema susjedu
						# zeta[k, j] - povjerenje susjeda prema agentu za kojeg se racuna povjerenje
						# zeta[i, j] - povjerenje od agenta koji racuna povjerenje prema agentu za kojeg se racuna
						# sum_of_neighbours_trust += zeta[i, k] * numpy.sign(zeta[k, j] - zeta[i, j])
						sum_of_neighbours_trust += zeta[i, k] * (zeta[k, j] - zeta[i, j])

			direct_trust = 0
			if a:  # if agent i and agent j are communicating
				delta = abs(x[i] - x[j])  # calculating measurement error
				obs_function = observation_function(sigma[i, j], delta)
				if obs_function < 0.001:
					obs_function = 0.0
				# direct trust is derived from
				# direct connection between agent i and agent j
				# it is calculated only if these two agents communicate
				zeta_previous = zeta[i, j]
				direct_trust = obs_function - zeta[i, j]
				sigma[i, j] += update_sigma(sigma[i, j], K, delta, zeta[i, j])

			dzeta = sum_of_neighbours_trust + direct_trust
			zeta[i, j] += epsilon * dzeta

	mean = numpy.mean(zeta, axis=0)
	all_inside_lines = True
	for col in [0, 1, 2, 3, 4]:
		if not all_inside_lines:
			break
		column = [item[0] for item in zeta[:, [col]]]
		for trust in column:
			if abs(trust - mean[col]) > allowed_error:
				all_inside_lines = False
				break

	return zeta


def update_sigma(sigma, K, delta, trust_between_agents):
	"""
	Updating confidence value from agent i to agent j.
	:param sigma: previous confidence value (float)
	:param K: adaptation constant (float)
	:param delta: error in measurement (float)
	:param trust_between_agents: trust between agent i and agent j
	:return: float (dsigma)
	"""
	obs_func = observation_function(sigma, delta)
	if obs_func < 0.001:
		obs_func = 0.0
	return -K * (obs_func - trust_between_agents)


if __name__ == "__main__":
	"""
	n - number of agents
	"""
	n = 5
	epsilon = 0.01
	#epsilon = 1
	x = numpy.array([1, 1, 1, 1, 15])
	A, zeta0, sigma0, delta = initialize(n)
	# update_zeta(zeta0, x, epsilon, A, sigma0, delta)
	convergence_zeta(zeta0, x, A, sigma0, number_of_iterations=1000, plot=True)
