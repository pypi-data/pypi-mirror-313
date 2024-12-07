
'A Python implemntation of a kd-tree\n\nThis package provides a simple implementation of a kd-tree in Python.\nhttps://en.wikipedia.org/wiki/K-d_tree\n'
from __future__ import print_function
import heapq
import itertools
import math
from collections import deque
from functools import wraps
__author__ = 'Stefan Kögl <stefan@skoegl.net>'
__version__ = '0.16'
__website__ = 'https://github.com/stefankoegl/kdtree'
__license__ = 'ISC license'

class Node(object):
    'A Node in a kd-tree\n\n    A tree is represented by its root node, and every node represents\n    its subtree'

    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @property
    def is_leaf(self):
        'Returns True if a Node has no subnodes\n\n        >>> Node().is_leaf\n        True\n\n        >>> Node( 1, left=Node(2) ).is_leaf\n        False\n        '
        return ((not self.data) or all(((not bool(c)) for (c, p) in self.children)))

    def preorder(self):
        'iterator for nodes: root, left, right'
        if (not self):
            return
        (yield self)
        if self.left:
            for x in self.left.preorder():
                (yield x)
        if self.right:
            for x in self.right.preorder():
                (yield x)

    def inorder(self):
        'iterator for nodes: left, root, right'
        if (not self):
            return
        if self.left:
            for x in self.left.inorder():
                (yield x)
        (yield self)
        if self.right:
            for x in self.right.inorder():
                (yield x)

    def postorder(self):
        'iterator for nodes: left, right, root'
        if (not self):
            return
        if self.left:
            for x in self.left.postorder():
                (yield x)
        if self.right:
            for x in self.right.postorder():
                (yield x)
        (yield self)

    @property
    def children(self):
        '\n        Returns an iterator for the non-empty children of the Node\n\n        The children are returned as (Node, pos) tuples where pos is 0 for the\n        left subnode and 1 for the right.\n\n        >>> len(list(create(dimensions=2).children))\n        0\n\n        >>> len(list(create([ (1, 2) ]).children))\n        0\n\n        >>> len(list(create([ (2, 2), (2, 1), (2, 3) ]).children))\n        2\n        '
        if (self.left and (self.left.data is not None)):
            (yield (self.left, 0))
        if (self.right and (self.right.data is not None)):
            (yield (self.right, 1))

    def set_child(self, index, child):
        "Sets one of the node's children\n\n        index 0 refers to the left, 1 to the right child"
        if (index == 0):
            self.left = child
        else:
            self.right = child

    def height(self):
        '\n        Returns height of the (sub)tree, without considering\n        empty leaf-nodes\n\n        >>> create(dimensions=2).height()\n        0\n\n        >>> create([ (1, 2) ]).height()\n        1\n\n        >>> create([ (1, 2), (2, 3) ]).height()\n        2\n        '
        min_height = int(bool(self))
        return max(([min_height] + [(c.height() + 1) for (c, p) in self.children]))

    def get_child_pos(self, child):
        'Returns the position if the given child\n\n        If the given node is the left child, 0 is returned. If its the right\n        child, 1 is returned. Otherwise None'
        for (c, pos) in self.children:
            if (child == c):
                return pos

    def __repr__(self):
        return ('<%(cls)s - %(data)s>' % dict(cls=self.__class__.__name__, data=repr(self.data)))

    def __nonzero__(self):
        return (self.data is not None)
    __bool__ = __nonzero__

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.data == other)
        else:
            return (self.data == other.data)

    def __hash__(self):
        return id(self)

def require_axis(f):
    'Check if the object of the function has axis and sel_axis members'

    @wraps(f)
    def _wrapper(self, *args, **kwargs):
        if (None in (self.axis, self.sel_axis)):
            raise ValueError(('%(func_name) requires the node %(node)s to have an axis and a sel_axis function' % dict(func_name=f.__name__, node=repr(self))))
        return f(self, *args, **kwargs)
    return _wrapper

