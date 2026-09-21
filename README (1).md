# ♻️ EPR & Plastic Packaging Assistant

**In short:** Ask a question about India's plastic packaging (EPR) rules and get the most relevant rule clauses back, with sources shown. Optionally, IBM Granite turns those clauses into a plain-language answer. Built for the 1M1B AI for Sustainability Virtual Internship (with IBM SkillsBuild and AICTE). SDG 12 (primary), SDG 11, SDG 14.

---

## The problem
Plastic packaging and Extended Producer Responsibility (EPR) rules sit in long, technical government documents. Small brands and packaging teams struggle to find the clause that applies to them, which leads to confusion and non-compliance.

**How might we use AI to make plastic packaging and EPR rules easy to understand, so that small brands and packaging teams can comply and reduce plastic waste?**

## SDG alignment
| SDG | Link to this project |
|---|---|
| **SDG 12** (primary) | Responsible consumption and production: better packaging compliance and less plastic waste |
| SDG 11 | Sustainable cities: better waste management |
| SDG 14 | Life below water: less plastic reaching waterways |

## Who it is for
- Small and mid-size FMCG brands
- Packaging and compliance teams
- Recyclers and waste processors

## How it works (RAG)
1. **Load:** the rules text in `rules.txt` (Plastic Waste Management Amendment Rules, 2022, Schedule II: EPR guidelines for plastic packaging) is split into clauses.
2. **Retrieve:** the user's question is matched to the most relevant clauses using TF-IDF similarity (scikit-learn).
3. **Show sources:** the matching clauses are displayed with match scores, so every result can be verified.
4. **Generate (optional):** with an API key, IBM Granite answers using only the retrieved clauses and cites them. If the answer is not in the rules, it says so.

```
Rules text -> clauses -> retrieve best matches -> IBM Granite -> answer + cited clauses
```

## Features
- Question box with example questions
- Source clauses shown with match scores
- Retrieval-only mode: works with no API key
- Optional Granite answers via Hugging Face or watsonx.ai
- Upload your own rules `.txt` in the sidebar
- SDG badges and Responsible AI notes built into the app

## Run it locally
```
pip install -r requirements.txt
streamlit run app.py
```
1. Keep `rules.txt` in the same folder as `app.py`. Clauses are separated by blank lines.
2. Open the local link shown in the terminal (usually http://localhost:8501).
3. Pick an example question or type your own, then click **Ask**.

**Enable Granite answers (optional):** set an environment variable before running. Never put keys in the code or upload them to GitHub.
- Hugging Face: `HF_TOKEN`
- watsonx.ai: `WATSONX_API_KEY` and `WATSONX_PROJECT_ID`

Model availability on free tiers can change. If the Granite call fails, change `HF_MODEL` at the top of `app.py` or use retrieval-only mode.

## Example questions
- Which entities must register on the centralized portal?
- What are the recycling targets?
- What applies to multilayer plastic packaging?

## Responsible AI
- **Fairness:** uses only the official rule text provided, with no assumptions beyond it.
- **Transparency:** every result shows the source clauses used.
- **Ethics:** says "I could not find this in the provided rules" instead of guessing. It is general information, **not legal advice**.
- **Privacy:** no personal data is collected or stored.

## Limitations
- Retrieval is keyword-based (TF-IDF), so questions work best when they use words from the rules.
- Covers only the rules text you load. It may not include the latest amendments.
- The rules text was copied from the Gazette PDF and reformatted for readability (wording unchanged). Check the official notification for anything important.

## Future scope
- Semantic search with embeddings for better matching
- More languages (Hindi and regional)
- State-specific rules and later amendments
- Upload a brand's packaging details to check obligations

## Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit app |
| `rules.txt` | Rules text used for retrieval |
| `requirements.txt` | Python packages |
| `README.md` | This file |

## Author
**Prerna** | BSc IT, Mumbai University | 1M1B AI for Sustainability Virtual Internship, Jul-Sep 2026
