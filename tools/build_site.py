"""Builds the multi-page Trust Scan+ site.

Usage: python3 site.py <source-index.html> <repo-root>

Section content is taken from the single-page homepage (source-index.html) so the
wording stays exactly as approved. Every page shares one header, menu and footer.
No inline scripts or styles: the site runs under a strict CSP.
"""
import os
import re
import sys

SRC, ROOT = sys.argv[1], sys.argv[2]
src = open(SRC).read()

# Version stamp for the stylesheet and script: it changes whenever either file
# changes, so browsers and Cloudflare fetch the new copy instead of a cached one.
import hashlib
VER = hashlib.sha256(open(os.path.join(ROOT, 'styles.css'), 'rb').read() +
                     open(os.path.join(ROOT, 'script.js'), 'rb').read()).hexdigest()[:10]


def section(name):
    """Return the <section>…</section> that follows <!-- name -->."""
    m = re.search(r'    <!-- ' + re.escape(name) + r' -->\n(    <section.*?\n    </section>\n)', src, re.S)
    assert m, name
    return m.group(1)


def strip_head(html):
    """Remove the first centred section heading (the page hero replaces it)."""
    out, n = re.subn(r'\n        <div class="section-head center">.*?\n        </div>\n', '\n', html, count=1, flags=re.S)
    assert n == 1
    return out


def set_bg(html, alt):
    """Force a section's background: alt (lighter) or plain."""
    html = html.replace(' class="section-alt"', '', 1)
    if alt:
        html = re.sub(r'<section( id="[^"]+")?', lambda m: '<section' + (m.group(1) or '') + ' class="section-alt"', html, count=1)
    return html


def trust_strip():
    m = re.search(r'(    <div class="trust-strip">.*?\n    </div>\n)', src, re.S)
    return m.group(1)


NAV = [
    ('how-it-works.html', 'How it works'),
    ('example-report.html', 'Example report'),
    ('monitoring.html', 'Monitoring'),
    ('pricing.html', 'Pricing'),
    ('faq.html', 'FAQ'),
]

ICON = '''  <link rel="icon" type="image/png" sizes="32x32" href="{p}assets/site/img/favicon-32.png">
  <link rel="apple-touch-icon" href="{p}assets/site/img/apple-touch-icon.png">'''


def head(fn, title, desc, p, noindex=False, og=False):
    canon = '' if noindex else f'\n  <link rel="canonical" href="https://trustscanapp.com/{"" if fn == "index.html" else fn}">'
    robots = '\n  <meta name="robots" content="noindex">' if noindex else ''
    ogt = ''
    if og:
        ogt = f'''
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://trustscanapp.com/{"" if fn == "index.html" else fn}">
  <meta property="og:image" content="https://trustscanapp.com/assets/site/img/social-card.png">
  <meta name="twitter:card" content="summary_large_image">'''
    return f'''<!DOCTYPE html>
<html lang="en-GB" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">{canon}{robots}
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta name="theme-color" content="#001020">{ogt}
{ICON.format(p=p)}
  <link rel="preload" href="{p}assets/site/fonts/poppins-bold.woff" as="font" type="font/woff" crossorigin>
  <link rel="stylesheet" href="{p}styles.css?v={VER}">
  <script src="{p}script.js?v={VER}" defer></script>
</head>
'''


def header(fn, p):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == fn else ''
        items.append(f'          <li><a href="{p}{href}"{cur}>{label}</a></li>')
    cur_app = ' aria-current="page"' if fn == 'coming-soon.html' else ''
    home = './' if not p else p
    return f'''<body>
  <a class="skip-link" href="#main">Skip to content</a>

  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="{home}" aria-label="Trust Scan+ home">
        <img src="{p}assets/site/img/mascot-bigflex.webp" alt="" width="44" height="44">
        <span>Trust Scan<span class="plus">+</span></span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul>
{chr(10).join(items)}
          <li><a class="btn btn-primary btn-small" href="{p}coming-soon.html" data-app-link{cur_app}>Get the app</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="main">
'''


