from typing import Literal, List, Dict


Role = Literal["citizen", "doctor", "hospital_admin", "policy_maker"]


def _role_instructions(role: Role) -> str:
    if role == "citizen":
        return (
            "Explain in simple, non-technical language. Focus on eligibility, coverage, "
            "and how the person can practically use the scheme. Avoid medical jargon."
        )
    if role == "doctor":
        return (
            "Explain with moderate technical and clinical detail. Focus on package coverage, "
            "indications, exclusions, and documentation required from the hospital side."
        )
    if role == "hospital_admin":
        return (
            "Focus on empanelment, claims workflow, approvals, documentation, and audit-related "
            "requirements. Mention any ceilings, limits, and processes clearly."
        )
    if role == "policy_maker":
        return (
            "Explain with system-level perspective: objectives, implementation architecture, "
            "state/central roles, funding patterns, and key performance indicators."
        )
    return "Explain clearly and accurately based only on the provided policy context."


def build_rag_prompt(query: str, role: Role, docs: List[Dict]) -> str:
    """
    docs: list of dicts with keys: source, page_start, page_end, text
    """
    role_instr = _role_instructions(role)

    context_parts = []
    for i, d in enumerate(docs, start=1):
        context_parts.append(
            f"[DOC {i}] (source={d['source']}, pages={d['page_start']}-{d['page_end']}):\n{d['text']}"
        )
    context_block = "\n\n".join(context_parts) if context_parts else "No documents were retrieved."

    prompt = f"""
You are an expert assistant answering questions about India's Ayushman Bharat / PM-JAY and related health schemes.

User role: {role}
Role-specific instructions: {role_instr}

You are given the following context snippets from official policy documents:

{context_block}

User question:
{query}

Instructions:
- Answer ONLY using the policy context above. If the answer is not clearly present, say you are not sure.
- Cite relevant document numbers like [DOC 1], [DOC 2] in your answer.
- Be concise but complete.
- Do NOT invent policy details.
"""
    return prompt.strip()
