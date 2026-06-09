/**
 * main.js — GroundLM 2026
 * Renders all dynamic sections from data/config.js.
 * Each render* function targets a specific element ID.
 */

/* ── HELPERS ── */
function initials(name) {
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
}

function avatar(person, size = 'md') {
  const dim = size === 'sm' ? 56 : 80;
  const fs  = size === 'sm' ? '1.1rem' : '1.6rem';
  if (person.photo) {
    return `<div class="speaker-avatar" style="width:${dim}px;height:${dim}px">
      <img src="${person.photo}" alt="${person.name}" loading="lazy">
    </div>`;
  }
  return `<div class="${size === 'sm' ? 'organizer-avatar' : 'speaker-avatar'}" style="font-size:${fs}">
    ${initials(person.name)}
  </div>`;
}

/* ── ANNOUNCEMENT BAR ── */
function renderAnnouncement() {
  const el = document.getElementById('ann-bar');
  if (!el || !SITE.announcement) return;
  const href = SITE.announcement.linkHref;
  const linkHref = href.startsWith('#') && !document.querySelector(href)
    ? `index.html${href}`
    : href;
  el.innerHTML = `${SITE.announcement.text}
    <a href="${linkHref}">${SITE.announcement.linkText}</a>`;
}

/* ── HERO ── */
function renderHero() {
  const h = SITE.hero;
  const el = document.getElementById('hero-content');
  if (!el) return;
  el.innerHTML = `
    <div class="hero-badge">${SITE.conference} Workshop</div>
    <h1>${SITE.fullName.replace(/:\s*/, ':<br><em>') + '</em>'}</h1>
    <div class="hero-subtitle">
      <span>📅 ${h.date}</span>
      <span class="sep">·</span>
      <span>📍 ${h.location}</span>
    </div>
    <p class="hero-desc">${h.description}</p>
    <div class="hero-ctas">
      <a href="#cfp" class="btn btn-primary">Call for Papers</a>
      <a href="shared-tasks.html" class="btn btn-primary">Shared Tasks</a>
      <span class="hero-cta-break" aria-hidden="true"></span>
      <a href="${SITE.openreviewUrl}" class="btn btn-outline">Track 1 Submission</a>
      <a href="${SITE.arrCommitmentOpenreviewUrl}" class="btn btn-outline">Track 2 ARR Commitment</a>
      <a href="${SITE.reviewerFormUrl}" class="btn btn-outline">Reviewer / AC Self-Nomination</a>
      <a href="#dates" class="btn btn-outline">Paper Submission Dates</a>
    </div>`;
}

/* ── TOPICS ── */
function renderTopics() {
  const el = document.getElementById('topics-list');
  if (!el) return;
  el.innerHTML = TOPICS.map(t => `<div class="topic-item">${t}</div>`).join('');
}

/* ── DATES ── */
function renderDates() {
  const el = document.getElementById('dates-body');
  if (!el) return;
  el.innerHTML = DATES.map(d => {
    const badge = d.badge
      ? `<span class="badge badge-${d.badge}">${d.badge}</span>`
      : '';
    return `<tr>
      <td>${d.label}${badge}</td>
      <td class="date-col">${d.date}</td>
    </tr>`;
  }).join('');
}

/* ── SPEAKERS ── */
function renderSpeakers() {
  const el = document.getElementById('speakers-grid');
  if (!el) return;
  el.innerHTML = SPEAKERS.map(s => `
    <div class="speaker-card">
      ${avatar(s, 'md')}
      <h3>${s.url && s.url !== '#'
        ? `<a href="${s.url}" style="color:inherit;text-decoration:none">${s.name}</a>`
        : s.name}</h3>
      <p class="speaker-affil">${s.affiliation}</p>
      <span class="badge badge-${s.status}">${s.status}</span>
      ${s.bio ? `<p class="speaker-bio">${s.bio}</p>` : ''}
    </div>`).join('');
}

/* ── ORGANIZERS ── */
function renderOrganizers() {
  const el = document.getElementById('organizers-grid');
  if (!el) return;
  el.innerHTML = ORGANIZERS.map(o => `
    <div class="organizer-card">
      ${avatar(o, 'sm')}
      <h3>${o.url && o.url !== '#'
        ? `<a href="${o.url}" style="color:inherit;text-decoration:none">${o.name}</a>`
        : o.name}</h3>
      <div class="organizer-affil">${o.affiliation}</div>
    </div>`).join('');
}

/* ── PROGRAM ── */
function renderProgram() {
  const el = document.getElementById('program-rows');
  if (!el) return;
  el.innerHTML = PROGRAM.map(p => `
    <div class="program-row type-${p.type}">
      <div class="program-time">${p.time}</div>
      <div class="program-event">
        <strong>${p.title}</strong>
        ${p.speaker ? `<div class="speaker-tag">${p.speaker}</div>` : ''}
      </div>
    </div>`).join('');
}

/* ── FAQ ── */
function renderFaq() {
  const el = document.getElementById('faq-list');
  if (!el) return;
  el.innerHTML = FAQ.map(f => `
    <div class="faq-item">
      <div class="faq-q" onclick="this.closest('.faq-item').classList.toggle('open')">${f.q}</div>
      <div class="faq-a">${f.a}</div>
    </div>`).join('');
}

/* ── FOOTER CONTACT ── */
function renderContactLinks() {
  document.querySelectorAll('[data-email]').forEach(el => {
    el.href = `mailto:${SITE.email}`;
    el.textContent = SITE.email;
  });
  document.querySelectorAll('[data-emnlp-url]').forEach(el => {
    el.href = SITE.emnlpUrl;
  });
  document.querySelectorAll('[data-openreview-url]').forEach(el => {
    el.href = SITE.openreviewUrl;
  });
  document.querySelectorAll('[data-arr-openreview-url]').forEach(el => {
    el.href = SITE.arrCommitmentOpenreviewUrl;
  });
  document.querySelectorAll('[data-shared-tasks-openreview-url]').forEach(el => {
    el.href = SITE.sharedTasksOpenreviewUrl;
  });
  document.querySelectorAll('[data-reviewer-form-url]').forEach(el => {
    el.href = SITE.reviewerFormUrl;
  });
}

/* ── NAV SCROLL HIGHLIGHT ── */
function initScrollNav() {
  const sections = document.querySelectorAll('section[id], .hero[id]');
  const navLinks  = document.querySelectorAll('nav a[href^="#"]');
  if (!sections.length || !navLinks.length) return;
  window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(s => {
      if (window.scrollY >= s.offsetTop - 100) current = s.id;
    });
    navLinks.forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === '#' + current);
    });
  }, { passive: true });
}

/* ── HAMBURGER ── */
function initHamburger() {
  const btn = document.getElementById('hamburger');
  const nav = document.getElementById('main-nav');
  if (btn && nav) btn.addEventListener('click', () => nav.classList.toggle('open'));
}

/* ── BOOT ── */
document.addEventListener('DOMContentLoaded', () => {
  renderAnnouncement();
  renderHero();
  renderTopics();
  renderDates();
  renderSpeakers();
  renderOrganizers();
  renderProgram();
  renderFaq();
  renderContactLinks();
  initScrollNav();
  initHamburger();
});
