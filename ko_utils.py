import os
import re



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
    actions = []

    # Get action from object animation data
    if obj.animation_data:
        if obj.animation_data.action:
            actions.append(obj.animation_data.action)

        # Get all actions from NLA tracks
        for nla_track in obj.animation_data.nla_tracks:
            for strip in nla_track.strips:
                if strip.action:
                    actions.append(strip.action)

    return actions

def match_any_prefix(s, prefixes_str):
    prefixes = [p.strip() for p in prefixes_str.split(",") if p.strip()]
    return any(s.startswith(prefix) for prefix in prefixes)

def set_scene_frame_range_by_active_action(context, obj):
    if obj and obj.animation_data and obj.animation_data.action:
        action = obj.animation_data.action 
        context.scene.frame_start = int(action.frame_range[0])
        context.scene.frame_end = int(action.frame_range[1])