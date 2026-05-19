import streamlit as st
from google import genai
from google.genai import types

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Math& 172 AI Thinking Partner",
    page_icon="📐",
    layout="wide",
)

# ── Brand color injection ────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    :root { --brand: #1D9E75; }
    .stApp { font-family: 'Segoe UI', sans-serif; }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        margin-right: 4px;
        color: #fff;
    }
    .badge-tilt  { background: #1D9E75; }
    .badge-udl   { background: #2563EB; }
    .badge-oer   { background: #9333EA; }
    .tilt-label  { font-size: 0.78rem; font-weight: 700; color: #1D9E75;
                   text-transform: uppercase; letter-spacing: 0.05em; }
    .quote-box   { font-style: italic; font-size: 0.82rem; color: #555;
                   border-left: 3px solid #1D9E75; padding-left: 8px;
                   margin-top: 16px; }
    /* starter buttons */
    div[data-testid="stHorizontalBlock"] button {
        border: 1px solid #1D9E75 !important;
        color: #1D9E75 !important;
        background: #f0faf6 !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 52px !important;
        text-align: left !important;
        padding: 8px 10px !important;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        background: #d4f1e6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Topic data ───────────────────────────────────────────────────────────────
TOPICS = {
    "Tangrams": {
        "label": "Tangrams",
        "pages": "pp. 374–377",
        "oer_summary": (
            "Seven-piece puzzle from Song Dynasty China (~1100 AD). Students cut and "
            "rearrange all seven pieces with no overlaps or gaps to form target shapes. "
            "Builds spatial reasoning and shape classification."
        ),
        "tilt_purpose": (
            "Develop spatial reasoning by manipulating and reasoning about geometric pieces."
        ),
        "tilt_task": (
            "Use all seven tangram pieces to form target shapes, trace solutions, "
            "compare difficulty across puzzle types."
        ),
        "tilt_criteria": (
            "You can explain why pieces fit or don't fit using geometric language "
            "and compare difficulty with reasoning."
        ),
        "contextualizer_starters": [
            "Think about your own life or career — where do things have to fit together precisely with no gaps? How does that connect to tangrams?",
            "Tangrams come from China and have been used for centuries. What geometric puzzles or fitting-together designs exist in your own cultural background?",
            "If you were teaching this to a 3rd grader from your community, what real object would you compare the seven-piece fitting challenge to?",
            "Some tangram shapes were harder than others. What made a shape hard — was it math, or something else?",
        ],
        "reflection_starters": [
            "Describe the very first strategy you tried on a hard tangram puzzle. What were you thinking?",
            "At what moment did you realize that strategy wasn't working? What did you try next, and why?",
            "The book says you can never trust a drawing. Did a tangram drawing mislead you? Describe what happened.",
            "What would you tell a classmate who is stuck — not the solution, but the thinking approach?",
        ],
    },
    "Triangles & Quadrilaterals": {
        "label": "Triangles & Quadrilaterals",
        "pages": "pp. 378–395",
        "oer_summary": (
            "Classification by sides (scalene, isosceles, equilateral) and angles "
            "(acute, obtuse, right, equiangular). Angle sum = 180° discovered by tearing "
            "corners and placing vertices together. Tick marks as shared notation."
        ),
        "tilt_purpose": (
            "Understand triangle classification and why angle sum is always 180° "
            "through reasoning, not memorization."
        ),
        "tilt_task": (
            "Draw five different triangles, cut one out and tear the corners, "
            "place vertices together to discover angle sum."
        ),
        "tilt_criteria": (
            "You can classify any triangle and justify it; you can explain the 180° "
            "result using the physical activity."
        ),
        "contextualizer_starters": [
            "Bridges and roof trusses use triangles for structural strength. Why do you think that is, and how does the angle sum relate to stability?",
            "Think about your community, profession, or home. Where do you see triangles used intentionally? What kind are they?",
            "How would you convince a skeptical student without algebra that the angles of any triangle always add to 180°?",
            "Tick marks exist so mathematicians can communicate clearly across languages. Where else in your life does a shared symbol system matter?",
        ],
        "reflection_starters": [
            "When you drew your five different triangles, what features did you actually change each time?",
            "What surprised you when you tore the corners and placed the vertices together?",
            "Where in your reasoning today did you go on instinct and then have to check yourself?",
            "How does the angle sum idea connect to something you already knew before this chapter?",
        ],
    },
    "Polygons": {
        "label": "Polygons",
        "pages": "pp. 396–410",
        "oer_summary": (
            "Naming by side count, interior angle sums via triangulation, "
            "(n−2)×180° formula, regular vs. irregular, convex vs. concave, "
            "and Platonic solids. Formula derived through reasoning."
        ),
        "tilt_purpose": (
            "Derive the interior angle sum formula by triangulating polygons "
            "and reasoning about triangles."
        ),
        "tilt_task": (
            "Triangulate polygons of increasing sides, track the pattern, "
            "justify (n−2)×180°, explore which regular polygons tile a plane."
        ),
        "tilt_criteria": (
            "You can explain where (n−2) comes from visually and predict angle sums "
            "for any polygon without looking it up."
        ),
        "contextualizer_starters": [
            "A stop sign is a regular octagon. These shapes communicate meaning before drivers read the words. What does geometry have to do with that?",
            "Honeybees build hexagonal combs. Regular hexagons tile perfectly but regular pentagons do not. How does the angle sum explain this?",
            "Think about a career or community context you know. Where does someone need to reason about interior angles even if they don't call it geometry?",
            "The (n−2) in the formula comes from a visual idea, not algebra. Can you describe that visual idea in plain words?",
        ],
        "reflection_starters": [
            "How did you figure out the angle-sum pattern — did you spot it before you could explain it?",
            "Describe a moment today when a drawing seemed to give you the answer but you had to reason beyond it.",
            "What is the difference between knowing the formula and understanding why it works?",
            "How did today's polygon reasoning build on what you already knew about triangles?",
        ],
    },
    "Symmetry": {
        "label": "Symmetry",
        "pages": "pp. 411–420",
        "oer_summary": (
            "Line symmetry, rotational symmetry (center and angle of rotation), "
            "translational symmetry. Cultural examples: M.C. Escher, Hawaiian and "
            "Polynesian tattoo designs, Islamic tile work."
        ),
        "tilt_purpose": (
            "Distinguish three types of symmetry by reasoning about what stays the "
            "same under a transformation."
        ),
        "tilt_task": (
            "Identify symmetry types in figures, find center and angle of rotation, "
            "complete designs, create your own symmetric design."
        ),
        "tilt_criteria": (
            "You can determine symmetry type and justify it; you can specify angle "
            "and direction precisely."
        ),
        "contextualizer_starters": [
            "The book shows Polynesian tattoo designs as an example of translational symmetry. What does it mean to you that mathematical structure shows up in cultural art?",
            "Think about your own background or community. Is there a design, textile, or art form that uses symmetry? Which type, and how do you know?",
            "Rotational symmetry at 72° means the star looks identical after turning exactly 72°. How would you verify that it is exactly 72° and not just close?",
            "A designer deliberately breaks symmetry to create tension. Where have you seen intentional asymmetry? What was the effect?",
        ],
        "reflection_starters": [
            "How would you have defined symmetry before this section? How has your definition changed?",
            "Which type of symmetry — line, rotational, or translational — was hardest for you to see? What made it hard?",
            "When you created your own symmetric design, at what point did it feel like you were doing mathematics?",
            "How does verifying symmetry require reasoning rather than just looking?",
        ],
    },
    "Tessellations": {
        "label": "Tessellations",
        "pages": "pp. 421–430",
        "oer_summary": (
            "Any triangle or quadrilateral tessellates, proven via angle sums around "
            "a point. Regular hexagons tessellate; regular pentagons do not. Escher "
            "drawings made by modifying a tessellating tile."
        ),
        "tilt_purpose": (
            "Understand which shapes tessellate and why using angle-sum reasoning, "
            "then apply that understanding creatively."
        ),
        "tilt_task": (
            "Test tiles, prove why triangles and quads always tessellate using angle "
            "arguments, create an Escher-style drawing."
        ),
        "tilt_criteria": (
            "You can prove a shape tessellates using angle arguments; your Escher tile "
            "preserves the tessellation property."
        ),
        "contextualizer_starters": [
            "Islamic geometric art, Japanese komon, and Moroccan zellige tilework all use tessellations with deep cultural meaning. Choose one — what shapes does it use and what symmetry does it have?",
            "If you were designing the floor of a community space such as a school or cultural center, what tile shape would you choose and why?",
            "The proof that any triangle tessellates uses the 180° angle sum. Can you explain that proof in plain language to a curious 5th grader?",
            "When you modified a tile to make an Escher drawing, the math worked even though it looked like art. What does that tell you about creativity and mathematical structure?",
        ],
        "reflection_starters": [
            "What conjecture did you form while testing tiles before you had any proof?",
            "How did angle-sum reasoning give you more certainty than just testing many triangles?",
            "When you made your Escher-style drawing, were you doing mathematics? What is your evidence?",
            "Where did your intuition mislead you today, and how did you correct it?",
        ],
    },
    "Polyhedra": {
        "label": "Polyhedra",
        "pages": "pp. 430–450",
        "oer_summary": (
            "Platonic solids, Euler's formula V − E + F = 2, building towers with "
            "toothpicks. Structural rigidity: triangles are rigid, squares collapse. "
            "Exactly five Platonic solids due to geometric constraints."
        ),
        "tilt_purpose": (
            "Discover Euler's formula empirically, understand triangle rigidity, "
            "and reason about why exactly five Platonic solids exist."
        ),
        "tilt_task": (
            "Build toothpick structures, verify Euler's formula on multiple solids, "
            "argue why a sixth Platonic solid is impossible."
        ),
        "tilt_criteria": (
            "You can state and verify Euler's formula; you can explain triangle rigidity; "
            "you can argue why there is no sixth Platonic solid."
        ),
        "contextualizer_starters": [
            "A toothpick square collapses under pressure but a toothpick triangle does not. Where do you see this principle used in real structures in your community?",
            "Viruses, buckyballs, and dice all take polyhedral forms. Pick one — why does that shape make sense for that object?",
            "There are exactly five Platonic solids, known since ancient Greece. Why exactly five? What geometric constraint stops a sixth?",
            "Euler's formula V − E + F = 2 works for every convex polyhedron. After verifying it on a few solids, does it feel like a coincidence or a deep truth? What is the difference?",
        ],
        "reflection_starters": [
            "Describe your toothpick tower strategy. When did it fail, and what did that failure teach you?",
            "How did verifying Euler's formula on multiple solids feel different from being told it is true?",
            "What does it mean to prove something in geometry as opposed to just checking many examples?",
            "Which part of this section most surprised you, and why?",
        ],
    },
}

TOPIC_KEYS = list(TOPICS.keys())

# ── System prompt builder ────────────────────────────────────────────────────
def build_system_prompt(topic_key: str, mode: str) -> str:
    t = TOPICS[topic_key]
    mode_instruction = (
        "You are in CONTEXTUALIZER mode. Your role is to help the student bridge "
        "abstract geometric ideas to their own culture, community, lived experience, "
        "and career aspirations. Connect every geometric concept to something real "
        "and meaningful in their world."
        if mode == "Contextualizer"
        else
        "You are in PROCESS REFLECTION mode. Your role is to help the student "
        "articulate and examine their own thinking process metacognitively. Focus "
        "on HOW they reasoned, not on content answers. Ask about strategies, "
        "surprises, moments of confusion, and shifts in understanding."
    )
    return f"""You are an AI Thinking Partner for Math& 172 (Mathematics for Elementary Teachers) at a community college, aligned to the OER textbook "Mathematics for Elementary Teachers" by Michelle Manes.

CURRENT TOPIC: {t['label']} ({t['pages']})
TOPIC OVERVIEW: {t['oer_summary']}

TILT FRAMEWORK FOR THIS TOPIC:
- Purpose: {t['tilt_purpose']}
- Task: {t['tilt_task']}
- Criteria for Success: {t['tilt_criteria']}

YOUR GUIDING SPIRIT: "Geometry is the art of good reasoning from bad drawings." — Poincaré

CORE PEDAGOGY — SOCRATIC TUTOR:
- Never give the final answer. Always respond with a question or a sub-question.
- If the student is correct, affirm briefly (one sentence) then immediately push deeper with a follow-up question.
- If the student is confused or stuck, ask a simpler, more concrete question to scaffold understanding.
- Reference OER page numbers when useful (e.g., "Take another look at page 382...").
- Keep every response to 3–5 sentences maximum — one of which must be a question.
- Honor the student's cultural context and lived experience. When they share something personal, weave it into the geometric reasoning.
- Align with UDL principles: multiple means of engagement, representation, and expression.

MODE-SPECIFIC BEHAVIOR:
{mode_instruction}

Remember: your job is to develop the student's reasoning, not to demonstrate your own. Every response ends with a genuine question that moves their thinking forward."""


# ── Gemini call with model fallback ─────────────────────────────────────────
_MODELS = ["models/gemini-1.5-flash", "gemini-pro"]

def call_gemini(contents, system_prompt: str) -> str:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    last_err = None
    for model in _MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=512,
                ),
            )
            return response.text
        except Exception as e:
            last_err = e
    raise last_err


# ── Session state init ───────────────────────────────────────────────────────
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = TOPIC_KEYS[0]
if "mode" not in st.session_state:
    st.session_state.mode = "Contextualizer"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_starter" not in st.session_state:
    st.session_state.pending_starter = None


def on_topic_change():
    st.session_state.selected_topic = st.session_state._topic_radio
    st.session_state.messages = []
    st.session_state.pending_starter = None


def on_mode_change():
    st.session_state.mode = st.session_state._mode_radio


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📐 Math& 172\n**AI Thinking Partner**")
    st.divider()

    st.markdown("### Topic")
    st.radio(
        "Select a topic",
        TOPIC_KEYS,
        index=TOPIC_KEYS.index(st.session_state.selected_topic),
        key="_topic_radio",
        on_change=on_topic_change,
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Mode")
    st.radio(
        "Select a mode",
        ["Contextualizer", "Process Reflection"],
        index=["Contextualizer", "Process Reflection"].index(st.session_state.mode),
        key="_mode_radio",
        on_change=on_mode_change,
        label_visibility="collapsed",
    )
    st.markdown(
        "<small><b>Contextualizer</b> — connects geometry to your world.<br>"
        "<b>Process Reflection</b> — examines how you think.</small>",
        unsafe_allow_html=True,
    )

    st.divider()
    with st.expander("🔍 Available Gemini models"):
        try:
            _client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
            model_names = sorted(m.name for m in _client.models.list())
            st.code("\n".join(model_names), language=None)
        except Exception as _e:
            st.error(f"Could not fetch models: {_e}")

    st.divider()
    st.markdown(
        '<div class="quote-box">'
        '"Geometry is the art of good reasoning from bad drawings."'
        "<br>— Henri Poincaré"
        "</div>",
        unsafe_allow_html=True,
    )

topic_key = st.session_state.selected_topic
mode = st.session_state.mode
t = TOPICS[topic_key]

# ── Main area ────────────────────────────────────────────────────────────────
# Header row
col_title, col_badges = st.columns([3, 1])
with col_title:
    st.markdown(f"## {t['label']}")
    st.markdown(f"*{t['pages']} · Mathematics for Elementary Teachers, Manes*")
with col_badges:
    st.markdown(
        '<br><span class="badge badge-tilt">TILT</span>'
        '<span class="badge badge-udl">UDL</span>'
        '<span class="badge badge-oer">OER</span>',
        unsafe_allow_html=True,
    )

# TILT panel
with st.container(border=True):
    st.markdown(
        f"🎯 &nbsp; **PURPOSE** &nbsp; {t['tilt_purpose']}\n\n"
        f"📋 &nbsp; **TASK** &nbsp; {t['tilt_task']}\n\n"
        f"✅ &nbsp; **CRITERIA FOR SUCCESS** &nbsp; {t['tilt_criteria']}"
    )

st.divider()

# ── Starter prompt buttons ───────────────────────────────────────────────────
starters = (
    t["contextualizer_starters"]
    if mode == "Contextualizer"
    else t["reflection_starters"]
)

st.markdown(f"**✨ Starter prompts — {mode} mode**")
col_a, col_b = st.columns(2)
for i, prompt_text in enumerate(starters):
    target_col = col_a if i % 2 == 0 else col_b
    with target_col:
        if st.button(prompt_text, key=f"starter_{topic_key}_{mode}_{i}"):
            st.session_state.pending_starter = prompt_text

st.divider()

# ── Chat history display ─────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle pending starter (must run before chat_input to inject the message) ─
if st.session_state.pending_starter:
    user_text = st.session_state.pending_starter
    st.session_state.pending_starter = None
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        gemini_contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part(text=m["content"])],
            )
            for m in st.session_state.messages
        ]
        with st.spinner("Thinking…"):
            assistant_text = call_gemini(gemini_contents, build_system_prompt(topic_key, mode))
        st.markdown(assistant_text)
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})

# ── Chat input ───────────────────────────────────────────────────────────────
user_input = st.chat_input("Share your thinking…")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        gemini_contents = [
            types.Content(
                role="user" if m["role"] == "user" else "model",
                parts=[types.Part(text=m["content"])],
            )
            for m in st.session_state.messages
        ]
        with st.spinner("Thinking…"):
            assistant_text = call_gemini(gemini_contents, build_system_prompt(topic_key, mode))
        st.markdown(assistant_text)
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
