from random import random,choice

def mutationItem(prob_muta):
    def muta_neigh(cromo,item_matrix):
        if random() < prob_muta and cromo:
            new_cromo = cromo[:]
            index = choice(list(range(len(cromo))))
            #buscar valor valido para index
            indices = [i+1 for i, x in enumerate(item_matrix[index]) if x == 1]
            indices.append(0)
            newvalue = choice(indices)
            #mudar o valor
            new_cromo[index] = newvalue
            return new_cromo
        return cromo[:]
    return muta_neigh