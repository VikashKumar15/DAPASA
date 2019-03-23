import networkx as nx

def sng(sg, ss):
	l = []
	for node in sg:
		if node in ss:
			l.append(node)
	return l

def gen_merged_subgraph(sgs, ss):
	combining = True
	while combining:
		combining = False
		len_graph = len(sgs)
		for i in range(0, len_graph):
			for j in range(i + 1, len_graph):
				G = sgs[i]
				H = sgs[j]
				G_sen_api = sng(G, ss)
				H_sen_api = sng(H, ss)
				if set(G_sen_api).intersection(set(H_sen_api)):
					I = nx.compose(G,H)
					sgs = list((set(sgs) | set([I])) - set([G,H]))					
					combining = True
					break
			if len_graph != len(sgs):
#			if combining:
				break
	return sgs
