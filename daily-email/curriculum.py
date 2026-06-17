"""90-day reading curriculum derived from 99-optional-speedrun.

Every study day names the exact rule sections and cases to read, links each to a
verified free source, says what to DO with it, and carries a one-line "connect"
note so the 90 days build on each other.

Link sources (all verified):
  - Rules / statutes:  Cornell LII  (FRCP, FRE, UCC, U.S. Code)
  - Supreme Court:     Cornell LII  /supremecourt/text/<vol>/<page>
  - Constitution:      Cornell LII  /constitution/<name>
  - Non-SCOTUS cases:  CourtListener search (deterministic; opens the opinion)
  - ABA Model Rules:   ABA Model Rules table of contents (open the named rule)

Run `python curriculum.py` to print the full schedule and assert it is 90 days.
"""
from urllib.parse import quote

PHASE_ONE = "Phase One: Foundations"
PHASE_TWO = "Phase Two: Core and Codes"
PHASE_THREE = "Phase Three: Advanced and Litigation"

# Real-JD-year placement. Pacing stays even (one subject per week), but every
# subject is tagged with the year a traditional JD student would take it, so the
# email parallels a real 1L -> 2L -> 3L curriculum (matches the repo's
# 01-1l / 02-2l / 03-3l structure). Descriptors come from those folder names.
YEAR_LABELS = {
    "1L": "1L · Foundation Year",
    "2L": "2L · Doctrinal Depth and Codes",
    "3L": "3L · Practice, Synthesis and Launch",
}
YEAR_ORDER = ["1L", "2L", "3L"]

LII = "https://www.law.cornell.edu"


def frcp(n):   return f"{LII}/rules/frcp/rule_{n}"
def fre(n):    return f"{LII}/rules/fre/rule_{n}"
def ucc(a, s): return f"{LII}/ucc/{a}/{s}"
def usc(t, s): return f"{LII}/uscode/text/{t}/{s}"
def scotus(vol, page): return f"{LII}/supremecourt/text/{vol}/{page}"
def const(name):       return f"{LII}/constitution/{name}"
def cl(query): return f"https://www.courtlistener.com/?q={quote(query)}&type=o&order_by=score+desc"


ABA_RULES = ("https://www.americanbar.org/content/aba-cms-dotorg/en/groups/"
             "professional_responsibility/publications/model_rules_of_professional_conduct/"
             "model_rules_of_professional_conduct_table_of_contents/")

# Teaching materials follow the repo's T10/Ivy rule (see 00-start-here/05). Primary
# law and case-reading deliberately use Cornell LII + CourtListener, which that rule
# names as the nonprofit backbone for reading the law itself, regardless of rank.
# Casebook spines (Harvard H2O, Ivy):
CB_CIVPRO = ("Harvard H2O Civil Procedure 2024 (Harvard, Ivy)", "https://opencasebook.org/casebooks/9188-civil-procedure-2024/")
CB_TORTS = ("Harvard H2O Torts! (Harvard, Ivy)", "https://opencasebook.org/casebooks/2566-torts/")
CB_CONTRACTS = ("Harvard H2O Contracts (Harvard, Ivy)", "https://opencasebook.org/casebooks/11568-contracts/")
CB_PROPERTY = ("Harvard H2O Open Source Property (Harvard, Ivy)", "https://opencasebook.org/casebooks/510-open-source-property/")
CB_CRIM = ("Harvard H2O Criminal Law (Harvard, Ivy)", "https://opencasebook.org/casebooks/2459-criminal-law-spring-2021/")
CB_CRIMPRO = ("Harvard H2O Criminal Procedure (Harvard, Ivy)", "https://opencasebook.org/casebooks/8116-criminal-procedure/")
CB_BIZ = ("Harvard H2O Business Associations (Harvard, Ivy)", "https://opencasebook.org/casebooks/15328-business-associations/")
CB_EVID = ("Harvard H2O Federal Rules of Evidence (Harvard, Ivy)", "https://opencasebook.org/casebooks/230-federal-rules-of-evidence/as-printable-html/")
CB_ADMIN = ("Harvard H2O Administrative Law (Harvard, Ivy)", "https://opencasebook.org/casebooks/8962-administrative-law/")
CB_PR = ("Harvard H2O Professional Responsibility (Harvard, Ivy)", "https://opencasebook.org/casebooks/15389-professional-responsibility/")

# T10/Ivy deepening guides (from 00-start-here/06 directory), Ivy-first:
G_DUKE_RULES = ("Duke Court Rules guide (Duke, T10)", "https://law.duke.edu/lib/research-guides/court-rules")
G_DUKE_BA = ("Duke Business Associations guide (Duke, T10)", "https://law.duke.edu/lib/research-guides/business-associations/")
G_DUKE_UCC = ("Duke UCC research guide (Duke, T10)", "https://law.duke.edu/lib/research-guides/ucc/")
G_DUKE_ADMIN = ("Duke Federal Administrative Law guide (Duke, T10)", "https://law.duke.edu/lib/research-guides/federal-administrative-law/")
G_DUKE_ETHICS = ("Duke Legal Ethics guide (Duke, T10)", "https://law.duke.edu/lib/research-guides/legal-ethics/")
G_HARV_RESEARCH = ("Harvard Legal Research Strategy (Harvard, Ivy)", "https://guides.library.harvard.edu/law/researchstrategy")
G_HARV_STATUTES = ("Harvard Statutes research guide (Harvard, Ivy)", "https://guides.library.harvard.edu/law/statutes")
G_HARV_JUSTICE = ("Harvard Justice, Michael Sandel (Harvard, Ivy)", "https://justiceharvard.org/")
G_YALE_AVALON = ("Yale Avalon constitutional materials (Yale, Ivy)", "https://avalon.law.yale.edu/subject_menus/constpap.asp")
G_YALE_AMAR = ("Akhil Amar, Amarica's Constitution (Yale, Ivy)", "https://amaricasconstitution.podbean.com/")
G_COL_WRITING = ("Columbia legal writing resources (Columbia, Ivy)", "https://www.law.columbia.edu/academics/experiential/legal-writing/writing-center/legal-writing-resources")
G_COL_BLUESKY = ("Columbia CLS Blue Sky Blog (Columbia, Ivy)", "https://clsbluesky.law.columbia.edu/")
G_COL_GFOE = ("Columbia Global Freedom of Expression (Columbia, Ivy)", "https://globalfreedomofexpression.columbia.edu/")
G_PENN_RESEARCH = ("Penn Legal Research Fundamentals (Penn, Ivy)", "https://law.upenn.libguides.com/researchfundamentals")
G_PENN_STATUTES = ("Penn statutory research guide (Penn, Ivy)", "https://law.upenn.libguides.com/researchfundamentals/statutes")
G_PENN_REGREV = ("Penn The Regulatory Review (Penn, Ivy)", "https://www.theregreview.org/")
G_STAN_SCOTUS = ("Stanford Supreme Court Materials (Stanford, T10)", "https://guides.law.stanford.edu/supremecourt")

