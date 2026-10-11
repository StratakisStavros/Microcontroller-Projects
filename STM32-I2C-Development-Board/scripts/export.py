#!/usr/bin/env python3
"""Check and export the board with KiCad 9; Python standard library only."""
from pathlib import Path
import argparse, csv, hashlib, json, re, subprocess, tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
BOARD = 'hardware/stm32-i2c-board.kicad_pcb'
SCH = 'hardware/stm32-i2c-board.kicad_sch'

def natural(s):
    return [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', s)]

def parse_sexpr(path):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', path.read_text(encoding='utf-8'))
    stack = [[]]
    for token in tokens:
        if token == '(':
            child = []
            stack[-1].append(child)
            stack.append(child)
        elif token == ')':
            stack.pop()
        else:
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    return stack[0][0]

def make_map():
    board = parse_sexpr(ROOT / BOARD)
    x0, y0, scale = 66.25, 73.75, 24
    w, h, margin, top = 40*scale, 28.75*scale, 55, 95
    parts = []
    for fp in board:
        if not isinstance(fp, list) or fp[0] != 'footprint':
            continue
        ref = next(x[2] for x in fp if isinstance(x, list) and x[:2] == ['property','Reference'])
        at = next(x for x in fp if isinstance(x, list) and x[0] == 'at')
        parts.append((ref, margin+(float(at[1])-x0)*scale, top+(float(at[2])-y0)*scale))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w+110}" height="{h+170}" viewBox="0 0 {w+110} {h+170}">',
           '<rect width="100%" height="100%" fill="#f8fafc"/>',
           '<g font-family="Arial,sans-serif">',
           '<text x="55" y="42" font-size="27" font-weight="700" fill="#152c3a">STM32 I²C board · component map</text>',
           '<text x="55" y="69" font-size="16" fill="#475569">Top view · footprint origins · match pin 1 to the square PCB pad</text>',
           f'<rect x="{margin}" y="{top}" width="{w}" height="{h}" rx="60" fill="#e8f1ed" stroke="#365e4f" stroke-width="3"/>']
    for ref,x,y in parts:
        if ref.startswith('H'):
            svg.append(f'<circle cx="{x}" cy="{y}" r="26.4" fill="#f8fafc" stroke="#64748b"/>')
        else:
            svg.append(f'<rect x="{x-20}" y="{y-12}" width="40" height="24" rx="4" fill="white" stroke="#75978b"/>')
        svg.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" font-size="15" font-weight="700" fill="#173d31">{ref}</text>')
    svg += [f'<text x="55" y="{h+139}" font-size="16" fill="#475569">J1 USB · J2 SWD · J3 UART · J4 I²C · U1 MCU · U2 regulator · SW1 BOOT0</text>', '</g></svg>']
    (ROOT/'docs/images/component-map.svg').write_text('\n'.join(svg),encoding='utf-8')

