# CourtListener Direct Linking Notes

Last updated: 2026-06-30

## Goal

Replace all CourtListener search links for landmark cases with direct case links.

The current search-link pattern is:

```text
https://www.courtlistener.com/?q=...&type=o&order_by=score+desc
```

The preferred target pattern is:

```text
https://www.courtlistener.com/opinion/<id>/<slug>/
```

Do not replace a search link with the first CourtListener search result unless the result is verified as the actual case. Some search results point to citing cases, cert denials, or unrelated opinions.

## Current State

The direct-link rewrite has been applied to the 14 subject/case Markdown files listed below. The original state had 210 CourtListener search-link occurrences across these files.

File counts:

| Count | File |
| ---: | --- |
| 131 | `00-start-here/assessment/landmark-case-canon.md` |
| 6 | `01-1l-foundation-year/civil-procedure/README.md` |
| 17 | `01-1l-foundation-year/constitutional-law/README.md` |
| 4 | `01-1l-foundation-year/contracts/README.md` |
| 3 | `01-1l-foundation-year/criminal-law/README.md` |
| 3 | `01-1l-foundation-year/property/README.md` |
| 4 | `01-1l-foundation-year/torts/README.md` |
| 5 | `02-2l-doctrinal-depth-and-codes/administrative-law/README.md` |
| 3 | `02-2l-doctrinal-depth-and-codes/business-associations/README.md` |
| 10 | `02-2l-doctrinal-depth-and-codes/conflict-of-laws/README.md` |
| 6 | `02-2l-doctrinal-depth-and-codes/criminal-procedure/README.md` |
| 5 | `02-2l-doctrinal-depth-and-codes/evidence/README.md` |
| 5 | `02-2l-doctrinal-depth-and-codes/family-law/README.md` |
| 8 | `02-2l-doctrinal-depth-and-codes/legislation-and-regulation/README.md` |

There were 127 unique decoded case queries behind those 210 occurrences. The resolver cache ended with 127 resolved mappings and 0 unresolved mappings.

## Work Already Done

Two parallel agents audited the problem:

- Franklin found all CourtListener search-link occurrences and confirmed they are concentrated in the 14 files listed above.
- Pauli identified risky case queries where taking the first CourtListener API result is likely unsafe.

The landmark canon intro was updated so it no longer describes the links as CourtListener opinion searches.

Subject guide gotchas Franklin flagged:

- Civil Procedure: `Hanna`
- Constitutional Law: `Gibbons`, `Lopez`, `Youngstown`, `Washington v. Davis`, `Smith`
- Contracts: `Hadley`
- Administrative Law: `Loper Bright`
- Conflict of Laws: `Erie`, `Klaxon`
- Criminal Procedure: `Katz`
- Evidence: `Crawford`
- Legislation and Regulation: `Loper Bright`, `Skidmore`

## Risky Queries

These were manually verified or handled with stronger matching before replacement:

- `Martin v. State`
- `People v. Anderson`
- `People v. Conley`
- `Commonwealth v. Carroll`
- `United States v. Lopez`
- `New York v. United States`
- `Goodyear v. Brown`
- `In re Caremark`
- `Chevron v. NRDC`
- `Vermont Yankee v. NRDC`
- `INS v. Chadha`
- `NFIB v. Sebelius`
- `TVA v. Hill`
- `West Virginia v. EPA`
- `Byrne v. Boadle`
- `Hadley v. Baxendale`
- `M'Naghten's Case`
- `Overseas Tankship v. Morts Dock (The Wagon Mound No. 1)`
- `Raffles v. Wichelhaus`
- `Regina v. Cunningham`
- `Regina v. Dudley and Stephens`

Older English cases and broad state-law names were especially risky. Where CourtListener did not host the original opinion, the rewrite uses a direct external case page rather than linking to an unrelated citing opinion.

## Resolver Notes

CourtListener API lookup works through `curl`:

```bash
curl -L -s -A 'Mozilla/5.0' 'https://www.courtlistener.com/api/rest/v4/search/?q=Lucy%20v.%20Zehmer&type=o&order_by=score%20desc'
```

Ruby `Net::HTTP` failed DNS in the sandbox. Use `curl -L` for API fetching unless the environment changes.

Do not use normal browser search-page fetches as the API source. Fetching `https://www.courtlistener.com/?q=...` returned CloudFront 403 during testing.

Known good examples:

- `Lucy v. Zehmer` -> `https://www.courtlistener.com/opinion/1305339/lucy-v-zehmer/`
- `Bell Atlantic v. Twombly` should resolve through a better query variant such as `Bell Atlantic Corp. v. Twombly` -> `https://www.courtlistener.com/opinion/145730/bell-atlantic-corp-v-twombly/`

Known bad attempt:

- A naive first-result resolver mis-resolved `Bell Atlantic v. Twombly` to `Lane v. Page`.

Resolver outcome:

- `00-start-here/maintenance/tools/courtlistener_direct_link_resolver.rb` now contains the repeatable resolver and manual canonical overrides.
- The resolver cache at `/tmp/courtlistener-direct-link-cache.json` ended with 127 resolved mappings and 0 unresolved mappings.
- The bad naive cache `/tmp/courtlistener-direct-map.json` was deleted earlier because it came from an unsafe first-result resolver.
- The old partial cache `/tmp/courtlistener-strict-map.json` should not be trusted.

## Rewrite Checklist Used

1. Extract every `https://www.courtlistener.com/?q=...` URL from Markdown files.
2. Decode the query and strip surrounding quote characters.
3. Generate query variants for abbreviated names and official reporter names.
4. Query the CourtListener search API with `curl -L -s -A 'Mozilla/5.0'`.
5. Accept a result only when `caseName` or `caseNameFull` actually matches the target case.
6. Reject citing cases, cert denials, law-review references, and loose keyword hits.
7. For risky or old non-US cases, use a manual mapping or a different free direct source if CourtListener does not host the original opinion.
8. Rewrite only accepted mappings.
9. Update the landmark canon intro so it no longer says the links are search links.
10. Verify no subject/case pages retain CourtListener search links.

## Verification Commands

Count remaining CourtListener search links:

```bash
ruby -r uri -e 'urls=[]; Dir.glob("**/*.md").each { |f| File.read(f).scan(%r{https://www\.courtlistener\.com/\?[^)\s]+}) { |u| urls << [f,u] } }; puts "search_url_occurrences=#{urls.size}"; puts "files=#{urls.map(&:first).uniq.size}"'
```

List files with remaining search links:

```bash
ruby -r uri -e 'counts=Hash.new(0); Dir.glob("**/*.md").each { |f| File.read(f).scan(%r{https://www\.courtlistener\.com/\?[^)\s]+}) { counts[f] += 1 } }; counts.sort.each { |f,n| puts "#{n}\t#{f}" }'
```

After rewrite, useful checks:

```bash
rg 'https://www\.courtlistener\.com/\?q=' -g '*.md' -g '!00-start-here/maintenance/courtlistener-direct-linking-notes.md'
rg -P 'https://www\.courtlistener\.com/(?!opinion/)' -g '*.md' -g '!00-start-here/maintenance/courtlistener-direct-linking-notes.md'
```

Run the repo's local Markdown link checks after any rewrite if those scripts are still present.
