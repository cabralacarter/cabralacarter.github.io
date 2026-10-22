"""Rebuild the static student resource page using only Python's standard library."""

from collections import Counter
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCE_DIR = ROOT / 'resources'
BOOKS = json.loads((RESOURCE_DIR / 'catalog.json').read_text())
MANIFEST = json.loads((RESOURCE_DIR / 'manifest.json').read_text())
TOPICS = {
    'all': 'All resources',
    'raspberry-pi': 'Raspberry Pi',
    'coding-games': 'Coding & games',
    'linux': 'Linux & terminal',
    'electronics': 'Electronics',
    'making': 'Projects & making',
    'history': 'Computer history',
    'teaching': 'Teaching & outreach',
}

OPEN_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M14 3h7v7M21 3 10 14"/><path d="M10 3H4a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-6"/></svg>'
DOWNLOAD_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 3v12m-5-5 5 5 5-5M4 15v5a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-5"/></svg>'


def card(book):
    info = MANIFEST[book['id']]
    pdf_url = 'pdf/' + book['file']
    keywords = ' '.join([book['title'], book['edition'], book['description'], book['keywords'], book['author'], book['hardware'], *[TOPICS[topic] for topic in book['topics']]])
    title = escape(book['title'])
    return f'''<article class="resource-card" id="{book['id']}" data-resource data-topics="{escape(' '.join(book['topics']), quote=True)}" data-search="{escape(keywords, quote=True)}" aria-labelledby="title-{book['id']}">
          <div class="book-main">
            <a class="cover-link" href="{pdf_url}" target="_blank" rel="noopener" aria-label="Open {escape(book['title'], quote=True)} PDF (new tab)">
              <img class="book-cover" src="covers/{book['id']}.webp" alt="" width="{info['cover_width']}" height="{info['cover_height']}" loading="lazy" decoding="async">
            </a>
            <div class="book-content">
              <p class="book-topic">{escape(TOPICS[book['topics'][0]])}</p>
              <h3 id="title-{book['id']}">{title}</h3>
              <p class="book-edition">{escape(book['edition'])}</p>
              <p class="book-description">{escape(book['description'])}</p>
              <p class="book-specs"><span>{escape(book['level'])}</span><span>{info['pages']} pages</span><span>PDF · {info['bytes'] / 1e6:.1f} MB</span></p>
              <p class="book-hardware">{escape(book['hardware'])}</p>
            </div>
          </div>
          <div class="book-actions">
            <a class="pdf-action" href="{pdf_url}" target="_blank" rel="noopener" aria-label="Read {escape(book['title'], quote=True)} PDF (new tab)">Read PDF {OPEN_ICON}</a>
            <a class="pdf-action download-action" href="{pdf_url}" download="{book['file']}" aria-label="Download {escape(book['title'], quote=True)} PDF">Download {DOWNLOAD_ICON}</a>
          </div>
          <p class="book-credit"><a href="{escape(book['publisher_url'], quote=True)}" target="_blank" rel="noopener" aria-label="Publisher information for {escape(book['title'], quote=True)} (new tab)">{escape(book['author'])}</a> · Raspberry Pi Press</p>
        </article>'''


counts = Counter(topic for book in BOOKS for topic in book['topics'])
counts['all'] = len(BOOKS)
filters = '\n            '.join(
    f'<button class="topic-filter" type="button" data-topic-filter="{key}" aria-pressed="{str(key == "all").lower()}">{escape(label)} <span>{counts[key]}</span></button>'
    for key, label in TOPICS.items()
)
cards = '\n        '.join(card(book) for book in BOOKS)

PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Tiger Den student resources: free books, lab equipment, request forms, and safety guides. Find us in CIC 102 at St. Philip’s College.">
  <meta name="theme-color" content="#0d1117">
  <meta property="og:title" content="Student Resources | Carter Cabral">
  <meta property="og:description" content="Free books. Practical projects. Find a place to start with coding, Raspberry Pi, electronics, and more.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://cartercabral.com/resources/">
  <link rel="canonical" href="https://cartercabral.com/resources/">
  <title>Student Resources | Carter Cabral</title>
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="resources.css">
  <script src="resources.js" defer></script>
