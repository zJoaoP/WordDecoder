import random
import string
import sys

SECRET_STRING = ""
ALPHABET = string.printable

def generateRandomWord(size = 10):
	return "".join([random.choice(ALPHABET) for i in range(size)])

def compareWords(a, b):
	assert len(a) == len(b), "As duas strings devem ter o mesmo tamanho! (%d e %d)" % (len(a), len(b))
	return sum([pow(abs(ord(i) - ord(j)), 2) for i, j in zip(a, b)]) / len(a)

def generateRandomPopulation(populationSize, stringSize):
	return [generateRandomWord(stringSize) for i in range(populationSize)]

def getBestHalf(population):
	population = sorted(population, key = lambda x : compareWords(x, SECRET_STRING), reverse = False)
	threshold = len(population) // 2
	return population[:threshold]

def performCrossOver(mom, dad):
	threshold = random.randint(0, len(mom) - 2)
	return (mom[threshold:] + dad[:threshold]), (dad[threshold:] + mom[:threshold])

def performMutations(individuals):
	newIndividuals = []
	for i in range(len(individuals)):
		if random.random() >= 0.96:
			individual = list(individuals[i])
			pos = random.randint(0, len(individual) - 1)
			
			individual[pos] = random.choice(ALPHABET)
			newIndividuals += ["".join(individual)]
		else:
			newIndividuals += [individuals[i]]
	
	return newIndividuals

def reproduceParents(parents):
	individuals = []
	for i in range(len(parents) // 2):
		mom, dad = random.sample(parents, 2)
		individuals += performCrossOver(mom, dad)

	return performMutations(individuals)

def main():
	global SECRET_STRING

	if len(sys.argv) != 3:
		print("Uso correto: %s [tamanho da populacao] [palavra secreta]" % (sys.argv[0]))
		return

	SECRET_STRING = sys.argv[2]
	population = generateRandomPopulation(int(sys.argv[1]), len(SECRET_STRING))

	generation = 0
	while True:
		parents = getBestHalf(population)
		population = parents + reproduceParents(parents)

		print("[Generation %d] Best Individual: %s (%f), Second Best: %s (%f)" % (generation + 1, population[0], compareWords(population[0], SECRET_STRING), population[1], compareWords(population[1], SECRET_STRING)))

		if compareWords(population[0], SECRET_STRING) == 0.0:
			break
		else:
			generation += 1


if __name__ == "__main__":
	main()