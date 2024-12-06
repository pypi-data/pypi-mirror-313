import argparse
from typing_test.typing_test import typing_test

def main():
    parser = argparse.ArgumentParser(
        description="Process test parameters with optional blind mode."
    )
    parser.add_argument(
        "tests",
        type=int,
        nargs="?",
        default=2,
        help="The number of tests to run (default: 2).",
    )
    parser.add_argument(
        "sentences_per_test",
        type=int,
        nargs="?",
        default=1,
        help="The number of sentences per test (default: 1).",
    )
    parser.add_argument(
        "blind_mode",
        type=str,
        nargs="?",
        default="no",
        help="Set blind mode to 'y' or 'yes' to enable it (default: no).",
    )

    # Parse arguments, silently fallback to defaults for invalid input
    try:
        args = parser.parse_args()
        # Validate inputs and fallback silently if necessary
        tests = args.tests if isinstance(args.tests, int) else 2
        sentences_per_test = args.sentences_per_test if isinstance(args.sentences_per_test, int) else 1
        blind_mode = args.blind_mode if isinstance(args.blind_mode, str) else "no"
        blind_mode_bool = blind_mode.lower()[0] == "y"
        typing_test(tests, sentences_per_test, blind_mode_bool)
    except KeyboardInterrupt:
        print("\n\nExiting Typing Speed Test...")
        exit(0)
    except Exception:
        # Fallback to default values
        typing_test()

if __name__ == "__main__":
    main()