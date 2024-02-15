"""
    Description: Intelligent Gallery app iniator.
    Author: Sachin Khandewal
    Email: sachinkhandewal5@gmail.com
"""

from src.intelligent_gallery import IntelligentGallery

int_gallery = IntelligentGallery("cats_and_dogs")
# specify mode as "public" for a Gradio public hosted UI.
int_gallery.gradio_ui(mode="local")