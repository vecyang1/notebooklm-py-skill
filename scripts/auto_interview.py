#!/usr/bin/env python3
import argparse
import json
import subprocess
import os
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

def ask_question(q_id, q_text, notebook_id, notebooklm_cli, max_retries=2):
    # Jitter to prevent all playwright instances starting at the exact same ms and causing CPU spikes
    time.sleep(random.uniform(0.1, 2.0))
    
    for attempt in range(max_retries + 1):
        print(f"[{q_id}] Starting (Attempt {attempt + 1}/{max_retries + 1}): {q_text[:50]}...")
        cmd = [notebooklm_cli, "ask", q_text, "--notebook", notebook_id]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=240)
            stdout = result.stdout
            
            answer = stdout
            if "Answer:\n" in stdout:
                answer = stdout.split("Answer:\n")[1].strip()
            if "Conversation:" in answer:
                answer = answer.split("Conversation:")[0].strip()
                
            print(f"[{q_id}] Completed successfully.")
            return {"id": q_id, "question": q_text, "answer": answer, "error": None}
            
        except subprocess.CalledProcessError as e:
            err_msg = e.stderr.strip() or e.stdout.strip()
            print(f"[{q_id}] FAILED with exit code {e.returncode}. Error: {err_msg}")
            if attempt == max_retries:
                return {"id": q_id, "question": q_text, "answer": None, "error": err_msg}
        except subprocess.TimeoutExpired as e:
            print(f"[{q_id}] FAILED with timeout.")
            if attempt == max_retries:
                return {"id": q_id, "question": q_text, "answer": None, "error": "Request timed out after 240s."}
        except Exception as e:
            print(f"[{q_id}] FAILED with exception: {e}")
            if attempt == max_retries:
                return {"id": q_id, "question": q_text, "answer": None, "error": str(e)}
                
        print(f"[{q_id}] Retrying in 10 seconds...")
        time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description="Batch interview a NotebookLM project")
    parser.add_argument("--notebook", required=True, help="Notebook ID")
    parser.add_argument("--questions", required=True, help="Path to JSON file containing list of questions")
    parser.add_argument("--output", required=True, help="Path to output Markdown file")
    parser.add_argument("--workers", type=int, default=8, help="Number of parallel workers")
    parser.add_argument("--retries", type=int, default=2, help="Max retries per question if timeout or error occurs")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.questions):
        print(f"Error: Questions file not found at {args.questions}")
        return
        
    with open(args.questions, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    notebooklm_cli = os.path.join(skill_dir, "repo", ".venv", "bin", "notebooklm")
    
    if not os.path.exists(notebooklm_cli):
        print(f"Error: notebooklm CLI not found at {notebooklm_cli}")
        return
    
    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)
    
    # State file to save incremental progress
    state_file = os.path.join(out_dir, "interview_state.json")
    results = {}
    
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                results = json.load(f)
                print(f"Loaded {len(results)} existing results from state file {state_file}.")
        except json.JSONDecodeError:
            print("Warning: State file is corrupted, starting fresh.")
            pass

    # Filter out already successfully answered questions
    pending_questions = [q for q in questions if q.get("id") not in results or results[q.get("id")].get("error") is not None]
    
    if not pending_questions:
        print("All questions already answered. Generating final markdown...")
    else:
        print(f"Starting {len(pending_questions)} pending questions with {args.workers} workers...")
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_qid = {
                executor.submit(ask_question, item.get("id", f"Q{i+1}"), item.get("question", ""), args.notebook, notebooklm_cli, args.retries): item.get("id", f"Q{i+1}")
                for i, item in enumerate(pending_questions)
            }
            
            for future in as_completed(future_to_qid):
                res = future.result()
                results[res["id"]] = res
                
                # Save incremental state safely
                with open(state_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                
    # Write to final Markdown file sequentially to guarantee correct order
    print(f"Writing final results to {args.output}...")
    with open(args.output, "w", encoding="utf-8") as out_f:
        out_f.write(f"# NotebookLM Batch Interview Results\n\n")
        out_f.write(f"**Notebook ID**: `{args.notebook}`\n\n---\n\n")
        for i, item in enumerate(questions):
            q_id = item.get("id", f"Q{i+1}")
            res = results.get(q_id)
            
            if not res:
                continue
                
            if res.get("error"):
                out_f.write(f"## {q_id} (FAILED)\n\n")
                out_f.write(f"**问:** \n{res['question']}\n\n")
                out_f.write(f"**Error:**\n{res['error']}\n\n---\n\n")
            else:
                out_f.write(f"## {q_id}\n\n")
                out_f.write(f"**问:** \n{res['question']}\n\n")
                out_f.write(f"**答:**\n{res['answer']}\n\n---\n\n")
                
    print(f"\nAll done! Results saved to {args.output}")

if __name__ == "__main__":
    main()
