import streamlit as st
import pandas as pd
import time
import random
from PIL import Image, ImageDraw, ImageFont
import io
from PIL import ImageFilter
import datetime

# 1. Page Configuration
st.set_page_config(
    page_title="VAK Learning Style Quiz",
    page_icon="🧠",
    layout="centered"
)

# 2. Custom CSS
st.markdown("""
    <style>
    .stRadio > label {
        font-weight: bold;
        font-size: 16px;
    }
    div[data-testid="stMarkdownContainer"] > p {
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTION: GENERATE PNG REPORT ---

def create_report_image(name, dominant, scores, total):
    # --- 1. SETTINGS ---
    width, height = 800, 600
    bg_color = (245, 245, 247)       # Apple light grey
    card_color = (255, 255, 255)     # Pure white
    text_main = (0, 0, 0)            # Pure Black
    text_sub = (134, 134, 139)       # Grey
    
    colors = {
        "Visual": (0, 122, 255),       # Blue
        "Auditory": (52, 199, 89),     # Green
        "Kinesthetic": (255, 149, 0)   # Orange
    }
    dominant_color = colors.get(dominant, text_main)

    # --- 2. FONTS ---
    # We load fonts slightly larger for the avatar
    try:
        font_avatar = ImageFont.truetype("arialbd.ttf", 35)
        font_super = ImageFont.truetype("arialbd.ttf", 45) 
        font_title = ImageFont.truetype("arialbd.ttf", 28)
        font_label = ImageFont.truetype("arialbd.ttf", 18)     
        font_pct = ImageFont.truetype("arial.ttf", 18)   
        font_small = ImageFont.truetype("arial.ttf", 14)   
    except IOError:
        font_avatar = ImageFont.load_default()
        font_super = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_pct = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # --- 3. CREATE BASE & SHADOW ---
    # We create a larger canvas to hold the blur
    base = Image.new('RGB', (width, height), bg_color)
    
    # Create a separate layer for shadow
    shadow_layer = Image.new('RGBA', (width, height), (0,0,0,0))
    s_draw = ImageDraw.Draw(shadow_layer)
    
    # Card Geometry
    cx1, cy1 = 100, 60
    w, h = 600, 480
    cx2, cy2 = cx1 + w, cy1 + h
    radius = 20

    # Draw Black Rectangle on Shadow Layer
    s_draw.rounded_rectangle([cx1+5, cy1+10, cx2+5, cy2+10], radius=radius, fill=(0,0,0,30))
    
    # Blur the shadow layer
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(15))
    
    # Paste shadow onto base
    base.paste(shadow_layer, (0,0), mask=shadow_layer)

    # --- 4. DRAW MAIN CARD ---
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([cx1, cy1, cx2, cy2], radius=radius, fill=card_color)
    
    # --- 5. DRAW AVATAR (Initials Circle) ---
    # Extract initials
    initials = "".join([n[0] for n in name.split()[:2]]).upper()
    
    avatar_size = 70
    ax, ay = cx1 + 40, cy1 + 40
    
    # Draw Circle
    d.ellipse([ax, ay, ax+avatar_size, ay+avatar_size], fill=(230, 230, 235))
    
    # Center Initials using textbbox (newer PIL) or approximate centering
    try:
        # Calculate text width/height to center it
        bbox = d.textbbox((0, 0), initials, font=font_avatar)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        d.text((ax + (avatar_size - text_w)/2, ay + (avatar_size - text_h)/2 - 5), initials, fill=text_sub, font=font_avatar)
    except:
        # Fallback for older PIL
        d.text((ax + 20, ay + 15), initials, fill=text_sub, font=font_avatar)

    # --- 6. TEXT CONTENT ---
    # Name (Next to Avatar)
    name_x = ax + avatar_size + 20
    d.text((name_x, cy1 + 45), "Learning Profile", fill=text_sub, font=font_small)
    d.text((name_x, cy1 + 65), name, fill=text_main, font=font_super)
    
    # Date (Top Right)
    date_str = datetime.date.today().strftime("%b %d, %Y")
    d.text((cx2 - 120, cy1 + 50), date_str, fill=(180,180,180), font=font_small)

    # Divider
    line_y = cy1 + 140
    d.line([(cx1 + 40, line_y), (cx2 - 40, line_y)], fill=(240, 240, 240), width=1)

    # Dominant Style Section
    d.text((cx1 + 40, line_y + 30), "Your Dominant Style", fill=text_sub, font=font_small)
    d.text((cx1 + 40, line_y + 55), dominant.title(), fill=dominant_color, font=font_title)

    # --- 7. PROGRESS BARS (Aligned) ---
    def draw_row(y, label, score, color):
        # Calculate width
        pct = score / total
        bar_max_w = 350
        bar_w = int(bar_max_w * pct)
        
        # Label (Left)
        d.text((cx1 + 40, y), label, fill=text_main, font=font_label)
        
        # Bar Background (Pill)
        bx = cx1 + 160
        by = y + 2
        bh = 14
        d.rounded_rectangle([bx, by, bx + bar_max_w, by + bh], radius=7, fill=(240, 240, 245))
        
        # Bar Fill
        if bar_w > 0:
             d.rounded_rectangle([bx, by, bx + bar_w, by + bh], radius=7, fill=color)
        
        # Percentage (Right Aligned to Card Edge)
        pct_text = f"{int(pct*100)}%"
        # Align to right margin (cx2 - 40)
        d.text((cx2 - 80, y), pct_text, fill=text_sub, font=font_pct)

    start_y = line_y + 120
    gap = 50
    
    draw_row(start_y, "Visual", scores['Visual'], colors['Visual'])
    draw_row(start_y + gap, "Auditory", scores['Auditory'], colors['Auditory'])
    draw_row(start_y + gap*2, "Kinesthetic", scores['Kinesthetic'], colors['Kinesthetic'])

    # --- 8. FOOTER ---
    d.text((cx1 + 40, cy2 - 40), "Generated via VAK Quiz by alenso", fill=(200, 200, 200), font=font_small)

    # Save
    buf = io.BytesIO()
    base.save(buf, format="PNG")
    return buf.getvalue()

# --- DATA PREPARATION ---
raw_quiz_data = [
    {"q": "When learning something new, you prefer to:", "opts": [("Looking at diagrams or charts", "Visual"), ("Listening to explanations", "Auditory"), ("Doing hands-on activities", "Kinesthetic")]},
    {"q": "You remember information best when you:", "opts": [("Visualizing it", "Visual"), ("Hearing it", "Auditory"), ("Practicing it", "Kinesthetic")]},
    {"q": "In a classroom, you learn better when the teacher:", "opts": [("Uses slides and diagrams", "Visual"), ("Explains verbally", "Auditory"), ("Uses activities", "Kinesthetic")]},
    {"q": "When giving directions, you prefer:", "opts": [("Maps or written steps", "Visual"), ("Spoken instructions", "Auditory"), ("Following physically", "Kinesthetic")]},
    {"q": "You study best by:", "opts": [("Reading notes", "Visual"), ("Listening to audio", "Auditory"), ("Practicing", "Kinesthetic")]},
    {"q": "You understand instructions better when they are:", "opts": [("Written or visual", "Visual"), ("Spoken", "Auditory"), ("Demonstrated", "Kinesthetic")]},
    {"q": "When solving a problem, you:", "opts": [("Visualize the solution", "Visual"), ("Talk it through", "Auditory"), ("Try it out", "Kinesthetic")]},
    {"q": "You prefer books that:", "opts": [("Have images", "Visual"), ("Have audio versions", "Auditory"), ("Include exercises", "Kinesthetic")]},
    {"q": "You recall people by:", "opts": [("Their face", "Visual"), ("Their voice", "Auditory"), ("Their actions", "Kinesthetic")]},
    {"q": "During free time, you enjoy:", "opts": [("Watching videos", "Visual"), ("Listening to music", "Auditory"), ("Physical activities", "Kinesthetic")]},
    {"q": "You learn a new skill by:", "opts": [("Watching a demo", "Visual"), ("Listening to instructions", "Auditory"), ("Trying it yourself", "Kinesthetic")]},
    {"q": "You prefer presentations that:", "opts": [("Have visuals", "Visual"), ("Have explanations", "Auditory"), ("Have demonstrations", "Kinesthetic")]},
    {"q": "You remember phone numbers by:", "opts": [("Seeing them written", "Visual"), ("Repeating them aloud", "Auditory"), ("Dialing them", "Kinesthetic")]},
    {"q": "In group work, you:", "opts": [("Draw diagrams", "Visual"), ("Explain ideas", "Auditory"), ("Build or act", "Kinesthetic")]},
    {"q": "You understand concepts better through:", "opts": [("Diagrams", "Visual"), ("Lectures", "Auditory"), ("Practice", "Kinesthetic")]},
    {"q": "You feel distracted when:", "opts": [("Visual clutter", "Visual"), ("Noise", "Auditory"), ("Sitting still", "Kinesthetic")]},
    {"q": "You prefer learning environments that are:", "opts": [("Well-organized visually", "Visual"), ("Quiet", "Auditory"), ("Interactive", "Kinesthetic")]},
    {"q": "You like explanations that:", "opts": [("Use charts", "Visual"), ("Use words", "Auditory"), ("Use examples", "Kinesthetic")]},
    {"q": "When assembling something, you:", "opts": [("Follow diagrams", "Visual"), ("Listen to instructions", "Auditory"), ("Experiment", "Kinesthetic")]},
    {"q": "You prefer teachers who:", "opts": [("Show examples", "Visual"), ("Explain concepts", "Auditory"), ("Involve activities", "Kinesthetic")]},
    {"q": "You revise notes by:", "opts": [("Rewriting them", "Visual"), ("Reading aloud", "Auditory"), ("Using movements", "Kinesthetic")]},
    {"q": "You grasp ideas faster when:", "opts": [("You see it", "Visual"), ("You hear it", "Auditory"), ("You do it", "Kinesthetic")]},
    {"q": "You enjoy activities that involve:", "opts": [("Movement", "Visual"), ("Sounds", "Auditory"), ("Touch", "Kinesthetic")]},
    {"q": "You prefer instructions that:", "opts": [("Are written", "Visual"), ("Are spoken", "Auditory"), ("Are shown", "Kinesthetic")]},
    {"q": "You learn best when:", "opts": [("You observe", "Visual"), ("You listen", "Auditory"), ("You are involved", "Kinesthetic")]},
    {"q": "You remember events by:", "opts": [("Images", "Visual"), ("Sounds", "Auditory"), ("Actions", "Kinesthetic")]},
    {"q": "You enjoy classes that:", "opts": [("Include visuals", "Visual"), ("Include discussions", "Auditory"), ("Include activities", "Kinesthetic")]},
    {"q": "You understand topics when:", "opts": [("You see it demonstrated", "Visual"), ("You hear it explained", "Auditory"), ("You can try it", "Kinesthetic")]},
    {"q": "You prefer feedback that:", "opts": [("Written comments", "Visual"), ("Verbal feedback", "Auditory"), ("Practical correction", "Kinesthetic")]},
    {"q": "You learn efficiently by:", "opts": [("Seeing", "Visual"), ("Hearing", "Auditory"), ("Doing", "Kinesthetic")]}
]

# 3. Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'intro'
    
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Guest"

if 'shuffled_quiz' not in st.session_state:
    random.shuffle(raw_quiz_data)
    for item in raw_quiz_data:
        random.shuffle(item['opts'])
    st.session_state.shuffled_quiz = raw_quiz_data

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {} 

# --- PAGE 1: INTRO & NAME INPUT ---
if st.session_state.page == 'intro':
    st.title("🧠 VAK Learning Style Quiz")
    st.markdown("### Discover your unique learning DNA")
    st.image("https://cdn-icons-png.flaticon.com/512/3069/3069172.png", width=150) # Optional illustrative icon
    st.info("Answer 30 questions to reveal if you are a **Visual**, **Auditory**, or **Kinesthetic** learner.")
    
    name_input = st.text_input("📝 Enter your Name to start:", placeholder="e.g. John Doe")
    
    if st.button("Start Quiz"):
        if name_input.strip():
            st.session_state.user_name = name_input
            st.session_state.page = 'quiz'
            st.rerun()
        else:
            st.warning("Please enter your name to proceed!")

# --- PAGE 2: THE QUIZ ---
elif st.session_state.page == 'quiz':
    st.title(f"👋 Hi, {st.session_state.user_name}!")
    st.markdown("Select the option that fits you best.")

    with st.form("quiz_form"):
        for i, item in enumerate(st.session_state.shuffled_quiz):
            st.write(f"**{i+1}. {item['q']}**")
            option_texts = [opt[0] for opt in item['opts']]
            
            st.radio(
                label="Select one:",
                options=option_texts,
                key=f"q{i}",
                index=None,
                label_visibility="collapsed"
            )
            st.markdown("---")

        submitted = st.form_submit_button("🚀 Submit & Get Report", type="primary")

        if submitted:
            complete = True
            temp_answers = []
            
            for i, item in enumerate(st.session_state.shuffled_quiz):
                key = f"q{i}"
                user_choice_text = st.session_state.get(key)
                
                if user_choice_text is None:
                    complete = False
                    break
                
                chosen_tuple = next(opt for opt in item['opts'] if opt[0] == user_choice_text)
                temp_answers.append(chosen_tuple)

            if not complete:
                st.error("⚠️ Please answer all 30 questions to get an accurate result!")
            else:
                st.session_state.user_answers = temp_answers
                st.session_state.page = 'results'
                st.rerun()

# --- PAGE 3: THE RESULTS ---
elif st.session_state.page == 'results':
    
    # Calculation
    scores = {"Visual": 0, "Auditory": 0, "Kinesthetic": 0}
    for answer_tuple in st.session_state.user_answers:
        style = answer_tuple[1]
        scores[style] += 1

    total = sum(scores.values())
    dominant = max(scores, key=scores.get)
    
    # ---------------- UI DISPLAY ----------------
    st.balloons()
    st.title(f"📊 Result for {st.session_state.user_name}")
    st.success(f"**Dominant Style: {dominant} Learner**")
    
    col1, col2, col3 = st.columns(3)
    v_pct = (scores["Visual"] / total) * 100
    a_pct = (scores["Auditory"] / total) * 100
    k_pct = (scores["Kinesthetic"] / total) * 100

    col1.metric("👁️ Visual", f"{v_pct:.1f}%", f"{scores['Visual']} pts")
    col2.metric("👂 Auditory", f"{a_pct:.1f}%", f"{scores['Auditory']} pts")
    col3.metric("✋ Kinesthetic", f"{k_pct:.1f}%", f"{scores['Kinesthetic']} pts")

    st.subheader("Analysis Breakdown")
    chart_data = pd.DataFrame({
        "Style": ["Visual", "Auditory", "Kinesthetic"],
        "Score": [scores["Visual"], scores["Auditory"], scores["Kinesthetic"]]
    })
    st.bar_chart(chart_data, x="Style", y="Score", color="Style")

    # ---------------- GENERATE & DOWNLOAD PNG ----------------
    st.markdown("### 📥 Save Your Report")
    
    # Generate image bytes
    report_img_bytes = create_report_image(st.session_state.user_name, dominant, scores, total)
    
    st.download_button(
        label="Download Report Card (PNG)",
        data=report_img_bytes,
        file_name=f"{st.session_state.user_name}_VAK_Report.png",
        mime="image/png"
    )

# Detailed Insights
    st.subheader(f"💡 Tips for {dominant} Learners")
    
    if dominant == "Visual":
        st.info("""
        **How you learn best:**
        You need to **see** the material. Text-heavy pages can be boring; you prefer images, maps, and graphs.
        
        **🚀 Actionable Study Tips:**
        * **Color Code:** Use different colored pens for different topics.
        * **Visualize:** Close your eyes and try to "see" the page notes.
        * **Watch:** YouTube tutorials and video lectures are your best friend.
        """)
    elif dominant == "Auditory":
        st.info("""
        **How you learn best:**
        You need to **hear** the information. You might find yourself reading out loud to understand better.
        
        **🚀 Actionable Study Tips:**
        * **Record:** Record yourself reading key notes and listen to them while walking.
        * **Discuss:** Study with a friend and explain concepts to them.
        * **Rhyme:** Make up songs or rhymes to remember facts.
        """)
    else: # Kinesthetic
        st.info("""
        **How you learn best:**
        You need to **do** it. You likely tap your pen or move your leg while studying. You learn by trial and error.
        
        **🚀 Actionable Study Tips:**
        * **Move:** Walk around the room while reading.
        * **Build:** Use models, lego, or physical objects to represent concepts.
        * **Short Bursts:** Study in 25-minute blocks (Pomodoro) with active breaks.
        """)

    st.markdown("---")
    if st.button("🔄 Start Over"):
        st.session_state.page = 'intro'
        del st.session_state['shuffled_quiz']
        st.session_state.user_answers = []
        st.rerun()