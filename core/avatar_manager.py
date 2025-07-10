import streamlit as st
import base64
from PIL import Image
import io
import os
from config.settings import AGENTS_INFO, ROLE_TO_AVATAR, AVATAR_SIZE_CHAT, AVATAR_SIZE_ROUNDTABLE
import logging

# Set up logging
logger = logging.getLogger(__name__)

@st.cache_data
def get_image_base64(image_path):
    """Convert image to base64 string"""
    try:
        import base64
        from PIL import Image
        import io
        
        # Open and process image
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to avatar size
            img = img.resize((60, 60), Image.Resampling.LANCZOS)
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return img_str
            
    except Exception as e:
        print(f"Error converting image {image_path}: {e}")
        return None

@st.cache_data
def load_avatar_image(image_path, size=AVATAR_SIZE_CHAT):
    """Load avatar image for Streamlit chat display"""
    try:
        if not os.path.exists(image_path):
            logger.warning(f"Avatar image not found: {image_path}")
            return None
            
        img = Image.open(image_path)
        
        # Convert to RGB if necessary
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize image
        img = img.resize(size, Image.Resampling.LANCZOS)
        
        return img
        
    except Exception as e:
        logger.error(f"Error loading avatar for chat: {image_path} - {e}")
        return None

def create_role_to_image_mapping():
    """Create mapping of roles to avatar images"""
    role_to_image = {}
    
    for agent in AGENTS_INFO:
        agent_name = agent["name"]
        
        # Try to load avatar image
        if "image" in agent and os.path.exists(agent["image"]):
            avatar_img = load_avatar_image(agent["image"], size=AVATAR_SIZE_CHAT)
            if avatar_img is not None:
                role_to_image[agent_name] = avatar_img
            else:
                logger.warning(f"Failed to load avatar for {agent_name}, using emoji fallback")
                role_to_image[agent_name] = None
        else:
            logger.info(f"No avatar image configured for {agent_name}, using emoji")
            role_to_image[agent_name] = None
    
    # Add user avatar
    role_to_image["User"] = None
    
    return role_to_image

def get_avatar_for_role(role, role_to_image=None):
    """Get avatar for a role - ensure it returns proper image data"""
    if role_to_image and role in role_to_image:
        avatar_data = role_to_image[role]
        
        # If it's base64 image data, return it properly
        if isinstance(avatar_data, str) and avatar_data.startswith('data:image'):
            return avatar_data
        
        # If it's a file path or URL, convert to base64
        if isinstance(avatar_data, str):
            try:
                import base64
                from PIL import Image
                import io
                
                # Load and convert image to base64
                img = Image.open(avatar_data)
                img = img.resize((60, 60))  # Resize for consistency
                
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                
                return f"data:image/png;base64,{img_str}"
            except:
                pass
    
    # Return emoji fallback
    from config.settings import ROLE_TO_AVATAR
    return ROLE_TO_AVATAR.get(role, "❓")

def create_roundtable_avatar_html(agent_name, position, is_active=False, is_thinking=False):
    """Create HTML for a single roundtable avatar"""
    agent_info = next((agent for agent in AGENTS_INFO if agent["name"] == agent_name), None)
    
    if not agent_info:
        return ""
    
    # Determine avatar classes
    classes = ["avatar"]
    if is_thinking:
        classes.append("thinking")
    elif is_active:
        classes.append("active")
    
    # Create avatar content (image or emoji)
    avatar_content = agent_info["avatar"]  # Default to emoji
    
    if "image" in agent_info and os.path.exists(agent_info["image"]):
        image_base64 = get_image_base64(agent_info["image"], AVATAR_SIZE_ROUNDTABLE)
        if image_base64:
            avatar_content = f'<img src="data:image/png;base64,{image_base64}" alt="{agent_name}">'
    
    # Create HTML
    html = f'''
    <div class="{" ".join(classes)}" 
         style="left: {position[0]}px; top: {position[1]}px;" 
         title="{agent_name}">
        {avatar_content}
        <div class="avatar-label">{agent_name}</div>
    </div>
    '''
    
    return html

def validate_avatar_files():
    """Validate that avatar files exist and are accessible"""
    missing_files = []
    corrupted_files = []
    
    for agent in AGENTS_INFO:
        if "image" in agent:
            image_path = agent["image"]
            
            # Check if file exists
            if not os.path.exists(image_path):
                missing_files.append(f"{agent['name']}: {image_path}")
                continue
            
            # Try to load the image
            try:
                with Image.open(image_path) as img:
                    # Basic validation
                    if img.size[0] < 10 or img.size[1] < 10:
                        corrupted_files.append(f"{agent['name']}: Image too small")
                    elif img.size[0] > 1000 or img.size[1] > 1000:
                        logger.warning(f"Large avatar image for {agent['name']}: {img.size}")
            except Exception as e:
                corrupted_files.append(f"{agent['name']}: {str(e)}")
    
    # Report results
    if missing_files:
        logger.warning(f"Missing avatar files: {missing_files}")
    
    if corrupted_files:
        logger.error(f"Corrupted avatar files: {corrupted_files}")
    
    return {
        "missing": missing_files,
        "corrupted": corrupted_files,
        "total_agents": len(AGENTS_INFO),
        "valid_avatars": len(AGENTS_INFO) - len(missing_files) - len(corrupted_files)
    }

def get_avatar_fallback_emoji(agent_name):
    """Get fallback emoji for an agent if image is not available"""
    emoji_mapping = {
        "Academic Mentor": "🎓",
        "Career Guide": "💼", 
        "Tech Innovator": "💻",
        "Wellness Coach": "🧘",
        "Life Skills Mentor": "🌟",
        "Creative Mentor": "🎨",
        "Leadership Coach": "👑",
        "Financial Advisor": "💰",
        "Communication Expert": "🗣️",
        "Global Perspective Mentor": "🌍"
    }
    
    return emoji_mapping.get(agent_name, "❓")

def optimize_avatar_for_web(image_path, output_size=(60, 60), quality=85):
    """Optimize avatar image for web display"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            
            # Save optimized version
            optimized_path = image_path.replace('.png', '_optimized.png')
            img.save(optimized_path, 'PNG', optimize=True, quality=quality)
            
            return optimized_path
            
    except Exception as e:
        logger.error(f"Error optimizing avatar {image_path}: {e}")
        return image_path