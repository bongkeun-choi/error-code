import requests

TURSO_DB_URL = "https://volvoerror-bongkeun-choi.aws-ap-northeast-1.turso.io"
TURSO_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3ODcwOTA3MDQsImlkIjoiMDFhMDE1M2QtNDAwMS03OWU4LTlmYWUtNWJmZDMyZjcyMGE3Iiwia2lkIjoicEo1RHFMd2V3dHJZLTBXWGNxRTd0cnVRNWxrWDlYOVFJNTYxZl9lSC1YTSIsInJpZCI6IjY1YmYwM2JjLTc1ZmEtNGQ1NC05MzY0LWFhNjYzNjRlNzZjNyJ9.O2P-wN5MFUe6jCbxxxSrvtMZt_MyTyavApqJ-2se7NwSgCbi1byQezjfr6Ba49TWcou0Cg4hBq1xUOg7DAVSBg"

url = f"{TURSO_DB_URL}/v2/pipeline"
headers = {
    "Authorization": f"Bearer {TURSO_TOKEN}",
    "Content-Type": "application/json"
}

sqls = [
    "DROP TABLE IF EXISTS diagnostics;",
    """
    CREATE TABLE diagnostics (
        unique_id TEXT PRIMARY KEY,
        dtc TEXT NOT NULL,
        model_name TEXT,
        doc_type TEXT NOT NULL,
        ecu TEXT,
        comp_name TEXT,
        search_text TEXT,
        content_json TEXT NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE INDEX idx_diag_dtc ON diagnostics(dtc);",
    "CREATE INDEX idx_diag_model ON diagnostics(model_name);",
    "CREATE INDEX idx_diag_comp ON diagnostics(comp_name);"
]

payload = {
    "requests": [{"type": "execute", "stmt": {"sql": sql.strip()}} for sql in sqls]
}

res = requests.post(url, headers=headers, json=payload, timeout=15)
if res.status_code == 200:
    print("\n🎉 [성공] 기종별 독립 보존(Composite Key) 지원 DB 스키마가 완벽하게 구축되었습니다!")
else:
    print("\n❌ 실패:", res.text)