import os
import pygame
from level_loader import load_level

# Screen dimensions (should match main.py)
WIDTH, HEIGHT = 1280, 720


def get_available_levels():
    """Get list of available level files"""
    levels_dir = "levels"
    levels = []
    if os.path.exists(levels_dir):
        for file in os.listdir(levels_dir):
            if file.endswith('.json'):
                level_name = file[:-5]  # Remove .json extension
                levels.append(level_name)
    return sorted(levels)


def generate_level_preview(level_name, preview_width=400, preview_height=300):
    """Generate a preview surface for a level using actual game images"""
    preview_surface = pygame.Surface((preview_width, preview_height))
    preview_surface.fill((50, 50, 100))  # Dark blue background
    
    try:
        # Load level data
        objects = load_level(level_name)
        
        # Find bounds of the level
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for obj in objects:
            min_x = min(min_x, obj.rect.x)
            min_y = min(min_y, obj.rect.y)
            max_x = max(max_x, obj.rect.x + obj.rect.width)
            max_y = max(max_y, obj.rect.y + obj.rect.height)
        
        if min_x == float('inf'):  # Empty level
            return preview_surface
        
        # Calculate scale to fit level in preview
        level_width = max_x - min_x
        level_height = max_y - min_y
        
        scale_x = preview_width / max(level_width, 1)
        scale_y = preview_height / max(level_height, 1)
        scale = min(scale_x, scale_y, 0.3)  # Limit max scale for better visibility
        
        # Draw objects using their actual images
        for obj in objects:
            # Calculate preview position
            preview_x = int((obj.rect.x - min_x) * scale)
            preview_y = int((obj.rect.y - min_y) * scale)
            preview_w = max(int(obj.rect.width * scale), 1)
            preview_h = max(int(obj.rect.height * scale), 1)
            
            # Get the actual image from the object and scale it down
            if hasattr(obj, 'image') and obj.image:
                try:
                    # Scale the object's image to fit the preview
                    scaled_image = pygame.transform.scale(obj.image, (preview_w, preview_h))
                    preview_surface.blit(scaled_image, (preview_x, preview_y))
                except (pygame.error, ValueError):
                    # If scaling fails, use a colored rectangle as fallback
                    color = get_object_fallback_color(obj)
                    pygame.draw.rect(preview_surface, color, (preview_x, preview_y, preview_w, preview_h))
            else:
                # If no image, use colored rectangle
                color = get_object_fallback_color(obj)
                pygame.draw.rect(preview_surface, color, (preview_x, preview_y, preview_w, preview_h))
    
    except Exception as e:
        # If level fails to load, show error message
        font = pygame.font.SysFont("Arial", 20)
        error_text = font.render("Preview Error", True, (255, 100, 100))
        preview_surface.blit(error_text, (10, 10))
        print(f"Preview generation error for {level_name}: {e}")
    
    return preview_surface


def get_object_fallback_color(obj):
    """Get fallback color for objects when image is not available"""
    if hasattr(obj, 'name'):
        if obj.name == "fire":
            return (255, 100, 0)  # Orange for fire
        elif obj.name == "fan":
            return (150, 150, 255)  # Light blue for fan
        elif "saw" in obj.name.lower():
            return (200, 200, 200)  # Gray for saw
        elif obj.name == "finish":
            return (255, 215, 0)  # Gold for finish line
    return (100, 200, 100)  # Default green for blocks


