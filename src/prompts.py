"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK PROMPTS                                   ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to define prompts/instructions for your task.            ║
║  Prompts are selected based on task type and returned to the model.           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
from typing import Optional, Dict


# ══════════════════════════════════════════════════════════════════════════════
#  DEFINE YOUR PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def get_shape_description(shape: str) -> str:
    """Get a descriptive name for a shape."""
    shape_map = {
        "circle": "circular",
        "square": "square",
        "triangle": "triangular",
        "star": "star-shaped"
    }
    return shape_map.get(shape, shape)


def get_prompt(task_type: str = "default", object_shape: str = None, task_data: Optional[Dict] = None) -> str:
    """
    Generate a detailed prompt for the counting objects task.
    
    Args:
        task_type: Type of task (key in PROMPTS dict)
        object_shape: Shape of objects in the task (for shape-specific prompts)
        task_data: Dictionary containing task information (num_objects, shapes, etc.)
        
    Returns:
        Detailed prompt string following the specification format
    """
    # Determine the shape type and count
    if task_data:
        num_objects = task_data.get("num_objects", 0)
        shapes = task_data.get("shapes", [])
        
        # Count shapes by type
        shape_counts = {}
        for shape in shapes:
            shape_counts[shape] = shape_counts.get(shape, 0) + 1
        
        # Determine if all objects are the same shape
        unique_shapes = set(shapes)
        is_same_shape = len(unique_shapes) == 1
        
        if is_same_shape:
            # All objects are the same shape
            shape_name = list(unique_shapes)[0]
            shape_desc = get_shape_description(shape_name)
            
            if shape_name == "circle":
                prompt = f"The scene shows {shape_desc} objects scattered across the image. Each object is a filled circle with a black outline. Starting from any position in the image, systematically count all the {shape_desc} objects visible in the scene. Count each object exactly once, ensuring that no object is missed or counted multiple times. After completing the count, display the total number of {shape_desc} objects found in the scene."
            
            elif shape_name == "square":
                prompt = f"The scene shows {shape_desc} objects scattered across the image. Each object is a filled square with a black outline. Starting from any position in the image, systematically count all the {shape_desc} objects visible in the scene. Count each object exactly once, ensuring that no object is missed or counted multiple times. After completing the count, display the total number of {shape_desc} objects found in the scene."
            
            elif shape_name == "triangle":
                prompt = f"The scene shows {shape_desc} objects scattered across the image. Each object is a filled equilateral triangle with a black outline. Starting from any position in the image, systematically count all the {shape_desc} objects visible in the scene. Count each object exactly once, ensuring that no object is missed or counted multiple times. After completing the count, display the total number of {shape_desc} objects found in the scene."
            
            elif shape_name == "star":
                prompt = f"The scene shows {shape_desc} objects scattered across the image. Each object is a filled five-pointed star with a black outline. Starting from any position in the image, systematically count all the {shape_desc} objects visible in the scene. Count each object exactly once, ensuring that no object is missed or counted multiple times. After completing the count, display the total number of {shape_desc} objects found in the scene."
            
            else:
                prompt = f"The scene shows {shape_desc} objects scattered across the image. Starting from any position in the image, systematically count all the {shape_desc} objects visible in the scene. Count each object exactly once, ensuring that no object is missed or counted multiple times. After completing the count, display the total number of {shape_desc} objects found in the scene."
        
        else:
            # Mixed shapes - list shape types without counts
            unique_shape_names = sorted(list(unique_shapes))
            shape_descriptions = [get_shape_description(shape) for shape in unique_shape_names]
            
            if len(shape_descriptions) == 1:
                shape_description = shape_descriptions[0]
            elif len(shape_descriptions) == 2:
                shape_description = f"{shape_descriptions[0]} and {shape_descriptions[1]}"
            else:
                shape_description = ", ".join(shape_descriptions[:-1]) + f", and {shape_descriptions[-1]}"
            
            prompt = f"The scene shows objects of different shapes scattered across the image, including {shape_description} objects. Each object is a filled geometric shape with a black outline. Starting from any position in the image, systematically count all the objects visible in the scene regardless of their shape. Count each object exactly once, ensuring that no object is missed or counted multiple times. After completing the count, display the total number of objects found in the scene."
    
    else:
        # Fallback to simple prompts if no task_data provided
        if object_shape == "circle":
            prompt = "The scene shows circular objects scattered across the image. Count all the circular objects in the scene and display the total number."
        elif object_shape == "square":
            prompt = "The scene shows square objects scattered across the image. Count all the square objects in the scene and display the total number."
        elif object_shape == "triangle":
            prompt = "The scene shows triangular objects scattered across the image. Count all the triangular objects in the scene and display the total number."
        elif object_shape == "star":
            prompt = "The scene shows star-shaped objects scattered across the image. Count all the star-shaped objects in the scene and display the total number."
        elif object_shape == "mixed":
            prompt = "The scene shows objects of different shapes scattered across the image. Count all the objects in the scene regardless of their shape and display the total number."
        else:
            prompt = "The scene shows objects scattered across the image. Count all the objects in the scene and display the total number."
    
    return prompt


def get_all_prompts(task_type: str = "default") -> list[str]:
    """Get all prompts for a given task type (deprecated - prompts are now generated dynamically)."""
    # This function is kept for backward compatibility but prompts are now generated dynamically
    return []
