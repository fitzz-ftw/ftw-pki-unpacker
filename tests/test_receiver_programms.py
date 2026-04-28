import pytest
from pathlib import Path
from io import BytesIO
from ftwpki.receiver.programms import prog_receive_certs


def test_prog_receive_certs_full_flow(mocker):
    # 1. MOCK: CLI-Argumente
    mock_args = mocker.Mock()
    mock_args.private_key = "test.key"
    mock_args.cert_file = "package.zip.enc"
    mocker.patch("ftwpki.receiver.programms.ReceiverCliParser.parse_args", return_value=mock_args)

    # 2. MOCK: Konfiguration & Pfade
    # Statt die Instanz zu patchen, patchen wir die Methode der Klasse Path
    # innerhalb des Zielmoduls.
    mocker.patch("ftwpki.receiver.programms.Path.is_file", return_value=True)

    mocker.patch("ftwpki.receiver.programms.toml2config", return_value={
        "private_keys": "/tmp/priv", 
        "certs": "/tmp/certs", 
        "public_data": "/tmp/pub", 
        "chains": "/tmp/chain",
        "ext_cert": ".crt", 
        "ext_public": ".pub", 
        "ext_chain": ".pem"
    })

    # Verhindert mkdir() und sorgt für konsistente Rückgabewerte
    mocker.patch("ftwpki.receiver.programms.create_app_pathes", return_value={
        "private_keys": Path("/tmp/priv"), 
        "certs": Path("/tmp/certs"),
        "public_data": Path("/tmp/pub"), 
        "chains": Path("/tmp/chain")
    })

    # 3. MOCK: Dateizugriffe & Krypto
    mocker.patch("pathlib.Path.read_bytes", return_value=b"fake_encrypted_data")
    mocker.patch("ftwpki.receiver.programms.load_private_key_from_pem", return_value=mocker.Mock())
    mocker.patch(
        "ftwpki.receiver.programms.decrypt_transport_package", return_value=b"fake_zip_content"
    )

    # Mock für get_password (getpass)
    mocker.patch("ftwpki.receiver.programms.get_password", return_value="1234")

    # 4. MOCK: ZipFile


    mock_zip = mocker.MagicMock()
    mock_zip.namelist.return_value = ["user.crt", "data.pub", "chain.pem", "readme.txt"]

    # WICHTIG: ZipFile(...) liefert den Mock, und dieser Mock
    # liefert sich selbst beim Betreten des 'with'-Blocks (__enter__).
    mocker.patch("ftwpki.receiver.programms.ZipFile", return_value=mock_zip)
    mock_zip.__enter__.return_value = mock_zip

    # Ausführung
    result = prog_receive_certs(["test.key", "package.zip.enc"])

    # Assertions
    assert result == 0
    # Jetzt prüfen wir direkt auf dem mock_zip
    assert mock_zip.extract.call_count == 4


def test_prog_receive_certs_creates_config(mocker):
    mocker.patch("ftwpki.receiver.programms.Path.is_file", return_value=False)
    mock_write = mocker.patch("ftwpki.receiver.programms.write_example_config")

    # Wir lassen es danach absichtlich krachen, da uns nur die Zeile 32 interessiert
    mocker.patch("ftwpki.receiver.programms.toml2config", side_effect=RuntimeError("Stop"))

    prog_receive_certs(["key.pem", "bundle.zip.enc"])
    assert mock_write.called

def test_prog_receive_certs_exception_handling(mocker):
    # Wir provozieren einen Fehler beim Laden des Keys
    mocker.patch("ftwpki.receiver.programms.Path.is_file", return_value=True)
    mocker.patch(
        "ftwpki.receiver.programms.load_private_key_from_pem",
        side_effect=Exception("Kritischer Fehler"),
    )

    # Mock für print, damit die Konsole beim Testlauf sauber bleibt
    mocker.patch("builtins.print")

    result = prog_receive_certs(["test.key", "test.zip.enc"])
    assert result == 1



def test_prog_receive_certs_interrupt_final(mocker):
    # Setup
    mocker.patch("ftwpki.receiver.programms.Path.is_file", return_value=True)
    mocker.patch("ftwpki.receiver.programms.toml2config", return_value={})

    # Wir nehmen parse_args als Vehikel für den Interrupt,
    # da es sicher im try-Block ausgeführt wird.
    mocker.patch(
        "ftwpki.receiver.programms.ReceiverCliParser.parse_args", side_effect=KeyboardInterrupt
    )

    result = prog_receive_certs(["any.key", "any.zip"])

    # Wenn result 1 ist und die Coverage für 67 steigt, hat es gezündet.
    assert result == 1
