"""Date normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  DATE TESTS")
    print("─"*70)

    for name, text in [
        ("Date with slash (15/08/2024)", "சுதந்திர தினம் 15/08/2024 அன்று வருகிறது"),
        ("Date with dash (01-01-2025)", "புது ஆண்டு 01-01-2025 முதல் தொடங்கும்"),
        ("Date with dot (26.01.2026)", "குடியரசு தினம் 26.01.2026 அன்று வருகிறது"),
    ]:
        print_test_result(
            name, text, ['date'],
            engine.normalize(text, ['date']),
        )

    print("✅ Date tests passed!")


if __name__ == '__main__':
    run()