WEEKS = [
    {
        "num": 1, "year": "1L", "phase": PHASE_ONE, "subject": "Civil Procedure and Torts",
        "focus": "Learn how a lawsuit moves and why civil wrongs create liability.",
        "source_links": [CB_CIVPRO, CB_TORTS, G_DUKE_RULES],
        "canon": ["International Shoe (personal jurisdiction)", "Twombly / Iqbal (plausibility pleading)",
                  "FRCP 8, 12, 56", "Carroll Towing (Hand formula)", "Palsgraf (duty / proximate cause)"],
        "days": [
            {"topic": "Court power: jurisdiction and getting a defendant into court.",
             "reads": [
                 {"label": "FRCP 1", "url": frcp(1), "do": "Read just the rule itself — the two sentences at the top, not the Advisory Committee notes that fill the rest of the page. Note the 'just, speedy, and inexpensive' purpose that colors every other rule."},
                 {"label": "FRCP 4 (Summons)", "url": frcp(4), "do": "Skim (a)-(e), (h), (k); note how a court actually obtains power over a defendant through service."},
                 {"label": "International Shoe Co. v. Washington, 326 U.S. 310 (1945)", "url": scotus(326, 310), "do": "Read the majority; write the 'minimum contacts / fair play and substantial justice' test in one sentence."},
             ],
             "connect": "Personal jurisdiction is the gate: it decides whether a court may act at all. Tomorrow's pleading rules decide whether your complaint survives once you are through that gate."},
            {"topic": "Pleading a claim and the motion to dismiss.",
             "reads": [
                 {"label": "FRCP 8(a)", "url": frcp(8), "do": "Read (a): this is the 'notice pleading' baseline that Twombly and Iqbal later tightened."},
                 {"label": "FRCP 12(b)(6)", "url": frcp(12), "do": "Focus on (b)(6) and the (b) defenses: this is how a defendant attacks a complaint before answering."},
                 {"label": "Bell Atlantic Corp. v. Twombly, 550 U.S. 544 (2007)", "url": cl("Bell Atlantic Corp. v. Twombly"), "do": "Extract the 'plausibility' standard that replaced 'no set of facts.'"},
                 {"label": "Ashcroft v. Iqbal, 556 U.S. 662 (2009)", "url": cl("Ashcroft v. Iqbal"), "do": "Note the two-step method (set aside conclusions, then test plausibility) and that it applies to all civil cases."},
             ],
             "connect": "Yesterday's jurisdiction got you in the door; Twombly/Iqbal decide whether the complaint states a claim. Both sit at the front of your 'complaint -> judgment' attack outline."},
            {"topic": "Discovery and summary judgment.",
             "reads": [
                 {"label": "FRCP 26(b)(1)", "url": frcp(26), "do": "Read (b)(1) on scope and proportionality: this defines what each side can demand in discovery."},
                 {"label": "FRCP 56(a)", "url": frcp(56), "do": "Read (a): learn the 'no genuine dispute of material fact' standard for summary judgment."},
             ],
             "connect": "Pleadings frame the dispute, discovery fills in the facts, and summary judgment tests whether any fact actually needs a trial. That is the spine of the pretrial timeline."},
            {"topic": "Intentional torts.",
             "reads": [
                 {"label": "Vosburg v. Putney", "url": cl("Vosburg v. Putney"), "do": "Read for the 'unlawful touching' rule and the eggshell-plaintiff idea: intent to contact, not intent to harm."},
                 {"label": "Garratt v. Dailey", "url": cl("Garratt v. Dailey"), "do": "Read for 'substantial certainty' as a form of intent (the chair-pulling case)."},
             ],
             "connect": "Shift from procedure to substance. Note that tort 'intent' means intent to make contact, a lower bar than moral fault, and that negligence tomorrow needs no intent at all."},
            {"topic": "Negligence: duty, breach, causation, damages.",
             "reads": [
                 {"label": "United States v. Carroll Towing Co., 159 F.2d 169 (2d Cir. 1947)", "url": cl("United States v. Carroll Towing"), "do": "Learn the Hand formula (B < P x L) as the test for breach."},
                 {"label": "Palsgraf v. Long Island Railroad", "url": cl("Palsgraf v. Long Island Railroad"), "do": "Read Cardozo's majority: duty runs only to foreseeable plaintiffs (limits proximate cause)."},
             ],
             "connect": "Carroll Towing gives you 'breach'; Palsgraf bounds 'duty' and 'proximate cause.' With damages, those are the four elements you will spot in every negligence fact pattern."},
            {"topic": "Causation, defenses, and synthesis writing.",
             "reads": [
                 {"label": "Palsgraf (re-read the dissent)", "url": cl("Palsgraf v. Long Island Railroad"), "do": "Read Andrews' dissent on proximate cause, then write the four-element negligence checklist from memory."},
             ],
             "connect": "You now have a whole lawsuit: jurisdiction -> pleading -> discovery/SJ, plus the tort theories litigated inside it. The review day turns this into charts."},
        ],
        "build": ["Chart: subject-matter vs personal jurisdiction.", "Chart: intentional torts vs negligence.",
                  "Attack outline: complaint -> summary judgment.", "Negligence checklist with elements and defenses."],
        "writing": ["A plaintiff files in federal court: explain the court-power and pleading questions before the case can move.",
                    "A negligence hypo involving duty, breach, actual cause, proximate cause, and comparative fault."],
        "exit": "You can state the difference between a court's power over a case and the merits of a claim, the elements of negligence, and why Palsgraf still matters.",
    },
    {
        "num": 2, "year": "1L", "phase": PHASE_ONE, "subject": "Contracts and Property",
        "focus": "Learn exchange and ownership: how promises become enforceable and how law allocates control over things.",
        "source_links": [CB_CONTRACTS, CB_PROPERTY],
        "canon": ["Lucy v. Zehmer (objective assent)", "Hamer v. Sidway (consideration)",
                  "Hawkins v. McGee (expectation damages)", "Pierson v. Post (first possession)",
                  "Jacque v. Steenberg Homes (right to exclude)", "Johnson v. M'Intosh (chain of title)"],
        "days": [
            {"topic": "Offer, acceptance, and objective assent.",
             "reads": [
                 {"label": "Lucy v. Zehmer", "url": cl("Lucy v. Zehmer"), "do": "Read for the objective theory: outward expression controls over secret intent (the 'napkin' land-sale)."},
             ],
             "connect": "Contracts begins where intent meets expression. Hold the objective-theory lens; it explains most formation disputes you will see."},
            {"topic": "Consideration and promissory estoppel.",
             "reads": [
                 {"label": "Hamer v. Sidway", "url": cl("Hamer v. Sidway"), "do": "Read for the rule that forbearance of a legal right is valid consideration (uncle and nephew)."},
             ],
             "connect": "Yesterday asked 'did they agree?'; today asks 'is the promise paid for?' Both must be satisfied before a promise is enforceable."},
            {"topic": "Remedies and defenses overview.",
             "reads": [
                 {"label": "Hawkins v. McGee", "url": cl("Hawkins v. McGee"), "do": "Read for expectation damages = value promised minus value delivered (the 'hairy hand')."},
             ],
             "connect": "Once a contract is formed and supported by consideration, remedies measure the gap. Expectation is the default; keep reliance and restitution as alternatives."},
            {"topic": "Possession and acquisition (property begins).",
             "reads": [
                 {"label": "Pierson v. Post", "url": cl("Pierson v. Post"), "do": "Read for first possession by capture/control, not mere pursuit (the fox)."},
                 {"label": "Jacque v. Steenberg Homes", "url": cl("Jacque v. Steenberg Homes"), "do": "Read for the right to exclude: nominal trespass can support punitive damages."},
             ],
             "connect": "Property is entitlement to things; contracts was promises between people. Pierson defines how ownership starts; Jacque shows what ownership protects."},
            {"topic": "Estates and future interests at a basic level.",
             "reads": [
                 {"label": "Johnson v. M'Intosh, 21 U.S. 543 (1823)", "url": scotus(21, 543), "do": "Read for the origin of title: only the sovereign chain of discovery conveys good title."},
             ],
             "connect": "Estates are slices of ownership across time. M'Intosh shows where the whole chain of title begins before you can carve estates out of it."},
            {"topic": "Landlord-tenant, servitudes, and synthesis writing.",
             "reads": [
                 {"label": "Property map (no new case)", "url": CB_PROPERTY[1], "do": "Skim the casebook's landlord-tenant section, then build your property map and remedies chart."},
             ],
             "connect": "You now hold both halves of private ordering: promises (contracts) and things (property). Review day connects remedies logic across both."},
        ],
        "build": ["Contract formation flowchart.", "Remedies chart: expectation, reliance, restitution.",
                  "Property map: possession, right to exclude, estates, landlord-tenant.", "Property vocabulary glossary."],
        "writing": ["Short contract analysis: is a promise enforceable, and what remedy fits?",
                    "Short property analysis: who has the better entitlement and why?"],
        "exit": "You can explain why not every promise is enforceable, the difference between ownership and possession language, and how remedies shape contract analysis.",
    },
    {
        "num": 3, "year": "1L", "phase": PHASE_ONE, "subject": "Criminal Law Basics",
        "focus": "Learn the architecture of crime: prohibited act, culpable mental state, causation, and defenses.",
        "source_links": [CB_CRIM, G_HARV_JUSTICE],
        "canon": ["Martin v. State (voluntary act)", "Regina v. Cunningham (recklessness)",
                  "People v. Conley (intent)", "State v. Norman (self-defense / imminence)",
                  "MPC mens rea hierarchy"],
        "days": [
            {"topic": "Actus reus and omissions.",
             "reads": [
                 {"label": "Martin v. State", "url": cl("Martin v. State drunk highway"), "do": "Read for the rule that the act must be voluntary: no liability for an involuntary 'act.'"},
             ],
             "connect": "Crime starts with a voluntary act. Tomorrow's mental-state requirement is the second half of the act/intent pairing."},
            {"topic": "Mens rea and mistake.",
             "reads": [
                 {"label": "Regina v. Cunningham", "url": cl("Regina v. Cunningham"), "do": "Read 'maliciously' as recklessness, not wickedness: read the statutory term as defined, not morally."},
                 {"label": "People v. Conley", "url": cl("People v. Conley intent"), "do": "Read for proving intent/knowledge in a specific-intent crime."},
             ],
             "connect": "Actus reus and mens rea must line up in time and target. This pairing is the engine of every offense you analyze."},
            {"topic": "Causation and homicide.",
             "reads": [
                 {"label": "Homicide ladder (casebook)", "url": CB_CRIM[1], "do": "Read the homicide section; map the ladder from murder degrees down to manslaughter by mens rea."},
             ],
             "connect": "Homicide is where act, intent, and causation combine. The 'ladder' is just mens rea sorting the same killing into different grades."},
            {"topic": "Attempt, conspiracy, accomplice liability.",
             "reads": [
                 {"label": "Inchoate offenses (casebook)", "url": CB_CRIM[1], "do": "Read the attempt/conspiracy section; note that liability attaches before harm completes."},
             ],
             "connect": "Inchoate crimes push liability earlier in time; the act/intent framework still governs, just at the planning stage."},
            {"topic": "Justification defenses.",
             "reads": [
                 {"label": "State v. Norman", "url": cl("State v. Norman self defense"), "do": "Read for the imminence requirement: note why the battered-spouse facts failed it."},
             ],
             "connect": "Justifications say the act was right; tomorrow's excuses say the actor was not culpable. Sorting the two is the defense half of criminal analysis."},
            {"topic": "Excuse defenses and synthesis writing.",
             "reads": [
                 {"label": "Insanity and intoxication (casebook)", "url": CB_CRIM[1], "do": "Read the excuse-defenses section; write one homicide and one self-defense answer."},
             ],
             "connect": "You can now break any offense into act -> intent -> causation -> defense. Review day builds the MPC matrix and homicide ladder."},
        ],
        "build": ["Matrix: purpose, knowledge, recklessness, negligence.", "Homicide ladder.",
                  "Defenses chart.", "Common law vs MPC-style framing sheet."],
        "writing": ["Analyze a homicide hypo with disputed mental state.",
                    "Analyze a self-defense hypo with an imperfect factual record."],
        "exit": "You can explain why criminal liability is never just about bad outcomes: it is a required act, a required mental state, and the fit between the two.",
    },
    {
        "num": 4, "year": "1L", "phase": PHASE_ONE, "subject": "Legal Research and Synthesis",
        "focus": "Learn to move between cases, statutes, rules, and secondary sources without getting lost. This is where reading becomes legal workflow.",
        "source_links": [G_HARV_RESEARCH, G_PENN_RESEARCH, G_COL_WRITING],
        "canon": ["Research map", "Statute brief vs case brief", "Case + rule + secondary triangulation"],
        "days": [
            {"topic": "Find and read primary law quickly.",
             "reads": [
                 {"label": "FRCP 12", "url": frcp(12), "do": "Land on the exact text of one FRCP provision; time yourself getting here from a cold search."},
                 {"label": "FRE 802", "url": fre(802), "do": "Do the same for one Federal Rule of Evidence; confirm you can reach primary law in under a minute."},
             ],
             "connect": "This week converts reading into workflow. Start by proving you can reach primary law fast, on demand."},
            {"topic": "Use secondary sources to orient.",
             "reads": [
                 {"label": "Harvard Legal Research Strategy", "url": "https://guides.library.harvard.edu/law/researchstrategy", "do": "Read the 'secondary sources / getting started' guidance; start your personal research map of go-to sources."},
             ],
             "connect": "Secondary sources are scaffolding: they orient you before you commit time to primary law."},
            {"topic": "Brief a statute separately from a case.",
             "reads": [
                 {"label": "templates/statute-brief-template.md and case-brief-template.md", "url": "https://github.com/mktcowboy/law-school-speedrun-jd/tree/main/templates", "do": "Open both templates in your repo's templates/ folder; complete one statute brief and one case brief on a Week 1-3 topic."},
             ],
             "connect": "A statute brief and a case brief are different instruments. Knowing which to use is half of legal reading."},
            {"topic": "Trace one doctrine across sources.",
             "reads": [
                 {"label": "One case + one rule + one secondary source", "url": cl("Palsgraf v. Long Island Railroad"), "do": "Pick a Week 1-3 topic; gather one case (Cornell/CourtListener), one rule/statute (Cornell), and one secondary explanation."},
             ],
             "connect": "This is the core research move: triangulate a doctrine across case + code + commentary until they agree."},
            {"topic": "Citation basics.",
             "reads": [
                 {"label": "Indigo Book", "url": "https://indigobook.github.io/", "do": "Build a one-page citation cheat sheet for cases, statutes, and rules."},
             ],
             "connect": "Citation is how you prove the chain you traced yesterday so a reader can verify it."},
            {"topic": "Write the mini research memo.",
             "reads": [
                 {"label": "500-800 word memo", "url": "https://www.law.columbia.edu/academics/experiential/legal-writing/writing-center/legal-writing-resources", "do": "Answer a Week 1-3 question using at least one case, one rule/statute, and one secondary source."},
             ],
             "connect": "The memo proves the whole workflow. You will reuse this format in every later writing assignment."},
        ],
        "build": ["Personal research map of go-to sources.", "Citation cheat sheet.",
                  "Three completed templates from the templates/ folder."],
        "writing": ["A 500-800 word mini memo answering a Week 1-3 question with one case, one rule/statute, and one secondary source."],
        "exit": "You can answer: where do I start, what source controls, and how do I prove it?",
    },
    {
        "num": 5, "year": "1L", "phase": PHASE_TWO, "subject": "Constitutional Law and Individual Rights",
        "focus": "Shift into constitutional structure and rights analysis: speech, religion, equal protection, and due process.",
        "source_links": [G_YALE_AVALON, G_YALE_AMAR, G_COL_GFOE],
        "canon": ["Marbury (judicial review)", "NYT v. Sullivan / Tinker (speech)",
                  "Emp. Div. v. Smith (free exercise)", "Brown (equal protection)", "Levels of scrutiny"],
        "days": [
            {"topic": "Structure, judicial review, and state action.",
             "reads": [
                 {"label": "Marbury v. Madison, 5 U.S. 137 (1803)", "url": scotus(5, 137), "do": "Read for judicial review: 'it is emphatically the province and duty of the judicial department to say what the law is.'"},
             ],
             "connect": "Marbury is the foundation: it gives courts the power to enforce every right that follows this week."},
            {"topic": "Freedom of speech.",
             "reads": [
                 {"label": "First Amendment (text)", "url": const("first_amendment"), "do": "Read the text; note speech, press, assembly, religion all live in one clause."},
                 {"label": "New York Times Co. v. Sullivan, 376 U.S. 254 (1964)", "url": scotus(376, 254), "do": "Extract the 'actual malice' standard for public-official defamation."},
                 {"label": "Tinker v. Des Moines, 393 U.S. 503 (1969)", "url": scotus(393, 503), "do": "Read for the rule that student speech is protected absent material disruption."},
             ],
             "connect": "Speech doctrine layers tests on one clause. Watch how the intensity of scrutiny tracks the kind of restriction."},
            {"topic": "The religion clauses.",
             "reads": [
                 {"label": "Employment Division v. Smith, 494 U.S. 872 (1990)", "url": scotus(494, 872), "do": "Read for the rule that neutral, generally applicable laws survive free-exercise challenge."},
             ],
             "connect": "Religion splits into Free Exercise and Establishment. Smith sets the modern Free Exercise baseline you build everything else against."},
            {"topic": "Equal protection.",
             "reads": [
                 {"label": "Fourteenth Amendment, Section 1", "url": const("amendmentxiv"), "do": "Read Section 1; locate the Equal Protection and Due Process Clauses."},
                 {"label": "Brown v. Board of Education, 347 U.S. 483 (1954)", "url": scotus(347, 483), "do": "Read for 'separate is inherently unequal,' the engine of modern equal-protection analysis."},
             ],
             "connect": "EP analysis is: classification -> level of scrutiny -> fit. Brown shows scrutiny applied to race."},
            {"topic": "Due process.",
             "reads": [
                 {"label": "Fifth Amendment (text)", "url": const("fifth_amendment"), "do": "Read the Due Process Clause; pair it with the Fourteenth Amendment's clause from yesterday."},
             ],
             "connect": "Procedural vs substantive due process share text but ask different questions. They often travel with equal protection."},
            {"topic": "Mixed constitutional writing.",
             "reads": [
                 {"label": "Scrutiny issue-spotter (no new case)", "url": "https://constitution.congress.gov/", "do": "Write one First Amendment spotter and one EP/DP answer using the correct scrutiny framework."},
             ],
             "connect": "Every rights question reduces to: find the clause -> pick the scrutiny -> apply the fit. Review day builds the scrutiny chart."},
        ],
        "build": ["Levels-of-scrutiny chart.", "Speech-analysis checklist.",
                  "Equal-protection checklist.", "Due-process checklist."],
        "writing": ["One short First Amendment issue spotter.",
                    "One equal-protection or due-process answer using the correct level of scrutiny."],
        "exit": "You can identify the right constitutional framework before talking about who should win.",
    },
    {
        "num": 6, "year": "2L", "phase": PHASE_TWO, "subject": "Criminal Procedure",
        "focus": "Study the constitutional limits on policing and prosecution.",
        "source_links": [CB_CRIMPRO, G_STAN_SCOTUS],
        "canon": ["Katz (expectation of privacy)", "Terry (stop and frisk)", "Mapp (exclusionary rule)",
                  "Miranda (warnings)", "Gideon (right to counsel)"],
        "days": [
            {"topic": "What counts as a search or seizure.",
             "reads": [
                 {"label": "Fourth Amendment (text)", "url": const("fourth_amendment"), "do": "Read the text; note the two clauses (reasonableness and warrants)."},
                 {"label": "Katz v. United States, 389 U.S. 347 (1967)", "url": scotus(389, 347), "do": "Read for the 'reasonable expectation of privacy' test that replaced the trespass doctrine."},
             ],
             "connect": "Criminal procedure is constitutional law applied to police. Katz defines when the Fourth Amendment even switches on."},
            {"topic": "Warrants and probable cause.",
             "reads": [
                 {"label": "Fourth Amendment, Warrant Clause", "url": const("fourth_amendment"), "do": "Re-read the warrant clause: probable cause plus particularity. This is the default rule before exceptions."},
             ],
             "connect": "Once Katz says it is a search, the default is: get a warrant on probable cause. Tomorrow's exceptions explain when you need not."},
            {"topic": "Exceptions and the exclusionary rule.",
             "reads": [
                 {"label": "Terry v. Ohio, 392 U.S. 1 (1968)", "url": scotus(392, 1), "do": "Read for stop-and-frisk on reasonable suspicion, the biggest exception to the warrant rule."},
                 {"label": "Mapp v. Ohio, 367 U.S. 643 (1961)", "url": scotus(367, 643), "do": "Read for the exclusionary rule applied to the states, the remedy that makes the Fourth Amendment bite."},
             ],
             "connect": "Terry loosens the warrant requirement; Mapp supplies the consequence for violating it. Exceptions plus remedy define real-world search law."},
            {"topic": "Custodial interrogation and Miranda.",
             "reads": [
                 {"label": "Fifth Amendment (text)", "url": const("fifth_amendment"), "do": "Read the self-incrimination clause."},
                 {"label": "Miranda v. Arizona, 384 U.S. 436 (1966)", "url": scotus(384, 436), "do": "Read for the warnings required before custodial interrogation."},
             ],
             "connect": "Shift from searches (Fourth) to statements (Fifth). Miranda is the prophylactic rule that protects the privilege."},
            {"topic": "Charging, counsel, and prosecution-stage rights.",
             "reads": [
                 {"label": "Gideon v. Wainwright, 372 U.S. 335 (1963)", "url": scotus(372, 335), "do": "Read for the Sixth Amendment right to appointed counsel in state felony cases."},
             ],
             "connect": "The right to counsel completes the arc from street stop to courtroom."},
            {"topic": "Synthesis writing.",
             "reads": [
                 {"label": "Two issue spotters (no new case)", "url": CB_CRIMPRO[1], "do": "Write one search-and-seizure spotter and one interrogation/right-to-counsel spotter."},
             ],
             "connect": "You now track state power from suspicion -> search -> arrest -> interrogation -> counsel. Review day builds the Fourth Amendment trigger chart and Miranda checklist."},
        ],
        "build": ["Fourth Amendment trigger chart.", "Warrant-exception sheet.",
                  "Miranda checklist.", "Right-to-counsel timeline."],
        "writing": ["One search-and-seizure issue spotter.", "One interrogation/right-to-counsel issue spotter."],
        "exit": "You can explain how the Constitution regulates state power before trial.",
    },
    {
        "num": 7, "year": "2L", "phase": PHASE_TWO, "subject": "Business Associations and Corporations",
        "focus": "Learn the forms through which people organize business activity and the fiduciary duties that govern them.",
        "source_links": [CB_BIZ, G_COL_BLUESKY, G_DUKE_BA],
        "canon": ["Meinhard v. Salmon (loyalty)", "Walkovszky v. Carlton (veil piercing)",
                  "Smith v. Van Gorkom (care)", "Business judgment rule"],
        "days": [
            {"topic": "Agency and authority.",
             "reads": [
                 {"label": "Agency basics (casebook)", "url": CB_BIZ[1], "do": "Read the agency section; distinguish actual, apparent, and inherent authority and when the principal is bound."},
             ],
             "connect": "Agency is the atom of business law: everything an entity does, it does through agents."},
            {"topic": "Partnerships and LLCs.",
             "reads": [
                 {"label": "Meinhard v. Salmon", "url": cl("Meinhard v. Salmon"), "do": "Read for the partner's fiduciary duty: the 'punctilio of an honor the most sensitive.'"},
             ],
             "connect": "Partnerships add fiduciary duty on top of agency. Meinhard's loyalty standard echoes up into corporate law."},
            {"topic": "Corporation structure and limited liability.",
             "reads": [
                 {"label": "Walkovszky v. Carlton", "url": cl("Walkovszky v. Carlton"), "do": "Read for limited liability and when courts will pierce the corporate veil (the taxicab case)."},
                 {"label": "Delaware Code, Title 8, §§ 101-102", "url": "https://delcode.delaware.gov/title8/c001/", "do": "Skim how a corporation is formed and what the certificate must contain."},
             ],
             "connect": "The corporation's signature feature is limited liability; Walkovszky marks its outer limit."},
            {"topic": "Fiduciary duties.",
             "reads": [
                 {"label": "Smith v. Van Gorkom", "url": cl("Smith v. Van Gorkom"), "do": "Read for the duty of care: directors must inform themselves; gross negligence breaches care."},
             ],
             "connect": "Loyalty (Meinhard) plus care (Van Gorkom) are the two fiduciary duties. Tomorrow's business judgment rule shields care claims."},
            {"topic": "Shareholder litigation and governance.",
             "reads": [
                 {"label": "Business judgment rule (casebook)", "url": CB_BIZ[1], "do": "Read the BJR section and the derivative-vs-direct distinction; note what rebuts the presumption."},
             ],
             "connect": "The BJR presumes directors acted properly; Van Gorkom shows what defeats it. This is the litigation frame for governance."},
            {"topic": "Synthesis writing.",
             "reads": [
                 {"label": "Entity + fiduciary problems (no new case)", "url": CB_BIZ[1], "do": "Compare entity forms for three scenarios; analyze one loyalty-or-care problem."},
             ],
             "connect": "You can now form an entity, allocate authority, and trace duty inside it. Review day builds the entity-choice and authority charts."},
        ],
        "build": ["Entity-choice chart.", "Authority chart: actual, apparent, inherent.",
                  "Fiduciary-duty checklist.", "Business-judgment-rule outline."],
        "writing": ["Compare which entity form fits three business scenarios.",
                    "Analyze one fiduciary-duty problem involving loyalty or care."],
        "exit": "You can explain not just how businesses are formed, but how legal duty travels inside them.",
    },
    {
        "num": 8, "year": "2L", "phase": PHASE_TWO, "subject": "UCC Sales and Secured Transactions",
        "focus": "Move from common-law contracts into code-based commercial law: extract rules straight from statutory text.",
        "source_links": [G_DUKE_UCC, G_PENN_STATUTES, G_HARV_STATUTES],
        "canon": ["UCC 2-102/2-104 (scope, merchant)", "UCC 2-207 (battle of forms)",
                  "UCC 2-313/314/315 (warranties)", "Article 9: attachment -> perfection -> priority"],
        "days": [
            {"topic": "How to read the UCC: scope and merchants.",
             "reads": [
                 {"label": "UCC 2-102", "url": ucc(2, "2-102"), "do": "Read the scope: Article 2 governs transactions in goods (not services or land)."},
                 {"label": "UCC 2-104", "url": ucc(2, "2-104"), "do": "Read the definition of 'merchant'; many Article 2 rules turn on this status."},
             ],
             "connect": "Code reading is a new posture: rules come from defined terms, not opinions. Scope plus definitions decide everything downstream."},
            {"topic": "Formation and the battle of the forms.",
             "reads": [
                 {"label": "UCC 2-207", "url": ucc(2, "2-207"), "do": "Read all three subsections; see how it displaces the common-law mirror-image rule."},
             ],
             "connect": "Contrast Week 2's common-law formation: 2-207 lets a contract form despite differing terms. That is the whole point of code-based commercial law."},
            {"topic": "Warranties and remedies.",
             "reads": [
                 {"label": "UCC 2-313", "url": ucc(2, "2-313"), "do": "Read express warranties: how seller statements become promises."},
                 {"label": "UCC 2-314", "url": ucc(2, "2-314"), "do": "Read the implied warranty of merchantability (arises automatically for merchants)."},
                 {"label": "UCC 2-315", "url": ucc(2, "2-315"), "do": "Read the implied warranty of fitness for a particular purpose."},
             ],
             "connect": "Warranties are promises the code reads into a sale. Note which arise automatically vs by the seller's conduct."},
            {"topic": "Secured transactions: attachment.",
             "reads": [
                 {"label": "UCC 9-203", "url": ucc(9, "9-203"), "do": "Read attachment: when a security interest becomes enforceable against the debtor."},
             ],
             "connect": "Shift to Article 9. Attachment is step one of the secured-creditor ladder you finish tomorrow."},
            {"topic": "Perfection and priority.",
             "reads": [
                 {"label": "UCC 9-310", "url": ucc(9, "9-310"), "do": "Read the general rule that a financing statement must be filed to perfect."},
                 {"label": "UCC 9-322", "url": ucc(9, "9-322"), "do": "Read first-to-file-or-perfect priority: who wins among competing secured creditors."},
             ],
             "connect": "Attachment -> perfection -> priority is the ladder. Priority decides who collects when a debtor defaults, the practical payoff of the whole article."},
            {"topic": "Mixed code-reading and writing.",
             "reads": [
                 {"label": "Two issue spotters (no new section)", "url": "https://www.law.cornell.edu/ucc", "do": "Write one UCC sales spotter and one secured-transactions priority spotter."},
             ],
             "connect": "You can now extract rules straight from statutory text. Review day builds the scope chart and the attachment->perfection->priority ladder."},
        ],
        "build": ["Article 2 scope chart.", "Battle-of-the-forms checklist.",
                  "Warranties chart.", "Secured-transactions ladder: attachment -> perfection -> priority."],
        "writing": ["One UCC sales issue spotter.", "One secured-transactions priority issue spotter."],
        "exit": "You can move through a statute in order and explain how definitions, scope, and priority rules interact.",
    },
    {
        "num": 9, "year": "2L", "phase": PHASE_THREE, "subject": "Evidence and Trial",
        "focus": "Learn what information can come into court and why.",
        "source_links": [CB_EVID, G_DUKE_RULES],
        "canon": ["FRE 401-403 (relevance, balancing)", "FRE 404 (character)",
                  "FRE 801-802 (hearsay)", "FRE 803-804 (exceptions)"],
        "days": [
            {"topic": "Relevance and Rule 403 balancing.",
             "reads": [
                 {"label": "FRE 401", "url": fre(401), "do": "Read the definition of relevance: any tendency to make a fact more or less probable."},
                 {"label": "FRE 402", "url": fre(402), "do": "Read the default: relevant evidence is admissible unless something excludes it."},
                 {"label": "FRE 403", "url": fre(403), "do": "Read the judge's override: exclude when probative value is substantially outweighed by unfair prejudice."},
             ],
             "connect": "Relevance is the threshold every exhibit must clear; 403 is the judge's override. Everything else this week is exceptions to these two."},
            {"topic": "Character, conduct, and impeachment.",
             "reads": [
                 {"label": "FRE 404", "url": fre(404), "do": "Read the propensity bar and its exceptions, including 404(b) other-acts evidence."},
             ],
             "connect": "Character evidence is presumptively barred because it is persuasive in the wrong way, a specialized 403 judgment baked into a rule."},
            {"topic": "Hearsay: definition and non-hearsay.",
             "reads": [
                 {"label": "FRE 801", "url": fre(801), "do": "Read the definition and the statements defined as 'not hearsay'; this is the hardest and most-tested rule."},
                 {"label": "FRE 802", "url": fre(802), "do": "Read the rule against hearsay itself."},
             ],
             "connect": "Nail the hearsay definition first. Tomorrow's exceptions only matter once a statement actually IS hearsay."},
            {"topic": "Exclusions and exceptions.",
             "reads": [
                 {"label": "FRE 803", "url": fre(803), "do": "Read the exceptions that apply whether or not the declarant is available."},
                 {"label": "FRE 804", "url": fre(804), "do": "Read the exceptions that require the declarant to be unavailable."},
             ],
             "connect": "803 vs 804 split on whether the declarant's availability matters. That split is your first sort when an exception is needed."},
            {"topic": "Confrontation and trial application.",
             "reads": [
                 {"label": "Sixth Amendment Confrontation Clause + apply the rules", "url": const("sixth_amendment"), "do": "Read the clause, then run the hearsay rules across a short witness narrative."},
             ],
             "connect": "In criminal cases the Constitution adds a layer on top of the hearsay rules. Note where they overlap and where they diverge."},
            {"topic": "Objection drills and writing.",
             "reads": [
                 {"label": "Admissibility checklist (no new rule)", "url": CB_EVID[1], "do": "Run your admissibility checklist on a fact pattern; write one full-sentence hearsay analysis."},
             ],
             "connect": "Evidence is applied procedure: relevance -> character -> hearsay -> constitutional overlay. Review day builds the hearsay flowchart."},
        ],
        "build": ["Admissibility checklist.", "Hearsay flowchart.",
                  "Chart: 404, impeachment, habit vs character.", "Mini trial notebook of objections and responses."],
        "writing": ["Take a witness narrative and list every admissibility fight.",
                    "Write one hearsay analysis in full sentences, not just labels."],
        "exit": "You can answer not only whether a fact matters, but whether the jury is allowed to hear it.",
    },
    {
        "num": 10, "year": "2L", "phase": PHASE_THREE, "subject": "Administrative Law",
        "focus": "Study the administrative state: agencies, delegation, rulemaking, adjudication, and judicial review.",
        "source_links": [CB_ADMIN, G_PENN_REGREV, G_DUKE_ADMIN],
        "canon": ["APA 553 (rulemaking)", "APA 554 (adjudication)", "APA 706 (review)",
                  "Chevron (historical)", "Skidmore (persuasion)"],
        "days": [
            {"topic": "Agency structure and delegation.",
             "reads": [
                 {"label": "Delegation background (casebook)", "url": CB_ADMIN[1], "do": "Read the nondelegation/structure section; note where an agency's power comes from (an enabling statute)."},
             ],
             "connect": "Administrative law is structural constitutional law for the fourth branch. Start with the source of agency power."},
            {"topic": "Rulemaking.",
             "reads": [
                 {"label": "APA 553 (5 U.S.C. 553)", "url": usc(5, 553), "do": "Read notice-and-comment rulemaking: notice, comment, then a final rule with a statement of basis."},
             ],
             "connect": "Rulemaking is how agencies make law that looks like a statute. Section 553 is the procedure that legitimizes it."},
            {"topic": "Adjudication and procedure.",
             "reads": [
                 {"label": "APA 554 (5 U.S.C. 554)", "url": usc(5, 554), "do": "Read formal adjudication; contrast it with rulemaking as the other way agencies make law."},
             ],
             "connect": "Adjudication is how agencies make law that looks like a court judgment. Rulemaking vs adjudication is the core dichotomy."},
            {"topic": "Judicial review.",
             "reads": [
                 {"label": "APA 706 (5 U.S.C. 706)", "url": usc(5, 706), "do": "Read the scope of review, including the 'arbitrary and capricious' standard."},
             ],
             "connect": "Section 706 is where courts re-enter. Arbitrary-and-capricious is the workhorse standard for reviewing agency action."},
            {"topic": "Deference doctrines and the current landscape.",
             "reads": [
                 {"label": "Chevron U.S.A. v. NRDC, 467 U.S. 837 (1984)", "url": scotus(467, 837), "do": "Read the two-step framework as historical background; know it even as the doctrine shifts."},
                 {"label": "Skidmore v. Swift & Co., 323 U.S. 134 (1944)", "url": scotus(323, 134), "do": "Read for deference by 'power to persuade' rather than by command."},
             ],
             "connect": "Deference allocates interpretive authority between court and agency. Chevron and Skidmore are the two poles."},
            {"topic": "Synthesis writing.",
             "reads": [
                 {"label": "Statute -> regulation trace (no new source)", "url": "https://www.federalregister.gov/", "do": "Explain how a statute becomes a binding regulation; analyze a simple agency-review problem."},
             ],
             "connect": "You can now map statute -> agency -> rule/adjudication -> judicial review. Review day builds that map and the standards-of-review chart."},
        ],
        "build": ["Map: statute -> agency -> regulation -> adjudication -> judicial review.", "APA terminology sheet.",
                  "Standards-of-review chart.", "Agency-action checklist."],
        "writing": ["Explain how a federal statute can turn into a binding regulation.", "Analyze a simple agency-review problem."],
        "exit": "You can explain how the legal system governs the people who govern.",
    },
    {
        "num": 11, "year": "2L", "phase": PHASE_THREE, "subject": "Professional Responsibility and Ethics",
        "focus": "Study the duties that govern lawyers themselves.",
        "source_links": [CB_PR, G_DUKE_ETHICS],
        "canon": ["Rule 1.1 (competence)", "Rule 1.6 (confidentiality)", "Rules 1.7/1.9 (conflicts)",
                  "Rule 3.3 (candor)", "Rule 4.1 (truthfulness)"],
        "days": [
            {"topic": "Competence, scope, communication, fees.",
             "reads": [
                 {"label": "Model Rule 1.1 (Competence)", "url": ABA_RULES, "do": "From the table of contents, open Rule 1.1; read the rule and its comments on required knowledge and skill."},
             ],
             "connect": "Competence is the baseline duty; every other rule assumes a lawyer capable of the work."},
            {"topic": "Confidentiality and privilege.",
             "reads": [
                 {"label": "Model Rule 1.6 (Confidentiality of Information)", "url": ABA_RULES, "do": "Read (a) and the (b) exceptions; distinguish the ethics duty from the evidentiary privilege."},
             ],
             "connect": "Confidentiality (ethics) is broader than privilege (evidence). Keeping the two straight is a classic exam trap."},
            {"topic": "Conflicts of interest.",
             "reads": [
                 {"label": "Model Rules 1.7 and 1.9", "url": ABA_RULES, "do": "Open Rule 1.7 (current clients) and 1.9 (former clients); note the consent/waiver mechanics."},
             ],
             "connect": "Conflicts are the most-tested PR topic. Current client (1.7) vs former client (1.9) is your first sort."},
            {"topic": "Litigation duties and candor.",
             "reads": [
                 {"label": "Model Rule 3.3 (Candor Toward the Tribunal)", "url": ABA_RULES, "do": "Read 3.3; note that the duty of candor can override the duty of confidentiality."},
             ],
             "connect": "Rule 3.3 is where duties collide: candor to the court can override 1.6. That collision is prime essay material."},
            {"topic": "Duties to third parties and business development.",
             "reads": [
                 {"label": "Model Rule 4.1 (Truthfulness to Others)", "url": ABA_RULES, "do": "Read 4.1 alongside 3.3 to see the in-court vs out-of-court honesty line."},
             ],
             "connect": "Rule 4.1 governs truth to non-clients; with 3.3 it maps the lawyer's honesty duties everywhere."},
            {"topic": "Ethics writing.",
             "reads": [
                 {"label": "Conflict + confidentiality problems (no new rule)", "url": ABA_RULES, "do": "Analyze one conflict problem and one confidentiality/candor collision."},
             ],
             "connect": "PR reduces to: find the rule that governs the lawyer before reasoning about morality. Review day builds the conflicts and confidentiality charts."},
        ],
        "build": ["Confidentiality vs privilege chart.", "Current-client vs former-client conflicts chart.",
                  "Candor/truthfulness checklist.", "Ethics issue-spotting outline."],
        "writing": ["Analyze one conflict problem.", "Analyze one confidentiality/candor problem where duties collide."],
        "exit": "You can identify the rule that governs the lawyer before drifting into gut-feel morality.",
    },
    {
        "num": 12, "year": "3L", "phase": PHASE_THREE, "subject": "Capstone Synthesis and Bar Bridge",
        "focus": "Pull the subjects together and convert doctrinal understanding into exam-usable structure.",
        "source_links": [("NCBE NextGen overview", "https://www.ncbex.org/exams/nextgen"),
                         ("NextGen content scope", "https://www.ncbex.org/exams/nextgen/content-scope")],
        "canon": ["negligence", "personal jurisdiction", "offer/acceptance/consideration", "mens rea",
                  "equal protection", "Miranda", "attachment/perfection/priority", "hearsay", "conflicts"],
        "days": [
            {"topic": "Cross-subject synthesis: torts + evidence.",
             "reads": [
                 {"label": "Palsgraf + FRE 401-403", "url": fre(403), "do": "Re-open Palsgraf (duty) and FRE 401-403; write a hypo where a negligence fact also raises an admissibility fight."},
             ],
             "connect": "Real exams cross subjects. Torts supplies the claim; evidence decides what the jury hears about it."},
            {"topic": "Cross-subject synthesis: contracts + UCC.",
             "reads": [
                 {"label": "Hawkins v. McGee + UCC 2-207/2-313", "url": ucc(2, "2-207"), "do": "Re-open expectation damages and 2-207; write a sale-of-goods hypo mixing common law and the code."},
             ],
             "connect": "The same deal can be governed by common law or the code. Spotting which regime applies is the threshold move."},
            {"topic": "Cross-subject synthesis: con law + criminal procedure.",
             "reads": [
                 {"label": "Katz/Miranda + 4th/5th Amendments", "url": scotus(384, 436), "do": "Re-open Miranda and the Fourth/Fifth Amendments; write a hypo linking a search to a confession."},
             ],
             "connect": "Criminal procedure is constitutional law in action. One fact pattern often triggers both a Fourth and a Fifth Amendment issue."},
            {"topic": "Outline compression I.",
             "reads": [
                 {"label": "Full outline -> attack outline", "url": "https://www.ncbex.org/exams/nextgen/content-scope", "do": "Take three subjects from full outline to attack outline; use the content scope to prioritize."},
             ],
             "connect": "Attack outlines convert understanding into exam speed. Compress the heaviest subjects first."},
            {"topic": "Outline compression II + PR/Civ Pro.",
             "reads": [
                 {"label": "Attack outline -> one-page checklist", "url": "https://www.ncbex.org/exams/nextgen/content-scope", "do": "Compress remaining subjects to one-pagers; write a professional-responsibility + civil-procedure hypo."},
             ],
             "connect": "One-pagers are your closed-book recall targets. PR + Civ Pro is a common cross because both govern how litigation is conducted."},
            {"topic": "Closed-book rule recall.",
             "reads": [
                 {"label": "Recall the nine core rules", "url": "https://www.ncbex.org/exams/nextgen/preparing-nextgen-ube", "do": "From memory: negligence, personal jurisdiction, offer/acceptance/consideration, mens rea, equal protection, Miranda, attachment/perfection/priority, hearsay, conflicts."},
             ],
             "connect": "If you can state these nine cold, you have the spine of the bar-tested core. Review day is your written reflection; the final six days bridge to the exam."},
        ],
        "build": ["One cleaned-up outline per subject.", "One attack outline per subject.",
                  "Several completed mixed-subject issue spotters."],
        "writing": ["A 2-4 page reflection: which subjects feel intuitive, which need mechanical drilling, and what your next 8-12 weeks should prioritize."],
        "exit": "You have outlines, attack outlines, and a clear next step into either NextGen UBE or legacy-jurisdiction prep.",
    },
]

