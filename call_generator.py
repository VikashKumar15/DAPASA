import fnmatch
import os
import networkx as nx
import matplotlib.pyplot as plt
from store_call import save_call
		
def gen_call_graph(smali_loc):
	graph = nx.DiGraph()
	smali_folders = [f for f in os.listdir(smali_loc) if 'smali' in f]
	for folder in smali_folders:
		path = smali_loc + '/' + folder
		for dirpath, dirs, files in os.walk(path):
			for filename in fnmatch.filter(files, '*.smali'):
				save_call(os.path.join(dirpath, filename), graph)
	print('Total Nodes = {}',format(len(graph.nodes())))
	print('Total Edges = {}',format(len(graph.edges())))
	return graph
