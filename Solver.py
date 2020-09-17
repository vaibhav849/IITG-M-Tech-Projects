#!/usr/bin/env python
# coding: utf-8

# In[19]:


#This method is used to perform unit_resolution on sentence
def unit_resolution(sentence, variable):
    
    #creating an empty list of clauses which will be updated after
    #performing unit resolution and will be returned after completion of excution
    updated_sentence = []
    
    #performing unit resolution by checking each clause in the sentence
    for clause in sentence:
        
        #if variable is available in the clause then continue and check for another 
        #clause as this clause is redundant so removing it from sentence
        if variable in clause:
            continue
        
        #if clause contains -variable then remove it from the clause
        #Example if for variable p variable -p is in the clause then 
        #remove it and append this updated clause
        if -variable in clause:
            
            #creating new_clause which contains updated clause
            new_clause = []
            
            #inserting all variables other than -variable in the new_clause
            for var in clause:
                
                #inserting all variables other than -variable
                if var != -variable:
                    new_clause.append(var)
                    
            #if new_clause is empty that means we have found an empty clause
            #so we are returning 1 here as this unit resolution results in 
            #unsatisfiability
            if not new_clause:
                return 1
            
            #inserting new_clause into updated_sentense
            updated_sentence.append(new_clause)
        
        #if both variable and -variable are not available in clause then append 
        #this clause without any updation
        else:
            updated_sentence.append(clause)
            
    #returning updated sentence
    return updated_sentence


# In[20]:


#Method to perform unit resolution until it is not further possible
def unit_propagation(sentence):
    
    #creating empty list unit_clauses to find the clauses whose lengths
    #are 1 i.e. we can perform unit resolution using these clauses
    unit_clauses = []
    
    #creating empty list unit_assignment to store the variables
    #by using which we have performed the unit resolution
    unit_assignment = []
    
    #appending all the unit clauses in the unit_clause list
    for clause in sentence:
        
        #checking if this clause is unit clause or not
        if len(clause) == 1:
            
            #if it is unit clause then appending in unit_clause list
            unit_clauses.append(clause)
    
    #performing unit resolution until unit_clauses list is not empty
    while unit_clauses:
        
        #selecting first clause from unit_clauses list
        clause = unit_clauses[0]
        
        #updatig the sentence after performing unit resolution
        sentence = unit_resolution(sentence, clause[0])
        
        #appending the variable on which we have performed 
        #unit resolution into the unit_assignment list
        unit_assignment.append(clause[0])
        
        #if sentence returned by unit resolution is 1 that means
        #it contains empty clause so we are returning 1 and empty
        #Unit_assignment as this assignment results in unsatisfiability
        if sentence == 1:
            return 1, []
        
        #if sentence is empty then we are returning from
        #here as no further unit resolution is possible
        if not sentence:
            return sentence, unit_assignment
        
        #again finding unit clauses in updated sentence
        unit_clauses = []
        
        #appending all the unit clauses in the unit_clause list
        for clause in sentence:

            #checking if this clause is unit clause or not
            if len(clause) == 1:

                #if it is unit clause then appending in unit_clause list
                unit_clauses.append(clause)
                
    #returning updated sentence and unit_assignment list
    #after performing unit_propagation operation
    return sentence, unit_assignment


# In[21]:


#jeroslow wang 2 sided method for optimization of dpll
def jeroslow_wang_2_sided(sentence):
    
    #creating empty dictionary to store couter of eack variable
    counter = {}
    
    #calculating counter of each variable by iterating through sentence
    for clause in sentence:
        
        #calculating counter of every variable in each clause
        for variable in clause:
            
            #if variable is already available in counter dictionary then
            if abs(variable) in counter:
                
                #adding 2 ** -len(clause) to the value of stored variable
                counter[abs(variable)] += 2 ** -len(clause)
                
            #if variable is not available in counter dictionary then   
            else:
                
                #storing the variable to the dictionary with value 2 ** -len(clause)
                counter[abs(variable)] = 2 ** -len(clause)
    
    #returning the variable with maximum counter value
    return max(counter, key=counter.get)


