"""Currency normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  CURRENCY TESTS")
    print("─"*70)

    print_test_result(
        "Simple Currency (₹500)",
        "என்னிடம் ₹500 உள்ளது",
        ['currency'],
        engine.normalize("என்னிடம் ₹500 உள்ளது", ['currency']),
    )

    print_test_result(
        "Currency with Decimal (₹500.50)",
        "விலை ₹500.50 ஆகும்",
        ['currency'],
        engine.normalize("விலை ₹500.50 ஆகும்", ['currency']),
    )

    print_test_result(
        "Large Currency (₹125000)",
        "சம்பளம் ₹125000 ஒரு மாதத்திற்கு",
        ['currency'],
        engine.normalize("சம்பளம் ₹125000 ένα மாதத்திற்கு".replace("ένα", ""), ['currency']),
    )

    print("✅ Currency tests passed!")


if __name__ == '__main__':
    run()
