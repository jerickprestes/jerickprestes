(function () {
  // 1vw sem a barra de rolagem: mantém a página exatamente na largura visível
  function setVw() { document.documentElement.style.setProperty('--vw', (document.documentElement.clientWidth / 100) + 'px'); }
  setVw(); window.addEventListener('resize', setVw); window.addEventListener('load', setVw);
  // menu mobile
  var hd = document.querySelector('.hd'), btn = document.querySelector('.menu-btn');
  if (btn) {
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open);
      btn.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    });
    document.querySelectorAll('.navwrap a').forEach(function (a) {
      a.addEventListener('click', function () { document.body.classList.remove('menu-open'); });
    });
  }
  // formulário: monta a mensagem e abre o WhatsApp (wa.me) já preenchida — site estático, sem back-end
  var WA_NUMERO = '5512981452330';   // (12) 98145-2330 — formato internacional, só dígitos
  var form = document.getElementById('form-contato');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.ft-msg'), f = form.elements;
      if (!f.nome.value.trim()) { msg.textContent = 'Preencha seu nome.'; f.nome.focus(); return; }
      if (f.email.value.trim() && !/.+@.+\..+/.test(f.email.value)) { msg.textContent = 'Confira o e-mail digitado.'; f.email.focus(); return; }
      var L = ['Olá, Erick! Vim pelo seu site e gostaria de conversar sobre um projeto.', '',
        '*Nome:* ' + f.nome.value.trim()];
      if (f.email.value.trim()) L.push('*E-mail:* ' + f.email.value.trim());
      if (f.telefone.value.trim()) L.push('*Telefone/WhatsApp:* ' + f.telefone.value.trim());
      L.push('*Tipo de projeto:* ' + f.tipo.value, '*Prazo desejado:* ' + f.prazo.value);
      if (f.mensagem.value.trim()) L.push('', '*Sobre o projeto:*', f.mensagem.value.trim());
      var url = 'https://wa.me/' + WA_NUMERO + '?text=' + encodeURIComponent(L.join('\n'));
      msg.textContent = 'Abrindo o WhatsApp…';
      if (!window.open(url, '_blank', 'noopener')) window.location.href = url;   // se o navegador bloquear a nova aba
    });
  }

  // ---------- motor de carrossel arrastável e infinito (mouse/touch, inércia, encaixe, setas, teclado) ----------
  // O trilho recebe 2 cópias extras dos slides (antes e depois). A posição é "dobrada" de volta para o conjunto do meio
  // sempre que sai dele, então o loop não tem fim nem pulo visível.
  function initCar(car, track, o) {
    o = o || {};
    var n = track.children.length;
    for (var k = 0; k < 2; k++) {
      for (var m = 0; m < n; m++) {
        var cl = track.children[m].cloneNode(true); cl.setAttribute('aria-hidden', 'true');
        cl.querySelectorAll('a,button').forEach(function (e) { e.tabIndex = -1; });
        track.appendChild(cl);
      }
    }
    var cards = track.children, x = 0, target = 0, dragging = false, startX = 0, startPos = 0, lastX = 0, lastT = 0, vel = 0, moved = 0, raf = null, ci = 0;
    function step() { return cards[1].offsetLeft - cards[0].offsetLeft; }
    function per() { return n * step(); }
    function wrap() {   // mantém x no conjunto do meio: (-2P, -P]
      var P = per(); if (!P) return;
      while (x > -P) { x -= P; target -= P; startPos -= P; }
      while (x <= -2 * P) { x += P; target += P; startPos += P; }
    }
    function idx() { var s = step(); return s ? (((Math.round((-x - per()) / s)) % n) + n) % n : 0; }
    function ui() { ci = idx(); if (o.cur) o.cur.textContent = (ci < 9 ? '0' : '') + (ci + 1); }
    function paint() { track.style.transform = 'translate3d(' + x + 'px,0,0)'; }
    function tick() {
      x += (target - x) * (dragging ? 0.5 : 0.14);
      if (Math.abs(target - x) < 0.3) { x = target; raf = null; } else raf = requestAnimationFrame(tick);
      wrap(); paint(); ui();
    }
    function go(t) { target = t; if (!raf) raf = requestAnimationFrame(tick); }
    function snap(v) { var s = step(); return -Math.round(-v / s) * s; }
    function to(i) { go(-per() - (((i % n) + n) % n) * step()); }
    function move(d) { go(snap(x + d * step() * 0.6)); }
    car.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      if (e.target.closest && e.target.closest('button')) return;
      dragging = true; moved = 0; startX = lastX = e.clientX; startPos = x; lastT = performance.now(); vel = 0;
      car.setPointerCapture(e.pointerId);
    });
    car.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var dx = e.clientX - startX; moved = Math.max(moved, Math.abs(dx));
      if (moved > 4) car.classList.add('dragging');
      var now = performance.now(), dt = Math.max(1, now - lastT);
      vel = 0.8 * vel + 0.2 * ((e.clientX - lastX) / dt); lastX = e.clientX; lastT = now;
      target = startPos + dx; if (!raf) raf = requestAnimationFrame(tick);
    });
    function end() {
      if (!dragging) return; dragging = false;
      go(snap(x + vel * 220));   // inércia + encaixe
      setTimeout(function () { car.classList.remove('dragging'); }, 0);
    }
    car.addEventListener('pointerup', end); car.addEventListener('pointercancel', end);
    car.addEventListener('click', function (e) { if (moved > 4) { e.preventDefault(); e.stopPropagation(); } }, true);
    car.addEventListener('dragstart', function (e) { e.preventDefault(); });
    if (o.prev) o.prev.addEventListener('click', function () { move(1); });
    if (o.next) o.next.addEventListener('click', function () { move(-1); });
    car.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); move(-1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); move(1); }
    });
    function refit() { x = target = -per() - ci * step(); paint(); ui(); }
    window.addEventListener('resize', refit); window.addEventListener('load', refit); refit();
    return { to: to, idx: idx, next: function () { to(idx() + 1); }, count: function () { return n; }, refit: refit };
  }

  // ---------- carrossel de layouts + thumbnail que desliza no hover ----------
  var car = document.getElementById('car'), track = document.getElementById('carTrack');
  if (car && track) {
    initCar(car, track, { cur: document.getElementById('carCur'), prev: document.getElementById('carPrev'), next: document.getElementById('carNext') });
    function measure() {
      track.querySelectorAll('.lc-p').forEach(function (box) {
        var im = box.querySelector('img'); if (!im || !im.naturalWidth) return;
        var dist = Math.max(0, im.getBoundingClientRect().height - box.clientHeight);
        box.style.setProperty('--dist', dist + 'px');
        box.style.setProperty('--dur', Math.min(9, Math.max(3, dist / 110)) + 's');
      });
    }
    track.querySelectorAll('img').forEach(function (im) { im.addEventListener('load', measure); });
    window.addEventListener('resize', measure); window.addEventListener('load', measure); measure();
  }

  // ---------- carrossel da hero (web / graph / tech / code) ----------
  var hc = document.getElementById('heroCar'), ht = document.getElementById('heroTrack');
  if (hc && ht) {
    var H = initCar(hc, ht);
    hc.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.hs-n'); if (b) H.next(); });
    // troca automática: cada slide fica parado AUTO_MS e então avança; arrastar/clicar/teclar reinicia a contagem
    var AUTO_MS = 6000, autoT = null, held = false;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion:reduce)').matches;
    function arm() {
      clearTimeout(autoT); if (reduce) return;
      autoT = setTimeout(function () {
        if (!document.hidden && !held && !hc.classList.contains('dragging')) H.next();
        arm();
      }, AUTO_MS);
    }
    hc.addEventListener('pointerdown', function () { held = true; clearTimeout(autoT); });
    ['pointerup', 'pointercancel'].forEach(function (ev) { window.addEventListener(ev, function () { if (held) { held = false; arm(); } }); });
    hc.addEventListener('click', arm); hc.addEventListener('keydown', arm);
    document.addEventListener('visibilitychange', arm);
    arm();
  }

  // ---------- lightbox dos projetos (mosaico "Projetos gráficos") ----------
  var dataEl = document.getElementById('bhData'), lb = document.getElementById('lb');
  if (dataEl && lb) {
    var P = JSON.parse(dataEl.textContent), cur = -1, lastFocus = null;
    var lbGrid = document.getElementById('lbGrid'), lbBody = document.getElementById('lbBody'), lbTitle = document.getElementById('lbTitle'),
        lbNum = document.getElementById('lbNum'), lbBe = document.getElementById('lbBe'), lbPrev = document.getElementById('lbPrev'),
        lbNext = document.getElementById('lbNext'), lbClose = document.getElementById('lbClose');
    function pad(n) { return (n < 10 ? '0' : '') + n; }
    var mqW = window.matchMedia('(min-width:1101px)'), mqM = window.matchMedia('(max-width:560px)');
    function colCount(n) { return Math.min(n, mqM.matches ? 2 : (mqW.matches ? 3 : 2)); }
    function fill() {
      var p = P[cur], k = colCount(p.i.length), cols = [], h = [], i;
      lbGrid.innerHTML = ''; lbGrid.className = 'lb-grid' + (p.i.length === 1 ? ' n1' : p.i.length === 2 ? ' n2' : ''); lbGrid.setAttribute('data-k', k);
      for (i = 0; i < k; i++) { var c = document.createElement('div'); c.className = 'lb-col'; lbGrid.appendChild(c); cols.push(c); h.push(0); }
      var pend = p.i.length, bad = 0;
      function chk() {
        if (--pend || bad !== p.i.length) return;
        var m = document.createElement('p'); m.className = 'lb-empty mono';
        m.innerHTML = 'As imagens deste projeto não foram encontradas em <b>img/behance/' + p.id + '/</b>.<br>Rode <b>python3 baixar-capas-behance.py</b> na pasta do site (uma vez) e recarregue a página.';
        lbGrid.appendChild(m); if (window.console) console.warn('[lightbox] arquivos ausentes: ' + p.i[0][0]);
      }
      p.i.forEach(function (im) {      // masonry: cada imagem vai para a coluna mais baixa (mantém a ordem de leitura)
        var m = h.indexOf(Math.min.apply(null, h)), el = new Image();
        el.alt = p.t; el.draggable = false; el.decoding = 'async'; el.loading = 'lazy';
        el.style.aspectRatio = '100 / ' + im[1];
        el.onload = function () { el.classList.add('ok'); chk(); }; el.onerror = function () { el.remove(); bad++; chk(); };
        el.src = im[0]; cols[m].appendChild(el); h[m] += im[1] + 3;
      });
    }
    function render(i) {
      cur = (i + P.length) % P.length; var p = P[cur];
      lbTitle.textContent = p.t; lbNum.textContent = 'PROJETO ' + pad(cur + 1) + ' / ' + P.length; lbBe.href = p.u;
      fill(); lbBody.scrollTop = 0;
    }
    window.addEventListener('resize', function () {
      if (lb.classList.contains('on') && +lbGrid.getAttribute('data-k') !== colCount(P[cur].i.length)) { var s = lbBody.scrollTop; fill(); lbBody.scrollTop = s; }
    });
    function openLb(i) {
      lastFocus = document.activeElement; render(i);
      lb.classList.add('on'); lb.setAttribute('aria-hidden', 'false'); document.documentElement.style.overflow = 'hidden';
      lbClose.focus();
    }
    function closeLb() {
      lb.classList.remove('on'); lb.setAttribute('aria-hidden', 'true'); document.documentElement.style.overflow = '';
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('.tile[data-i]');
      if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault(); openLb(+a.getAttribute('data-i'));
    });
    lbClose.addEventListener('click', closeLb);
    lbPrev.addEventListener('click', function () { render(cur - 1); });
    lbNext.addEventListener('click', function () { render(cur + 1); });
    lbBody.addEventListener('click', function (e) { if (e.target === lbBody) closeLb(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') closeLb();
      else if (e.key === 'ArrowLeft') render(cur - 1);
      else if (e.key === 'ArrowRight') render(cur + 1);
      else if (e.key === 'Tab') {
        var f = [lbBe, lbPrev, lbNext, lbClose], i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
  }

  // ---------- leitor de artigos (seções Tech / IA) ----------
  var pb = document.getElementById('pb'), pdEl = document.getElementById('pbData');
  if (pb && pdEl) {
    var PD = JSON.parse(pdEl.textContent), pk = '', pi = 0, pLast = null;
    var pbTitle = document.getElementById('pbTitle'), pbKick = document.getElementById('pbKick'), pbArt = document.getElementById('pbArt'),
        pbBody = document.getElementById('pbBody'), pbPrev = document.getElementById('pbPrev'), pbNext = document.getElementById('pbNext'), pbClose = document.getElementById('pbClose');
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function showPost(k, i) {
      var L = PD[k]; if (!L || !L.length) return;
      pk = k; pi = (i + L.length) % L.length; var p = L[pi];
      pbKick.textContent = (k === 'ia' ? 'IA' : 'TECH') + ' · ' + p.d + (p.draft ? ' · RASCUNHO' : '') + '  (' + (pi + 1) + '/' + L.length + ')';
      pbTitle.textContent = p.t;
      var ban = '<div class="pb-ban' + (p.c ? ' cv' : '') + '" style="--c:' + esc(p.col || '#ddd') + ';--tc:' + esc(p.tc || '#111') + '">' +
        (p.c ? '<img src="' + esc(p.c) + '" alt="" draggable="false" onerror="this.parentNode.classList.remove(\'cv\');this.remove()">' : '') +
        '<span class="mono pb-l">' + (k === 'ia' ? 'IA' : 'TECH') + '</span><span class="pb-n">' + esc(p.n || '') + '</span></div>';
      pbArt.innerHTML = ban + '<div class="art-tags">' + p.g.map(function (t) { return '<span>' + esc(t) + '</span>'; }).join('') + '</div>' + p.h;
      pbBody.scrollTop = 0;
    }
    function openPost(k, i) {
      pLast = document.activeElement; showPost(k, i);
      pb.classList.add('on'); pb.setAttribute('aria-hidden', 'false'); document.documentElement.style.overflow = 'hidden'; pbClose.focus();
    }
    function closePost() {
      pb.classList.remove('on'); pb.setAttribute('aria-hidden', 'true'); document.documentElement.style.overflow = '';
      if (pLast && pLast.focus) pLast.focus();
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('.pc[data-p]');
      if (a && !(e.button || e.metaKey || e.ctrlKey || e.shiftKey)) { e.preventDefault(); var s = a.getAttribute('data-p').split(':'); openPost(s[0], +s[1]); return; }
      var l = e.target.closest && pb.classList.contains('on') && e.target.closest('#pbArt a[href^="#"]');   // links internos (#grafico…) fecham o leitor
      if (l) closePost();
    });
    pbClose.addEventListener('click', closePost);
    pbPrev.addEventListener('click', function () { showPost(pk, pi - 1); });
    pbNext.addEventListener('click', function () { showPost(pk, pi + 1); });
    pbBody.addEventListener('click', function (e) { if (e.target === pbBody) closePost(); });
    document.addEventListener('keydown', function (e) {
      if (!pb.classList.contains('on')) return;
      if (e.key === 'Escape') closePost();
      else if (e.key === 'ArrowLeft') showPost(pk, pi - 1);
      else if (e.key === 'ArrowRight') showPost(pk, pi + 1);
      else if (e.key === 'Tab') {
        var f = [pbPrev, pbNext, pbClose], i = f.indexOf(document.activeElement);
        if (e.shiftKey && i <= 0) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && i === f.length - 1) { e.preventDefault(); f[0].focus(); }
      }
    });
  }

  // ---------- contato em painel (off-canvas, sobe de baixo para cima) ----------
  var cp = document.getElementById('cp');
  if (cp) {
    var cpClose = document.getElementById('cpClose'), cpBody = document.getElementById('cpBody'), cpLast = null;
    var cpFocusable = function () { return Array.prototype.slice.call(cp.querySelectorAll('a[href],button,input,select,textarea')).filter(function (el) { return !el.disabled && el.offsetParent !== null; }); };
    var gotoForm = function () {
      var f = document.getElementById('form-contato'); if (!f) return;
      cpBody.scrollTo({ top: f.getBoundingClientRect().top - cpBody.getBoundingClientRect().top + cpBody.scrollTop - 40, behavior: 'smooth' });
      var i = f.querySelector('input'); if (i) i.focus({ preventScroll: true });
    };
    var openCp = function () {
      if (cp.classList.contains('on')) return;
      cpLast = document.activeElement; document.body.classList.remove('menu-open');
      cp.classList.add('on'); cp.setAttribute('aria-hidden', 'false'); document.documentElement.style.overflow = 'hidden';
      cpBody.scrollTop = 0; cpClose.focus({ preventScroll: true });
    };
    var closeCp = function () {
      if (!cp.classList.contains('on')) return;
      cp.classList.remove('on'); cp.setAttribute('aria-hidden', 'true'); document.documentElement.style.overflow = '';
      if (location.hash === '#contato') history.replaceState(null, '', location.pathname + location.search);
      if (cpLast && cpLast.focus) cpLast.focus({ preventScroll: true });
    };
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href]'); if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var h = a.getAttribute('href');
      if (h === '#contato') { e.preventDefault(); openCp(); return; }
      if (cp.classList.contains('on') && cp.contains(a)) {
        if (h === '#form-contato') { e.preventDefault(); gotoForm(); }
        else if (h.charAt(0) === '#') closeCp();             // links internos (#topo, #tech…) fecham o painel e seguem para a seção
      }
    });
    cpClose.addEventListener('click', closeCp);
    cp.addEventListener('click', function (e) { if (e.target === cp) closeCp(); });
    document.addEventListener('keydown', function (e) {
      if (!cp.classList.contains('on')) return;
      if (e.key === 'Escape') closeCp();
      else if (e.key === 'Tab') {
        var f = cpFocusable(); if (!f.length) return;
        if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
        else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
      }
    });
    window.addEventListener('hashchange', function () { if (location.hash === '#contato') openCp(); });
    if (location.hash === '#contato') openCp();
  }

  // ---------- navbar do mobile: recolhe ao rolar para baixo e reaparece ao rolar para cima ----------
  (function () {
    var lastY = window.pageYOffset || 0, tick = false;
    function update() {
      tick = false;
      var y = Math.max(0, window.pageYOffset || 0), d = y - lastY;
      if (document.body.classList.contains('menu-open') || y < 60) document.body.classList.remove('nav-hide');
      else if (d > 6) document.body.classList.add('nav-hide');
      else if (d < -6) document.body.classList.remove('nav-hide');
      if (Math.abs(d) > 6) lastY = y;
    }
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(update); } }, { passive: true });
    document.addEventListener('focusin', function (e) { if (e.target.closest && e.target.closest('.hd')) document.body.classList.remove('nav-hide'); });
  })();
})();
