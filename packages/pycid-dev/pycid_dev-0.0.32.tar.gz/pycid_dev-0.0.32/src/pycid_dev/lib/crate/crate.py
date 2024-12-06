from pycid_dev.lib.component.component import Component


class Crate(object):
    """
    Wrapper for the "Crate" Object
    """

    def __init__(self, client, raw_components, tree_ids):
        self._tree_ids = tree_ids

        self._client = client
        # # Make sure the necessary network callbacks are present
        # assert sorted(["component_resync_query",
        #                "component_resync_execute",
        #                "component_attribute_edit",
        #                "component_attribute_remove",
        #                ]) == sorted(
        #     self._network_callbacks.keys())

        # Immediately shovel all the raw components into python classes. Also attach the necessary network callbacks.
        # Note the owning tree_ids have alreadwy been added a layer above as this is an aggregate struct.
        self._components = [
            Component(
                self._client,
                raw_component,
                #  {k: self._network_callbacks[k] for k in [
                #     "component_resync_query",
                #     "component_resync_execute",
                #     "component_attribute_edit",
                #     "component_attribute_remove",
                # ]}
            )
            for raw_component in raw_components
        ]

    def __repr__(self):
        return f"Crate({len(self._components)} components: {','.join(self._tree_ids)})"

    def __iter__(self):
        return iter(self._components)

    def filter_by_name(self, name: str):
        result = []
        for component in self._components:
            if component.name == name:
                result.append(component)
        return result

    def filter_by_attributes_with_name(self, name: str):
        result = []
        for component in self._components:
            if component.has_attribute_by_name(name):
                result.append(component)
        return result
