# QA Report — CAMIS Patisserie demo site

**Build dir:** `~/workspace/lead-builds/br-camis-patisserie-venceslau/`
**Date:** 2026-11-09
**Source of truth:** FACTS.md (verified) + STITCH-EXPORT.md (Stitch project 4390840610102313812, 7 screens)
**Method:** Playwright (Chromium) against a local static server — every page at 1440×900 and 390×844, plus screenshot review. Script: `qa-check.py` (raw JSON in `/tmp/camis-qa.json`).

## Verdict: ✅ PASS

All 6 pages: **0px horizontal overflow** at both viewports, **0 console errors**, **0 failed requests**, all internal links return **200**, business name renders on every page (filled from the single `SITE.businessName` constant in `assets/js/site.js`).

## Per-page results

| Page | 1440px overflow | 390px overflow | Console errors | Failed requests | Internal links | Interactions verified |
|---|---|---|---|---|---|---|
| index.html | 0px | 0px | 0 | 0 | all 200 | burger nav opens |
| cardapio.html | 0px | 0px | 0 | 0 | all 200 | burger nav opens; anchor nav 1–4 |
| ensaio.html | 0px | 0px | 0 | 0 | all 200 | before/after slider sets clip (`inset(0 0 0 25%)`), slider has real hit-area, burger nav opens |
| conteudo.html | 0px | 0px | 0 | 0 | all 200 | burger nav opens |
| encomendas.html | 0px | 0px | 0 | 0 | all 200 | occasion selector updates message preview; form fields update preview; FAQ accordion opens; burger nav opens |
| historia.html | 0px | 0px | 0 | 0 | all 200 | burger nav opens |

Screenshot review (desktop + mobile home, desktop ensaio, mobile encomendas): giant raspberry CAMIS wordmark, buttercream/cocoa colour-blocking, sticker badges, hero cookie photo with caption card — matches the Stitch "Doce Atelier" language. No layout defects after fixes below.

## Defects found and fixed during QA

1. **Mobile overflow (cardapio 90px, encomendas 196px, historia 148px)** — cause: `.ph` placeholders had `white-space:nowrap` inside grid items with default `min-width:auto`, forcing tracks wider than the viewport. Fix: placeholders now wrap (`overflow-wrap:break-word`) + `min-width:0` on all grid/flex children. Re-tested: 0px everywhere.
2. **Before/after slider collapsed (ensaio)** — `.ba-wrap` had zero in-flow height (both images absolutely positioned; the range input had 0 height under `appearance:none`). Fix: `aspect-ratio:16/10` on the wrap + `height:100%` on the slider. Re-tested: slider visible with real hit-area, clip updates on input.
3. **Desktop header wrapped to two rows** — the mobile-only "Encomendar" button was visible on desktop. Fix: `.nav-cta.mobile{display:none}` by default (shown only ≤860px). Re-tested via screenshot: single-line header.
4. **Google Fonts CDN unreachable from headless Chromium in this sandbox** (`ERR_TUNNEL_CONNECTION_FAILED`) — environment-only, but removed the dependency entirely: Fraunces + Archivo are now **self-hosted** as woff2 in `assets/fonts/` (latin subsets, cover pt-BR diacritics). After the change: 0 failed requests.

## Strip list — Stitch inventions removed (per export's Honest Audit + FACTS.md)

- **Invented flavours/dish names** (all removed; replaced with generic verified category names): "Cookie Red Velvet & Callebaut Branco", "Cookie Pistache & Chocolate Nobre", "Cookie Triplo Cacau Intenso", "Bolo Pistache Puro com Framboesas Frescas", "Bolo Caramelo Dourado & Callebaut Gold", "Latte de Pistache Especial", "Entremets Individuais", "Copos de Afeto Artesanais", "Cookie Clássico Callebaut", "Bolo Autoral Ganache Belga & Frutas Vermelhas", "Cookie Artesanal com Flor de Sal" (flor de sal detail dropped).
- **Invented numbers/claims**: "+340% Atenção", "96% / 92% / 98%" neurogastronomy figures, "3200K–4500K" and "f/2.2 Macro Bokeh" shoot parameters, "100% MANTEIGA EXTRA", "Callebaut 54.5% & Branco W2", "Bolo Médio (~12 a 15 fatias)", "100% Callebaut" / "Callebaut 100% belga" (→ "chocolate belga Callebaut"), "100% AFETO REAL" hero stat (→ plain chips), "manteiga de primeira linha" and "grãos de alta altitude / torra especial" (unverified).
- **Invented lead time**: every "48h / pelo menos 48h de antecedência / no mínimo 48 horas" → visible `[PLACEHOLDER — confirmar prazo com Camila]`.
- **Invented press wording**: Stitch's Portal Proezas headline and the quote "Uma pausa imperdível para quem valoriza a verdadeira confeitaria." removed. Press block now uses the **real** article title from FACTS.md ("CAMIS Patisserie: o toque autoral de Camila Coelho reúne arte e sabor afetivo") with the **real** link.
- **"Retirada no centro de Presidente Venceslau"** (unverified address detail) → "retirada no ateliê em Presidente Venceslau – SP".
- **Founder portrait**: Stitch's ensaio shot 4 was a portrait of Camila — no real photo exists, and a generated face must never stand in for her. Replaced with a bastidores/process shot; no generated person is presented as Camila anywhere.
- **WhatsApp**: no number invented. Only a visible placeholder ("número não confirmado; consulte o perfil @patisseriecamis"); all "Direct ou WhatsApp" copy changed to Direct only.
- **Fonts**: Stitch substituted Newsreader + Archivo Narrow; site uses the **prompt fonts** Fraunces + Archivo (self-hosted).
- **Form defaults**: Stitch's pre-filled "Cliente CAMIS" / "Bolo Médio (~12 a 15 fatias)" / "Final de Semana" defaults removed — fields start empty with neutral example placeholders.

## Remaining [Placeholder]s (visible on-site, awaiting Camila — nothing invented)

- Prices: every menu item — "[Preço sob consulta no Instagram]"
- Sabores da semana / lista de sabores — "[Sabor da semana — confirmar]"
- Lead time / prazo mínimo de encomenda — "[Prazo mínimo — confirmar com Camila]"
- Endereço físico exato — "[Endereço — confirmar no Instagram]"
- Horários de funcionamento — "[Horários — confirmar no Instagram]"
- WhatsApp — "[número não confirmado; consulte o perfil @patisseriecamis]"
- Formas de pagamento / entrega — "[confirmar com Camila]"
- Carta de cafés — "[Carta de cafés — confirmar]"

## Notes

- **Images:** 4 AI-generated product shots in `assets/img/` (hero-cookie.jpg, bolo-autoral.jpg, cafe-latte.jpg, bastidores.jpg; 1408×1760). Every on-site use carries a visible "Amostra gerada por IA" label; the ensaio before/after "foto de celular" side is the same image with an illustrative filter and is labelled as a simulation.
- **Forms are demo-only:** the order form builds a DM text preview and links out to Instagram; nothing is submitted or stored.
- **Business name:** one swappable constant — `SITE.businessName` in `assets/js/site.js` fills every `[data-site]` slot (wordmark, footer, order message).
- **vercel.json** present with `cleanUrls: true`.
- Not done here (parent handles): GitHub repo, Vercel deploy, outreach, seen_leads.json.
