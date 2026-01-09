#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           TASK GENERATION SCRIPT                              ║
║                                                                               ║
║  Run this to generate your dataset.                                           ║
║  Customize TaskConfig and TaskGenerator in src/ for your task.                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Usage:
    python3 examples/generate.py --num-samples 100
    python3 examples/generate.py --num-samples 100 --output data/my_task --seed 42
    python3 examples/generate.py --by-task-type --tasks-per-type 20
"""

import argparse
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import OutputWriter
from core.video_utils import VideoGenerator
from src import TaskGenerator, TaskConfig


def main():
    parser = argparse.ArgumentParser(
        description="Generate task dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 examples/generate.py --num-samples 10
    python3 examples/generate.py --num-samples 100 --output data/output --seed 42
    python3 examples/generate.py --by-task-type --tasks-per-type 20
    python3 examples/generate.py --total-tasks 20  # Generate 20 tasks total, distributed across all types
        """
    )
    parser.add_argument(
        "--num-samples",
        type=int,
        default=None,
        help="Number of task samples to generate (legacy mode)"
    )
    parser.add_argument(
        "--by-task-type",
        action="store_true",
        help="Generate tasks by task type"
    )
    parser.add_argument(
        "--tasks-per-type",
        type=int,
        default=None,
        help="Number of tasks to generate per task type"
    )
    parser.add_argument(
        "--total-tasks",
        type=int,
        default=None,
        help="Total number of tasks to generate, distributed across all task types"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/questions",
        help="Output directory (default: data/questions)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--no-videos",
        action="store_true",
        help="Disable video generation"
    )
    
    args = parser.parse_args()
    
    # ──────────────────────────────────────────────────────────────────────────
    #  Configure your task here
    #  Add any additional TaskConfig parameters as needed
    # ──────────────────────────────────────────────────────────────────────────
    
    generate_videos = not args.no_videos
    
    # Check video generation availability
    if generate_videos:
        if VideoGenerator.is_available():
            print("✅ Video generation enabled (ground_truth.mp4 will be generated)")
        else:
            print("⚠️  Warning: opencv-python not installed. Video generation will be disabled.")
            print("   Install with: pip install opencv-python")
            print("   Continuing without video generation...")
            generate_videos = False
    
    config = TaskConfig(
        num_samples=args.num_samples or 0,  # Not used when by-task-type
        random_seed=args.seed,
        output_dir=Path(args.output),
        generate_videos=generate_videos,
    )
    
    # Generate tasks
    generator = TaskGenerator(config)
    
    if args.total_tasks:
        # Generate total tasks distributed across all task types
        task_types = config.object_types + ["mixed"]
        num_types = len(task_types)
        tasks_per_type = args.total_tasks // num_types
        remainder = args.total_tasks % num_types
        
        print(f"🎲 Generating {args.total_tasks} total tasks ({tasks_per_type} per type, with {remainder} extra)...")
        tasks = []
        
        # Generate base tasks for each type
        for i, task_type in enumerate(task_types):
            num_tasks = tasks_per_type + (1 if i < remainder else 0)
            if num_tasks > 0:
                print(f"  Generating {num_tasks} tasks for type: {task_type}")
                type_tasks = generator.generate_tasks_for_type(
                    task_type=task_type,
                    num_tasks=num_tasks,
                    task_id_prefix=config.domain
                )
                tasks.extend(type_tasks)
    elif args.by_task_type:
        # Generate tasks by type: specified number per type
        tasks_per_type = args.tasks_per_type or 20
        print(f"🎲 Generating {tasks_per_type} unique tasks for each task type...")
        tasks = generator.generate_dataset_by_task_type(
            tasks_per_type=tasks_per_type
        )
    else:
        # Legacy mode: generate random tasks
        if args.num_samples is None:
            parser.error("Either --num-samples, --by-task-type, or --total-tasks must be specified")
        print(f"🎲 Generating {args.num_samples} tasks...")
        tasks = generator.generate_dataset()
    
    # Write to disk
    writer = OutputWriter(Path(args.output))
    writer.write_dataset(tasks)
    
    print(f"✅ Done! Generated {len(tasks)} tasks in {args.output}/{config.domain}_task/")


if __name__ == "__main__":
    main()
