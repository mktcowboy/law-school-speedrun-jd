#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "open3"
require "set"
require "time"
require "uri"

ROOT = File.expand_path("../../..", __dir__)
CACHE_PATH = ENV.fetch("COURTLISTENER_LINK_CACHE", "/tmp/courtlistener-direct-link-cache.json")
USER_AGENT = "Mozilla/5.0"

IGNORED_FILES = Set.new([
  "00-start-here/maintenance/courtlistener-direct-linking-notes.md"
])

STOPWORDS = Set.new(%w[
  a ag and assn association co company corp corporation ct dept department dist division d
  elec electric enterprises for inc incorporated llc ltd no of r rr sa school the transp u usa
  us v vs
])

MANUAL_QUERY_VARIANTS = {
  "Bell Atlantic v. Twombly" => [
    "Bell Atlantic Corp. v. Twombly",
    "Bell Atlantic Corporation v. Twombly"
  ],
  "Goodyear v. Brown" => [
    "Goodyear Dunlop Tires Operations, S.A. v. Brown"
  ],
  "Chevron v. NRDC" => [
    "Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc."
  ],
  "Vermont Yankee v. NRDC" => [
    "Vermont Yankee Nuclear Power Corp. v. Natural Resources Defense Council"
  ],
  "INS v. Chadha" => [
    "Immigration and Naturalization Service v. Chadha"
  ],
  "NFIB v. Sebelius" => [
    "National Federation of Independent Business v. Sebelius"
  ],
  "TVA v. Hill" => [
    "Tennessee Valley Authority v. Hill"
  ],
  "United States v. Carolene Products" => [
    "United States v. Carolene Products Co."
  ],
  "New York Times v. Sullivan" => [
    "New York Times Co. v. Sullivan"
  ],
  "Employment Division v. Smith" => [
    "Employment Div. v. Smith",
    "Employment Division Department of Human Resources of Oregon v. Smith"
  ],
  "United States v. Carroll Towing" => [
    "United States v. Carroll Towing Co."
  ],
  "Palsgraf v. Long Island R.R." => [
    "Palsgraf v. Long Island Railroad Co."
  ],
  "MacPherson v. Buick" => [
    "MacPherson v. Buick Motor Co."
  ],
  "Tarasoff v. Regents" => [
    "Tarasoff v. Regents of University of California"
  ],
  "Wood v. Lucy, Lady Duff-Gordon" => [
    "Wood v. Lucy Lady Duff-Gordon"
  ],
  "Pennsylvania Coal v. Mahon" => [
    "Pennsylvania Coal Co. v. Mahon"
  ],
  "Motor Vehicle Mfrs. Assn. v. State Farm" => [
    "Motor Vehicle Manufacturers Association v. State Farm Mutual Automobile Insurance Co."
  ],
  "Revlon v. MacAndrews & Forbes" => [
    "Revlon, Inc. v. MacAndrews & Forbes Holdings, Inc."
  ],
  "In re Caremark" => [
    "In re Caremark International Inc. Derivative Litigation"
  ],
  "Overseas Tankship v. Morts Dock (The Wagon Mound No. 1)" => [
    "Overseas Tankship (U.K.) Ltd. v. Morts Dock & Engineering Co.",
    "The Wagon Mound No. 1"
  ],
  "M'Naghten's Case" => [
    "M'Naghten's Case",
    "Regina v. M'Naghten"
  ],
  "Regina v. Dudley and Stephens" => [
    "Regina v. Dudley and Stephens",
    "R v. Dudley and Stephens"
  ],
  "Regina v. Cunningham" => [
    "Regina v. Cunningham",
    "R v. Cunningham"
  ]
}.freeze

