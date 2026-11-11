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
  // formulário: abre o e-mail já preenchido (site estático — troque por seu endpoint/back-end quando houver)
  var form = document.getElementById('form-contato');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = form.querySelector('.ft-msg'), f = form.elements;
      if (!f.nome.value.trim() || !/.+@.+\..+/.test(f.email.value)) {
        msg.textContent = 'Preencha nome e um e-mail válido.'; return;
      }
      var body = 'Nome: ' + f.nome.value + '\nE-mail: ' + f.email.value + '\nTelefone/WhatsApp: ' + f.telefone.value +
        '\nTipo de projeto: ' + f.tipo.value + '\nPrazo desejado: ' + f.prazo.value + '\n\n' + f.mensagem.value;
      msg.textContent = 'Abrindo seu aplicativo de e-mail…';
      window.location.href = 'mailto:jerickprestes@gmail.com?subject=' + encodeURIComponent('Contato pelo site — ' + f.tipo.value) + '&body=' + encodeURIComponent(body);
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
})();
