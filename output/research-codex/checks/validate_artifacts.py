#!/usr/bin/env python3
"""Validate research-package structure, arithmetic, local links and source integrity."""
from pathlib import Path
from urllib.parse import unquote
import argparse
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/ideas-codex'

def check_sources(manifest, source_dir):
    """Verify supplied PDFs only when their directory is explicitly provided."""
    if source_dir is None:
        return 'not_checked', []
    errors = []
    for source in manifest['sources']:
        relative = Path(source['relative_path'])
        path = source_dir / relative
        if not path.is_file():
            errors.append(f'Source missing: {relative}')
        elif hashlib.sha256(path.read_bytes()).hexdigest() != source['sha256']:
            errors.append(f'Source changed: {relative}')
    return ('failed' if errors else 'passed'), errors

def check(source_dir=None):
    errors, records, scores = [], [], []
    versions = sorted(DOCS.glob('v0[1-7]_*.md'))
    if len(versions) != 7:
        errors.append(f'Expected seven canonical versions, found {len(versions)}')
    seen = set()
    for p in versions:
        n = int(p.name[1:3])
        if n in seen:
            errors.append(f'Duplicate version {n}')
        seen.add(n)
        text = p.read_text()
        for required in (f'Version {n}', '## Abstract', 'Status:'):
            if required not in text:
                errors.append(f'{p.name}: missing {required}')
        records.append({'version':n,'path':str(p.relative_to(ROOT)),
                        'word_count':len(text.split()),
                        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    if len({x['sha256'] for x in records}) != len(records):
        errors.append('Two canonical versions have identical content')
    for n in range(8):
        matches = list(OUT.glob('review-v00-original.md' if n == 0 else f'review-v{n:02d}.md'))
        if len(matches) != 1:
            errors.append(f'Missing or duplicate review for version {n}')
            continue
        p=matches[0]
        rows=[]
        for line in p.read_text().splitlines():
            if not line.startswith('|'):
                continue
            cells=[x.strip().replace('**','') for x in line.strip('|').split('|')]
            if len(cells) >= 3 and re.fullmatch(r'\d+(?:\.\d+)?%',cells[1]) and re.fullmatch(r'\d+(?:\.\d+)?',cells[2]):
                rows.append((cells[0],float(cells[1][:-1]),float(cells[2])))
        if len(rows) < 10:
            errors.append(f'{p.name}: fewer than ten score rows')
            continue
        # Each complete table is validated; a final addendum may retain its original table.
        tables=[rows[i:i+10] for i in range(0,len(rows),10)]
        for table in tables:
            if len(table)!=10 or abs(sum(x[1] for x in table)-100)>1e-9:
                errors.append(f'{p.name}: invalid rubric weights')
        total=sum(w*s/5 for _,w,s in tables[-1])
        claims=re.findall(r'\*\*Weighted total\*\*[^\n]*?\*\*([0-9.]+)/100\*\*',p.read_text())
        if claims and abs(float(claims[-1])-total)>0.051:
            errors.append(f'{p.name}: reported {claims[-1]} but calculated {total:.1f}')
        scores.append({'version':n,'design_score':round(total,1),'dimensions':[
            {'name':name,'weight':w,'score_out_of_5':s} for name,w,s in tables[-1]]})
    # Handle ordinary Markdown destinations including one level of parentheses.
    link_re=re.compile(r'!?\[[^\]]*\]\(([^)\n]*(?:\([^)\n]*\)[^)\n]*)*)\)')
    checked=0
    docs=versions+list(OUT.glob('*.md'))+list((OUT/'figures').glob('*.md'))+list((OUT/'checks').glob('*.md'))+list((OUT/'rendering').glob('*.md'))
    for p in docs:
        for match in link_re.finditer(p.read_text()):
            target=match.group(1).strip().strip('<>')
            if target.startswith(('http:','https:','mailto:','#')):
                continue
            target=unquote(target.split('#',1)[0])
            if not target:
                continue
            q=Path(target) if target.startswith('/') else p.parent/target
            checked+=1
            if q.resolve() == (OUT/'artifact-validation.json').resolve():
                continue  # This check creates its own linked report below.
            if not q.exists():
                errors.append(f'{p.relative_to(ROOT)}: missing local link {target}')
    audit=json.loads((OUT/'rendering/render-audit.json').read_text())
    if audit['status'] != 'passed' or len(audit['versions']) != 7:
        errors.append('Rendering audit failed or does not cover all seven versions')
    for rec in audit['versions']:
        source=ROOT/rec['source']
        if not source.is_file():
            errors.append(f'Rendered source missing: {source}')
        elif hashlib.sha256(source.read_bytes()).hexdigest()!=rec['source_sha256']:
            errors.append(f'Rendered copy is stale: {source.name}')
        for field in ('html','pdf'):
            if not (ROOT/rec[field]).is_file():
                errors.append(f'Missing rendered {field}: {source.name}')
    manifest=json.loads((OUT/'source-manifest.json').read_text())
    source_status, source_errors = check_sources(manifest, source_dir)
    errors.extend(source_errors)
    svg=ET.parse(OUT/'figures/training-pipeline.svg')
    tags={e.tag.split('}')[-1] for e in svg.iter()}
    if not {'title','desc'} <= tags:
        errors.append('SVG lacks accessibility title or description')
    if {'script','image','foreignObject'} & tags:
        errors.append('SVG includes script, raster image, or foreign content')
    result={'status':'passed' if not errors else 'failed','canonical_proposals':records,
            'scores':scores,'local_links_checked':checked,'source_pdf_verification':source_status,
            'svg_is_original_vector_with_accessibility_metadata':not any('SVG' in x for x in errors),
            'scope':'Document consistency and source hashes only. No neural model or human experiment was executed.',
            'errors':errors}
    (OUT/'artifact-validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'versions':len(versions),'reviews':len(scores),'local_links':checked,'source_pdf_verification':source_status,'errors':errors},indent=2))
    return 1 if errors else 0

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, help='directory containing the three supplied source PDFs')
    raise SystemExit(check(parser.parse_args().source_dir))
