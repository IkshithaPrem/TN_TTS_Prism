"""Named entity normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  NAMED ENTITY TESTS")
    print("─"*70)

    for name, text in [
        ("Tamil title (டா.)", "டா. ராஜ் வருகிறார்"),
        ("Tamil title (திரு)", "திரு ரவி அவர்களை சந்திக்கவும்"),
        ("English title (Dr.)", "Dr. Kumar கூறினார்"),
    ]:
        print_test_result(
            name, text, ['named_entity'],
            engine.normalize(text, ['named_entity']),
        )

    print("✅ Named entity tests passed!")


if __name__ == '__main__':
    run()
