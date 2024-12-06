import src.logtator as ld


def test_patch(capsys):
    settings = ld.Settings()
    ld.patch(settings)

    import logging
    log = logging.getLogger()
    # msg, *args, **kwargs
    log.warning("Hello, world!", kol="er")
    log.warning("Houston, we have a %s", "interesting problem")
    captured = capsys.readouterr()
    assert captured.err == "Hello, world!\nHouston, we have a interesting problem\n"

