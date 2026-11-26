/* Relais IA de l'assistant du site CD33 (Cloudflare Worker).
   Reçoit { question, context:[{titre, source, texte}] } depuis le site,
   demande une réponse à Claude avec la clé API gardée secrète ici, renvoie { answer }.
   Variables à définir dans Cloudflare : ANTHROPIC_API_KEY (secret), ALLOWED_ORIGIN (ex. https://mrodier.github.io). */
const SYSTEM = `Tu es l'assistant du site du Comité départemental de basket-ball de la Gironde (CD33).
Réponds en français, clairement et brièvement, UNIQUEMENT à partir des extraits fournis.
N'invente aucun nom, date, montant ni lien. Si les extraits ne suffisent pas, dis-le et oriente vers secretariat@basket33.fr / 06 19 86 37 71.
Ne donne aucune donnée personnelle. Si la question ne concerne pas le basket en Gironde, réponds poliment que tu es dédié au comité.
Termine par une ligne « Source : » avec l'URL de l'extrait utilisé.`;

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": env.ALLOWED_ORIGIN || "",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST" || origin !== env.ALLOWED_ORIGIN) return new Response("Refusé", { status: 403, headers: cors });

    let body;
    try { body = await request.json(); } catch { return new Response("Requête invalide", { status: 400, headers: cors }); }
    const question = String(body.question || "").slice(0, 500);
    const context = (Array.isArray(body.context) ? body.context : []).slice(0, 6)
      .map((c, i) => `[Extrait ${i + 1}] ${String(c.titre || "").slice(0, 200)}\nSource : ${String(c.source || "").slice(0, 300)}\n${String(c.texte || "").slice(0, 2500)}`).join("\n\n");
    if (!question) return new Response("Question vide", { status: 400, headers: cors });

    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({
        model: "claude-haiku-5-5",
        max_tokens: 700,
        system: SYSTEM,
        messages: [{ role: "user", content: `${context || "Aucun extrait trouvé."}\n\n---\nQuestion : ${question}` }],
      }),
    });
    if (!r.ok) return new Response(JSON.stringify({ error: "ia_indisponible" }), { status: 502, headers: { ...cors, "Content-Type": "application/json" } });
    const data = await r.json();
    const answer = (data.content || []).filter((b) => b.type === "text").map((b) => b.text).join("\n");
    return new Response(JSON.stringify({ answer }), { headers: { ...cors, "Content-Type": "application/json" } });
  },
};
