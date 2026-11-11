import json, html as H

def n(v): return ('%.3f' % v).rstrip('0').rstrip('.')

def vars_(d, m, fs, lh, ls):
    out = []
    if d:
        for k, v in zip('xywh', d): out.append(f'--{k}:{n(v)}')
    if m:
        for k, v in zip('xywh', m): out.append(f'--m{k}:{n(v)}')
    if fs:
        out.append(f'--fs:{n(fs[0])}')
        if len(fs) > 1 and fs[1] is not None: out.append(f'--mfs:{n(fs[1])}')
    if lh:
        out.append(f'--lh:{n(lh[0])}')
        if len(lh) > 1 and lh[1] is not None: out.append(f'--mlh:{n(lh[1])}')
    if ls:
        out.append(f'--ls:{n(ls[0])}')
        if len(ls) > 1 and ls[1] is not None: out.append(f'--mls:{n(ls[1])}')
    return ';'.join(out)

def fmt(t):
    """'|' quebra nos dois; '|d' quebra só no desktop (espaço no mobile); '|m' quebra só no mobile (espaço no desktop)"""
    t = t.replace('|d', '<span class="dm"><br></span><span class="mo"> </span>').replace('|m', '<span class="mo"><br></span><span class="dm"> </span>')
    return t.replace('|', '<br>')

class Sec:
    def __init__(self, tag='section', H=100, mH=None, cls='', attrs='', off=(0, 0)):
        self.tag, self.H, self.mH, self.cls, self.attrs, self.off = tag, H, mH if mH is not None else H, cls, attrs, off
        self.items = []
    def E(self, tag, d, m, content='', cls='', fs=None, lh=None, ls=None, style='', attrs='', base='a'):
        """d/m = (x,y[,w,h]) in reference px; None => hidden on that breakpoint. off is subtracted from y."""
        oy_d, oy_m = self.off
        d2 = (d[0], d[1] - oy_d) + tuple(d[2:]) if d else None
        m2 = (m[0], m[1] - oy_m) + tuple(m[2:]) if m else None
        c = base + (' mo' if not d else '') + (' dm' if not m else '') + (' ' + cls if cls else '')
        st = vars_(d2, m2, fs, lh, ls) + (';' + style if style else '')
        self.items.append(f'<{tag} class="{c}" style="{st}"{(" " + attrs) if attrs else ""}>{content}</{tag}>')
    def T(self, d, m, txt, cls='', fs=None, lh=None, ls=None, tag='p', style='', attrs=''):
        self.E(tag, d, m, txt, cls, fs, lh, ls, style, attrs)
    def R(self, d, m, color, cls='', style='', content='', attrs=''):
        self.E('i', d, m, content, cls, style=f'background:{color};' + style, attrs=attrs, base='bar')
    def X(self, cx, cy, r, mcx=None, mcy=None, mr=None):
        d = (cx - r, cy - r, 2 * r, 2 * r) if cx is not None else None
        m = (mcx - mr, mcy - mr, 2 * mr, 2 * mr) if mcx is not None else None
        self.E('i', d, m, '', 'xh', base='xh a')
    def raw(self, s): self.items.append(s)
    def html(self):
        st = f'--H:{n(self.H)};--mH:{n(self.mH)}'
        return f'<{self.tag} class="s {self.cls}" style="{st}" {self.attrs}>' + '\n'.join(self.items) + f'</{self.tag}>'

def RULE(s, y, color='#8A8A8A', my=None, x=(12, 722), mx=(12, 378), th=1, hide_m=False):
    d = (x[0], y, x[1] - x[0], th)
    m = None if hide_m else (mx[0], y if my is None else my, mx[1] - mx[0], th)
    s.R(d, m, color)

_mk=[0]
def MK(s, label, y, my=None, color='#333', hide_m=False):
    _mk[0]+=1; label=f'{_mk[0]:03d}'
    """section marker (mono 7.5) — y/my are the top of the text box"""
    s.T((12, y), None if hide_m else (16, y if my is None else my), label, 'mono', fs=(7.5, 9), lh=(9, 10.8), tag='span', style=f'color:{color}')

def RL(s, x, y, h, color='#999'):
    s.R((x, y, .8, h), None, color)

def GLOBE():
    return ('<svg viewBox="0 0 100 100" fill="none" stroke="#0B0B0B" aria-hidden="true">'
            '<circle cx="50" cy="50" r="48" stroke-width="4.8"/><ellipse cx="50" cy="50" rx="23" ry="48" stroke-width="4"/>'
            '<ellipse cx="50" cy="50" rx="48" ry="19" stroke-width="4"/><path d="M50 2v96M2 50h96" stroke-width="4"/></svg>')

ARROW_LONG = '<svg class="long" viewBox="0 0 7 8" fill="none" stroke="#444" stroke-width=".9"><path d="M0 0.5L6.5 4L0 7.5"/></svg>'

# ============================================================ cabeçalho
def header(active=None):
    links = [('Início', '#topo'), ('Experiência', '#experiencia'), ('Web', '#web'), ('Gráfico', '#grafico'), ('Contato', '#contato')]
    nav = ''.join(f'<a href="{h}">{l}</a>' for l, h in links)
    return ('<header class="hd">'
        '<div class="hc hc-logo"><a class="disp logo" href="#topo" aria-label="J. Erick Prestes — início">J. erick prestes</a></div>'
        f'<nav class="hc hc-nav nav dm" aria-label="Principal">{nav}</nav>'
        '<div class="hc hc-loc mono dm">BRASIL / SP / TAUBATÉ</div>'
        '<a class="cta dm" href="#footer">Contrate ↗</a>'
        '<button class="menu-btn mo-btn" aria-label="Abrir menu" aria-expanded="false"><i></i><i></i><i></i></button>'
        '<nav class="navwrap nav" aria-label="Principal móvel"><a href="#topo">Início</a><a href="#experiencia">Experiência</a><a href="#web">Web</a><a href="#grafico">Gráfico</a><a href="#contato">Contato</a><span class="navloc">BRASIL / SP / TAUBATÉ</span></nav>'
        '<i class="hline"></i><i class="mdiv"></i></header>')

