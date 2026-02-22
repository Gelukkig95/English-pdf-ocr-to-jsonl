import os

def run_finetune():
    dataset_path = "data/processed/merged_dataset.jsonl"

    base_model = "gpt-4o-mini"

    command = f"""
    openai api fine_tunes.create \\
        -t {dataset_path} \\
        -m {base_model}
    """

    print("Running finetune command...")
    os.system(command)

if __name__ == "__main__":
    run_finetune()
