# Script to verfiy the generated SAT solutions 

#from os import listdir
import os 

path = '' # add path

folder = os.fsencode(path)

filenames_sol = []
filenames_lp = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.sol') ):
        filenames_sol.append(filename)
    elif filename.endswith( ('.lp') ):
        filenames_lp.append(filename)
        
filenames_sol.sort()
filenames_lp.sort()
#print(filenames_sol)
#print(filenames_lp)

def load_sol(k):
    Sol = []    # array for solutions
    with open(os.path.join(path, filenames_sol[k])) as file:
        whole2 = file.read().split("\n")
        if "  " in whole2[0]: whole2[0] = whole2[0].replace ("  ", " ")
        var = whole2[0].split(" ")
        while "  " in whole2[1]: whole2[1] = whole2[1].replace ("  ", " ")
        Sol = whole2[1].split(" ")
        
        i = 0        
        sol_dict = {}
        while i in range(0,len(Sol)):
            if len(Sol[i]) > 0:
                sol_dict[var[i]] = int(Sol[i])
            i += 1
        return sol_dict

def load_SAT():
    res = []    # array for the constraints 
    for k in range(0,len(filenames_lp)):
        with open(os.path.join(path, filenames_lp[k])) as f:
            whole = f.read().split("\n")   
            phase = ''	# indicates the contents of each line in the file according to keywords therein    
            vars = load_sol(k)
            for line in whole:	# write contents of ".lp" file into arrays
        
                if line == "Bounds":
                    phase = 'Bounds'
                if line == "Binaries":
                    phase = 'Binaries'
                if line =="End":
                    phase = 'End'
                if line == "Subject To":
                    phase = 'Constraints'
                
                # Write the constraints into array res
                if phase == 'Constraints' and not line == "Subject To":
                    vres = line.split("\n")[0]
                    # Allow for constraints distributed over several lines 
                    constraint = vres.split(": ")[1]
                    result = int(constraint.split(" >= ")[1])
                    consRest = constraint.split(" >= ")[0]
                    # print("constraint", constraint)
                    # print("result", result)
                    if consRest[0] != '-':
                        consRest = "+ " + consRest
                    # print("consRest", consRest)
                    consRest = consRest.split(" ")
                    # print(consRest)
                    sum = 0
                    i = 0
                    while i in range(len(consRest)):
                        if consRest[i] == '-':
                            sum -= vars[consRest[i+1]]
                        else:
                            sum += vars[consRest[i+1]]
                        i = i+2
                    if sum < result:    
                        print("The constraint "+vres+" is not satisfied:")
                        print(str(sum)+" >= "+str(result))
                        return False
                    else:
                        print("The constraint "+vres+" is satisfied:")
                        print(str(sum)+" >= "+str(result))
                                 
    print("The variables satisfy all the constraints")
    return True   
load_SAT()
