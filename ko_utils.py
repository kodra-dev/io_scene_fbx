import os
import re
import bpy


def set_report(r):
    global report
    report = r

# Convert a directory from "raw" to "asset"
# For example:
# Input: H:\Gamedev\Horny Dungeon\Horny Dungeon Project\Raw\__HornyDungeon\_Prep\models\Iris
# Output: H:\Gamedev\Horny Dungeon\Horny Dungeon Project\Assets\__HornyDungeon\_Prep\Media\models\Iris\
# Note that besides changing "Raw" to "Assets", the output path has "Media" inserted before the "models" folder.
# Also we'd like it to run on both Windows and Linux.
# Also if the output path is not an existing directory, we'd like to return input path.
def to_hdg_directory_if_exists(path):
    parts = path.split(os.sep)
    # Check if "Raw" is in the path
    if "Raw" in parts:
        # Get the index of "Raw"
        index = parts.index("Raw")
        # Replace "Raw" with "Assets"
        parts[index] = "Assets"
        # Insert "Media" before "models"
        if "models" in parts:
            models_index = parts.index("models")
            if parts[models_index - 1] != "Media":
                parts.insert(models_index, "Media")
        # Join the parts back together
        new_path = os.sep.join(parts)
        # Check if the new directory exists
        if os.path.isdir(new_path):
            return new_path
    # If the new directory does not exist, or "Raw" was not in the path, return the original path
    return path
  

def action_to_export_path(action, master_name, export_dir):
    action_name = action.name if action.name else "clip"

    # Append the action name to the directory
    filename = f"{master_name}_{action_name}" + ".fbx"
    filepath = os.path.join(export_dir, filename)
    return filepath

def get_prefix(s):
    match = re.match(r'^([A-Z_]*_)', s)
    if match:
        return match.group(1)
    else:
        return None

def get_master_name(context):
    # Return the current collection name
    if context.collection:
        return context.collection.name
    else:
        return None

def get_all_actions(obj):
    actions = set()

    # Get action from object animation data
    if obj.animation_data:
        if obj.animation_data.action:
            actions.add(obj.animation_data.action)

        # Get all actions from NLA tracks
        for nla_track in obj.animation_data.nla_tracks:
            for strip in nla_track.strips:
                if strip.action and strip.action not in actions:
                    actions.add(strip.action)

    return actions

def match_any_prefix(s, prefixes_str):
    prefixes = [p.strip() for p in prefixes_str.split(",") if p.strip()]
    return any(s.startswith(prefix) for prefix in prefixes)

def set_scene_frame_range_by_active_action(context, obj):
    if obj and obj.animation_data and obj.animation_data.action:
        action = obj.animation_data.action 
        context.scene.frame_start = int(action.frame_range[0])
        context.scene.frame_end = int(action.frame_range[1])

def operator_exists(operator_path):
    operator = bpy.ops
    for part in operator_path.split("."):
        if hasattr(operator, part):
            operator = getattr(operator, part)
        else:
            return False
    return operator.poll() is not None

def store_selection_state():
    # Store active object
    # For some reason context.active_object just doesn't work
    active_obj = bpy.context.object

    # Store selected objects
    selected_objects = bpy.context.selected_objects.copy()

    return active_obj, selected_objects


def restore_selection_state(active_obj, selected_objects):
    
    # Restore active object
    if active_obj is not None:
        was_visible = active_obj.visible_get()
        active_obj.hide_set(False)
        bpy.context.view_layer.objects.active = active_obj
        active_obj.hide_set(not was_visible)

    o = bpy.context.object
    if o:
        mode = o.mode
        if mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')

    # Restore selected objects
    for obj in selected_objects:
        obj.select_set(True)

    if o:
        # Restore the mode
        if mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=mode)


def ensure_single_selected(obj_name):
    # Deselect all objects
    for obj in bpy.data.objects:
        obj.select_set(False)
        
    # Select and activate the desired object
    if obj_name in bpy.data.objects:
        bpy.data.objects[obj_name].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
        return True
    else:
        return False

def object_exists(obj):
    return obj is not None and obj.name in bpy.data.objects and bpy.data.objects[obj.name]


def leave_local_view():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            if space.local_view: #check if using local view
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {'area': area, 'region': region} #override context
                        bpy.ops.view3d.localview(override) #switch to global view