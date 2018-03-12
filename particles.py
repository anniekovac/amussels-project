import pygame
import PyParticles
from pprint import pprint as pp
import warnings
from main import update_zeta, convergence_zeta
import numpy
import time
import threading

start_time = time.time()
(width, height) = (400, 400)
screen = pygame.display.set_mode((width, height))


def switch_talking_mussel(env):
	global t
	t = threading.Timer(3, switch_talking_mussel, [env])
	t.start()

	for idx, mussel in enumerate(env.particles):
		if mussel.communicating:
			mussel.communicating_change(unselect=1)
			env.particles[(idx + 1) % 5].communicating_change()
			break

# inicijaliziranje environmenta
env = PyParticles.Environment((width, height))
# dodavanje agenata u environment
env.addParticles(5)

A = numpy.zeros(shape=(5, 5))
convergence_mode = False

running = True
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			t.cancel()

		elif event.type == pygame.MOUSEBUTTONDOWN:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			selected_particle = env.findParticle(mouseX, mouseY)
			measurements = [agent.measurement for agent in env.particles]

			# case one : if we want to calculate only one update of zeta for every agent
			if one_calculate[1].collidepoint((mouseX, mouseY)):
				print("Calculating just one update of zeta for every agent...")
				try:
					for idx, particle in enumerate(env.particles):
						if not particle.communicating:
							particle.zeta = update_zeta(particle.zeta, measurements, A, particle.sigma)
							numpy.set_printoptions(suppress=True, precision=2)
							print("Agent {}".format(idx+1))
							for row in particle.zeta:
								print(row)
				except NameError:
					warnings.warn("None of the agents started communicating yet.")

			# case two : if we want to wait till consensus converges
			if convergate[1].collidepoint((mouseX, mouseY)):
				convergence_mode = True
				print("Calculating consensus by trust...")
				switch_talking_mussel(env)

			if selected_particle is None:
				continue
			for idx, other_particle in enumerate(env.particles):
				if other_particle != selected_particle:
					env.particles[idx].communicating = 0
					other_particle.communicating_change(unselect=True)
			selected_particle.communicating_change()

	if not numpy.array_equal(env.create_matrix_A(), A):
		A = env.create_matrix_A()
		print("A:")
		print(A)

	if convergence_mode:
		for idx, mussel in enumerate(env.particles):
			mussel.zeta = update_zeta(mussel.zeta, measurements, A, mussel.sigma)
			print("Zeta agenta {}".format(idx))
			pp(mussel.zeta)

	env.update()
	screen.fill(env.colour)

	one_calculate = PyParticles.Buttonify('one.png', (int(width/1.5), int(height/1.3)), screen)
	convergate = PyParticles.Buttonify('conv.png', (int(width / 1.2), int(height / 1.3)), screen)

	for p in env.particles:
		pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size)
		# pygame.draw.polygon(screen, p.colour, [[100, 100], [0, 200], [200, 200]], 5)

	pygame.font.init()
	for idx, particle in enumerate(env.particles):
		myfont = pygame.font.SysFont('Comic Sans MS', 30)
		textsurface = myfont.render(str(particle.measurement), False, (0, 0, 0))
		screen.blit(textsurface, (particle.x, particle.y))
	pygame.display.update()

	pygame.display.flip()
