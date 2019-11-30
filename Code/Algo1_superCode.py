G, k_type = createGraph(data_1, data_2, data_col, word)
Gtt = createTheGttMatrix(G,V)
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
    
    # Step 2: Call Search(G,S(G))
    start_time = time.time()
    SG,C,L = getOptimalSuperNode(G, SG, S, C, L, V, CN_sim)
    print("Time taken to update Summary Graph:",(time.time()-start_time)/60)
    
    D = calcDiagonalMatrix(CN_sim)
    # Step 3: update C
    while True:
        C_new = updateC(G, V, C, L, sim, D)
        L_new = updateL(G, V, C_new, L)
        sum_C=0
        sum_L=0
        print(sum_C,sum_L)
        for i in range(0,len(C)):
            sum_C+=np.sum(abs(C[i]-C_new[i])
        for j in range(0,len(L)):
            sum_L+=np.sum(abs(L[i]-L_new[i]))
        
        C = C_new
        L = L_new
        if sum_C<0.1 and sum_L<0.1:
            break
        else:
            continue