import random

def cycle_cross(indiv_1,indiv_2,prob_cross):
    size = len(indiv_1[0])
    value = random.random()
    positions = [0]*size
    crosses = []
    if value < prob_cross:
        while(sum(positions)<size):
            #get first unocupied place
            i = getUnocupied(positions)
            temp1 = []
            while(True):
                positions[i] = 1
                temp1.append(i)
                #get place where ind1(i) = ind2(j)
                #actualiza valor i

                i = indiv_1[0].index(indiv_2[0][i])
                if(i in temp1):
                    crosses.append(temp1)
                    break
        cycles_num = len(crosses)
        if(cycles_num <2):
            #print("So existe um ciclo")
            return indiv_1,indiv_2

        #buscar matrix de decisão EDIT modfiquei isto para não ter de reestruturar tudo e aproveitar o que ja estava feito
        new_indiv_1 = getDecision(cycles_num)
        new_indiv_2 = getDecision(cycles_num,True)

        #montar os individuos a devolver
        individual1 = mountIndividual(indiv_1,indiv_2,new_indiv_1,crosses,size)
        individual2 = mountIndividual(indiv_1,indiv_2,new_indiv_2,crosses,size)
        return individual1 , individual2
    else:
        return indiv_1,indiv_2

def getDecision(cycles_num,inverse= False):
    decision = []
    if(inverse == False):
        for i in range(cycles_num):
            if(i%2):
                decision.append(1)
            else:
                decision.append(2)
    elif(inverse == True):
        for i in range(cycles_num):
            if(i%2):
                decision.append(2)
            else:
                decision.append(1)
    return decision

def mountIndividual(indiv_1,indiv_2,structure,cycles,size):
    individual = [0]*size
    for ind,i in enumerate(cycles):
        for j in i:
            if (structure[ind] ==1 ):
                individual[j] = indiv_1[0][j]
            elif(structure[ind] ==2 ):
                individual[j] = indiv_2[0][j]
    return [individual,0]

def getUnocupied(positions):
    return positions.index(0)

if __name__ == '__main__':
    individual1 = [[1,2,3,4,5,6,7,8],0]
    individual2 = [[2,5,3,4,1,8,6,7],0]
    #print(individual2[0][1])
    #cycles=[[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]]
    #structure=[1,1,1,1,1]
    """
    for ind,i in enumerate(cycles):
        print(i)
        for j in i:
            print(j)
    """

    new_individual1, new_individual2 = cycle_cross(individual1,individual2,1)
    print(new_individual1)
    print(new_individual2)