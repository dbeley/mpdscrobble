from mpdscribble_history import read_journal


def test_read_journal_handles_values_containing_separator(tmp_path):
    journal = tmp_path / "journal"
    journal.write_text(
        "a = Foo\nt = She = Me\nb = Album\ni = 1700000000\n\n"
        "a = Bar\nt = Baz\nb = Qux  \ni = 1700000100\n"
    )

    tracks = read_journal(str(journal))

    assert [t.artist for t in tracks] == ["Foo", "Bar"]
    assert [t.title for t in tracks] == ["She = Me", "Baz"]
    assert [t.album for t in tracks] == ["Album", "Qux"]
    assert [t.timestamp for t in tracks] == [1700000000, 1700000100]
