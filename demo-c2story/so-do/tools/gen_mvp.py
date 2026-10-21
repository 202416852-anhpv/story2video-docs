"""Sinh sơ đồ MVP và tô xám phần sau MVP trong sơ đồ đầy đủ.

Nguồn duy nhất:
- Giai đoạn use case: dòng "| Giai đoạn | ... |" trong tai-lieu/03-dac-ta-use-case/m*.md
- Bảng sau MVP: các dòng "| `bảng` *(sau MVP)* |" trong tai-lieu/04-mo-hinh-du-lieu.md

Chạy trong demo-c2story/:  python3 so-do/tools/gen_mvp.py
Kết quả: so-do/mvp/01-use-case/phan-ra/*-mvp.puml, so-do/mvp/02-du-lieu/erd-mvp.puml,
so-do/mvp/02-du-lieu/domain-class-mvp.puml, bản MVP của sơ đồ có đánh dấu '@sau-mvp / '@mvp
(03-kien-truc, 04-tuan-tu, 05-hoat-dong) và mọi sơ đồ 07-tich-hop-ai trừ seq-ai-tts-vbee; sơ đồ đầy đủ tương ứng được tô xám (#DDDDDD) phần sau MVP.
Các sơ đồ MVP khác (tổng quan, tuần tự, trạng thái...) viết tay trong so-do/mvp/.
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
GRAY = ' #DDDDDD'


def path(*p):
    return os.path.join(ROOT, *p)


def uc_phases():
    ph = {}
    for f in glob.glob(path('tai-lieu', '03-dac-ta-use-case', 'm*.md')):
        cur = None
        for line in open(f, encoding='utf-8'):
            m = re.match(r'^#{2,3} UC-(\d\d\.\d\d[a-z]?) ', line)
            if m:
                cur = m.group(1)
            m = re.match(r'^\| Giai đoạn \| (.+?) \|', line)
            if m and cur:
                ph[cur] = m.group(1)
    return ph


def post_mvp_tables():
    s = open(path('tai-lieu', '04-mo-hinh-du-lieu.md'), encoding='utf-8').read()
    return set(re.findall(r'^\| `(\w+)` \*\(sau MVP\)\*', s, re.M))


def drop_aliases(src, dropped):
    """Bỏ khai báo, quan hệ và note gắn với các alias trong `dropped`."""
    out, skip_note = [], False
    for line in src.split('\n'):
        if skip_note:
            skip_note = line.strip() != 'end note'
            continue
        m = re.match(r'\s*note \w+ of (\w+)', line)
        if m and m.group(1) in dropped:
            skip_note = True
            continue
        words = set(re.findall(r'\b\w+\b', line))
        if re.match(r'\s*usecase ".*" as (\w+)', line) and re.match(r'\s*usecase ".*" as (\w+)', line).group(1) in dropped:
            continue
        if re.match(r'^\w+ .*(--|\.\.).*\w+', line) and words & dropped:
            continue
        out.append(line)
    # bỏ actor/rectangle ngoài không còn quan hệ nào
    body = '\n'.join(out)
    rels = [l for l in out if re.match(r'^\w+ \S*(--|\.\.)\S* \w+', l)]
    used = {w for l in rels for w in re.findall(r'\b\w+\b', l)}
    res = []
    for l in out:
        m = re.match(r'^(actor|rectangle) ".*" as (\w+)\s*$', l)
        if m and m.group(2) not in used:
            continue
        res.append(l)
    return '\n'.join(res)


def use_cases(ph):
    files = sorted(glob.glob(path('so-do', '01-use-case', 'phan-ra', '*.puml')))
    os.makedirs(path('so-do', 'mvp', '01-use-case', 'phan-ra'), exist_ok=True)
    for f in files:
        src = open(f, encoding='utf-8').read().replace(GRAY, '')
        src = re.sub(r'\ncaption .*', '', src)
        alias = {m.group(2): m.group(1) for m in re.finditer(r'usecase "UC-(\d\d\.\d\d[a-z]?)\\n[^"]*" as (\w+)', src)}
        post = {a for a, u in alias.items() if ph[u].startswith('Sau')}
        # bản đầy đủ: tô xám
        full = re.sub(r'(usecase "UC-(\d\d\.\d\d[a-z]?)\\n[^"]*" as \w+)',
                      lambda m: m.group(1) + (GRAY if ph[m.group(2)].startswith('Sau') else ''), src)
        if post:
            full = full.replace('\n@enduml', '\ncaption Nền xám: use case sau MVP (bản chỉ gồm MVP: so-do/mvp/)\n@enduml')
        open(f, 'w', encoding='utf-8').write(full)
        # bản MVP
        if len(post) == len(alias):
            print('bỏ qua (không có UC MVP):', os.path.basename(f))
            continue
        mvp = drop_aliases(src, post)
        mvp = re.sub(r'@startuml (\w+)', r'@startuml \1_MVP', mvp, count=1)
        mvp = re.sub(r'^title (.+)$', r'title \1 (MVP)', mvp, count=1, flags=re.M)
        mvp = mvp.replace('!theme plain', "' Sinh tự động bởi so-do/tools/gen_mvp.py - không sửa tay\n!theme plain", 1)
        out = path('so-do', 'mvp', '01-use-case', 'phan-ra', os.path.basename(f).replace('.puml', '-mvp.puml'))
        open(out, 'w', encoding='utf-8').write(mvp)
        print(os.path.basename(out), len(alias) - len(post), 'UC MVP /', len(alias))


def erd(post):
    f = path('so-do', '02-du-lieu', 'erd.puml')
    src = open(f, encoding='utf-8').read().replace(GRAY + ' {', ' {')
    full = re.sub(r'^(    entity (\w+)) \{', lambda m: m.group(1) + (GRAY if m.group(2) in post else '') + ' {', src, flags=re.M)
    full = re.sub(r'\ncaption .*', '', full)
    full = full.replace('\n@enduml', '\ncaption Nền xám: bảng sau MVP (ERD chỉ gồm MVP: so-do/mvp/02-du-lieu/erd-mvp.puml)\n@enduml')
    open(f, 'w', encoding='utf-8').write(full)
    mvp = re.sub(r'    entity (\w+) \{.*?\n    \}\n', lambda m: '' if m.group(1) in post else m.group(0), src, flags=re.S)
    mvp = '\n'.join(l for l in mvp.split('\n')
                    if not (re.match(r'^\w+ \S*--\S* \w+', l) and {l.split()[0], l.split()[2]} & post))
    mvp = mvp.replace('@startuml ERD_StoryStudio', "@startuml ERD_StoryStudio_MVP\n' Sinh tự động bởi so-do/tools/gen_mvp.py - không sửa tay\ntitle ERD - phạm vi MVP", 1)
    os.makedirs(path('so-do', 'mvp', '02-du-lieu'), exist_ok=True)
    open(path('so-do', 'mvp', '02-du-lieu', 'erd-mvp.puml'), 'w', encoding='utf-8').write(mvp)
    total = len(re.findall(r'^    entity \w+', src, re.M))
    print('erd-mvp.puml', total - len(post), 'bảng MVP /', total)


# Lớp miền chỉ dùng sau MVP (khớp các bảng *(sau MVP)* ở 04)
POST_CLASSES = {'Subscription', 'LibraryAsset', 'Archive', 'Note', 'ChapterRule',
                'DirectorPlan', 'DirectorMessage', 'ToolProposal', 'AssetVariant'}


def domain():
    f = path('so-do', '02-du-lieu', 'domain-class.puml')
    src = open(f, encoding='utf-8').read().replace(GRAY, '')
    cls = r'^(    (?:abstract )?class (\w+)(?: <<\w+>>)?)'
    full = re.sub(cls + r'( \{|$)', lambda m: m.group(1) + (GRAY if m.group(2) in POST_CLASSES else '') + m.group(3), src, flags=re.M)
    open(f, 'w', encoding='utf-8').write(full)
    mvp = re.sub(r'^    (?:abstract )?class (\w+)(?: <<\w+>>)?(?: \{.*?\n    \})?\n',
                 lambda m: '' if m.group(1) in POST_CLASSES else m.group(0), src, flags=re.M | re.S)
    mvp = '\n'.join(l for l in mvp.split('\n')
                    if not (re.match(r'^\w+ ', l) and set(re.findall(r'\b[A-Z]\w+\b', l.split(':')[0])) & POST_CLASSES))
    mvp = '\n'.join(l for l in mvp.split('\n') if '(sau MVP)' not in l)
    mvp = re.sub(r'@startuml (\w+)', r"@startuml \1_MVP\n' Sinh tự động bởi so-do/tools/gen_mvp.py - không sửa tay", mvp, count=1)
    mvp = mvp.replace('  • Nền xám: lớp chỉ dùng sau MVP\n', '')
    mvp = mvp.replace('  • LibraryAsset được sao chép thành StoryAsset khi thêm vào dự án\n', '')
    mvp = re.sub(r'^(title .+)$', r'\1 (MVP)', mvp, count=1, flags=re.M)
    open(path('so-do', 'mvp', '02-du-lieu', 'domain-class-mvp.puml'), 'w', encoding='utf-8').write(mvp)
    print('domain-class-mvp.puml bỏ', len(POST_CLASSES), 'lớp sau MVP')


def marked(folder, all_files=False, skip_files=()):
    """Sơ đồ có đánh dấu (tuần tự; gói, lớp thiết kế): dòng giữa '@sau-mvp và '@/sau-mvp chỉ ở bản đầy đủ; dòng "'@mvp …" chỉ ở bản MVP.
    all_files: sinh bản MVP cho mọi sơ đồ trong thư mục, trừ `skip_files` (sơ đồ toàn bộ sau MVP)."""
    d = path('so-do', folder)
    os.makedirs(path('so-do', 'mvp', folder), exist_ok=True)
    for name in sorted(os.listdir(d)):
        if not name.endswith('.puml') or name in skip_files:
            continue
        src = open(os.path.join(d, name), encoding='utf-8').read()
        if not all_files and "'@sau-mvp" not in src and "'@mvp " not in src:
            continue
        out, skip = [], False
        for l in src.split('\n'):
            if l.strip() == "'@sau-mvp":
                skip = True
            elif l.strip() == "'@/sau-mvp":
                skip = False
            elif l.lstrip().startswith("'@mvp "):
                out.append(l.replace("'@mvp ", '', 1))
            elif not skip:
                out.append(l)
        mvp = re.sub(r'@startuml (\w+)', r"@startuml \1_MVP\n' Sinh tự động bởi so-do/tools/gen_mvp.py - không sửa tay", '\n'.join(out), count=1)
        mvp = mvp.replace('!include ../', '!include ../../')
        mvp = mvp.replace('!include _style-', '!include ../../' + folder + '/_style-')
        open(path('so-do', 'mvp', folder, name.replace('.puml', '-mvp.puml')), 'w', encoding='utf-8').write(mvp)
        print(name, '→ bản MVP')


if __name__ == '__main__':
    use_cases(uc_phases())
    erd(post_mvp_tables())
    domain()
    marked('03-kien-truc')
    marked('04-tuan-tu')
    marked('05-hoat-dong')
    marked('07-tich-hop-ai', all_files=True, skip_files={'seq-ai-tts-vbee.puml'})
