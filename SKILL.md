---
name: notebooklm-py
description: Advanced Python API and CLI for Google NotebookLM. Supports deep research, multi-format content generation (podcasts, videos, quizzes), and batch artifact downloading.
---

# NotebookLM-Py Skill (Unofficial)

> ⚠️ **Unofficial API**: Use responsibly.
> 🔗 **Source**: [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)

A powerful skill for interacting with Google NotebookLM programmatically. It goes beyond the web UI by offering batch operations, advanced exports (JSON/Markdown for quizzes), and automated research pipelines.

## 🚀 Usage

**Prerequisite**: You must be logged in. Run this once:

```bash
source internal-docs
notebooklm login
```

### 🧠 Research & Knowledge Management

**Create & Add Sources:**
```bash
# Create a new notebook
notebooklm create "My Research Topic"

# Add sources (URL, PDF, YouTube, Drive)
notebooklm source add "https://en.wikipedia.org/wiki/Artificial_intelligence"
notebooklm source add "./local_paper.pdf"
```

**Deep Research (Auto-Crawl):**
Use the built-in research agent to find and add relevant sources automatically.
```bash
# Research a topic and add to current notebook
notebooklm source add-research "The future of solid state batteries" --depth deep
```

### 💬 Chat with Sources

Query your notebook context directly from the terminal.
```bash
notebooklm ask "What are the key themes in these documents?"
```

### 🤖 Agentic Workflow & Proxy Interviews (Batch QA)

Use the built-in script to run parallel, automated interviews against a NotebookLM project.

```bash
# 1. Initialize a new QA workspace (creates questions.json & runner script)
python3 internal-docs --dir /path/to/workspace

# 2. Add questions to questions.json, then run the interview script inside the workspace:
# Recommended 8 workers for stability and speed on high-end Macs.
source repo/.venv/bin/activate
python3 scripts/auto_interview.py --notebook <notebook_id> --questions questions.json --output answers.md --workers 8
```

**💡 Agent Proxy Tip (The Master Interviewer Protocol):**
When acting on behalf of the user, follow this "Think-Act-Audit" loop:

1. **Phase 1: Context Locking**: Ask the notebook to **"介绍你自己"** to verify persona alignment.
2. **Phase 2: Navigation Mapping**: Ask for **"50 个关键问题"** to understand the total knowledge boundaries of the sources.
3. **Phase 3: Strategic Outlining**: 
   - DO NOT just pick questions. 
   - **Plan**: Synthesize the map + User Context (e.g., income, location, fears) into a **Deep Outline**. 
   - Refine questions to be more "surgical" (e.g., instead of "How to invest?", ask "Given my 1.5w income, how exactly do I split my first 1000 CNY between VOO and BTC?").
4. **Phase 4: Execution (Batch QA)**: Run the interview using 8 parallel workers.
5. **Phase 5: Audit & Deep Dive (Iterative)**:
   - **Review**: Read the generated `answers.md`.
   - **Identify Gaps**: Flag any vague, generic, or incomplete answers (e.g., "Go to a broker" is too vague; "Which specific broker supports fractional shares for China users?" is the deep dive).
   - **Supplement**: Run a secondary targeted QA for these gaps until the user has a production-ready manual.
6. **Stability**: Use **8 parallel workers** for optimal speed and reliability.


### 🎨 Content Generation

Generate various study aids and content formats.

**Audio & Video:**
```bash
# Generate Audio Overview (Podcast)
notebooklm generate audio "Focus on technical details" --wait

# Generate Video (requires previous audio)
notebooklm generate video --style whiteboard --wait
```

**Study Materials:**
```bash
# Generate Quiz (and export as structured data!)
notebooklm generate quiz --difficulty hard

# Generate Flashcards
notebooklm generate flashcards --quantity 20

# Generate Study Guide
notebooklm generate study-guide
```

**Visuals & Data:**
```bash
# Generate Mind Map
notebooklm generate mind-map

# Generate Infographic
notebooklm generate infographic --orientation portrait

# Generate Data Table
notebooklm generate data-table "Compare key specifications"
```

### 📥 Download & Export

Download generated artifacts to your local machine.

```bash
# Download specific artifacts
notebooklm download audio ./podcast.mp3
notebooklm download video ./overview.mp4
notebooklm download slide-deck ./slides.pdf

# Export structured data (Not available in Web UI)
notebooklm download quiz --format markdown ./quiz.md
notebooklm download flashcards --format json ./cards.json
notebooklm download mind-map ./mindmap.json
notebooklm download data-table ./data.csv
```

## 🛠️ Update & Maintenance

To update the skill to the latest version of `notebooklm-py`:

```bash
bash internal-docs
```

## 🔧 Troubleshooting

- **Login Issues**: If authentication fails, try `notebooklm login` again. A browser window should open.
- **Browser Automation**: This tool uses Playwright. You may see a browser window appear briefly during operations.

## 📂 File Structure

- `repo/`: The cloned `notebooklm-py` repository (git-tracked).
- `scripts/`: Helper scripts for maintenance.



## ⚖️ Principles

### 🛡️ Systemic Principles (Inherited)
1. **Respect Original Intent**: Do not change *what* the skill does, only *how* well it does it.
2. **Consolidate for Agents**: Future agents prefer clear CLIs over messy scripts.
3. **Traceability**: Always leave breadcrumbs (comments, logs) for the next agent.
4. **Safety First**: backup files if unsure (simple `cp file file.bak`).
5. **Token Economy**: `SKILL.md` is read often. Move static, one-time setup info to subfolders.
6. **Safe Updating (User Wisdom > Source)**: Prioritize user customizations. If the user has heavily iterated, think twice before overwriting with source updates. User's specific wisdom is more valuable than generic upstream changes.


## 🧬 Self-Evolution (Autopoiesis)

**Post-Task Reflection**: 
Before ending the session, the Agent MUST ask: "Did I learn a new pattern, fix a bug, or add a critical feature?"
-   **YES**: Log it in `CHANGELOG.md` and update `SKILL.md` / `references/` immediately.
-   **NO**: Do nothing.
-   **Constraint**: Only log **High-Signal** improvements (e.g., "Added retry logic"). Ignore noise (e.g., "Fixed typo").
-   **Principle Check**: Ensure any changes align with the `## ⚖️ Principles` section.
