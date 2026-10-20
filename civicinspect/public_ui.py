"""Static public UI shell for CivicInspect v0.2.2."""

from __future__ import annotations


def render_public_lookup_page() -> str:
    """Render the public-facing CivicInspect sample page."""

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicInspect Inspection Support</title>
<style>
  :root { --ink:#17202a; --muted:#526170; --paper:#fffaf2; --blue:#174f68; --green:#27604b; --gold:#d8ad48; --line:#d8c7a5; --warn:#8f4a2b; }
  * { box-sizing: border-box; }
  body { margin:0; color:var(--ink); font-family:"Aptos","Segoe UI",sans-serif; background:linear-gradient(135deg,#fff6e8,#e8f3f4); }
  .skip-link { position:absolute; left:1rem; top:-4rem; background:var(--ink); color:white; padding:.7rem 1rem; border-radius:8px; }
  .skip-link:focus { top:1rem; }
  header, main, footer { width:min(1120px, calc(100% - 32px)); margin:0 auto; }
  header { padding:48px 0 24px; }
  .eyebrow { color:var(--blue); text-transform:uppercase; font-weight:800; font-size:.78rem; }
  h1 { max-width:980px; margin:0; font-family:Georgia,"Times New Roman",serif; font-size:4.8rem; line-height:1; }
  .lede { max-width:820px; font-size:1.25rem; line-height:1.55; color:#31404a; }
  .badge { display:inline-flex; width:fit-content; padding:.45rem .75rem; border-radius:8px; background:var(--green); color:white; font-weight:900; }
  .grid { display:grid; grid-template-columns:repeat(12,1fr); gap:18px; }
  .panel { grid-column:span 6; min-width:0; padding:24px; border:1px solid var(--line); border-radius:8px; background:rgba(255,250,242,.92); box-shadow:0 18px 40px rgba(35,43,50,.10); }
  .panel.large { grid-column:span 12; }
  h2,h3 { font-family:Georgia,"Times New Roman",serif; }
  h2 { margin:0 0 14px; font-size:2.2rem; }
  p, li { line-height:1.65; }
  label { display:block; margin:.9rem 0 .35rem; font-weight:800; }
  input, textarea, select, button { width:100%; border:1px solid #b9c6cc; border-radius:8px; padding:.85rem 1rem; font:inherit; }
  input, textarea, select { background:#f5f8f8; color:var(--ink); }
  button { width:fit-content; min-width:190px; margin-top:1rem; border:0; background:var(--blue); color:white; font-weight:900; cursor:pointer; }
  button:disabled { opacity:.65; cursor:wait; }
  .result { margin-top:18px; padding:18px; border-left:6px solid var(--green); border-radius:8px; background:white; }
  .result.warning { border-left-color:var(--warn); background:#fff8f4; }
  .result.error { border-left-color:#a4262c; background:#fff2f2; }
  .kicker { color:var(--muted); font-size:.86rem; font-weight:900; text-transform:uppercase; }
  footer { padding:38px 0 56px; color:var(--muted); }
  :focus-visible { outline:4px solid var(--gold); outline-offset:3px; }
  @media (max-width:760px) {
    header, main, footer { margin:0; max-width:430px; width:100%; padding-left:24px; padding-right:24px; }
    header { padding-top:34px; }
    h1 { font-size:2.7rem; }
    h2 { font-size:1.8rem; }
    .panel { grid-column:span 12; padding:20px; }
    button { width:100%; }
  }
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header>
  <p class="eyebrow">CivicSuite / CivicInspect public sample</p>
  <h1>Turn field notes into review-ready inspection drafts.</h1>
  <p class="lede">CivicInspect demonstrates inspection support: sample repeat-case lookup, inspector-owned report drafting, notice draft support, staff review queues, CivicCode context packets, and records-ready exports without issuing findings or replacing the system of record.</p>
  <p><span class="badge">v0.2.2 inspection support + staff review queues</span></p>
</header>
<main id="main" tabindex="-1">
  <section class="grid" aria-labelledby="lookup-title">
    <article class="panel large">
      <p class="kicker">Sample repeat-case lookup</p>
      <h2 id="lookup-title">Draft inspection support</h2>
      <label for="property">Property reference</label>
      <input id="property" value="100 Main Street">
      <label for="violation">Inspection type</label>
      <select id="violation">
        <option value="nuisance">Nuisance</option>
        <option value="building">Building condition</option>
        <option value="fire">Fire prevention</option>
      </select>
      <label for="notes">Inspector notes</label>
      <textarea id="notes" rows="4">Inspector observed overgrown vegetation near the alley and two prior related cases for the same property.</textarea>
      <button id="draft-button" type="button">Draft sample report</button>
      <div id="result" class="result" role="status" aria-live="polite">
        <h3>Ready for sample input</h3>
        <p>Enter property notes and create a review-required draft. Use "100 Main Street" or "42 Oak Avenue" to show sample repeat-case context.</p>
      </div>
    </article>
    <article class="panel"><p class="kicker">Inspector-owned</p><h2>Humans decide</h2><div class="result"><p>Every draft is explicitly marked for inspector review; CivicInspect does not make findings, issue citations, or assess fines.</p></div></article>
    <article class="panel"><p class="kicker">Notice support</p><h2>Draft, not issuance</h2><div class="result"><p>Notice drafts list required staff actions: confirm code section, ownership, address, and repeat-case context.</p></div></article>
    <article class="panel"><p class="kicker">Staff queue</p><h2>Route review work</h2><div class="result"><p>Persisted draft reports can be routed to staff-only review queues with status, assignment, and resolution records.</p></div></article>
    <article class="panel"><p class="kicker">Records-ready export</p><h2>Keep provenance</h2><div class="result"><p>Exports preserve notes, draft text, reviewer, queue status, review date, and system-of-record links.</p></div></article>
    <article class="panel large"><p class="kicker">Boundary</p><h2>No official inspection action</h2><div class="result warning"><p>CivicInspect does not issue official findings, citations, fines, notices, inspection schedules, or system-of-record updates.</p></div></article>
  </section>
</main>
<footer><p>CivicInspect is part of the AGPL-3.0 CivicSuite open-source municipal AI project.</p></footer>
<script>
  const result = document.querySelector("#result");
  const button = document.querySelector("#draft-button");
  const property = document.querySelector("#property");
  const notes = document.querySelector("#notes");

  function setResult(kind, title, body) {
    result.className = `result ${kind}`;
    result.innerHTML = `<h3>${title}</h3><p>${body}</p>`;
  }

  button.addEventListener("click", () => {
    button.disabled = true;
    setResult("", "Checking sample context", "Reviewing local sample data. This does not call a live inspection system.");
    window.setTimeout(() => {
      const propertyText = property.value.trim();
      const noteText = notes.value.trim();
      button.disabled = false;
      if (!propertyText || !noteText) {
        setResult("error", "More detail is needed", "Add a property reference and inspector notes, then draft again. CivicInspect cannot create useful review text from blank inputs.");
        return;
      }
      const lower = propertyText.toLowerCase();
      if (lower.includes("stale")) {
        setResult("warning", "Staff refresh required", "This sample context is marked stale. Refresh code and case records in the system of record before using the draft.");
        return;
      }
      if (!lower.includes("100 main") && !lower.includes("42 oak")) {
        setResult("warning", "No repeat cases found", "Create a draft from the inspector notes, then confirm ownership, address, and case history in the system of record.");
        return;
      }
      setResult("", "Draft ready for staff review", "Sample repeat-case context was found. The draft remains non-authoritative and must be reviewed by inspection staff before any notice or enforcement action.");
    }, 250);
  });
</script>
</body>
</html>
"""