def draw_slideshow_menu(window, background, bg_image, selected_level, available_levels, level_previews, completion_tracker):
    """Draw the slideshow-style level selection menu"""
    # Draw background
    for tile in background:
        window.blit(bg_image, tile)
    
    # Semi-transparent overlay for better text visibility
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))
    
    # Fonts
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    level_font = pygame.font.SysFont("Arial", 48, bold=True)
    counter_font = pygame.font.SysFont("Arial", 36)
    instruction_font = pygame.font.SysFont("Arial", 28)
    
    # Title
    title_text = title_font.render("JUMP N RUN", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
    window.blit(title_text, title_rect)
    
    if available_levels:
        current_level = available_levels[selected_level]
        is_completed = completion_tracker.is_completed(current_level)
        
        # Level counter
        counter_text = counter_font.render(f"{selected_level + 1} / {len(available_levels)}", True, (200, 200, 200))
        counter_rect = counter_text.get_rect(center=(WIDTH // 2, 150))
        window.blit(counter_text, counter_rect)
        
        # Completion status
        if is_completed:
            completed_text = counter_font.render("✓ COMPLETED", True, (0, 255, 0))
            completed_rect = completed_text.get_rect(center=(WIDTH // 2 + 200, 150))
            window.blit(completed_text, completed_rect)
        
        # Current level name
        level_color = (0, 255, 0) if is_completed else (255, 255, 100)
        level_text = level_font.render(current_level.upper(), True, level_color)
        level_rect = level_text.get_rect(center=(WIDTH // 2, 200))
        window.blit(level_text, level_rect)
        
        # Preview box
        preview_width = 400
        preview_height = 300
        preview_x = (WIDTH - preview_width) // 2
        preview_y = 250
        
        # draw preview border (green if completed, yellow if not)
        border_color = (0, 255, 0) if is_completed else (255, 255, 100)
        border_rect = pygame.Rect(preview_x - 5, preview_y - 5, preview_width + 10, preview_height + 10)
        pygame.draw.rect(window, border_color, border_rect, 3)
        
        # Draw preview
        if current_level in level_previews:
            window.blit(level_previews[current_level], (preview_x, preview_y))
        else:
            # Generate preview if not cached
            preview = generate_level_preview(current_level, preview_width, preview_height)
            level_previews[current_level] = preview
            window.blit(preview, (preview_x, preview_y))
        
        # Navigation arrows
        arrow_font = pygame.font.SysFont("Arial", 60, bold=True)
        
        # Left arrow (if not first level)
        if selected_level > 0:
            left_arrow = arrow_font.render("◀", True, (255, 255, 255))
            left_rect = left_arrow.get_rect(center=(100, 400))
            window.blit(left_arrow, left_rect)
        
        # Right arrow (if not last level)
        if selected_level < len(available_levels) - 1:
            right_arrow = arrow_font.render("▶", True, (255, 255, 255))
            right_rect = right_arrow.get_rect(center=(WIDTH - 100, 400))
            window.blit(right_arrow, right_rect)
    
    pygame.display.update()


def draw_death_screen(window):
    """Draw the death/game over screen"""
    # Semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(10)
    overlay.fill((0, 0, 0))
    window.blit(overlay, (0, 0))
    
    # Fonts 
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    instruction_font = pygame.font.SysFont("Arial", 36)
    
    # Game Over text
    game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    window.blit(game_over_text, game_over_rect)
    
    # Instructions
    retry_text = instruction_font.render("Press R to Retry", True, (255, 255, 255))
    retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    window.blit(retry_text, retry_rect)
    
    menu_text = instruction_font.render("Press Q or ESC to Return to Menu", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70))
    window.blit(menu_text, menu_rect)
    
    pygame.display.update()


def draw_level_completion_ui(window):
    """Draw the level completion overlay"""
    font = pygame.font.SysFont("Arial", 48, bold=True)
    completion_text = font.render("LEVEL COMPLETE!", True, (255, 255, 0))
    completion_rect = completion_text.get_rect(center=(WIDTH // 2, 100))
    window.blit(completion_text, completion_rect)
    
    instruction_font = pygame.font.SysFont("Arial", 32)
    next_text = instruction_font.render("Press N for next level or ESC for menu", True, (255, 255, 255))
    next_rect = next_text.get_rect(center=(WIDTH // 2, 150))
    window.blit(next_text, next_rect)


class MenuHandler:
    """Class to handle menu state and navigation"""
    
    def __init__(self):
        self.available_levels = get_available_levels()
        self.selected_level_index = 0
        self.level_previews = {}  # Cache for level previews
    
    def get_current_level_name(self):
        """Get the currently selected level name"""
        if self.available_levels:
            return self.available_levels[self.selected_level_index]
        return "level"
    
    def navigate_left(self):
        """Navigate to previous level"""
        if self.available_levels:
            self.selected_level_index = (self.selected_level_index - 1) % len(self.available_levels)
    
    def navigate_right(self):
        """Navigate to next level"""
        if self.available_levels:
            self.selected_level_index = (self.selected_level_index + 1) % len(self.available_levels)
    
    def go_to_next_level(self):
        """Move to the next level (for level completion)"""
        if self.available_levels:
            self.selected_level_index = (self.selected_level_index + 1) % len(self.available_levels)
            return self.get_current_level_name()
        return "level"
    
    def draw(self, window, background, bg_image, completion_tracker):
        """Draw the menu"""
        draw_slideshow_menu(
            window, background, bg_image, 
            self.selected_level_index, self.available_levels, 
            self.level_previews, completion_tracker
        )
