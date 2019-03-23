import os
import time
import sys
import shutil
import networkx as nx
import matplotlib.pyplot as plt
from call_generator import gen_call_graph
from sensitive_api import gen_api
from subgraph_generator import gen_subgraph_set
from merge_subgraph import gen_merged_subgraph

def main():
	f = open('categ', 'r')
	for line in f :
		count = 0
		categ = line.strip()
		os.mkdir(categ)
		files = os.listdir('../{}'.format(categ))
		for apk in files:
			os.system('apktool d ../{}/{}'.format(categ, apk))
			smali_loc = os.getcwd() + '/{}/'.format(apk[:-4])
			print('Disassembling of the APK Completed.')
	
			sfcg = gen_call_graph(smali_loc)
			print('Genration of Call Graph Completed.')
	
			ss = gen_api(sfcg, categ)

			sgs = gen_subgraph_set(sfcg, ss)
			print('Genration of Sub-Graph-Set Completed.')

			msg = gen_merged_subgraph(sgs, ss)
			print('Merging of Common Sub-Graph Completed.')
		
			i = 0
			for graph in msg:
				if graph.edges():
					i += 1
					nx.write_gexf(graph, '{}.gexf'.format(i))

			shutil.rmtree(apk[:-4])
			os.mkdir(categ + '/' + apk[:-4])
			files = [f for f in os.listdir('.') if '.gexf' in f]
			for f in files:
				shutil.move(f, '{}/{}/'.format(categ, apk[:-4]))
			count += 1
			print ("------------------------------{} Done------------------------------".format(count))
		print('{} Category Done'.format(categ))
				
if __name__ == '__main__':
	main()
