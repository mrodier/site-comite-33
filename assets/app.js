/* Site du CD33 : menu, clubs par district (clubs.html), zone documents (documents.html)
   et assistant (assistant.html). L'assistant cherche dans data/kb.json et data/documents.json ;
   sans relais IA configuré (assets/config.js), il affiche les passages les plus pertinents avec leur source. */
(function () {
  "use strict";
  const CONFIG = window.SITE_CONFIG || {};
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = (u) => (/^https:\/\//.test(u) ? u : "#");
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

  /* ---------- Menu ---------- */
  const topbar = $("#topbar"), toggle = $("#menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      const open = !topbar.classList.contains("open");
      topbar.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && topbar.classList.contains("open")) { topbar.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); toggle.focus(); } });
  }
  /* Sous-menus : survol sur ordinateur (CSS), bouton chevron au clavier et dans le tiroir mobile */
  const subs = [...document.querySelectorAll(".mi.has-sub")];
  const closeSubs = (except) => subs.forEach((li) => { if (li !== except) { li.classList.remove("sub-open"); li.querySelector(".sub-toggle").setAttribute("aria-expanded", "false"); } });
  subs.forEach((li) => {
    const b = li.querySelector(".sub-toggle");
    b.addEventListener("click", (e) => { e.stopPropagation(); const open = !li.classList.contains("sub-open"); closeSubs(li); li.classList.toggle("sub-open", open); b.setAttribute("aria-expanded", String(open)); });
    li.addEventListener("keydown", (e) => { if (e.key === "Escape" && li.classList.contains("sub-open")) { closeSubs(); b.focus(); e.stopPropagation(); } });
  });
  document.addEventListener("click", (e) => { if (!e.target.closest(".mi.has-sub")) closeSubs(); });


  /* ---------- Carrousel ---------- */
  document.querySelectorAll("[data-carousel]").forEach((root) => {
    const track = root.querySelector(".slides"), slides = [...track.children], dots = [...root.querySelectorAll(".dot")];
    const section = root.closest("section");
    let i = 0, timer = null;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const go = (n, smooth = true) => {
      const perView = Math.max(1, Math.round(track.clientWidth / slides[0].offsetWidth)); const last = slides.length - perView; i = n > last ? (n === i + 1 ? 0 : last) : n < 0 ? last : n;
      track.scrollTo({ left: slides[i].offsetLeft - track.offsetLeft, behavior: smooth && !reduce ? "smooth" : "auto" });
      dots.forEach((d, k) => d.setAttribute("aria-current", String(k === i)));
    };
    dots.forEach((d, k) => d.addEventListener("click", () => { stop(); go(k); }));
    section.querySelectorAll(".cbtn").forEach((b) => b.addEventListener("click", () => { stop(); go(i + Number(b.dataset.dir)); }));
    let t;
    track.addEventListener("scroll", () => { clearTimeout(t); t = setTimeout(() => {
      const step = slides[1] ? slides[1].offsetLeft - slides[0].offsetLeft : track.clientWidth; const k = Math.round(track.scrollLeft / step);
      if (k !== i && slides[k]) { i = k; dots.forEach((d, j) => d.setAttribute("aria-current", String(j === i))); }
    }, 80); }, { passive: true });
    const start = () => { if (!reduce && !timer) timer = setInterval(() => go(i + 1), 6000); };
    const stop = () => { clearInterval(timer); timer = null; };
    root.addEventListener("mouseenter", stop); root.addEventListener("mouseleave", start);
    root.addEventListener("focusin", stop); root.addEventListener("touchstart", stop, { passive: true });
    start();
  });

  const needAsk = !!$("#ask-form"), needDocs = !!$("#doc-list") && !!$("#doc-filters"), needClubs = !!$("#districts");
  if (!needAsk && !needDocs && !needClubs) return;

  /* ---------- Recherche plein texte (BM25) ---------- */
  const STOP = new Set("les des une un du de la le et en au aux pour par sur dans est sont que qui quoi quel quelle quels quelles comment combien quand ou avec pas plus ce cette ces son sa ses leur leurs mon ma mes nous vous il elle ils elles on je tu faire fait peut doit doivent etre avoir y a ne se si tout tous toute toutes".split(" "));
  const toks = (s) => norm(s).split(/[^a-z0-9]+/).filter((w) => w.length > 1 && !STOP.has(w)).map((w) => (w.length > 4 && w.endsWith("s") ? w.slice(0, -1) : w));
  let INDEX = [], DF = new Map(), AVG = 1;
  function buildIndex(kb, docs) {
    INDEX = kb.map((p) => ({ kind: "Page du site", t: p.t, u: p.u, x: p.c }));
    docs.chunks.forEach((c) => { const d = docs.docs[c.d]; INDEX.push({ kind: "Document", t: d.t, u: d.u, x: c.x }); });
    DF = new Map(); let total = 0;
    INDEX.forEach((e) => {
      e.tf = new Map();
      const tt = toks(e.t), all = tt.concat(tt, toks(e.x));
      e.len = all.length; total += all.length;
      all.forEach((w) => e.tf.set(w, (e.tf.get(w) || 0) + 1));
      e.tf.forEach((_, w) => DF.set(w, (DF.get(w) || 0) + 1));
    });
    AVG = total / Math.max(INDEX.length, 1);
  }
  function search(q, k) {
    const qs = [...new Set(toks(q))], N = INDEX.length;
    return INDEX.map((e) => {
      let s = 0;
      for (const w of qs) {
        const f = e.tf.get(w); if (!f) continue;
        const idf = Math.log(1 + (N - DF.get(w) + 0.5) / (DF.get(w) + 0.5));
        s += idf * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * e.len / AVG));
      }
      return { e, s };
    }).filter((r) => r.s > 0).sort((a, b) => b.s - a.s).slice(0, k).map((r) => r.e);
  }
  function snippet(text, q) {
    const words = toks(q);
    const sentences = text.split(/(?<=[.!?;])\s+|\n+/).filter(Boolean);
    const scored = sentences.map((s, i) => ({ i, s, n: words.filter((w) => norm(s).includes(w)).length })).sort((a, b) => b.n - a.n || a.i - b.i);
    const best = scored.slice(0, 3).sort((a, b) => a.i - b.i).map((x) => x.s).join(" ");
    let out = esc(best.length > 520 ? best.slice(0, 520) + "…" : best);
    words.filter((w) => w.length > 2).forEach((w) => {
      out = out.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "[a-zà-ÿ]*)", "gi"), "<mark>$1</mark>");
    });
    return out.replace(/(https:\/\/[^\s<]+[^\s<.,;:)])/g, '<a href="$1" target="_blank" rel="noopener">lien</a>');
  }
  function fmt(text) {
    const lines = esc(text).split(/\n/); let html = "", list = false;
    for (let l of lines) {
      l = l.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>").replace(/(https:\/\/[^\s<)]+[^\s<).,;:!?])/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
      const m = l.match(/^\s*[-•*]\s+(.*)/);
      if (m) { if (!list) { html += "<ul>"; list = true; } html += "<li>" + m[1] + "</li>"; continue; }
      if (list) { html += "</ul>"; list = false; }
      if (l.trim()) html += "<p>" + l + "</p>";
    }
    return html + (list ? "</ul>" : "");
  }

  /* ---------- Assistant ---------- */
  let ask = () => {};
  if (needAsk) {
    const SUGG = ["Combien coûte une licence U13 ?", "Comment inscrire une équipe en 3x3 ?", "Comment devenir arbitre ?", "Quelle est l'amende pour un forfait en seniors ?", "Quand ont lieu les finales des Coupes 33 ?", "Quel brevet pour entraîner des U11 ?"];
    const input = $("#ask-q"), answer = $("#answer");
    $("#suggest").innerHTML = SUGG.map((s, i) => `<button type="button" data-i="${i}">${esc(s)}</button>`).join("");
    $("#suggest").addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) { input.value = SUGG[b.dataset.i]; ask(input.value); } });
    $("#ask-form").addEventListener("submit", (e) => { e.preventDefault(); ask(input.value); });
    function renderHits(q, hits, intro) {
      if (!hits.length) {
        answer.innerHTML = `<p class="ans-intro">Je n'ai rien trouvé à ce sujet dans les pages et documents du comité. Contactez le secrétariat : <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a> · 06 19 86 37 71.</p>`;
        return;
      }
      answer.innerHTML = `<p class="ans-intro">${esc(intro)}</p>` + hits.map((h) => `<article class="hit"><span class="hit-kind">${esc(h.kind)}</span><h3>${esc(h.t)}</h3><p>${snippet(h.x, q)}</p><a href="${esc(safeUrl(h.u))}" target="_blank" rel="noopener">Ouvrir la source</a></article>`).join("");
    }
    let busy = false;
    ask = async function (q) {
      q = (q || "").trim();
      if (!q || busy) return;
      if (!INDEX.length) { answer.innerHTML = `<p class="ans-intro">Chargement des documents…</p>`; pending = q; return; }
      const hits = search(q, 6);
      if (!CONFIG.assistantEndpoint) { renderHits(q, hits.slice(0, 3), "Voici les passages des documents officiels qui répondent le mieux à votre question :"); return; }
      busy = true;
      answer.innerHTML = `<p class="ans-intro">Je cherche dans les documents du comité…</p>`;
      try {
        const r = await fetch(CONFIG.assistantEndpoint, {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: q, context: hits.map((h) => ({ titre: h.t, source: h.u, texte: h.x.slice(0, 2500) })) })
        });
        if (!r.ok) throw new Error("HTTP " + r.status);
        const data = await r.json();
        if (!data || typeof data.answer !== "string") throw new Error("format");
        answer.innerHTML = `<div class="ans-text">${fmt(data.answer)}</div>`;
      } catch (err) {
        renderHits(q, hits.slice(0, 3), "L'assistant ne peut pas rédiger de réponse pour le moment. Voici les passages les plus pertinents :");
      } finally { busy = false; }
    };
  }
  let pending = new URLSearchParams(location.search).get("q") || "";
  if (pending && needAsk) $("#ask-q").value = pending;

  /* ---------- Clubs ---------- */
  function renderDistricts(kb) {
    const ds = kb.filter((p) => /^Clubs du district/.test(p.t));
    $("#districts").innerHTML = ds.map((d) => {
      const name = d.t.replace(/^Clubs du district (de |du )?/, "");
      const clubs = d.c.replace(/\([^)]*\)/g, "").replace(/\.$/, "").split(/,\s*/).map((s) => s.trim()).filter(Boolean);
      return `<details class="district"><summary><h3>${esc(name)}</h3><span>${clubs.length} clubs</span></summary><ul>${clubs.map((c) => `<li>${esc(c)}</li>`).join("")}</ul></details>`;
    }).join("");
  }

  /* ---------- Ressources documentaires ----------
     data/catalogue.json : tous les documents présents sur le site (titre t, lien u, catégorie cat, type k,
     pages où il apparaît p, index i dans documents.json pour le texte intégral). */
  const CAT_ORDER = ["Règlements", "Compétitions", "Mini-basket", "Clubs et licences", "Formations et officiels", "Finances", "Le CD33", "Notes du comité"];
  const slugCat = (c) => norm(c).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const HASH_ALIAS = { "clubs-licences": "clubs-et-licences", "formations": "formations-et-officiels", "notes": "notes-du-comite" };
  function renderDocs(cat0, docs) {
    const text = {};
    (docs.chunks || []).forEach((c) => { text[c.d] = (text[c.d] || "") + " " + c.x; });
    const items = cat0.docs.map((d) => {
      const full = d.i != null ? text[d.i] || "" : "";
      const dash = (s) => s + " " + s.replace(/[-'’]/g, ""); /* « ré-affiliation » se trouve aussi en tapant « reaffiliation » */
      return { ...d, full, head: dash(norm([d.t, d.cat, d.k, ...d.p.map((x) => x[1])].join(" "))), body: dash(norm(full)) };
    });
    const cats = [...new Set([...CAT_ORDER.filter((c) => items.some((d) => d.cat === c)), ...items.map((d) => d.cat)])];
    const list = $("#doc-list"), q = $("#doc-q"), filters = $("#doc-filters"), count = $("#doc-count"), sort = $("#doc-sort");
    const h = location.hash.slice(1);
    let cat = cats.find((c) => slugCat(c) === (HASH_ALIAS[h] || h)) || "Tous";
    const params = new URLSearchParams(location.search);
    if (params.get("q")) q.value = params.get("q");
    function drawFilters(counts) {
      filters.innerHTML = ["Tous", ...cats].map((c) => `<button type="button" data-c="${esc(c)}" aria-pressed="${c === cat}">${esc(c)} <span class="n">${counts[c] || 0}</span></button>`).join("");
    }
    function excerpt(d, words) {
      const src = d.full.replace(/\s+/g, " ");
      const n = norm(src);
      let pos = -1; for (const w of words) { pos = n.indexOf(w); if (pos >= 0) break; }
      if (pos < 0) return "";
      const a = Math.max(0, pos - 90), b = Math.min(src.length, pos + 140);
      let out = esc((a ? "…" : "") + src.slice(a, b) + (b < src.length ? "…" : ""));
      words.filter((w) => w.length > 2).forEach((w) => { out = out.replace(new RegExp("(" + w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "[a-z0-9]*)", "gi"), "<mark>$1</mark>"); });
      return out;
    }
    function card(d, words) {
      const where = d.p.length
        ? "Sur le site : " + d.p.map(([s, t]) => `<a href="${esc(s)}.html">${esc(t)}</a>`).join(", ")
        : "Disponible uniquement dans les ressources documentaires";
      const inText = words.length && !words.every((w) => d.head.includes(w));
      return `<article class="res-item">
        <div class="res-main"><p class="res-meta"><span class="res-kind">${esc(d.k)}</span><span>${esc(d.cat)}</span></p>
        <h3><a href="${esc(safeUrl(d.u))}" target="_blank" rel="noopener">${esc(d.t)}</a></h3>
        ${inText ? `<p class="res-ex"><span>Trouvé dans le texte :</span> ${excerpt(d, words)}</p>` : ""}
        <p class="res-where">${where}</p></div>
        <a class="res-open" href="${esc(safeUrl(d.u))}" target="_blank" rel="noopener" aria-label="Ouvrir : ${esc(d.t)}">Ouvrir ↗</a>
      </article>`;
    }
    function draw() {
      const words = toks(q.value);
      const matched = items.map((d) => {
        if (!words.length) return { d, s: 1 };
        let s = 0;
        for (const w of words) { if (d.head.includes(w)) s += 3; else if (d.body.includes(w)) s += 1; else return null; }
        return { d, s };
      }).filter(Boolean);
      const counts = { Tous: matched.length };
      matched.forEach(({ d }) => { counts[d.cat] = (counts[d.cat] || 0) + 1; });
      drawFilters(counts);
      let rows = matched.filter(({ d }) => cat === "Tous" || d.cat === cat);
      const byTitle = (a, b) => a.d.t.localeCompare(b.d.t, "fr");
      if (words.length) rows.sort((a, b) => b.s - a.s || byTitle(a, b));
      else if (sort.value === "az") rows.sort(byTitle);
      else rows.sort((a, b) => cats.indexOf(a.d.cat) - cats.indexOf(b.d.cat) || byTitle(a, b));
      count.textContent = rows.length + (rows.length > 1 ? " documents" : " document") + (cat !== "Tous" ? " · " + cat : "") + (words.length ? " pour « " + q.value.trim() + " »" : "");
      if (!rows.length) {
        list.innerHTML = `<p class="doc-empty">Aucun document ne correspond${cat !== "Tous" ? " dans cette catégorie" : ""}. Essayez un autre mot, la catégorie « Tous », ou <a href="assistant.html?q=${encodeURIComponent(q.value)}">posez la question à l'assistant</a>.</p>`;
        return;
      }
      let html = "", last = "";
      rows.forEach(({ d }) => {
        if (!words.length && sort.value === "cat" && cat === "Tous" && d.cat !== last) { html += `<h2 class="res-group">${esc(d.cat)}</h2>`; last = d.cat; }
        html += card(d, words);
      });
      list.innerHTML = html;
    }
    filters.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      cat = b.dataset.c;
      history.replaceState(null, "", cat === "Tous" ? location.pathname + location.search : "#" + slugCat(cat));
      draw();
    });
    let t; q.addEventListener("input", () => { clearTimeout(t); t = setTimeout(draw, 120); });
    sort.addEventListener("change", draw);
    window.addEventListener("hashchange", () => { const k = location.hash.slice(1); cat = cats.find((c) => slugCat(c) === (HASH_ALIAS[k] || k)) || "Tous"; draw(); });
    draw();
  }

  Promise.all([
    fetch("data/kb.json").then((r) => r.json()),
    fetch("data/documents.json").then((r) => r.json()),
    needDocs ? fetch("data/catalogue.json").then((r) => r.json()) : null
  ]).then(([kb, docs, cat]) => {
    if (needClubs) renderDistricts(kb);
    if (needDocs) renderDocs(cat, docs);
    if (needAsk) { buildIndex(kb, docs); if (pending) { const q = pending; pending = ""; ask(q); } }
  }).catch(() => {
    const el = $("#doc-list") || $("#answer") || $("#districts");
    if (el) el.innerHTML = `<p class="doc-empty">Le contenu n'a pas pu être chargé. Rechargez la page.</p>`;
  });
})();
