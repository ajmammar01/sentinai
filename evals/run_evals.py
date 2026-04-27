import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Resolve project paths from this file location (works from any cwd).
EVALS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = EVALS_DIR.parent
APP_DIR = PROJECT_ROOT / "app"
TEST_CASES_PATH = EVALS_DIR / "test_cases.json"

# Ensure `import app...` works when running from evals/.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load .env defensively for standalone script execution.
# Primary: app/.env (current project layout), fallback: root/.env.
load_dotenv(dotenv_path=APP_DIR / ".env", override=False)
load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)

from app.services.processor import EmailProcessor

def main():
    processor = EmailProcessor()
    
    # Load the test cases
    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"Starting evaluation on {len(test_cases)} cases...\n")
    passed = 0

    for case in test_cases:
        print(f"Testing: [{case['name']}]")
        
        # Run your actual app logic
        result = processor.process_email(case["input"])
        
        # Check if the AI's classification matches our expectation
        predicted_type = result.data.type
        if predicted_type == case["expected_type"]:
            print(f"  PASS: Classified as '{predicted_type}'")
            passed += 1
        else:
            print(f"  FAIL: Expected '{case['expected_type']}', but got '{predicted_type}'")

    print(f"\n--- Score: {passed}/{len(test_cases)} ---")

if __name__ == "__main__":
    main()
    