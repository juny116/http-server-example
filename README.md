# Image HTTP Server

지정한 PNG 파일을 HTTP로 제공하는 작은 서버입니다. devpod_VScode와 test01의 같은 구현을 하나로 묶었습니다.

## 코드 구조

| 경로 | 역할 |
|---|---|
| `image_server/server.py` | 요청 처리, 파일 읽기, HTTP 응답 및 CLI |

## 실행

```bash
python -m image_server.server --image /path/to/image.png --port 8080
```

루트 경로만 이미지를 반환하고 다른 경로와 없는 파일은 404로 응답합니다. 기본 바인딩은 localhost입니다.

## Source and license

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for project origins and third-party licenses.
