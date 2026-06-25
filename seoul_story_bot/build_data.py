# -*- coding: utf-8 -*-
"""[사용 중단됨 / DEPRECATED]

예전에는 이 스크립트가 contents.json에 작품·장소 데이터를 생성했습니다.
지금은 모든 시드 데이터가 app/catalog.py 한 곳에 있고,
서버 시작 시 app/db.py가 SQLite(data/app.db)로 자동 시드합니다.
contents.json은 화면 문구(ui) 전용으로 바뀌었습니다.

데이터를 바꾸려면:
  1) app/catalog.py 를 편집하고
  2) data/app.db 를 삭제한 뒤
  3) 서버를 재시작하세요. (시드는 DB가 비어 있을 때만 동작)

이 파일은 더 이상 필요 없으며 삭제해도 됩니다.
"""
import sys

if __name__ == "__main__":
    print(__doc__)
    sys.exit(0)
