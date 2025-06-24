import json
import os

class CompletionTracker:
    def __init__(self, save_file="completed_levels.json"):
        self.save_file = save_file
        self.completed_levels = self.load_completed_levels()
    
    def load_completed_levels(self):
        #Load completed levels from file
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return set(json.load(f))
            return set()
        except (json.JSONDecodeError, FileNotFoundError):
            return set()
    
    def save_completed_levels(self):
        #Save completed levels to file
        try:
            with open(self.save_file, 'w') as f:
                json.dump(list(self.completed_levels), f)
        except Exception as e:
            print(f"Error saving completed levels: {e}")
    
    def mark_completed(self, level_name):
        #Mark a level as completed
        self.completed_levels.add(level_name)
        self.save_completed_levels()
    
    def is_completed(self, level_name):
        #Check if a level is completed
        return level_name in self.completed_levels
    
    def get_completion_percentage(self, available_levels):
        #Get completion percentage
        if not available_levels:
            return 0
        return (len(self.completed_levels) / len(available_levels)) * 100
    
    def reset_progress(self):
        #Reset all completion progress
        self.completed_levels.clear()
        self.save_completed_levels()
