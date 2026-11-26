/* Site vitrine du CD33 : menu, clubs par district, zone documents et assistant.
   L'assistant cherche dans data/kb.json (pages du site) et data/documents.json (documents officiels).
   Sans relais IA configuré, il affiche les passages les plus pertinents avec leur source. */
(function () {
  "use strict";
  const CONFIG = window.SITE_CONFIG || {};
  const $ = (s) => document.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = (u) => (/^https:\/\//.test(u) ? u : "#");

  /* ---------- Menu ---------- */
  const topbar = $("#topbar"), toggle = $("#menu-toggle");
  toggle.addEventListener("click", () => {
    const open = !topbar.classList.contains("open");
    topbar.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
  });
  document.querySelectorAll(".nav a").forEach((a) => a.addEventListener("click", () => {
    topbar.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
  }));
  const links = [...document.querySelectorAll(".nav a")];
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id));
    });
  }, { rootMargin: "-45% 0px -50% 0px" });
  document.querySelectorAll("main section[id]").forEach((s) => spy.observe(s));

  /* ---------- Recherche plein texte (BM25) ---------- */
  const STOP = new Set("les des une un du de la le et en au aux pour par sur dans est sont que qui quoi quel quelle quels quelles comment combien quand ou avec pas plus ce cette ces son sa ses leur leurs mon ma mes nous vous il elle ils elles on je tu faire fait peut doit doivent etre avoir y a ne se si tout tous toute toutes".split(" "));
  const norm = (s) => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");
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

  /* ---------- Assistant ---------- */
  const SUGG = ["Combien coûte une licence U13 ?", "Comment inscrire une équipe en 3x3 ?", "Comment devenir arbitre ?", "Quelle est l'amende pour un forfait en seniors ?", "Quand ont lieu les finales des Coupes 33 ?", "Quel brevet pour entraîner des U11 ?"];
  const form = $("#ask-form"), input = $("#ask-q"), answer = $("#answer");
  $("#suggest").innerHTML = SUGG.map((s, i) => `<button type="button" data-i="${i}">${esc(s)}</button>`).join("");
  $("#suggest").addEventListener("click", (e) => { const b = e.target.closest("button"); if (b) { input.value = SUGG[b.dataset.i]; ask(input.value); } });
  form.addEventListener("submit", (e) => { e.preventDefault(); ask(input.value); });

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
  function renderHits(q, hits, intro) {
    if (!hits.length) {
      answer.innerHTML = `<p class="ans-intro">Je n'ai rien trouvé à ce sujet dans les pages et documents du comité. Contactez le secrétariat : <a href="mailto:secretariat@basket33.fr">secretariat@basket33.fr</a> · 06 19 86 37 71.</p>`;
      return;
    }
    answer.innerHTML = `<p class="ans-intro">${esc(intro)}</p>` + hits.map((h) => `<article class="hit"><span class="hit-kind">${esc(h.kind)}</span><h3>${esc(h.t)}</h3><p>${snippet(h.x, q)}</p><a href="${esc(safeUrl(h.u))}" target="_blank" rel="noopener">Ouvrir la source</a></article>`).join("");
  }
  let busy = false;
  async function ask(q) {
    q = (q || "").trim();
    if (!q || busy) return;
    if (!INDEX.length) { answer.innerHTML = `<p class="ans-intro">Chargement des documents… réessayez dans un instant.</p>`; return; }
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
  }

  /* ---------- Clubs et documents ---------- */
  function renderDistricts(kb) {
    const ds = kb.filter((p) => /^Clubs du district/.test(p.t));
    $("#districts").innerHTML = ds.map((d) => {
      const name = d.t.replace(/^Clubs du district (de |du )?/, "");
      const clubs = d.c.replace(/\([^)]*\)/g, "").replace(/\.$/, "").split(/,\s*/).map((s) => s.trim()).filter(Boolean);
      return `<details class="district"><summary><h3>${esc(name)}</h3><span>${clubs.length} clubs</span></summary><ul>${clubs.map((c) => `<li>${esc(c)}</li>`).join("")}</ul></details>`;
    }).join("");
  }
  function renderDocs(docs) {
    const cats = ["Tous", ...new Set(docs.docs.map((d) => d.cat))];
    let cat = "Tous";
    const list = $("#doc-list"), q = $("#doc-q"), filters = $("#doc-filters");
    filters.innerHTML = cats.map((c) => `<button type="button" aria-pressed="${c === cat}">${esc(c)}</button>`).join("");
    function draw() {
      const term = norm(q.value.trim());
      const rows = docs.docs.filter((d) => (cat === "Tous" || d.cat === cat) && (!term || norm(d.t + " " + d.cat).includes(term)));
      list.innerHTML = rows.length ? rows.map((d) => `<a class="doc" href="${esc(safeUrl(d.u))}" target="_blank" rel="noopener"><span class="doc-title">${esc(d.t)}</span><span class="doc-cat">${esc(d.cat)}</span><span class="doc-open">Ouvrir ↗</span></a>`).join("")
        : `<p class="doc-empty">Aucun document ne correspond. Essayez l'assistant : il cherche aussi à l'intérieur des documents.</p>`;
    }
    filters.addEventListener("click", (e) => {
      const b = e.target.closest("button"); if (!b) return;
      cat = b.textContent;
      filters.querySelectorAll("button").forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      draw();
    });
    q.addEventListener("input", draw);
    draw();
  }

  Promise.all([
    fetch("data/kb.json").then((r) => r.json()),
    fetch("data/documents.json").then((r) => r.json())
  ]).then(([kb, docs]) => {
    renderDistricts(kb);
    renderDocs(docs);
    buildIndex(kb, docs);
  }).catch(() => {
    $("#doc-list").innerHTML = `<p class="doc-empty">Les documents n'ont pas pu être chargés. Rechargez la page.</p>`;
  });
})();
