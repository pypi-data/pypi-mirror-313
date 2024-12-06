from pycid_dev.lib.attribute.attribute import Attribute
from pycid_dev.lib.attribute.constants import kInheritanceSourceTrait


def yes_or_no(question):
    while True:
        reply = str(input(question + " (y/n): ")).lower().strip()
        if reply[0] == "y":
            return True
        if reply[0] == "n":
            return False


class Component(object):
    """
    Wrapper for the "Component" Object
    """

    def __init__(self, client, raw_component):
        self.name = raw_component["name"]
        self.id = raw_component["id"]
        self._attributes = raw_component["attributes"]
        self.generic_component_ids = raw_component["template_ids"]
        self.tree_id = raw_component["tree_id"]

        # self._network_callbacks = network_callbacks
        self._client = client

        # # Make sure the necessary network callbacks are present
        # assert sorted(["component_resync_query",
        #                "component_resync_execute",
        #                "component_attribute_remove",
        #                "component_attribute_edit",
        #                ]
        #               ) == sorted(self._network_callbacks.keys())

    def __repr__(self):
        return f"Component({self.name}: {self.id}, {len(self._attributes)} attributes, {len(self.generic_component_ids)} generic components)"

    def rename(self, new_name):
        result = self._client.rename_node(self.tree_id, self.id, new_name)
        return {"edited": result["success"], "error": ""}

    def attributes(self):
        return [
            Attribute(self._client, self.tree_id, self.id, attr)
            for attr in self._attributes
        ]

    def get_attribute_by_id(self, attribute_id):
        for attr in self._attributes:
            if attr["id"] == attribute_id:
                return Attribute(self._client, self.tree_id, self.id, attr)
        return None

    def get_attribute_by_name(self, name, inheritance_source: str = None):
        for attr in self._attributes:
            if attr["name"] == name:
                # If an inheritance_source was provided, check if it was inherited from
                if (
                    inheritance_source
                    and inheritance_source != attr[kInheritanceSourceTrait]
                ):
                    continue

                return Attribute(self._client, self.tree_id, self.id, attr)
        return None

    def has_attribute_by_name(self, name, inheritance_source: str = None):
        return self.get_attribute_by_name(name, inheritance_source) is not None

    def need_resync(self):
        result = self._client.node_resync_query(self.id, self.tree_id)
        # Return if any changes are proposed
        return result["data_changed"]

    # def resync(self, ignore_prompt=False):
    #     if not ignore_prompt:
    #         if not yes_or_no(
    #                 f"Are you sure you want to resync {self.name} ({self.id})?"):
    #             return False

    #     result = self._network_callbacks["component_resync_execute"](
    #         self.id, self.tree_id)
    #     return {"error": result["error"], "changes_made": result["data_changed"]}

    def edit_attribute_by_id(
        self,
        attribute_id,
        new_attribute_name: str = None,
        new_attribute_value=None,
        new_attribute_aux=None,
    ):
        """
        new_attribute_aux: tuple with a key and value for the aux
        """
        attr = next(a for a in self._attributes if a["id"] == attribute_id)
        if not attr:
            return (
                False,
                f'Could not find attribute in {self.name} with id "{attribute_id}"',
            )

        #
        # If new fields were not supplied then use the exiting ones
        #
        if (
            (not new_attribute_name)
            and (not new_attribute_value)
            and (not new_attribute_aux)
        ):
            return (
                False,
                f'Must provide something to edit for attribute with id "{attribute_id}"',
            )
        attribute_name = new_attribute_name if new_attribute_name else attr["name"]
        attribute_value = new_attribute_value if new_attribute_value else attr["value"]

        attribute_aux = {} if "aux" not in attr else attr["aux"]
        if new_attribute_aux:
            attribute_aux[new_attribute_aux[0]] = new_attribute_aux[1]

        attribute_traits = attr["traits"]

        result = self._client.attribute_edit(
            self.id,
            attribute_name,
            attribute_id,
            attribute_value,
            attribute_traits,
            attribute_aux,
            self.tree_id,
        )
        # return {"edited": result["edited"], "error": result["error"]}
        # TODO support better error returns
        return {"edited": result["success"], "error": ""}

    def remove_attribute_by_id(self, attribute_id, ignore_prompt=False):
        if not any(attr["id"] == attribute_id for attr in self._attributes):
            return (
                False,
                f'Could not find attribute in {self.name} with id "{attribute_id}"',
            )

        # Start with the removal
        if not ignore_prompt:
            if not yes_or_no(
                f"Are you sure you want to remove attribute from {self.name} (attr: {attribute_id})?"
            ):
                return False

        result = self._client.attribute_remove(self.id, attribute_id, self.tree_id)
        return {"removed": result["removed"], "error": result["error"]}

    def remove_attribute_by_name(self, attribute_name, ignore_prompt=False):
        """
        Simply remove an attribute from this component with a specific name
        """
        attribute_id = None
        for attribute in self._attributes:
            if attribute["name"] == attribute_name:
                attribute_id = attribute["id"]
                break
        if not attribute_id:
            return (
                False,
                f'Could not find attribute in {self.name} by name "{attribute_name}"',
            )

        return self.remove_attribute_by_id(attribute_id, ignore_prompt=ignore_prompt)

