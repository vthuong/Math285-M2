# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 21:35:41 2018

@author: Kate
"""


import numpy as np
import random
import matplotlib.pyplot as plt

TREE = 1
EMPTY = 0
ONFIRE = -1

def monitor_forest(x, y, fire_x, fire_y):
    '''
    Draw the area map
    '''
    plt.scatter(x, y, marker = '.', color = 'g')
    plt.scatter(fire_x, fire_y, marker = '.', color = 'r')
    plt.show()
    
def reset_forest(forest):
    '''
        Reset the forest to initial condition
    '''
    for x in xrange(max_x):
        for y in xrange(max_y):
            if forest[x][y] != EMPTY:
               forest[x][y] = TREE 

def create_forest(max_x, max_y, tree_density):
    '''
    Create the simulation environment
    max_x: int
        length of the area
    max_y: int
        width of the area
    tree_density: float
        density of tree
    '''
    x = []
    y = []
    forest = np.zeros((max_x, max_y))
    for j in range(len(forest)):
        for i in range(len(forest[j])):
            if random.random() < tree_density:
                forest[i][j] = TREE
                x.append(i)
                y.append(j)
    return [forest, x, y]

# define neighbour, only in row and column direction
neighbours = [[0, 1],[0, -1],[-1, 0], [1, 0]]
prob_fires = [0.25, 0.75, 1]
tree_densities = [0.25, 0.5, 0.75]
# Set parameter of the area and tree density
max_x = 50
max_y = 50
tree_density = 1

for tree_density in tree_densities:
    # Create initial condition
    [forest, x, y] = create_forest(max_x, max_y, tree_density)

    for prob_catch_fire in prob_fires:
        # Number of tree burnt counter
        n_iter = 10
        max_time = 50
        time_counter = np.zeros(max_time)
        tree_counter = np.zeros(max_time)
        
        for i in range(n_iter):
            # Assume fire start at center (just assume a center always has tree)
            reset_forest(forest)
            new_x = [int(max_x / 2)]
            new_y = [int(max_y / 2)]
        
            # Set up
            fire_x = []
            fire_y = []
            forest[new_x[-1]][new_y[-1]] = ONFIRE
            time_iter = 0
            has_tree = False
            
            # monitor_forest(x, y, new_x, new_y)
            while (any([len(new_x) > 0, has_tree]) and time_iter < max_time):
                has_tree = False
                fire_x.extend(new_x)
                # print 'fire_x = ' + str(fire_x)
                fire_y.extend(new_y)
                new_x = []
                new_y = []
                time_counter[time_iter] += 1
                tree_counter[time_iter] += len(fire_x)
        
                # if (_iter % 20 == 0):
                #    print _iter
                #    monitor_forest(x, y, fire_x, fire_y)
                #    print len(fire_x)
                time_iter += 1
            
                for i in xrange(len(fire_x)):
                    cur_x = fire_x[i]
                    cur_y = fire_y[i]
                    for neighbour in neighbours:
                        next_x = cur_x + neighbour[0]
                        next_y = cur_y + neighbour[1]
                        if all([next_x >= 0, next_x < max_x, next_y >= 0, next_y < max_y]):
            #                print ('Check x = ' + str(next_x) + ' y= ' + str(next_y) 
            #                + ' forest = ' + str(forest[next_x][next_y]))
                            if forest[next_x][next_y] == TREE:
                                has_tree = True
                                if random.random() < prob_catch_fire:
                                    forest[next_x][next_y] = ONFIRE
                                    new_x.append(next_x)
                                    new_y.append(next_y)
        
        coef = (2.0 * tree_density * prob_catch_fire)**(0.5)
        t = np.arange(max_time)
        x = t * coef + 1
        y = x * x
        plt.plot(t, y, label = 'Theory')
        
        zidx = np.where(np.equal(time_counter, 0))
        time_counter[zidx] = 1
        plt.plot(t, tree_counter / time_counter, label = 'Simulation')
        
        plt.xlabel('Time step')
        plt.ylabel('Tree burnt')
        plt.title('Tree burnt vs time (density=' + str(tree_density) + ', prob.fire=' + 
                                       str(prob_catch_fire)+ ')') 
        plt.legend()
        plt.show()


#fire_x.extend(new_x)
#fire_y.extend(new_y)
#print _iter
#print 'Percentage of tree burnt: ' + '{:.2f}'.format(100 * float(len(fire_x)) / float(len(x)))
#monitor_forest(x, y, fire_x, fire_y)


