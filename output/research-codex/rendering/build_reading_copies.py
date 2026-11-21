#!/usr/bin/env python3
"""Build offline MathML HTML and vector PDFs; verify every page in Chromium.
Dependencies: pandoc; Python playwright, pymupdf, pillow; an isolated Chromium.
"""
from pathlib import Path
from urllib.parse import unquote, quote
import base64, hashlib, html, json, os, re, subprocess, sys
from playwright.sync_api import sync_playwright
import pymupdf as fitz
from PIL import Image, ImageOps, ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'output/research-codex'
DEST=OUT/'rendered'
QA=OUT/'rendering/qa'
DEST.mkdir(exist_ok=True);QA.mkdir(exist_ok=True)
PROPOSALS=sorted((ROOT/'notes/archive/ideas-codex').glob('v0[1-7]_*.md'))
CSS=(Path(__file__).with_name('reader.css')).read_text()
for token,path in [('__TEXT_FONT__','/System/Library/Fonts/Supplemental/STIXTwoText.ttf'),('__MATH_FONT__','/System/Library/Fonts/Supplemental/STIXTwoMath.otf')]:
 CSS=CSS.replace(token,'data:font/otf;base64,'+base64.b64encode(Path(path).read_bytes()).decode())
CSS+='\n@page diagram{size:A4 landscape;margin:13mm 15mm 16mm}\n@media print{.pipeline-page{page:diagram;break-before:page;break-after:page}.pipeline-page h2{margin-top:0}figure.pipeline img{max-height:155mm;width:auto;max-width:100%}figure.pipeline figcaption{margin-top:5pt}}\n'
STEMS={p.resolve():p.stem for p in PROPOSALS}

def run(args,**kw):
 r=subprocess.run(args,text=True,capture_output=True,check=True,**kw)
 if r.stderr.strip():raise RuntimeError(r.stderr)
 return r.stdout

def transform(node,source):
 if isinstance(node,list):return [transform(x,source) for x in node]
 if not isinstance(node,dict):return node
 node={k:transform(v,source) for k,v in node.items()}
 if node.get('t') in ('Image','Link'):
  target=node['c'][-1][0]
  if not re.match(r'^(https?:|mailto:|#|data:)',target):
   clean=unquote(target.split('#',1)[0]);path=(source.parent/clean).resolve()
   if not path.exists():raise FileNotFoundError(f'{source.name}: {target}')
   if node['t']=='Image':
    if path.name=='training-pipeline.png':path=path.with_suffix('.svg')
    mime='image/svg+xml' if path.suffix=='.svg' else 'image/png'
    node['c'][-1][0]='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
   elif path in STEMS:node['c'][-1][0]=STEMS[path]+'.html'
   else:node['c'][-1][0]=quote(os.path.relpath(path,DEST),safe='/')
 return node

