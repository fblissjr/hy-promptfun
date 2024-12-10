# cli.py

import argparse
import sys
import os
from typing import Optional
from pathlib import Path
import json
from datetime import datetime
from prompt_emulator import HunyuanPromptEmulator
from openai import OpenAI

def setup_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Hunyuan-style prompt generator for video generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Input arguments
    input_group = parser.add_argument_group('Input Options')
    input_group.add_argument(
        '--text', '-t',
        type=str,
        help='Text input to generate prompt from'
    )
    input_group.add_argument(
        '--image', '-i',
        type=str,
        help='Path to input image'
    )
    
    # Mode and model arguments
    model_group = parser.add_argument_group('Model Options')
    model_group.add_argument(
        '--mode',
        choices=['normal', 'master'],
        default='normal',
        help='Prompt generation mode (default: normal)'
    )
    model_group.add_argument(
        '--model',
        choices=['gpt-4', 'gpt-3.5-turbo', 'claude'],
        default='gpt-4',
        help='LLM model to use (default: gpt-4)'
    )
    
    # Output arguments
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (default: prints to console)'
    )
    output_group.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    output_group.add_argument(
        '--save-components',
        action='store_true',
        help='Save intermediate structured components'
    )
    
    return parser

class LLMClient:
    """Factory for different LLM clients"""
    
    @staticmethod
    def create(model_name: str):
        if model_name.startswith('gpt'):
            return OpenAIClient(model_name)
        elif model_name == 'claude':
            # Add Claude implementation
            raise NotImplementedError("Claude support coming soon")
        else:
            raise ValueError(f"Unsupported model: {model_name}")

class OpenAIClient:
    def __init__(self, model_name: str):
        self.client = OpenAI()
        self.model = model_name
        
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating with OpenAI: {e}", file=sys.stderr)
            sys.exit(1)

def save_output(content: str, 
                output_path: Optional[str] = None, 
                format: str = 'text',
                components: Optional[dict] = None):
    """Save or print the generated prompt"""
    
    if output_path:
        path = Path(output_path)
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            output = {
                'prompt': content,
                'timestamp': datetime.now().isoformat(),
                'components': components
            }
            path.write_text(json.dumps(output, indent=2))
        else:
            path.write_text(content)
        print(f"Output saved to: {output_path}")
    else:
        if format == 'json':
            print(json.dumps({
                'prompt': content,
                'components': components
            }, indent=2))
        else:
            print("\nGenerated Prompt:")
            print("-" * 50)
            print(content)
            print("-" * 50)

def main():
    parser = setup_argparser()
    args = parser.parse_args()
    
    # Validate inputs
    if not args.text and not args.image:
        parser.error("Must provide either --text or --image input")
    if args.text and args.image:
        parser.error("Cannot provide both text and image input")
        
    # Create LLM client
    try:
        llm_client = LLMClient.create(args.model)
    except Exception as e:
        print(f"Error creating LLM client: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize prompt emulator
    emulator = HunyuanPromptEmulator(llm_client)
    
    try:
        # Generate prompt
        print(f"Generating {args.mode} mode prompt...")
        if args.image:
            with open(args.image, 'rb') as f:
                input_data = f.read()
        else:
            input_data = args.text
            
        prompt = emulator.generate_prompt(input_data, mode=args.mode)
        
        # Get components if requested
        components = None
        if args.save_components:
            components = emulator._get_structured_description(
                text=args.text,
                image=input_data if args.image else None
            )
        
        # Save/print output
        save_output(
            prompt, 
            args.output, 
            args.format,
            components
        )
        
    except Exception as e:
        print(f"Error during prompt generation: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()