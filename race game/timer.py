import pygame

class Timer:
    def __init__(self):
        self.total_milliseconds = 0
        self.lap_times = []  # Stores all completed lap times
        self.previous_lap_time = None  # Last completed lap time
        self.lap_number = 0
    
    def update(self, delta):
        """delta: Time elapsed in seconds"""
        self.total_milliseconds += delta * 1000
    
    def complete_lap(self):
        """Call this when a car crosses the finish line"""
        self.lap_times.append(self.total_milliseconds)
        self.previous_lap_time = self.total_milliseconds
        self.total_milliseconds = 0  # Reset for next lap
        return self.previous_lap_time
    
    def get_best_lap(self):
        """Returns the fastest lap time, or None if no laps completed"""
        return min(self.lap_times[1:]) if len(self.lap_times) > 1 else None
    
    def format_time(self, milliseconds):
        """Helper to format milliseconds as MM:SS.mmm"""
        total_seconds = milliseconds / 1000
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        ms = int(milliseconds % 1000)
        return f'{minutes:02d}:{seconds:02d}.{ms:03d}'
    
    def draw(self, font: pygame.font.Font, surface: pygame.surface.Surface, position):
        text = self.format_time(self.total_milliseconds)
        rendered_text = font.render(text, False, (255, 255, 255))
        surface.blit(rendered_text, position)
    
    def draw_lap_info(self, font: pygame.font.Font, surface: pygame.surface.Surface, position):
        """Draw current lap, best lap, and previous lap"""
        self.lap_number = len(self.lap_times)
        best_lap = self.get_best_lap()
        
        info_lines = [
            f"LAP: {self.lap_number}",
            f"BEST: {self.format_time(best_lap) if best_lap != None else '--:--.---'}"
        ]
        if self.previous_lap_time:
            info_lines.append(f"PREV: {self.format_time(self.previous_lap_time)}")
        
        y_offset = 0
        for line in info_lines:
            rendered = font.render(line, False, (255, 255, 255))
            surface.blit(rendered, (position[0], position[1] + y_offset))
            y_offset += rendered.get_rect().height+1
    
    def reset(self):
        self.total_milliseconds = 0
        self.lap_times = []
        self.previous_lap_time = None
        self.lap_number = 0
