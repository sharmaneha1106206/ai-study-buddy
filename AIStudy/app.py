import os

import time

import streamlit as st

from dotenv import load_dotenv

from google import genai



# =========================================================

# AI STUDY BUDDY — complete app with modern CSS + model fallback

# =========================================================



load_dotenv()



st.set_page_config(

    page_title="AI Study Buddy",

    page_icon="🎓",

    layout="wide",

    initial_sidebar_state="expanded",

)



# ----------------------------- CSS -----------------------------

st.markdown(

    """

    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');



    :root { --primary:#635bff; --ink:#172033; --muted:#667085; --line:#e7eaf2; }



    html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }

    .stApp {

        background: radial-gradient(circle at 8% 0%,rgba(99,91,255,.10),transparent 27rem),

                    radial-gradient(circle at 100% 12%,rgba(23,184,166,.08),transparent 25rem),

                    #f7f8fc;

        color:var(--ink);

    }

    .block-container { max-width:1250px; padding-top:1.8rem; padding-bottom:2.5rem; }

    h1,h2,h3 { font-family:'Manrope',sans-serif!important; letter-spacing:-.035em; color:var(--ink); }



    [data-testid="stSidebar"] { background:#11182b; border-right:1px solid rgba(255,255,255,.08); }

    [data-testid="stSidebar"] * { color:#eef1ff; }

    [data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.13); }

    [data-testid="stSidebar"] .stRadio label {

        background:rgba(255,255,255,.045); border:1px solid rgba(255,255,255,.08);

        padding:.68rem .78rem; border-radius:12px; margin-bottom:.35rem; transition:.2s ease;

    }

    [data-testid="stSidebar"] .stRadio label:hover {

        background:rgba(255,255,255,.10); border-color:rgba(164,159,255,.65);

    }



    .brand { display:flex; align-items:center; gap:12px; padding:.25rem 0 1.1rem; }

    .brand-icon {

        width:46px; height:46px; display:flex; align-items:center; justify-content:center;

        border-radius:15px; font-size:1.45rem;

        background:linear-gradient(135deg,#766cff,#4b8dff); box-shadow:0 8px 22px rgba(99,91,255,.32);

    }

    .brand-name { font-family:'Manrope',sans-serif; font-size:1.18rem; font-weight:800; letter-spacing:-.04em; }

    .brand-caption { font-size:.78rem; color:#aeb7d0; margin-top:2px; }



    .hero {

        padding:1.55rem 1.8rem; border-radius:24px; color:white;

        background:linear-gradient(120deg,#252b55 0%,#5148e5 58%,#6b8cff 100%);

        box-shadow:0 16px 40px rgba(64,67,155,.18); margin-bottom:1.35rem;

        position:relative; overflow:hidden;

    }

    .hero:after {

        content:""; position:absolute; width:230px; height:230px; right:-60px; top:-105px;

        border:1px solid rgba(255,255,255,.22); border-radius:50%;

        box-shadow:0 0 0 24px rgba(255,255,255,.04),0 0 0 50px rgba(255,255,255,.03);

        pointer-events:none;

    }

    .hero-kicker { text-transform:uppercase; letter-spacing:.14em; font-size:.72rem; font-weight:700; opacity:.82; margin-bottom:.55rem; }

    .hero h1 { color:white!important; font-size:clamp(1.8rem,3vw,2.55rem); line-height:1.15; margin:0 0 .6rem; }

    .hero p { color:rgba(255,255,255,.85); font-size:1rem; max-width:740px; margin:0; }



    .section-heading { font-family:'Manrope',sans-serif; font-size:1.25rem; font-weight:800; letter-spacing:-.03em; margin:1.2rem 0 .25rem; }

    .section-subtitle { color:var(--muted); margin-bottom:1rem; font-size:.92rem; }

    .feature-card {

        background:rgba(255,255,255,.9); border:1px solid var(--line); border-radius:18px;

        padding:1.15rem 1.2rem; min-height:128px; box-shadow:0 5px 18px rgba(20,30,70,.035);

    }

    .feature-icon { font-size:1.4rem; margin-bottom:.5rem; }

    .feature-title { font-weight:800; font-size:1rem; margin-bottom:.3rem; color:var(--ink); }

    .feature-copy { color:var(--muted); font-size:.88rem; line-height:1.5; }



    .stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"] { border-radius:12px!important; }

    .stTextArea textarea { background:#fff; border-color:#dfe3ee; line-height:1.6; }

    .stTextInput input:focus,.stTextArea textarea:focus { border-color:var(--primary)!important; box-shadow:0 0 0 3px rgba(99,91,255,.12)!important; }



    .stButton>button,.stFormSubmitButton>button {

        border:0; border-radius:12px; min-height:2.7rem; padding:.65rem 1.1rem;

        font-weight:700; color:white; background:linear-gradient(135deg,#635bff,#4e70f5);

        box-shadow:0 7px 16px rgba(99,91,255,.18); transition:transform .15s ease,box-shadow .15s ease;

    }

    .stButton>button:hover,.stFormSubmitButton>button:hover {

        color:white; transform:translateY(-1px); box-shadow:0 10px 22px rgba(99,91,255,.25);

    }

    [data-testid="stChatMessage"] {

        background:rgba(255,255,255,.92); border:1px solid var(--line);

        border-radius:16px; padding:.85rem 1rem; margin-bottom:.7rem;

    }

    [data-testid="stAlert"] { border-radius:14px; }

    .tip { background:#eef2ff; border:1px solid #dce2ff; color:#39417b; border-radius:14px; padding:.9rem 1rem; font-size:.9rem; margin-top:.8rem; }

    .footer { color:#8a91a5; font-size:.8rem; text-align:center; padding-top:2rem; }

    </style>

    """,

    unsafe_allow_html=True,

)