def header_fix(html_):  # divisor do botão de menu só no mobile
    return html_

# ============================================================ footer
def footer():
    s = Sec('footer', 490, 1170, cls='ft', attrs='id="footer"')
    RULE(s, 8)
    MK(s, '006', 19.5, 18.6)
    RL(s, 20.1, 34, 358)
    s.X(296, 30, 4); s.X(708, 30, 4)
    s.R((690, 70, 45, 250), (366, 29.6, 24, 130), 'var(--yel)')
    s.R((300, 34, 406, 366), (0, 220, 390, 650), 'var(--blk)')
    s.T((46, 49.5), (24, 61), 'ENTRE EM<br>CONTATO', 'xb', fs=(34, 30), lh=(33, 30), ls=(-.9, -.7), tag='h2', style='color:#111;white-space:nowrap')
    s.T((46, 139.2), (24, 140), 'Conte um pouco sobre o<span class="dm"><br></span><span class="mo"> </span>seu projeto.<span class="dm"> </span><span class="mo"><br></span>Sem compromisso,<span class="dm"><br></span><span class="mo"> </span>é só o primeiro<span class="mo"><br></span><span class="dm"> </span>passo<span class="dm"><br></span><span class="mo"> </span>de uma conversa.', 'nw', fs=(10.5, 14), lh=(13.5, 20), ls=(-.1,))
    # tile vermelho com globo
    s.E('div', (46, 366.3, 89.5, 63.2), (236.5, 29.6, 129.5, 91.4), GLOBE(), 'globe', style='background:var(--red)', base='a')
    # dados de contato
    info = [('E-MAIL', 'JERICKPRESTES@GMAIL.COM', 'mailto:jerickprestes@gmail.com'), ('TELEFONE', '(12) 98145-2330', 'tel:+5512981452330'),
            ('LOCALIZAÇÃO', 'TAUBATÉ / SP / BRASIL', None), ('REDES', None, None)]
    for i, (lab, val, href) in enumerate(info):
        y = 229.6 + i * 34.0; my = 910 + i * 46 - 10
        s.R((46, y, 224, .8), (24, my, 342, .8), '#999')
        s.T((46, y + 4.7), (24, my + 9), lab, 'mono', fs=(6.2, 8), lh=(7.4, 10), tag='span', style='color:#666')
        if lab == 'REDES':
            val = '<a href="https://www.behance.net/jerickprestes" target="_blank" rel="noopener">BEHANCE</a><span class="dm"> · </span><span class="mo-sp"></span><a href="https://www.linkedin.com/in/jerickprestes/" target="_blank" rel="noopener">LINKEDIN</a><span class="dm"> · </span><span class="mo-sp"></span><a href="https://github.com/jerickprestes" target="_blank" rel="noopener">GITHUB</a>'
        elif href: val = f'<a href="{href}">{val}</a>'
        s.T((46, y + 15.8), (24, my + 25.5), val, 'mono', fs=(7.6, 11), lh=(9.1, 13), tag='span', style='color:#111')
    s.R((46, 365.6, 224, .8), (24, 910 + 4 * 46 - 10, 342, .8), '#999')
    # formulário
    form = '''<form class="ft-form" id="form-contato" novalidate>
<div class="fld"><label for="f-nome">Nome</label><input id="f-nome" name="nome" type="text" placeholder="Seu nome completo" autocomplete="name" required></div>
<div class="fld"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" placeholder="seu@email.com" autocomplete="email" required></div>
<div class="fld"><label for="f-tel">Telefone / WhatsApp</label><input id="f-tel" name="telefone" type="tel" placeholder="(00) 00000-0000" autocomplete="tel"></div>
<div class="fld"><label for="f-tipo">Tipo de projeto</label><select id="f-tipo" name="tipo"><option>Site institucional</option><option>Landing page</option><option>E-commerce / loja virtual</option><option>Identidade visual</option><option>Peças gráficas e social media</option><option>Automação / IA</option><option>Outro</option></select></div>
<div class="fld full"><label for="f-prazo">Prazo desejado</label><select id="f-prazo" name="prazo"><option>Urgente (até 15 dias)</option><option>Até 30 dias</option><option>Até 60 dias</option><option>Sem pressa</option></select></div>
<div class="fld full"><label for="f-msg">Conte um pouco do que você precisa</label><textarea id="f-msg" name="mensagem" placeholder="Descreva brevemente seu projeto..."></textarea></div>
<button class="send" type="submit">Enviar e começar a conversa ↗</button>
<p class="ft-msg" role="status" aria-live="polite"></p>
</form>'''
    s.E('div', (320, 58.1, 366), (40, 241.2, 310), form, '', base='a')
    RULE(s, 429.5, my=1110, mx=(24, 366))
    s.T((46, 451.8), (24, 1130.5), 'J. ERICK PRESTES · © 2026', 'mono', fs=(7, 8.5), lh=(8.4, 11), tag='span', style='color:#333')
    s.T((430, 451.8), None, '<a href="#topo">INÍCIO</a> &nbsp;&nbsp; <a href="#experiencia">EXPERIÊNCIA</a> &nbsp;&nbsp; <a href="#web">WEB</a> &nbsp;&nbsp; <a href="#grafico">GRÁFICO</a> &nbsp;&nbsp; <a href="#contato">CONTATO</a>', 'mono', fs=(7,), lh=(8.4,), tag='nav', style='color:#333', attrs='aria-label="Rodapé"')
    s.T((656, 451.8), (250, 1130.5), '<a href="#topo">VOLTAR AO TOPO ↑</a>', 'mono', fs=(7, 8.5), lh=(8.4, 11), tag='span', style='color:#333')
    return s

