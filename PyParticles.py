import math, random
import numpy, pygame


def Buttonify(Picture, coords, surface):
    image = pygame.image.load(Picture)
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image, imagerect)
    return (image, imagerect)


def addVectors(arg1, arg2):
	""" Returns the sum of two vectors """
	angle1, length1 = arg1
	angle2, length2 = arg2
	x = math.sin(angle1) * length1 + math.sin(angle2) * length2
	y = math.cos(angle1) * length1 + math.cos(angle2) * length2

	angle = 0.5 * math.pi - math.atan2(y, x)
	length = math.hypot(x, y)

	return (angle, length)



class Particle:
	""" A circular object with a velocity, size and mass """

	def __init__(self, my_tuple, size):
		x, y = my_tuple
		self.measurement = 10
		self.x = x
		self.y = y
		self.size = size
		self.colour = (0, 0, 255)
		self.communicating = 0
		self.sigma = numpy.random.uniform(low=0.1, high=0.8, size=(5, 5))
		# self.zeta = numpy.array([[1.0, 0.1, 0, 0, 0],
		# 						[0.1, 1.0, 0.1, 0, 0.1],
		# 						[0, 0.1, 1.0, 0.1, 0.1],
		# 						[0, 0, 0.1, 1.0, 0],
		# 						[0, 0.1, 0.1, 0, 1]])
		self.zeta = numpy.zeros((5, 5))

	def communicating_change(self, unselect=False):
		if unselect:
			self.colour = (0, 0, 255)
			self.communicating = 0
		else:
			self.colour = (0, 255, 0)
			self.communicating = 1


class Environment:
	""" Defines the boundary of a simulation and its properties """

	def __init__(self, dim_tuple):
		width, height = dim_tuple
		self.width = width
		self.height = height
		self.particles = []
		self.colour = (255, 255, 255)

	def addParticles(self, n, **kargs):
		""" Add n particles with properties given by keyword arguments """

		for i in range(n):
			size = kargs.get('size', 20)
			x = kargs.get('x', size + self.width/5 + 50*i)
			y = kargs.get('y', size + self.width/2)

			particle = Particle((x, y), size)
			particle.colour = kargs.get('colour', (0, 0, 255))
			if i == 3:
				particle.measurement = 15
			self.particles.append(particle)

	def update(self):
		"""  Moves particles and tests for collisions with the walls and each other """
		pass

	def findParticle(self, x, y):
		""" Returns any particle that occupies position x, y """

		for particle in self.particles:
			if math.hypot(particle.x - x, particle.y - y) <= particle.size:
				return particle
		return None
	
	def create_matrix_A(self):
		A = numpy.zeros(shape=(len(self.particles), len(self.particles)))
		for idx, agent in enumerate(self.particles):
			if agent.communicating:
				A[:, [idx]] = 1
				A[idx, idx] = 0
		return(A)