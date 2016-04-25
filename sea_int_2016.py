"""
sea_int_visual.py
A very simple EA for integers representation.
Ernesto Costa, March 2016
"""

__author__ = 'Ernesto Costa'
__date__ = 'March 2016'


from random import random,randint, sample, choice
from operator import itemgetter

# For the statistics
def run(numb_runs,numb_generations,size_pop, dimension, prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func):
    statistics = []
    for i in range(numb_runs):
        best,stat_best,stat_aver = sea_int_for_plot(numb_generations,size_pop, dimension,   prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func)
        statistics.append(stat_best)
    stat_gener = list(zip(*statistics))
    boa = [max(g_i) for g_i in stat_gener] # maximization
    aver_gener =  [sum(g_i)/len(g_i) for g_i in stat_gener]
    return boa,aver_gener
    
def run_for_file(filename,numb_runs,numb_generations,size_pop, dimension, prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func):
    with open(filename,'w') as f_out:
        for i in range(numb_runs):
            best= sea_int(numb_generations,size_pop, dimension, prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func)
            f_out.write(str(best[1])+'\n')


# Simple Evolutionary Algorithm		
def sea_int(numb_generations,size_pop, dimension, prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func):
    # inicialize population: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,dimension)
    # evaluate population
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]
    for i in range(numb_generations):
        # sparents selection
        mate_pool = sel_parents(populacao)
	# Variation
	# ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            indiv_1= mate_pool[i]
            indiv_2 = mate_pool[i+1]
            filhos = recombination(indiv_1,indiv_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for cromo,fit in progenitores:
            mutation = choice(mutation_oper)
            novo_cromo = mutation(cromo,dimension)
            descendentes.append((novo_cromo,fitness_func(novo_cromo)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Evaluate the new population
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]     
    return best_pop(populacao)


# Simple  Evolutionary Algorithm 
# Return the best plus, best by generation, average population by generation
def sea_int_for_plot(numb_generations,size_pop, dimension, prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func):
    # inicializa população: indiv = (cromo,fit)
    populacao = gera_pop(size_pop,dimension)
    # avalia população
    populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao]
    
    # para a estatística
    stat = [best_pop(populacao)[1]]
    stat_aver = [average_pop(populacao)]
    
    for i in range(numb_generations):
        # selecciona progenitores
        mate_pool = sel_parents(populacao)
	# Variation
	# ------ Crossover
        progenitores = []
        for i in  range(0,size_pop-1,2):
            cromo_1= mate_pool[i]
            cromo_2 = mate_pool[i+1]
            filhos = recombination(cromo_1,cromo_2, prob_cross)
            progenitores.extend(filhos) 
        # ------ Mutation
        descendentes = []
        for indiv,fit in progenitores:
            mutation = choice(mutation_oper) # uniform choice of the mutation operator...
            novo_indiv = mutation(indiv,dimension)
            descendentes.append((novo_indiv,fitness_func(novo_indiv)))
        # New population
        populacao = sel_survivors(populacao,descendentes)
        # Avalia nova _população
        populacao = [(indiv[0], fitness_func(indiv[0])) for indiv in populacao] 
	
	# Estatística
        stat.append(best_pop(populacao)[1])
        stat_aver.append(average_pop(populacao))
	
    return best_pop(populacao),stat, stat_aver


# Initialize population
def gera_pop(size_pop,dimension):
    return [(gera_indiv(dimension),0) for i in range(size_pop)]

def gera_indiv(dimension):
    """ indiv: a subset of integers between 1 and dimension."""
    # random initialization
    inf = int(0.1 * dimension)
    sup = int(0.5 * dimension)
    size =  randint(inf,sup)
    indiv = sample(list(range(1,dimension+1)),size)
    return indiv

# Variation operators:  mutation 
def mutation(size_neigh,prob_muta):
    def muta_neigh(cromo, dimension):
        if random() < prob_muta and cromo:
            new_cromo = cromo[:]
            index = choice(list(range(len(cromo))))
            number = new_cromo.pop(index)
            delta = choice(list(range(-size_neigh,size_neigh)))
            number = (number + delta)
            value = abs(number - dimension)
            if number < 1:
                number =  1 
            if number > dimension:
                number = dimension 
            if number not in new_cromo:
                new_cromo.insert(index,number)
                return new_cromo
        return cromo[:]
    return muta_neigh

def delete_mutation(prob_muta):
    def muta_delete(cromo, dimension):
        if random() < prob_muta and cromo:
            new_cromo = cromo[:]
            index = choice(list(range(len(cromo))))
            new_cromo.pop(index)
            return new_cromo
        return cromo[:]
    return muta_delete


def add_mutation(prob_muta):
    def muta_add(cromo, dimension):
        if random() < prob_muta and cromo:
            new_cromo = cromo[:]
            universe = set(list(range(1,dimension+1)))
            elements = set(new_cromo)
            candidates = list(universe.difference(elements))
            element = choice(candidates)
            new_cromo.append(element)
            return new_cromo
        return cromo[:]
    return muta_add
	

# Variation Operators: Crossover
def merge_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    size_cromo_1 = len(cromo_1)
	    cromo_2 = indiv_2[0]
	    size_cromo_2 = len(cromo_2)
	    
	    pos_1 = randint(0,size_cromo_1-1)
	    pos_2 = randint(0,size_cromo_2-1)
	    
	    f1 = list(set(cromo_1[0:pos_1] + cromo_2[pos_2:]))
	    f2 = list(set(cromo_2[0:pos_2] + cromo_1[pos_1:]))
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)


