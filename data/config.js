/**
 * config.js — Central configuration for GroundLM 2026
 * Edit this file to update site-wide content without touching HTML/CSS.
 */

const SITE = {
  name: "GroundLM 2026",
  fullName: "Grounding Language Models: Learning Faithfully and Efficiently",
  conference: "EMNLP 2026",
  email: "groundlm@googlegroups.com",
  openreviewUrl: "https://openreview.net/group?id=EMNLP/2026/Workshop/GroundLM",
  arrCommitmentOpenreviewUrl: "https://openreview.net/group?id=EMNLP/2026/Workshop/GroundLM_ARR_Commitment",
  sharedTasksOpenreviewUrl: "https://openreview.net/group?id=EMNLP/2026/Workshop/GroundLM_Shared_Tasks",
  discordUrl: "https://discord.gg/qY8Agahbn",
  reviewerFormUrl: "https://forms.gle/PMB4cfb1p32exSB19",
  emnlpUrl: "https://2026.emnlp.org/",      // Replace with EMNLP 2026 URL

  announcement: {
    text: "Camera-ready paper instructions will be released on <strong>2026-09-03 (AoE)</strong>. Stay tuned!",
    linkText: "View important dates ↗",
    linkHref: "#dates",
  },

  hero: {
    date: "October 29, 2026, 9:00-17:30",
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
  { label: "Track 1: Direct submission deadline", date: "2026-07-07", badge: "past" },
  { label: "Track 2: ARR commitment deadline",    date: "2026-08-05", badge: "past" },
  { label: "Acceptance release",                  date: "2026-08-29", badge: "past" },
  { label: "Camera-ready paper due",              date: "2026-09-12", badge: "upcoming" },
  { label: "Workshop date",                      date: "2026-10-29, 9:00-17:30", badge: "upcoming" },
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
    bio: "Assistant Professor at the University of Waterloo and Faculty Member at the Vector Institute; works on computational linguistics and natural language processing.",
    url: "https://cs.uwaterloo.ca/~fhs/",
    photo: "img/freda.jpg",
  },
  {
    name: "Lei Li",
    affiliation: "Carnegie Mellon University",
    status: "confirmed",
    bio: "Associate Professor at Carnegie Mellon University; works on generative AI for language and science",
    url: "https://lileicc.github.io/",
    photo: "img/lei.jpg",
  },
  {
    name: "Krzysztof Czarnecki",
    affiliation: "University of Waterloo",
    status: "confirmed",
    bio: "Professor at the University of Waterloo; works on autonomous systems and generative software development.",
    url: "https://uwaterloo.ca/electrical-computer-engineering/profile/k2czarne",
    photo: "img/krzysztof.jpg",
  },
  {
    name: "Valentino Maiorca",
    affiliation: "Institute of Science and Technology Austria (ISTA)",
    status: "confirmed",
    bio: "Postdoctoral Researcher at ISTA; works on latent geometry, representation alignment, and controllable neural networks.",
    url: "https://vale.maiorca.xyz/",
    photo: "img/valentino-maiorca.jpg",
  },
  {
    name: "Danae Sánchez",
    affiliation: "University of Copenhagen",
    status: "confirmed",
    bio: "Postdoctoral Researcher at the Center for AI in Society, University of Copenhagen; works on vision-language models, multimodal reasoning, AI safety, and robustness.",
    url: "https://danaesavi.github.io/",
    photo: "img/danae_photo.jpg",
  },
  {
    name: "Anya Belz",
    affiliation: "Dublin City University",
    status: "confirmed",
    bio: "Full Professor of Computer Science (Natural Language Processing) at Dublin City University; works on natural language generation, NLP evaluation, text analysis, and image description.",
    url: "https://www.dcu.ie/computing/people/anya-belz",
    photo: "img/anya-belz.jpg",
  },
  {
    name: "Iryna Gurevych",
    affiliation: "Technical University of Darmstadt",
    status: "confirmed",
    bio: "Full Professor at the Technical University of Darmstadt and head of the UKP Lab; works on information extraction, semantic text processing, machine learning, and NLP applications in the social sciences and humanities.",
    url: "https://www.informatik.tu-darmstadt.de/ukp/ukp_home/head_ukp/index.en.jsp",
    photo: "img/iryna-gurevych.png",
  },
  {
    name: "Ivan Titov",
    affiliation: "University of Edinburgh",
    status: "confirmed",
    bio: "Personal Chair of Natural Language Processing at the University of Edinburgh's School of Informatics and member of the Institute for Language, Cognition and Computation.",
    url: "https://people.inf.ed.ac.uk/Ivan_Titov.html",
    photo: "img/ivan-titov.gif",
  },


];

