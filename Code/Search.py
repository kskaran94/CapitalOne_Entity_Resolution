import numpy as np
import copy

def ComputeTheta(C, k_type):
	C_t = C[k_type]
	vertex_cluster_contribution_sum = np.sum(C_t, axis = 0))
	theta = min(vertex_cluster_contribution_sum)
	return theta, vertex_cluster_contribution_sum


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




