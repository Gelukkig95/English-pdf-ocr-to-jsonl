import os
import argparse
from openai import OpenAI

def build_parser():
    p = argparse.ArgumentParser(description="Run inference with a fine-tuned model.")
    p.add_argument("--model", default=os.getenv("OPENAI_MODEL", ""), help="Fine-tuned model id (or set OPENAI_MODEL).")
    p.add_argument("--system", default="You are a helpful writing assistant.", help="System prompt.")
    p.add_argument("--max_tokens", type=int, default=900, help="Max tokens for output.")
    p.add_argument("--temperature", type=float, default=0.9, help="Creativity level.")
    return p

def run():
    args = build_parser().parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set. Set it in your environment first.")

    if not args.model:
        raise SystemExit("Model id is empty. Pass --model <MODEL_ID> or set OPENAI_MODEL.")

    client = OpenAI()

    prompt = input("What should I write about? ").strip()
    if not prompt:
        raise SystemExit("Empty prompt.")

    try:
        resp = client.chat.completions.create(
            model=args.model,
            messages=[
                {"role": "system", "content": args.system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=args.max_tokens,
            temperature=args.temperature,
        )
        print("\n=== writing ===\n")
        print(resp.choices[0].message.content)

    except Exception as e:
        raise SystemExit(f"API error: {e}")

if __name__ == "__main__":
    run()