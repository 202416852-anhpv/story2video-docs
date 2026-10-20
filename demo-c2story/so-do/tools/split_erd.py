import re,sys
import os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '02-du-lieu'))
src=open('erd.puml',encoding='utf-8').read()
# entities grouped by package
pk_re=re.compile(r'package "([^"]+)" (#\w+) \{(.*?)\n\}\n',re.S)
ent_re=re.compile(r'    entity (\w+)(?: #\w+)? \{.*?\n    \}\n',re.S)
packages={}
for name,color,body in pk_re.findall(src):
    packages[name]=(color,{m.group(1):m.group(0) for m in ent_re.finditer(body+"\n")})
rels=[l for l in src.splitlines() if re.match(r'^\w+ [|}o.]{2}--[|{o.]{2} \w+',l)]
groups=[
 ('erd-1-tai-khoan-vi','ERD 1 - Tài khoản, ví & thanh toán',['Tài khoản & thanh toán']),
 ('erd-2-du-an-ban-thao','ERD 2 - Dự án & bản thảo',['Dự án & bản thảo']),
 ('erd-3-the-gioi-truyen','ERD 3 - Thế giới truyện',['Thế giới truyện']),
 ('erd-4-sinh-tu-lieu','ERD 4 - Sinh tư liệu: storyboard, ảnh, thuyết minh nguyên văn',['Sinh tư liệu']),
 ('erd-5-trinh-chinh-sua-video','ERD 5 - Trình chỉnh sửa & xuất video',['Trình chỉnh sửa & xuất video']),
 ('erd-6-director-job-ha-tang','ERD 6 - Director, job & hạ tầng',['Director, job & hạ tầng']),
]
for fn,title,pkgs in groups:
    own={e for p in pkgs for e in packages[p][1]}
    used=[r for r in rels if r.split()[0] in own or r.split()[2] in own]
    ext=sorted({x for r in used for x in (r.split()[0],r.split()[2])}-own)
    out=[f'@startuml {fn.replace("-","_")}','\' Sinh tự động từ erd.puml - chỉ sửa erd.puml rồi chạy: python3 so-do/tools/split_erd.py',
         '!theme plain','skinparam defaultFontName "Segoe UI"','skinparam linetype ortho','hide circle','hide empty members',
         f'title {title}','']
    for p in pkgs:
        c,ents=packages[p]
        out.append(f'package "{p}" {c} {{'); out+= [e.rstrip('\n') for e in ents.values()]; out.append('}')
    if ext:
        out.append('package "Bảng thuộc phân hệ khác" #FFFFFF {')
        out+= [f'    entity {e} #EEEEEE' for e in ext]
        out.append('}')
    out+=['']+used+['@enduml','']
    open(fn+'.puml','w',encoding='utf-8').write('\n'.join(out))
    print(fn,len(own),'bảng,',len(ext),'bảng ngoài,',len(used),'quan hệ')
