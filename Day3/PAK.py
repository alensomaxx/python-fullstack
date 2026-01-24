#streamlit run vakquiz.py
import streamlit as st

st.set_page_config(page_title="VAK Learning Style Quiz", layout="centered")

st.title("🧠 VAK Learning Style Quiz")
st.write("Discover whether you are a **Visual, Auditory, or Kinesthetic learner**")

# 30 VAK Questions
questions = [
    "When learning something new, you prefer to:",
    "You remember information best when you:",
    "In a classroom, you learn better when the teacher:",
    "When giving directions, you prefer:",
    "You study best by:",
    "You understand instructions better when they are:",
    "When solving a problem, you:",
    "You prefer books that:",
    "You recall people by:",
    "During free time, you enjoy:",
    "You learn a new skill by:",
    "You prefer presentations that:",
    "You remember phone numbers by:",
    "In group work, you:",
    "You understand concepts better through:",
    "You feel distracted when:",
    "You prefer learning environments that are:",
    "You like explanations that:",
    "When assembling something, you:",
    "You prefer teachers who:",
    "You revise notes by:",
    "You grasp ideas faster when:",
    "You enjoy activities that involve:",
    "You prefer instructions that:",
    "You learn best when:",
    "You remember events by:",
    "You enjoy classes that:",
    "You understand topics when:",
    "You prefer feedback that:",
    "You learn efficiently by:"
]

options = [
    ("Looking at diagrams or charts", "Listening to explanations", "Doing hands-on activities"),
    ("Visualizing it", "Hearing it", "Practicing it"),
    ("Uses slides and diagrams", "Explains verbally", "Uses activities"),
    ("Maps or written steps", "Spoken instructions", "Following physically"),
    ("Reading notes", "Listening to audio", "Practicing"),
    ("Written or visual", "Spoken", "Demonstrated"),
    ("Visualize the solution", "Talk it through", "Try it out"),
    ("Have images", "Have audio versions", "Include exercises"),
    ("Their face", "Their voice", "Their actions"),
    ("Watching videos", "Listening to music", "Physical activities"),
    ("Watching a demo", "Listening to instructions", "Trying it yourself"),
    ("Have visuals", "Have explanations", "Have demonstrations"),
    ("Seeing them written", "Repeating them aloud", "Dialing them"),
    ("Draw diagrams", "Explain ideas", "Build or act"),
    ("Diagrams", "Lectures", "Practice"),
    ("Visual clutter", "Noise", "Sitting still"),
    ("Well-organized visually", "Quiet", "Interactive"),
    ("Use charts", "Use words", "Use examples"),
    ("Follow diagrams", "Listen to instructions", "Experiment"),
    ("Show examples", "Explain concepts", "Involve activities"),
    ("Rewriting them", "Reading aloud", "Using movements"),
    ("You see it", "You hear it", "You do it"),
    ("Movement", "Sounds", "Touch"),
    ("Are written", "Are spoken", "Are shown"),
    ("You are involved", "You listen", "You observe"),
    ("Images", "Sounds", "Actions"),
    ("Include visuals", "Include discussions", "Include activities"),
    ("You can try it", "You hear it explained", "You see it demonstrated"),
    ("Written comments", "Verbal feedback", "Practical correction"),
    ("Seeing", "Hearing", "Doing")
]

scores = {"Visual": 0, "Auditory": 0, "Kinesthetic": 0}

st.subheader("📋 Answer all questions")

responses = []

for i, question in enumerate(questions):
    response = st.radio(
        f"{i+1}. {question}",
        options[i],
        key=i,index=None
    )
    responses.append(response)

if st.button("✅ Submit Quiz"):
    for i, response in enumerate(responses):
        if response == options[i][0]:
            scores["Visual"] += 1
        elif response == options[i][1]:
            scores["Auditory"] += 1
        else:
            scores["Kinesthetic"] += 1

    total = sum(scores.values())

    st.subheader("📊 Your Learning Style Result")

    for style in scores:
        percentage = (scores[style] / total) * 100
        st.write(f"**{style}**: {percentage:.2f}%")

    dominant = max(scores, key=scores.get)
    st.success(f"🎯 Your dominant learning style is **{dominant}**")