class KDNode(Node):
    'A Node that contains kd-tree specific data and methods'

    def __init__(self, data=None, left=None, right=None, axis=None, sel_axis=None, dimensions=None):
        'Creates a new node for a kd-tree\n\n        If the node will be used within a tree, the axis and the sel_axis\n        function should be supplied.\n\n        sel_axis(axis) is used when creating subnodes of the current node. It\n        receives the axis of the parent node and returns the axis of the child\n        node.'
        super(KDNode, self).__init__(data, left, right)
        self.axis = axis
        self.sel_axis = sel_axis
        self.dimensions = dimensions

    @require_axis
    def add(self, point):
        '\n        Adds a point to the current node or iteratively\n        descends to one of its children.\n\n        Users should call add() only to the topmost tree.\n        '
        current = self
        while True:
            check_dimensionality([point], dimensions=current.dimensions)
            if (current.data is None):
                current.data = point
                return current
            if (point[current.axis] < current.data[current.axis]):
                if (current.left is None):
                    current.left = current.create_subnode(point)
                    return current.left
                else:
                    current = current.left
            elif (current.right is None):
                current.right = current.create_subnode(point)
                return current.right
            else:
                current = current.right

    @require_axis
    def create_subnode(self, data):
        'Creates a subnode for the current node'
        return self.__class__(data, axis=self.sel_axis(self.axis), sel_axis=self.sel_axis, dimensions=self.dimensions)

    @require_axis
    def find_replacement(self):
        'Finds a replacement for the current node\n\n        The replacement is returned as a\n        (replacement-node, replacements-parent-node) tuple'
        if self.right:
            (child, parent) = self.right.extreme_child(min, self.axis)
        else:
            (child, parent) = self.left.extreme_child(max, self.axis)
        return (child, (parent if (parent is not None) else self))

    def should_remove(self, point, node):
        "checks if self's point (and maybe identity) matches"
        if (not (self.data == point)):
            return False
        return ((node is None) or (node is self))

    @require_axis
    def remove(self, point, node=None):
        'Removes the node with the given point from the tree\n\n        Returns the new root node of the (sub)tree.\n\n        If there are multiple points matching "point", only one is removed. The\n        optional "node" parameter is used for checking the identity, once the\n        removeal candidate is decided.'
        if (not self):
            return
        if self.should_remove(point, node):
            return self._remove(point)
        if (self.left and self.left.should_remove(point, node)):
            self.left = self.left._remove(point)
        elif (self.right and self.right.should_remove(point, node)):
            self.right = self.right._remove(point)
        if (point[self.axis] <= self.data[self.axis]):
            if self.left:
                self.left = self.left.remove(point, node)
        if (point[self.axis] >= self.data[self.axis]):
            if self.right:
                self.right = self.right.remove(point, node)
        return self

    @require_axis
    def _remove(self, point):
        if self.is_leaf:
            self.data = None
            return self
        (root, max_p) = self.find_replacement()
        (tmp_l, tmp_r) = (self.left, self.right)
        (self.left, self.right) = (root.left, root.right)
        (root.left, root.right) = ((tmp_l if (tmp_l is not root) else self), (tmp_r if (tmp_r is not root) else self))
        (self.axis, root.axis) = (root.axis, self.axis)
        if (max_p is not self):
            pos = max_p.get_child_pos(root)
            max_p.set_child(pos, self)
            max_p.remove(point, self)
        else:
            root.remove(point, self)
        return root

    @property
    def is_balanced(self):
        'Returns True if the (sub)tree is balanced\n\n        The tree is balanced if the heights of both subtrees differ at most by\n        1'
        left_height = (self.left.height() if self.left else 0)
        right_height = (self.right.height() if self.right else 0)
        if (abs((left_height - right_height)) > 1):
            return False
        return all((c.is_balanced for (c, _) in self.children))

    def rebalance(self):
        '\n        Returns the (possibly new) root of the rebalanced tree\n        '
        return create([x.data for x in self.inorder()])

    def axis_dist(self, point, axis):
        '\n        Squared distance at the given axis between\n        the current Node and the given point\n        '
        return math.pow((self.data[axis] - point[axis]), 2)

    def dist(self, point):
        '\n        Squared distance between the current Node\n        and the given point\n        '
        r = range(self.dimensions)
        return sum([self.axis_dist(point, i) for i in r])

    def search_knn(self, point, k, dist=None):
        "Return the k nearest neighbors of point and their distances\n\n        point must be an actual point, not a node.\n\n        k is the number of results to return. The actual results can be less\n        (if there aren't more nodes to return) or more in case of equal\n        distances.\n\n        dist is a distance function, expecting two points and returning a\n        distance value. Distance values can be any comparable type.\n\n        The result is an ordered list of (node, distance) tuples.\n        "
        if (k < 1):
            raise ValueError('k must be greater than 0.')
        if (dist is None):
            get_dist = (lambda n: n.dist(point))
        else:
            get_dist = (lambda n: dist(n.data, point))
        results = []
        self._search_node(point, k, results, get_dist, itertools.count())
        return [(node, (- d)) for (d, _, node) in sorted(results, reverse=True)]

    def _search_node(self, point, k, results, get_dist, counter):
        if (not self):
            return
        nodeDist = get_dist(self)
        item = ((- nodeDist), next(counter), self)
        if (len(results) >= k):
            if ((- nodeDist) > results[0][0]):
                heapq.heapreplace(results, item)
        else:
            heapq.heappush(results, item)
        split_plane = self.data[self.axis]
        plane_dist = (point[self.axis] - split_plane)
        plane_dist2 = (plane_dist * plane_dist)
        if (point[self.axis] < split_plane):
            if (self.left is not None):
                self.left._search_node(point, k, results, get_dist, counter)
        elif (self.right is not None):
            self.right._search_node(point, k, results, get_dist, counter)
        if (((- plane_dist2) > results[0][0]) or (len(results) < k)):
            if (point[self.axis] < self.data[self.axis]):
                if (self.right is not None):
                    self.right._search_node(point, k, results, get_dist, counter)
            elif (self.left is not None):
                self.left._search_node(point, k, results, get_dist, counter)

    @require_axis
    def search_nn(self, point, dist=None):
        '\n        Search the nearest node of the given point\n\n        point must be an actual point, not a node. The nearest node to the\n        point is returned. If a location of an actual node is used, the Node\n        with this location will be returned (not its neighbor).\n\n        dist is a distance function, expecting two points and returning a\n        distance value. Distance values can be any comparable type.\n\n        The result is a (node, distance) tuple.\n        '
        return next(iter(self.search_knn(point, 1, dist)), None)

    def _search_nn_dist(self, point, dist, results, get_dist):
        if (not self):
            return
        nodeDist = get_dist(self)
        if (nodeDist < dist):
            results.append(self.data)
        split_plane = self.data[self.axis]
        if (point[self.axis] <= (split_plane + dist)):
            if (self.left is not None):
                self.left._search_nn_dist(point, dist, results, get_dist)
        if (point[self.axis] >= (split_plane - dist)):
            if (self.right is not None):
                self.right._search_nn_dist(point, dist, results, get_dist)

    @require_axis
    def search_nn_dist(self, point, distance, best=None):
        '\n        Search the n nearest nodes of the given point which are within given\n        distance\n\n        point must be a location, not a node. A list containing the n nearest\n        nodes to the point within the distance will be returned.\n        '
        results = []
        get_dist = (lambda n: n.dist(point))
        self._search_nn_dist(point, distance, results, get_dist)
        return results

    @require_axis
    def is_valid(self):
        'Checks recursively if the tree is valid\n\n        It is valid if each node splits correctly'
        if (not self):
            return True
        if (self.left and (self.data[self.axis] < self.left.data[self.axis])):
            return False
        if (self.right and (self.data[self.axis] > self.right.data[self.axis])):
            return False
        return (all((c.is_valid() for (c, _) in self.children)) or self.is_leaf)

    def extreme_child(self, sel_func, axis):
        'Returns a child of the subtree and its parent\n\n        The child is selected by sel_func which is either min or max\n        (or a different function with similar semantics).'
        max_key = (lambda child_parent: child_parent[0].data[axis])
        me = ([(self, None)] if self else [])
        child_max = [c.extreme_child(sel_func, axis) for (c, _) in self.children]
        child_max = [(c, (p if (p is not None) else self)) for (c, p) in child_max]
        candidates = (me + child_max)
        if (not candidates):
            return (None, None)
        return sel_func(candidates, key=max_key)

