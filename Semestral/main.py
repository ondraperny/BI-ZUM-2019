from PIL import Image
from random import choice, randint, uniform
from numba import jit


def vertex_to_number(vertex, line_length):
    return vertex[0] * line_length + vertex[1]


def number_to_vertex(number, line_length):
    y = number // line_length
    x = number % line_length
    return y, x


def load_dataset():
    alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',)
    img_alphabet = {}
    for character in alphabet:
        img = Image.open("dataset/" + character + ".bmp")
        img_alphabet[character] = img.convert('RGB')
    return img_alphabet


class Individual:
    """One individual is represented as a set of 5 coordinates in 16x16 space, where every coordinate is represented
    by one number(which is calculated by 'vertex_to_number' function"""
    alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',)

    def __init__(self, dataset):
        """choose 5 random points"""
        self.dataset = dataset
        self.img_width = 16
        self.fitness = float('nan')
        self.individuals = {}

        numbers = list(range(256))

        # uninformed initialization
        for i in range(5):
            self.individuals[i] = choice(numbers)
            numbers.remove(self.individuals[i])

    def get_color(self, img, pixel_position):
        y, x = number_to_vertex(pixel_position, self.img_width)
        r, g, b = img.getpixel((x, y))
        # print(r, g, b)
        if (r, g, b) == (0, 0, 0):
            return 0
        else:
            return 1

    @jit
    def calc_fitness(self):
        """Calculate fitness of Individual, based on how many photos can be distinguished by those five coordinated"""
        fitness = 0
        for character in self.alphabet:
            img = self.dataset[character]
            pixels_color = {}
            for index, individual in self.individuals.items():
                pixels_color[index] = self.get_color(img, individual)

            # print(pixels_color)

            for inner_character in self.alphabet:
                if inner_character == character:
                    continue

                inner_img = self.dataset[inner_character]

                flag = False
                for inner_index, inner_individual in self.individuals.items():
                    if self.get_color(inner_img, inner_individual) != pixels_color[inner_index]:
                        flag = True
                        break

                if flag:
                    fitness += 1

        return fitness

    def mutate(self):
        """Mutate on or two coordinates in individual"""
        number_of_mutations = randint(1, 2)
        for i in range(number_of_mutations):
            number = randint(0, 4)
            new_block = randint(0, 255)
            while True:
                if new_block not in self.individuals.values():
                    self.individuals[number] = new_block
                    break
                else:
                    new_block = randint(0, 255)
        return self


class Population:
    """Population is set of individuals that forms current generation"""
    def __init__(self, population_size, selection_size):
        self.population_size = population_size
        self.selection_size = selection_size
        self.dataset = load_dataset()
        self.reduced_population = {}
        self.number_of_generation = 0
        self.mutation_chance = 0.2

        self.population = {}
        for i in range(population_size):
            self.population[i] = Individual(self.dataset)

    def tournament_selection(self):
        """classic tournament selection used in GA"""
        fitness_sharing_dict = {}
        for key, value in self.population.items():
            fitness_sharing_dict[value] = self.fitness_sharing(value)

        tournament_competitors = 5
        self.reduced_population.clear()
        for i in range(self.selection_size):
            tmp = []
            for inner_i in range(tournament_competitors):
                key_tmp, individual_tmp = choice(list(self.population.items()))
                self.population.pop(key_tmp, None)
                tmp.append(individual_tmp)

            best_fitness = [0, None]
            for candidate in tmp:
                # fitness sharing didn't bring notable improvement so is by default disabled
                current_fitness = candidate.calc_fitness()  # - fitness_sharing_dict[candidate]
                if current_fitness > best_fitness[0]:
                    best_fitness[0] = current_fitness
                    best_fitness[1] = candidate

            self.reduced_population[i] = best_fitness[1]

    def cross_over(self, catastrophe_flag):
        """Create new individuals from parents of previous generation, some individuals are mutated instead,
        child that is same as other individual that is already in population is as well mutated(to prevent
        redundancy in population"""
        if not catastrophe_flag:
            self.tournament_selection()

        self.population.clear()
        for index, individual in self.reduced_population.items():
            self.population[index] = individual

        while len(self.population) != self.population_size:
            first = randint(0, len(self.reduced_population) - 1)
            second = randint(0, len(self.reduced_population) - 1)
            while first == second:
                second = randint(0, len(self.reduced_population) - 1)
            result = Individual(self.dataset)
            crossover = randint(1, 4)
            for i in range(5):
                if crossover < i:
                    result.individuals[i] = self.reduced_population[first].individuals[i]
                else:
                    result.individuals[i] = self.reduced_population[second].individuals[i]

            # checking if individual is already in population
            flag = True
            for index_inner, value_inner in self.population.items():
                for i in range(5):
                    if result.individuals[i] != value_inner.individuals[i]:
                        flag = False
                        break
                if flag:
                    break

                flag = True

            if flag:
                self.population[len(self.population)] = result.mutate()
            else:
                if self.mutation_chance > uniform(0.0, 1.0):
                    self.population[len(self.population)] = result.mutate()
                else:
                    self.population[len(self.population)] = result

        self.number_of_generation += 1

    def fitness_sharing(self, individual):
        """Calculate distance of individuals, as supporting factor for fitness function, the more distant individuals
        are the more interesting they are(as children of more distant individuals have higher chance of bringing
        new good solutions, without this, individuals tend to converge to specific values"""
        fitness = 0
        for ind, indiv in self.population.items():
            if individual is indiv:
                continue
            for ind_inner, indiv_inner in indiv.individuals.items():
                for ind_param, indiv_param in individual.individuals.items():
                    if indiv_inner == indiv_param:
                        fitness += 1
        return fitness

    @staticmethod
    def print_best_result(final_individual, generation_number):
        print("Individual's axis:|  x  |  y  | with fitness", final_individual.calc_fitness(),
              ", in", generation_number, "generation")
        for key, value in final_individual.individuals.items():
            y, x = number_to_vertex(value, 16)
            print("                  |%4s |%4s |" % (x, y))

    def best_fitness_in_generation(self):
        best_fitness = 0
        best_individual = 0
        for _, individual in self.population.items():
            current_individual_fitness = individual.calc_fitness()
            if current_individual_fitness > best_fitness:
                best_fitness = current_individual_fitness
                best_individual = individual
        return best_fitness, best_individual

    def flow_control(self, required_fitness, max_generations):
        while True:
            fin_val, final_indiv = self.best_fitness_in_generation()
            if self.number_of_generation >= max_generations:
                print("Maximum amount of generations exceeded")
                input_catastrophe = input("Do you want to apply catastrophe and continue evolution?(y/n)")

                if input_catastrophe == "y":
                    max_generations += 30
                    self.catastrophe(5)
                    self.cross_over(True)
                    fin_val, final_indiv = self.best_fitness_in_generation()

                    print("Generation: %3s" % self.number_of_generation + ", Best fitness generation", fin_val)
                    continue
                else:
                    self.print_best_result(final_indiv, self.number_of_generation)
                    break

            elif fin_val >= required_fitness:
                print("Individual with required(or better) fitness has been found")
                self.print_best_result(final_indiv, self.number_of_generation)
                break

            self.cross_over(False)
            print("Generation: %3s" % self.number_of_generation + ", Best fitness generation", fin_val)

    def catastrophe(self, number_of_survivors):
        """Kill all individuals except 'number_of_survivors' weakest individuals"""
        self.reduced_population.clear()

        # kill just random individuals - new population tend to stay very similar as pre-catastrophe population
        # for i in range(number_of_survivors):
        #     tmp = self.population.pop(choice(list(self.population.keys())))
        #     self.reduced_population[i] = tmp

        # kill best individuals
        for i in range(number_of_survivors):
            fin_val = 651
            final_index = 0
            for index, individual in self.population.items():
                tmp = individual.calc_fitness()
                if tmp < fin_val:
                    fin_val = tmp
                    final_index = individual
            self.reduced_population[i] = final_index


