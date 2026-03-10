/**
 * config.js — Central configuration for GroundLM 2026
 * Edit this file to update site-wide content without touching HTML/CSS.
 */

const SITE = {
  name: "GroundLM 2026",
  fullName: "Grounding Language Models: Learning Faithfully and Efficiently",
  conference: "EMNLP 2026",
  email: "groundlm@googlegroups.com",
  openreviewUrl: "#", // Replace with actual OpenReview URL
  emnlpUrl: "https://2026.emnlp.org/",      // Replace with EMNLP 2026 URL

  announcement: {
    text: "CFP Open — Direct submissions due <strong>2026-06-01 (AoE)</strong>.",
    linkText: "Read CFP ↗",
    linkHref: "#cfp",
  },

  hero: {
    date: "24-29 Oct, 2026 (date&time TBD)",
    location: "Budapest, Hungary",
    description: `A workshop at EMNLP 2026 bringing together researchers working on grounding,
      faithfulness, and efficiency in large language models — from retrieval-augmented generation
      and knowledge grounding to hallucination mitigation and evaluation.`,
  },
};

/**
 * Important dates. Each entry: { label, date, badge }
 * badge: "upcoming" | "past" | null
 */
const DATES = [
  { label: "Direct paper submission deadline",   date: "2026-06-01", badge: "upcoming" },
  { label: "ARR commitment deadline",            date: "2026-06-25", badge: null },
  { label: "Notification of acceptance",         date: "2026-07-03", badge: null },
  { label: "Camera-ready paper due",             date: "2026-08-01", badge: null },
  { label: "Workshop date",                      date: "2026-10-TBD", badge: null },
];

/**
 * Invited speakers. Each entry: { name, affiliation, status, bio, url, photo }
 * status: "confirmed" | "tba"
 * photo: path to image, or null to show initials
 */
const SPEAKERS = [
  {
    name: "Speaker Name",
    affiliation: "University / Organization, Country",
    status: "confirmed",
    bio: "Brief bio or research focus describing the speaker's expertise in grounding and LLMs.",
    url: "#",
    photo: null,
  },
  {
    name: "Speaker Name",
    affiliation: "University / Organization, Country",
    status: "confirmed",
    bio: "Brief bio or research focus describing the speaker's expertise in grounding and LLMs.",
    url: "#",
    photo: null,
  },
  {
    name: "Speaker Name",
    affiliation: "University / Organization, Country",
    status: "tba",
    bio: "Brief bio or research focus describing the speaker's expertise in grounding and LLMs.",
    url: "#",
    photo: null,
  },
  {
    name: "Speaker Name",
    affiliation: "University / Organization, Country",
    status: "tba",
    bio: "Brief bio or research focus describing the speaker's expertise in grounding and LLMs.",
    url: "#",
    photo: null,
  },
];

/**
 * Organizers. Each entry: { name, affiliation, url, photo }
 * photo: path to image, or null to show initials
 */
const ORGANIZERS = [
  { name: "Organizer Name", affiliation: "University, Country", url: "#", photo: null },
  { name: "Organizer Name", affiliation: "University, Country", url: "#", photo: null },
  { name: "Organizer Name", affiliation: "University, Country", url: "#", photo: null },
  { name: "Organizer Name", affiliation: "University, Country", url: "#", photo: null },
  { name: "Organizer Name", affiliation: "University, Country", url: "#", photo: null },
];

/**
 * Workshop program. Each entry: { time, title, speaker, type }
 * type: "talk" | "break" | "panel" | "poster"
 */
const PROGRAM = [
  { time: "9:00",  title: "Opening Remarks",                              speaker: "Organizing Committee",    type: "talk"   },
  { time: "9:15",  title: "Invited Talk 1",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "10:00", title: "Invited Talk 2",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "10:45", title: "☕ Coffee Break",                              speaker: null,                      type: "break"  },
  { time: "11:00", title: "Contributed Oral Papers",                      speaker: "Selected papers (TBD)",   type: "talk"   },
  { time: "12:30", title: "🍽 Lunch + Student Mentoring",                speaker: null,                      type: "break"  },
  { time: "14:00", title: "Invited Talk 3",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "14:45", title: "Invited Talk 4",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "15:30", title: "☕ Coffee Break",                              speaker: null,                      type: "break"  },
  { time: "15:45", title: "Poster Session",                               speaker: "All accepted papers",     type: "poster" },
  { time: "17:00", title: "Panel Discussion: Open Challenges in Grounding", speaker: "Invited speakers + moderator", type: "panel" },
  { time: "17:45", title: "Closing Remarks + Best Paper Award",           speaker: "Organizing Committee",    type: "talk"   },
  { time: "18:00", title: "🎉 Social / Reception",                       speaker: null,                      type: "break"  },
];

/**
 * Topics of interest. Plain strings.
 */
const TOPICS = [
  "Retrieval-augmented generation (RAG): architectures, training, and evaluation.",
  "Knowledge grounding: incorporating structured and unstructured knowledge into LLMs.",
  "Hallucination detection, mitigation, and faithful generation.",
  "Efficient fine-tuning and adaptation for grounded language understanding.",
  "Grounding in multimodal settings: vision-language models and beyond.",
  "Attribution, citation, and source verification in generated text.",
  "Benchmarking and evaluation of factuality, faithfulness, and groundedness.",
  "Parameter-efficient learning for knowledge-intensive tasks.",
  "Entity linking, coreference resolution, and world knowledge integration.",
  "Applications in healthcare, science, law, and enterprise settings.",
  "Robustness, reliability, and calibration of grounded LLM systems.",
  "Data-centric approaches: annotation, augmentation, and quality for grounding.",
];

/**
 * FAQ items. Each entry: { q, a }
 */
const FAQ = [
  {
    q: "Can I submit work that is under review elsewhere?",
    a: "For archival submissions, the work must not be under review at any other venue during the GroundLM review period. For non-archival extended abstracts, concurrent submission to other venues is allowed.",
  },
  {
    q: "Can I submit work that has already been published?",
    a: "Previously published work may be submitted as a non-archival extended abstract (up to 2 pages). It will not appear in the proceedings but may be presented as a poster or talk. Please indicate prior publication clearly in your submission.",
  },
  {
    q: "Is there a preprint policy?",
    a: "Yes. Authors may post preprints at any time without violating our anonymity policy. If your paper is under review, the preprint should not explicitly identify it as a GroundLM submission.",
  },
  {
    q: "Will the workshop have a proceedings volume?",
    a: "Yes. Accepted archival papers will appear in the ACL Anthology as part of the EMNLP 2026 workshop proceedings. Non-archival papers will not appear in the anthology.",
  },
  {
    q: "What template should I use for formatting?",
    a: "Please use the official EMNLP 2026 style files (LaTeX and Word templates). The style files will be linked once released by the EMNLP organizers. Reviews are double-blind, so please remove all author information.",
  },
  {
    q: "Will there be a virtual attendance option?",
    a: "We plan to accommodate virtual participation to the extent possible, following EMNLP 2026 guidelines. Further details will be shared closer to the workshop date.",
  },
  {
    q: "How can I contact the organizers?",
    a: `For questions not covered by this FAQ, please email us at <a href="mailto:${SITE.email}" style="color:var(--accent)">${SITE.email}</a>. We aim to respond within 3 business days.`,
  },
];
