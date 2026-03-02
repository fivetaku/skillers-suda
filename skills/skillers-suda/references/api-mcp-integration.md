# API/MCP 연동 가이드

## 개요

스킬에서 외부 도구와 연동할 때의 판단 기준과 구현 방법.

## 연동 우선순위

```
1순위: API가 있으면 → API 직접 호출 (스크립트로 구현)
2순위: API 없고 MCP가 있으면 → MCP 서버 연동
3순위: 둘 다 없으면 → Claude가 직접 구현
```

### 왜 API를 우선하는가?
- API: 표준화된 인터페이스, 문서화 되어 있음, 스크립트로 반복 호출 가능
- MCP: Claude Code에 의존적, 서버 설치 필요, 동적 호출
- 직접 구현: Claude의 추론에 의존, 일관성 보장 어려움

## API 연동

### 판단 기준
- 공식 API 문서가 있는가?
- REST API 또는 GraphQL 인가?
- 인증 방식이 API 키 또는 OAuth 인가?

### 구현 방식
API 호출은 **반드시 스크립트(script 타입)로** 구현한다.

```
### Step N: {API 연동 단계}
**타입**: script
**스크립트**: `scripts/call_{service}_api.py`

{service} API를 호출하여 {목적}을 수행한다.

환경변수:
- `{SERVICE}_API_KEY`: API 인증 키

Bash로 실행:
\`\`\`bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/{skill}/scripts/call_{service}_api.py "$INPUT"
\`\`\`
```

### API 스크립트 패턴
```python
#!/usr/bin/env python3
import os
import json
import urllib.request

API_KEY = os.environ.get("{SERVICE}_API_KEY", "")
BASE_URL = "https://api.{service}.com/v1"

def call(endpoint, data=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())
```

### 인증 방식별 처리

| 인증 | 환경변수 | 헤더 |
|------|---------|------|
| API Key | `{SERVICE}_API_KEY` | `Authorization: Bearer {key}` |
| Basic Auth | `{SERVICE}_USER`, `{SERVICE}_PASS` | `Authorization: Basic {base64}` |
| OAuth | `{SERVICE}_TOKEN` | `Authorization: Bearer {token}` |
| No Auth | - | - |

API 키는 환경변수로만 전달. 코드에 하드코딩 금지.

## MCP 연동

### 판단 기준
- API가 없거나 복잡한가?
- MCP 서버가 이미 설치되어 있는가?
- Claude Code의 MCP 도구로 충분한가?

### 사용 가능한 MCP 서버 확인

사용자에게 물어보거나 환경을 스캔:
```bash
# .mcp.json 또는 claude_desktop_config.json 확인
cat ~/.claude/.mcp.json 2>/dev/null || echo "MCP 설정 없음"
```

### 구현 방식

MCP 도구는 SKILL.md에서 직접 호출한다:

```
### Step N: {MCP 연동 단계}
**타입**: api_mcp (MCP)
**MCP 서버**: {server-name}

{server-name} MCP 서버의 {tool-name} 도구를 사용하여 {목적}을 수행한다.

도구 호출:
- 서버: {server-name}
- 도구: {tool-name}
- 파라미터: {param1}, {param2}

실패 시:
- MCP 서버가 없으면 → 사용자에게 설치 안내
- 도구 호출 실패 → {fallback 동작}
```

### 일반적인 MCP 서버 목록

| MCP 서버 | 용도 | 도구 예시 |
|---------|------|---------|
| slack-mcp | Slack 메시지 | send_message, read_channel |
| notion-mcp | Notion 페이지 | create_page, query_database |
| github-mcp | GitHub | create_issue, create_pr |
| filesystem-mcp | 파일 시스템 | read_file, write_file |
| postgres-mcp | PostgreSQL | query, execute |

## 직접 구현 (fallback)

### 판단 기준
- API도 MCP도 없는 경우
- 단순한 웹 스크래핑이나 데이터 처리
- Claude의 내장 도구로 충분한 경우

### 구현 방식
```
### Step N: {직접 구현 단계}
**타입**: prompt 또는 script

{Claude가 직접 처리하거나 스크립트로 구현}

사용 도구: {Read/Write/WebFetch/Bash 등}
```

## 핵심 규칙

### API/MCP 결과는 반드시 검토

```
Step N: API/MCP 호출 → Step N+1: 검토(review) → Step N+2: 생성(generate)
```

외부 데이터를 그대로 최종 출력으로 사용하면 안 된다.
반드시 검토 단계를 거쳐서:
- 데이터 형식이 올바른지
- 예상한 내용인지
- 누락된 정보는 없는지

### 에러 처리

모든 API/MCP 단계에는 fallback 설계가 필수:

```
실패 시 대안:
1. 캐시된 이전 결과 사용
2. 기본값 사용
3. 사용자에게 수동 입력 요청
4. 해당 단계 스킵 (워크플로우가 허용하는 경우)
```

### 환경 의존성 문서화

API 키나 MCP 서버가 필요한 스킬은 SKILL.md에 명시:

```markdown
## 요구사항

이 스킬을 사용하려면:
- `{SERVICE}_API_KEY` 환경변수 설정 필요
- 또는 `{mcp-server}` MCP 서버 설치 필요

설정 방법:
\`\`\`bash
export {SERVICE}_API_KEY="your-api-key"
\`\`\`
```
