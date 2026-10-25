# Investigación: IA generativa en hackathones y concursos de programación

## Resumen

No official source found for CCC AI-use rules: the pages we could verify (Cloudflight blog posts 2021 and 2023, the GLS Poznan site rules, a Cluj university announcement) are silent on generative-AI use, and the only "AI" they mention is a machine-learning track (#ai, started 2021) that is separate from any policy on AI tools. The CCC is physically hosted at partner venues (45 locations in 15 countries in spring 2023; hybrid since 2021), so on-site supervision is its implicit main defence. Elsewhere, measures documented are: MOSS similarity checks with human review (HackerRank), explicit LLM rule sets (AtCoder Heuristic Contest), embracing AI (MIT Policy Hackathon, Searce), and academic proposals (chess-style governance, in-person contests). Evidence suggests similarity detectors miss AI-assisted cheating, which pushes organizers toward in-person formats and human interviews. For the next CCC, a reasonable expectation (inference, not verified) is that on-site format continues, with the separate AI/data track retained and possibly an explicit written AI policy. The CCC's own register.codingcontest.org rules/FAQ, the 41st/42nd edition announcements and the Codeforces policy were not verified here.

## Hallazgos

### 1. (medium, voto 3-0 on each underlying claim)

No verified official CCC rule on generative-AI use (ChatGPT/Copilot/Claude) was found; the Cloudflight blog posts (2021, 2023) and the GLS Poznan CCC rules page contain no AI-use, plagiarism, proctoring or supervision provisions.

**Evidencia:** All four pages were fetched and checked by 3 verifiers each; all are silent on AI-use rules. The GLS page only defers to the Organiser's regulations at register.codingcontest.org, which were not fetched. The GLS rules date from March 2024 and a Cloudflight 42nd edition (Oct 23, 2026) page was mentioned by one verifier, not examined. Silence is not proof of no policy.

- https://www.cloudflight.io/en/blog/europes-biggest-coding-contest-will-take-place-on-november-5th-as-hybrid-event/
- https://www.cloudflight.io/en/blog/cloudflight-coding-contest-2023-new-partners-and-locations-continue-event-success/
- https://gls-group.com/PL/en/ccc-rules
- https://ac.utcluj.ro/anunt/cloudflight-coding-contest.html

### 2. (high, voto 3-0)

CCC 'AI' is a machine-learning competition track, not a policy on AI tools. Tracks: School (up to 19 years old, 2h), Classic (algorithmic, afternoon) and AI/ML challenge (since 2021). Local sites such as GLS Poznan run #classic and/or #ai categories with prizes for top 3 in each. Cluj listed 4h for #classic/#ai and 2h for #school.

**Evidencia:** Organizer pages describe the AI track as 'a complex machine learning task', introduced in 2021 (35th CCC). Track structure confirmed for 2021 and 2023; a verifier noted a 42nd edition (Oct 2026) listing #school, #classic, #data/ai, not independently checked.

- https://www.cloudflight.io/en/blog/cloudflight-coding-contest-2023-new-partners-and-locations-continue-event-success/
- https://www.cloudflight.io/en/blog/europes-biggest-coding-contest-will-take-place-on-november-5th-as-hybrid-event/
- https://gls-group.com/PL/en/ccc-rules
- https://ac.utcluj.ro/anunt/cloudflight-coding-contest.html

### 3. (high, voto 3-0)

The CCC is run on-site at partner venues (hybrid since the 35th edition in Nov 2021, about 20 cities; spring 2023: 45 locations in 15 countries, about 4,000 participants). Participants bring their own laptops per the GLS site rules. This physical format is the implicit main supervision, but no source states it was chosen to counter AI.

**Evidencia:** Organizer blog posts give the figures (self-reported marketing numbers). The GLS 'own laptop' clause (II.8) appeared in verifier notes; a separate claim that the host supervises/provides internet was refuted 0-3 and is not asserted. Whether any on-site proctoring exists is unverified.

- https://www.cloudflight.io/en/blog/europes-biggest-coding-contest-will-take-place-on-november-5th-as-hybrid-event/
- https://www.cloudflight.io/en/blog/cloudflight-coding-contest-2023-new-partners-and-locations-continue-event-success/
- https://gls-group.com/PL/en/ccc-rules

### 4. (medium, voto 3-0 (20250616 ban); 0-3 on permitted-uses claim)

AtCoder Heuristic Contest (AHC) published explicit LLM rules (Version 20250616) banning automated mass generation of outputs/prompts via APIs or scripts and selecting among candidates by score. These rules were later reported (search snippets only, unverified) to be superseded for short AHCs by a stricter version (20260818) banning generative AI broadly, with human-only and with-AI divisions under consideration for long contests.

**Evidencia:** Primary AtCoder page fetched; ban on 'Automatically generating a large number of outputs using APIs or scripts' confirmed, including the 100-prompt example. The page says it no longer applies to short-term contests. The detailed list of permitted uses was refuted 0-3, so do not cite it. The 2026 rule set comes from snippets only.

- https://info.atcoder.jp/entry/ahc-llm-rules-en

### 5. (medium, voto 3-0 (HackerRank, Purdue anecdote); 0-3 on interview-efficacy and low-similarity claims)

Automated similarity detection is the standard tool (HackerRank enables MOSS by default; Kattis runs similarity checks) but has documented limits: MOSS cannot identify the source and HackerRank recommends human review of code playback; a Purdue course case shows ChatGPT-assisted code passing Moss and Kattis, caught only by instructor intuition and an interview.

**Evidencia:** HackerRank vendor documentation (primary) confirmed 3-0. The Purdue claim is a single-author preprint with one anecdote plus cited work, so it supports 'can fail', not a measured detection rate. Claims that oral interviews are near-100% effective and that ChatGPT code has lower pairwise similarity were refuted 0-3 and must not be repeated.

- https://hackerrank-knowledge-base.help.usepylon.com/articles/2106056073
- https://arxiv.org/html/2505.08244v1

### 6. (medium, voto 3-0 (FAIR method and proposals; HackerNoon thesis); 0-3 on AI-resistant-problems claim)

Academic proposals: the FAIR paper (CHI 2026) combines 37 interviews, a survey of 207 contestants and Codeforces logs 2022-2025, and proposes chess-inspired governance: real-time LLM checks in online contests, peer monitoring and reporting, and cross-validation against offline performance. A HackerNoon opinion piece argues online contests cannot be secured against AI and that in-person contests are the fix.

**Evidencia:** The arXiv abstract was fetched and confirmed. These are proposals, not evidence the measures work or are adopted. The HackerNoon piece is an opinion blog (the 'no online solution' line is relayed from a third party); a claim that the author judges AI-resistant problem design futile was refuted 0-3.

- https://arxiv.org/pdf/2509.15867v2
- https://hackernoon.com/the-end-of-fair-play-in-coding-contests

### 7. (medium, voto 3-0)

Some events embrace AI instead of fighting it: the 2024 MIT Policy Hackathon encouraged teams to use and cite generative AI tools, and the Searce Gen AI hackathon (Aug 2023) scored 'Use of GenAI' at 40 of 100 points. These are not models for combating AI use.

**Evidencia:** Both are organizer/institutional primary pages for single events with a GenAI theme; one verifier flagged that Searce 'required' is slightly strong (heavily weighted, not strictly mandated). Outcomes of the stance were not assessed.

- https://news.mit.edu/2024/generating-policy-of-tomorrow-0124
- https://lp.searce.com/contest-rules-gen-ai-hackathon-august-2023

## Advertencias

- Large gaps remain against the original question. Not verified or not surviving verification: the official CCC rules/FAQ at codingcontest.org and register.codingcontest.org; CCC 41st and autumn 2026 announcements; ICPC, Codeforces (only mentioned via the FAIR paper's logs and a search aside about a Codeforces AI ban), Google Hash Code, Advent of Code, Kaggle and MLH policies; documented disqualification cases and controversies; proctoring and AI-code-detector effectiveness; time-based anomaly detection; oral defences. Several sources are old (2021-2024), so their silence on AI is expected. Seven claims were refuted and excluded, including that rule breaches lead to exclusion by the host (rejected as phrased) and that oral interviews are near-100% effective. The prediction for the next CCC edition is inference, not evidence. Item (4) of the question is therefore answered only tentatively. Most strong sources are tangential (AtCoder, HackerRank, academic papers) rather than CCC-specific.

## Preguntas abiertas

- What do the official CCC rules and FAQ on register.codingcontest.org / codingcontest.org say about AI tools, and do they differ between the School, Classic and Data/AI tracks in the 41st and 42nd (autumn 2026) editions?
- Do CCC on-site venues apply any proctoring or device restrictions (network limits, screen monitoring, own-laptop checks), and has any participant been disqualified for AI use?
- What are the current ICPC, Codeforces, Google Hash Code/Advent of Code and Kaggle AI policies, and what disqualification cases or controversies have been documented since 2023?
- Did AtCoder actually adopt the 20260818 short-contest ban and split human-only/with-AI divisions, and how effective were those rules in practice?

## Refutado

- {"claim": "The page was published in October 2021 (updated 2024), so it predates generative-AI tools like ChatGPT and Copilot and has no bearing on 2023-2026 AI rules.", "vote": "0-3", "source": "https://www.cloudflight.io/en/blog/europes-biggest-coding-contest-will-take-place-on-november-5th-as-hybrid-event/"}
- {"claim": "Oral interviews/code defense are highly effective at detecting plagiarism (near 100% success) but very labor-intensive (about 120 interviews over 12 weeks in S25).", "vote": "0-3", "source": "https://arxiv.org/html/2505.08244v1"}
- {"claim": "ChatGPT-generated code tends to have lower pairwise similarity with other submissions than students' code has with each other, so similarity detection is unreliable for LLM code.", "vote": "0-3", "source": "https://arxiv.org/html/2505.08244v1"}
- {"claim": "The rules still permit generative AI for translation, idea generation, code completion, bug fixing and natural-language-to-code, provided the use is not in the prohibited category. Single-prompt agent tools are allowed only if they do not internally generate or select among multiple candidates.", "vote": "0-3", "source": "https://info.atcoder.jp/entry/ahc-llm-rules-en"}
- {"claim": "The author states that LLM cheating is not really preventable and that organizers should not discard solid problems just because AI can solve them (i.e. AI-resistant problem design is judged futile).", "vote": "0-3", "source": "https://hackernoon.com/the-end-of-fair-play-in-coding-contests"}
- {"claim": "Rule breaches are judged by the on-site Host team, whose decision is final, and a breach leads to exclusion from the Contest.", "vote": "0-3", "source": "https://gls-group.com/PL/en/ccc-rules"}
- {"claim": "Participants compete at the venue on their own laptops, with the Host providing space and internet access (on-site, host-supervised format).", "vote": "0-3", "source": "https://gls-group.com/PL/en/ccc-rules"}

