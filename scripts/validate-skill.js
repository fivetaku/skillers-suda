#!/usr/bin/env node
// 생성된 스킬의 구조와 품질을 검증하는 스크립트
// Usage: node validate-skill.js <skill_directory>

const fs = require('fs');
const path = require('path');

// 색상
const RED = '\x1b[0;31m';
const GREEN = '\x1b[0;32m';
const YELLOW = '\x1b[1;33m';
const NC = '\x1b[0m';

let ERRORS = 0;
let WARNINGS = 0;

const args = process.argv.slice(2);
if (args.length < 1) {
  console.error('Usage: node validate-skill.js <skill_directory>');
  console.error('Example: node validate-skill.js skills/my-skill');
  process.exit(1);
}

const TARGET = args[0];

console.log(`=== 스킬 검증: ${TARGET} ===`);
console.log('');

// --- 필수 파일 검증 ---
console.log('파일 구조 검증:');

function checkFile(file, desc) {
  if (fs.existsSync(file) && fs.statSync(file).isFile()) {
    console.log(`  ${GREEN}[OK]${NC} ${desc}`);
  } else {
    process.stderr.write(`  ${RED}[FAIL]${NC} ${desc}: ${file}\n`);
    ERRORS++;
  }
}

checkFile(path.join(TARGET, 'SKILL.md'), 'SKILL.md 존재');

// --- SKILL.md Frontmatter 검증 ---
console.log('');
console.log('SKILL.md 검증:');

const skillMdPath = path.join(TARGET, 'SKILL.md');
if (fs.existsSync(skillMdPath) && fs.statSync(skillMdPath).isFile()) {
  const content = fs.readFileSync(skillMdPath, 'utf8');
  const lines = content.split('\n');

  // frontmatter 존재 확인
  if (lines[0] && lines[0].startsWith('---')) {
    console.log(`  ${GREEN}[OK]${NC} frontmatter 존재`);
  } else {
    process.stderr.write(`  ${RED}[FAIL]${NC} frontmatter 없음 (---로 시작해야 함)\n`);
    ERRORS++;
  }

  // name 필드 확인
  if (lines.some(l => /^name:/.test(l))) {
    console.log(`  ${GREEN}[OK]${NC} name 필드 존재`);
  } else {
    process.stderr.write(`  ${RED}[FAIL]${NC} name 필드 없음\n`);
    ERRORS++;
  }

  // description 필드 확인
  const descLine = lines.find(l => /^description:/.test(l));
  if (descLine) {
    console.log(`  ${GREEN}[OK]${NC} description 필드 존재`);

    if (/should be used when/i.test(descLine)) {
      console.log(`  ${GREEN}[OK]${NC} description에 트리거 패턴 포함`);
    } else {
      process.stderr.write(`  ${YELLOW}[WARN]${NC} description에 'should be used when' 패턴 권장\n`);
      WARNINGS++;
    }
  } else {
    process.stderr.write(`  ${RED}[FAIL]${NC} description 필드 없음\n`);
    ERRORS++;
  }

  // 본문 단어 수 확인 (frontmatter 이후 내용)
  // frontmatter는 --- 사이에 있음: 첫 번째 ---와 두 번째 --- 사이
  const parts = content.split(/^---$/m);
  // parts[0] = 첫 --- 이전 (비어있거나 없음)
  // parts[1] = frontmatter 내용
  // parts[2] = 본문
  let bodyText = '';
  if (parts.length >= 3) {
    bodyText = parts.slice(2).join('---');
  }
  const wordCount = bodyText.split(/\s+/).filter(Boolean).length;

  if (wordCount > 0) {
    console.log(`  ${GREEN}[OK]${NC} 본문 존재 (약 ${wordCount} 단어)`);
    if (wordCount > 3000) {
      process.stderr.write(`  ${YELLOW}[WARN]${NC} 본문이 너무 김 (${wordCount} 단어, 2000 이하 권장)\n`);
      WARNINGS++;
    }
  } else {
    process.stderr.write(`  ${RED}[FAIL]${NC} 본문이 비어있음\n`);
    ERRORS++;
  }
}

