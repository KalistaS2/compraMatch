import networkx as nx
import pickle

# Em vez de nx.read_gpickle, use o pickle.load
with open("grafo_Similaridade_70.gexf", "rb") as f:
    G = pickle.load(f)

# Agora você pode exportar para o Gephi normalmente
nx.write_gexf(G, "grafo_Similaridade_70.gexf")