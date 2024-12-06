from czo import DateLib, DirLib, NetLib, PathLib, Person, Random


def test_random(capsys):
    Random.help()

    captured = capsys.readouterr()

    assert "Random" in captured.out and "help" in captured.out


def test_person(capsys):
    Person.help()

    captured = capsys.readouterr()

    assert "Person" in captured.out and "help" in captured.out


def test_pathlib(capsys):
    PathLib.help()

    captured = capsys.readouterr()

    assert "PathLib" in captured.out and "help" in captured.out


def test_netlib(capsys):
    NetLib.help()

    captured = capsys.readouterr()

    assert "NetLib" in captured.out and "help" in captured.out


def test_dirlib(capsys):
    DirLib.help()

    captured = capsys.readouterr()

    assert "DirLib" in captured.out and "help" in captured.out


def test_datelib(capsys):
    DateLib.help()

    captured = capsys.readouterr()

    assert "DateLib" in captured.out and "help" in captured.out
