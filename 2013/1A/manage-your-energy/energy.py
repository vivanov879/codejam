#!python
# https://code.google.com/codejam/contest/2418487/dashboard#s=p1
# You've got a very busy calendar today, full of important stuff to do. You worked hard to prepare and make sure all the activities don't overlap. Now it's morning, and you're worried that despite all of your enthusiasm, you won't have the energy to do all of this with full engagement.
import collections

def solve_greedy(E, R, values):
	"Solve using greedy algorithm."
	score = 0
	energy = [E for v in values] # energy left after activity [i] before regeneration
	assigned = [0 for v in values] # energy before activity i that has been assigned for use somewhere.

	best_to_worse = list(reversed(sorted(range(len(values)), key = lambda i: values[i])))

	for i in best_to_worse:
		while assigned[i] < E and not (i > 0 and assigned[i] >= energy[i-1] + R):
			assigned[i] += 1
			energy[i] -= 1
			score += values[i]

		for j in range(i+1, len(values)):
			# energy[j] = min(energy[j], energy[j-1]+R)
			if energy[j] > energy[j-1]+R:
				energy[j] = energy[j-1]+R
			else:
				break

		for j in reversed(range(i)):
			# assigned[j] = max(assigned[j], assigned[j+1]-R)
			if assigned[j] < assigned[j+1] - R:
				assigned[j] = assigned[j+1] - R
			else:
				break

		assert all(0<=e<=E for e in energy)
		assert all(0<=a<=E for a in assigned)

	return score

def first(collection):
	for x in collection:
		return x

def solve(E, R, values):
	energy = E
	gain = 0

	values = list(values)	# copy

	while values:
		v = values.pop(0)
		last = not values

		if last or v > max(values):
			spend = energy
		else:
			for i,x in enumerate(values):
				if x >= v:
					how_long_until_better = 1+i
					break
			else:
				assert False

 			# spent as much as we can while being sure will have full energy by then
			how_much_to_save = E - R*how_long_until_better
			how_much_to_save = max(0, how_much_to_save)

			spend = max(0, energy - how_much_to_save)

		assert 0 <= spend <= energy

		energy -= spend
		energy = min(E, energy+R)

		gain += v*spend

	return gain

if __name__ == "__main__":
	import fileinput
	f = fileinput.input()

	T = int(f.readline())

	for case in range(1,T+1):
		E,R,N = [int(x) for x in f.readline().split()]
		values = [int(x) for x in f.readline().split()]
		assert len(values) == N
		answer = solve(E, R, values)
		print "Case #%d: %s" % (case, answer)
		# assert solve(E, R, values) == solve_greedy(E, R, values)