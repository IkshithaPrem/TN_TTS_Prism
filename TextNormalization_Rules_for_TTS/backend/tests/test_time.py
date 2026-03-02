"""Time normalization tests (Tamil)."""

from helpers import get_engine, print_test_result


def run():
    engine = get_engine()

    print("\n" + "─"*70)
    print("  TIME TESTS")
    print("─"*70)

    for name, text in [
        ("Simple Time (10:30)", "கூட்டம் 10:30 மணிக்கு உள்ளது"),
        ("24-hour Time (14:45)", "ரயில் 14:45 மணிக்கு வரும்"),
        ("Time with seconds (10:30:15)", "நேரம் 10:30:15 ஆகிறது"),
        ("Exact hour (2:00)", "நிகழ்ச்சி 2:00 மணிக்கு தொடங்கும்"),
    ]:
        print_test_result(
            name, text, ['time'],
            engine.normalize(text, ['time']),
        )

    print("✅ Time tests passed!")


if __name__ == '__main__':
    run()