def page(title, body, desc):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="css/style.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="icon" href="favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/BauhausBox-Regular.otf" as="font" type="font/otf" crossorigin>
</head>
<body>
<div class="page">
{body}
</div>
<script src="js/main.js"></script>
</body>
</html>
'''

# ============================================================ INÍCIO
def inicio_sections():
    off = (38, 56)
    hero = Sec(H=569.5 - 38, mH=770 - 56, off=off, attrs='id="inicio"', cls='hero')
    def Y(d, m): return d, m
    # trilho (alinhado em rem com todas as seções)
    hero.E('span', (12, 48.5), (16, 62.6), '001', 'mono rx', fs=(7.5, 9), lh=(9, 10.8), style='color:#333')
    _mk[0] += 1  # o 001 da hero é literal; a numeração das demais seções segue a partir dele
    hero.E('i', (20.1, 63, .8, 506.5), None, '', 'rx', style='background:#999', base='bar')
    # cruzetas
    def XH(cx, cy, r, mcx, mcy, mr, side, mside):
        d = (cx - r, cy - r, 2 * r, 2 * r) if cx is not None else None
        m = (mcx - mr, mcy - mr, 2 * mr, 2 * mr) if mcx is not None else None
        cls = []
        hero.E('i', d, m, '', 'xh ' + side, base='xh a')
    XH(356, 53, 4, 24, 372, 4, 'sh', 'sh')
    XH(652, 53, 4, 360, 372, 4, 'rt', 'rt')
    XH(329, 447, 5, None, None, None, 'sh', 'sh')
    XH(652, 467, 4, None, None, None, 'rt', 'rt')
    XH(667, 526, 7, None, None, None, 'rt', 'rt')
    hero.T((32.5, 86.5), (22, 85.6), 'web<br>graph<br>tech<br>code', 'disp sh', fs=(66, 64), lh=(66, 64), ls=(.8, .5), tag='h1', style='color:#111')
    # bloco azul elástico: borda esquerda na coluna esquerda, borda direita ancorada à direita (desktop 90u, mobile 24u)
    # ---- carrossel da hero: janela que começa na linha do "+" e vai até a borda direita
    HERO_IMG = "https://images.pexels.com/photos/4164418/pexels-photo-4164418.jpeg?auto=compress&w=1260&h=750&dpr=1"
    SL = [('hs1', 'web', 'Landing pages, e-commerces e sistemas web com WordPress, WooCommerce e Elementor: rápidos, responsivos e feitos para converter.', 'right'),
          ('hs2', 'graph', 'Identidade visual, redes sociais, impresso e embalagem: peças gráficas com linguagem própria e consistência de marca.', 'left'),
          ('hs3', 'tech', 'Do protótipo no Figma à implementação em WordPress, WooCommerce e Elementor, com PHP e JavaScript sob medida.', 'right'),
          ('hs4', 'code', 'Automação com Python, Adobe Firefly e design via terminal: peças em lote, adaptação de formatos e validação de tudo que a IA entrega.', 'right')]
    arrow = '<svg viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1" aria-hidden="true"><path d="M0 4h11M7.5.5L11 4 7.5 7.5"/></svg>'
    sl = ''
    for i, (cl, t, d, _) in enumerate(SL):
        sl += (f'<article class="hs {cl}"><img class="bgi" src="{HERO_IMG}" alt="" draggable="false" loading="eager">'
               f'<span class="mono hs-i"><b>{i+1:02d}</b> / 04</span><button type="button" class="hs-n" aria-label="Próximo slide">{arrow}</button>'
               f'<h2 class="disp hs-t">{t}</h2><p class="hs-d">{d}</p></article>')
    hero.E('div', (356, 52, 0, 415), (24, 350, 0, 230), f'<div class="hc-track" id="heroTrack">{sl}</div>', 'hcar', attrs='id="heroCar" role="region" aria-roledescription="carrossel" aria-label="Web, graph, tech e code" tabindex="0"', base='a')
    hero.E('img', (335, 424.5, 158, 145.5), (236, 456, 134, 124), '', 'sh mrt', style='object-fit:contain', attrs='src="img/pessoa.png" alt="J. Erick Prestes"', base='a')
    hero.items[-1] = hero.items[-1].replace('></img>', '>')
    hero.T((269, 477), None, 'j erick prestes', 'sh', fs=(9,), lh=(10.8,), tag='span', style='color:#444')
    hero.E('div', (296, 492, 34, 22), None, '<svg viewBox="0 0 34 22" fill="none" stroke="#555" stroke-width=".9" width="100%" height="100%"><path d="M.5 .5C2 14 14 19 32 16.5"/><path d="M25.5 11.5L32.5 16.5L26.5 21"/></svg>', 'sh')
    hero.T((43, 443.7), (24, 596), 'Designer gráfico e web designer<br>com mais de 5 anos em agências<br>e liderança de equipe de criação.', 'nw sh', fs=(10.5, 15), lh=(12.6, 20), ls=(-.1,))
    hero.T((43, 504.1), (24, 679.5), 'PORTFÓLIO / 2026<br>DESIGN · WEB · IA E AUTOMAÇÃO', 'mono sh', fs=(7, 9), lh=(9.7, 13))
    hero.E('a', (43, 538.3), (24, 724.2), 'Ver trabalhos ↘', 'lk sh', fs=(9.5, 13), lh=(11.4, 15.6), attrs='href="#web"')
    hero.T((616, 517.5, 70), (290, 684.5, 60), '23.0264° S<br>45.5557° W', 'mono rt', fs=(6.8, 8), lh=(10, 11), style='color:#111')

    # ---- 002
    s2 = Sec(H=161, mH=400, off=(0, 0))
    RULE(s2, 0, my=0)
    MK(s2, '002', 12, 8.6)
    RL(s2, 20.1, 26.5, 114)
    s2.T((46, 21), (24, 44.5), 'DESIGN, CÓDIGO E IA /<br>PARA MARCAS QUE QUEREM<br>SE DESTACAR.', 'xb nw', fs=(34, 22), lh=(33, 23), ls=(-.9, -.7), tag='h2')
    s2.T((574, 37), (24, 127), fmt('Mais de 5 anos em|d agências de |mpublicidade:|d design digital,|m impresso|d e web, com IA e|automação no processo.'), 'nw', fs=(9.5, 13), lh=(11, 18))
    labs = ['CONTEÚDO', 'IMPRESSO', 'DIGITAL', 'AUTOMAÇÃO']
    lis = ''
    widths = [181, 170, 162, 164]
    for i, lab in enumerate(labs):
        last = i == 3
        lis += (f'<li style="width:{widths[i]}rem"><span class="n">0{i+1}</span><span class="l">{lab}</span><i class="ln"></i>' + (ARROW_LONG if last else '') +
                '<svg class="chev" viewBox="0 0 7 10" fill="none" stroke="#444" stroke-width=".9"><path d="M.5.5L6 5 .5 9.5"/></svg></li>')
    s2.E('ol', (45, 128.7, 661, 20), (24, 232, 342, 168), lis, 'idx', base='a')
    s2.items[-1] = s2.items[-1].replace('class="a idx"', 'class="a idx"')

    # ---- 003 cards
    s3 = Sec(H=232.5, mH=480)
    RULE(s3, 0, '#B5B2AA', my=0)
    MK(s3, '003', 10, 8.6)
    RL(s3, 20.1, 24.5, 207)
    cards = [('var(--red)', 'web', 'LANDING PAGES<br>E E-COMMERCE', '#C9C9C9', '#EDEDED'),
             ('var(--blue)', 'graph', 'IDENTIDADE VISUAL,<br>REDES SOCIAIS<br>IMPRESSO E EMBALAGEM', '#C9C9C9', '#EDEDED'),
             ('#fff', 'tech', 'FIGMA, WORDPRESS<br>PHP E JAVASCRIPT', '#C9C9C9', '#8A8A8A'),
             ('var(--lime)', 'IA', 'CRIAÇÃO, VELOCIDADE<br>E AUTOMAÇÃO', '#C9C9C9', '#8A8A8A')]
    cs = ''
    for i, (col, word, desc, lc, lcm) in enumerate(cards):
        cs += (f'<a class="card" href="{"#web" if i in (0,2) else "#grafico" if i==1 else "#contato"}" style="background:{col};--lc:{lc};--lcm:{lcm}">'
               f'<span class="mono c-l">ATUAÇÃO</span><span class="mono c-n">0{i+1}</span><span class="disp c-w">{word}</span><span class="mono c-d">{desc}</span><span class="c-a">→</span></a>')
    s3.E('div', (36, .5, 686, 232), (24, 38, 342, 424), cs, 'cards', base='a')
    # ---- 004 faixa
    s4 = Sec(H=60, mH=140, cls='band on-dark')
    s4.R((0, 0, 735, 60), (0, 0, 390, 140), 'var(--blk)')
    MK(s4, '', 11.5, 8.6, color='#DDD')
    for txt, dx, mx, col, href in (('web', 46, 24, '#C9C9C9', '#web'), ('graph', 250.5, 124, '#C9C9C9', '#grafico'), ('tech', 483.5, 266.5, '#E8FF3A', '#web')):
        s4.T((dx, 18.8), (mx, 33.8), txt, 'disp bw', fs=(25.3, 22), lh=(25.3, 22), ls=(0, .4), tag='a', style=f'color:{col};--hc:{"#F72B10" if txt=="web" else "#0373DF" if txt=="graph" else "#fff"}', attrs=f'href="{href}"')
    s4.R((155, 30.5, 88, 1), (100, 43.7, 16, 1), '#666'); s4.R((383, 30.5, 87, 1), (242.5, 43.7, 16, 1), '#666')
    s4.T((627, 8.9), (24, 80.75), 'DESIGN, CÓDIGO<br>E IA A SERVIÇO<br>DA SUA MARCA.', 'mono', fs=(6.8, 8), lh=(8.2, 10.5), style='color:#F2F2F2')
    s4.T((627, 38.4), (230, 80.75), 'J. ERICK PRESTES<br>© 2026', 'mono', fs=(6.8, 8), lh=(8.2, 10.5), style='color:#F2F2F2')
    return ['<div class="top" id="topo">' + header() + hero.html() + '</div>', s2.html(), s3.html(), s4.html()]


# ============================================================ EXPERIÊNCIA
def experiencia_sections():
    ROWS = [('AGO 2025 — AGO 2026', 'Supervisor de Projetos', 'EQUIPE DE CRIAÇÃO · TOMORROW AGENCY & BUSINESS',
             'Liderei a equipe de criação de 6 pessoas (copywriter, dois designers, editor de vídeo, gestora de tráfego e web designer) e em média 15 projetos simultâneos. Implantei um fluxo de produção com IA e automação (Python e Adobe Firefly) e estruturei briefing, revisão e aprovação no Monday e no ClickUp.', 72, 192),
            ('MAI 2024 — AGO 2025', 'Designer', 'EQUIPE DE CRIAÇÃO · TOMORROW AGENCY & BUSINESS',
             'Em média 50 peças por mês para 15 clientes ativos: redes sociais, anúncios, e-mail marketing e impressos. Landing pages e layouts de site com foco em responsividade e conversão.', 54, 156),
            ('MAR 2024 — MAI 2024', 'Designer', 'SETOR DE PUBLICIDADE · AGÊNCIA VIRTUA BRASIL', 'Elaboração de criativos e textos para mídias digitais.', 42, 108),
            ('JUN 2022 — MAR 2024', 'Designer', 'SETOR DE MÍDIAS ONLINE · AGÊNCIA PROVOCA', 'Elaboração de criativos para redes sociais.', 42, 108),
            ('DEZ 2021 — JUN 2022', 'Designer', 'EQUIPE DE MARKETING · CLIQUERIA', 'Criação e diagramação de produtos e criativos publicitários.', 42, 108)]
    ty, mty = 214, 322 + 0
    Hd = ty + sum(r[4] for r in ROWS) + 72
    Hm = mty + sum(r[5] for r in ROWS) + 130
    s = Sec(H=Hd, mH=Hm, attrs='id="experiencia"')
    RULE(s, 0, '#B5B2AA', my=0); MK(s, '', 11.5, 14.6); RL(s, 20.1, 26, Hd - 34)
    s.T((46, 31.5), (24, 51), 'EXPERIÊNCIA', 'xb', fs=(34, 26), lh=(33, 26), ls=(-.9, -.7), tag='h2')
    s.T((574, 36.5), (24, 92), fmt('Mais de 5 anos em agências|d de publicidade:|m do design|d à liderança da equipe|d de criação.'), 'nw', fs=(9.5, 12), lh=(11, 17))
    s.T((45, 90), (24, 138), 'LIDERANÇA / SUPERVISOR DE PROJETOS · TOMORROW AGENCY & BUSINESS', 'mono', fs=(6.8, 8), lh=(8.2, 10), tag='span', style='color:#333')
    stats = [('var(--red)', '#111', '6', 'PESSOAS NA EQUIPE<br>LIDERADA'), ('var(--blue)', '#fff', '~15', 'PROJETOS<br>SIMULTÂNEOS'),
             ('var(--yel)', '#111', '95%', 'ENTREGAS<br>NO PRAZO'), ('var(--lime)', '#111', '~30%', 'MENOS TEMPO DE ENTREGA<br>COM IA E AUTOMAÇÃO')]
    html = ''.join(f'<div class="xst" style="background:{c};color:{t}"><span class="disp xs-n">{n}</span><span class="mono xs-l">{l}</span></div>' for c, t, n, l in stats)
    s.E('div', (36, 104, 686, 94), (24, 158, 342, 150), html, 'xstats', base='a')
    y, my = ty, mty
    for dt, role, comp, desc, h, mh in ROWS:
        s.R((12, y, 710, 1), (12, my, 366, 1), '#8A8A8A')
        s.T((45, y + 10.5), (24, my + 13), dt, 'mono', fs=(7.5, 9), lh=(9, 11), tag='span', style='color:#333')
        s.T((190, y + 8.5), (24, my + 34), role, 'xb nw', fs=(14, 16), lh=(16, 18), ls=(-.4,), tag='h3')
        s.T((190, y + 28), (24, my + 56), comp, 'mono nw', fs=(6.4, 7.4), lh=(8, 9.5), tag='span', style='color:#333')
        s.T((410, y + 10.5, 305), (24, my + 76, 342), desc, '', fs=(9, 12), lh=(11.4, 15.5))
        y += h; my += mh
    s.R((12, y, 710, 1), (12, my, 366, 1), '#8A8A8A')
    s.T((45, y + 10.5), (24, my + 13), 'PARCERIAS E PROJETOS (MEI)', 'mono', fs=(7.5, 9), lh=(9, 11), tag='span', style='color:#333')
    s.T((190, y + 10.5, 525), (24, my + 36, 342), '<b class="xb">SP Leituras:</b> design ON/OFF para equipamentos e projetos públicos. <b class="xb">Talassa Comunicação e Agência Cratix:</b> conteúdo digital. <b class="xb">Monquei Sites:</b> layouts de landing pages e sites.', '', fs=(9, 12), lh=(11.4, 15.5))
    return [s.html()]

# ============================================================ WEB
def web_sections():
    s = Sec(H=330, mH=540, attrs='id="web"')
    RULE(s, 8)
    MK(s, '001', 19.5, 18.6); RL(s, 20.1, 34, 266)
    s.T((34, 47), (22, 49.6), 'web', 'disp', fs=(150, 104), lh=(150, 104), ls=(1.2, 1), tag='h1', style='color:#111')
    s.R((480, 30, 175, 232), (150, 170, 216, 170), 'var(--blue)')
    s.R((669, 96, 66, 166), (366, 140, 24, 200), 'var(--yel)')
    s.X(468, 30, 4, 150, 162, 4); s.X(667, 30, 4, 358, 162, 4); s.X(667, 270, 4)
    s.T((43, 215.7), (24, 366), fmt('Layouts produzidos e sites em que|m trabalhei: landing pages,|d e-commerces|m e sistemas web.'), 'nw', fs=(10.5, 14), lh=(12.6, 20), ls=(-.1,))
    s.T((43, 257.15), (24, 444), 'LAYOUTS + SITES / 2026<br>FIGMA · WORDPRESS · WOOCOMMERCE · ELEMENTOR', 'mono', fs=(7, 8.5), lh=(9.7, 12))
    s.E('a', (43, 286.3), (24, 492.2), 'Ver layouts ↘', 'lk', fs=(9.5, 13), lh=(11.4, 15.6), attrs='href="#layouts"')
    s.T((480, 271.9), None, 'WEB / 2026', 'mono', fs=(6.8,), lh=(8.2,), tag='span')
    # ---- 002 layouts
    s2 = Sec(H=506, mH=1180, attrs='id="layouts"')
    RULE(s2, 0, my=0); MK(s2, '002', 11.5, 14.6); RL(s2, 20.1, 26, 480)
    s2.T((46, 31.5), (24, 51), 'LAYOUTS<br>PRODUZIDOS', 'xb', fs=(34, 26), lh=(33, 26), ls=(-.9, -.7), tag='h2')
    s2.T((574, 36.5), (24, 119.5), fmt('Galeria de layouts e protótipos<span class="dm"><br>de</span><span class="mo"> de<br></span> interfaces criados para|d landing pages,|m e-commerces|d e sistemas web.'), 'nw', fs=(9.5, 12), lh=(11, 17))
    # controles do carrossel (contador + linha + setas)
    ctrl = ('<span class="mono cc-n"><b id="carCur">01</b> / 06</span><i class="ln"></i>'
            '<button type="button" class="cc-b" id="carPrev" aria-label="Layout anterior"><svg viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1"><path d="M12 4H1M4.5.5L1 4l3.5 3.5"/></svg></button>'
            '<button type="button" class="cc-b" id="carNext" aria-label="Próximo layout"><svg viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1"><path d="M0 4h11M7.5.5L11 4 7.5 7.5"/></svg></button>')
    s2.E('div', (45, 124.2, 661, 20), (24, 186, 342, 24), ctrl, 'cc', base='a')
    RULE(s2, 160, '#B5B2AA', my=None, hide_m=True)
    L = [('var(--red)', '#111', 'SP Leituras 2025', 'Site institucional de projetos públicos', 'sp-leituras-2025'),
         ('var(--blue)', '#D7E2FF', 'Cookies da Kel', 'Design Mobile-First para delivery', 'cookies-da-kels'),
         ('var(--lime)', '#111', 'Clube de Negócios LMA', 'Design moderno focado em conversão e UX', 'clube-lma'),
         ('var(--yel)', '#111', 'Fillos', 'Layout institucional clean e responsivo', 'fillos'),
         ('#fff', '#111', 'Mayra Hall', 'Landing page de bem-estar e saúde', 'mayra-hall'),
         ('var(--red)', '#111', 'Jornada Literária', 'Landing page de evento literário', 'jornada-literaria-2025')]
    cs = ''
    for i, (col, lc, t, dsc, img) in enumerate(L):
        bd = ';box-shadow:inset 0 0 0 1px #111' if col == '#fff' else ''
        cs += (f'<article class="lcard" style="background:{col}{bd}"><span class="mono lc-l" style="color:{lc}">LAYOUT</span><span class="disp lc-n">{i+1:02d}</span>'
               f'<span class="lc-p"><img src="img/layouts/{img}.jpg" alt="Prévia do layout {t}" loading="lazy" draggable="false"></span>'
               f'<span class="mono lc-c">PRÉVIA DO LAYOUT</span><h3 class="xb lc-t">{t}</h3><p class="lc-d">{dsc}</p>'
               f'<a class="lk lc-k" href="https://github.com/jerickprestes/" target="_blank" rel="noopener" aria-label="Acessar projeto {t}">Acessar projeto ↗</a></article>')
    s2.E('div', (36, 160, 699, 340), (24, 228, 366, 320), f'<div class="car-track" id="carTrack">{cs}</div>', 'car', attrs='id="car" role="region" aria-roledescription="carrossel" aria-label="Layouts produzidos" tabindex="0"', base='a')
    s2.mH = 228 + 320 + 28
    # ---- 003 sites
    s3 = Sec(H=498, mH=1180 + 0, attrs='id="sites"')
    # mobile height computed below
    RULE(s3, 0, '#B5B2AA', my=0); MK(s3, '003', 11.5, 14.6); RL(s3, 20.1, 26, 456)
    s3.T((46, 31.5), (24, 51), 'SITES EM QUE<br>TRABALHEI', 'xb', fs=(34, 26), lh=(33, 26), ls=(-.9, -.7), tag='h2')
    s3.T((574, 36.5), (24, 119.5), fmt('Projetos e plataformas web|d desenvolvidos|m focando em|d alta conversão, responsividade| e experiência do usuário.'), 'nw', fs=(9.5, 12), lh=(11, 17))
    sites = [('NutraSolis', 'Loja virtual com WooCommerce, Elementor e Snippets personalizados'),
             ('Imprima.vc', 'Manutenção em páginas e personalização via ACF e Snippets'),
             ('Nexo Varietta', 'Adaptação do layout estático para layout dinâmico e refinamento dos functions.php'),
             ('Dell Anno', 'Correções no SMTP e integração com CRM'),
             ('St. Nicholas School', 'Soluções personalizadas via snippets, integrações com CRM, manutenção em páginas e diversas personalizações no tema'),
             ('TTjus', 'Adaptação do layout estático para layout dinâmico, integrações com CRM e configuração de SMTP'),
             ('LD Administradora', 'Adaptação do layout estático para layout dinâmico, integrações com CRM e configuração de SMTP'),
             ('Craftmania Brasil', 'Adaptação do layout estático para layout dinâmico, integrações com CRM e configuração de SMTP e personalização via functions.php')]
    pal = ['var(--red)', 'var(--blue)', 'var(--yel)', 'var(--lime)']
    ty, rh = 104, 96
    mty, mrh = 196, 100
    s3.R((12, ty, 710, 1), (12, mty, 366, 1), '#8A8A8A')
    s3.R((379, ty, 1, 4 * rh), None, '#8A8A8A')
    for i, (nm, ds) in enumerate(sites):
        r, k = divmod(i, 2)
        x0 = 36 + k * 343; y0 = ty + r * rh; my0 = mty + i * mrh
        if k == 0: s3.R((12, y0 + rh, 710, 1), None, '#8A8A8A')
        s3.R((0, 0, 0, 0), (12, my0 + mrh, 366, 1), '#8A8A8A', cls='mo')
        col = pal[(r + k * 2) % 4]
        s3.T((x0 + 10, y0 + 9.5), (24, my0 + 10.6), f'{i+1:02d}', 'mono', fs=(7.5, 9), lh=(9, 11), tag='span', style='color:#333')
        s3.E('div', (x0 + 10, y0 + 28, 44, 44), (24, my0 + 32, 52, 52), f'<span class="disp lg">{nm[0].upper()}</span>', 'logo', style=f'background:{col}', base='a')
        s3.T((x0 + 66, y0 + 14), (90, my0 + 29), nm, 'xb nw', fs=(14, 16), lh=(16, 18), ls=(-.4,), tag='h3')
        s3.T((x0 + 66, y0 + 32.6, 262), (90, my0 + 49.5, 278), ds, '', fs=(8.8, 11), lh=(10.8, 13), tag='p')
    s3.mH = (mty - 0) + 8 * mrh + 16 + 0
    s3.H = 498
    band = Sec(H=60, mH=140, cls='band on-dark')
    band.R((0, 0, 735, 60), (0, 0, 390, 140), 'var(--blk)')
    MK(band, '004', 11.5, 8.6, color='#DDD')
    for txt, dx, col in (('layouts', 46, '#C9C9C9'), ('sites', 0, '#C9C9C9'), ('code', 0, '#F2FB48')):
        pass
    band.T((46, 18.8), (24, 36), 'layouts', 'disp bw', fs=(25, 16), lh=(25, 16), ls=(.4,), tag='a', style='color:#C9C9C9;--hc:#F72B10', attrs='href="#layouts"')
    band.T((306, 18.8), (168, 36), 'sites', 'disp bw', fs=(25, 16), lh=(25, 16), ls=(.4,), tag='a', style='color:#C9C9C9;--hc:#0373DF', attrs='href="#layouts"')
    band.T((516, 18.8), (282, 36), 'code', 'disp bw', fs=(25, 16), lh=(25, 16), ls=(.4,), tag='a', style='color:#F2FB48;--hc:#fff', attrs='href="#contato"')
    band.R((232, 30.5, 58, 1), (142, 43.2, 16, 1), '#666'); band.R((442, 30.5, 58, 1), (256, 43.2, 16, 1), '#666')
    band.T((627, 8.9), (24, 80.75), 'LAYOUTS RESPONSIVOS<br>E SITES COM FOCO<br>EM CONVERSÃO.', 'mono', fs=(6.8, 8), lh=(8.2, 10.5), style='color:#F2F2F2')
    band.T((627, 38.4), (230, 80.75), 'J. ERICK PRESTES<br>© 2026', 'mono', fs=(6.8, 8), lh=(8.2, 10.5), style='color:#F2F2F2')
    return [s.html(), s2.html(), s3.html(), band.html()]

# ============================================================ GRÁFICO
def grafico_sections():
    T = json.load(open('/home/claude/site/tiles.json'))
    dt, mt = T['513'], T['868']
    dbot = max(y + h for _, _, y, h, _ in dt) + 4
    mbot = max(y + h for _, _, y, h, _ in mt) + 4
    s = Sec(H=int(dbot + 90), mH=int(mbot + 120), attrs='id="grafico"')
    RULE(s, 8)
    MK(s, '001', 19.5, 18.6); RL(s, 20.1, 34, 266)
    s.T((34, 50), (22, 49.6), 'graph', 'disp', fs=(120, 64), lh=(120, 64), ls=(1, .8), tag='h1', style='color:#111')
    s.R((655, 62, 80, 126), (366, 40, 24, 100), 'var(--yel)')
    s.R((560, 214, 70, 70), (290, 112, 56, 56), 'var(--red)')
    s.X(644, 62, 4, 360, 48, 4); s.X(644, 200, 4)
    s.T((43, 219.7), (24, 176), 'Identidade visual, redes sociais, impressos<br>e embalagens: peças criadas em agências<br>e em projetos próprios.', 'nw', fs=(10.5, 14), lh=(12.6, 20), ls=(-.1,))
    s.T((43, 267), (24, 256), 'TRABALHOS SELECIONADOS / 2026<br>SOCIAL · IMPRESSO · IDENTIDADE VISUAL', 'mono', fs=(7, 8.5), lh=(9.7, 12))
    s.E('a', (43, 295), None, 'Ver trabalhos selecionados ↘', 'lk', fs=(9.5,), lh=(11.4,), attrs='href="#projetos"')
    s.T((662, 271.75), (24, 294), '19 PROJETOS<br class="dm">PUBLICADOS', 'mono', fs=(6.8, 8.5), lh=(8.5, 12))
    s.items[-1] = s.items[-1].replace('19 PROJETOS<br class="dm">PUBLICADOS', '19 PROJETOS<span class="dm"><br></span><span class="mo"> </span>PUBLICADOS')
    RULE(s, 330, my=330)
    MK(s, '002', 341.5, 338.6)
    RL(s, 20.1, 356, int(dbot + 10) - 356)
    s.T((46, 361.5), (24, 381), 'PROJETOS<br>GRÁFICOS', 'xb', fs=(34, 26), lh=(33, 26), ls=(-.9, -.7), tag='h2', attrs='id="projetos"')
    s.T((574, 366.5), (24, 453.5), fmt('Mosaico com os projetos|d publicados:|m identidade visual,|d campanhas e|m peças gráficas.'), 'nw', fs=(9.5, 12), lh=(11, 17))
    s.T((46, 439.2), (24, 524.5), '19 / 19', 'mono', fs=(8, 9), lh=(9.6, 11), tag='span')
    s.R((100, 449.05, 606, .9), (70, 534.55, 296, .9), '#444')
    s.E('div', (699, 445.5, 8, 8), (359, 531, 8, 8), '<svg viewBox="0 0 8 8" fill="none" stroke="#444" stroke-width=".9"><path d="M0 0.2L7 4L0 7.8"/></svg>', '')
    RULE(s, 460, '#B5B2AA', my=570)
    cw_d, cw_m = 168.5, 169
    for (n_, x, y, h, col), (_, mx_, my_, mh_, mcol) in zip(dt, mt):
        dark = col == '#0B0B0B'
        tc = '#fff' if dark else '#111'
        mtc = '#fff' if mcol == '#0B0B0B' else '#111'
        st = f'background:{col};' + ('border:.6rem solid #111;' if col == '#FFFFFF' else '') + f'--tc:{tc};--mtc:{mtc};--mbg:{mcol};' + ('--msh:inset 0 0 0 .6px #111;' if mcol == '#FFFFFF' else '')
        inner = (f'<span class="mono t-l">PROJETO</span><span class="disp t-n">{n_:02d}</span><span class="t-a">→</span>')
        s.raw(f'<a class="tile" href="#" style="--x:{n(x)};--y:{n(y-0)};--w:{cw_d};--h:{n(h)};--mx:{n(mx_)};--my:{n(my_)};--mw:{cw_m};--mh:{n(mh_)};{st}" aria-label="Projeto {n_:02d}">{inner}</a>')
    s.E('a', (36, dbot + 17.8), (24, mbot + 18.5), 'VER TODOS OS PROJETOS', 'mono', fs=(7, 9), lh=(8.4, 11), style='color:#333', attrs='href="#"')
    s.R((36, dbot + 40, 686, 1), (24, mbot + 46, 342, 1), '#B5B2AA')
    return [s.html()]

# ============================================================ CONTATO
def contato_sections():
    s = Sec(H=259.5, mH=250, attrs='id="contato"')
    RULE(s, 8)
    MK(s, '001', 19.5, 18.6); RL(s, 20.1, 34, 225.5)
    s.T((34, 53.2), (22, 55.4), 'contato', 'disp', fs=(88, 46), lh=(88, 46), ls=(.8, .6), tag='h1', style='color:#111')
    s.R((669, 110, 66, 100), (366, 120, 24, 110), 'var(--yel)')
    s.X(None, None, None, 358, 112, 4)
    s.T((43, 169.7), (24, 132), 'Vamos conversar sobre o seu próximo projeto: sites, layouts e peças gráficas.', 'nw', fs=(10.5, 14), lh=(12.6, 20), ls=(-.1,))
    s.items[-1] = s.items[-1].replace('próximo projeto:', 'próximo<span class="dm"> </span><span class="mo"><br></span>projeto:')
    s.T((43, 201.8), (24, 194), 'RETORNO POR E-MAIL OU WHATSAPP', 'mono', fs=(7, 8.5), lh=(8.4, 12))
    s2 = Sec(H=190, mH=410)
    RULE(s2, 0, my=0); MK(s2, '002', 12, 8.6); RL(s2, 20.1, 26.5, 144)
    s2.T((46, 43.5), (24, 49.5), 'VAMOS CONSTRUIR ALGO', 'xb nw', fs=(36, 24), lh=(38, 25), ls=(-1.4, -.7), tag='h2')
    s2.T((46, 81.5), (24, 74.5), 'EXTRAORDINÁRIO.', 'xb nw red', fs=(36, 24), lh=(38, 25), ls=(-1.4, -.7), tag='p')
    s2.E('a', (46, 134.2), (24, 122.2), 'Iniciar um projeto ↗', 'lk', fs=(10.5, 13), lh=(12.6, 15.6), attrs='href="#form-contato"')
    RL(s2, 519.6, 20.5, 170)
    info = [('E-MAIL', 'JERICKPRESTES@GMAIL.COM', 'mailto:jerickprestes@gmail.com'), ('TELEFONE', '(12) 98145-2330', 'tel:+5512981452330'), ('LOCALIZAÇÃO', 'TAUBATÉ / SP / BRASIL', None)]
    for i, (lab, val, href) in enumerate(info):
        s2.R((0, 0, 0, 0), (24, 190 + i * 46 - 10, 342, .8), '#999', cls='mo') if False else None
        s2.T((548, 24.6 + i * 32), (24, 189 + i * 46), lab, 'mono', fs=(6.5, 8), lh=(7.8, 10), tag='span', style='color:#666')
        v = f'<a href="{href}">{val}</a>' if href else val
        s2.T((548, 35 + i * 32), (24, 205.5 + i * 46), v, 'mono', fs=(7.5, 11), lh=(9, 13), tag='span')
        s2.R((0, 0, 0, 0), (24, 190 + i * 46 - 10 + 0, 342, .8), '#999', cls='mo')
    s2.R((548, 120.1, 174, .8), (24, 190 + 3 * 46 - 10, 342, .8), '#999')
    s2.T((548, 128.6), (24, 345), 'REDES', 'mono', fs=(6.5, 8), lh=(7.8, 10), tag='span', style='color:#666')
    s2.T((548, 139.3), (24, 363.5), '<a href="https://www.behance.net/jerickprestes" target="_blank" rel="noopener">BEHANCE</a><br class="dm"><span class="mo">&nbsp;&nbsp; </span><a href="https://www.linkedin.com/in/jerickprestes/" target="_blank" rel="noopener">LINKEDIN</a><br class="dm"><span class="mo">&nbsp;&nbsp; </span><a href="https://github.com/jerickprestes" target="_blank" rel="noopener">GITHUB</a>', 'mono', fs=(7.5, 11), lh=(8.5, 13), tag='span')
    return [s.html(), s2.html()]

if __name__ == '__main__':
    parts = inicio_sections() + experiencia_sections() + web_sections() + grafico_sections() + contato_sections() + [footer().html()]
    open('/home/claude/site/index.html', 'w').write(page('J. Erick Prestes — Web, Gráfico, Tech & Code', '\n'.join(parts),
        'Portfólio de J. Erick Prestes: design gráfico, web design e automação com IA.'))
    print('ok')
