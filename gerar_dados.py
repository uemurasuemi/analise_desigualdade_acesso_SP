import csv,json,glob,os,zipfile,xml.etree.ElementTree as ET,re,statistics,unicodedata
BASE=os.path.dirname(__file__); SRC='/mnt/data'
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',str(s).upper()) if unicodedata.category(c)!='Mn')
def num(s):
 try:
  s=str(s).strip().replace('%','');return float(s.replace('.','').replace(',','.')) if ',' in s else float(s)
 except:return None
def xrows(path,sheet):
 z=zipfile.ZipFile(path);ss=[]
 if 'xl/sharedStrings.xml' in z.namelist():ss=[''.join(t.text or '' for t in si.iter() if t.tag.endswith('}t')) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
 root=ET.fromstring(z.read('xl/worksheets/sheet%d.xml'%sheet));out=[]
 for row in root.findall('.//{*}sheetData/{*}row'):
  d={}
  for c in row:
   ref=c.get('r','');col=re.match('[A-Z]+',ref)
   if not col:continue
   idx=0
   for ch in col.group():idx=idx*26+ord(ch)-64
   v=c.find('{*}v');t=c.find('{*}is');value=v.text if v is not None else ''.join(t.itertext()) if t is not None else ''
   if c.get('t')=='s' and value:value=ss[int(value)]
   d[idx-1]=value
  if d:out.append(d)
 return out
zones={'NORTE':'Norte','SUL':'Sul','LESTE':'Leste','OESTE':'Oeste'}
def zona(d):
 n=norm(d)
 for k,v in zones.items():
  if re.search(r'\b'+k+r'\b',n):return v
 return 'Outras diretorias'
rows=[]
for path in glob.glob(SRC+'/*.csv'):
 with open(path,'rb') as f:sample=f.read(2500)
 enc='utf-8-sig'
 try:sample.decode(enc)
 except:enc='latin1'
 with open(path,encoding=enc,newline='') as f:
  reader=csv.DictReader(f,delimiter=';' if sample.count(b';')>sample.count(b',') else ',')
  for r in reader:
   ano=int(r.get('ANO_LETIVO') or 0);mun=norm(r.get('NM_MUNICIPIO',''));reg='Capital' if mun=='SAO PAULO' else 'Interior / demais municipios';diret=r.get('NM_DIRETORIA','');z=zona(diret) if reg=='Capital' else 'Fora da capital'
   for i,etapa in [(1,'Etapa 1'),(2,'Etapa 2'),(3,'Etapa 3')]:
    a,b,c=[num(r.get(k+'_'+str(i))) for k in ['APR','REP','ABA']]
    if None in (a,b,c) or a+b+c<95 or a+b+c>105:continue
    rows.append((ano,reg,z,etapa,a,b,c))
print('Registros válidos',len(rows))
from collections import defaultdict
agg=defaultdict(list)
for y,reg,z,et,a,b,c in rows:
 for scope,name in [('Estado','Estado de São Paulo'),('Local',reg)]:agg[(y,name,et)].append((a,b,c))
 if reg=='Capital' and z!='Outras diretorias':agg[(y,z,et)].append((a,b,c))
summary=[]
for (y,g,e),vals in agg.items():
 means=[round(sum(v[j] for v in vals)/len(vals),3) for j in range(3)]
 summary.append(dict(ano=y,grupo=g,etapa=e,aprovacao=means[0],reprovacao=means[1],abandono=means[2],escolas_etapa=len(vals)))
summary.sort(key=lambda x:(x['ano'],x['grupo'],x['etapa']))
# Renda e abandono por distrito são comparáveis na planilha 2025, sem atribuir escolas a distritos.
renda=[]
for path in sorted(glob.glob(SRC+'/*.xlsx')):
 year=int(re.search(r'202[1-5]',os.path.basename(path)).group())
 sheet=4 if year>=2023 else 3
 rr=xrows(path,sheet)
 header=rr[0] if year>=2023 else next((r for r in rr if 'DISTRITO' in norm(' '.join(map(str,r.values())))),{})
 columns={i:norm(v) for i,v in header.items()}
 district=next((i for i,v in columns.items() if v in ('DISTRITO','DISTRITOS')),None)
 inc=next((i for i,v in columns.items() if 'REMUNERACAO MEDIA MENSAL DO EMPREGO FORMAL' in v),None)
 aba=next((i for i,v in columns.items() if 'ABANDONO ESCOLAR NO ENSINO FUNDAMENTAL' in v),None)
 if district is None or inc is None:continue
 for row in rr[1:] if year>=2023 else rr[rr.index(header)+1:]:
  d=row.get(district);v=num(row.get(inc));a=num(row.get(aba)) if aba is not None else None
  if not d or v is None or v<=0:continue
  # Em 2021 valores como 2.868 representam R$ 2.868 (milhares na fonte).
  if year==2021 and v<100:v*=1000
  renda.append(dict(ano=year,distrito=str(d).strip(),renda=round(v,2),abandono_municipal=a))
print('Registros renda',len(renda))
for name,data in [('fluxo.json',summary),('renda.json',renda)]:
 with open(os.path.join(BASE,'dados',name),'w',encoding='utf8') as f:json.dump(data,f,ensure_ascii=False)
