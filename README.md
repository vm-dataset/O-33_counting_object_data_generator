# Counting Objects Task Data Generator 🔢

A data generator for creating counting objects reasoning tasks for VMEvalKit. Generates images with random numbers of objects (circles, squares, triangles, stars) for video models to count.

This task generator follows the [template-data-generator](https://github.com/vm-dataset/template-data-generator.git) format and is compatible with [VMEvalKit](https://github.com/Video-Reason/VMEvalKit.git).

Repository: [O-33_counting_object_data-generator](https://github.com/vm-dataset/O-33_counting_object_data-generator)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/vm-dataset/O-33_counting_object_data-generator.git
cd O-33_counting_object_data-generator

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# 4. Generate counting tasks
python examples/generate.py --num-samples 50
```

---

## 📁 Project Structure

```
counting_objects_task-data-generator/
├── core/                    # ✅ Framework utilities (DO NOT MODIFY)
│   ├── __init__.py
│   ├── base_generator.py   # Abstract base class
│   ├── schemas.py          # Pydantic models
│   ├── image_utils.py      # Image helpers
│   ├── video_utils.py      # Video generation
│   └── output_writer.py    # File output
├── src/                     # ✅ Counting objects task implementation
│   ├── __init__.py
│   ├── generator.py        # Counting objects generator
│   ├── prompts.py          # Counting task prompts
│   └── config.py           # Task configuration
├── examples/
│   └── generate.py         # Entry point script
├── setup.py                # Package setup
├── requirements.txt        # Dependencies
└── README.md               # This file
```

---

## 📦 Output Format

Every generator produces tasks in the following structure:

```
data/questions/{domain}_task/{task_id}/
├── first_frame.png          # Initial state (REQUIRED)
├── final_frame.png          # Goal state (or goal.txt)
├── prompt.txt               # Instructions (REQUIRED)
└── ground_truth.mp4         # Solution video (OPTIONAL)
```

### File Descriptions

- **`first_frame.png`**: Initial image containing objects to count (always present)
- **`final_frame.png`**: Final image showing the count result (optional, can use `goal.txt` instead)
- **`goal.txt`**: Text file containing the answer (alternative to `final_frame.png`)
- **`prompt.txt`**: Task instructions for the video model (always present)
- **`ground_truth.mp4`**: Ground truth video showing the counting process (optional)

---

## 🎨 Configuration

The counting objects task can be customized via `src/config.py`:

```python
class TaskConfig(GenerationConfig):
    # Object counting settings
    min_objects: int = 1              # Minimum number of objects
    max_objects: int = 20             # Maximum number of objects
    object_types: list[str] = ["circle", "square", "triangle", "star"]
    object_size_range: tuple[int, int] = (30, 60)  # Size in pixels
    use_same_shape: bool = True       # All objects same shape or mixed
    allow_overlap: bool = False       # Whether objects can overlap
    use_final_image: bool = True      # Use final_frame.png (default) or goal.txt
    # ... and more
```

### Usage Examples

```bash
# Generate 50 tasks with default settings
python examples/generate.py --num-samples 50

# Generate 100 tasks with custom output directory and seed
python examples/generate.py --num-samples 100 --output data/my_tasks --seed 42

# Generate tasks without videos (faster)
python examples/generate.py --num-samples 20 --no-videos
```

---

## 📊 Task Description

### Counting Objects Task

This task generates images with random numbers of geometric objects (circles, squares, triangles, stars) and asks the video model to count them. Each task includes:

- **`first_frame.png`**: Image with objects to count
- **`final_frame.png`**: Image showing the count result (default) or `goal.txt` if configured
- **`prompt.txt`**: Instructions for the video model (e.g., "Count the number of objects in the image and show the result.")
- **`ground_truth.mp4`**: Optional animation showing the counting process

The task can be configured to use different object shapes, colors, sizes, and layouts. Objects can be constrained to not overlap, or allowed to overlap for more complex counting scenarios.

---

## 🔧 Development

### Customizing the Task

To customize this task generator:

1. **Modify prompts**: Edit `src/prompts.py` to change task instructions
2. **Adjust configuration**: Edit `src/config.py` to change generation parameters
3. **Change generation logic**: Edit `src/generator.py` to modify how tasks are created

### Framework Files

Files in the `core/` directory are framework utilities and should **NOT** be modified. These are shared across all task generators using the template-data-generator format.

---

## 📝 License

This project follows the template-data-generator format and is licensed under the MIT License.