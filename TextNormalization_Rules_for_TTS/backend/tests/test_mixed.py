"""Mixed / combined category normalization tests (Tamil)."""

from helpers import get_engine, print_test_result, ALL_CATEGORIES


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  MIXED / COMBINED TESTS")
    print("─"*70)

    # Currency + Cardinal in a single sentence
    text_currency_cardinal = "என்னிடம் ₹500 உள்ளது மற்றும் எனக்கு 25 புத்தகங்கள் வேண்டும்"
    print_test_result(
        "Mixed: Currency + Cardinal",
        text_currency_cardinal,
        ['currency', 'cardinal'],
        engine.normalize(
            text_currency_cardinal,
            ['currency', 'cardinal'],
        ),
    )

    # All categories in one Tamil sentence
    text_all = (
        "டா. ராஜ் அவர்கள் 15/08/2024 அன்று 10:30 மணிக்கு ₹500 க்கு 5kg அரிசியை "
        "முதல் முறையாக வாங்கினார்"
    )
    print_test_result(
        "Mixed: All Categories",
        text_all,
        ALL_CATEGORIES,
        engine.normalize(
            text_all,
            ALL_CATEGORIES,
        ),
    )

    # Plain Tamil text, nothing to normalize
    plain_text = "இது ஒரு சாதாரண வாக்கியம்"
    print_test_result(
        "Plain Text (No normalization needed)",
        plain_text,
        ALL_CATEGORIES,
        engine.normalize(plain_text, ALL_CATEGORIES),
    )

    print("✅ Mixed tests passed!")


if __name__ == '__main__':
    run()
