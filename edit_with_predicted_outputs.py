import os
import time
from pathlib import Path

from openai import OpenAI

# MODEL = "gpt-4o-mini"  # must be a model that supports predicted outputs
MODEL = "gpt-5-chat-latest"
CODE_PATH = Path("sample_module.py")
CODE_PATH_2 = Path("sample_module_2.py")

client = OpenAI(api_key="api_key_here")


def edit_without_prediction():
    """Baseline: send the whole file in the prompt, no prediction param."""
    original_code = CODE_PATH.read_text()
    original_code_2 = CODE_PATH_2.read_text()


    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior Python engineer. "
                "You carefully modify existing files with minimal, targeted changes."
            ),
        },
        {
            "role": "user",
            "content": (
                # "Here is a Python module. Add basic logging only to the "
                "Here are two Python modules. Add basic logging only to the "
                "`process_orders` function:\n"
                "- Use the standard `logging` module.\n"
                "- Log before processing orders and after computing the summary.\n"
                "- Do not change behavior of any other functions.\n\n"
                "Return the FULL updated file as plain code (no markdown).\n\n"
                "=== FILE START ===\n"
                "Module 1"
                f"{original_code}\n"
                "===================="
                "Module 2"
                f"{original_code_2}\n"
                "=== FILE END ===\n"
            ),
        },
    ]

    start = time.perf_counter()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        # IMPORTANT: no prediction here
    )
    elapsed = time.perf_counter() - start

    new_code = completion.choices[0].message.content

    print("\n--- WITHOUT predicted output ---")
    print(f"Latency: {elapsed:.3f} s")
    print("Usage:", completion.usage)
    return new_code


def edit_with_prediction():
    """
    Optimized path: we reuse the ENTIRE file as the predicted output.

    The file is NOT in the user message text; it's only passed via `prediction`.
    The model uses that as both context and a candidate output and only tweaks
    the parts it disagrees with.
    """
    original_code = CODE_PATH.read_text()
    original_code_2 = CODE_PATH_2.read_text()

    messages = [
        {
            "role": "system",
            "content": (
                "You are a senior Python engineer. "
                "You carefully modify existing files with minimal, targeted changes."
            ),
        },
        {
            "role": "user",
            "content": (
                # "You are editing an existing Python module.\n\n"
                # "The current contents of the file are provided via the "
                # "`prediction` parameter (not in this message).\n\n"
                # "Task:\n"
                # "- Add basic logging only to the `process_orders` function.\n"
                # "  * Import `logging` if needed.\n"
                # "  * Log before processing orders and after computing the summary.\n"
                # "- Do not change behavior of any other functions or classes.\n"
                # "- Return the FULL updated file as plain code (no markdown).\n"
                # "Here is a Python module. Add basic logging only to the "
                # "`process_orders` function:\n"
                # "- Use the standard `logging` module.\n"
                # "- Log before processing orders and after computing the summary.\n"
                # "- Do not change behavior of any other functions.\n\n"
                # "Return the FULL updated file as plain code (no markdown).\n\n"
                # "=== FILE START ===\n"
                # f"{original_code}\n"
                # "=== FILE END ===\n"
                "Here are two Python modules. Add basic logging only to the "
                "`process_orders` function:\n"
                "- Use the standard `logging` module.\n"
                "- Log before processing orders and after computing the summary.\n"
                "- Do not change behavior of any other functions.\n\n"
                "Return the FULL updated file as plain code (no markdown).\n\n"
                "=== FILE START ===\n"
                "Module 1"
                f"{original_code}\n"
                "===================="
                "Module 2"
                f"{original_code_2}\n"
                "=== FILE END ===\n"
            ),
        },
    ]

    start = time.perf_counter()
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        # This is the key bit: reuse the entire file as predicted output
        prediction={
            "type": "content",
            # "content": original_code,
            "content": [
                {
                "type": "text",
                "text": original_code
                },
                {
                "type": "text",
                "text": original_code_2
                }
            ]
        },
    )
    elapsed = time.perf_counter() - start

    new_code = completion.choices[0].message.content

    print("\n--- WITH predicted output ---")
    print(f"Latency: {elapsed:.3f} s")
    print("Usage:", completion.usage)
    return new_code


def main():
    if not CODE_PATH.exists():
        raise SystemExit(
            f"{CODE_PATH} does not exist. Run this in the same folder as sample_module.py"
        )

    # 1) Edit without predicted output
    new_code_no_pred = edit_without_prediction()

    # 2) Edit with predicted output
    new_code_pred = edit_with_prediction()

    # Optionally, write results to disk so you can diff them in your editor
    Path("sample_module_without_prediction.py").write_text(new_code_no_pred)
    Path("sample_module_with_prediction.py").write_text(new_code_pred)

    print("\nWrote:")
    print("  sample_module_without_prediction.py")
    print("  sample_module_with_prediction.py")
    print("Diff them to see if the edits are equivalent.")


if __name__ == "__main__":
    main()