from main import main


def test_main_runs(capsys):
    main()
    captured = capsys.readouterr()
    assert "Agent Trade inicializado" in captured.out
