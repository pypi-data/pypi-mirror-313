# from pycid_dev.lib.attribute.constants import kInheritanceSourceTrait


def yes_or_no(question):
    while True:
        reply = str(input(question + " (y/n): ")).lower().strip()
        if reply[0] == "y":
            return True
        if reply[0] == "n":
            return False


class Attribute(object):
    """
    Wrapper for the "Attribute" Object
    """

    def __init__(self, client, tree_id, node_id, raw_attribute):
        self.id = raw_attribute["id"]
        self.name = raw_attribute["name"]
        # TODO metadata
        self.traits = raw_attribute["traits"]
        self.value = raw_attribute["value"]
        # Recursively make Attribute children objects
        self.children = []
        if "children" in raw_attribute:
            for child in raw_attribute["children"]:
                # TODO add the path here too
                self.children.append(Attribute(client, tree_id, node_id, child))

        self._raw_attribute = raw_attribute

        # Save upstream ids
        self.tree_id = tree_id
        self.node_id = node_id

        # Save client for network calls
        self._client = client

    def __repr__(self):
        # return f"Attribute({self.name}: {self.id}, {len(self.attributes)} attributes, {len(self.generic_component_ids)} generic components)"
        return f"Attribute({self.name}: {self.id})"

    # def set_name(self, new_name):
    #     result = self._client.rename_node(self.id, new_name, self.tree_id)
    #     return {"edited": result["success"], "error": ""}

    def set_value(self, new_value):
        result = self._client.attribute_value_update(
            self.tree_id,
            self.node_id,
            self.id,
            new_value,
        )
        return {"updated": result["success"], "error": ""}

    # def edit_attribute_by_id(
    #     self,
    #     attribute_id,
    #     new_attribute_name: str = None,
    #     new_attribute_value=None,
    #     new_attribute_aux=None,
    # ):
    #     """
    #     new_attribute_aux: tuple with a key and value for the aux
    #     """
    #     attr = next(a for a in self.attributes if a["id"] == attribute_id)
    #     if not attr:
    #         return (
    #             False,
    #             f'Could not find attribute in {self.name} with id "{attribute_id}"',
    #         )

    #     #
    #     # If new fields were not supplied then use the exiting ones
    #     #
    #     if (
    #         (not new_attribute_name)
    #         and (not new_attribute_value)
    #         and (not new_attribute_aux)
    #     ):
    #         return (
    #             False,
    #             f'Must provide something to edit for attribute with id "{attribute_id}"',
    #         )
    #     attribute_name = new_attribute_name if new_attribute_name else attr["name"]
    #     attribute_value = new_attribute_value if new_attribute_value else attr["value"]

    #     attribute_aux = {} if "aux" not in attr else attr["aux"]
    #     if new_attribute_aux:
    #         attribute_aux[new_attribute_aux[0]] = new_attribute_aux[1]

    #     attribute_traits = attr["traits"]

    #     result = self._client.attribute_edit(
    #         self.id,
    #         attribute_name,
    #         attribute_id,
    #         attribute_value,
    #         attribute_traits,
    #         attribute_aux,
    #         self.tree_id,
    #     )
    #     # return {"edited": result["edited"], "error": result["error"]}
    #     # TODO support better error returns
    #     return {"edited": result["success"], "error": ""}

    # def remove_attribute_by_id(self, attribute_id, ignore_prompt=False):
    #     if not any(attr["id"] == attribute_id for attr in self.attributes):
    #         return (
    #             False,
    #             f'Could not find attribute in {self.name} with id "{attribute_id}"',
    #         )

    #     # Start with the removal
    #     if not ignore_prompt:
    #         if not yes_or_no(
    #             f"Are you sure you want to remove attribute from {self.name} (attr: {attribute_id})?"
    #         ):
    #             return False

    #     result = self._client.attribute_remove(self.id, attribute_id, self.tree_id)
    #     return {"removed": result["removed"], "error": result["error"]}

    # def remove_attribute_by_name(self, attribute_name, ignore_prompt=False):
    #     """
    #     Simply remove an attribute from this component with a specific name
    #     """
    #     attribute_id = None
    #     for attribute in self.attributes:
    #         if attribute["name"] == attribute_name:
    #             attribute_id = attribute["id"]
    #             break
    #     if not attribute_id:
    #         return (
    #             False,
    #             f'Could not find attribute in {self.name} by name "{attribute_name}"',
    #         )

    #     return self.remove_attribute_by_id(attribute_id, ignore_prompt=ignore_prompt)
