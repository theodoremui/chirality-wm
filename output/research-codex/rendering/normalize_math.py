#!/usr/bin/env python3
"""One-time, idempotent typographic conversion; numerical/scientific claims unchanged."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[3]

EXACT={
 'ceil((1.645s_D/(δ/4))²)':r'\left\lceil\left(\frac{1.645s_D}{\delta/4}\right)^2\right\rceil',
 'ceil((1.645s_D/ε)²)':r'\left\lceil\left(\frac{1.645s_D}{\epsilon}\right)^2\right\rceil',
 'ceil((1.96 s/ε)²)':r'\left\lceil\left(\frac{1.96s}{\epsilon}\right)^2\right\rceil',
 'n=ceil((1.96s_D/ε)²)':r'n=\left\lceil\left(\frac{1.96s_D}{\epsilon}\right)^2\right\rceil',
 'sqrt(150)':r'\sqrt{150}',
 '(m_+−m_−)²/4':r'\frac{(m_+-m_-)^2}{4}',
 'candidate MSE − 0.95 × comparator MSE':r'\operatorname{MSE}_{\mathrm{candidate}}-0.95\operatorname{MSE}_{\mathrm{comparator}}',
 'RMSE_C,delay0−RMSE_B,delay0<0.02 N·s':r'\operatorname{RMSE}_{C,0}-\operatorname{RMSE}_{B,0}<0.02\,\mathrm{N\,s}',
 'CRPS_C−CRPS_B<0.01 N·s':r'\operatorname{CRPS}_C-\operatorname{CRPS}_B<0.01\,\mathrm{N\,s}',
 'τ dq_L/dt=a+u−q_L':r'\tau\frac{dq_L}{dt}=a+u-q_L',
 'τ dq_R/dt=a−u−q_R':r'\tau\frac{dq_R}{dt}=a-u-q_R',
 'τ dq_s/dt=φ_α(a±u)−q_s':r'\tau\frac{dq_s}{dt}=\phi_\alpha(a\pm u)-q_s',
 'φ_α(v)=tanh(αv)/tanh(α)':r'\phi_\alpha(v)=\frac{\tanh(\alpha v)}{\tanh(\alpha)}',
}

def mathify(s):
 if s in EXACT:return EXACT[s]
 s=s.replace('{',r'\{').replace('}',r'\}')
 s=s.replace('|b|',r'\lvert b\rvert').replace('|u|',r'\lvert u\rvert')
 s=s.replace('|',r'\mid ')
 for old,new in {'N·s/m':r'\mathrm{N\,s/m}','N·s':r'\mathrm{N\,s}','N/m':r'\mathrm{N/m}','m/s':r'\mathrm{m/s}','kg':r'\mathrm{kg}'}.items():s=s.replace(old,new)
 s=re.sub(r'(?<=[0-9\]])\s+(N|m|s)\b',lambda m:r'\,\mathrm{'+m[1]+'}',s)
 for old,new in [('x_end',r'x_{\mathrm{end}}'),('v_end',r'v_{\mathrm{end}}'),('F_average',r'F_{\mathrm{average}}'),('F_total',r'F_{\mathrm{total}}'),('C_odd',r'C_{\mathrm{odd}}'),('R_candidate',r'R_{\mathrm{candidate}}'),('R_comparator',r'R_{\mathrm{comparator}}')]:s=s.replace(old,new)
 s=s.replace("q'_L",r'\dot q_L').replace("q'_R",r'\dot q_R').replace("x''",r'\ddot x').replace("x'",r'\dot x')
 for old,new in {'τ':r'\tau ','φ':r'\phi ','α':r'\alpha ','μ':r'\mu ','σ':r'\sigma ','δ':r'\delta ','ε':r'\epsilon ','Σ':r'\sum ','∈':r'\in ','∝':r'\propto ','±':r'\pm ','≤':r'\le ','−':'-','×':r'\times ','…':r'\ldots ','⁻⁴':'^{-4}','⁻³':'^{-3}','²':'^2'}.items():s=s.replace(old,new)
 # A macro in a subscript is one TeX atom; no unintended raw underscores remain.
 s=re.sub(r'\b(exp|tanh|log)\b',lambda m:'\\'+m[1]+' ',s)
 s=s.replace('Normal',r'\mathcal{N}').replace(' ~ ',r'\sim ')
 return s.replace(r't_\{k+1\}',r't_{k+1}').strip()

changes=[]
for p in sorted((ROOT/'docs/ideas-codex').glob('v*.md')):
 src=p.read_text(); s=src
 s=re.sub(r'\\\[(.*?)\\\]',lambda m:'$$'+m[1]+'$$',s,flags=re.S)
 s=re.sub(r'\\\((.*?)\\\)',lambda m:'$'+m[1]+'$',s,flags=re.S)
 count=[0]
 def code(m):
  raw=m[1]
  if re.fullmatch(r'\[(?:episode|batch|time|20)[a-z0-9, ]*\]',raw):return m[0]
  count[0]+=1
  return '$'+mathify(raw)+'$'
 s=re.sub(r'`([^`\n]+)`',code,s)
 # Standalone mathematical statements deserve display layout.
 s=re.sub(r'^\$(J\s*=.+?)\$(\.)?$',lambda m:'$$\n'+m[1]+'\n$$'+('\n' if m[2] else ''),s,flags=re.M)
 if p.name.startswith('v01'):
  s=re.sub(r'\$\$\s*F_L=.*?\$\$',lambda m:r'''$$
\begin{aligned}
F_L &= (g+b)(a+u), \\
F_R &= (g-b)(a-u), \\
F_+ &= 2ga+2bu, \\
F_- &= 2ba+2gu.
\end{aligned}
$$''',s,count=1,flags=re.S)
 if p.name.startswith('v02'):
  s=s.replace(r'\tau\dot q_L=a+u-q_L,\qquad \tau\dot q_R=a-u-q_R,',r'\begin{aligned}\tau\dot q_L&=a+u-q_L, \\ \tau\dot q_R&=a-u-q_R.\end{aligned}')
 if s!=src:p.write_text(s)
 changes.append({'file':str(p.relative_to(ROOT)),'code_expressions_typeset':count[0]})
print(changes)