MANUAL_RESOLUTIONS = {
  "Martin v. State" => {
    "direct_url" => "https://www.courtlistener.com/opinion/3233100/martin-v-state/",
    "caseName" => "Martin v. State",
    "citation" => ["17 So. 2d 427", "31 Ala. App. 334"],
    "court" => "Court of Appeals of Alabama"
  },
  "People v. Anderson" => {
    "direct_url" => "https://www.courtlistener.com/opinion/1312544/people-v-anderson/",
    "caseName" => "People v. Anderson",
    "citation" => ["447 P.2d 942", "70 Cal. 2d 15"],
    "court" => "Supreme Court of California"
  },
  "People v. Conley" => {
    "direct_url" => "https://www.courtlistener.com/opinion/2097961/people-v-conley/",
    "caseName" => "People v. Conley",
    "citation" => ["543 N.E.2d 138", "187 Ill. App. 3d 234"],
    "court" => "Illinois Appellate Court"
  },
  "Commonwealth v. Carroll" => {
    "direct_url" => "https://www.courtlistener.com/opinion/2302175/commonwealth-v-carroll/",
    "caseName" => "Commonwealth v. Carroll",
    "citation" => ["194 A.2d 911", "412 Pa. 525"],
    "court" => "Supreme Court of Pennsylvania"
  },
  "United States v. Lopez" => {
    "direct_url" => "https://www.courtlistener.com/opinion/117927/united-states-v-lopez/",
    "caseName" => "United States v. Lopez",
    "citation" => ["514 U.S. 549"],
    "court" => "Supreme Court of the United States"
  },
  "New York v. United States" => {
    "direct_url" => "https://www.courtlistener.com/opinion/112768/new-york-v-united-states/",
    "caseName" => "New York v. United States",
    "citation" => ["505 U.S. 144"],
    "court" => "Supreme Court of the United States"
  },
  "Goodyear v. Brown" => {
    "direct_url" => "https://www.courtlistener.com/opinion/219732/goodyear-dunlop-tires-operations-s-a-v-brown/",
    "caseName" => "Goodyear Dunlop Tires Operations, S.A. v. Brown",
    "citation" => ["564 U.S. 915"],
    "court" => "Supreme Court of the United States"
  },
  "In re Caremark" => {
    "direct_url" => "https://www.courtlistener.com/opinion/1968607/in-re-caremark-international-inc-derivative-litigation/",
    "caseName" => "In Re Caremark International Inc. Derivative Litigation",
    "citation" => ["698 A.2d 959"],
    "court" => "Delaware Court of Chancery"
  },
  "Chevron v. NRDC" => {
    "direct_url" => "https://www.courtlistener.com/opinion/111221/chevron-u-s-a-inc-v-natural-resources-defense-council-inc/",
    "caseName" => "Chevron U.S.A. Inc. v. Natural Resources Defense Council, Inc.",
    "citation" => ["467 U.S. 837"],
    "court" => "Supreme Court of the United States"
  },
  "Vermont Yankee v. NRDC" => {
    "direct_url" => "https://www.courtlistener.com/opinion/109827/vermont-yankee-nuclear-power-corp-v-natural-resources-defense-council/",
    "caseName" => "Vermont Yankee Nuclear Power Corp. v. Natural Resources Defense Council, Inc.",
    "citation" => ["435 U.S. 519"],
    "court" => "Supreme Court of the United States"
  },
  "INS v. Chadha" => {
    "direct_url" => "https://www.courtlistener.com/opinion/110985/immigration-naturalization-service-v-chadha/",
    "caseName" => "Immigration & Naturalization Service v. Chadha",
    "citation" => ["462 U.S. 919"],
    "court" => "Supreme Court of the United States"
  },
  "NFIB v. Sebelius" => {
    "direct_url" => "https://www.courtlistener.com/opinion/809122/national-federation-of-independent-business-v-sebelius/",
    "caseName" => "National Federation of Independent Business v. Sebelius",
    "citation" => ["567 U.S. 519"],
    "court" => "Supreme Court of the United States"
  },
  "TVA v. Hill" => {
    "direct_url" => "https://www.courtlistener.com/opinion/109897/tennessee-valley-authority-v-hill/",
    "caseName" => "Tennessee Valley Authority v. Hill",
    "citation" => ["437 U.S. 153"],
    "court" => "Supreme Court of the United States"
  },
  "West Virginia v. EPA" => {
    "direct_url" => "https://www.courtlistener.com/opinion/6620345/west-virginia-v-epa/",
    "caseName" => "West Virginia v. EPA",
    "citation" => ["597 U.S. 697"],
    "court" => "Supreme Court of the United States"
  },
  "Johnson v. M'Intosh" => {
    "direct_url" => "https://www.courtlistener.com/opinion/85404/johnson-grahams-lessee-v-mcintosh/",
    "caseName" => "Johnson & Graham's Lessee v. McIntosh",
    "citation" => ["21 U.S. 543", "8 Wheat. 543"],
    "court" => "Supreme Court of the United States"
  },
  "Penn Central Transp. Co. v. New York City" => {
    "direct_url" => "https://www.courtlistener.com/opinion/109924/penn-central-transportation-co-v-new-york-city/",
    "caseName" => "Penn Central Transportation Co. v. New York City",
    "citation" => ["438 U.S. 104"],
    "court" => "Supreme Court of the United States"
  },
  "Vincent v. Lake Erie Transp. Co." => {
    "direct_url" => "https://www.courtlistener.com/opinion/8019723/vincent-v-lake-erie-transportation-co/",
    "caseName" => "Vincent v. Lake Erie Transportation Co.",
    "citation" => ["109 Minn. 456", "124 N.W. 221"],
    "court" => "Supreme Court of Minnesota"
  }
}.freeze

