EPR & Plastic Packaging Assistant
A small AI assistant that explains plastic packaging and EPR (Extended Producer Responsibility) rules in simple language. It finds the most relevant rule clauses for a question and shows them as sources. Optionally, IBM Granite can turn those clauses into a plain-language answer.

Built for the 1M1B AI for Sustainability Virtual Internship (with IBM SkillsBuild and AICTE). Primary SDG: SDG 12 - Responsible Consumption and Production

Problem
How might we use AI to make plastic packaging and EPR rules easy to understand, so that small brands and packaging teams can comply and reduce plastic waste?

How it works (RAG)
Rules text (rules.txt) is split into clauses.
A question is matched to the most relevant clauses (TF-IDF retrieval).
The matched clauses are shown as sources.
Optional: IBM Granite answers using only those clauses and cites them.
Run it
pip install -r requirements.txt
streamlit run app.py
Put your rules text in rules.txt, with a blank line between clauses (or upload a .txt in the sidebar).
Without an API key the app runs in retrieval-only mode (shows matching clauses).
To enable Granite answers, set an HF_TOKEN (Hugging Face) or watsonx.ai credentials as environment variables. Never commit keys to GitHub.
Responsible AI
Fairness: uses only the rule text provided.
Transparency: every answer shows its source clauses.
Ethics: says "I could not find this in the provided rules" instead of guessing. Not legal advice.
Privacy: no personal data is collected or stored.
Files
app.py - Streamlit app
rules.txt - rules text used for retrieval
requirements.txt - Python packages


