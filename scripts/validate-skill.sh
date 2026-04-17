#!/usr/bin/env bash
# 생성된 스킬의 구조와 품질을 검증하는 스크립트
# Usage: bash validate-skill.sh <skill_directory>
#
# DEPRECATED (scheduled for removal in the next release):
#   This bash script does not run on Windows PowerShell / CMD without
#   Git Bash or WSL. Use the cross-platform equivalents instead:
#     - scripts/validate-skill.js           (Node.js, identical checks)
#     - skills/skillers-suda/scripts/verify-skill.py  (Python, richer output)
#   The in-plugin workflow (Phase E-verify) already invokes verify-skill.py;
#   this file is kept temporarily only for external callers.

set -euo pipefail

echo "[DEPRECATION] validate-skill.sh is deprecated. Prefer 'node scripts/validate-skill.js' or 'python3 skills/skillers-suda/scripts/verify-skill.py'." >&2

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0
WARNINGS=0

if [ $# -lt 1 ]; then
    echo "Usage: bash $0 <skill_directory>" >&2
    echo "Example: bash $0 skills/my-skill" >&2
    exit 1
fi

TARGET="$1"

echo "=== 스킬 검증: $TARGET ==="
echo ""

# --- 필수 파일 검증 ---
echo "📁 파일 구조 검증:"

check_file() {
    local file="$1"
    local desc="$2"
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}[OK]${NC} $desc"
    else
        echo -e "  ${RED}[FAIL]${NC} $desc: $file" >&2
        ERRORS=$((ERRORS + 1))
    fi
}

check_file "$TARGET/SKILL.md" "SKILL.md 존재"

# --- SKILL.md Frontmatter 검증 ---
echo ""
echo "📝 SKILL.md 검증:"

if [ -f "$TARGET/SKILL.md" ]; then
    # frontmatter 존재 확인
    if head -1 "$TARGET/SKILL.md" | grep -q "^---"; then
        echo -e "  ${GREEN}[OK]${NC} frontmatter 존재"
    else
        echo -e "  ${RED}[FAIL]${NC} frontmatter 없음 (---로 시작해야 함)" >&2
        ERRORS=$((ERRORS + 1))
    fi

    # name 필드 확인
    if grep -q "^name:" "$TARGET/SKILL.md"; then
        echo -e "  ${GREEN}[OK]${NC} name 필드 존재"
    else
        echo -e "  ${RED}[FAIL]${NC} name 필드 없음" >&2
        ERRORS=$((ERRORS + 1))
    fi

    # description 필드 확인
    if grep -q "^description:" "$TARGET/SKILL.md"; then
        echo -e "  ${GREEN}[OK]${NC} description 필드 존재"

        # description에 트리거 키워드 포함 확인
        if grep "^description:" "$TARGET/SKILL.md" | grep -qi "should be used when"; then
            echo -e "  ${GREEN}[OK]${NC} description에 트리거 패턴 포함"
        else
            echo -e "  ${YELLOW}[WARN]${NC} description에 'should be used when' 패턴 권장" >&2
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo -e "  ${RED}[FAIL]${NC} description 필드 없음" >&2
        ERRORS=$((ERRORS + 1))
    fi

    # 본문 단어 수 확인
    WORD_COUNT=$(awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2' "$TARGET/SKILL.md" | wc -w | tr -d ' ')
    if [ "$WORD_COUNT" -gt 0 ]; then
        echo -e "  ${GREEN}[OK]${NC} 본문 존재 (약 ${WORD_COUNT} 단어)"
        if [ "$WORD_COUNT" -gt 3000 ]; then
            echo -e "  ${YELLOW}[WARN]${NC} 본문이 너무 김 (${WORD_COUNT} 단어, 2000 이하 권장)" >&2
            WARNINGS=$((WARNINGS + 1))
        fi
    else
        echo -e "  ${RED}[FAIL]${NC} 본문이 비어있음" >&2
        ERRORS=$((ERRORS + 1))
    fi
fi

# --- 참조 파일 검증 ---
echo ""
echo "📚 참조 파일 검증:"

if [ -d "$TARGET/references" ]; then
    REF_COUNT=$(find "$TARGET/references" -name "*.md" | wc -l | tr -d ' ')
    echo -e "  ${GREEN}[OK]${NC} references/ 디렉토리 존재 (${REF_COUNT}개 파일)"

    # SKILL.md에서 참조된 파일이 실제 존재하는지
    if [ -f "$TARGET/SKILL.md" ]; then
        while IFS= read -r ref; do
            ref_file=$(echo "$ref" | sed 's/.*`references\///' | sed 's/`.*//')
            # 템플릿 변수({file} 등)나 빈 경로는 스킵
            if echo "$ref_file" | grep -qE '^\{|^$|/$'; then
                continue
            fi
            if [ -f "$TARGET/references/$ref_file" ]; then
                echo -e "  ${GREEN}[OK]${NC} 참조됨: references/$ref_file"
            else
                echo -e "  ${RED}[FAIL]${NC} 참조됨 but 없음: references/$ref_file" >&2
                ERRORS=$((ERRORS + 1))
            fi
        done < <(grep -o '`references/[^`]*`' "$TARGET/SKILL.md" 2>/dev/null || true)
    fi
else
    echo -e "  ${YELLOW}[WARN]${NC} references/ 디렉토리 없음" >&2
    WARNINGS=$((WARNINGS + 1))
fi

# --- 스크립트 검증 ---
echo ""
echo "🔧 스크립트 검증:"

if [ -d "$TARGET/scripts" ]; then
    SCRIPT_COUNT=$(find "$TARGET/scripts" -type f | wc -l | tr -d ' ')
    echo -e "  ${GREEN}[OK]${NC} scripts/ 디렉토리 존재 (${SCRIPT_COUNT}개 파일)"

    for script in "$TARGET/scripts"/*; do
        [ -f "$script" ] || continue
        fname=$(basename "$script")

        # shebang 확인
        if head -1 "$script" | grep -q "^#!"; then
            echo -e "  ${GREEN}[OK]${NC} $fname: shebang 존재"
        else
            echo -e "  ${RED}[FAIL]${NC} $fname: shebang 없음" >&2
            ERRORS=$((ERRORS + 1))
        fi

        # 실행 권한 확인
        if [ -x "$script" ]; then
            echo -e "  ${GREEN}[OK]${NC} $fname: 실행 권한 있음"
        else
            echo -e "  ${YELLOW}[WARN]${NC} $fname: 실행 권한 없음 (chmod +x 필요)" >&2
            WARNINGS=$((WARNINGS + 1))
        fi
    done
else
    echo -e "  ${YELLOW}[INFO]${NC} scripts/ 디렉토리 없음 (스크립트 단계 없으면 OK)"
fi

# --- 결과 요약 ---
echo ""
echo "=== 검증 결과 ==="
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}모든 검증 통과!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}통과 (${WARNINGS}개 경고)${NC}"
    exit 0
else
    echo -e "${RED}${ERRORS}개 실패, ${WARNINGS}개 경고${NC}" >&2
    exit 1
fi
