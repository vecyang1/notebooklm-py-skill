# NotebookLM Master Interviewer Skill 🧠

An advanced Agent Skill for Google NotebookLM that goes beyond simple summaries. This tool implements the **Master Interviewer Protocol**, designed to extract the "underlying code" (底层逻辑) from sources while wearing the user's shoes.

## 🚀 Key Features

- **Strategic Proxy Interviewer**: Automatically acts on behalf of the user to navigate complex topics (investment, career, wealth mindset).
- **High-Concurrency Batch QA**: Optimized for **8-worker parallel execution** with built-in retry and self-healing logic.
- **Master Interviewer Protocol**:
  1. **Context Locking**: Introduction check.
  2. **Navigation Map**: Auto-generation of 50 high-value questions.
  3. **User-Perspective Outlining**: Synthesizing maps into surgical questions (e.g., tailored to specific income/goals).
  4. **Iterative Audit & Deep Dive**: Automatically identify and follow up on vague answers.

## 🛠️ Installation

```bash
# Clone the skill into your Agent Skill directory
git clone https://github.com/vecyang1/notebooklm-py-skill.git

# Initialize virtual environment
cd notebooklm-py-skill/repo
python3 -m venv .venv
source .venv/bin/activate
pip install notebooklm-py
```

## 📖 Usage

### 1. Initialize a Project
```bash
python3 scripts/init_project.py "My_Wealth_Research"
```

### 2. Run the Interview Loop
Follow the **Master Interviewer Protocol** outlined in `SKILL.md` to get deep, actionable insights.

## ⚖️ License
MIT