def title_of(p):return p.read_text().splitlines()[0].removeprefix('# ')
records=[]
for i,p in enumerate(PROPOSALS):
 ast=json.loads(run(['pandoc','-f','markdown+tex_math_dollars','-t','json',str(p)]))
 ast=transform(ast,p)
 body=run(['pandoc','-f','json','-t','html5','--mathml'],input=json.dumps(ast))
 body=body.replace('<figure>','<figure class="pipeline">')
 body=re.sub(r'(<h2 id="causal-data-and-training-pipeline">.*?</h2>)\s*(<figure class="pipeline">.*?</figure>)', r'<section class="pipeline-page">\1\2</section>',body,flags=re.S)
 # User-visible navigation never becomes part of the typeset scientific text.
 nav='<a href="index.html">All seven proposals</a><a href="'+p.stem+'.pdf">Download PDF</a>'
 if i:nav+='<a href="'+PROPOSALS[i-1].stem+'.html">Previous version</a>'
 if i<6:nav+='<a href="'+PROPOSALS[i+1].stem+'.html">Next version</a>'
 page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+html.escape(title_of(p))+'</title><style>'+CSS+'</style></head><body><nav aria-label="Proposal navigation">'+nav+'</nav><main>'+body+'</main></body></html>'
 target=DEST/(p.stem+'.html');target.write_text(page)
 records.append({'version':i+1,'source':str(p.relative_to(ROOT)),'html':str(target.relative_to(ROOT)), 'pdf':str((DEST/(p.stem+'.pdf')).relative_to(ROOT)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})

cards=''
for p in PROPOSALS:
 cards+='<section class="card"><h2>Version '+p.name[1:3].lstrip('0')+' · '+html.escape(title_of(p))+'</h2><p><a href="'+p.stem+'.html">Read formatted HTML</a> &nbsp; · &nbsp; <a href="'+p.stem+'.pdf">Open PDF</a> &nbsp; · &nbsp; <a href="'+quote(os.path.relpath(p,DEST),safe='/')+'">Markdown source</a></p></section>'
index='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Seven research proposals · Reading editions</title><style>'+CSS+'</style></head><body><main><h1>Asymmetric mechanics in world models</h1><p>Seven successive research proposals, formatted for dependable reading and printing. Each HTML file contains its own fonts, typeset mathematics, and any figures; it can be read offline.</p><p><a href="'+PROPOSALS[-1].stem+'.html">Start with the final proposal →</a></p><div class="cards">'+cards+'</div><p><a href="../README.md">Research reviews and supporting analysis</a></p><p>Presentation repair only. Earlier scientific claims and revision-specific methods are preserved; these documents describe proposed experiments.</p></main></body></html>'
(DEST/'index.html').write_text(index)

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 context=browser.new_context(viewport={'width':1280,'height':960},device_scale_factor=1)
 # All reading resources are embedded. Verify no network dependency is concealed.
 context.route(re.compile(r'^https?://'),lambda route:route.abort())
 for rec in records:
  page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto((ROOT/rec['html']).as_uri(),wait_until='networkidle')
  page.evaluate('document.fonts.ready')
  checks=page.evaluate('''() => ({
    images:[...document.images].map(i=>({loaded:i.complete&&i.naturalWidth>0,embedded:i.src.startsWith('data:'),width:i.naturalWidth})),
    mathCount:document.querySelectorAll('math').length,
    mathErrors:document.querySelectorAll('merror').length,
    tableRows:[...document.querySelectorAll('table')].map(t=>[...t.rows].map(r=>r.cells.length)),
    bodyOverflow:document.documentElement.scrollWidth>innerWidth+2,
    resourceDependencies:[...document.querySelectorAll('[src],link[rel=stylesheet]')].map(e=>e.src||e.href).filter(v=>!v.startsWith('data:')),
    rawDollars:document.querySelector('main').innerText.includes('$'),
    h1Count:document.querySelectorAll('h1').length
  })''')
  page.screenshot(path=str(QA/f"v{rec['version']:02d}-desktop.png"),full_page=True)
  page.set_viewport_size({'width':390,'height':844})
  page.screenshot(path=str(QA/f"v{rec['version']:02d}-mobile.png"),full_page=True)
  checks['mobileBodyOverflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
  checks['mobileWideElements']=page.evaluate('''() => [...document.querySelectorAll('main *')].filter(e=>{let b=e.getBoundingClientRect();return b.width>0&&(b.right>innerWidth+2||b.left < -2)}).slice(0,12).map(e=>({tag:e.tagName,text:e.textContent.slice(0,90)}))''')
  page.set_viewport_size({'width':1280,'height':960})
  page.pdf(path=str(ROOT/rec['pdf']),print_background=True,prefer_css_page_size=True,display_header_footer=True,
   header_template='<div></div>',footer_template='<div style="font-size:8px;color:#6b7786;width:100%;text-align:center;font-family:Arial">Proposal '+str(rec['version'])+' · <span class="pageNumber"></span> / <span class="totalPages"></span></div>')
  checks['browserErrors']=errors
  rec['browser_checks']=checks
  page.close()
 browser.close()

for rec in records:
 # Make supporting-file links portable with the research folder.
 pdfpath=ROOT/rec['pdf']
 with fitz.open(pdfpath) as pdf:
  link_count=0
  for pdfpage in pdf:
   for link in pdfpage.get_links():
    if link.get('file'):
     target=Path(link['file'])
     if target.is_absolute():
      if not target.exists():raise FileNotFoundError(target)
      link['file']=os.path.relpath(target,pdfpath.parent)
      pdfpage.update_link(link);link_count+=1
  pdf.saveIncr()
 rec['portable_pdf_local_links']=link_count
 doc=fitz.open(pdfpath);pages=[];thumbs=[]
 for i,page in enumerate(doc):
  pix=page.get_pixmap(matrix=fitz.Matrix(1.35,1.35))
  path=QA/f"v{rec['version']:02d}-page-{i+1:02d}.png";pix.save(path)
  text=page.get_text();bad=[]
  for block in page.get_text('dict')['blocks']:
   if 'lines' not in block:continue
   for line in block['lines']:
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     if x0 < -1 or y0 < -1 or x1>page.rect.width+1 or y1>page.rect.height+1:bad.append(span['text'])
  pages.append({'page':i+1,'width_pt':round(page.rect.width,1),'height_pt':round(page.rect.height,1),'text_characters':len(text),'replacement_characters':text.count('\ufffd'),'out_of_page_spans':bad,'raster_images':len(page.get_images()),'preview':str(path.relative_to(ROOT))})
  im=Image.open(path).convert('RGB');im.thumbnail((430,585))
  tile=Image.new('RGB',(470,625),'#e6ebef');tile.paste(im,((470-im.width)//2,25))
  ImageDraw.Draw(tile).text((20,603),f"V{rec['version']} · page {i+1}",fill='#182f45');thumbs.append(tile)
 columns=2;rows=(len(thumbs)+1)//2
 sheet=Image.new('RGB',(columns*470,rows*625),'white')
 for i,im in enumerate(thumbs):sheet.paste(im,((i%columns)*470,(i//columns)*625))
 sheetpath=QA/f"v{rec['version']:02d}-contact-sheet.png";sheet.save(sheetpath)
 rec['pdf_pages']=pages;rec['contact_sheet']=str(sheetpath.relative_to(ROOT))
 doc.close()

failures=[]
for rec in records:
 c=rec['browser_checks']
 for key in ['mathErrors','bodyOverflow','mobileBodyOverflow','rawDollars','browserErrors','resourceDependencies']:
  if c[key]:failures.append({'version':rec['version'],'check':key,'value':c[key]})
 if any(len(set(rows)) != 1 for rows in c['tableRows']):failures.append({'version':rec['version'],'check':'inconsistent table columns'})
 if not c['mathCount']:failures.append({'version':rec['version'],'check':'no rendered mathematics'})
 if not all(i['loaded'] and i['embedded'] for i in c['images']):failures.append({'version':rec['version'],'check':'images'})
 for page in rec['pdf_pages']:
  if page['replacement_characters'] or page['out_of_page_spans']:failures.append({'version':rec['version'],'check':'PDF text bounds/glyphs','page':page['page']})
report={'status':'passed' if not failures else 'failed','renderer':'Pandoc 3.10.2 HTML5 with embedded STIX fonts, native MathML, isolated Chromium PDF export','offline':True,'versions':records,'failures':failures}
(OUT/'rendering/render-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'pdfs':len(records),'pages':sum(len(x['pdf_pages']) for x in records),'failures':failures},indent=2))
