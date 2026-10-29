import re, json, requests, pathlib
KEY="fk_nZb9pbqyBF80RsTX_Ay1qj3oVH6QZMm6"
URL="https://gateway.finest.so/gateway/openai/v1/chat/completions"
MODEL="claude-opus-5"
css=pathlib.Path("style.css").read_text()
RULES="""You write production HTML for datapartners.online, a small independent referral-partner site for businesses (30+ employees) that may be eligible for AI data partnership programs. Funnel CTA link: https://go.datapartners.online
HARD RULES:
- Output ONLY the complete HTML document, no markdown fences, no commentary.
- ZERO em dashes and zero double hyphens anywhere. Use commas, colons, periods.
- Plain, direct, trustworthy tone for business owners. No hype.
- NEVER promise or guarantee payment. No 'you will earn'. Any dollar figure must be attributed as past fact, e.g. 'Companies have been offered $100K+ for anonymized data', and followed by 'not all companies qualify'.
- Never mention referral rewards or what we earn per deal except in the disclosure sentence 'we may receive compensation if a company we refer is approved'.
- No brand impersonation: do not use the name micro1 as our brand, no logos. We are an independent referral partner, not the data buyer.
- Use only these classes from the stylesheet (already linked at /style.css): header, wrap, nav, logo (with <span> for 'Partners'), link, hero, btn, section, alt, grid, card, num, note, footer, doc.
- Include responsive meta viewport, a real <title> and meta description.
- Footer must link /privacy.html and /terms.html and show contact goldstandardsolutions24@gmail.com.
STYLESHEET FOR REFERENCE:
"""+css
PAGES={
"index.html":"Homepage. Hero H1 should hook owners of companies with 30+ employees. Sections: how it works (3 steps: quick eligibility check, secure partner portal, review and decide), what kind of data (anonymized operational material like SOPs, project histories, documentation; not customer personal data), 3 FAQ cards (who are you, does everyone qualify, cost), and a clear disclosure note. Primary CTA button 'Check eligibility' to the funnel link, repeated once mid-page.",
"privacy.html":"Privacy Policy page (class doc). Cover data collected (name, email, phone, company size, systems used), use, no sale of personal info, mobile information never shared with third parties for marketing, STOP to opt out, deletion requests via email. Dated October 28, 2026.",
"terms.html":"Terms and SMS Terms page (class doc). Independent referral partner, no guarantees, may receive compensation if referral approved. SMS program: consent not a condition of purchase, message frequency varies, msg and data rates may apply, STOP to cancel, HELP for help, link to privacy. Dated October 28, 2026."}
for name,brief in PAGES.items():
    for attempt in range(3):
        r=requests.post(URL,headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"},
          json={"model":MODEL,"max_tokens":6000,"messages":[{"role":"system","content":RULES},{"role":"user","content":f"Write {name}. {brief}"}]},timeout=180)
        r.raise_for_status()
        html=r.json()["choices"][0]["message"]["content"].strip()
        html=re.sub(r"^```(?:html)?\s*|\s*```$","",html)
        bad=[x for x in ["\u2014","--"] if x in html.replace("<!--","").replace("-->","")]
        ok=html.lower().startswith("<!doctype") and "</html>" in html.lower() and not bad
        if name=="index.html": ok=ok and "go.datapartners.online" in html and "/privacy.html" in html and "/terms.html" in html
        if ok: pathlib.Path(name).write_text(html); print("OK",name,len(html)); break
        print("retry",name,bad)
    else: raise SystemExit("failed "+name)
