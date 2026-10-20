"""Sinh nháp product backlog (tai-lieu/11-product-backlog.md) từ đặc tả use case.

- Mỗi use case (gốc hoặc con) thuộc MVP = một story; Gherkin sinh từ Tiền điều kiện,
  Luồng chính, Hậu điều kiện và từng nhánh Luồng thay thế / ngoại lệ (QĐ-11, QĐ-12).
- Use case sau MVP gom thành epic theo phân hệ, mỗi epic một dòng.
Nhóm rà lại Gherkin rồi chép sang GitHub Projects; không sửa tay file sinh ra.

Chạy trong demo-c2story/:  python3 tools/gen_backlog.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
UC_DIR = os.path.join(ROOT, 'tai-lieu', '03-dac-ta-use-case')
OUT = os.path.join(ROOT, 'tai-lieu', '11-product-backlog.md')
PHASES = ['P0', 'P1', 'P2', 'P3']


def clean(t):
    t = re.sub(r'\*\*|`', '', t).strip()
    return t.rstrip('.')


def parse(path):
    text = open(path, encoding='utf-8').read()
    module = text.split('\n', 1)[0].lstrip('# ').strip()
    ucs = []
    parts = re.split(r'^(?=#{2,3} UC-\d\d\.\d\d[a-z]? )', text, flags=re.M)
    for p in parts[1:]:
        m = re.match(r'#{2,3} UC-(\d\d\.\d\d[a-z]?) (.+)', p)
        uc = {'id': m.group(1), 'name': m.group(2).strip(), 'module': module, 'file': os.path.basename(path)}
        for k, v in re.findall(r'^\| ([^|]+?) \| (.+) \|$', p, re.M):
            uc[k.strip()] = v.strip()
        main = re.search(r'\*\*Luồng chính\*\*\n(.*?)(?:\n\n|\Z)', p, re.S)
        uc['main'] = [clean(re.sub(r'^\d+\. ', '', l)) for l in main.group(1).split('\n') if re.match(r'^\d+\. ', l)] if main else []
        alt = re.search(r'\*\*Luồng thay thế / ngoại lệ\*\*\n(.*?)(?:\n\n|\Z)', p, re.S)
        uc['alt'] = []
        if alt:
            for l in alt.group(1).split('\n'):
                mm = re.match(r'^- \*\*\\?(\*?[\w]+)\.\*\* (.+)$', l)
                if mm:
                    uc['alt'].append((mm.group(1).replace('\\', ''), clean(mm.group(2))))
        ucs.append(uc)
    return ucs


def actor(uc):
    a = uc.get('Tác nhân chính') or uc.get('Tác nhân chính / phụ') or uc.get('Tác nhân') or 'Người dùng'
    return clean(a.split('/')[0]).replace('Editor', 'Owner')


def split_success(post):
    post = clean(post)
    m = re.search(r'Thành công:\s*(.+?)(?:\s*Tối thiểu:\s*(.+))?$', post)
    return (m.group(1).strip(' .'), (m.group(2) or '').strip(' .')) if m else (post, '')


def gherkin(uc):
    ok, _ = split_success(uc.get('Hậu điều kiện', ''))
    pre = clean(uc.get('Tiền điều kiện', '—'))
    lines = [f'Feature: UC-{uc["id"]} {uc["name"]}']
    if pre and pre != '—':
        lines += ['  Background:', f'    Given {pre}']
    steps = uc['main'] or [clean(uc.get('Mô tả', ''))]
    lines += ['', '  Scenario: Luồng chính']
    for i, s in enumerate(steps):
        lines.append(f'    {"When" if i == 0 else "And"} {s}')
    lines.append(f'    Then {ok}')
    for code, txt in uc['alt']:
        cond, _, outcome = txt.partition(':')
        lines += ['', f'  Scenario: {code} {cond.strip()[:80]}']
        step = int(re.match(r'\d+', code).group()) if re.match(r'\d+', code) else None
        if step and step > 1 and len(uc['main']) >= step - 1:
            lines.append(f'    Given luồng chính đã tới bước {step}')
        lines.append(f'    When {cond.strip()}')
        lines.append(f'    Then {outcome.strip() or "hệ thống xử lý như mô tả"}')
    return '\n'.join(lines)


def main():
    ucs = [u for f in sorted(glob.glob(os.path.join(UC_DIR, 'm*.md'))) for u in parse(f)]
    mvp = [u for u in ucs if not u['Giai đoạn'].startswith('Sau')]
    post = [u for u in ucs if u['Giai đoạn'].startswith('Sau')]
    out = ['# 11 — Product backlog (nháp)', '',
           '> **Sinh tự động** bởi `tools/gen_backlog.py` từ [đặc tả use case](03-dac-ta-use-case/00-muc-luc.md); không sửa tay. '
           'Sửa đặc tả rồi chạy lại `python3 tools/gen_backlog.py`.',
           '> Quy ước (QĐ-10..12): mỗi use case thuộc MVP (gốc hoặc con) là một story; Gherkin là **bản nháp** sinh từ tiền điều kiện, '
           'luồng chính, hậu điều kiện và từng nhánh thay thế, nhóm rà lại trước khi chép sang GitHub Projects. '
           'Story point để trống, điền sau planning poker. Use case sau MVP gom thành epic ở §3.', '',
           '## 1. Tổng hợp', '', '| Giai đoạn | Số story | Use case |', '|---|---|---|']
    for ph in PHASES:
        items = [u for u in mvp if u['Giai đoạn'].split()[0] == ph]
        out.append(f'| {ph} | {len(items)} | ' + ', '.join(f'UC-{u["id"]}' for u in items) + ' |')
    out += [f'| **MVP** | **{len(mvp)}** | |', f'| Sau MVP (epic) | {len(post)} use case | §3 |', '',
            '## 2. Story thuộc MVP', '']
    for ph in PHASES:
        out += [f'### Giai đoạn {ph}', '']
        for u in [u for u in mvp if u['Giai đoạn'].split()[0] == ph]:
            sid = 'ST-' + u['id'].replace('.', '-')
            cut = ' ' + ' '.join(re.findall(r'✂\d', u['Giai đoạn'])) if '✂' in u['Giai đoạn'] else ''
            out += [f'#### {sid} {u["name"]}{cut}', '',
                    '| Mục | Nội dung |', '|---|---|',
                    f'| Story | Là **{actor(u)}**, tôi muốn {u["name"][0].lower() + u["name"][1:]} |',
                    f'| Mô tả | {clean(u.get("Mô tả", "—"))} |',
                    f'| Use case | [UC-{u["id"]}](03-dac-ta-use-case/{u["file"]}#uc-{u["id"].replace(".", "")}) · {u["module"]} |',
                    f'| Giai đoạn | {u["Giai đoạn"]} |',
                    f'| Truy vết | {u.get("Truy vết", "—")} |',
                    '| Story point | |', '',
                    '```gherkin', gherkin(u), '```', '']
    out += ['## 3. Epic sau MVP', '', 'Mỗi epic một dòng; tách story khi được đưa vào kế hoạch.', '',
            '| Epic | Phân hệ | Use case | Số UC |', '|---|---|---|---|']
    mods = {}
    for u in post:
        mods.setdefault(u['module'], []).append(u)
    for i, (mod, items) in enumerate(mods.items(), 1):
        names = '; '.join(f'UC-{u["id"]} {u["name"]}' for u in items)
        out.append(f'| EP-{i:02d} | {mod} | {names} | {len(items)} |')
    out.append('')
    open(OUT, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'{len(mvp)} story MVP, {len(post)} UC sau MVP -> {os.path.relpath(OUT, ROOT)}')


if __name__ == '__main__':
    main()
