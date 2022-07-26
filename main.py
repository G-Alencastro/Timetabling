from random import shuffle, randint, random

por = 0
mat = 1
ing = 2
geo = 3
bio = 4

"""
([X, X, X, X] 
 [X, X, X, X]
 [X, X, X, X]
 [X, X, X, X])

([X, X, X, X]
 [X, X, X, X]
 [X, X, X, X]
 [X, X, X, X])

 ()=day
 []=grade
 X=subject
"""

class Individual:
    def __init__(self):
        self.genome = [[[randint(0, 4) for _ in range(5)] for _ in range(4)] for _ in range(5)]
        self.fit = 0

    def get_fit(self):
        def check_consecutive():
            times = 0
            for day in self.genome:
                for grade in day:
                    for i in range(len(grade)-1):
                            if grade[i] == grade[i+1]:
                                times += 1
                    return times * 50

        fit = 1000
        fit -= check_consecutive()


        fit = 1 if fit <= 0 else fit
        self.fit = fit
        return fit    

class Population:
    def __init__(self, n_ind):
        self.n_ind = n_ind
        self.individuals = [Individual() for _ in range(n_ind)]
        self.mean_fit = 0

    def fit_pop(self):
        # get mean fit of population
        for ind in self.individuals:
            self.mean_fit += ind.get_fit()
        self.mean_fit /= self.n_ind

        # sorting the population by fitness
        changed = True
        while changed:
            changed = False
            for c in range(1, self.n_ind):
                if self.individuals[c].fit > self.individuals[c-1].fit:
                    self.individuals[c], self.individuals[c-1] = self.individuals[c-1], self.individuals[c]
                    changed = True

    def new_population(self, elite_num=50):
        def crossover(fathers):
            son = Individual()

            for day_i in range(len(fathers[0].genome)):
                cut_num = randint(0, len(fathers[0].genome[day_i]))
                son.genome[day_i] = fathers[0].genome[day_i][:cut_num] + fathers[0].genome[day_i][cut_num:-1]
            return son

        def mutation(ind, mut_tax=0.005):
            mut = random()
            if mut <= mut_tax:
                s_genes = randint(0, ind.geno_len-1) 
                ind.genome[s_genes], ind.genome[s_genes-1] = ind.genome[s_genes-1], ind.genome[s_genes]
        
        def choose_father():
            ag_fit = 0
            ag_fit_list = []
            for ind in self.individuals:
                ag_fit += ind.fit
                ag_fit_list.append(ag_fit)
            self.mean_fit = ag_fit/self.n_ind
            
            chosen_num = randint(0, int(ag_fit))
            for c in range(self.n_ind-1):
                if ag_fit_list[c] < chosen_num < ag_fit_list[c+1]:
                    return self.individuals[c]
            return self.individuals[0]

        new_inds = [] +self.individuals[:elite_num]
        for _ in range(self.n_ind-elite_num):
            father01, father02 = choose_father(), choose_father()
            son = crossover([father01, father02])
            mutation(son)
            new_inds.append(son)

        self.individuals = new_inds

        
if __name__ == '__main__':
    pass
        