</head>
<body class="resource-page">
  <a class="skip-link" href="#main">Skip to resources</a>
  <header>
    <nav class="container resource-nav" aria-label="Main navigation">
      <a class="logo" href="../">Carter Cabral</a>
      <div class="nav-links">
        <a href="../">Portfolio</a>
        <a href="./" aria-current="page">Student resources</a>
      </div>
    </nav>
  </header>

  <main id="main" class="container">
    <section class="resource-hero" aria-labelledby="page-title">
      <p class="eyebrow">Tiger Den &nbsp; / &nbsp; CIC 102</p>
      <h1 id="page-title">Student resources.</h1>
      <p class="resource-intro"><strong>Learn a skill. Make something. Follow your curiosity.</strong><br>Explore free books, plan a lab project, and find the forms you need for the Tiger Den at St. Philip’s College.</p>
      <div class="collection-facts" aria-label="About this collection">
        <span><svg class="fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M3 4h6a4 4 0 0 1 3 1.5A4 4 0 0 1 15 4h6v16h-6a4 4 0 0 0-3 1.5A4 4 0 0 0 9 20H3Z"/><path d="M12 5.5v16"/></svg>{len(BOOKS)} books to explore</span>
        <span><svg class="fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg>Free PDF downloads</span>
        <span><svg class="fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M7 10V7a5 5 0 0 1 9-3M5 10h14v11H5Z"/><path d="M12 14v3"/></svg>No sign-in needed</span>
      </div>
      <nav class="resource-shortcuts" aria-label="On this page">
        <a href="#library">Browse 16 free books <span aria-hidden="true">&darr;</span></a>
        <a href="#lab-equipment">Lab &amp; equipment <span aria-hidden="true">&darr;</span></a>
        <a href="#forms-safety">Forms &amp; safety <span aria-hidden="true">&darr;</span></a>
      </nav>
    </section>

    <section class="starting-points" aria-labelledby="start-title">
      <div class="section-heading"><h2 id="start-title">Not sure where to start?</h2><p>Pick something you want to try.</p></div>
      <div class="pathways">
        <a class="pathway" href="#raspberry-pi-beginners-guide" data-start-resource="raspberry-pi-beginners-guide">
          <span class="pathway-number" aria-hidden="true">01</span>
          <h3>Get started with Raspberry Pi</h3>
          <p>Set it up, explore the basics, and try a first project.</p>
          <span class="pathway-link">Open the beginner’s guide &rarr;</span>
        </a>
        <a class="pathway" href="#make-games-with-python" data-start-resource="make-games-with-python">
          <span class="pathway-number" aria-hidden="true">02</span>
          <h3>Make a game with Python</h3>
          <p>Put code on screen and turn an idea into something playable.</p>
          <span class="pathway-link">Explore Python games &rarr;</span>
        </a>
        <a class="pathway" href="#conquer-the-command-line" data-start-resource="conquer-the-command-line">
          <span class="pathway-number" aria-hidden="true">03</span>
          <h3>Get comfortable with Linux</h3>
          <p>Learn your way around files, commands, and the terminal.</p>
          <span class="pathway-link">Start with the command line &rarr;</span>
        </a>
      </div>
    </section>

    <section id="library" class="library-section" aria-labelledby="library-title">
      <div class="library-topline"><h2 id="library-title">Find your next read</h2><p>Browse the collection or narrow it down by what interests you.</p></div>
      <div id="resource-controls" hidden>
        <form id="resource-search-form" role="search" aria-label="Search student resources">
          <label class="sr-only" for="resource-search">Search by title, topic, or skill</label>
          <div class="search-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>
            <input type="search" id="resource-search" name="q" placeholder="Search by title, topic, or skill…" autocomplete="off" aria-controls="resource-grid">
            <button type="button" id="clear-search" class="clear-search" aria-label="Clear search" hidden>&times;</button>
          </div>
        </form>
        <p class="filter-label" id="filter-label">Explore a topic</p>
        <div class="topic-filters" role="group" aria-labelledby="filter-label">
            {filters}
        </div>
      </div>
      <div class="results-bar">
        <p id="resource-count" role="status" aria-live="polite" aria-atomic="true">{len(BOOKS)} resources to explore</p>
        <button type="button" id="reset-filters" class="text-button" hidden>Clear filters</button>
      </div>
      <noscript><p class="no-script-note">All books are listed below. Search and topic filters are available when JavaScript is enabled.</p></noscript>
      <div id="resource-grid" class="resource-grid">
        {cards}
      </div>
      <div id="empty-results" class="empty-results" hidden>
        <h3>No matching resources yet.</h3>
        <p>Try a broader search or choose a different topic.</p>
        <button type="button" id="empty-reset" class="text-button">Show all resources</button>
      </div>
    </section>

    <section id="lab-equipment" class="lab-section" aria-labelledby="lab-title">
      <div class="library-topline"><h2 id="lab-title">Make it happen in the Tiger Den</h2><p>Cybersecurity &amp; Information Technology &nbsp;·&nbsp; CIC 102</p></div>
      <div class="lab-meta"><p><strong>Visit the lab</strong> Operating hours: 8 a.m.–7 p.m. Ask staff about the current daily schedule.</p><a href="documents/tiger-den-technology.pdf" target="_blank" rel="noopener">Explore the equipment guide <span class="sr-only">(PDF, new tab)</span>&rarr;</a></div>
      <div class="equipment-grid">
        <article class="equipment-card"><p class="equipment-type">Reserve a time</p><h3>3D printing</h3><p>Bring your design to life with the Prusa XL printers. Complete the printer request form and discuss your material, color, and filament needs with staff.</p><a href="documents/3d-printer-request-form.pdf" target="_blank" rel="noopener">Printer request form <span class="sr-only">(PDF, new tab)</span>&rarr;</a></article>
        <article class="equipment-card"><p class="equipment-type">Reserve a time</p><h3>Laser cutting &amp; engraving</h3><p>Plan a project with the xTool P3 CO₂ laser cutter. Bring your design and exact material details; all materials and jobs require staff approval.</p><a href="documents/laser-cutter-request-form.pdf" target="_blank" rel="noopener">Laser cutter request form <span class="sr-only">(PDF, new tab)</span>&rarr;</a></article>
        <article class="equipment-card"><p class="equipment-type">Ask about availability</p><h3>Robotics &amp; coding</h3><p>Explore the SO-ARM101 robotic arms and Sphero BOLT+ and RVR robots. Stop by for equipment availability and help getting started.</p><a href="documents/tiger-den-technology.pdf" target="_blank" rel="noopener">See the technology guide <span class="sr-only">(PDF, new tab)</span>&rarr;</a></article>
        <article class="equipment-card"><p class="equipment-type">Ask about availability</p><h3>Virtual reality</h3><p>Try the Meta Quest 3 with help from lab staff. Read the VR safety sheet before using the headset.</p><a href="documents/vr-headset-safety.pdf" target="_blank" rel="noopener">Read the VR safety sheet <span class="sr-only">(PDF, new tab)</span>&rarr;</a></article>
      </div>
      <div class="project-steps"><h3>Have a class project in mind?</h3><ol><li>Choose your equipment and prepare a design or project idea.</li><li>For printing or laser work, complete the relevant request form and bring it to the Tiger Den.</li><li>Arrange professor sign-off, or have your professor contact Carter about the device and time slot.</li></ol><p>Filament and print-time limits apply. Larger class projects can be discussed with staff and your professor ahead of time.</p></div>
    </section>

    <section id="forms-safety" class="lab-section" aria-labelledby="forms-title">
      <div class="library-topline"><h2 id="forms-title">Forms &amp; safety guides</h2><p>Open or download a copy before your visit.</p></div>
      <div class="document-list">
        <article class="document-row"><div><h3>3D Printer Request Form</h3><p>Requester information, print details, and acknowledgments.</p></div><div><a href="documents/3d-printer-request-form.pdf" target="_blank" rel="noopener" aria-label="Open 3D Printer Request Form PDF in a new tab">Open PDF</a><a href="documents/3d-printer-request-form.pdf" download aria-label="Download 3D Printer Request Form PDF">Download</a></div></article>
        <article class="document-row"><div><h3>xTool P3 Laser Cutter Request Form</h3><p>Project details, intended material, and staff approval.</p></div><div><a href="documents/laser-cutter-request-form.pdf" target="_blank" rel="noopener" aria-label="Open Laser Cutter Request Form PDF in a new tab">Open PDF</a><a href="documents/laser-cutter-request-form.pdf" download aria-label="Download Laser Cutter Request Form PDF">Download</a></div></article>
        <article class="document-row"><div><h3>3D Printing Materials Guide</h3><p>PLA, PETG, and TPU information. Ask staff about availability; ABS is not used in the Tiger Den.</p></div><div><a href="documents/3d-printing-materials.pdf" target="_blank" rel="noopener" aria-label="Open 3D Printing Materials Guide PDF in a new tab">Open PDF</a><a href="documents/3d-printing-materials.pdf" download aria-label="Download 3D Printing Materials Guide PDF">Download</a></div></article>
        <article class="document-row"><div><h3>VR Headset Safety</h3><p>Read before using the lab’s Meta Quest 3.</p></div><div><a href="documents/vr-headset-safety.pdf" target="_blank" rel="noopener" aria-label="Open VR Headset Safety PDF in a new tab">Open PDF</a><a href="documents/vr-headset-safety.pdf" download aria-label="Download VR Headset Safety PDF">Download</a></div></article>
        <article class="document-row"><div><h3>Tiger Den Technology Overview</h3><p>Explore the lab equipment, project examples, and how to request access.</p></div><div><a href="documents/tiger-den-technology.pdf" target="_blank" rel="noopener" aria-label="Open Tiger Den Technology Overview PDF in a new tab">Open PDF</a><a href="documents/tiger-den-technology.pdf" download aria-label="Download Tiger Den Technology Overview PDF">Download</a></div></article>
      </div>
      <p class="form-note">Bring completed forms to lab staff for review and scheduling.</p>
    </section>

    <aside class="help-panel" aria-labelledby="help-title">
      <div><h2 id="help-title">A little help getting started?</h2><p>Stop by the Tiger Den and ask Carter for help choosing a resource, planning a first project, or figuring out the equipment you’ll need.</p></div>
      <p class="help-location"><strong>Tiger Den</strong>CIC 102</p>
    </aside>

    <div class="collection-notes">
      <p>PDFs open in a new tab. Use Download to save a copy for offline reading. Some files are large; Wi-Fi is recommended. The page lists suggested equipment, which varies by project.</p>
      <p>Books and cover artwork are credited to their authors and Raspberry Pi Press. Except where otherwise noted within each publication, they are shared under <a href="https://creativecommons.org/licenses/by-nc-sa/3.0/" target="_blank" rel="noopener">Creative Commons BY-NC-SA 3.0<span class="sr-only"> (new tab)</span></a>. Cover images are resized from the original books. PDF photographs have been optimized where helpful; page content and existing credits are retained. See each book for full credits and any exceptions.</p>
    </div>
  </main>

  <footer class="resource-footer"><div class="container"><p>&copy; 2026 Carter Cabral &nbsp;·&nbsp; Curated for student learning</p><a href="../">Back to portfolio &rarr;</a></div></footer>
</body>
</html>
'''

(RESOURCE_DIR / 'index.html').write_text(PAGE, encoding='utf-8')
print(f"Built resources/index.html with {len(BOOKS)} books.")