# ----------------------------- Gemini setup -----------------------------

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:

    st.error("GEMINI_API_KEY nahi mila. Project folder mein .env file check karein.")

    st.code("GEMINI_API_KEY=your_actual_api_key")

    st.stop()



client = genai.Client(api_key=API_KEY)



# Updated model candidates for optimal speed and reliability
MODEL_CANDIDATES = [

    "gemini-2.5-flash",

    "gemini-1.5-flash",

    "gemini-1.5-pro",

]





def _is_temporary_or_model_error(exc):

    msg = str(exc).lower()

    return any(term in msg for term in (

        "503", "unavailable", "429", "resource_exhausted",

        "404", "not found", "model", "high demand", "overloaded",

        "500", "internal", "deadline", "timeout",

    ))





def ask_ai(prompt):

    last_error = None



    for model_name in MODEL_CANDIDATES:

        for attempt in range(2):

            try:

                response = client.models.generate_content(

                    model=model_name,

                    contents=prompt,

                )

                text = getattr(response, "text", None)

                if text and text.strip():

                    return text

                last_error = RuntimeError(f"{model_name} returned an empty response.")

                break



            except Exception as exc:

                last_error = exc

                msg = str(exc).lower()



                if any(term in msg for term in ("401", "403", "api key", "permission denied", "unauthorized")):

                    raise



                temporary = any(term in msg for term in (

                    "503", "unavailable", "429", "resource_exhausted",

                    "high demand", "overloaded", "500", "internal",

                    "deadline", "timeout",

                ))

                if temporary and attempt == 0:

                    time.sleep(1.0)

                    continue



                break



    raise RuntimeError(

        "Configured Gemini models could not complete the request. "

        f"Last error: {last_error}"

    )





def show_hero(kicker, title, subtitle):

    st.html(

        f"""

        <div class="hero">

            <div class="hero-kicker">{kicker}</div>

            <h1>{title}</h1>

            <p>{subtitle}</p>

        </div>

        """,

    )





def run_ai_task(prompt):

    with st.spinner("AI answer prepare kar raha hai..."):

        try:

            st.markdown(ask_ai(prompt))

        except Exception as exc:

            st.error("AI se response nahi aa saka. Model busy, quota limit, ya API issue ho sakta hai.")

            st.caption(str(exc))





# ----------------------------- Sidebar -----------------------------