def create(point_list=None, dimensions=None, axis=0, sel_axis=None):
    'Creates a kd-tree from a list of points\n\n    All points in the list must be of the same dimensionality.\n\n    If no point_list is given, an empty tree is created. The number of\n    dimensions has to be given instead.\n\n    If both a point_list and dimensions are given, the numbers must agree.\n\n    Axis is the axis on which the root-node should split.\n\n    sel_axis(axis) is used when creating subnodes of a node. It receives the\n    axis of the parent node and returns the axis of the child node.'
    if ((not point_list) and (not dimensions)):
        raise ValueError('either point_list or dimensions must be provided')
    elif point_list:
        dimensions = check_dimensionality(point_list, dimensions)
    sel_axis = (sel_axis or (lambda prev_axis: ((prev_axis + 1) % dimensions)))
    if (not point_list):
        return KDNode(sel_axis=sel_axis, axis=axis, dimensions=dimensions)
    point_list = list(point_list)
    point_list.sort(key=(lambda point: point[axis]))
    median = (len(point_list) // 2)
    loc = point_list[median]
    left = create(point_list[:median], dimensions, sel_axis(axis))
    right = create(point_list[(median + 1):], dimensions, sel_axis(axis))
    return KDNode(loc, left, right, axis=axis, sel_axis=sel_axis, dimensions=dimensions)

def check_dimensionality(point_list, dimensions=None):
    dimensions = (dimensions or len(point_list[0]))
    for p in point_list:
        if (len(p) != dimensions):
            raise ValueError('All Points in the point_list must have the same dimensionality')
    return dimensions

def level_order(tree, include_all=False):
    'Returns an iterator over the tree in level-order\n\n    If include_all is set to True, empty parts of the tree are filled\n    with dummy entries and the iterator becomes infinite.'
    q = deque()
    q.append(tree)
    while q:
        node = q.popleft()
        (yield node)
        if (include_all or node.left):
            q.append((node.left or node.__class__()))
        if (include_all or node.right):
            q.append((node.right or node.__class__()))

def visualize(tree, max_level=100, node_width=10, left_padding=5):
    'Prints the tree to stdout'
    height = min(max_level, (tree.height() - 1))
    max_width = pow(2, height)
    per_level = 1
    in_level = 0
    level = 0
    for node in level_order(tree, include_all=True):
        if (in_level == 0):
            print()
            print()
            print((' ' * left_padding), end=' ')
        width = int(((max_width * node_width) / per_level))
        node_str = (str(node.data) if node else '').center(width)
        print(node_str, end=' ')
        in_level += 1
        if (in_level == per_level):
            in_level = 0
            per_level *= 2
            level += 1
        if (level > height):
            break
    print()
    print()
