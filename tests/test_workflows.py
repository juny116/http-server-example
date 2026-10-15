from functools import partial
from http.server import ThreadingHTTPServer
from threading import Thread
from urllib.request import urlopen
from urllib.error import HTTPError
import pytest
from image_server.server import ImageHandler


def test_image_server_serves_requested_file_and_rejects_other_paths(tmp_path):
    image = tmp_path / "example.png"; image.write_bytes(b"synthetic-image")
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(ImageHandler, image_path=image))
    thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        with urlopen(base) as response:
            assert response.read() == b"synthetic-image"
            assert response.headers["Content-Type"] == "image/png"
        with pytest.raises(HTTPError) as error: urlopen(base + "/missing")
        assert error.value.code == 404
    finally:
        server.shutdown(); server.server_close(); thread.join()