if "pending_page_nav" in st.session_state:

    st.session_state["page_nav"] = st.session_state.pop("pending_page_nav")



with st.sidebar:

    st.html(

        """

        <div class="brand">

            <div class="brand-icon">🎓</div>

            <div>

                <div class="brand-name">AI Study Buddy</div>

                <div class="brand-caption">Your personal learning space</div>

            </div>

        </div>

        """,

    )

    st.markdown("---")

    page = st.radio(

        "YOUR WORKSPACE",

        ["🏠 Home", "💬 AI Chatbot", "📝 Notes Summarizer", "🧠 Quiz Generator", "📅 Study Planner"],

        key="page_nav",

    )

    st.markdown("---")

    st.caption("Made for focused learning ✨")

    st.caption("Ask clearly, learn confidently.")





# ----------------------------- Home -----------------------------

if page == "🏠 Home":

    show_hero(

        "LEARN SMARTER · NOT HARDER",

        "Your study partner, powered by AI.",

        "Ask questions, simplify notes, practise with quizzes, and build a study plan—all in one place.",

    )

    st.html('<div class="section-heading">Your learning toolkit</div>')

    st.html('<div class="section-subtitle">Choose a tool from the sidebar to get started.</div>')



    columns = st.columns(2, gap="large")

    cards = [

        ("💬", "AI Chatbot", "Ask about study, coding, concepts, and general questions."),

        ("📝", "Notes Summarizer", "Turn notes into structured revision material."),

        ("🧠", "Quiz Generator", "Create practice questions with answers."),

        ("📅", "Study Planner", "Plan study time around your subjects and deadlines."),

    ]

    for col, (emoji, title, description) in zip(columns * 2, cards):

        with col:

            st.html(

                f'<div class="feature-card"><div class="feature-icon">{emoji}</div>'

                f'<div class="feature-title">{title}</div><div class="feature-copy">{description}</div></div>',

            )

            st.write("")

            target_pages = {

                "AI Chatbot": "💬 AI Chatbot",

                "Notes Summarizer": "📝 Notes Summarizer",

                "Quiz Generator": "🧠 Quiz Generator",

                "Study Planner": "📅 Study Planner",

            }

            if st.button(

                f"Open {title} →",

                key=f"open_{title.lower().replace(' ', '_')}",

                use_container_width=True,

            ):

                st.session_state["pending_page_nav"] = target_pages[title]

                st.rerun()



    st.html(

        '<div class="tip">💡 Official information, such as a university syllabus, should be checked against the university website or latest official PDF.</div>',

    )



# ----------------------------- Chatbot -----------------------------

elif page == "💬 AI Chatbot":

    show_hero(

        "ASK · UNDERSTAND · GROW",

        "AI Chatbot",

        "Ask questions across subjects and topics. Get explanations, examples, and step-by-step help.",

    )



    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []



    left, right = st.columns([5, 1])

    with left:

        st.markdown("### Your conversation")

    with right:

        if st.button("Clear chat", use_container_width=True):

            st.session_state.chat_history = []

            st.rerun()



    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])



    question = st.chat_input("Ask anything: coding, BCA, science, writing, or general knowledge...")

    if question:

        st.session_state.chat_history.append({"role": "user", "content": question})

        with st.chat_message("user"):

            st.markdown(question)



        recent = st.session_state.chat_history[-10:]

        history_text = "\n\n".join(

            f'{item["role"].upper()}: {item["content"]}'

            for item in recent

        )

        prompt = f"""

You are AI Study Buddy, a capable and helpful general-purpose AI assistant and tutor.

Answer the user's actual question, even if it is not related to BCA or studying.

Use the same language as the user (Hindi, Hinglish, or English).

Give a complete answer that directly addresses the question. Do not stop mid-sentence or leave unfinished Markdown.

Use headings, numbered steps, examples, tables, or code when useful.

For broad questions, cover the key aspects in an organized way; for simple questions, be concise.

If the user asks for complete code, provide complete code, not just a fragment.

For official or changing facts that you cannot verify, clearly state uncertainty instead of inventing details.



Conversation so far:

{history_text}



Now write the assistant's next answer:

"""

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    answer = ask_ai(prompt)

                    st.markdown(answer)

                    st.session_state.chat_history.append(

                        {"role": "assistant", "content": answer}

                    )

                except Exception as exc:

                    st.error("AI request fail hua. API key, model availability, internet, ya quota check karein.")

                    st.caption(str(exc))



