/* ============================================================
   CAMIS Patisserie — site config & interactions
   THE BUSINESS NAME IS ONE SWAPPABLE CONSTANT:
   change SITE.businessName here and every [data-site] element
   on every page updates automatically.
   ============================================================ */
const SITE = {
  businessName: "CAMIS Patisserie",
  wordmark: "CAMIS",
  tagline: "Café, afeto e confeitaria.",
  city: "Presidente Venceslau – SP",
  instagramHandle: "@patisseriecamis",
  instagramUrl: "https://www.instagram.com/patisseriecamis/",
  opened: "Dezembro de 2025",
  pressName: "Portal Proezas",
  pressDate: "Setembro de 2026",
  pressUrl: "https://www.portalproezas.com.br/camis-patisserie-o-toque-autoral-de-camila-coelho-reune-arte-e-sabor-afetivo"
};

document.addEventListener("DOMContentLoaded", () => {
  /* Fill every [data-site="..."] slot from the single constant. */
  document.querySelectorAll("[data-site]").forEach((el) => {
    const key = el.getAttribute("data-site");
    if (SITE[key] !== undefined) el.textContent = SITE[key];
  });
  document.querySelectorAll("[data-site-href]").forEach((el) => {
    const key = el.getAttribute("data-site-href");
    if (SITE[key] !== undefined) el.setAttribute("href", SITE[key]);
  });
  document.querySelectorAll("[data-site-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });

  /* Mobile nav toggle */
  const burger = document.querySelector(".burger");
  const navLinks = document.querySelector(".nav-links");
  if (burger && navLinks) {
    burger.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navLinks.querySelectorAll("a").forEach((a) =>
      a.addEventListener("click", () => navLinks.classList.remove("open"))
    );
  }

  /* Before / after slider (Ensaio page) */
  const ba = document.querySelector(".ba-wrap");
  if (ba) {
    const slider = ba.querySelector(".ba-slider");
    const after = ba.querySelector(".ba-after");
    const divider = ba.querySelector(".ba-divider");
    const setSplit = (v) => {
      after.style.clipPath = `inset(0 0 0 ${v}%)`;
      divider.style.left = v + "%";
    };
    setSplit(50);
    slider.addEventListener("input", (e) => setSplit(Number(e.target.value)));
  }

  /* Order form (Encomendas page) — demo only, no backend.
     Builds the DM text from the form and links out to Instagram. */
  const form = document.querySelector("#order-form");
  if (form) {
    const preview = document.querySelector("#msg-preview");
    const occasionBtns = form.querySelectorAll(".occasion");
    let occasion = "Aniversário";

    const buildMessage = () => {
      const date = form.querySelector("#f-date").value.trim();
      const size = form.querySelector("#f-size").value.trim();
      const name = form.querySelector("#f-name").value.trim();
      const notes = form.querySelector("#f-notes").value.trim();
      const lines = [
        "Olá, Camila! Tudo bem?",
        `Gostaria de verificar a disponibilidade de uma encomenda na ${SITE.businessName}:`,
        "",
        `• Ocasião: ${occasion}`,
      ];
      if (date) lines.push(`• Data prevista: ${date}`);
      if (size) lines.push(`• Tamanho / formato: ${size}`);
      if (name) lines.push(`• Para: ${name}`);
      if (notes) lines.push(`• Observações: ${notes}`);
      lines.push("", "Pode me confirmar disponibilidade e valores? Obrigada!");
      return lines.join("\n");
    };

    const refresh = () => { if (preview) preview.textContent = buildMessage(); };

    occasionBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        occasionBtns.forEach((b) => {
          b.classList.remove("selected");
          b.setAttribute("aria-pressed", "false");
        });
        btn.classList.add("selected");
        btn.setAttribute("aria-pressed", "true");
        occasion = btn.dataset.occasion || btn.querySelector("b").textContent.trim();
        refresh();
      });
    });
    form.querySelectorAll("input, select, textarea").forEach((el) =>
      el.addEventListener("input", refresh)
    );
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      window.open(SITE.instagramUrl, "_blank", "noopener");
    });
    const copyBtn = document.querySelector("#copy-msg");
    if (copyBtn) {
      copyBtn.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(buildMessage());
          copyBtn.textContent = "Texto copiado ✓";
          setTimeout(() => { copyBtn.textContent = "Copiar texto da mensagem"; }, 2500);
        } catch (err) {
          copyBtn.textContent = "Selecione e copie o texto acima";
          setTimeout(() => { copyBtn.textContent = "Copiar texto da mensagem"; }, 3000);
        }
      });
    }
    refresh();
  }
});
