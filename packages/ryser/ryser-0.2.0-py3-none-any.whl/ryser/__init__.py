import networkx as nx

def row(cell, size): 
    """
    The row label of the row in a square of dimension 'size'
    containing the cell with label 'cell'.

    :param cell: A cell index.
    :param size: The number of rows and columns.
    :return The row label of the row containing the given cell.
    """
    return int((cell - 1)/size) 

def col(cell, size): 
    """
    The column label of the column in a square of dimension 'size'
    containing the cell with label 'cell'.

    :param cell: A cell index.
    :param size: The number of rows and columns.
    :return The column label of the row containing the given cell.
    """
    return (cell - 1) % size

def row_r(cell, size): 
    """
    A range of all labels of cells in the same row as 'cell'.

    :param cell: A cell index.
    :param size: The number of rows and columns.
    :return A range of labels in the same row as cell.
    """
    return range(row(cell, size)*size + 1, (row(cell, size) + 1)*size + 1)

def col_r(cell, size): 
    """
    A range of all labels of cells in the same column as 'cell'.

    :param cell: A cell index.
    :param size: The number of rows and columns.
    :return A range of labels in the same column as cell.
    """
    return range(col(cell, size) + 1, size**2 + 1, size)

def list_assignment(P, size):
    """
    List assignment for a partial latin square. The list of
    a filled cell is the list containing just the element in that cell. The
    list of an empty cell contains only those symbols not already used in the
    same row and column as that cell.
    
    :param P: A partial latin square fixed cell dictionary.
    :param size: The number of rows and colums of the completed latin square.
    :return A dictionary representing the list assignment corresponding to P.
    """
    L = {}
    # initialise lists
    for i in range(1, size**2 + 1):
      if i in P.keys():
        L[row(i,size),col(i,size)] = [P[i]]
      else:
        L[row(i,size),col(i,size)] = list(range(1, size + 1))
    # update lists (remove used symbols from lists of same row/col)
    for i in range(1, size**2 + 1):
      if i in P.keys():
        # then remove P[i] from any list of a cell not in P from the same row/col
        for j in list(row_r(i, size)) + list(col_r(i, size)):
          if j not in P.keys():
            if P[i] in L[row(j, size), col(j, size)]:
              L[row(j, size), col(j, size)].remove(P[i])
    return L

def pls_list_colouring_problem(fixed, size):
    """
    Return a complete digraph (including self-loops on every node) with a list-assignment
    to edges such that the list on edge (i, j) is the set of all symbols not used in row i
    or column j in the partial latin square represented by the input dictionary.

    :param fixed: A dictionary of filled cells of a partial latin square.
    :param size: Number of rows and columns in the completed latin square.
    :return A complete digraph with edge list-assignment representing a partial latin square completion problem.
    """
    G = nx.complete_graph(size, create_using = nx.DiGraph)
    for node in G.nodes():
      G.add_edge(node, node)
    nx.set_edge_attributes(G, list_assignment(fixed, size), "permissible")
    return G