# ----------------------------- Notes Summarizer -----------------------------

elif page == "📝 Notes Summarizer":

    show_hero(

        "LESS CLUTTER · MORE CLARITY",

        "Notes Summarizer",

        "Turn your study material into readable revision notes.",

    )

    notes = st.text_area(

        "Paste your notes here",

        height=260,

        placeholder="Paste class notes, textbook content, or study material...",

    )

    style = st.selectbox(

        "Summary style",

        ["Quick revision", "Detailed explanation", "Key points only", "Exam-ready notes"],

    )

    if st.button("✨ Summarize notes"):

        if not notes.strip():

            st.warning("Pehle notes paste karein.")

        else:

            prompt = f"""

Summarize the following study material.

Style: {style}

Use clear headings and bullets. Explain difficult terms in simple language.

For exam-ready notes, include key definitions and likely revision points.

Do not invent details not supported by the provided material. Keep important concepts.



STUDY MATERIAL:

{notes}

"""

            st.markdown("### Your summary")

            run_ai_task(prompt)



# ----------------------------- Quiz Generator -----------------------------

elif page == "🧠 Quiz Generator":

    show_hero(

        "PRACTISE · RECALL · IMPROVE",

        "Quiz Generator",

        "Generate practice questions to test your understanding and prepare for exams.",

    )

    topic = st.text_input("Topic", placeholder="e.g. Conditional statements in C language")

    difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Mixed"])

    number_of_questions = st.slider("Number of questions", 3, 15, 5)

    question_format = st.selectbox("Question format", ["Multiple-choice (MCQ)", "Short answer", "Mixed"])

    include_answers = st.checkbox("Include answers and explanations", value=True)



    if st.button("🧠 Generate quiz"):

        if not topic.strip():

            st.warning("Pehle topic enter karein.")

        else:

            answers_instruction = (

                "Include the correct answer and a brief explanation for each question."

                if include_answers else

                "Do not reveal answers unless needed to clarify the question."

            )

            prompt = f"""

Create a useful quiz for a student.

Topic: {topic}

Difficulty: {difficulty}

Number of questions: {number_of_questions}

Question format: {question_format}

{answers_instruction}



Number each question clearly. For MCQs, include four plausible options (A, B, C, D).

Keep questions accurate, varied, and focused on the requested topic.

"""

            st.markdown("### Your practice quiz")

            run_ai_task(prompt)



# ----------------------------- Study Planner -----------------------------

elif page == "📅 Study Planner":

    show_hero(

        "PLAN · FOCUS · FINISH",

        "Study Planner",

        "Create a practical timetable around your subjects, deadline, and available time.",

    )

    subjects = st.text_area(

        "Subjects and topics",

        height=140,

        placeholder="e.g. Python: functions, lists; DBMS: SQL, normalization; Maths: matrices",

    )

    days_available = st.number_input("Days available", min_value=1, max_value=180, value=7)

    study_hours = st.slider("Study hours per day", min_value=1, max_value=12, value=3)

    include_breaks = st.checkbox("Include breaks, revision, and practice", value=True)



    if st.button("📅 Create my study plan"):

        if not subjects.strip():

            st.warning("Pehle subjects ya topics enter karein.")

        else:

            prompt = f"""

Create a realistic study plan for a student.

Subjects/topics:

{subjects}

Days available: {days_available}

Study hours per day: {study_hours}

Include breaks, revision, and practice: {include_breaks}



Organize it day by day. Balance topics, include review and practice sessions, and do not exceed the daily study-hour limit. Use a readable table if useful, then add a few practical tips.

"""

            st.markdown("### Your study plan")

            run_ai_task(prompt)



st.markdown('<div class="footer">AI Study Buddy · Learn at your own pace ✦</div>', unsafe_allow_html=True)