def footer(p):
    home = './' if not p else p
    return f'''  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <a class="brand" href="{home}">
            <img src="{p}assets/site/img/mascot-bigflex.webp" alt="" width="44" height="44" loading="lazy">
            <span>Trust Scan<span class="plus">+</span></span>
          </a>
          <p>Security checks and monitoring for websites you own.</p>
        </div>
        <div>
          <h3>Explore</h3>
          <ul>
            <li><a href="{p}how-it-works.html">How it works</a></li>
            <li><a href="{p}example-report.html">Example report</a></li>
            <li><a href="{p}monitoring.html">Monitoring</a></li>
            <li><a href="{p}pricing.html">Pricing</a></li>
            <li><a href="{p}faq.html">FAQ</a></li>
          </ul>
        </div>
        <div>
          <h3>Help and legal</h3>
          <ul>
            <li><a href="{p}coming-soon.html" data-app-link>Get the app</a></li>
            <li><a href="{p}support.html">Support</a></li>
            <li><a href="{p}privacy.html">Privacy</a></li>
            <li><a href="{p}terms.html">Terms</a></li>
            <li><a href="{p}account-deletion.html">Account deletion</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-base">
        <span>&copy; <span data-year>2026</span> Trust Scan+</span>
        <span>Scheduled checks, not real-time protection.</span>
      </div>
    </div>
  </footer>
</body>
</html>
'''


def page_hero(eyebrow, h1, lead, img, alt=''):
    pic = ''
    if img:
        pic = f'\n        <img class="page-hero-img" src="assets/site/img/{img}" alt="{alt}" width="600" height="600">'
    return f'''    <section class="page-hero">
      <div class="wrap page-hero-inner">
        <div>
          <span class="eyebrow">{eyebrow}</span>
          <h1>{h1}</h1>
          <p class="lead">{lead}</p>
        </div>{pic}
      </div>
    </section>

'''


def pager(href, label, blurb):
    return f'''    <nav class="pager" aria-label="Next page">
      <div class="wrap">
        <a class="pager-link" href="{href}">
          <span class="pager-kicker">Next</span>
          <span class="pager-title">{label} <span aria-hidden="true">&rarr;</span></span>
          <span class="pager-blurb">{blurb}</span>
        </a>
      </div>
    </nav>

'''


def write(fn, title, desc, body, p='', noindex=False, og=False):
    html = head(fn, title, desc, p, noindex, og) + header(fn, p) + body + footer(p)
    with open(os.path.join(ROOT, fn), 'w') as f:
        f.write(html)


T = ' | Trust Scan+'

# ---------------------------------------------------------------- Home
hero = section('Hero').replace('href="#report"', 'href="example-report.html"')
who = section('What you get')
final = section('Final CTA')

explore = '''    <section id="explore" class="section-alt">
      <div class="wrap">
        <div class="section-head center">
          <span class="eyebrow">Find out more</span>
          <h2>Everything in one place.</h2>
          <p class="lead">Pick what you want to know about.</p>
        </div>
        <div class="explore">
          <a class="explore-card" href="how-it-works.html">
            <img src="assets/site/img/mascot-point.webp" alt="" width="640" height="570" loading="lazy">
            <h3>How it works</h3>
            <p>Four simple steps, and how we check that a website is yours.</p>
            <span class="explore-more">Read more <span aria-hidden="true">&rarr;</span></span>
          </a>
          <a class="explore-card" href="example-report.html">
            <img src="assets/site/img/mascot-spotlight.webp" alt="" width="570" height="600" loading="lazy">
            <h3>Example report</h3>
            <p>See what a real report looks like, in plain English.</p>
            <span class="explore-more">See the report <span aria-hidden="true">&rarr;</span></span>
          </a>
          <a class="explore-card" href="monitoring.html">
            <img src="assets/site/img/mascot-alert.webp" alt="" width="570" height="600" loading="lazy">
            <h3>Monitoring</h3>
            <p>Checks twice a day, and an alert when something changes.</p>
            <span class="explore-more">How alerts work <span aria-hidden="true">&rarr;</span></span>
          </a>
          <a class="explore-card" href="pricing.html">
            <img src="assets/site/img/mascot-thumbs.webp" alt="" width="580" height="600" loading="lazy">
            <h3>Pricing</h3>
            <p>A free plan and a full plan, each for one website.</p>
            <span class="explore-more">See prices <span aria-hidden="true">&rarr;</span></span>
          </a>
        </div>
        <p class="explore-faq">Got a question? <a href="faq.html">Read the FAQ</a>.</p>
      </div>
    </section>

'''

