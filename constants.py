# constants.py

CAMERA_MOVEMENTS = [
    "static shot",
    "pan up", "pan down", "pan left", "pan right",
    "tilt up", "tilt down", "tilt left", "tilt right", 
    "zoom in", "zoom out",
    "dolly tracking",
    "around left", "around right",
    "handheld shot"
]

VISUAL_STYLES = [
    "cinematic",
    "documentary",
    "realistic",
    "professional",
    "high-end film",
]

LIGHTING_CONDITIONS = [
    "natural daylight",
    "golden hour",
    "blue hour",
    "studio lighting",
    "practical lights",
    "dramatic lighting",
    "soft diffused light",
    "high contrast",
    "volumetric lighting"
]

PROMPT_TEMPLATES = {
    "normal": """Convert this input into clear, accurate video instructions.

Required components:
1. Main subject and action
2. Camera movement (choose from: {camera_movements})
3. Visual style (choose from: {visual_styles})
4. Lighting (choose from: {lighting_conditions})
5. Scene atmosphere

Format the output as:
[Main Action], [Camera Movement]. [Style] with [Lighting]. [Atmosphere]

Focus on accuracy and clarity over stylistic elements.
""",
    
    "master": """Convert this input into professional cinematic video instructions.

Required components:
1. Main subject and action with technical details
2. Advanced camera movement (choose from: {camera_movements})
3. Professional style (choose from: {visual_styles})
4. Complex lighting setup (choose from: {lighting_conditions})
5. Composition details
6. Motion dynamics

Format the output as:
[Detailed Action] with [Technical Details]. [Advanced Camera Movement] with [Professional Lighting]. [Composition Details]

Emphasize cinematic quality and professional production value.
"""
}