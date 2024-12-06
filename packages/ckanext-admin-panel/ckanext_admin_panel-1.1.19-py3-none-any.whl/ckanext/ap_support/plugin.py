from __future__ import annotations

import ckan.types as types
import ckan.plugins as p
import ckan.plugins.toolkit as tk

from ckanext.ap_main.interfaces import IAdminPanel
from ckanext.ap_main.types import ColRenderer

from ckanext.ap_support.col_renderers import get_renderers
from ckanext.ap_support.collection import SupportCollection


@tk.blanket.blueprints
@tk.blanket.actions
@tk.blanket.auth_functions
@tk.blanket.validators
@tk.blanket.helpers
class AdminPanelSupportPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer)
    p.implements(p.ISignal)
    p.implements(IAdminPanel, inherit=True)

    # IConfigurer

    def update_config(self, config_: tk.CKANConfig):
        tk.add_template_directory(config_, "templates")
        tk.add_public_directory(config_, "public")
        tk.add_resource("assets", "ap_support")

    # ISignal

    def get_signal_subscriptions(self) -> types.SignalMapping:
        return {
            tk.signals.ckanext.signal("ap_main:collect_config_sections"): [
                self.collect_config_sections_subs
            ],
            tk.signals.ckanext.signal("collection:register_collections"): [
                self.collect_collections_subs
            ],
        }

    @staticmethod
    def collect_collections_subs(sender: None):
        return {"ap-support": SupportCollection}

    @staticmethod
    def collect_config_sections_subs(sender: None):
        return {
            "name": "Support system",
            "configs": [
                {
                    "name": "Global settings",
                    "blueprint": "ap_user.list",
                    "info": "Support system configuration",
                },
                {
                    "name": "Dashboard",
                    "blueprint": "ap_support.list",
                    "info": "Support dashboard",
                },
            ],
        }

    # IAdminPanel

    def get_col_renderers(self) -> dict[str, ColRenderer]:
        return get_renderers()
