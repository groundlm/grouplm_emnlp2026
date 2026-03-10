# GroundLM 2026 — Workshop Website

## Quick Start

Open `index.html` in a browser. No build step required.

---

## File Structure

```
groundlm/
├── index.html              ← Main page (assembles everything)
│
├── data/
│   └── config.js           ← ⭐ MAIN CONTENT FILE — edit this first
│
├── css/
│   └── styles.css          ← All styles (tokens, layout, components)
│
├── js/
│   └── main.js             ← Renders dynamic sections from config.js
│
└── sections/               ← HTML partials (for reference / copy-paste)
    ├── announcement.html
    ├── header.html
    ├── hero.html
    ├── glance.html
    ├── topics.html
    ├── cfp.html
    ├── dates.html
    ├── speakers.html
    ├── organizers.html
    ├── program.html
    ├── venue.html
    ├── faq.html
    └── footer.html
```

---

## How to Edit

### 🔧 Most common updates → `data/config.js`

| What to change | Where in config.js |
|---|---|
| Workshop name, email, URLs | `SITE` object |
| Announcement bar text | `SITE.announcement` |
| Hero date, location, description | `SITE.hero` |
| Important dates | `DATES` array |
| Invited speakers | `SPEAKERS` array |
| Organizers | `ORGANIZERS` array |
| Program schedule | `PROGRAM` array |
| Topics of interest | `TOPICS` array |
| FAQ questions & answers | `FAQ` array |

### Adding a speaker photo
```js
{
  name: "Jane Smith",
  affiliation: "MIT, USA",
  status: "confirmed",
  bio: "...",
  url: "https://janesmith.com",
  photo: "assets/people/smith-jane.jpg",  // ← add photo path here
}
```
Place the image in `assets/people/`.

### Editing static sections
Some sections are best edited directly in `index.html`:
- **At a Glance** cards (glance section)
- **CFP** text
- **Venue** description

### Adding/removing nav items
Edit the `<nav>` in `index.html` and add the corresponding `<section id="...">`.

---

## Styles

All CSS custom properties (colors, fonts, spacing) are defined at the top of
`css/styles.css` under `:root { ... }`. Change them there to retheme the site.

Key tokens:
- `--navy` / `--navy-dark` — header and hero backgrounds
- `--accent` / `--accent-light` — blue accent color
- `--gold` — gold badge color
- `--serif` / `--sans` / `--mono` — font stacks

---

## Deployment

This is a static site. Deploy by uploading the entire `groundlm/` folder to:
- **GitHub Pages** — push to a repo, enable Pages on the `main` branch
- **Netlify / Vercel** — drag and drop the folder
- Any static file host

No server, no build tools required.
