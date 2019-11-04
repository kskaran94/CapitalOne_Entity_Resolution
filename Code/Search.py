import numpy as np
import copy

def ComputeTheta(C, k_type):
	C_t = C[k_type]
	vertex_cluster_contribution_sum = np.sum(C_t, axis = 0))
	theta = min(vertex_cluster_contribution_sum)
	return theta, vertex_cluster_contribution_sum

def ComputeObjectiveFunction(S, C, L, CN_sim):
	#k_type = 2
	for type_ in range(k_type):
		sim_t = CN_sim[type_]
		C_t = C[type_]
		n_t = len(sim_t)

		first_term = 0
		for i in range(n_t):
			for j in range(i):
				first_term += sim_t[i][j]*(C_t[i] - C_t[j])**2 ### doubt

		second_term = 0
		for t in range():
			for t_dash in range():
				#create subgraph G_t_t_dash
				temp1 = np.matmul(C[t], L[t][t_dash])
				temp2 = np.matmul(temp1, C[t_dash].transpose())

				second_term += (G_t_t_dash - temp2)**2 ### doubt

		objective = first_term + second_term
		return objective
	

def GetOptimalSuperNode(G, SG, S, C):
	#S is a list of dictionaries; C is a list of numpy matrices
	#Keys in dictionary: order, name, position
	#Another key exists for the merged nodes - **** need to give key name ****
	#Should we keep a key to indicate which k-type?

	for type_t in S: 
		S_t, k_type = type_t['merged'], type_t['type']
		theta, vertex_cluster_contribution_sum = ComputeTheta(C, k_type)
		#assuming S_t is a list of clusters
		for index, s in enumerate(S_t):
			info = vertex_cluster_contribution_sum[index]
			#create a deepcopy and remove the current supernode s
			#SG_temp = copy.deepcopy(G)
			change_in_objective_function = ComputeObjectiveFunction(SG) - ComputeObjectiveFunction(SG_temp)
			if info == theta and change_in_objective_function > 0:
				##delete s from S(G)





