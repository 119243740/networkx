#-*- coding: utf-8 -*-
"""
Recognition Tests
=================

A *forest* is an acyclic, undirected graph, and a *tree* is a connected forest.
Depending on the subfield, there are various conventions for generalizing these
definitions to directed graphs.

In one convention, directed variants of forest and tree are defined in an
identical manner, except that the direction of the edges is ignored. In effect,
each directed edge is treated as a single undirected edge. Then, additional
restrictions are imposed to define *branchings* and *arborescences*.

In another convention, directed variants of forest and tree correspond to
the previous convention's branchings and arborescences, respectively. Then two
new terms, *polyforest* and *polytree*, are defined to correspond to the other
convention's forest and tree.

Summarizing::

   +-----------------------------+
   | Convention 1 | Convention 2 |
   +=============================+
   | forest       | polyforest   |
   | tree         | polytree     |
   | branching    | forest       |
   | arborescence | tree         |
   +-----------------------------+

Each convention has its reasons. The first convention emphasizes definitional
similarity in that directed forests and trees are only concerned with
acyclicity and do not have an in-degree constraint, just as their undirected
counterparts do not. The second convention emphasizes functional similarity
in the sense that the directed analog of a spanning tree is an arborescence.
That is, take any spanning tree and choose one node as the root. Then
every edge is assigned a direction such there is a directed path from the
root to every other node. The result is an arborescence (or tree according to
the second convention).

NetworkX follows the first convention. Explicitly, these are:

undirected forest
   An undirected graph with no undirected cycles.

undirected tree
   A connected, undirected forest.

directed forest
   A directed graph with no undirected cycles. Equivalently, the underlying
   graph structure (which ignores edge orientations) is an undirected forest.
   In another convention, this is known as a polyforest.

directed tree
   A weakly connected, directed forest. Equivalently, the underlying graph
   structure (which ignores edge orientations) is an undirected tree. In
   another convention, this is known as a polytree.

branching
   A directed forest with each node having, at most, one parent. So the maximum
   in-degree is equal to 1. In another convention, this is known as a forest.

arborescence
   A directed tree with each node having, at most, one parent. So the maximum
   in-degree is equal to 1. In another convention, this is known as a tree.

"""

import networkx as nx

__author__ = """\n""".join([
    'Ferdinando Papale <ferdinando.papale@gmail.com>',
    'chebee7i <chebee7i@gmail.com>',
])


__all__ = ['is_arborescence', 'is_branching', 'is_forest', 'is_tree']

@nx.utils.not_implemented_for('undirected')
def is_arborescence(G):
    """
    Returns `True` if `G` is an arborescence.

    An arborescence is a directed tree with maximum in-degree equal to 1.

    Parameters
    ----------
    G : graph
        The graph to test.

    Returns
    -------
    b : bool
        A boolean that is `True` if `G` is an arborescence.

    Notes
    -----
    In another convention, an arborescence is known as a *tree*.

    See Also
    --------
    is_tree

    """
    if not is_tree(G):
        return False

    if max(G.in_degree().values()) > 1:
        return False

    return True

@nx.utils.not_implemented_for('undirected')
def is_branching(G):
    """
    Returns `True` if `G` is a branching.

    A branching is a directed forest with maximum in-degree equal to 1.

    Parameters
    ----------
    G : directed graph
        The directed graph to test.

    Returns
    -------
    b : bool
        A boolean that is `True` if `G` is a branching.

    Notes
    -----
    In another convention, a branching is also known as a *forest*.

    See Also
    --------
    is_forest

    """
    if not is_forest(G):
        return False

    if max(G.in_degree().values()) > 1:
        return False

    return True

def is_forest(G):
    """
    Returns `True` if G is a forest.

    A forest is a graph with no undirected cycles.

    For directed graphs, `G` is a forest if the underlying graph is a forest.
    The underlying graph is obtained by treating each directed edge as a single
    undirected edge in a multigraph.

    Parameters
    ----------
    G : graph
        The graph to test.

    Returns
    -------
    b : bool
        A boolean that is `True` if `G` is a forest.

    Notes
    -----
    In another convention, a directed forest is known as a *polyforest* and
    then *forest* corresponds to a *branching*.

    See Also
    --------
    is_branching

    """
    n = G.number_of_nodes()
    if n == 0:
        raise nx.exception.NetworkXPointlessConcept('G has no nodes.')

    if G.is_directed():
        components = nx.weakly_connected_component_subgraphs
    else:
        components = nx.connected_component_subgraphs

    for component in components(G):
        # Make sure the component is a tree.
        if component.number_of_edges() != component.number_of_nodes() - 1:
            return False

    return True

def is_tree(G):
    """
    Returns `True` if `G` is a tree.

    A tree is a connected graph with no undirected cycles.

    For directed graphs, `G` is a tree if the underlying graph is a tree. The
    underlying graph is obtained by treating each directed edge as a single
    undirected edge in a multigraph.

    Parameters
    ----------
    G : graph
        The graph to test.

    Returns
    -------
    b : bool
        A boolean that is `True` if `G` is a tree.

    Notes
    -----
    In another convention, a directed tree is known as a *polytree* and then
    *tree* corresponds to an *arborescence*.

    See Also
    --------
    is_arborescence

    """
    n = G.number_of_nodes()
    if n == 0:
        raise nx.exception.NetworkXPointlessConcept('G has no nodes.')

    if G.is_directed():
        is_connected = nx.is_weakly_connected
    else:
        is_connected = nx.is_connected

    # A simple, connected graph with no cycles has n-1 edges.

    if G.number_of_edges() != n - 1:
        return False

    return is_connected(G)
