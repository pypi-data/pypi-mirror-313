from __future__ import annotations

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckanext.collection.interfaces import ICollection, CollectionFactory
from ckanext.ap_main.interfaces import IAdminPanel
import ckanext.ap_main.types as ap_types

from ckanext.ap_log.col_renderers import get_renderers
from ckanext.ap_log import collection


@tk.blanket.blueprints
class AdminPanelLogPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(IAdminPanel, inherit=True)
    p.implements(ICollection, inherit=True)

    # IConfigurer

    def update_config(self, config_: tk.CKANConfig):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "ap_log")

    # IAdminPanel

    def get_col_renderers(self) -> dict[str, ap_types.ColRenderer]:
        return get_renderers()

    def register_toolbar_button(
        self, toolbar_buttons_list: list[ap_types.ToolbarButton]
    ) -> list[ap_types.ToolbarButton]:
        """Extension will receive the list of toolbar button objects."""

        for button in toolbar_buttons_list:
            if button.get("label") == "Reports":
                button.setdefault("subitems", [])

                button["subitems"].append(  # type: ignore
                    ap_types.ToolbarButton(
                        label=tk._("Logs"),
                        url=tk.url_for("ap_log.list"),
                    )
                )

        return toolbar_buttons_list

    # ICollection
    def get_collection_factories(self) -> dict[str, CollectionFactory]:
        return {
            "ap-logs": collection.DbLogCollection,
        }