def best_fitness_in_generation_outer(population):
    best_fitness = 0
    best_individual = 0
    for _, individual in population.items():
        current_individual_fitness = individual.calc_fitness()
        if current_individual_fitness > best_fitness:
            best_fitness = current_individual_fitness
            best_individual = individual
    return best_fitness, best_individual


def print_best_result_outer(final_individual, generation_number):
    print("Individual's axis:|  x  |  y  | with fitness", final_individual.calc_fitness(),
          ", in", generation_number, "generation")
    for key, value in final_individual.individuals.items():
        y, x = number_to_vertex(value, 16)
        print("                  |%4s |%4s |" % (x, y))


def island(number_of_generations, sufficient_fitness):
    exchange_probability = 0.4
    """evolution on two separate populations, on both applied 'number_of_generation' generations,
    then they are merged together to form new population"""
    first_population = Population(10, 2)
    second_population = Population(10, 2)
    while first_population.number_of_generation < number_of_generations:
        first_population.cross_over(False)
        second_population.cross_over(False)

        if uniform(0.0, 1.0) < exchange_probability:
            exchange_index = randint(0, len(first_population.population) - 1)
            tmp = first_population.population[exchange_index]
            first_population.population[exchange_index] = second_population.population[exchange_index]
            second_population.population[exchange_index] = tmp

        best_fitness_1, best_individual_1 = best_fitness_in_generation_outer(first_population.population)
        best_fitness_2, best_individual_2 = best_fitness_in_generation_outer(second_population.population)

        print("Generation: %3s" % first_population.number_of_generation + ", Best fitness generation", best_fitness_1,
              "on 1st island")
        print("Generation: %3s" % second_population.number_of_generation + ", Best fitness generation", best_fitness_2,
              "on 2nd island")

        if best_fitness_1 >= sufficient_fitness or best_fitness_2 >= sufficient_fitness:
            print("Individual with required(or better) fitness has been found")
            if best_fitness_1 > best_fitness_2:
                print_best_result_outer(best_individual_1, first_population.number_of_generation)
            else:
                print_best_result_outer(best_individual_2, first_population.number_of_generation)
            break

        elif number_of_generations == first_population.number_of_generation:
            print("Maximum amount of generations exceeded")
            input_continue = input("Do you want to continue evolution?(y/n)")
            if input_continue == "y":
                number_of_generations += 30
            else:
                if best_fitness_1 > best_fitness_2:
                    print_best_result_outer(best_individual_1, first_population.number_of_generation)
                else:
                    print_best_result_outer(best_individual_2, first_population.number_of_generation)


#################################################################################

def main():
    """Simple user interface"""
    max_number_of_generations = int(input("Input maximum number of generations: "))
    sufficient_fitness = int(input("Input sufficient fitness value(max 650 ... expected result is 640+): "))
    island_flag = input(
        "Do you want to apply island method - two populations will be evolving separately and sometimes intercept"
        "(y/n)")

    if island_flag == "y":
        island(max_number_of_generations, sufficient_fitness)
    else:
        pop = Population(20, 4)
        pop.flow_control(sufficient_fitness, max_number_of_generations)

#################################################################################


if __name__ == "__main__":
    main()