def clean_assembly():
    """Keep one reference label per component; omit value labels from the drawing."""
    path=ROOT/'manufacturing/assembly/assembly-top.svg'
    tree=ET.parse(path)
    root=tree.getroot()
    ns={'s':'http://www.w3.org/2000/svg'}
    parents={c:p for p in root.iter() for c in p}
    seen=set()
    for group in list(root.findall('.//s:g[@class="stroked-text"]',ns)):
        desc=group.find('s:desc',ns)
        label='' if desc is None else desc.text or ''
        if not re.fullmatch(r'(?:C|R|H|J|U|D|Y|FB|SW)\d+',label) or label in seen:
            parents[group].remove(group)
        else:
            seen.add(label)
    # KiCad's hidden text duplicates the rendered stroke paths.
    for elem in list(root.findall('.//s:text',ns)):
        parents[elem].remove(elem)
    for elem in root.iter():
        if 'style' in elem.attrib:
            elem.set('style',re.sub(r'#[0-9A-Fa-f]{6}', '#243746', elem.get('style')))
    view=root.get('viewBox').split()
    bg=ET.Element('{http://www.w3.org/2000/svg}rect',dict(zip(('x','y','width','height'),view)),fill='white')
    root.insert(0,bg)
    ET.register_namespace('','http://www.w3.org/2000/svg')
    tree.write(path,encoding='utf-8',xml_declaration=True)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--kicad-cli', default='kicad-cli')
    ap.add_argument('--skip-renders', action='store_true')
    args = ap.parse_args()
    def run(*argv):
        subprocess.run([args.kicad_cli,*argv],cwd=ROOT,check=True)
    for d in ('validation','docs/images','docs/schematic','manufacturing/gerbers','manufacturing/drill','manufacturing/assembly'):
        (ROOT/d).mkdir(parents=True,exist_ok=True)
    run('version')
    run('sch','erc','--format','json','--exit-code-violations','-o','validation/erc.json',SCH)
    run('pcb','drc','--schematic-parity','--format','json','--exit-code-violations','-o','validation/drc.json',BOARD)
    run('sch','export','pdf','-o','docs/schematic/stm32-i2c-board.pdf',SCH)
    run('sch','export','svg','-o','docs/schematic/',SCH)
    for outfile,layers,extra in (
        ('docs/images/layout-top.svg','F.Cu,F.SilkS,Edge.Cuts',[]),
        ('docs/images/layout-bottom.svg','B.Cu,B.SilkS,Edge.Cuts',['--mirror']),
        ('manufacturing/assembly/assembly-top.svg','F.Fab,Edge.Cuts',[])):
        run('pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layers,*extra,'-o',outfile,BOARD)
    run('pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts','--subtract-soldermask','--no-protel-ext','-o','manufacturing/gerbers/',BOARD)
    run('pcb','export','drill','--excellon-separate-th','--generate-map','--map-format','svg','-o','manufacturing/drill/',BOARD)
    run('pcb','export','pos','--format','csv','--units','mm','--smd-only','-o','manufacturing/assembly/placement.csv',BOARD)
    with tempfile.TemporaryDirectory() as tmp:
        net = Path(tmp)/'netlist.xml'
        run('sch','export','netlist','--format','kicadxml','-o',str(net),SCH)
        grouped = defaultdict(list)
        for comp in ET.parse(net).getroot().findall('./components/comp'):
            if comp.get('ref').startswith('H'):
                continue
            grouped[(comp.findtext('value'),comp.findtext('footprint'))].append(comp.get('ref'))
        with (ROOT/'manufacturing/bom.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow(['References','Quantity','Value','Footprint','Procurement status'])
            for (val,fp),refs in sorted(grouped.items(),key=lambda x:natural(sorted(x[1],key=natural)[0])):
                writer.writerow([', '.join(sorted(refs,key=natural)),len(refs),val,fp,'Select and verify exact manufacturer part'])
    make_map()
    clean_assembly()
    for path in ROOT.rglob('*.svg'):
        text='\n'.join(line.rstrip() for line in path.read_text(encoding='utf-8').splitlines())+'\n'
        path.write_bytes(text.encode('utf-8'))
    if not args.skip_renders:
        run('pcb','render','--width','1800','--height','1200','--rotate','35,0,25','--background','opaque','--quality','high','-o','docs/images/board-perspective.png',BOARD)
        run('pcb','render','--width','1600','--height','1100','--side','top','--background','opaque','-o','docs/images/board-top.png',BOARD)
    paths = sorted(p for p in (ROOT/'hardware').rglob('*') if p.is_file() and p.suffix not in ('.kicad_prl','.lck'))
    manifest='\n'.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(ROOT).as_posix()}' for p in paths)+'\n'
    (ROOT/'validation/source-sha256.txt').write_text(manifest,encoding='utf-8')
    print('Checks and exports complete. Bench validation remains separate.')

if __name__ == '__main__':
    main()
