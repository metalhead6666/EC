"""
jb_int_2016.py

Ernesto Costa, February, 2016
"""

from sea_int_2016 import *

# João Brandão

def fitness(dimension):
    def fit(indiv):
        return evaluate(phenotype(indiv), dimension)
    return fit

def phenotype(indiv):
    """Genotype is identical to phenotype."""
    return indiv


def evaluate(indiv, dimension):
    alfa = 1.0
    beta = 3.0
    return alfa * len(indiv) - beta * viola(indiv,dimension)

def viola(indiv,dimension):
    # Count violations
    v = 0
    for elem in indiv:
	    limite = min(elem-1,dimension-elem)
	    vi = 0
	    for j in range(1,limite+1):
		    if ((elem - j) in indiv) and ((elem+j) in indiv):
			    vi += 1
	    v += vi
    return v


if __name__ == '__main__':
    generations = 50
    pop_size = 50
    dimension = 50
    #prob_muta = 0.05
    prob_cross = 0.9
    tour_size = 3
    elite_percent = 0.02
    numb_runs = 10
    
    mutation_neighbors = mutation(1,0.1)
    mutation_delete = delete_mutation(0.01)
    mutation_add = add_mutation(0.01)
    mutation_operators = [mutation_neighbors]
    #crossover_operator = merge_cross
    crossover_operator = sample_cross
    
    fitness_func = fitness(dimension)
    
    #best = sea_int(numb_generations,size_pop, dimension, prob_cross,sel_parents,recombination,mutation_oper,sel_survivors, fitness_func)
    #best = sea_int(generations, pop_size, dimension,prob_cross,tour_sel(tour_size),crossover_operator,mutation_operators,sel_survivors_elite(elite_percent), fitness_func)
    
    #best, best_stat,average_stat = sea_int_for_plot(generations, pop_size, dimension,prob_cross,tour_sel(tour_size),crossover_operator,mutation_operators,sel_survivors_elite(elite_percent), fitness_func)
    
    #numb_viola = viola(phenotype(best[0]),dimension)
    #print(best)
    #print('Violations: ',numb_viola)
    #display_stat_1(best_stat,average_stat)
    
    #boa,average_best = run(numb_runs,generations, pop_size, dimension,prob_cross,tour_sel(tour_size),crossover_operator,mutation_operators,sel_survivors_elite(elite_percent), fitness_func)
    #display_stat_n(boa,average_best)
    
    
    run_for_file('/Users/ernestojfcosta/tmp/jb_1.txt',numb_runs,generations, pop_size, dimension,prob_cross,tour_sel(tour_size),crossover_operator,mutation_operators,sel_survivors_elite(elite_percent), fitness_func)
    
    
    
    
    