preview = '''    <section id="preview">
      <div class="wrap preview">
        <div>
          <span class="eyebrow">Example report</span>
          <h2>Problems explained, with what to do next.</h2>
          <p class="lead">Every finding says how serious it is, what it means and how to fix it, so you or your web developer know exactly where to start.</p>
          <div class="cta-row">
            <a class="btn btn-primary" href="example-report.html">See the example report</a>
          </div>
        </div>
        <div class="mini-rpt" aria-label="Preview of a simplified example report">
          <div class="mini-rpt-top">
            <span class="badge badge-sample">Example</span>
            <span class="mini-score"><b>48</b>/100 · Needs attention</span>
          </div>
          <div class="rpt-find">
            <div class="rpt-find-top"><span class="pill pill-medium">Medium</span><span class="rpt-find-area">Browser protection</span></div>
            <h4>Other websites can show your pages inside theirs</h4>
            <p class="rpt-do"><span class="col-label">What to do next</span>Ask your developer to switch on framing protection.</p>
          </div>
        </div>
      </div>
    </section>

'''

write('index.html',
      'Trust Scan+ | Website security checks in plain English',
      'Trust Scan+ checks your website for security problems, explains what it found in plain English and keeps watch twice a day. Coming soon to the app.',
      hero + '\n' + trust_strip() + '\n' + set_bg(who, False) + '\n' + explore + preview + final + '\n',
      og=True)

# ---------------------------------------------------------------- How it works
how = set_bg(strip_head(section('How it works')), True)
verify = set_bg(section('Verification'), False)
write('how-it-works.html', 'How it works' + T,
      'How Trust Scan+ works: four simple steps in the app, how you prove a website is yours, and how our servers do the checking.',
      page_hero('How it works', 'Four simple steps, all in the app.',
                'Add your website, prove it is yours, and our servers check it for you. You get a report you can understand, with clear steps to fix each problem.',
                'mascot-point.webp')
      + how + '\n' + verify + '\n'
      + pager('example-report.html', 'Example report', 'See what a report looks like.'))

# ---------------------------------------------------------------- Example report
report = set_bg(strip_head(section('Example report')), True)
write('example-report.html', 'Example report' + T,
      'A simplified example of a Trust Scan+ website security report, based on a real report with the website name changed.',
      page_hero('Example report', 'A quick look at a report.',
                'This is a short, simplified preview based on a real Trust Scan+ report, shared with permission and with the website name changed. Your full report checks far more, in much more depth.',
                'mascot-spotlight.webp')
      + report + '\n'
      + pager('monitoring.html', 'Monitoring', 'How twice-daily checks and alerts work.'))

# ---------------------------------------------------------------- Monitoring
mon = set_bg(strip_head(section('Monitoring')), True)
write('monitoring.html', 'Monitoring' + T,
      'Trust Scan+ monitoring checks your website twice a day and tells you what changed, with clear steps to fix it.',
      page_hero('Monitoring', 'We check twice a day and tell you what changed.',
                "Switch on monitoring and we'll check that your website is online, your security certificate is still valid and your key security settings are still switched on. Checks are planned for around 9am and 9pm UK time.",
                'mascot-alert.webp')
      + mon + '\n'
      + pager('pricing.html', 'Pricing', 'A free plan and a full plan, each for one website.'))

# ---------------------------------------------------------------- Pricing
price = set_bg(strip_head(section('Pricing')), True)
limits = set_bg(section('Honesty'), False)
write('pricing.html', 'Pricing' + T,
      'Trust Scan+ pricing: a free plan and a full plan, each for one website. Prices are a draft and may change before launch.',
      page_hero('Pricing', 'Simple pricing.',
                'Each plan covers one website. These prices are a draft and may change before launch.',
                'mascot-thumbs.webp')
      + price + '\n' + limits + '\n'
      + pager('faq.html', 'FAQ', 'Answers to the questions people ask.'))

# ---------------------------------------------------------------- FAQ
faq = set_bg(strip_head(section('FAQ')), True)
write('faq.html', 'FAQ' + T,
      'Answers to common questions about Trust Scan+: which websites you can check, privacy, monitoring and getting the app.',
      page_hero('FAQ', 'Questions people ask.',
                "Straight answers about Trust Scan+. Can't find what you need? Contact support.",
                'mascot-tip.webp')
      + faq + '\n' + final + '\n')

