import bpy
from bpy.types import Panel
from bl_ui.properties_data_modifier import DATA_PT_modifiers as original_DATA_PT_modifiers

from .modifiers.modifiers_ui import modifiers_ui


class DATA_PT_modifiers(Panel):
    bl_label = "Modifiers"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "modifier"
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        if context.object is not None:
            return context.object.type in {'MESH', 'CURVE', 'SURFACE', 'FONT', 'LATTICE'}
        return False

    def draw(self, context):
        layout = self.layout
        modifiers_ui(context, layout)


def register_DATA_PT_modifiers(self, context):
    """Callback function for enabling/disabling Modifier List layout
    in properties panel.
    """
    from bpy.utils import register_class, unregister_class

    prefs = bpy.context.preferences.addons["modifier_list"].preferences
    use_properties_panel = prefs.use_properties_panel

    if use_properties_panel:
        register_class(DATA_PT_modifiers)
    else:
        try:
            unregister_class(DATA_PT_modifiers)
            register_class(original_DATA_PT_modifiers)
        except RuntimeError:
            pass


def register():
    prefs = bpy.context.preferences.addons["modifier_list"].preferences
    use_properties_panel = prefs.use_properties_panel

    if use_properties_panel:
        from bpy.utils import register_class

        register_class(DATA_PT_modifiers)


def unregister():
    from bpy.utils import unregister_class

    try:
        unregister_class(DATA_PT_modifiers)
    except RuntimeError:
        pass