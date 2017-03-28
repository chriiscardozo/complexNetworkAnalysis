from graph_tool.all import *
import os
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from bisect import bisect_left
from scipy.stats import norm
from collections import Counter
import math

def pagerank(g, name):
	pr = graph_tool.centrality.pagerank(g)
	maxx = 0.0
	maxx_v = 0
	for v in g.vertices():
		if pr[v] > maxx:
			maxx = pr[v]
			maxx_v = v
	
	print('Maior pg: ' + g.vp.label[maxx_v] + '('+str(maxx)+')')

	graph_draw(g, vertex_fill_color=pr,
               vertex_size=prop_to_size(pr, mi=5, ma=15),
               vorder=pr, vcmap=matplotlib.cm.gist_heat,output='out/pr_'+name+'.png')


def caracteristica_grau(vertices, g):
	print('5 maiores graus: ')
	i = -1
	while i >= -5:
		print(g.vp.label[vertices[i]] + ' ' + str(vertices[i].out_degree()))
		i = i - 1

	print '\nGrau medio: ' + str((sum(v.out_degree() for v in vertices))/len(vertices))
	print('Grau min: ' + str(vertices[0].out_degree()))
	print('Grau max: ' + str(vertices[-1].out_degree()))
	print('Grau desvio: ' + str(np.std([i.out_degree() for i in vertices])))

def caracteristica_clustering(g):
	#local (Watts coefficient)
	clust = graph_tool.clustering.local_clustering(g)
	print('Local cluster min: ' + str(min(clust)))
	print('Local cluster max: ' + str(max(clust)))
	print('Local Avg/STD cluster :' + str(graph_tool.stats.vertex_average(g, clust)))

	#global (Newman coefficient)
	print('Global clustering coeffi/STD: ' + str(graph_tool.clustering.global_clustering(g)))


def hist_grau(g):
	hist = graph_tool.stats.vertex_hist(g, "out")
	y = [i/sum(np.append(hist[0], 0)) for i in np.append(hist[0], 0)]

	plt.plot(hist[1], y)
	plt.show()

def hist_dist(g):
	hist = graph_tool.stats.distance_histogram(g)
	y = [i/sum(np.append(hist[0], 0)) for i in np.append(hist[0], 0)]

	plt.plot(hist[1], y)
	plt.show()

	i = 0
	summ = 0.0
	freq = np.append(hist[0], 0)
	val = hist[1]

	while i < len(freq):
		summ += (freq[i] * val[i])
		i += 1

	media = summ/float(sum(freq))

	i = 0
	dp_summ = 0.0
	while(i < len(freq)):
		dp_summ += ((val[i] - media)**2)*freq[i]
		i += 1

	dp = math.sqrt(dp_summ/float(sum(freq)))

	print('dist min: 1')
	print('dist max: ' + str(hist[1][-2]))
	print('dist media: ' + str(media))
	print('dist desvio: ' + str(dp))


def grafo(g):
	V = len(list(g.vertices()))
	E = len(list(g.edges()))
	print('Direcionado: ' + str(g.is_directed()))
	print(str(V) + ' vertices')
	print(str(E) + ' arestas')

	print 'Pseudo-diametro: ' + str(graph_tool.topology.pseudo_diameter(g)[0])
	comp, hist = graph_tool.topology.label_components(g)
	print 'Maior componente(existe so uma p/ todos): ' + str(hist[0])
	print 'Densidade: ' + str((2.0*E)/(V*(V-1.0)))

def main():

	names = ['lesmis', 'football', 'internet']

	for name in names:
		print '########## ' + name + ' ##########'
		g = load_graph(os.path.join(name, name + '.gml'))
		vertices = sorted([v for v in g.vertices()], key=lambda v: v.out_degree())
		
		grafo(g)
		caracteristica_grau(vertices, g)
		hist_grau(g)
		hist_dist(g)
		caracteristica_clustering(g)
		pagerank(g, name)

		print('\n\n')

main()