# In[22]:


#main method to apply dpll algorithm on given sentence to check satisfiability
def dpll(sentence, assignment):
    
    #performing unit propagation step and updating the sentence
    sentence, unit_assignment = unit_propagation(sentence)
    
    #adding the returned unit assignment in assignment
    assignment = assignment + unit_assignment
    
    #if sentence is equal to 1 then returning empty solution list as the given 
    #sentence is unsatisfiable as returned by unit propagation step
    if sentence == 1:
        return []
    
    #if sentence is empty then we are returning from here as no need to 
    #further apply dpll algorithm so returning the calculated assignment
    if not sentence:
        return assignment
    
    #using jeroslow wang 2 sided optimization to find the variable
    #which can be used now to perform the decide step
    variable = jeroslow_wang_2_sided(sentence)
    
    #checking satisfiability with assignment + variable
    solution = dpll(unit_resolution(sentence, variable), assignment + [variable])
    
    #if solution is empty that means above check is unsatisfiable so
    #checking satisfiability with assignment + (-variable)
    if not solution:
        solution = dpll(unit_resolution(sentence, -variable), assignment + [-variable])
        
    #returning solution
    return solution


# In[23]:


#main driver method
def main():
    
    #getting the name of input file from user
    input_file = input("Enter Input File: ")
    
    #creating empty sentencse to store list of clauses
    sentence = []
    
    #parsing the file
    for line in open(input_file):
        
        #ignoring the comments as all comments in DIMACS CNF file starts with c
        if line.startswith('c'):
            continue
            
        #if line starts with p then reading the number of variables from this line
        if line.startswith('p'):
            n_vars = int(line.split()[2])
            continue
            
        #if line is not either starts with c or p then this is clause line so reading the clause
        #line and creating list by spilling this line and storing in temp each clause 
        #line ends with 0 in DIMACS CNF file, the type of temp list will be string
        temp = line.split()
        
        #creating empty clause to store the clause extracted from temp list
        clause = []
        
        #reading the temp list till second last element as last element is 0
        for i in range(len(temp) - 1):
            
            #appending the elements of temp in clause and converting into int 
            clause.append(int(temp[i]))
            
        #appending the clauses into sentence
        sentence.append(clause)
        
    #creating a flag to check if sentence contains 
    #a empty clause and initializing with False
    flag = False
    
    #finding empty clause in sentence
    for clause in sentence:
        
        #if any clause is empty set the flag to True
        if len(clause) == 0:
            
            #set the flag to True
            flag = True  
            break
            
    #getting the name of output file from user
    output_file = input("Enter Output File: ")
    
    #opening output file
    f = open(output_file, "w") 
    
    #if flag is True that means sentence contains empty clause 
    #that means given sentence is unsatisfiable
    if flag:
        
        #so writing unsatisfiable in output file
        f.write("UNSATISFIABLE")
        
        #closing the file
        f.close()
    
    #if flag is false that means sentence does not contains empty  
    #clause so performing the dpll algorithm on the sentence
    else:
        
        #creating solution list to store solution which is returned by dpll algorithm
        solution = dpll(sentence, [])
        
        #if solution list is not empty that means it contains solution for sentence
        if solution:
            
            #sorting the solution list as it may contain 
            #variable assignments in random order
            solution.sort(key=abs)
            
            #writing satisfiable and calculated solution in output file
            f.write("SATISFIABLE\n\nState:\n")
            
            #iterating the solution list to store solution in output file
            for variable in solution:
                
                #writing assignment of each variable in output file
                f.write(str(variable) + "\t")
                
                    
        #if solution list is empty that means sentence is unsatisfiable
        else:
            
            #writing unsatisfiable in output file
            f.write('UNSATISFIABLE\n')
            
        #closing the file
        f.close()

# In[24]:


#starting execution from here
if __name__ == '__main__':
    
    #calling main method which performs whole operations
    main()
