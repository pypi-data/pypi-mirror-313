#!/usr/bin/python
import copy


def deserialize(raw_tree):
    raise Exception("tree deserialization is not supported yet")
    """
    Constructs a Tree object from a raw serializable map/list tree
    :param list raw_children: A nested list of maps containing a "guid" str and "child_nodes" list
    """
    def _deserialize_helper(guid_and_children):
        """
        Constructs a Tree object from a raw serializable map/list tree
        :param map guid_and_children: A map that containing a "guid" str and "child_nodes" list
        """
        children = []
        for raw_child in guid_and_children["child_nodes"]:
            child = _deserialize_helper(raw_child)
            children.append(child) 
        parent = Tree(guid_and_children["guid"], children)
        return parent

    if len(raw_tree) != 1:
        raise ValueError("Must have one root in tree to deserialize it.")
    return _deserialize_helper(raw_tree[0])

# def build_tree(child_ids, parent = None):
#     child_nodes = []
#     for child_id in child_ids:
#         child = Tree(child_id["uuid"])

#         if parent:
#             parent.add_child(child)
#             child.add_parent(parent)

#         if len(child_id["child_nodes"]) != 0:
#             grand_children, child = build_tree(child_id["child_nodes"], child)
#         child_nodes.append(child)

#     return child_nodes, parent


# def export_tree_to_json(tree_roots):
#     current_output = []
#     for root in tree_roots:
#         assert isinstance(root, Tree)

#         output_node = {"uuid" : root.id} # TODO should probs switch over to uuids dude
#         output_node["child_nodes"] = export_tree_to_json(root.children)

#         current_output.append(output_node)

#     return current_output

# def find_leaf_nodes(tree_roots):
#     leaf_nodes = []
#     for root in tree_roots:
#         if len(root.children) != 0:
#             leaf_nodes += find_leaf_nodes(root.children)
#         else:
#             leaf_nodes.append(root)

#     return leaf_nodes

# def push_link_up(tree_roots, link):
#     all_new_links = []
#     # Push the source up
#     for root in tree_roots:
#         current_source_node = root.find(link["source"])
#         if not current_source_node:
#             # TODO probs not good
#             continue
#         layers_above = 1
#         while current_source_node.parent:
#             new_link = copy.deepcopy(link)
#             new_link["source"] = current_source_node.parent.id
#             new_link["layers_above_actual_source"] = layers_above
#             all_new_links.append(new_link)
#             # Get ready for next level
#             current_source_node = current_source_node.parent
#             layers_above += 1


#     # Now the target
#     for root in tree_roots:
#         current_target_node = root.find(link["target"])
#         if not current_target_node:
#             # TODO probs not good
#             continue
#         layers_above = 1
#         while current_target_node.parent:
#             new_link = copy.deepcopy(link)
#             new_link["target"] = current_target_node.parent.id
#             new_link["layers_above_actual_target"] = layers_above
#             all_new_links.append(new_link)
#             # Get ready for next level
#             current_target_node = current_target_node.parent
#             layers_above += 1

#     return  all_new_links


# class TreeRoots


class Tree(object):
    def __init__(self, id='root', children=None, parent=None):
        self.id = id
        self.children = set()
        self.parent = None
        if children is not None:
            for child in children:
                self.add_child(child)
        if parent is not None:
            self.add_parent(parent)

    def __repr__(self):
        parent_id = "<NO-PARENT>"
        if self.parent is not None:
            parent_id = self.parent.id

        return f"NODE(Id: {self.id}, Parent: {parent_id}, Children: [{','.join([x.id for x in self.children])}])"

    def find(self, node_id):
        if self.id == node_id:
            return self
        for child in self.children:
            found = child.find(node_id)
            if found:
                return found
        return None

    # Add a child to the current tree
    def add_child(self, new_node):
        assert isinstance(new_node, Tree)
        self.children.add(new_node)
        new_node.parent = self

    # Add a parent to the current tree
    def add_parent(self, new_node):
        assert isinstance(new_node, Tree)
        self.parent = new_node
        new_node.children.add(self)

    # def move_child(self, child_node):
    #     # Remove the child node to previous parent connection
    #     if child_node.parent:
    #         child_node.parent.children.remove(child_node)
    #         child_node.parent = None

    #     # Add the child to the new parent.
    #     self.add_child(child_node)

    # def remove_and_reattach(self, node_id):
    #     found_node = self.find(node_id)
    #     if not found_node:
    #         return None

    #     # Remove this node from the parent
    #     if found_node.parent:
    #         found_node.parent.children.remove(found_node)

    #     # Remove this node from the children and add the parent
    #     if len(found_node.children) > 0:
    #         for child in found_node.children:
    #             child.parent = found_node.parent
    #         # TODO how do we handle setting the root now. do we return this?

    #     # If there was a child then attach it to the parent
    #     if found_node.parent:
    #         found_node.parent.children += found_node.children

    def pprint(self, indent=0):
        s = ""
        for ii in range(0, indent):
            s += " "

        print(s + "- " + self.id)

        for child in self.children:
            child.pprint(indent + 4)


#    def find_roots()??? or we just want to manage the roots separately??


# d = [{"id": "a", "child_nodes" : []},
#      {"id": "b", "child_nodes" : [
#         {"id": "c", "child_nodes" : [{"id": "e", "child_nodes" : []}]}, {"id": "d", "child_nodes" : [{"id": "f", "child_nodes" : []}]}]}]

# roots, garbage = build_tree(d)
# print roots
# roots[0].pprint()
# roots[1].pprint()


# l = {"source":"e", "target":"f", "id":"e-f"}
# print push_link_up(roots, l)

# print find_leaf_nodes(roots)


# print "\n\n\n\n"

# a =  export_tree_to_json(roots)

# roots, garbage = build_tree_children(a)
# print roots
# roots[0].pprint()
# roots[1].pprint()
