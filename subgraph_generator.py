import networkx as nx

def find_neighbors(G, api):
	first = list(G.neighbors(api))
	second = []
	for node in first:
		second = list(set(second) | set(G.neighbors(node)))
	result = list(set(first) | set(second))
	if api not in result:
		result.append(api)
	return result

def make_graph(sfcg, adj):
	H = nx.DiGraph()
	if len(adj) == 1:
		H.add_node(adj[0])
		return H
	for i in range(0, len(adj)):
		for j in range(i + 1, len(adj)):
			if not H.has_node(adj[i]):
				H.add_node(adj[i])
			if not H.has_node(adj[j]):
				H.add_node(adj[j])
			if sfcg.has_edge(adj[i], adj[j]):
				H.add_edge(adj[i], adj[j])
			elif sfcg.has_edge(adj[j], adj[i]):
				H.add_edge(adj[j], adj[i])
	return H

def remove_lib_nodes(nodes):
	lib = []
	f = open('LibD', 'r')
	for line in f:
		line = line.strip()
		lib.append(line)
	f.close()
	
	to_remove = []
	for node in nodes:
			if any((node.find(tpl) == 1) for tpl in lib):
				to_remove.append(node)
	return list(set(nodes) - set(to_remove))

def check_added(to_add, I):
	for graph in to_add:
		if graph.nodes() == I.nodes() and graph.edges() == I.edges():
			return True
	return False

def gen_subgraph_set(sfcg, ss):
	G = nx.Graph(sfcg)
	sgs = []
	for api in ss:
		adj = find_neighbors(G, api)
		adj = remove_lib_nodes(adj)
#		sgs.append(make_graph(sfcg, adj))
		H = make_graph(sfcg, adj)
		if not check_added(sgs, H):
			sgs.append(H)
	return sgs
