"""
EPR & Plastic Packaging Assistant  (SDG 12: Responsible Consumption & Production)
A small RAG demo: retrieves the most relevant rule clauses, then asks IBM Granite
to answer ONLY from them and cite the source.

SETUP
  pip install streamlit scikit-learn huggingface_hub
  (optional, for watsonx.ai)  pip install ibm-watsonx-ai

RUN
  1. Put your rules text in a file called rules.txt (same folder). Separate clauses
     with a blank line. Example of one clause:
         Rule 4(a) - Producers must register on the CPCB EPR portal ...
  2. Set your key (Windows PowerShell):   $env:HF_TOKEN="hf_xxx"
     (Mac/Linux):                         export HF_TOKEN=hf_xxx
  3. streamlit run app.py

No key? The app still works in "retrieval-only" mode (shows matched clauses).
"""
import os
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------- CONFIG ----------
HF_MODEL = "ibm-granite/granite-3.3-8b-instruct"   # change if this model isn't available to you
WATSONX_MODEL = "ibm/granite-3-8b-instruct"
TOP_K = 3

SYSTEM_PROMPT = (
    "You are an assistant that explains plastic packaging and EPR (Extended Producer "
    "Responsibility) rules in simple language. Answer ONLY using the context clauses "
    "provided. Cite the clause label (e.g. [Clause 2]) for every point. If the answer "
    "is not in the context, say: 'I could not find this in the provided rules.' "
    "This is general information, not legal advice."
)


# ---------- LOAD & CHUNK ----------
def load_chunks(text: str, max_len: int = 900):
    """Split on blank lines; merge tiny pieces; cap length."""
    parts = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, buf = [], ""
    for p in parts:
        if len(buf) + len(p) < max_len:
            buf = (buf + "\n" + p).strip()
        else:
            if buf:
                chunks.append(buf)
            buf = p
    if buf:
        chunks.append(buf)
    return chunks


@st.cache_resource
def build_index(chunks_tuple):
    chunks = list(chunks_tuple)
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vec.fit_transform(chunks)
    return vec, matrix


def retrieve(query, chunks, vec, matrix, k=TOP_K):
    q = vec.transform([query])
    scores = cosine_similarity(q, matrix).ravel()
    idx = scores.argsort()[::-1][:k]
    return [(i, float(scores[i]), chunks[i]) for i in idx if scores[i] > 0]


# ---------- GRANITE CALLS ----------
def ask_granite(question, hits, provider):
    context = "\n\n".join(f"[Clause {i + 1}] {txt}" for i, _, txt in hits)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    if provider == "Hugging Face":
        from huggingface_hub import InferenceClient
        client = InferenceClient(model=HF_MODEL, token=os.getenv("HF_TOKEN"))
        out = client.chat_completion(messages=messages, max_tokens=500, temperature=0.1)
        return out.choices[0].message.content
    else:  # watsonx.ai
        from ibm_watsonx_ai import Credentials
        from ibm_watsonx_ai.foundation_models import ModelInference
        model = ModelInference(
            model_id=WATSONX_MODEL,
            credentials=Credentials(
                url=os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com"),
                api_key=os.getenv("WATSONX_API_KEY"),
            ),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )
        resp = model.chat(messages=messages)
        return resp["choices"][0]["message"]["content"]


# ---------- UI ----------
st.set_page_config(page_title="EPR Plastic Packaging Assistant", page_icon="♻️")
st.title("♻️ EPR & Plastic Packaging Assistant")
st.caption("SDG 12 · RAG + IBM Granite · Answers come only from the rules you load.")

with st.sidebar:
    st.header("Settings")
    provider = st.radio("Granite via", ["Hugging Face", "watsonx.ai"])
    uploaded = st.file_uploader("Upload rules (.txt)", type=["txt"])
    st.markdown("**Responsible AI**\n- Answers cite source clauses\n- Says 'not found' instead of guessing\n- No personal data used\n- Not legal advice")

if uploaded:
    raw = uploaded.read().decode("utf-8", errors="ignore")
elif os.path.exists("rules.txt"):
    raw = open("rules.txt", encoding="utf-8").read()
else:
    raw = ""

if not raw.strip():
    st.warning("Add a rules.txt file next to app.py (or upload one in the sidebar) to begin.")
    st.stop()

chunks = load_chunks(raw)
vec, matrix = build_index(tuple(chunks))
st.success(f"Loaded {len(chunks)} rule sections.")

examples = [
    "Which producers need to register for EPR?",
    "What are the recycling targets?",
    "What applies to multilayer plastic packaging?",
]
choice = st.selectbox("Try an example (or type your own below)", [""] + examples)
question = st.text_input("Your question", value=choice)

if st.button("Ask") and question.strip():
    hits = retrieve(question, chunks, vec, matrix)
    if not hits:
        st.info("I could not find this in the provided rules.")
    else:
        has_key = bool(os.getenv("HF_TOKEN") or os.getenv("WATSONX_API_KEY"))
        if has_key:
            with st.spinner("Asking Granite..."):
                try:
                    st.subheader("Answer")
                    st.write(ask_granite(question, hits, provider))
                except Exception as e:
                    st.error(f"Granite call failed: {e}")
        else:
            st.info("No API key found - showing retrieval-only mode.")
        st.subheader("Sources used")
        for i, score, txt in hits:
            with st.expander(f"Clause {i + 1}  (match score {score:.2f})", expanded=True):
                st.write(txt)
    st.caption("General information only, not legal advice.")
