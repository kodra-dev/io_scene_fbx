import os


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
            parts.insert(models_index, "Media")
        # Join the parts back together
        new_path = os.sep.join(parts)
        # Check if the new directory exists
        if os.path.isdir(new_path):
            return new_path
    # If the new directory does not exist, or "Raw" was not in the path, return the original path
    return path
  