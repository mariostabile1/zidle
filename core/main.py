#!/usr/bin/env python3
import os
import sys
import json
import random
import glob
import importlib.util

# Add core dir to path to import engine
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def load_config():
    config_path = os.path.expanduser('~/.config/zidle/config.json')
    defaults = {
        "timeout": 60,
        "scenes": [
            "matrix", 
            "clock", 
            "stats", 
            "starfield", 
            "bouncing", 
            "life"
        ],
        "theme": "default",
        "random_scene": True
    }
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                defaults.update(json.load(f))
        except Exception:
            pass
    return defaults

def load_scenes(zidle_dir):
    scenes = {}
    
    built_in_scenes = os.path.join(zidle_dir, 'scenes')
    user_scenes = os.path.expanduser('~/.config/zidle/scenes')
    
    dirs_to_check = [built_in_scenes]
    if os.path.exists(user_scenes):
        dirs_to_check.append(user_scenes)
        
    for s_dir in dirs_to_check:
        for file in glob.glob(os.path.join(s_dir, '*.py')):
            name = os.path.basename(file)[:-3]
            if name == '__init__':
                continue
            try:
                spec = importlib.util.spec_from_file_location(name, file)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, 'Scene'):
                    scenes[name] = mod.Scene
            except Exception:
                pass
    return scenes

def main():
    zidle_dir = os.environ.get('ZIDLE_DIR')
    if not zidle_dir:
        # Fallback to current file's grandparent
        zidle_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
    config = load_config()
    scenes_map = load_scenes(zidle_dir)
    
    enabled_scenes = config.get('scenes', [])
    available_scenes = [name for name in enabled_scenes if name in scenes_map]
    
    # Fallback to all loaded scenes if specific config fails
    if not available_scenes:
        available_scenes = list(scenes_map.keys())
        
    if not available_scenes:
        print("No scenes available.")
        sys.exit(1)
        
    if config.get('random_scene', True):
        selected_scene_name = random.choice(available_scenes)
    else:
        selected_scene_name = available_scenes[0]
        
    scene_class = scenes_map[selected_scene_name]
    
    # Run the standard engine
    import engine
    engine.run(scene_class)

if __name__ == '__main__':
    main()
