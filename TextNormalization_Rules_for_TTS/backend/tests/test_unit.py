"""Unit normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  UNIT TESTS")
    print("─"*70)

    for name, text in [
        ("Weight Unit (5kg)", "என் எடை 5kg ஆகும்"),
        ("Distance Unit (10km)", "தூரம் 10km ஆகும்"),
        ("Volume Unit (100ml)", "தண்ணீர் 100ml வேண்டும்"),
        ("Temperature Unit (25°C)", "வெப்பநிலை 25°C ஆகும்"),
        ("Data Unit (500MB)", "டேட்டா 500MB மீதம் உள்ளது"),
    ]:
        print_test_result(
            name, text, ['unit'],
            engine.normalize(text, ['unit']),
        )

    print("✅ Unit tests passed!")


if __name__ == '__main__':
    run()
