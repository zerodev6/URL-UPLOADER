import time
import asyncio
import math
from typing import Optional

class Progress:
    """Progress tracker for downloads and uploads"""
    
    def __init__(self, client, message):
        self.client = client
        self.message = message
        self.start_time = time.time()
        self.last_update = 0
        self.update_interval = 3  # Update every 3 seconds
        
    async def progress_callback(self, current, total, status="Downloading"):
        """Progress callback for pyrogram"""
        now = time.time()
        
        # Update only every N seconds to avoid flood
        if now - self.last_update < self.update_interval:
            return
            
        self.last_update = now
        elapsed = now - self.start_time
        
        if current == 0 or elapsed == 0:
            return
            
        speed = current / elapsed
        percentage = current * 100 / total
        eta_seconds = (total - current) / speed if speed > 0 else 0
        
        # Format data
        current_mb = current / (1024 * 1024)
        total_mb = total / (1024 * 1024)
        speed_mb = speed / (1024 * 1024)
        
        # Create progress bar
        filled = int(percentage / 5)
        progress_bar = "█" * filled + "░" * (20 - filled)
        
        text = (
            f"**{status}**\n\n"
            f"{progress_bar} {percentage:.1f}%\n\n"
            f"**Size:** {current_mb:.2f} MB / {total_mb:.2f} MB\n"
            f"**Speed:** {speed_mb:.2f} MB/s\n"
            f"**ETA:** {format_time(eta_seconds)}\n"
            f"**Elapsed:** {format_time(elapsed)}"
        )
        
        try:
            await self.message.edit_text(text)
        except Exception:
            pass

def format_time(seconds):
    """Format seconds to human readable time"""
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        return f"{hours}h {minutes}m"

def humanbytes(size):
    """Convert bytes to human readable format"""
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    while size > power and n < len(units) - 1:
        size /= power
        n += 1
    return f"{size:.2f} {units[n]}"

async def speed_limiter(chunk_size, speed_limit):
    """Limit download/upload speed"""
    delay = chunk_size / speed_limit
    await asyncio.sleep(delay)

def is_url(text):
    """Check if text is a valid URL"""
    return text.startswith(('http://', 'https://', 'www.'))

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename
