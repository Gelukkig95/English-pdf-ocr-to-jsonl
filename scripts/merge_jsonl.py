import os
import argparse

def merge_jsonl(inputs, output_path, dedupe=False):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    seen = set()
    written = 0

    with open(output_path, "w", encoding="utf-8") as out_f:
        for path in inputs:
            if not os.path.exists(path):
                print(f"skip (not found): {path}")
                continue

            with open(path, "r", encoding="utf-8") as in_f:
                for line in in_f:
                    line = line.strip()
                    if not line:
                        continue

                    if dedupe:
                        if line in seen:
                            continue
                        seen.add(line)

                    out_f.write(line + "\n")
                    written += 1

    print(f"JSONL combined: {output_path}")
    print(f"lines written: {written}")

def build_parser():
    p = argparse.ArgumentParser(description="Merge multiple JSONL files into one.")
    p.add_argument("--inputs", nargs="+", required=True, help="Input JSONL paths.")
    p.add_argument("--output", required=True, help="Output JSONL path.")
    p.add_argument("--dedupe", action="store_true", help="Remove exact duplicate lines.")
    return p

if __name__ == "__main__":
    args = build_parser().parse_args()
    merge_jsonl(args.inputs, args.output, dedupe=args.dedupe)