/**
 * Panelists. Each entry: { name, affiliation, status, bio, url, photo }
 */
const PANELISTS = [
  {
    name: "Carolin Lawrence",
    affiliation: "NEC Laboratories Europe",
    status: "confirmed",
    bio: "Chief Research Scientist at NEC Laboratories Europe; works on making GenAI interpretable, trustworthy and reliable.",
    url: null,
    photo: "img/carolin-lawrence.jpg",
  },
  {
    name: "Amin Shabani",
    affiliation: "RBC Borealis",
    status: "confirmed",
    bio: "Senior Machine Learning Researcher at RBC Borealis, where he develops advanced models for financial applications. He holds a Ph.D. in Computer Science from Simon Fraser University and an M.Sc. from Seoul National University. His research focuses on the intersection of generative models, large language models, and time-series forecasting. He has published at ICLR, NeurIPS, and CVPR, and previously worked as a Research Scientist Intern at Adobe on automated layout design.",
    url: null,
    photo: "img/amin-shabani.jpg",
  },
];

/** Sponsors. Each entry: { name, url } */
const SPONSORS = [
  { name: "Tencent", url: null },
  { name: "RBC Borealis", url: null },
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
  { time: "9:15",  title: "Invited Talk 1",                               speaker: "Iryna Gurevych",          type: "talk"   },
  { time: "9:55",  title: "Invited Talk 2",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "10:35", title: "☕ Coffee Break",                              speaker: null,                      type: "break"  },
  { time: "10:55", title: "Invited Talk 3",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "11:35", title: "Invited Talk 4",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "12:15", title: "Invited Talk 5",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "12:55", title: "🍽 Lunch + Poster Session",                    speaker: "All accepted papers",     type: "poster" },
  { time: "13:40", title: "Invited Talk 6",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "14:20", title: "Invited Talk 7",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "15:00", title: "☕ Coffee Break",                              speaker: null,                      type: "break"  },
  { time: "15:20", title: "Invited Talk 8",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "16:00", title: "Invited Talk 9",                               speaker: "Speaker TBD",             type: "talk"   },
  { time: "16:40", title: "Panel Discussion: Open Challenges in Grounding", speaker: "Amin Shabani, Carolin Lawrence, invited speakers + moderator", type: "panel" },
  { time: "17:25", title: "Closing Remarks",                              speaker: "Organizing Committee",    type: "talk"   },
  { time: "17:30", title: "End of Workshop",                              speaker: null,                      type: "break"  },
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
    a: "For Track 1 archival submissions, the work must not be under review at another venue during the GroundLM review period. Non-archival submissions may overlap with previously published or concurrently submitted work. Track 2 is reserved for eligible ARR May 2026-or-earlier papers and papers rejected from other conferences.",
  },
  {
    q: "What are the two submission tracks?",
    a: "Track 1 direct submissions closed on July 7, 2026 AoE. Track 2 is an ARR commitment fast track, due August 5, 2026 AoE, for eligible ARR May 2026-or-earlier papers and papers rejected from other conferences.",
  },
  {
    q: "Can I self-nominate as a reviewer or area chair?",
    a: `Yes. Please fill out the <a href="${SITE.reviewerFormUrl}" style="color:var(--accent)">reviewer and area chair self-nomination form</a>.`,
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