def sample_cross(indiv_1, indiv_2,prob_cross):
	value = random()
	if value < prob_cross:
	    cromo_1 = indiv_1[0]
	    size_cromo_1 = len(cromo_1)
	    cromo_2 = indiv_2[0]
	    size_cromo_2 = len(cromo_2)
	    
	    pos_1 = randint(0,size_cromo_1-1)
	    pos_2 = randint(0,size_cromo_2-1)
	    
	    f1 = list(set(sample(cromo_1,pos_1) + sample(cromo_2, (size_cromo_2 - pos_2))))
	    f2 = list(set(sample(cromo_1,(size_cromo_1 - pos_1)) + sample(cromo_2, pos_2)))
	    return ((f1,0),(f2,0))
	else:
	    return (indiv_1,indiv_2)
	    
# Parents Selection: tournament
def tour_sel(t_size):
    def tournament(pop):
        size_pop= len(pop)
        mate_pool = []
        for i in range(size_pop):
            winner = one_tour(pop,t_size)
            mate_pool.append(winner)
        return mate_pool
    return tournament

def one_tour(population,size):
    """Maximization Problem. Deterministic"""
    pool = sample(population, size)
    pool.sort(key=itemgetter(1), reverse=True)
    return pool[0]


# Survivals Selection: elitism
def sel_survivors_elite(elite):
    def elitism(parents,offspring):
        size = len(parents)
        comp_elite = int(size* elite)
        offspring.sort(key=itemgetter(1), reverse=True)
        parents.sort(key=itemgetter(1), reverse=True)
        new_population = parents[:comp_elite] + offspring[:size - comp_elite]
        return new_population
    return elitism


# Auxiliary
def display(indiv, phenotype):
    print('Chromo: %s\nFitness: %s' % (phenotype(indiv[0]),indiv[1]))
    
def best_pop(populacao):
    populacao.sort(key=itemgetter(1),reverse=True)
    return populacao[0]

def average_pop(populacao):
    return sum([fit for cromo,fit in populacao])/len(populacao)
    

if __name__ == '__main__':
    #to test the code with oneMax function
    #prefix = '/Users/ernestojfcosta/tmp/'
    #best_1 = sea_int(100, 20,100,0.9,tour_sel(3),one_point_cross,muta_bin,sel_survivors_elite(0.02), merito)
    #display(best_1,fenotipo)
    indiv_1 = gera_indiv(15)
    indiv_2 = gera_indiv(15)
    
    #my_mutation = mutation(2)
    #new_indiv = my_mutation(indiv_1,1,20)
    #my_mutation = delete_mutation()
    #new_indiv_d = my_mutation(indiv_1,1,15)
    #print(indiv_1, new_indiv_d)
    
    #my_mutation = add_mutation()
    #new_indiv_a = my_mutation(indiv_2,1,15)
    #print(indiv_2, new_indiv_a)
    
    
    print(indiv_1,'\n',indiv_2)
    #print(merge_cross([indiv_1,0],[indiv_2,0],1))
    print(sample_cross([indiv_1,0],[indiv_2,0],1))
    
    