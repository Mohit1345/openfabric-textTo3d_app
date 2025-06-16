import streamlit as st
import requests
import uuid
import glob
import random
import os
import base64
import json
import time
# Assuming config.py contains something like: BACKEND_URL = "http://localhost:8000"
from config import BACKEND_URL

# Initialize session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

# App config
st.set_page_config(
    page_title="✨ Creative AI Partner",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS (No changes needed here, keeping it as is) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .block-container {
        padding: 0;
        margin: 0;
        max-width: 80%;
    }
    
    .main > div {
        padding: 0;
    }
    
    /* Dark theme with gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
        min-height: 100vh;
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 60px 40px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.3);
        z-index: 1;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        background: linear-gradient(45deg, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(255,255,255,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 300;
        opacity: 0.9;
        margin-bottom: 30px;
    }
    
    /* Create Section */
    .create-section {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 40px;
        margin: 40px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    .section-title {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 30px;
        color: #ffffff;
        text-align: center;
    }
    
    /* Input Styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(255,255,255,0.2) !important;
        border-radius: 16px !important;
        color: white !important;
        font-size: 16px !important;
        padding: 16px 20px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Toggle Switch */
    .stCheckbox > label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 16px 40px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 20px rgba(17, 153, 142, 0.3) !important;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 30px rgba(17, 153, 142, 0.5) !important;
    }
    
    /* Gallery Section */
    .gallery-section {
        margin: 85px;
        padding: 40px;
        background: rgba(255,255,255,0.03);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Recent Creations - Floating Cards */
    .recent-creations {
        position: relative;
        min-height: 400px;
        margin: 40px;
        padding: 40px;
        background: rgba(255,255,255,0.02);
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.1);
        overflow: hidden;
    }
    
    .floating-card {
        position: absolute;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: float 6s ease-in-out infinite;
    }
    
    .floating-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating-card img {
        border-radius: 12px;
        width: 100%;
        height: auto;
        max-width: 200px;
    }
    
    .floating-card h4 {
        color: white;
        margin: 10px 0 5px 0;
        font-size: 14px;
        font-weight: 600;
    }
    
    .floating-card p {
        color: rgba(255,255,255,0.7);
        font-size: 12px;
        margin: 0;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: rgba(17, 153, 142, 0.2) !important;
        border: 1px solid rgba(17, 153, 142, 0.4) !important;
        border-radius: 12px !important;
        color: #38ef7d !important;
    }
    
    .stError {
        background: rgba(234, 67, 53, 0.2) !important;
        border: 1px solid rgba(234, 67, 53, 0.4) !important;
        border-radius: 12px !important;
        color: #ff6b6b !important;
    }
    
    /* Image styling */
    .stImage {
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .create-section, .gallery-section, .recent-creations {
            margin: 20px;
            padding: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">✨ Creative AI Partner</h1>
            <p class="hero-subtitle">Transform your imagination into stunning visual art</p>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- Helper functions ---

# <<< CORRECTION >>>: get_gallery_images_from_json is largely okay, but robust path checking will be done later.
def get_gallery_images_from_json():
    """Extract gallery images and prompts from chat_data.json"""
    try:
        json_paths = ["../app/output/chat_data.json", "./output/chat_data.json", "output/chat_data.json", "app/output/chat_data.json", "chat_data.json"]
        chat_data = None
        json_file_path = None
        for path in json_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        chat_data = json.load(f)
                    json_file_path = path
                    break
                except (json.JSONDecodeError, IOError):
                    continue
        if not chat_data:
            return []

        gallery_items = []
        for idx, item in enumerate(chat_data):
            if isinstance(item, dict):
                session_entries = item.get('session_data', [])

                print("session, ", session_entries)
                
                for entry in session_entries:
                    image_path = entry.get('image_path')
                    print("img",image_path)
                    original_prompt = (
                        entry.get('original_prompt') or 
                        item.get('original_prompt') or 
                        item.get('prompt', 'No prompt found.')
                    )

                    if image_path:
                        print("Original image_path from JSON:", image_path)

                        # Always extract just the filename from the full path (works even for container paths)
                        filename = os.path.basename(image_path)
                        print("Resolved filename:", filename)

                        # Construct host-relative path (based on your volume mount)
                        # Example: app/output/images/image_123.png
                        relative_path = os.path.join("..","app", "output", "images", filename)

                        # Make it absolute for internal use (optional but recommended for safety)
                        abs_path = os.path.abspath(relative_path)

                        gallery_items.append({
                            'image_path': abs_path,  # This can also be relative_path if Streamlit works with relative paths
                            'original_prompt': original_prompt,
                            'filename': filename,
                            'index': idx
                        })


        # Optional: Sort by reverse index (most recent sessions first)
        gallery_items.sort(key=lambda x: x['index'], reverse=True)


        print("gallery_items", gallery_items)

        return gallery_items
    except Exception:
        return []

# <<< CORRECTION >>>: Made the fallback more robust by not stopping after the first match.
def get_gallery_images_fallback():
    """Fallback function using file glob to find all images."""
    try:
        possible_patterns = [
            "../app/output/images/*.png", "../app/output/*.png", "./output/images/*.png",
            "./output/*.png", "output/images/*.png", "output/*.png", "images/*.png", "*.png",
        ]
        
        # Use a set to store found images to avoid duplicates
        found_image_paths = set()
        for path_pattern in possible_patterns:
            found_image_paths.update(glob.glob(path_pattern))
            
        gallery_items = [{
            'image_path': img_path,
            'original_prompt': "Prompt not available (fallback)",
            'filename': os.path.basename(img_path),
            'index': i
        } for i, img_path in enumerate(sorted(list(found_image_paths), key=os.path.getmtime, reverse=True))]
        
        return gallery_items
    except Exception:
        return []

def get_gallery_data():
    """Main function to get gallery data - tries JSON first, then fallback"""
    gallery_items = get_gallery_images_from_json()
    print("gallery_items from json", gallery_items)
    if not gallery_items:
        gallery_items = get_gallery_images_fallback()
    return gallery_items

def get_image_base64(image_path):
    """Convert image to base64, return empty string if error"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def generate_random_positions(num_items):
    """Generate non-overlapping random positions for floating cards"""
    if num_items == 0:
        return []
    
    positions = []
    for i in range(num_items):
        attempts = 0
        while attempts < 50:
            left = random.randint(5, 75)
            top = random.randint(5, 65)
            overlap = any(abs(pos['left'] - left) < 20 and abs(pos['top'] - top) < 25 for pos in positions)
            if not overlap:
                positions.append({'left': left, 'top': top, 'delay': random.uniform(0, 2)})
                break
            attempts += 1
        if attempts == 50: # Fallback if no non-overlapping position is found
            positions.append({'left': (i * 25) % 75, 'top': (i * 20) % 65, 'delay': random.uniform(0, 2)})
    return positions


# --- Create Section ---
# st.markdown('<div class="create-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🎨 Create New Masterpiece</h2>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_input("", placeholder="Describe your creative vision...", key="prompt_input")
with col2:
    ai_enhance = st.checkbox("✨ AI Enhancement", value=True)
    long_term_memory = st.checkbox("🔍 Recall Long-Term Memory", value=True)

if st.button("🚀 Generate Art", key="generate_btn"):
    if prompt:
        payload = {
            "prompt": prompt,
            "ai_enhaned": ai_enhance,
            "session_id": st.session_state["session_id"],
            "recallLongTermMemory": long_term_memory
        }
        with st.spinner("🎨 Creating your masterpiece..."):
            try:
                response = requests.post(f"{BACKEND_URL}/execution", json=payload, timeout=300)
                if response.status_code == 200:
                    resp_json = response.json()
                    response_data = resp_json.get('response', {})
                    st.success(response_data.get('message', 'Art created successfully!'))
                    
                    if "image_path" in response_data and os.path.exists(response_data["image_path"]):
                        st.image(response_data["image_path"], caption="🎨 Generated Artwork")
                        with open(response_data["image_path"], "rb") as f:
                            st.download_button("💾 Download Image", f.read(), os.path.basename(response_data["image_path"]), "image/png")
                    elif "image_path" in response_data:
                        st.warning(f"⚠️ Generated image file not found at path: {response_data['image_path']}")
                    # ... (rest of the response handling is fine) ...
                else:
                    st.error(f"❌ Backend error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Could not connect to backend: {e}")
            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {e}")
    else:
        st.warning("⚠️ Please enter a creative prompt first!")
# st.markdown('</div>', unsafe_allow_html=True)


# --- Data Loading and Filtering ---
# <<< CORRECTION >>>: This is the key fix for the "blank spaces" problem.
# We get all potential data, then filter it to keep only items with image files that actually exist.
gallery_data = get_gallery_data()
valid_gallery_data = [item for item in gallery_data if item.get('image_path') and os.path.exists(item['image_path'])]


# --- Recent Creations Section ---
# <<< CORRECTION >>>: Check if there are any *valid* items before rendering the section.
if valid_gallery_data:
    #  class="recent-creations"
    st.markdown('<div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">✨ Recent Creations</h2>', unsafe_allow_html=True)

    # Select random items from the *valid* list
    recent_items = random.sample(valid_gallery_data, min(6, len(valid_gallery_data)))
    
    if recent_items:
        positions = generate_random_positions(len(recent_items))
        for i, item in enumerate(recent_items):
            pos = positions[i]
            img_base64 = get_image_base64(item['image_path'])
            # display_prompt = (item['original_prompt'][:30] + '...') if len(item['original_prompt']) > 30 else item['original_prompt']
            
            # This check is good practice, though less critical now that we pre-filter
            if img_base64:
                card_html = f"""
                <div class="floating-card" style="left: {pos['left']}%; top: {pos['top']}%; animation-delay: {pos['delay']}s;">
                    <img src="data:image/png;base64,{img_base64}" alt="Recent Creation"/>
                </div>
                """

            # <h4>🎨 {item['filename']}</h4>
                    # <p style="font-style: italic; color: rgba(255,255,255,0.8);">"{display_prompt}"</p>
                st.markdown(card_html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    # This message is now shown only if there are truly no valid images to display at all.
    st.markdown('<div class="recent-creations">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">✨ Recent Creations</h2>', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align: center; padding: 60px; color: rgba(255,255,255,0.6);">
            <h3>🎨 No creations yet</h3>
            <p>Start creating to see your masterpieces here!</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- Full Gallery Section ---
st.markdown('<div class="gallery-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-title">🖼️ Complete Gallery</h2>', unsafe_allow_html=True)

# <<< CORRECTION >>>: Use the pre-filtered `valid_gallery_data` list.
if valid_gallery_data:
    st.markdown("### 🎨 Generated Artworks")
    cols = st.columns(3)
    
    for idx, item in enumerate(valid_gallery_data):
        with cols[idx % 3]:
            # <<< CORRECTION >>>: Changed use_column_width to use_container_width to fix the warning.
            st.image(item['image_path'], caption=f"🎨 {item['filename']}", use_container_width=True)
            
            prompt_text = (item['original_prompt'][:100] + '...') if len(item['original_prompt']) > 100 else item['original_prompt']
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 10px; margin: 5px 0 15px 0; border-left: 3px solid #667eea;">
                    <strong>💭 Prompt:</strong><br>
                    <em style="color: rgba(255,255,255,0.9); font-size: 14px;">"{prompt_text}"</em>
                </div>
            """, unsafe_allow_html=True)
            
            try:
                with open(item['image_path'], "rb") as f:
                    st.download_button("💾 Download", f.read(), item['filename'], "image/png", key=f"img_download_{idx}")
            except Exception as e:
                st.caption(f"⚠️ Download unavailable: {e}")
else:
    st.markdown("""
        <div style="text-align: center; padding: 60px; color: rgba(255,255,255,0.6);">
            <h3>📁 Gallery is empty</h3>
            <p>Create your first masterpiece to populate the gallery!</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# --- Footer ---
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🔄 Refresh Gallery", key="refresh_btn"):
        st.rerun()

st.markdown("""
    <div style="text-align: center; padding: 40px; color: rgba(255,255,255,0.5); border-top: 1px solid rgba(255,255,255,0.1); margin-top: 60px;">
        <p>✨ Creative AI Partner - Where imagination meets technology</p>
    </div>
""", unsafe_allow_html=True)