// --- 참조 파일 검증 ---
console.log('');
console.log('참조 파일 검증:');

const referencesDir = path.join(TARGET, 'references');
if (fs.existsSync(referencesDir) && fs.statSync(referencesDir).isDirectory()) {
  function countMdFiles(dir) {
    let count = 0;
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.isFile() && entry.name.endsWith('.md')) {
        count++;
      } else if (entry.isDirectory()) {
        count += countMdFiles(path.join(dir, entry.name));
      }
    }
    return count;
  }
  const refCount = countMdFiles(referencesDir);
  console.log(`  ${GREEN}[OK]${NC} references/ 디렉토리 존재 (${refCount}개 파일)`);

  if (fs.existsSync(skillMdPath) && fs.statSync(skillMdPath).isFile()) {
    const content = fs.readFileSync(skillMdPath, 'utf8');
    const refMatches = content.match(/`references\/[^`]*`/g) || [];

    for (const match of refMatches) {
      // extract the path between backticks: `references/foo.md` -> foo.md
      const inner = match.replace(/^`references\//, '').replace(/`$/, '');
      // skip template variables or empty or trailing slash
      if (/^\{|^$|\//.test(inner)) {
        continue;
      }
      const refFile = path.join(referencesDir, inner);
      if (fs.existsSync(refFile) && fs.statSync(refFile).isFile()) {
        console.log(`  ${GREEN}[OK]${NC} 참조됨: references/${inner}`);
      } else {
        process.stderr.write(`  ${RED}[FAIL]${NC} 참조됨 but 없음: references/${inner}\n`);
        ERRORS++;
      }
    }
  }
} else {
  process.stderr.write(`  ${YELLOW}[WARN]${NC} references/ 디렉토리 없음\n`);
  WARNINGS++;
}

// --- 스크립트 검증 ---
console.log('');
console.log('스크립트 검증:');

const scriptsDir = path.join(TARGET, 'scripts');
if (fs.existsSync(scriptsDir) && fs.statSync(scriptsDir).isDirectory()) {
  const entries = fs.readdirSync(scriptsDir, { withFileTypes: true });
  const scripts = entries.filter(e => e.isFile());

  console.log(`  ${GREEN}[OK]${NC} scripts/ 디렉토리 존재 (${scripts.length}개 파일)`);

  for (const entry of scripts) {
    const scriptPath = path.join(scriptsDir, entry.name);
    const firstLine = fs.readFileSync(scriptPath, 'utf8').split('\n')[0] || '';

    if (firstLine.startsWith('#!')) {
      console.log(`  ${GREEN}[OK]${NC} ${entry.name}: shebang 존재`);
    } else {
      process.stderr.write(`  ${RED}[FAIL]${NC} ${entry.name}: shebang 없음\n`);
      ERRORS++;
    }

    // 실행 권한 확인 (Unix only)
    try {
      const stat = fs.statSync(scriptPath);
      const isExecutable = (stat.mode & 0o111) !== 0;
      if (isExecutable) {
        console.log(`  ${GREEN}[OK]${NC} ${entry.name}: 실행 권한 있음`);
      } else {
        process.stderr.write(`  ${YELLOW}[WARN]${NC} ${entry.name}: 실행 권한 없음 (chmod +x 필요)\n`);
        WARNINGS++;
      }
    } catch (e) {
      // Windows — skip permission check
    }
  }
} else {
  console.log(`  [INFO] scripts/ 디렉토리 없음 (스크립트 단계 없으면 OK)`);
}

// --- 결과 요약 ---
console.log('');
console.log('=== 검증 결과 ===');
if (ERRORS === 0 && WARNINGS === 0) {
  console.log(`${GREEN}모든 검증 통과!${NC}`);
  process.exit(0);
} else if (ERRORS === 0) {
  console.log(`${YELLOW}통과 (${WARNINGS}개 경고)${NC}`);
  process.exit(0);
} else {
  process.stderr.write(`${RED}${ERRORS}개 실패, ${WARNINGS}개 경고${NC}\n`);
  process.exit(1);
}
