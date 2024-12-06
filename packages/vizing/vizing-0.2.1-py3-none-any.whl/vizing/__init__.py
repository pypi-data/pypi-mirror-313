import constraint as ct

def node_list_colouring_problem(G):
  """
  Return a constraint problem representing a node list-colouring instance.

  :param G: A graph with lists of permissible colours assigned to nodes.
  :return A node list-colouring constraint problem.
  """
  P = ct.Problem()
  for node in G.nodes():
    P.addVariable(node, G.nodes[node]['permissible'])
  for edge in G.edges():
    P.addConstraint(ct.AllDifferentConstraint(), edge)
  return(P)

def node_list_colouring_solution(G):
  """
  Return a list-coloured graph.

  :param G: A graph with lists of permissible colours assigned to nodes.
  :return A properly list-coloured graph.
  """
  P = node_list_colouring_problem(G)
  S = P.getSolution()
  for node in S:
    G.nodes[node]['colour'] = S[node]
  return(G)

def edge_list_colouring_problem(G, directed = False):
  """
  Return a constraint problem representing an edge list-colouring instance.

  :param G: A graph with lists of permissible colours assigned to edges.
  :param directed: Is the input graph directed or not?
  :return An edge list-colouring constraint problem.
  """
  P = ct.Problem()
  for edge in G.edges():
    P.addVariable(edge, G.edges[edge]['permissible'])
  if(directed):
    for node in G.nodes():
      P.addConstraint(ct.AllDifferentConstraint(), [x for x in G.out_edges(node)])
      P.addConstraint(ct.AllDifferentConstraint(), [x for x in G.in_edges(node)])
    else:
      for node in G.nodes():
        P.addConstraint(ct.AllDifferentConstraint(), [tuple(sorted(x)) for x in G.edges(node)])
  return(P)

def edge_list_colouring_solution(G, directed = False):
  """
  Return an edge-coloured graph.

  :param G: A graph with lists of permissible colours assigned to edges.
  :param directed: Is the input graph directed or not?
  :return A properly edge list-coloured graph.
  """
  P = edge_list_colouring_problem(G, directed)
  S = P.getSolution()
  for edge in G.edges():
    G.edges()[edge]['colour'] = S[edge]
  return(G)

def total_list_colouring_problem(G):
  """
  Return a constraint problem representing a total list-colouring instance.

  :param G: A graph with lists of permissible colours assigned to nodes and edges.
  :return A total list-colouring constraint problem.
  """
  P = ct.Problem()
  for node in G.nodes():
    P.addVariable(node, G.nodes[node]['permissible'])
  for edge in G.edges():
    P.addVariable(edge, G.edges[edge]['permissible'])
  for edge in G.edges():
    P.addConstraint(ct.AllDifferentConstraint(), [edge[0], edge[1], edge])
  for node in G.nodes():
    P.addConstraint(ct.AllDifferentConstraint(), [node] + [tuple(sorted(x)) for x in G.edges(node)])
  return(P)

def total_list_colouring_solution(G):
  """
  Return a total list-coloured graph.

  :param G: A graph with lists of permissible colours assigned to nodes and edges.
  :return A properly total list-coloured graph.
  """
  P = total_list_colouring_problem(G)
  S = P.getSolution()
  for node in G.nodes:
    G.nodes[node]['colour'] = S[node]
  for edge in G.edges():
    G.edges()[edge]['colour'] = S[edge]
  return(G)

