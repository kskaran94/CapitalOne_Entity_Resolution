G, k_type = createGraph(data_1, data_2, data_col, word)
Gtt = createTheGttMatrix(G,V)
import sys
def runAlgoOne(G, k_type):
    # Step 1: A random k-type summary graph
    start_time = time.time()
    CN_sim, V = createJaccardSim(G, k_type)
    print("Time taken to create similarity matrix:", (time.time()-start_time)/60)
    number_super_nodes = calcSuperNodes(V)
    start_time = time.time()
    C = initializeMapping(CN_sim, number_super_nodes)
    print("Time taken to create the C Mapping:", (time.time()-start_time)/60)
    
    start_time = time.time()
    SG, S = createSummaryGraph(G, C, V, k_type)
    print("Time taken to create the Summary Graph:", (time.time()-start_time)/60)
    
    L = createTheSuperLinkMatrix(S)
    D = calcDiagonalMatrix(CN_sim)
    
    # Calculate the new objective function
    start_time = time.time()
    initial_obj = computeObjectiveFunction(C, L, V, CN_sim, G)
    print("Time taken to calculate the objective function:",(time.time()-start_time)/60)
    
    
    for i in range(10):
        # Step 2: Call Search(G,S(G))
        SG, C, L = getOptimalSuperNode(G, SG, S, C, L, V, CN_sim)
        
        # Step 3: update C and L
        C_values=[]
        change_C=[]
        L_values=[]
        change_L=[]
        for j in range(20):
            C_old = copy.deepcopy(C)
            C = updateC(G, V, C, L, CN_sim, D)
            L_old = copy.deepcopy(L)
            L = updateL(G, V, C, L)
            sum_C=0
            sum_L=0
            for i in range(0,len(C)):
                sum_C+=np.sum(abs(C[i]-C_old[i]))
            for tt_dash in L:
                sum_L+=np.sum(abs(L[tt_dash]['adj_matrix']-L_old[tt_dash]['adj_matrix']))
            
            print(sum_C,sum_L)
            change_C.append(sum_C)
            change_L.append(sum_L)
            C_values.append(C)
            L_values.append(L)
        
        index = change_C.index(min(change_C))
        C = C_values[index]
        index = change_L.index(min(change_L))
        L = L_values[index]
        
        # Construct the new summary graph S(G)
        start_time = time.time()
        SG, S = createSummaryGraph(SG, C, V, k_type)
        print("Time taken to update the Summary Graph:", (time.time()-start_time)/60)
        
        # Calculate the new objective function
        start_time = time.time()
        final_objective = computeObjectiveFunction(C, L, V, CN_sim, G)
        print("Time taken to calculate the objective function:",(time.time()-start_time)/60)
        
        if final_objective<initial_objective:
            SG_final = copy.deepcopy(SG)
            C_final = copy.deepcopy(C)
            S_final = copy.deepcopy(S)
            L_final = copy.deepcopy(L)
            initial_objective = final_objective

return SG_final, S_final, C_final, L_final
