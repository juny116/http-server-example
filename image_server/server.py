"""Serve one explicitly selected PNG file."""
import argparse
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

class ImageHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, image_path, **kwargs):
        self.image_path = Path(image_path)
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        try:
            content = self.image_path.read_bytes()
        except OSError:
            self.send_error(404, "Image not found")
            return
        self.send_response(200)
        self.send_header("Content-Type", "image/png")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    if not args.image.is_file():
        parser.error("--image must name an existing file")
    handler = partial(ImageHandler, image_path=args.image)
    with ThreadingHTTPServer((args.host, args.port), handler) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    main()
