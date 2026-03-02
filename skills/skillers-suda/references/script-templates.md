# 스크립트 템플릿 가이드

## 개요

워크플로우에서 script 타입 단계가 필요할 때 이 템플릿을 참고하여 스크립트를 생성한다.

## Python 스크립트 템플릿

### 기본 템플릿
```python
#!/usr/bin/env python3
"""
{스크립트 설명}
Usage: python3 {script_name}.py [args]
"""
import sys
import json

def main():
    # 인자 처리
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Usage: python3 {script_name}.py <arg>"}), file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]

    try:
        # 핵심 로직
        result = process(arg)

        # 성공 출력 (JSON stdout)
        print(json.dumps({
            "status": "success",
            "data": result
        }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)

def process(input_data):
    """핵심 처리 로직"""
    # TODO: 구현
    return {"processed": input_data}

if __name__ == "__main__":
    main()
```

### API 호출 템플릿
```python
#!/usr/bin/env python3
"""
{API 이름} API 호출 스크립트
Usage: python3 {script_name}.py <endpoint> [api_key]
"""
import sys
import json
import urllib.request
import urllib.error

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "endpoint required"}), file=sys.stderr)
        sys.exit(1)

    endpoint = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        result = call_api(endpoint, api_key)
        print(json.dumps({
            "status": "success",
            "data": result
        }, ensure_ascii=False))
    except urllib.error.HTTPError as e:
        print(json.dumps({
            "status": "error",
            "code": e.code,
            "message": f"HTTP {e.code}: {e.reason}"
        }), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)

def call_api(endpoint, api_key=None):
    """API 호출"""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(endpoint, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

if __name__ == "__main__":
    main()
```

### 파일 처리 템플릿
```python
#!/usr/bin/env python3
"""
파일 변환/처리 스크립트
Usage: python3 {script_name}.py <input_file> <output_file>
"""
import sys
import json
import os

def main():
    if len(sys.argv) < 3:
        print(json.dumps({"status": "error", "message": "Usage: python3 script.py <input> <output>"}), file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(json.dumps({"status": "error", "message": f"File not found: {input_file}"}), file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        result = process(content)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)

        print(json.dumps({
            "status": "success",
            "input": input_file,
            "output": output_file,
            "size": len(result)
        }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)

def process(content):
    """파일 내용 처리"""
    # TODO: 구현
    return content

if __name__ == "__main__":
    main()
```

## Bash 스크립트 템플릿

### 기본 템플릿
```bash
#!/bin/bash
# {스크립트 설명}
# Usage: bash {script_name}.sh [args]

set -euo pipefail

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# 인자 확인
if [ $# -lt 1 ]; then
    echo "Usage: bash $0 <arg>" >&2
    exit 1
fi

ARG="$1"

# 핵심 로직
echo -e "${GREEN}처리 중: ${ARG}${NC}"

# 결과 출력
echo "완료: ${ARG} 처리됨"
```

### 파일 검증 템플릿
```bash
#!/bin/bash
# 파일/디렉토리 구조 검증
# Usage: bash validate.sh <target_dir>

set -euo pipefail

TARGET="${1:-.}"
ERRORS=0

check() {
    local file="$1"
    local desc="$2"
    if [ -f "$file" ]; then
        echo "  [OK] $desc"
    else
        echo "  [FAIL] $desc: $file not found" >&2
        ERRORS=$((ERRORS + 1))
    fi
}

echo "=== 검증 시작: $TARGET ==="

check "$TARGET/SKILL.md" "SKILL.md 존재"
# 추가 검증...

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "모든 검증 통과!"
else
    echo "$ERRORS개 실패" >&2
    exit 1
fi
```

## 스크립트 공통 규칙

### 필수
- 항상 shebang 포함 (`#!/usr/bin/env python3` 또는 `#!/bin/bash`)
- 에러 시 exit code 1 + stderr 메시지
- 성공 시 stdout으로 결과 출력 (JSON 권장)
- 외부 의존성 최소화 (표준 라이브러리 우선)
- `${CLAUDE_PLUGIN_ROOT}` 경로 사용

### 권장
- Python: `json.dumps(result, ensure_ascii=False)` 로 한글 지원
- Bash: `set -euo pipefail` 로 안전 실행
- 인자 없으면 usage 출력
- UTF-8 인코딩 명시

### 금지
- `pip install` 등 런타임 패키지 설치
- 하드코딩된 절대 경로
- 네트워크 없이 동작 불가한 필수 로직 (fallback 필요)
- 표준 라이브러리 외 import (불가피하면 SKILL.md에 의존성 명시)
