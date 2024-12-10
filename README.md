# Hunyuan Prompt Generator

A lightweight alternative to Hunyuan's prompt rewrite model for video generation, designed to match their training data patterns and prompt structure.

## Why This Exists

The HunyuanVideo model was trained on a specific combination of datasets and prompt styles:
- ShareGPT4V annotations (high-quality GPT-4V descriptions)
- InternVL-SFT captioning patterns
- Structured JSON format with specific components
- 14 defined camera movement types

While Hunyuan provides their prompt rewrite model, it requires significant compute resources as it's based on Hunyuan-Large. This tool provides a lightweight alternative that:

1. Matches their structured format
2. Uses their specific camera movement types
3. Maintains their two-mode system:
   - Normal: Focus on accuracy and comprehension
   - Master: Enhanced composition, lighting, and camera movement
4. Can be used with various LLMs (GPT-4, GPT-3.5, etc.)

## Installation

```bash
# Clone the repository
git clone [repository-url]
cd hunyuan-prompt-generator

# Install requirements
pip install -r requirements.txt

# Set up your OpenAI API key
export OPENAI_API_KEY='your-key-here'
```

## Usage

### Basic Command Line Usage

Generate a normal mode prompt:
```bash
python cli.py -t "A cat playing in the garden" --mode normal
```

Generate a master mode prompt:
```bash
python cli.py -t "A cat playing in the garden" --mode master
```

Save output to JSON:
```bash
python cli.py -t "A cat playing in the garden" --format json --output prompts/output.json
```

### Arguments

```
Input Options:
  --text, -t TEXT         Text input to generate prompt from
  --image, -i IMAGE       Path to input image

Model Options:
  --mode {normal,master}  Prompt generation mode (default: normal)
  --model MODEL          LLM model to use (default: gpt-4)

Output Options:
  --output, -o OUTPUT     Output file path
  --format {text,json}    Output format (default: text)
  --save-components      Save intermediate structured components
```

### Example Outputs

Normal Mode:
```
A playful cat explores a sun-drenched garden, camera pans right to follow movement. 
Realistic style with natural daylight. Peaceful and serene atmosphere.
```

Master Mode:
```
A graceful feline explores a meticulously composed garden scene with balanced foreground elements. 
Smooth tracking shot with shallow depth of field, professional natural lighting with subtle rim highlights. 
Careful attention to motion continuity and spatial composition.
```

## Technical Details

Our prompt generation follows Hunyuan's structured approach:
1. Converts input to structured JSON components
2. Applies specific camera movement vocabulary
3. Maintains professional video production elements
4. Follows their training data hierarchy

The system supports two modes matching Hunyuan's approach:
- **Normal Mode**: Focuses on accurate interpretation of user intent
- **Master Mode**: Emphasizes composition, lighting, and camera movement for higher visual quality

## Camera Movements

Supports the same 14 camera movement types used in Hunyuan's training:
- Static shot
- Pan (up/down/left/right)
- Tilt (up/down/left/right)
- Zoom (in/out)
- Dolly tracking
- Around (left/right)
- Handheld shot

## Project Structure
```
hy-promptfun/
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
├── examples/
│   └── example_prompts.json
├── src/
│   └── hyprompt/
│       ├── __init__.py
│       ├── cli.py
│       ├── constants.py
│       ├── generator.py
│       └── llm_clients.py
└── tests/
    ├── __init__.py
    └── test_generator.py
```

## Disclaimer: Zero afflitation with any of the companies or models listed. And I have absolutely no idea if this will be effective or work.