MANUAL_EXTERNAL_RESOLUTIONS = {
  "Byrne v. Boadle" => {
    "direct_url" => "https://en.wikipedia.org/wiki/Byrne_v_Boadle",
    "caseName" => "Byrne v. Boadle",
    "citation" => ["2 Hurl. & Colt. 722", "159 Eng. Rep. 299"],
    "source" => "Wikipedia case page"
  },
  "Hadley v. Baxendale" => {
    "direct_url" => "https://en.wikipedia.org/wiki/Hadley_v_Baxendale",
    "caseName" => "Hadley v. Baxendale",
    "citation" => ["156 Eng. Rep. 145", "9 Exch. 341"],
    "source" => "Wikipedia case page"
  },
  "M'Naghten's Case" => {
    "direct_url" => "https://en.wikipedia.org/wiki/M%27Naghten_rules",
    "caseName" => "M'Naghten's Case",
    "citation" => ["10 Cl. & Fin. 200", "8 Eng. Rep. 718"],
    "source" => "Wikipedia case page"
  },
  "Overseas Tankship v. Morts Dock (The Wagon Mound No. 1)" => {
    "direct_url" => "https://en.wikipedia.org/wiki/Overseas_Tankship_(UK)_Ltd_v_Morts_Dock_and_Engineering_Co_Ltd",
    "caseName" => "Overseas Tankship (UK) Ltd v Morts Dock and Engineering Co Ltd",
    "citation" => ["[1961] UKPC 1", "[1961] AC 388"],
    "source" => "Wikipedia case page"
  },
  "Raffles v. Wichelhaus" => {
    "direct_url" => "https://en.wikipedia.org/wiki/Raffles_v_Wichelhaus",
    "caseName" => "Raffles v. Wichelhaus",
    "citation" => ["2 Hurl. & C. 906", "159 Eng. Rep. 375"],
    "source" => "Wikipedia case page"
  },
  "Regina v. Cunningham" => {
    "direct_url" => "https://en.wikipedia.org/wiki/R_v_Cunningham",
    "caseName" => "R v. Cunningham",
    "citation" => ["[1957] 2 QB 396"],
    "source" => "Wikipedia case page"
  },
  "Regina v. Dudley and Stephens" => {
    "direct_url" => "https://en.wikipedia.org/wiki/R_v_Dudley_and_Stephens",
    "caseName" => "R v. Dudley and Stephens",
    "citation" => ["14 QBD 273"],
    "source" => "Wikipedia case page"
  }
}.freeze

def markdown_files
  Dir.glob(File.join(ROOT, "**/*.md")).sort.map do |path|
    rel = path.delete_prefix("#{ROOT}/")
    next if IGNORED_FILES.include?(rel)

    path
  end.compact
end

