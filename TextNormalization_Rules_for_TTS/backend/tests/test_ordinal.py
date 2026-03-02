"""Ordinal normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  ORDINAL TESTS")
    print("─"*70)

    for name, text in [
        ("Ordinal 1st", "அவர் 1st இடத்தில் இருக்கிறார்"),
        ("Ordinal 5th", "அவர் 5th வகுப்பில் படிக்கிறார்"),
        ("Ordinal 21st", "இன்று 21st நூற்றாண்டு"),
        ("Tamil ordinal suffix (3ஆம்)", "அவரது 3ஆம் முயற்சி வெற்றி பெற்றது"),
    ]:
        print_test_result(
            name, text, ['ordinal'],
            engine.normalize(text, ['ordinal']),
        )

    print("✅ Ordinal tests passed!")


if __name__ == '__main__':
    run()
