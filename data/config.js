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
    name: "Freda Shi",
    affiliation: "University of Waterloo, Vector Institute",
    status: "confirmed",
    bio: "Assistant Professor at the University of Waterloo and Faculty Member at the Vector Institute; works on learning language through grounding, computational multilingualism, and related machine learning aspects.",
    url: "https://cs.uwaterloo.ca/~fhs/",
    photo: "img/freda.jpg",
  },
  {
    name: "Lei Li",
    affiliation: "Carnegie Mellon University",
    status: "confirmed",
    bio: "Associate Professor at Carnegie Mellon University; works on generative AI for language and science, including multilingual NLP, machine translation (text, speech), security of large language models, agentic LLM, and AI for drug discovery and protein design.",
    url: "https://lileicc.github.io/",
    photo: "img/lei.jpg",
  },

];

/**
 * Organizers. Each entry: { name, affiliation, url, photo }
 * photo: path to image, or null to show initials
 */
const ORGANIZERS = [
  { name: "Yimu Wang", affiliation: "University of Waterloo", url: "https://yimuwangcs.github.io/", photo: "img/yimuwang.jpg" },
  { name: "Yee Man Choi", affiliation: "University of Waterloo", url: "https://kathcym.github.io/", photo: "img/Kath_pic.jpg" },
  { name: "Di Wu", affiliation: "University of Amsterdam", url: "https://moore3930.github.io/", photo: "img/wu.jpg" },
  { name: "Siqi Ouyang", affiliation: "Carnegie Mellon University", url: "https://owaski.github.io/", photo: "img/siqi.jpg" },
  { name: "Mozhgan Nasr Azadani", affiliation: "University of Waterloo", url: "https://mozhgan91.github.io/", photo: "img/mozhgan.jpg" },
  { name: "Yi R. (May) Fung", affiliation: "Hong Kong University of Science and Technology", url: "https://mayrfung.github.io/", photo: "img/yfung.jpg" },
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
  "Efficient grounding: data-, feedback-, and compute-efficient methods; scaling strategies (merging, ensembles); parameter-efficient adaptation (PEFT, LoRA, prompt tuning)",
  "Faithful grounding: reducing hallucinations; attribution and verifiability; probing and diagnostics; implicit vs.\ explicit grounding",
  "Grounding mechanisms beyond text: retrieval and external knowledge; interaction, feedback, and outcomes; multimodal perception; action and embodiment",
  "Evaluation: benchmarks, metrics, and protocols for multimodal and interactive grounding",
  "Safety and reliability: robustness, privacy, and bias mitigation for grounded systems that connect to tools, sensors, or external data",
  "Low-resource and multilingual grounding: domain adaptation; support for underrepresented languages and communities",
  "Applications: domain-specific grounded systems (e.g., retrieval QA, education, healthcare, robotics, tool use)",
  "Open problems: long-horizon grounded reasoning and distribution shift; negative results, failure cases, and limitations",
];

/**
 * FAQ items. Each entry: { q, a }
 */
const FAQ = [
  {
    q: "Can I submit work that is under review elsewhere?",
    a: "For archival submissions, the work must not be under review at any other venue during the GroundLM review period. For non-archival submissions, concurrent submission to other venues is allowed.",
  },
  {
    q: "Can I submit work that has already been published?",
    a: "Previously published work may be submitted as a non-archival submission. It will not appear in the proceedings but may be presented as a poster or talk. Please indicate prior publication clearly in your submission.",
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