# ---------------------------------------------------------------- Coming soon and small pages
write('coming-soon.html', 'App coming soon' + T,
      'The Trust Scan+ app is coming soon. Sign up, verify your website, get reports and switch on monitoring in the app.',
      '''    <section class="page-hero page-hero-center">
      <div class="wrap">
        <div class="anim">
          <video autoplay muted loop playsinline preload="metadata" poster="assets/site/video/celebrate.jpg" aria-hidden="true">
            <source src="assets/site/video/celebrate.mp4" type="video/mp4">
          </video>
        </div>
        <span class="eyebrow">Coming soon</span>
        <h1>The Trust Scan+ app is on its way.</h1>
        <p class="lead">You'll sign up, verify your website, read reports and switch on monitoring in the app. It isn't in the app stores yet. Store links will appear here as soon as it is.</p>
        <div class="store-row">
          <a class="btn btn-primary store-btn" href="coming-soon.html" data-store="ios" aria-disabled="true">App Store<small>Coming soon</small></a>
          <a class="btn btn-primary store-btn" href="coming-soon.html" data-store="android" aria-disabled="true">Google Play<small>Coming soon</small></a>
        </div>
        <p class="cta-note">Want to know when it launches? <a href="support.html">Get in touch</a> and we'll let you know.</p>
      </div>
    </section>

''' + pager('how-it-works.html', 'How it works', 'While you wait, see how Trust Scan+ works.'))


def placeholder(what):
    return f'''      <div class="paper placeholder">
        <span class="badge badge-draft">Placeholder</span>
        <p>Our full {what} is being prepared and will be published here before the app launches. This page doesn't contain legal terms yet.</p>
      </div>
'''


def simple(fn, title, desc, eyebrow, h1, inner, img=None, alt=''):
    write(fn, title + T, desc,
          page_hero(eyebrow, h1, '', img, alt).replace('\n          <p class="lead"></p>', '')
          + '    <section class="prose-section">\n      <div class="wrap prose">\n' + inner + '      </div>\n    </section>\n\n')


simple('privacy.html', 'Privacy', 'Trust Scan+ privacy information.', 'Privacy', 'Privacy policy',
       placeholder('privacy policy') + '''        <h2>This website</h2>
        <p>This website is a static information page. It has no sign-up, login, forms, tracking or advertising cookies. Accounts, website verification and reports live in the Trust Scan+ app.</p>
        <h2>Questions</h2>
        <p>See <a href="support.html">support</a>.</p>
''')

simple('terms.html', 'Terms', 'Trust Scan+ terms of service.', 'Terms', 'Terms of service',
       placeholder('terms of service, including subscription, billing and cancellation terms,') + '''        <h2>Questions</h2>
        <p>See <a href="support.html">support</a>.</p>
''')

simple('account-deletion.html', 'Account deletion', 'How to delete your Trust Scan+ account and data.', 'Your data', 'Deleting your account',
       placeholder('account deletion process, including what is deleted and how long it takes,') + '''        <h2>Need help now?</h2>
        <p><a href="support.html">Contact support</a> from the email address on your account and we'll help.</p>
''')

simple('support.html', 'Support', 'Get help with Trust Scan+.', 'Support', 'How can we help?',
       '''        <div class="paper contact-card">
          <span class="contact-label">Email us</span>
          <!-- SUPPORT-EMAIL: the only place the support address appears on the site. -->
          <a class="contact-email" href="mailto:support@trustscanapp.com">support@trustscanapp.com</a>
          <p>Questions about Trust Scan+, the app launch, or your website? Send us an email and we'll get back to you. Once the app is live, you'll also be able to contact us from inside it.</p>
        </div>
        <h2>Common questions</h2>
        <p>Many answers are in the <a href="faq.html">FAQ</a>. To delete your account, see <a href="account-deletion.html">deleting your account</a>.</p>
''', 'mascot-thumbs.webp', 'Trust Scan+ mascot giving a thumbs up')

# 404 is served at any URL depth, so it uses absolute paths.
write('404.html', 'Page not found' + T, 'This page could not be found.',
      '''    <section class="page-hero page-hero-center">
      <div class="wrap">
        <img class="mascot mascot-sm" src="/assets/site/img/mascot-running.webp" alt="Startled Trust Scan+ mascot running" width="600" height="579">
        <span class="eyebrow">404</span>
        <h1>We couldn't find that page.</h1>
        <p class="lead">Trust Scan is now Trust Scan+, a website security service for site owners. The page you were looking for may have moved.</p>
        <div class="store-row">
          <a class="btn btn-primary" href="/">Go to the homepage</a>
        </div>
      </div>
    </section>

''', p='/', noindex=True)

print('built')
