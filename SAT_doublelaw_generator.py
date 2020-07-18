# Double-powerlaw CNF SAT generator.

import numpy
import matplotlib.pyplot as plt
from scipy import optimize
import random as rd
   
def const_sol(num_bin, prob_sol):
    
    import random as rd
    
    # Create a random solution
    sol = []
    for i in range(0, num_bin):
        if rd.random() <= prob_sol:        
            sol.append(1)
        else:
            sol.append(0)
        
    return(sol)    
    
    
def write_SAT_file(dat_name, constr_string, num_bin):
    with open(dat_name + ".lp" ,"w") as f: 
        f.write("Minimize" + "\n" + "  0" + "\n" + "Subject To" + "\n")
        f.write(constr_string)
        f.write("Bounds" + "\n" + "Binaries" + "\n" + " ")
        
        for i in range(1, num_bin + 1 ):
            f.write("X" + str(i -1 ) )
            if i != num_bin :
                f.write(" ")
        f.write("\n" + "End")



def write_sol_file(sol, dat_name, num_bin):
    with open(dat_name + ".sol","w") as f:         
        for i in range(0, num_bin ):
            f.write("X" + str(i) + " ")
        f. write("\n")
        for i in range(0, num_bin ):
            f.write(str(sol[i]))
            for j in range(0, len("X" + str(i) + " ")-1):
                f.write(" ")
    f.close()  


def powerlaw(x, alpha, beta):
    return alpha / x**(beta) 

def length_func(l, alpha, beta):  
    return  pow((2*l-1)/(2*alpha),-1/beta) -  pow((2*l+1)/(2*alpha),-1/beta)

def make_P(beta, ind_max): 
    P_y = []
    P_x = []
    for i in range(1, ind_max+1):
        P_y.append((i/ind_max)**(-beta))
        P_x.append(i/ind_max)
   
    s = sum(P_y)
    
    for i in range(1, ind_max+1):
        P_y[i-1] = P_y[i-1]/s
    
    return P_x, P_y

def SAT_gen():
      
    
    #Loop through all SAT problems to be generated    
    for i in range(0, num_sat):
        
        
        # Create name of the output file
        dat_name = dat_name_bas +  "_" + str(i+1) 
        

        # Create probability distributions for variables and clause lengths
        C = []      
        for i in range(1, m+1):
            C.append([])  
        (P_v_x, P_v_y) = make_P(beta_v, n)
        (P_c_x, P_c_y) = make_P(beta_c, m)


        # Choose the k*m literals for the problem        
        for i in range(1, k * m + 1):
            
#            print(str(i), " / ", str(k*m))
            
            double_occurrence = True
            while double_occurrence:
                # Choose a variable v (counting from 1)
                p = rd.random()
                v = 1      
                while p > P_v_y[v-1]:
                    p -= P_v_y[v-1]
                    v += 1
                
                 # Choose a clause c (counting from 1)
                p = rd.random()
                c = 1
                while p > P_c_y[c-1]:
                    p -= P_c_y[c-1]
                    c += 1
                
                # if chosen variable is already in the clause, choose v and c anew
#                double_occurrence = v in C[c-1] or -v in C[c-1]
                # Or: simply disregard multiple occurrences of variables
                double_occurrence = False
            
            # Determine if the literal is the positive or negated variable
            if rd.random() < prob_positive:
                C[c-1].append(v)
            else:
                C[c-1].append(-v)
                
         # count number of empty clauses         
#        print(C.count([]), "  ", len(C))
                
        # Remove empty clauses
        while [] in C:
            C.remove([])
        
        # Power-law fit: clause length over clause number
               
        vars_x = []
        vars_y = []
        
        # Fill two arrays with clause number and clause length     
        for i in range(1, len(C) ):
            vars_x.append(i)
            vars_y.append(len(C[i-1]))
        
        # Determine coefficient and exponent of power-law fit
        params, params_covariance = optimize.curve_fit(powerlaw, vars_x, vars_y, p0=[2, 2])
        
        # Plot clause  length over clause number and its fit function
        plt.figure(figsize=(6, 4))
        plt.scatter(vars_x, vars_y, label='')
        plt.plot(vars_x, powerlaw(vars_x, params[0], params[1]), label='Power-law fit')
        plt.legend(loc='best')
        plt.show()
        
        print("y = ", params[0], "* x^ -"+str(params[1]) )
    
        # histogram: number of clauses with specified clause length over clause length
        
        lengths = []
        for i in range(0, len(C)):
            lengths.append(len(C[i]))
        
        vars_x = []
        vars_y = []
#        vars_y_func = []
        
        print(max(lengths))
                
        for l in range(1, max(lengths) + 1):
           vars_x.append(l)
#           vars_y_func.append( length_func(l, alpha, beta ))
           vars_y.append( lengths.count(l) )

#        params, params_covariance = optimize.curve_fit(length_func, vars_x, vars_y, p0=[alpha, beta])        
        
        plt.figure(figsize=(6, 4))
        plt.scatter(vars_x, vars_y, label='')
#        plt.plot(vars_x, vars_y_func, label='Length-func fit')
        plt.legend(loc='best')
        plt.show()        
#        print("alpha = ", params[0], "beta = ", params[1] )

        # Make sure that the problem has at least one solution: 
        # Create a prospective solution for the problem
        sol = const_sol(n, prob_sol)          
        
        # Adjust the clauses so that each one is made true by the prospective splution
        
        # Run through all the clauses
        for i in range(0, len(C)):
            
            # Run through all the literals of the clause and  check if it is made true by the solution-to-be
            one_true = False
            for j in range(0, len(C[i])):
                lit = C[i][j]
                if ( (numpy.sign(lit) < 0 and sol[abs(lit)-1] == 0) or (numpy.sign(lit) > 0 and sol[abs(lit)-1] == 1) ):
                    one_true = True
                    break
            # If not a single one of the literals is made true by the solution:
            # Choose a random literal and flip its sign
            
            if not one_true:        
                j = rd.randint(0, len(C[i]) -1 )
                C[i][j] = - C[i][j]
        
        # Create the constraint string        
        constr = ""
        for i in range(0, len(C)):
            constr += " R" + str(i) + ": "
            
            for j in range(0, len(C[i])):
                if C[i][j] > 0 and j != 0:
                    constr += "+ "
                elif C[i][j] < 0:
                    constr += "- "      
                constr += "X" + str(abs(C[i][j]) - 1) + " "
                
            constr += ">= " + str( 1 - sum(x < 0 for x in C[i]))
            constr += "\n"
   
        # Write the problem and the solution into files     
        write_SAT_file(dat_name, constr, n)
        write_sol_file(sol, dat_name, n)
    


### MAIN: ###

dat_name_bas = "23571113"

# Choose the number of SAT problems to be generated
num_sat = 1

# Choose number of binary variables in the problem
n = 90

# Choose the number of clauses in the problem
m = round(2.65 * n)

# Choose the average number of literals per clause
k = 5

# Choose power law exponent for variable occurence
beta_v = 0.82

# Choose power law exponent for clause length
beta_c = 0.82

# Choose probability for positive literal in constraint
prob_positive = 0.5

# Ratio of "1"s in the guaranteed solution
prob_sol = 0.5

# Start the generation of the SAT problem and its solution
SAT_gen()
    

       
