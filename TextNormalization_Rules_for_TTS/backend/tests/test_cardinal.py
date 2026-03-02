"""Cardinal number normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  CARDINAL TESTS")
    print("─"*70)

    print_test_result(
        "Cardinal Numbers",
        "எனக்கு 25 புத்தகங்கள் வேண்டும்",
        ['cardinal'],
        engine.normalize("எனக்கு 25 புத்தகங்கள் வேண்டும்", ['cardinal']),
    )

    print_test_result(
        "Large Cardinal (Lakhs/Crores)",
        "மக்கள் தொகை 5000000 ஆகும்",
        ['cardinal'],
        engine.normalize("மக்கள் தொகை 5000000 ஆகும்", ['cardinal']),
    )

    print("✅ Cardinal tests passed!")


if __name__ == '__main__':
    run()