def extract_links
  links = []
  markdown_files.each do |path|
    rel = path.delete_prefix("#{ROOT}/")
    File.read(path).scan(%r{https://www\.courtlistener\.com/\?[^)\s]+}) do |url|
      query = URI.decode_www_form(URI.parse(url).query || "").assoc("q")&.last.to_s
      query = query.gsub(/\A"|"\z/, "")
      links << { "file" => rel, "url" => url, "query" => query }
    end
  end
  links
end

def variants_for(query)
  ([query] + MANUAL_QUERY_VARIANTS.fetch(query, [])).uniq
end

def normalize_tokens(text)
  text.downcase
      .gsub("&", " and ")
      .gsub(/[^a-z0-9]+/, " ")
      .split
      .reject { |token| token.length < 2 || STOPWORDS.include?(token) }
end

def important_tokens(text)
  tokens = normalize_tokens(text)
  tokens.reject { |token| token.match?(/\A\d+\z/) }
end

def candidate_text(result)
  [
    result["caseName"],
    result["caseNameFull"],
    Array(result["citation"]).join(" ")
  ].compact.join(" ")
end

def acceptable_match?(query_variant, result)
  target = important_tokens(query_variant)
  candidate = normalize_tokens(candidate_text(result))
  return false if target.empty? || candidate.empty?

  missing = target - candidate
  return true if missing.empty?

  # Allow abbreviated query tokens when the full names are in a manual variant.
  false
end

def search_api(query)
  params = URI.encode_www_form(q: query, type: "o", order_by: "score desc")
  url = "https://www.courtlistener.com/api/rest/v4/search/?#{params}"
  out, err, status = Open3.capture3("curl", "-L", "-s", "-A", USER_AGENT, url)
  raise "curl failed for #{query.inspect}: #{err}" unless status.success?

  JSON.parse(out)
end

def direct_url(result)
  absolute = result.fetch("absolute_url")
  absolute.start_with?("http") ? absolute : "https://www.courtlistener.com#{absolute}"
end

def resolve_query(query)
  if MANUAL_RESOLUTIONS.key?(query) || MANUAL_EXTERNAL_RESOLUTIONS.key?(query)
    manual = MANUAL_RESOLUTIONS.fetch(query, MANUAL_EXTERNAL_RESOLUTIONS[query])
    return manual.merge(
      "status" => "resolved",
      "query" => query,
      "variant" => "manual"
    )
  end

  variants_for(query).each do |variant|
    data = search_api(variant)
    Array(data["results"]).first(20).each do |result|
      next unless acceptable_match?(variant, result)

      return {
        "status" => "resolved",
        "query" => query,
        "variant" => variant,
        "direct_url" => direct_url(result),
        "caseName" => result["caseName"],
        "caseNameFull" => result["caseNameFull"],
        "citation" => result["citation"],
        "court" => result["court"],
        "dateFiled" => result["dateFiled"],
        "score" => result.dig("meta", "score", "bm25")
      }
    end
  rescue JSON::ParserError => e
    return {
      "status" => "error",
      "query" => query,
      "error" => "JSON parse failed for #{variant.inspect}: #{e.message}"
    }
  end

  {
    "status" => "unresolved",
    "query" => query,
    "variants" => variants_for(query)
  }
end

def load_cache
  return { "resolved_at" => nil, "queries" => {} } unless File.exist?(CACHE_PATH)

  JSON.parse(File.read(CACHE_PATH))
end

def save_cache(cache)
  File.write(CACHE_PATH, JSON.pretty_generate(cache))
end

def resolve_all
  links = extract_links
  queries = links.map { |link| link["query"] }.uniq.sort
  cache = load_cache
  cache["queries"] ||= {}

  queries.each_with_index do |query, index|
    if MANUAL_RESOLUTIONS.key?(query) || MANUAL_EXTERNAL_RESOLUTIONS.key?(query)
      warn "[#{index + 1}/#{queries.size}] manual #{query}"
      cache["queries"][query] = resolve_query(query)
      save_cache(cache)
      next
    end

    if cache["queries"][query]&.fetch("status", nil) == "resolved"
      warn "[#{index + 1}/#{queries.size}] cached #{query}"
      next
    end

    warn "[#{index + 1}/#{queries.size}] resolving #{query}"
    cache["queries"][query] = resolve_query(query)
    cache["resolved_at"] = Time.now.utc.iso8601
    save_cache(cache)
    sleep 0.15
  end

  save_cache(cache)
  cache
end

def apply_cache
  cache = load_cache
  resolved = cache.fetch("queries").select { |_query, entry| entry["status"] == "resolved" }
  by_query = resolved.transform_values { |entry| entry.fetch("direct_url") }

  changed = []
  markdown_files.each do |path|
    rel = path.delete_prefix("#{ROOT}/")
    original = File.read(path)
    updated = original.gsub(%r{https://www\.courtlistener\.com/\?[^)\s]+}) do |url|
      query = URI.decode_www_form(URI.parse(url).query || "").assoc("q")&.last.to_s
      query = query.gsub(/\A"|"\z/, "")
      by_query.fetch(query, url)
    end
    next if updated == original

    File.write(path, updated)
    changed << rel
  end

  changed
end

def report(cache)
  entries = cache.fetch("queries")
  resolved = entries.select { |_query, entry| entry["status"] == "resolved" }
  unresolved = entries.reject { |_query, entry| entry["status"] == "resolved" }

  puts "resolved=#{resolved.size}"
  puts "unresolved=#{unresolved.size}"
  unresolved.each do |query, entry|
    puts "#{entry["status"]}\t#{query}\t#{entry["error"]}"
  end
end

mode = ARGV.fetch(0, "resolve")

case mode
when "resolve"
  report(resolve_all)
when "apply"
  puts apply_cache
when "report"
  report(load_cache)
when "extract"
  puts JSON.pretty_generate(extract_links)
when "debug"
  query = ARGV.fetch(1)
  variants_for(query).each do |variant|
    puts "variant=#{variant}"
    data = search_api(variant)
    Array(data["results"]).first(5).each_with_index do |result, index|
      puts [
        index + 1,
        acceptable_match?(variant, result),
        result["caseName"],
        result["caseNameFull"],
        direct_url(result)
      ].join("\t")
    end
  end
else
  abort "usage: #{$PROGRAM_NAME} [resolve|apply|report|extract|debug QUERY]"
end
