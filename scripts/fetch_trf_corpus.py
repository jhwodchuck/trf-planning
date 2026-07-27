#!/usr/bin/env python3
"""
fetch_trf_corpus.py

Systematically fetches content from https://www.texrenfest.com/ pages,
converts them into clean Markdown documents, and places them into docs/trf-corpus/.
Uses ThreadPoolExecutor for fast concurrent fetching.
"""

import html
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Mapping of site pages to corpus categories and file slugs
PAGES = [
    # The Kingdom
    ("the-kingdom", "directions-and-parking", "https://www.texrenfest.com/p/the-kingdom/directions--parking", "Directions & Parking"),
    ("the-kingdom", "festival-map", "https://www.texrenfest.com/p/the-kingdom/festival-map", "Festival Map"),
    ("the-kingdom", "themed-weekends", "https://www.texrenfest.com/p/the-kingdom/themed-weekends", "Themed Weekends"),
    ("the-kingdom", "lockers", "https://www.texrenfest.com/p/the-kingdom/lockers", "Lockers"),
    ("the-kingdom", "accessibility", "https://www.texrenfest.com/p/the-kingdom/accessibility", "Accessibility"),
    ("the-kingdom", "faq", "https://www.texrenfest.com/p/the-kingdom/faq", "Festival FAQ"),
    ("the-kingdom", "lost-and-found", "https://www.texrenfest.com/p/the-kingdom/lost-and-found", "Lost and Found"),
    ("the-kingdom", "contact-us", "https://www.texrenfest.com/p/the-kingdom/contact-us", "Contact Us"),

    # Things to Do
    ("things-to-do", "entertainment-schedule", "https://www.texrenfest.com/p/things-to-do/entertainment-schedule", "Entertainment Schedule"),
    ("things-to-do", "performers", "https://www.texrenfest.com/events/performances", "Performers"),
    ("things-to-do", "for-lords-and-ladies-21", "https://www.texrenfest.com/p/things-to-do/for-lords--ladies-21", "For Lords & Ladies (21+)"),
    ("things-to-do", "for-friends-and-families", "https://www.texrenfest.com/p/things-to-do/for-friends--families", "For Friends & Families"),
    ("things-to-do", "survival-guide", "https://www.texrenfest.com/p/things-to-do/survival-guide-for-newbies", "Survival Guide for Newbies"),
    ("things-to-do", "guided-tours", "https://www.texrenfest.com/p/things-to-do/survival-guide-for-newbies/guided-tours", "Guided Tours"),
    ("things-to-do", "speak-like-a-trf-pro", "https://www.texrenfest.com/p/things-to-do/survival-guide-for-newbies/speak-like-a-trf-pro", "Speak Like a TRF Pro"),
    ("things-to-do", "whats-new", "https://www.texrenfest.com/p/things-to-do/whats-new", "What's New"),

    # Camping & More
    ("camping-and-more", "camping-overview", "https://www.texrenfest.com/p/camping-and-more/camping", "Camping Overview"),
    ("camping-and-more", "campground-map", "https://www.texrenfest.com/p/camping-and-more/camping/campground-map", "Campground Map"),
    ("camping-and-more", "campground-rules-faqs", "https://www.texrenfest.com/p/camping-and-more/campground-rules--faqs", "Campground Rules & FAQs"),
    ("camping-and-more", "camping-passes", "https://www.texrenfest.com/p/camping-and-more/camping-passes", "Camping Passes"),
    ("camping-and-more", "camping-reservations", "https://www.texrenfest.com/p/camping-and-more/camping-reservation", "Camping Reservations"),
    ("camping-and-more", "guilds", "https://www.texrenfest.com/p/camping-and-more/guilds", "Guilds & Land Requests"),
    ("camping-and-more", "lodging", "https://www.texrenfest.com/p/camping-and-more/lodging", "Lodging"),
    ("camping-and-more", "city-of-magnolia", "https://www.texrenfest.com/p/camping-and-more/city-of-magnolia", "The City of Magnolia"),

    # Weddings & Events
    ("weddings-and-events", "weddings-overview", "https://www.texrenfest.com/weddings", "Weddings Overview"),
    ("weddings-and-events", "weddings-trf", "https://www.texrenfest.com/p/weddings-and-events/weddings--trf", "Weddings @ TRF"),
    ("weddings-and-events", "parties-and-events", "https://www.texrenfest.com/p/weddings-and-events/parties--events", "Parties and Events"),
    ("weddings-and-events", "contact-weddings", "https://www.texrenfest.com/p/weddings-and-events/contact-weddings--events", "Contact Weddings & Events"),

    # Shoppes & Food
    ("shoppes-and-food", "shoppes", "https://www.texrenfest.com/businesses/shoppes", "Shoppes Directory"),
    ("shoppes-and-food", "food-and-drink", "https://www.texrenfest.com/businesses/food", "Food & Drink Directory"),

    # Media
    ("media", "media-pass-request", "https://www.texrenfest.com/p/media/media-pass-request", "Media Pass Request"),
    ("media", "press-kit", "https://www.texrenfest.com/p/media/press-kit--releases", "Press Kit & Releases"),
    ("media", "podcast", "https://www.texrenfest.com/p/media/podcast", "Podcast"),
    ("media", "sponsors", "https://www.texrenfest.com/p/media/sponsors", "Sponsors"),

    # Ticket Info
    ("ticket-info", "tickets-overview", "https://www.texrenfest.com/p/tickets", "Tickets Overview"),
    ("ticket-info", "general-ticket-info", "https://www.texrenfest.com/p/ticket-info/general-ticket-info", "General Ticket Info"),
    ("ticket-info", "parking-passes", "https://www.texrenfest.com/p/ticket-info/parking-passes", "Parking Passes"),
    ("ticket-info", "groups", "https://www.texrenfest.com/p/ticket-info/groups", "Group Tickets"),
    ("ticket-info", "donations", "https://www.texrenfest.com/p/ticket-info/donations", "Ticket Donations"),
    ("ticket-info", "liability-waiver", "https://www.texrenfest.com/p/ticket-info/liability-waiver", "Liability Waiver"),

    # Join Us & Policies
    ("join-us-and-policies", "join-us", "https://www.texrenfest.com/p/join-us", "Join Us Overview"),
    ("join-us-and-policies", "trf-careers", "https://www.texrenfest.com/p/join-us/trf-careers", "TRF Careers"),
    ("join-us-and-policies", "vendors", "https://www.texrenfest.com/p/join-us/for-our-vendors", "For Our Vendors / Participants"),
    ("join-us-and-policies", "privacy-terms-cookies", "https://www.texrenfest.com/privacy-terms-cookies", "Privacy, Terms & Cookies"),
    ("join-us-and-policies", "purchase-policy", "https://www.texrenfest.com/purchase-policy", "Purchase Policy"),
]

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def clean_html_to_markdown(raw_html: str, url: str, title: str) -> str:
    """Converts HTML string to readable Markdown text without external dependencies."""
    text = re.sub(r'<script.*?>.*?</script>', '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    text = re.sub(r'<h1.*?>\s*(.*?)\s*</h1>', r'\n\n# \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h2.*?>\s*(.*?)\s*</h2>', r'\n\n## \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h3.*?>\s*(.*?)\s*</h3>', r'\n\n### \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h[4-6].*?>\s*(.*?)\s*</h[4-6]>', r'\n\n#### \1\n\n', text, flags=re.DOTALL | re.IGNORECASE)

    def link_repl(match):
        href = match.group(1)
        anchor_text = re.sub(r'<.*?>', '', match.group(2)).strip()
        if href.startswith('/'):
            href = 'https://www.texrenfest.com' + href
        if not anchor_text:
            return href
        return f'[{anchor_text}]({href})'
    text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', link_repl, text, flags=re.DOTALL | re.IGNORECASE)

    text = re.sub(r'<p.*?>\s*(.*?)\s*</p>', r'\n\n\1\n\n', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<li.*?>\s*(.*?)\s*</li>', r'\n- \1', text, flags=re.DOTALL | re.IGNORECASE)

    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)

    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = []
    prev_blank = False
    for line in lines:
        if not line:
            if not prev_blank:
                cleaned_lines.append('')
                prev_blank = True
        else:
            cleaned_lines.append(line)
            prev_blank = False

    body = '\n'.join(cleaned_lines).strip()

    doc = f"""# {title}

- **Source URL:** [{url}]({url})
- **Category:** TRF Site Corpus
- **Fetched Date:** {time.strftime('%Y-%m-%d')}

---

{body}
"""
    return doc

def fetch_single(item, corpus_dir):
    cat, slug, url, title = item
    cat_dir = corpus_dir / cat
    cat_dir.mkdir(parents=True, exist_ok=True)
    out_file = cat_dir / f"{slug}.md"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            charset = resp.headers.get_param('charset') or 'utf-8'
            raw_html = resp.read().decode(charset, errors='replace')
            md_content = clean_html_to_markdown(raw_html, url, title)
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(md_content)
            return (cat, slug, url, title, "SUCCESS", len(md_content))
    except Exception as e:
        return (cat, slug, url, title, f"FAILED: {e}", 0)

def main():
    root_dir = Path(__file__).resolve().parent.parent
    corpus_dir = root_dir / "docs" / "trf-corpus"
    corpus_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {len(PAGES)} pages concurrently into {corpus_dir}...")
    results = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(fetch_single, item, corpus_dir): item for item in PAGES}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            print(f"  [{res[0]}] {res[3]}: {res[4]} ({res[5]} bytes)")

    print("\nFetch completed!")

if __name__ == "__main__":
    main()