# Days 85-90: bar-bridge consolidation finisher.
BAR_BRIDGE_TAIL = [
    {"subject": "Bar Bridge: Target Jurisdiction",
     "task": "Pick your target jurisdiction and confirm whether it uses the NextGen UBE or the legacy exam. Note its July 2026 status and any transition rules.",
     "reads": [{"label": "NextGen jurisdiction decisions", "url": "https://www.ncbex.org/exams/nextgen-ube/scores-score-portability/nextgen-ube-decisions-jurisdiction", "do": "Find your state and record NextGen vs legacy plus the first administration date."}],
     "connect": "Everything from here is exam-specific. The format you study for depends entirely on this one decision."},
    {"subject": "Bar Bridge: Map Content Scope",
     "task": "Study the NextGen content scope and map each subject from this curriculum onto the exam's tested areas. Flag gaps.",
     "reads": [{"label": "NextGen content scope", "url": "https://www.ncbex.org/exams/nextgen/content-scope", "do": "List every tested area; mark which of your 12 weeks covers it and which gaps remain."}],
     "connect": "Yesterday picked the exam; today maps your 90 days onto it so you know exactly what is left."},
    {"subject": "Bar Bridge: Timed Issue-Spotter",
     "task": "Write one mixed-subject issue spotter under timed exam conditions (45-60 minutes). Self-grade against your attack outlines.",
     "reads": [{"label": "Legacy/NextGen study aids", "url": "https://www.ncbex.org/study-aids/legacy-exam", "do": "Pull one practice prompt; write under time, then score it against your one-pagers."}],
     "connect": "Mapping is theory; a timed write is the first real rep. This exposes which one-pagers are actually exam-ready."},
    {"subject": "Bar Bridge: Rule Recall",
     "task": "Closed-book recall, round 2. Rewrite each core rule statement from memory.",
     "reads": [{"label": "The nine core rules", "url": "https://www.ncbex.org/exams/nextgen/preparing-nextgen-ube", "do": "Write out negligence, personal jurisdiction, offer/acceptance/consideration, mens rea, equal protection, Miranda, attachment/perfection/priority, hearsay, conflicts."}],
     "connect": "The timed write showed gaps; recall closes them. These nine are the spine you will lean on under exam pressure."},
    {"subject": "Bar Bridge: One-Pagers",
     "task": "Compress your two weakest subjects from attack outline to a single one-page checklist each. These become your final review sheets.",
     "reads": [{"label": "Your attack outlines", "url": "https://www.ncbex.org/exams/nextgen/preparing-nextgen-ube", "do": "Reduce each weak subject to one page: elements, tests, and the two or three cases that anchor them."}],
     "connect": "You are converging on a portable review kit: nine recalled rules plus a one-pager per subject."},
    {"subject": "Bar Bridge: Final Reflection",
     "task": "Write a 2-4 page reflection: which subjects feel intuitive, which need mechanical drilling, and the priorities for your next 8-12 weeks.",
     "reads": [{"label": "Plan your next phase", "url": "https://www.ncbex.org/exams/nextgen-ube/scores-score-portability/nextgen-ube-decisions-jurisdiction", "do": "Decide your concrete next step into NextGen or legacy prep and put dates on it."}],
     "connect": "Day 90 closes the loop: you started at personal jurisdiction and end with a dated plan into real bar prep."},
]

