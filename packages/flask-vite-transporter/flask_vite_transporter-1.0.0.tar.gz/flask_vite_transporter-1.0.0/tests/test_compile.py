import subprocess


def test_pack_vite_apps():
    p = subprocess.run(["vt", "pack"], stdout=subprocess.PIPE)
    terminal_output = p.stdout.decode("utf-8")
    assert "frontend packed!" in terminal_output


def test_list_vite_apps():
    p = subprocess.run(["vt", "list"], stdout=subprocess.PIPE)
    terminal_output = p.stdout.decode("utf-8")
    assert (
        "\x1b[92mfrontend/dist/assets\x1b[0m \x1b[1m=>\x1b[0m \x1b[92mapp_flask/vt/frontend/\x1b[0m"
        in terminal_output
    )


def test_app_flask(client):
    response = client.get("/")
    assert response.status_code == 200
