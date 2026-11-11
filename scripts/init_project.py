#!/usr/bin/env python3
import os
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Initialize a NotebookLM Batch QA Project")
    parser.add_argument("name", help="Name of the notebook project (creates a subfolder)")
    parser.add_argument("--base-dir", default="./projects", help="Base directory for all NotebookLM QA projects")
    args = parser.parse_args()

    # Create a subfolder under the base directory
    target_dir = os.path.join(args.base_dir, args.name)
    os.makedirs(target_dir, exist_ok=True)

    # Create empty questions.json if not exists
    q_json_path = os.path.join(target_dir, "questions.json")
    if not os.path.exists(q_json_path):
        with open(q_json_path, "w", encoding="utf-8") as f:
            json.dump([{"id": "Q1", "question": "Your question here..."}], f, indent=2, ensure_ascii=False)
            
    # Create an empty or touch results.md
    md_path = os.path.join(target_dir, "QA_Results.md")
    if not os.path.exists(md_path):
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# NotebookLM QA Results: {args.name}\n\n")

    # Create a convenience runner script
    runner_path = os.path.join(target_dir, "run_interview.sh")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    auto_interview_script = os.path.join(script_dir, "auto_interview.py")
    
    with open(runner_path, "w", encoding="utf-8") as f:
        f.write("#!/bin/bash\n")
        f.write(f'cd "{target_dir}"\n')
        f.write(f'python3 "{auto_interview_script}" \\\n')
        f.write('  --notebook "YOUR_NOTEBOOK_ID_HERE" \\\n')
        f.write('  --questions "questions.json" \\\n')
        f.write('  --output "QA_Results.md" \\\n')
        f.write('  --workers 8\n')
        
    os.chmod(runner_path, 0o755)

    print(f"Project initialized at: {target_dir}")
    print(f"💡 Best Practice (Proxy Interviewer Workflow):")
    print(f"   1. Ask '介绍你自己' (Introduce yourself) to lock persona.")
    print(f"   2. Ask '请根据你的内容，列出 50 个我应该或可以问你的关键问题' to get a navigation map.")
    print(f"   3. Wait for the answers, then analyze them while 'wearing the user's shoes'.")
    print(f"   4. Finalize your `questions.json` based on the user's specific context and goals.")
    print(f"1. Edit questions in: {q_json_path}")
    print(f"2. Update YOUR_NOTEBOOK_ID_HERE in: {runner_path}")
    print(f"3. Run: ./run_interview.sh")

if __name__ == "__main__":
    main()
