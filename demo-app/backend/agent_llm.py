"""
Agent: parse natural language task request via OpenAI LLM (or fallback) and return structured data for ClickUp.
Uses OPENAI_API_KEY from env. If missing, uses rule-based fallback.
"""
import json
import os
import re
from typing import Any, Dict, Optional

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def _parse_with_openai(prompt: str) -> Optional[Dict[str, Any]]:
    """Call OpenAI to extract task name, due date, assignee, tags, etc. Returns dict or None."""
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY.strip().strip('"'))
        sys = (
            "You are a task extraction assistant. From the user's natural language task request, "
            "extract and return a JSON object with exactly these keys: "
            "task_name (string), due_date (string, e.g. 'Friday' or '2025-03-15' or empty string), "
            "assignee (string, name or empty), list_or_pod (string, e.g. 'Mango Pod' or empty), "
            "tags (array of strings, e.g. ['high-priority', 'script-review']), "
            "dependencies (string, brief description or empty). "
            "Reply with only the JSON object, no markdown or explanation."
        )
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": sys}, {"role": "user", "content": prompt[:2000]}],
            max_tokens=500,
        )
        text = (r.choices[0].message.content or "").strip()
        # Strip markdown code block if present
        if text.startswith("```"):
            text = re.sub(r"^```\w*\n?", "", text)
            text = re.sub(r"\n?```\s*$", "", text)
        return json.loads(text)
    except Exception:
        return None


def _parse_fallback(prompt: str) -> Dict[str, Any]:
    """Rule-based fallback when OpenAI is not available."""
    prompt = (prompt or "").strip()
    lines = [ln.strip() for ln in prompt.split("\n") if ln.strip()]
    task_name = lines[0][:255] if lines else "Task from demo"
    due_date = ""
    assignee = ""
    list_or_pod = ""
    tags: list = []
    text_lower = prompt.lower()
    # Simple due date extraction
    for m in re.finditer(r"due\s+(?:by\s+)?(\w+(?:\s+\d{1,2}(?:st|nd|rd|th)?)?(?:\s+\w+)?)", text_lower, re.I):
        due_date = m.group(1).strip()
        break
    if not due_date and re.search(r"\b(friday|monday|next week)\b", text_lower):
        due_date = re.search(r"\b(friday|monday|next week)\b", text_lower).group(1)
    # Assignee: "assign to X" or "assign Editor 1"
    m = re.search(r"assign(?:ee)?\s+(?:to\s+)?([^.,\n]+)", text_lower, re.I)
    if m:
        assignee = m.group(1).strip()
    # Tags: "tags Mango, Lemon" or "tag X" or "high-priority"
    m_tags = re.search(r"tags?\s+([^.\n]+?)(?:\s+due|\s+depends|\.|$)", text_lower, re.I)
    if m_tags:
        for part in re.split(r"[\s,;]+", m_tags.group(1).strip()):
            if part and part not in ("and", "or") and len(part) < 32:
                tags.append(part.strip().title())
    if "mango" in text_lower and "mango" not in [t.lower() for t in tags]:
        tags.append("Mango")
    if "lemon" in text_lower and "lemon" not in [t.lower() for t in tags]:
        tags.append("Lemon")
    if ("high-priority" in text_lower or "high priority" in text_lower) and "high-priority" not in tags:
        tags.append("high-priority")
    if "script" in text_lower and "script-review" not in tags:
        tags.append("script-review")
    # Dependencies: "depends on X" or "dependencies: X"
    deps = ""
    m_dep = re.search(r"(?:depends on|dependencies?)\s*[:\s]+([^.\n]+)", text_lower, re.I)
    if m_dep:
        deps = m_dep.group(1).strip()
    return {
        "task_name": task_name,
        "due_date": due_date,
        "assignee": assignee,
        "list_or_pod": list_or_pod,
        "tags": tags[:10],
        "dependencies": deps,
    }


def parse_task_prompt(prompt: str) -> Dict[str, Any]:
    """Parse user prompt into structured task data. Uses OpenAI if key set, else fallback."""
    parsed = _parse_with_openai(prompt)
    if isinstance(parsed, dict):
        return {
            "task_name": str(parsed.get("task_name", ""))[:255] or "Task from agent",
            "due_date": str(parsed.get("due_date", "")),
            "assignee": str(parsed.get("assignee", "")),
            "list_or_pod": str(parsed.get("list_or_pod", "")),
            "tags": [str(t) for t in (parsed.get("tags") or [])][:10],
            "dependencies": str(parsed.get("dependencies", "")),
        }
    return _parse_fallback(prompt)


def is_llm_configured() -> bool:
    return bool(OPENAI_API_KEY)