TOTAL_DAYS = 90


def build_schedule():
    """Return a list of 90 dicts, one per day (day=1..90)."""
    schedule = []
    day = 0
    for week in WEEKS:
        week_arc = [d["topic"] for d in week["days"]]
        for i, d in enumerate(week["days"], start=1):
            day += 1
            schedule.append({
                "day": day, "phase": week["phase"], "week": week["num"], "subject": week["subject"],
                "year": week["year"], "year_label": YEAR_LABELS[week["year"]],
                "title": f"Week {week['num']} - Day {i}: {week['subject']}",
                "focus": week["focus"], "topic": d["topic"], "reads": d["reads"],
                "connect": d["connect"], "source_links": week["source_links"], "kind": "study",
                "day_in_week": i, "week_arc": week_arc, "exit": week["exit"],
            })
        day += 1
        schedule.append({
            "day": day, "phase": week["phase"], "week": week["num"], "subject": week["subject"],
            "year": week["year"], "year_label": YEAR_LABELS[week["year"]],
            "title": f"Week {week['num']} - Day 7: Review & Build ({week['subject']})",
            "focus": week["focus"],
            "topic": "Catch up on this week's reading, then build the artifacts and complete the writing assignment.",
            "reads": [], "source_links": week["source_links"], "canon": week["canon"],
            "build": week["build"], "writing": week["writing"], "exit": week["exit"],
            "connect": f"Lock in {week['subject']} before moving on; these artifacts become your review kit.",
            "kind": "review",
        })
    for entry in BAR_BRIDGE_TAIL:
        day += 1
        schedule.append({
            "day": day, "phase": PHASE_THREE, "week": 13, "subject": entry["subject"],
            "year": "3L", "year_label": YEAR_LABELS["3L"],
            "title": f"Day {day}: {entry['subject']}",
            "focus": "Consolidate the full curriculum and bridge into bar preparation.",
            "topic": entry["task"], "reads": entry["reads"], "connect": entry["connect"],
            "source_links": [], "kind": "barbridge",
        })
    return schedule


if __name__ == "__main__":
    sched = build_schedule()
    assert len(sched) == TOTAL_DAYS, f"expected {TOTAL_DAYS} days, got {len(sched)}"
    for d in sched:
        print(f"Day {d['day']:>2} | {d['title']}")
        print(f"        topic: {d['topic']}")
        for r in d["reads"]:
            print(f"        read:  {r['label']}  ->  {r['url']}")
        print(f"        connect: {d['connect']}")
    print(f"\nTotal: {len(sched)} days. OK.")
