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



