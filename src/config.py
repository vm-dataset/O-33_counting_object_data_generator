"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           YOUR TASK CONFIGURATION                             ║
║                                                                               ║
║  CUSTOMIZE THIS FILE to define your task-specific settings.                   ║
║  Inherits common settings from core.GenerationConfig                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from pydantic import Field
from core import GenerationConfig


class TaskConfig(GenerationConfig):
    """
    Your task-specific configuration.
    
    CUSTOMIZE THIS CLASS to add your task's hyperparameters.
    
    Inherited from GenerationConfig:
        - num_samples: int          # Number of samples to generate
        - domain: str               # Task domain name
        - difficulty: Optional[str] # Difficulty level
        - random_seed: Optional[int] # For reproducibility
        - output_dir: Path          # Where to save outputs
        - image_size: tuple[int, int] # Image dimensions
    """
    
    # ══════════════════════════════════════════════════════════════════════════
    #  OVERRIDE DEFAULTS
    # ══════════════════════════════════════════════════════════════════════════
    
    domain: str = Field(default="counting_objects")
    image_size: tuple[int, int] = Field(default=(512, 512))
    
    # ══════════════════════════════════════════════════════════════════════════
    #  VIDEO SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    generate_videos: bool = Field(
        default=True,
        description="Whether to generate ground truth videos"
    )
    
    video_fps: int = Field(
        default=10,
        description="Video frame rate"
    )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC SETTINGS
    # ══════════════════════════════════════════════════════════════════════════
    
    # Object counting settings
    min_objects: int = Field(
        default=1,
        description="Minimum number of objects to count"
    )
    
    max_objects: int = Field(
        default=20,
        description="Maximum number of objects to count"
    )
    
    object_types: list[str] = Field(
        default_factory=lambda: ["circle", "square", "triangle", "star"],
        description="Types of shapes to use as objects"
    )
    
    object_size_range: tuple[int, int] = Field(
        default=(30, 60),
        description="Min and max size of objects in pixels"
    )
    
    use_same_shape: bool = Field(
        default=True,
        description="Whether all objects in a task should be the same shape"
    )
    
    background_color: tuple[int, int, int] = Field(
        default=(240, 240, 240),
        description="Background color (RGB)"
    )
    
    object_colors: list[tuple[int, int, int]] = Field(
        default_factory=lambda: [
            (255, 100, 100),  # Red
            (100, 150, 255),  # Blue
            (100, 255, 100),  # Green
            (255, 200, 100),  # Orange
            (200, 100, 255),  # Purple
        ],
        description="Available colors for objects"
    )
    
    allow_overlap: bool = Field(
        default=False,
        description="Whether objects can overlap"
    )
    
    min_distance: int = Field(
        default=10,
        description="Minimum distance between objects (if no overlap)"
    )
    
    use_final_image: bool = Field(
        default=True,
        description="Whether to generate final_frame.png (showing count) or use goal.txt"
    )
