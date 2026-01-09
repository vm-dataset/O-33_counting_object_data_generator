"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    COUNTING OBJECTS TASK GENERATOR                            ║
║                                                                               ║
║  Generates images with objects to count, and corresponding answers.           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import math
import tempfile
import hashlib
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Set
from PIL import Image, ImageDraw, ImageFont

from core import BaseGenerator, TaskPair, ImageRenderer
from core.video_utils import VideoGenerator
from .config import TaskConfig
from .prompts import get_prompt


class TaskGenerator(BaseGenerator):
    """
    Counting objects task generator.
    
    Generates images with random numbers of objects (circles, squares, triangles, stars)
    and creates corresponding task pairs for counting.
    """
    
    def __init__(self, config: TaskConfig):
        super().__init__(config)
        self.renderer = ImageRenderer(image_size=config.image_size)
        
        # Initialize video generator if enabled
        self.video_generator = None
        if config.generate_videos and VideoGenerator.is_available():
            self.video_generator = VideoGenerator(fps=config.video_fps, output_format="mp4")
        
        # Track generated task signatures to ensure uniqueness
        self._generated_signatures: Set[str] = set()
    
    def generate_task_pair(self, task_id: str, task_type: Optional[str] = None) -> TaskPair:
        """Generate one counting task pair."""
        
        # Generate task data (number of objects, positions, shapes, colors)
        task_data = self._generate_task_data(task_type=task_type)
        
        # Render initial state image (with objects to count)
        first_image = self._render_initial_state(task_data)
        
        # Render final state (showing count) or prepare text answer
        final_image = None
        if self.config.use_final_image:
            final_image = self._render_final_state(task_data)
        
        # Generate video (optional - showing counting animation)
        video_path = None
        if self.config.generate_videos and self.video_generator:
            video_path = self._generate_video(first_image, task_data, task_id)
        
        # Select prompt based on object shape with task data for detailed prompts
        object_shape = task_data.get("object_shape", "default")
        prompt = get_prompt("default", object_shape, task_data=task_data)
        
        # Prepare goal text (answer)
        goal_text = None
        if not self.config.use_final_image:
            goal_text = str(task_data["num_objects"])
        
        return TaskPair(
            task_id=task_id,
            domain=self.config.domain,
            prompt=prompt,
            first_image=first_image,
            final_image=final_image,
            ground_truth_video=video_path,
            goal_text=goal_text
        )
    
    # ══════════════════════════════════════════════════════════════════════════
    #  TASK-SPECIFIC METHODS
    # ══════════════════════════════════════════════════════════════════════════
    
    def _generate_task_data(self, task_type: Optional[str] = None) -> dict:
        """Generate task data: number of objects, positions, shapes, colors."""
        # Random number of objects
        num_objects = random.randint(self.config.min_objects, self.config.max_objects)
        
        # Select object shape(s) based on task_type
        if task_type and task_type in self.config.object_types:
            # Specific shape task
            object_shape = task_type
            shapes = [object_shape] * num_objects
            final_shape_type = object_shape
        elif task_type == "mixed":
            # Mixed shapes task
            shapes = [random.choice(self.config.object_types) for _ in range(num_objects)]
            final_shape_type = "mixed"
        elif self.config.use_same_shape:
            # Default: same shape for all objects
            object_shape = random.choice(self.config.object_types)
            shapes = [object_shape] * num_objects
            final_shape_type = object_shape
        else:
            # Default: mixed shapes
            shapes = [random.choice(self.config.object_types) for _ in range(num_objects)]
            final_shape_type = "mixed"
        
        # Select colors
        colors = [random.choice(self.config.object_colors) for _ in range(num_objects)]
        
        # Generate positions for objects
        positions = self._generate_positions(num_objects)
        
        # Generate sizes
        sizes = [
            random.randint(self.config.object_size_range[0], self.config.object_size_range[1])
            for _ in range(num_objects)
        ]
        
        return {
            "num_objects": num_objects,
            "shapes": shapes,
            "colors": colors,
            "positions": positions,
            "sizes": sizes,
            "object_shape": final_shape_type,
        }
    
    def _get_task_signature(self, task_data: dict) -> str:
        """
        Generate a unique signature for a task to ensure uniqueness.
        
        The signature is based on:
        - Number of objects
        - Shape types and their counts
        - Color distribution
        - Size distribution  
        - Spatial arrangement (positions)
        
        This ensures that tasks with different arrangements, even with same
        number of objects, are considered unique.
        """
        # Create a comprehensive signature
        # For shapes: use both the shape sequence and counts
        shapes = task_data["shapes"]
        shape_counts = {}
        for shape in shapes:
            shape_counts[shape] = shape_counts.get(shape, 0) + 1
        
        # Sort objects by position (x, then y) to create a canonical order
        objects = list(zip(
            shapes,
            task_data["colors"],
            task_data["sizes"],
            task_data["positions"]
        ))
        objects_sorted = sorted(objects, key=lambda obj: (obj[3][0], obj[3][1], obj[0], sum(obj[1]), obj[2]))
        
        # Create signature data
        signature_data = {
            "num_objects": task_data["num_objects"],
            "shape_counts": tuple(sorted(shape_counts.items())),
            "object_sequence": tuple([
                (obj[0], tuple(obj[1]), obj[2], obj[3])
                for obj in objects_sorted
            ])
        }
        signature_str = str(signature_data)
        return hashlib.md5(signature_str.encode()).hexdigest()
    
    def generate_unique_task_pair(
        self, 
        task_id: str, 
        task_type: Optional[str] = None,
        max_attempts: int = 1000
    ) -> TaskPair:
        """
        Generate a unique task pair, ensuring it hasn't been generated before.
        
        Args:
            task_id: Unique identifier for the task
            task_type: Type of task (circle, square, triangle, star, mixed)
            max_attempts: Maximum number of attempts to generate a unique task
            
        Returns:
            TaskPair if unique task was generated, None otherwise
        """
        for attempt in range(max_attempts):
            task_data = self._generate_task_data(task_type=task_type)
            signature = self._get_task_signature(task_data)
            
            # Check if this task is unique
            if signature not in self._generated_signatures:
                self._generated_signatures.add(signature)
                
                # Render initial state image (with objects to count)
                first_image = self._render_initial_state(task_data)
                
                # Render final state (showing count) or prepare text answer
                final_image = None
                if self.config.use_final_image:
                    final_image = self._render_final_state(task_data)
                
                # Generate video (optional - showing counting animation)
                video_path = None
                if self.config.generate_videos and self.video_generator:
                    video_path = self._generate_video(first_image, task_data, task_id)
                
                # Select prompt based on object shape with task data for detailed prompts
                object_shape = task_data.get("object_shape", "default")
                prompt = get_prompt("default", object_shape, task_data=task_data)
                
                # Prepare goal text (answer)
                goal_text = None
                if not self.config.use_final_image:
                    goal_text = str(task_data["num_objects"])
                
                return TaskPair(
                    task_id=task_id,
                    domain=self.config.domain,
                    prompt=prompt,
                    first_image=first_image,
                    final_image=final_image,
                    ground_truth_video=video_path,
                    goal_text=goal_text
                )
        
        # Failed to generate unique task after max attempts
        raise RuntimeError(f"Failed to generate unique task after {max_attempts} attempts")
    
    def generate_tasks_for_type(
        self, 
        task_type: str, 
        num_tasks: int,
        task_id_prefix: Optional[str] = None
    ) -> List[TaskPair]:
        """
        Generate multiple unique tasks for a specific task type.
        
        Args:
            task_type: Type of task (circle, square, triangle, star, mixed)
            num_tasks: Number of tasks to generate
            task_id_prefix: Optional prefix for task IDs
            
        Returns:
            List of unique TaskPairs
        """
        tasks = []
        prefix = task_id_prefix or self.config.domain
        
        for i in range(num_tasks):
            task_id = f"{prefix}_{task_type}_{i:04d}"
            task_pair = self.generate_unique_task_pair(task_id, task_type=task_type)
            tasks.append(task_pair)
            print(f"  Generated: {task_id}")
        
        return tasks
    
    def _generate_positions(self, num_objects: int) -> List[Tuple[int, int]]:
        """Generate positions for objects, avoiding overlaps if configured."""
        width, height = self.config.image_size
        positions = []
        max_attempts = 1000
        
        for i in range(num_objects):
            attempts = 0
            while attempts < max_attempts:
                # Random position
                max_size = self.config.object_size_range[1]
                x = random.randint(max_size // 2, width - max_size // 2)
                y = random.randint(max_size // 2, height - max_size // 2)
                
                # Check if position is valid (no overlap or sufficient distance)
                valid = True
                if not self.config.allow_overlap:
                    for px, py in positions:
                        distance = math.sqrt((x - px) ** 2 + (y - py) ** 2)
                        if distance < self.config.min_distance + max_size:
                            valid = False
                            break
                
                if valid:
                    positions.append((x, y))
                    break
                
                attempts += 1
            
            # If we couldn't find a valid position, use a random one anyway
            if len(positions) <= i:
                x = random.randint(max_size // 2, width - max_size // 2)
                y = random.randint(max_size // 2, height - max_size // 2)
                positions.append((x, y))
        
        return positions
    
    def _render_initial_state(self, task_data: dict) -> Image.Image:
        """Render image with objects to count."""
        img = Image.new("RGB", self.config.image_size, self.config.background_color)
        draw = ImageDraw.Draw(img)
        
        shapes = task_data["shapes"]
        colors = task_data["colors"]
        positions = task_data["positions"]
        sizes = task_data["sizes"]
        
        for i in range(len(shapes)):
            shape = shapes[i]
            color = colors[i]
            x, y = positions[i]
            size = sizes[i]
            
            self._draw_shape(draw, shape, x, y, size, color)
        
        return img
    
    def _render_final_state(self, task_data: dict) -> Image.Image:
        """Render final image showing the count."""
        # Start with the initial image
        img = self._render_initial_state(task_data)
        draw = ImageDraw.Draw(img)
        
        # Add count text
        count = task_data["num_objects"]
        text = f"Count: {count}"
        
        # Get font
        font_size = min(self.config.image_size) // 10
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Calculate text position (center)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (self.config.image_size[0] - text_width) // 2
        y = (self.config.image_size[1] - text_height) // 2
        
        # Draw text with background
        padding = 10
        draw.rectangle(
            [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
            fill=(255, 255, 255, 200)
        )
        draw.text((x, y), text, fill=(0, 0, 0), font=font)
        
        return img
    
    def _draw_shape(
        self,
        draw: ImageDraw.Draw,
        shape: str,
        center_x: int,
        center_y: int,
        size: int,
        color: Tuple[int, int, int]
    ):
        """Draw a shape at the given position."""
        half_size = size // 2
        
        if shape == "circle":
            # Draw circle
            bbox = [
                center_x - half_size,
                center_y - half_size,
                center_x + half_size,
                center_y + half_size
            ]
            draw.ellipse(bbox, fill=color, outline=(0, 0, 0), width=2)
        
        elif shape == "square":
            # Draw square
            bbox = [
                center_x - half_size,
                center_y - half_size,
                center_x + half_size,
                center_y + half_size
            ]
            draw.rectangle(bbox, fill=color, outline=(0, 0, 0), width=2)
        
        elif shape == "triangle":
            # Draw triangle (equilateral)
            height = int(size * math.sqrt(3) / 2)
            points = [
                (center_x, center_y - height // 2),  # Top
                (center_x - half_size, center_y + height // 2),  # Bottom left
                (center_x + half_size, center_y + height // 2),  # Bottom right
            ]
            draw.polygon(points, fill=color, outline=(0, 0, 0), width=2)
        
        elif shape == "star":
            # Draw star (5-pointed)
            num_points = 5
            outer_radius = half_size
            inner_radius = outer_radius * 0.4
            points = []
            
            for i in range(num_points * 2):
                angle = (i * math.pi) / num_points - math.pi / 2
                if i % 2 == 0:
                    radius = outer_radius
                else:
                    radius = inner_radius
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))
            
            draw.polygon(points, fill=color, outline=(0, 0, 0), width=2)
    
    def _generate_video(
        self,
        first_image: Image.Image,
        task_data: dict,
        task_id: str
    ) -> Optional[str]:
        """Generate ground truth video showing counting animation."""
        temp_dir = Path(tempfile.gettempdir()) / f"{self.config.domain}_videos"
        temp_dir.mkdir(parents=True, exist_ok=True)
        video_path = temp_dir / f"{task_id}_ground_truth.mp4"
        
        # Create frames showing counting animation
        frames = self._create_counting_animation_frames(task_data)
        
        result = self.video_generator.create_video_from_frames(
            frames,
            video_path
        )
        
        return str(result) if result else None
    
    def _create_counting_animation_frames(
        self,
        task_data: dict,
        hold_frames: int = 10,
        highlight_frames: int = 5
    ) -> List[Image.Image]:
        """
        Create animation frames showing objects being counted one by one.
        
        Each object is highlighted in sequence, then the final count is shown.
        """
        frames = []
        num_objects = task_data["num_objects"]
        shapes = task_data["shapes"]
        colors = task_data["colors"]
        positions = task_data["positions"]
        sizes = task_data["sizes"]
        
        # Initial frame (all objects visible)
        base_frame = self._render_initial_state(task_data)
        frames.extend([base_frame] * hold_frames)
        
        # Highlight each object in sequence
        for i in range(num_objects):
            # Create frame with this object highlighted
            highlighted_frame = self._render_frame_with_highlight(
                task_data, i
            )
            frames.extend([highlighted_frame] * highlight_frames)
        
        # Final frame showing count
        if self.config.use_final_image:
            final_frame = self._render_final_state(task_data)
        else:
            final_frame = base_frame
        
        frames.extend([final_frame] * hold_frames)
        
        return frames
    
    def _render_frame_with_highlight(
        self,
        task_data: dict,
        highlight_index: int
    ) -> Image.Image:
        """Render a frame with one object highlighted."""
        img = Image.new("RGB", self.config.image_size, self.config.background_color)
        draw = ImageDraw.Draw(img)
        
        shapes = task_data["shapes"]
        colors = task_data["colors"]
        positions = task_data["positions"]
        sizes = task_data["sizes"]
        
        for i in range(len(shapes)):
            shape = shapes[i]
            color = colors[i]
            x, y = positions[i]
            size = sizes[i]
            
            # Highlight the selected object
            if i == highlight_index:
                # Draw highlight circle around object
                highlight_size = size + 20
                highlight_bbox = [
                    x - highlight_size // 2,
                    y - highlight_size // 2,
                    x + highlight_size // 2,
                    y + highlight_size // 2
                ]
                draw.ellipse(highlight_bbox, outline=(255, 255, 0), width=4)
                # Make object brighter
                bright_color = tuple(min(255, c + 50) for c in color)
                self._draw_shape(draw, shape, x, y, size, bright_color)
            else:
                # Draw normal object (slightly faded)
                faded_color = tuple(max(0, c - 50) for c in color)
                self._draw_shape(draw, shape, x, y, size, faded_color)
        
        return img
    
    def generate_dataset_by_task_type(
        self, 
        tasks_per_type: int = 20,
        task_types: Optional[List[str]] = None
    ) -> List[TaskPair]:
        """
        Generate dataset with specified number of tasks for each task type.
        
        Args:
            tasks_per_type: Number of unique tasks to generate for each type
            task_types: List of task types to generate. If None, generates for all types.
            
        Returns:
            List of all generated TaskPairs
        """
        if task_types is None:
            # Default: all shape types + mixed
            task_types = self.config.object_types + ["mixed"]
        
        all_tasks = []
        
        for task_type in task_types:
            print(f"Generating {tasks_per_type} tasks for type: {task_type}")
            tasks = self.generate_tasks_for_type(
                task_type=task_type,
                num_tasks=tasks_per_type,
                task_id_prefix=self.config.domain
            )
            all_tasks.extend(tasks)
        
        return all_tasks
