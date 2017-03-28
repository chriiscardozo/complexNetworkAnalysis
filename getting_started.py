from graph_tool.all import *

g = Graph()
ug = Graph(directed=False)

if(g.is_directed()):
	g.set_directed(False)

print g.is_directed()

cpyG = Graph(g)
cpyG.set_directed(True)
print cpyG.is_directed()

v1 = cpyG.add_vertex()
v2 = cpyG.add_vertex()

e1 = cpyG.add_edge(v1, v2)

graph_draw(cpyG, vertex_text=cpyG.vertex_index, vertex_font_size=18, output_size=(200,200))
# graph_draw(cpyG, vertex_text=cpyG.vertex_index, vertex_font_size=18, output_size=(200,200), output="2-nodes.png")

