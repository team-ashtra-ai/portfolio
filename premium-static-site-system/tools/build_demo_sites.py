#!/usr/bin/env python3
"""Build the 50 ASH-TRA premium static demo sites.

The generated pages are plain static HTML/CSS/JS files. This tool is only a
production helper so the large portfolio can be rebuilt consistently from the
approved matrix and then edited by hand per site if needed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import math
import re
import shutil
import struct
import textwrap
import zlib
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urljoin


ROOT = Path(__file__).resolve().parents[2]
SYSTEM_ROOT = ROOT / "premium-static-site-system"
DEMO_ROOT = ROOT / "demo-sites"
FORM_ENDPOINT = "https://formspree.io/f/mdabwgdk"
ASH_TRA_CONTACT = "https://ash-tra.com/contact/"
ASH_TRA_DISCOVERY = "https://ash-tra.com/discovery/"
WHATSAPP_NUMBER = "15550132456"

TRANSFORMATION_PACK_FILES = [
    "docs/inspiration-audit.md",
    "docs/design-extraction.md",
    "docs/theme-direction.md",
    "docs/theme-guide.md",
    "docs/layout-system.md",
    "docs/partials-system.md",
    "docs/component-system.md",
    "docs/css-system.md",
    "docs/js-system.md",
    "docs/js-interaction-plan.md",
    "docs/asset-system.md",
    "docs/asset-direction.md",
    "docs/page-section-style-map.md",
    "docs/mobile-system.md",
    "docs/mobile-behaviour.md",
    "docs/conversion-system.md",
    "docs/cross-site-difference-report.md",
]

SOURCE_PARTIALS = [
    "header.html",
    "mobile-menu.html",
    "footer.html",
    "hero.html",
    "cta.html",
    "form.html",
    "cards.html",
    "resources.html",
    "pricing.html",
    "faq.html",
    "cookie.html",
    "whatsapp.html",
    "back-to-top.html",
    "legal.html",
    "404.html",
    "thanks.html",
]

GENERATED_ASSET_DIRS = [
    "assets/brand",
    "assets/images",
    "assets/icons",
    "assets/illustrations",
    "assets/mockups",
    "assets/downloads",
    "assets/og",
    "assets/video",
]

REQUIRED_CSS_TOKENS = [
    "--font-display", "--font-body", "--font-accent", "--font-mono",
    "--text-xs", "--text-sm", "--text-md", "--text-lg", "--text-xl", "--text-hero",
    "--line-tight", "--line-normal", "--line-loose",
    "--tracking-tight", "--tracking-normal", "--tracking-wide",
    "--color-bg", "--color-bg-alt", "--color-surface", "--color-surface-raised", "--color-text",
    "--color-muted", "--color-primary", "--color-secondary", "--color-accent", "--color-border",
    "--color-success", "--color-warning", "--color-error",
    "--gradient-primary", "--gradient-surface", "--overlay-dark", "--overlay-light",
    "--container-sm", "--container-md", "--container-lg", "--container-xl", "--container-fluid",
    "--space-xs", "--space-sm", "--space-md", "--space-lg", "--space-xl", "--space-section",
    "--radius-none", "--radius-sm", "--radius-md", "--radius-lg", "--radius-xl", "--radius-pill",
    "--shadow-none", "--shadow-soft", "--shadow-medium", "--shadow-strong", "--shadow-glow",
    "--border-thin", "--border-medium", "--border-strong",
    "--motion-fast", "--motion-base", "--motion-slow", "--motion-ease",
]

COMPONENT_FAMILIES = [
    "site-header", "mobile-menu", "footer", "hero", "section", "section-header", "content-grid",
    "card", "button", "form", "input", "textarea", "select", "checkbox", "badge", "tag",
    "breadcrumb", "accordion", "tabs", "pricing", "table", "timeline", "gallery", "lightbox",
    "testimonial", "metric", "case-study", "article-card", "download-card", "profile-card",
    "product-card", "listing-card", "CTA-strip", "cookie-banner", "legal-page", "error-page",
    "thanks-page",
]

CSS_STATE_LIST = [
    "default", "hover", "focus", "focus-visible", "active", "disabled", "loading", "success",
    "error", "empty", "expanded", "collapsed", "selected", "current", "sticky", "scrolled",
    "reduced-motion",
]

SECTION_COMPOSITIONS = [
    "split text/image", "full-bleed image", "editorial masthead", "dashboard panel", "card grid",
    "asymmetric grid", "timeline", "stepper", "map block", "booking panel", "search panel",
    "filter grid", "gallery wall", "product shelf", "pricing comparison", "FAQ accordion",
    "report/download block", "quote/testimonial block", "metric band", "process ladder",
    "story block", "document checklist", "form panel", "CTA banner", "side-by-side comparison",
    "sticky sidebar section", "marquee/logos strip", "case-study block",
]

REFERENCE_EXTRACTION_FIELDS = [
    "Layout archetype", "Header structure", "Desktop navigation style", "Mobile menu behaviour",
    "Footer structure", "Typography mood", "Colour palette", "Surface system", "Hero type",
    "Section rhythm", "Card design", "Form pattern", "CTA flow", "Asset direction",
    "Image treatment", "Icon/illustration style", "JS interaction ideas", "Motion style",
    "Mobile behaviour", "What must not be copied",
]

REFERENCE_LINES = """
1|direct:Mayo Clinic@https://www.mayoclinic.org;direct:Cleveland Clinic@https://my.clevelandclinic.org;direct:One Medical@https://www.onemedical.com;adjacent:Tia@https://www.asktia.com;adjacent:Modern Animal@https://www.modernanimal.com;contrast:Aman@https://www.aman.com;contrast:GOV.UK@https://www.gov.uk;interaction:Zocdoc booking and search flows@https://www.zocdoc.com
2|direct:Moderna@https://www.modernatx.com;direct:Genentech@https://www.gene.com;direct:Ginkgo Bioworks@https://www.ginkgobioworks.com;adjacent:Benchling@https://www.benchling.com;adjacent:10x Genomics@https://www.10xgenomics.com;contrast:Databricks@https://www.databricks.com;contrast:MIT Media Lab@https://www.media.mit.edu;interaction:Mobbin research dashboard patterns@https://mobbin.com
3|direct:Headspace@https://www.headspace.com;direct:Calm@https://www.calm.com;direct:ClassPass@https://classpass.com;adjacent:Ritual@https://ritual.com;adjacent:Alo Moves@https://www.alomoves.com;contrast:Aesop@https://www.aesop.com;contrast:Soho House@https://www.sohohouse.com;interaction:Mindbody booking flows@https://www.mindbodyonline.com
4|direct:Cloudflare@https://www.cloudflare.com;direct:DigitalOcean@https://www.digitalocean.com;direct:Rackspace Technology@https://www.rackspace.com;adjacent:Atlassian@https://www.atlassian.com;adjacent:ServiceNow@https://www.servicenow.com;contrast:Linear@https://linear.app;contrast:Vercel@https://vercel.com;interaction:Mobbin support portal patterns@https://mobbin.com
5|direct:Linear@https://linear.app;direct:Stripe@https://stripe.com;direct:Figma@https://www.figma.com;adjacent:Notion@https://www.notion.com;adjacent:Vercel@https://vercel.com;contrast:Apple@https://www.apple.com;contrast:Arc Browser@https://arc.net;interaction:Mobbin SaaS onboarding flows@https://mobbin.com
6|direct:Starlink@https://www.starlink.com;direct:Verizon Business@https://www.verizon.com/business;direct:Google Fiber@https://fiber.google.com;adjacent:Ting Internet@https://ting.com/internet;adjacent:T-Mobile Business@https://www.t-mobile.com/business;contrast:Citymapper@https://citymapper.com;contrast:Octopus Energy@https://octopus.energy;interaction:Mobbin availability checker patterns@https://mobbin.com
7|direct:Wiz@https://www.wiz.io;direct:Snyk@https://snyk.io;direct:CrowdStrike@https://www.crowdstrike.com;adjacent:Okta@https://www.okta.com;adjacent:1Password@https://1password.com;contrast:Linear@https://linear.app;contrast:GOV.UK service patterns@https://design-system.service.gov.uk;interaction:Mobbin security console patterns@https://mobbin.com
8|direct:Databricks@https://www.databricks.com;direct:Snowflake@https://www.snowflake.com;direct:Tableau@https://www.tableau.com;adjacent:Looker@https://cloud.google.com/looker;adjacent:Amplitude@https://amplitude.com;contrast:Bloomberg@https://www.bloomberg.com;contrast:The Pudding@https://pudding.cool;interaction:Observable notebook patterns@https://observablehq.com
9|direct:Wise@https://wise.com;direct:Revolut@https://www.revolut.com;direct:Monzo@https://monzo.com;adjacent:Ramp@https://ramp.com;adjacent:Mercury@https://mercury.com;contrast:Apple Card@https://www.apple.com/apple-card;contrast:Financial Times@https://www.ft.com;interaction:Mobbin finance calculator flows@https://mobbin.com
10|direct:Lemonade@https://www.lemonade.com;direct:Oscar Health@https://www.hioscar.com;direct:Allianz@https://www.allianz.com;adjacent:Policygenius@https://www.policygenius.com;adjacent:Simply Business@https://www.simplybusiness.com;contrast:Wise@https://wise.com;contrast:GOV.UK benefits service flows@https://www.gov.uk;interaction:Mobbin quote and claims flows@https://mobbin.com
11|direct:Clio@https://www.clio.com;direct:AO Shearman@https://www.aoshearman.com;direct:Fragomen@https://www.fragomen.com;adjacent:Boundless@https://www.boundless.com;adjacent:LegalZoom@https://www.legalzoom.com;contrast:GOV.UK@https://www.gov.uk;contrast:USWDS@https://designsystem.digital.gov;interaction:Mobbin document checklist flows@https://mobbin.com
12|direct:Xero@https://www.xero.com;direct:QuickBooks@https://quickbooks.intuit.com;direct:FreshBooks@https://www.freshbooks.com;adjacent:Bench@https://www.bench.co;adjacent:Pilot@https://pilot.com;contrast:Notion@https://www.notion.com;contrast:GOV.UK tax service pages@https://www.gov.uk;interaction:Mobbin admin checklist flows@https://mobbin.com
13|direct:McKinsey@https://www.mckinsey.com;direct:BCG@https://www.bcg.com;direct:Bain@https://www.bain.com;adjacent:IDEO@https://www.ideo.com;adjacent:Accenture@https://www.accenture.com;contrast:Pentagram@https://www.pentagram.com;contrast:Harvard Business Review@https://hbr.org;interaction:Mobbin diagnostic quiz patterns@https://mobbin.com
14|direct:Coursera@https://www.coursera.org;direct:Duolingo@https://www.duolingo.com;direct:Khan Academy@https://www.khanacademy.org;adjacent:MasterClass@https://www.masterclass.com;adjacent:General Assembly@https://generalassemb.ly;contrast:Headspace@https://www.headspace.com;contrast:Apple Education@https://www.apple.com/education;interaction:Mobbin course onboarding flows@https://mobbin.com
15|direct:Greenhouse@https://www.greenhouse.com;direct:Workday@https://www.workday.com;direct:Lever@https://www.lever.co;adjacent:Indeed@https://www.indeed.com;adjacent:Remote@https://remote.com;contrast:Airbnb Careers@https://careers.airbnb.com;contrast:Spotify Careers@https://www.lifeatspotify.com;interaction:Mobbin job search and upload flows@https://mobbin.com
16|direct:Zillow@https://www.zillow.com;direct:Compass@https://www.compass.com;direct:Redfin@https://www.redfin.com;adjacent:The Modern House@https://www.themodernhouse.com;adjacent:Airbnb@https://www.airbnb.com;contrast:Aman@https://www.aman.com;contrast:Dezeen@https://www.dezeen.com;interaction:Mobbin property filter patterns@https://mobbin.com
17|direct:Turner Construction@https://www.turnerconstruction.com;direct:Skanska@https://www.skanska.com;direct:Procore@https://www.procore.com;adjacent:Hilti@https://www.hilti.com;adjacent:Houzz@https://www.houzz.com;contrast:Patagonia@https://www.patagonia.com;contrast:Tesla@https://www.tesla.com;interaction:Mobbin estimate and upload flows@https://mobbin.com
18|direct:Snohetta@https://www.snohetta.com;direct:BIG@https://big.dk;direct:Foster and Partners@https://www.fosterandpartners.com;adjacent:Dezeen@https://www.dezeen.com;adjacent:Heatherwick Studio@https://www.heatherwick.com;contrast:Aesop@https://www.aesop.com;contrast:Aman@https://www.aman.com;interaction:Mobbin portfolio gallery patterns@https://mobbin.com
19|direct:Studio McGee@https://www.studiomcgee.com;direct:Design Within Reach@https://www.dwr.com;direct:Soho Home@https://www.sohohome.com;adjacent:Muuto@https://www.muuto.com;adjacent:The Future Perfect@https://www.thefutureperfect.com;contrast:Aesop@https://www.aesop.com;contrast:The Modern House@https://www.themodernhouse.com;interaction:Mobbin moodboard and room selector patterns@https://mobbin.com
20|direct:Siemens@https://www.siemens.com;direct:Bosch@https://www.bosch.com;direct:Xometry@https://www.xometry.com;adjacent:Protolabs@https://www.protolabs.com;adjacent:Formlabs@https://formlabs.com;contrast:Tesla@https://www.tesla.com;contrast:Apple manufacturing stories@https://www.apple.com;interaction:Mobbin RFQ and spec table patterns@https://mobbin.com
21|direct:Arup@https://www.arup.com;direct:WSP@https://www.wsp.com;direct:Ramboll@https://www.ramboll.com;adjacent:Buro Happold@https://www.burohappold.com;adjacent:Mott MacDonald@https://www.mottmac.com;contrast:MIT Media Lab@https://www.media.mit.edu;contrast:NASA@https://www.nasa.gov;interaction:Mobbin diagram tabs and checklist patterns@https://mobbin.com
22|direct:Octopus Energy@https://octopus.energy;direct:Tesla Energy@https://www.tesla.com/energy;direct:GE Vernova@https://www.gevernova.com;adjacent:Enphase@https://enphase.com;adjacent:Sunrun@https://www.sunrun.com;contrast:Apple Environment@https://www.apple.com/environment;contrast:Patagonia@https://www.patagonia.com;interaction:Mobbin savings calculator patterns@https://mobbin.com
23|direct:National Grid@https://www.nationalgrid.com;direct:Thames Water@https://www.thameswater.co.uk;direct:Scottish Water@https://www.scottishwater.co.uk;adjacent:EDF@https://www.edfenergy.com;adjacent:gov.br service portal@https://www.gov.br;contrast:GOV.UK@https://www.gov.uk;contrast:USWDS@https://designsystem.digital.gov;interaction:Mobbin fault reporting flows@https://mobbin.com
24|direct:Watershed@https://watershed.com;direct:Plan A@https://plana.earth;direct:Sweep@https://www.sweep.net;adjacent:Project Drawdown@https://drawdown.org;adjacent:Carbon Trust@https://www.carbontrust.com;contrast:The Pudding@https://pudding.cool;contrast:Bloomberg Green@https://www.bloomberg.com/green;interaction:Mobbin impact filter patterns@https://mobbin.com
25|direct:John Deere@https://www.deere.com;direct:Bayer Crop Science@https://www.cropscience.bayer.com;direct:Indigo Ag@https://www.indigoag.com;adjacent:Farmers Business Network@https://www.fbn.com;adjacent:Yara@https://www.yara.com;contrast:Patagonia@https://www.patagonia.com;contrast:National Geographic@https://www.nationalgeographic.com;interaction:Mobbin seasonal planner patterns@https://mobbin.com
26|direct:Oatly@https://www.oatly.com;direct:Innocent Drinks@https://www.innocentdrinks.co.uk;direct:Tonys Chocolonely@https://tonyschocolonely.com;adjacent:Impossible Foods@https://impossiblefoods.com;adjacent:Chobani@https://www.chobani.com;contrast:Aesop@https://www.aesop.com;contrast:Dishoom@https://www.dishoom.com;interaction:Mobbin allergen filter patterns@https://mobbin.com
27|direct:Dishoom@https://www.dishoom.com;direct:Sketch London@https://sketch.london;direct:Noma@https://noma.dk;adjacent:Sweetgreen@https://www.sweetgreen.com;adjacent:Blue Bottle Coffee@https://bluebottlecoffee.com;contrast:Aman@https://www.aman.com;contrast:Aesop@https://www.aesop.com;interaction:Mobbin reservation and menu flows@https://mobbin.com
28|direct:Aman@https://www.aman.com;direct:Rosewood Hotels@https://www.rosewoodhotels.com;direct:Four Seasons@https://www.fourseasons.com;adjacent:Ace Hotel@https://acehotel.com;adjacent:Airbnb@https://www.airbnb.com;contrast:The Modern House@https://www.themodernhouse.com;contrast:Monocle@https://monocle.com;interaction:Mobbin room booking patterns@https://mobbin.com
29|direct:Intrepid Travel@https://www.intrepidtravel.com;direct:GetYourGuide@https://www.getyourguide.com;direct:Airbnb Experiences@https://www.airbnb.com;adjacent:Black Tomato@https://www.blacktomato.com;adjacent:Lonely Planet@https://www.lonelyplanet.com;contrast:Aman@https://www.aman.com;contrast:NYT Travel@https://www.nytimes.com/section/travel;interaction:Mobbin itinerary planner patterns@https://mobbin.com
30|direct:Uber@https://www.uber.com;direct:Lyft@https://www.lyft.com;direct:Bolt@https://bolt.eu;adjacent:Citymapper@https://citymapper.com;adjacent:Trainline@https://www.thetrainline.com;contrast:Starlink@https://www.starlink.com;contrast:Google Maps@https://www.google.com/maps;interaction:Mobbin route selector patterns@https://mobbin.com
31|direct:DHL@https://www.dhl.com;direct:Maersk@https://www.maersk.com;direct:Flexport@https://www.flexport.com;adjacent:UPS@https://www.ups.com;adjacent:project44@https://www.project44.com;contrast:Databricks@https://www.databricks.com;contrast:Bloomberg@https://www.bloomberg.com;interaction:Mobbin tracking dashboard patterns@https://mobbin.com
32|direct:Porsche@https://www.porsche.com;direct:Polestar@https://www.polestar.com;direct:Rivian@https://rivian.com;adjacent:Tesla@https://www.tesla.com;adjacent:Volvo Cars@https://www.volvocars.com;contrast:Apple@https://www.apple.com;contrast:Nike@https://www.nike.com;interaction:Mobbin inventory and finance flows@https://mobbin.com
33|direct:Virgin Atlantic@https://www.virginatlantic.com;direct:Boom Supersonic@https://boomsupersonic.com;direct:Airbus@https://www.airbus.com;adjacent:NetJets@https://www.netjets.com;adjacent:VistaJet@https://www.vistajet.com;contrast:NASA@https://www.nasa.gov;contrast:Aman@https://www.aman.com;interaction:Mobbin fleet tab patterns@https://mobbin.com
34|direct:Maersk@https://www.maersk.com;direct:MSC@https://www.msc.com;direct:Ocean Network Express@https://www.one-line.com;adjacent:Port of Rotterdam@https://www.portofrotterdam.com;adjacent:Stena Line@https://www.stenaline.com;contrast:National Geographic@https://www.nationalgeographic.com;contrast:Flexport@https://www.flexport.com;interaction:Mobbin cargo quote patterns@https://mobbin.com
35|direct:Apple Store@https://www.apple.com;direct:Nike@https://www.nike.com;direct:Patagonia@https://www.patagonia.com;adjacent:Muji@https://www.muji.com;adjacent:Target@https://www.target.com;contrast:Aesop@https://www.aesop.com;contrast:Oatly@https://www.oatly.com;interaction:Mobbin category and store finder patterns@https://mobbin.com
36|direct:Shopify@https://www.shopify.com;direct:Amazon@https://www.amazon.com;direct:Etsy@https://www.etsy.com;adjacent:Farfetch@https://www.farfetch.com;adjacent:Mercado Livre@https://www.mercadolivre.com.br;contrast:Stripe@https://stripe.com;contrast:Airbnb@https://www.airbnb.com;interaction:Mobbin commerce checkout flows@https://mobbin.com
37|direct:Gucci@https://www.gucci.com;direct:Burberry@https://www.burberry.com;direct:Loewe@https://www.loewe.com;adjacent:COS@https://www.cos.com;adjacent:SSENSE@https://www.ssense.com;contrast:A24@https://a24films.com;contrast:Monocle@https://monocle.com;interaction:Mobbin lookbook and sizing patterns@https://mobbin.com
38|direct:Aesop@https://www.aesop.com;direct:Glossier@https://www.glossier.com;direct:Fenty Beauty@https://fentybeauty.com;adjacent:The Ordinary@https://theordinary.com;adjacent:Sephora@https://www.sephora.com;contrast:Ritual@https://ritual.com;contrast:Apple product pages@https://www.apple.com;interaction:Mobbin routine finder patterns@https://mobbin.com
39|direct:The Verge@https://www.theverge.com;direct:Bloomberg@https://www.bloomberg.com;direct:Vox@https://www.vox.com;adjacent:BBC@https://www.bbc.com;adjacent:NPR@https://www.npr.org;contrast:Netflix@https://www.netflix.com;contrast:Spotify@https://www.spotify.com;interaction:Mobbin schedule filter patterns@https://mobbin.com
40|direct:Netflix@https://www.netflix.com;direct:A24@https://a24films.com;direct:Spotify@https://www.spotify.com;adjacent:Ticketmaster@https://www.ticketmaster.com;adjacent:Dice@https://dice.fm;contrast:Nike@https://www.nike.com;contrast:Aman@https://www.aman.com;interaction:Mobbin ticket selector patterns@https://mobbin.com
41|direct:Monocle@https://monocle.com;direct:The New Yorker@https://www.newyorker.com;direct:Financial Times@https://www.ft.com;adjacent:Substack@https://substack.com;adjacent:Harvard Business Review@https://hbr.org;contrast:Readymag@https://readymag.com;contrast:The Pudding@https://pudding.cool;interaction:Mobbin library search patterns@https://mobbin.com
42|direct:Wieden Kennedy@https://www.wk.com;direct:Ogilvy@https://www.ogilvy.com;direct:AKQA@https://www.akqa.com;adjacent:RGA@https://www.rga.com;adjacent:Media.Monks@https://media.monks.com;contrast:Pentagram@https://www.pentagram.com;contrast:Stripe@https://stripe.com;interaction:Mobbin case study filter patterns@https://mobbin.com
43|direct:Pentagram@https://www.pentagram.com;direct:COLLINS@https://www.wearecollins.com;direct:Buck@https://buck.co;adjacent:Instrument@https://www.instrument.com;adjacent:Metalab@https://www.metalab.com;contrast:A24@https://a24films.com;contrast:Apple@https://www.apple.com;interaction:Mobbin portfolio lightbox patterns@https://mobbin.com
44|direct:Nike@https://www.nike.com;direct:Equinox@https://www.equinox.com;direct:Strava@https://www.strava.com;adjacent:WHOOP@https://www.whoop.com;adjacent:Barrys@https://www.barrys.com;contrast:Peloton@https://www.onepeloton.com;contrast:Apple Fitness Plus@https://www.apple.com/apple-fitness-plus;interaction:Mobbin timetable and membership patterns@https://mobbin.com
45|direct:Luma@https://luma.com;direct:Eventbrite@https://www.eventbrite.com;direct:The Knot@https://www.theknot.com;adjacent:Cvent@https://www.cvent.com;adjacent:Vogue Weddings@https://www.vogue.com/weddings;contrast:Aman@https://www.aman.com;contrast:Aesop@https://www.aesop.com;interaction:Mobbin event planner patterns@https://mobbin.com
46|direct:GOV.UK@https://www.gov.uk;direct:GOV.UK Design System@https://design-system.service.gov.uk;direct:USWDS@https://designsystem.digital.gov;adjacent:NYC.gov@https://www.nyc.gov;adjacent:Data.gov@https://data.gov;contrast:Citymapper@https://citymapper.com;contrast:Octopus Energy@https://octopus.energy;interaction:USWDS service form patterns@https://designsystem.digital.gov
47|direct:charity water@https://www.charitywater.org;direct:WWF@https://www.worldwildlife.org;direct:Red Cross@https://www.redcross.org;adjacent:UNICEF@https://www.unicef.org;adjacent:Kiva@https://www.kiva.org;contrast:Patagonia@https://www.patagonia.com;contrast:National Geographic@https://www.nationalgeographic.com;interaction:Mobbin donation selector patterns@https://mobbin.com
48|direct:Rover@https://www.rover.com;direct:Chewy@https://www.chewy.com;direct:Modern Animal@https://www.modernanimal.com;adjacent:The Farmers Dog@https://www.thefarmersdog.com;adjacent:VCA Animal Hospitals@https://vcahospitals.com;contrast:One Medical@https://www.onemedical.com;contrast:Glossier@https://www.glossier.com;interaction:Mobbin appointment and emergency helper patterns@https://mobbin.com
49|direct:Rolex@https://www.rolex.com;direct:Louis Vuitton@https://www.louisvuitton.com;direct:Aman@https://www.aman.com;adjacent:Bang and Olufsen@https://www.bang-olufsen.com;adjacent:NetJets@https://www.netjets.com;contrast:Aesop@https://www.aesop.com;contrast:Polestar@https://www.polestar.com;interaction:Mobbin private access patterns@https://mobbin.com
50|direct:James Clear@https://jamesclear.com;direct:Seth Godin@https://seths.blog;direct:Tim Ferriss@https://tim.blog;adjacent:Marie Forleo@https://www.marieforleo.com;adjacent:Simon Sinek@https://simonsinek.com;contrast:Monocle@https://monocle.com;contrast:The New Yorker@https://www.newyorker.com;interaction:Mobbin media kit and newsletter patterns@https://mobbin.com
""".strip()


MATRIX_LINES = """
1|Healthcare, Medical Services & Patient Care|healthcare|Home:Hero,Need,Symptoms,Promise,Services,Pathway,Evidence,Reviews,Reassurance,CTA;Clinic:Hero,Story,Mission,Team,Standards,Facilities,Credentials,Values,Ethics,CTA;Care:Hero,Concerns,Assessment,Diagnosis,Options,Safety,Support,Followup,Suitability,CTA;Treatments:Hero,Overview,Preventive,Diagnostic,Specialist,Benefits,Preparation,Risks,Recovery,CTA;Journey:Hero,Booking,Intake,Consultation,Examination,Planning,Treatment,Monitoring,Aftercare,CTA;Doctors:Hero,Specialists,Profiles,Qualifications,Experience,Approach,Availability,Trust,Introductions,CTA;Outcomes:Hero,Results,Stories,Testimonials,Evidence,Expectations,Limits,Disclaimers,Confidence,CTA;Pricing:Hero,Fees,Consults,Procedures,Packages,Insurance,Payments,Policies,Clarity,CTA;Guides:Hero,Topics,Prevention,Symptoms,Recovery,Lifestyle,Articles,Downloads,Education,CTA;Contact:Hero,Appointments,Form,Phone,WhatsApp,Location,Hours,Map,Support,CTA
2|Life Sciences, Pharmaceuticals & Biotechnology|life-sciences|Home:Hero,Mission,Disease,Platform,Pipeline,Evidence,Partners,News,Trust,CTA;Company:Hero,Origin,Vision,Leadership,Ethics,Team,Milestones,Values,Governance,CTA;Science:Hero,Biology,Mechanism,Hypothesis,Models,Validation,Evidence,Publications,Limits,CTA;Pipeline:Hero,Programs,Discovery,Preclinical,Clinical,Milestones,Status,Differentiation,Updates,CTA;Trials:Hero,Purpose,Eligibility,Sites,Protocol,Safety,Patients,Teams,Questions,CTA;Platform:Hero,Technology,Assays,Molecules,Data,Applications,Validation,Differentiation,Uses,CTA;Research:Hero,Papers,Posters,Methods,Findings,Datasets,Collaborations,Citations,Downloads,CTA;Partners:Hero,Pharma,Academic,Clinical,Licensing,Models,Benefits,Process,Fit,CTA;News:Hero,Updates,Funding,Press,Events,Publications,Media,Archive,Highlights,CTA;Contact:Hero,Science,Investors,Media,Partners,Form,Office,Routing,Response,CTA
3|Wellness, Personal Care & Lifestyle Services|wellness|Home:Hero,Goal,Problem,Promise,Services,Method,Results,Reviews,Reassurance,CTA;Studio:Hero,Story,Philosophy,Expertise,Values,Atmosphere,Standards,Care,Trust,CTA;Services:Hero,Overview,Treatments,Programs,Consults,Benefits,Fit,Experience,Questions,CTA;Method:Hero,Assessment,Plan,Routine,Session,Support,Progress,Adjustments,Maintenance,CTA;Results:Hero,Outcomes,Stories,Reviews,Photos,Timeline,Expectations,Proof,Confidence,CTA;Pricing:Hero,Sessions,Packages,Memberships,Addons,Inclusions,Payments,Policies,Fit,CTA;Products:Hero,Range,Routines,Bundles,Ingredients,Usage,Benefits,Reviews,Questions,CTA;Journal:Hero,Topics,Selfcare,Lifestyle,Beauty,Recovery,Education,Tips,Articles,CTA;Questions:Hero,Suitability,Preparation,Frequency,Products,Safety,Payment,Cancellation,Support,CTA;Contact:Hero,Booking,Form,WhatsApp,Phone,Location,Hours,Socials,Map,CTA
4|Technology, IT Services & Digital Infrastructure|technology|Home:Hero,Problem,Risk,Promise,Services,Systems,Proof,Reliability,Questions,CTA;Company:Hero,Story,Expertise,Team,Standards,Tools,Partners,Values,Trust,CTA;Services:Hero,Support,Cloud,Networks,Devices,Monitoring,Maintenance,Benefits,Scope,CTA;Systems:Hero,Architecture,Servers,Cloud,Devices,Integrations,Monitoring,Documentation,Scale,CTA;Security:Hero,Risk,Access,Backup,Endpoints,Response,Compliance,Training,Protection,CTA;Process:Hero,Audit,Roadmap,Setup,Migration,Testing,Documentation,Training,Maintenance,CTA;Results:Hero,Uptime,Speed,Savings,Cases,Metrics,Reviews,Impact,Proof,CTA;Pricing:Hero,Plans,Support,SLAs,Retainers,Addons,Emergency,Comparison,Terms,CTA;Support:Hero,Tickets,Remote,Onsite,Emergency,Response,Escalation,Docs,Questions,CTA;Contact:Hero,Sales,Help,Emergency,Form,Phone,Location,Hours,Routing,CTA
5|Software, SaaS Platforms & Digital Products|saas|Home:Hero,Problem,Promise,Product,Features,Solutions,Proof,Integrations,Questions,CTA;Company:Hero,Story,Mission,Team,Vision,Roadmap,Values,Customers,Trust,CTA;Product:Hero,Overview,Modules,Screens,Workflows,Roles,Integrations,Benefits,Difference,CTA;Features:Hero,Automation,Reporting,Collaboration,Permissions,Security,Comparison,Details,Flexibility,CTA;Solutions:Hero,Uses,Teams,Industries,Problems,Outcomes,Workflows,Proof,Fit,CTA;Pricing:Hero,Plans,Starter,Growth,Enterprise,Limits,Addons,Comparison,Questions,CTA;Resources:Hero,Guides,Templates,Webinars,Downloads,Education,Tips,Content,Newsletter,CTA;Blog:Hero,Updates,Strategy,Industry,Tutorials,Opinion,Categories,Featured,Archive,CTA;Support:Hero,Help,Docs,Tickets,Status,Issues,Account,Billing,Security,CTA;Contact:Hero,Sales,Demo,Support,Partners,Form,Office,Response,Trust,CTA
6|Telecommunications, Internet & Connectivity|telecommunications|Home:Hero,Connectivity,Speed,Coverage,Plans,Business,Reliability,Reviews,Questions,CTA;Network:Hero,Mission,Company,Community,Infrastructure,Team,Standards,Expansion,Trust,CTA;Plans:Hero,Residential,Business,Enterprise,Speeds,Routers,Contracts,Comparison,Details,CTA;Coverage:Hero,Areas,Map,Check,Expansion,Waiting,Availability,Reliability,Questions,CTA;Business:Hero,Internet,Failover,Static,SLAs,Security,Support,Scale,Proof,CTA;Install:Hero,Booking,Equipment,Visit,Setup,Activation,Testing,WiFi,Aftercare,CTA;Support:Hero,Outages,Billing,Setup,Router,Speed,Tickets,Response,Escalation,CTA;Guides:Hero,WiFi,Security,Remote,Routers,Speed,Advice,Updates,Articles,CTA;Questions:Hero,Speeds,Contracts,Routers,Install,Billing,Support,Policies,Help,CTA;Contact:Hero,Sales,Help,Billing,Address,Phone,Hours,WhatsApp,Map,CTA
7|Cybersecurity, Privacy & Risk Protection|cybersecurity|Home:Hero,Threats,Exposure,Promise,Services,Risk,Proof,Compliance,Questions,CTA;Firm:Hero,Story,Ethics,Team,Credentials,Methods,Tools,Privacy,Trust,CTA;Services:Hero,Testing,Monitoring,Training,Advisory,Response,Deliverables,Benefits,Scope,CTA;Risk:Hero,Overview,People,Systems,Data,Vendors,Access,Priorities,Matrix,CTA;Compliance:Hero,Regulation,GDPR,LGPD,ISO,SOC,Policies,Evidence,Reporting,CTA;Process:Hero,Discovery,Scope,Testing,Findings,Remediation,Verification,Reporting,Monitoring,CTA;Response:Hero,Incident,Triage,Containment,Investigation,Recovery,Reporting,Lessons,Prevention,CTA;Pricing:Hero,Audits,Retainers,Response,Training,Scope,Deliverables,Comparison,Terms,CTA;Insights:Hero,Threats,Guides,Checklists,Privacy,Compliance,Training,Resources,Alerts,CTA;Contact:Hero,Secure,Emergency,Audit,Sales,Form,Confidentiality,Response,Details,CTA
8|Data, Analytics & Business Intelligence|data-analytics|Home:Hero,Problem,Blindspots,Promise,Dashboards,Services,Proof,Tools,Questions,CTA;Company:Hero,Story,Analysts,Standards,Ethics,Tools,Method,Fit,Trust,CTA;Services:Hero,Tracking,BI,Reporting,Governance,Training,Maintenance,Benefits,Scope,CTA;Dashboards:Hero,Executive,Sales,Marketing,Finance,Operations,KPIs,Examples,Benefits,CTA;Strategy:Hero,Maturity,Sources,Metrics,Models,Governance,Ownership,Roadmap,Priorities,CTA;Process:Hero,Audit,Mapping,Tracking,Modelling,Visualisation,Testing,Training,Iteration,CTA;Results:Hero,Visibility,Decisions,Revenue,Savings,Cases,Metrics,Reviews,Proof,CTA;Pricing:Hero,Setup,Dashboards,Reporting,Retainers,Training,Addons,Comparison,Terms,CTA;Tools:Hero,Stack,GA4,Looker,PowerBI,SQL,CRM,Integrations,Advice,CTA;Contact:Hero,Audit,Dashboard,Training,Quote,Form,Phone,Response,Submit,CTA
9|Finance, Banking & Financial Services|finance|Home:Hero,Goals,Risk,Promise,Services,Advice,Proof,Results,Questions,CTA;Firm:Hero,Regulation,Advisors,Standards,Independence,Credentials,Values,Security,Trust,CTA;Services:Hero,Planning,Lending,Wealth,Protection,Business,Benefits,Suitability,Scope,CTA;Advice:Hero,Personal,Business,Investment,Risk,Recommendations,Tools,Reviews,Action,CTA;Markets:Hero,Context,Rates,Trends,Products,Commentary,Risk,Opportunities,Disclaimer,CTA;Results:Hero,Outcomes,Savings,Growth,Protection,Cases,Reviews,Metrics,Notes,CTA;Pricing:Hero,Fees,Consults,Advisory,Retainers,Products,Inclusions,Comparison,Terms,CTA;Resources:Hero,Guides,Calculators,Reports,Checklists,Glossary,Downloads,Newsletter,Topics,CTA;Questions:Hero,Eligibility,Documents,Fees,Risk,Regulation,Timelines,Security,Support,CTA;Contact:Hero,Appointment,Form,Documents,Phone,Office,Routing,Response,Submit,CTA
10|Insurance, Protection & Risk Cover|insurance|Home:Hero,Protection,Risk,Promise,Cover,Claims,Proof,Reviews,Questions,CTA;Broker:Hero,Independence,Partners,Standards,Team,Values,Regulation,Experience,Trust,CTA;Cover:Hero,Overview,Life,Health,Business,Property,Vehicle,Exclusions,Suitability,CTA;Claims:Hero,Stress,Report,Evidence,Review,Approval,Payout,Support,Timelines,CTA;Advice:Hero,Gaps,Personal,Family,Business,Recommendations,Review,Updates,Questions,CTA;Compare:Hero,Choice,Coverage,Limits,Excess,Exclusions,Cost,Fit,Warnings,CTA;Pricing:Hero,Premiums,Age,Assets,Risk,Excess,Discounts,Payments,Terms,CTA;Resources:Hero,Guides,Checklists,Explainers,Claims,Risk,Downloads,Articles,Learn,CTA;Questions:Hero,Eligibility,Documents,Claims,Payments,Cancellations,Exclusions,Support,Contact,CTA;Contact:Hero,Quote,Claims,Support,Upload,Phone,Office,Hours,Submit,CTA
11|Legal, Compliance & Immigration Services|legal|Home:Hero,Problem,Risk,Promise,Services,Process,Trust,Cases,Questions,CTA;Firm:Hero,Credentials,Jurisdictions,Team,Values,Standards,Privacy,Experience,Trust,CTA;Services:Hero,Areas,Legal,Compliance,Immigration,Advisory,Documents,Representation,Scope,CTA;Cases:Hero,Types,Individuals,Families,Companies,Documents,Requirements,Timelines,Risks,CTA;Process:Hero,Assessment,Strategy,Review,Filing,Representation,Updates,Followup,Closure,CTA;Results:Hero,Outcomes,Testimonials,Summaries,Factors,Limits,Privacy,Proof,Disclaimer,CTA;Pricing:Hero,Models,Fixed,Hourly,Packages,Inclusions,Extras,Payments,Terms,CTA;Resources:Hero,Guides,Updates,Checklists,Documents,Explainers,Downloads,Articles,Learn,CTA;Questions:Hero,Eligibility,Documents,Timelines,Fees,Risks,Privacy,Policies,Support,CTA;Contact:Hero,Consultation,Upload,Phone,Office,Notes,Response,Emergency,Submit,CTA
12|Accounting, Tax & Financial Administration|accounting|Home:Hero,Disorder,Risk,Promise,Services,Flow,Proof,Deadlines,Questions,CTA;Practice:Hero,Accuracy,Team,Tools,Standards,Security,Values,Experience,Trust,CTA;Services:Hero,Bookkeeping,Reports,Advisory,Filing,Admin,Software,Benefits,Scope,CTA;Tax:Hero,Needs,Planning,Returns,Compliance,Deadlines,Documents,Risk,Updates,CTA;Payroll:Hero,Problem,Salaries,Benefits,Deductions,Reporting,Compliance,Support,Timelines,CTA;Process:Hero,Onboarding,Setup,Monthly,Review,Reporting,Filing,Advisory,Improvements,CTA;Pricing:Hero,Plans,Starter,Business,Advisory,Addons,Inclusions,Comparison,Terms,CTA;Resources:Hero,Calendars,Templates,Checklists,Guides,Software,Deadlines,Downloads,Learn,CTA;Questions:Hero,Documents,Software,Deadlines,Fees,Payroll,Tax,Security,Support,CTA;Contact:Hero,Quote,Documents,Consultation,Phone,Email,Office,Response,Submit,CTA
13|Consulting, Strategy & Business Advisory|consulting|Home:Hero,Challenge,Gap,Promise,Services,Process,Results,Trust,Questions,CTA;Firm:Hero,Expertise,Method,Values,Team,Fit,Standards,Experience,Trust,CTA;Services:Hero,Advisory,Strategy,Operations,Growth,Transformation,Workshops,Retainers,Benefits,CTA;Strategy:Hero,Market,Positioning,Priorities,Roadmap,Execution,Measurement,Risks,Alignment,CTA;Process:Hero,Diagnose,Analyse,Design,Execute,Measure,Adjust,Transfer,Sustain,CTA;Results:Hero,Revenue,Efficiency,Clarity,Metrics,Reviews,Before,Lessons,Proof,CTA;Pricing:Hero,Workshops,Projects,Retainers,Scope,Inclusions,Comparison,Fit,Terms,CTA;Insights:Hero,Frameworks,Reports,Trends,Analysis,Leadership,Growth,Downloads,Articles,CTA;Cases:Hero,Problem,Context,Approach,Execution,Outcome,Metrics,Lessons,Testimonial,CTA;Contact:Hero,Brief,Call,Budget,Timeline,Fit,Proposal,Response,Submit,CTA
14|Education, Training & Learning Services|education|Home:Hero,Goal,Struggle,Promise,Courses,Method,Results,Proof,Questions,CTA;School:Hero,Mission,Standards,Community,Values,Philosophy,Teachers,Outcomes,Trust,CTA;Courses:Hero,Overview,Levels,Subjects,Formats,Outcomes,Schedule,Materials,Fit,CTA;Method:Hero,Diagnosis,Practice,Feedback,Correction,Review,Progress,Confidence,Independence,CTA;Results:Hero,Outcomes,Scores,Confidence,Testimonials,Stories,Progress,Proof,Expectations,CTA;Pricing:Hero,Lessons,Packages,Groups,Materials,Inclusions,Payments,Policies,Fit,CTA;Teachers:Hero,Team,Qualifications,Experience,Specialisms,Profiles,Style,Availability,Trust,CTA;Resources:Hero,Worksheets,Guides,Videos,Practice,Plans,Downloads,Topics,Learn,CTA;Questions:Hero,Level,Schedule,Homework,Materials,Payment,Cancellation,Progress,Support,CTA;Contact:Hero,Trial,Placement,Booking,WhatsApp,Email,Response,Steps,Submit,CTA
15|Recruitment, HR & Workplace Services|recruitment|Home:Hero,Workforce,Pressure,Promise,Services,Process,Results,Reviews,Questions,CTA;Agency:Hero,Specialisms,Values,Team,Market,Standards,Care,Experience,Trust,CTA;Hiring:Hero,Need,Brief,Search,Screening,Shortlist,Interviews,Offers,Onboarding,CTA;Talent:Hero,Goal,Opportunities,CV,Interviews,Matching,Advice,Process,Apply,CTA;Services:Hero,Recruitment,HR,Payroll,Training,Policy,Support,Benefits,Scope,CTA;Process:Hero,Brief,Search,Screen,Present,Interview,Select,Onboard,Review,CTA;Results:Hero,Placements,Retention,Speed,Employers,Candidates,Metrics,Reviews,Trust,CTA;Pricing:Hero,Contingency,Retainer,Project,HR,Terms,Comparison,Inclusions,Fit,CTA;Insights:Hero,Hiring,Culture,Leadership,HR,Candidates,Salaries,Guides,Trends,CTA;Contact:Hero,Employers,Candidates,Partners,Roles,Upload,Response,Steps,Submit,CTA
16|Real Estate, Property & Land Services|real-estate|Home:Hero,Goal,Market,Featured,Services,Areas,Proof,Reviews,Questions,CTA;Agency:Hero,Market,Team,Values,Reviews,Standards,Local,Experience,Trust,CTA;Properties:Hero,Search,Featured,Filters,Cards,Details,Gallery,Enquiry,Similar,CTA;Services:Hero,Sales,Lettings,Management,Valuation,Land,Investment,Benefits,Scope,CTA;Areas:Hero,Locations,Neighbourhoods,Prices,Lifestyle,Schools,Transport,Maps,Tips,CTA;Process:Hero,Valuation,Marketing,Viewings,Offers,Negotiation,Documents,Closing,Aftercare,CTA;Pricing:Hero,Fees,Commission,Management,Marketing,Inclusions,Comparison,Terms,Clarity,CTA;Resources:Hero,Buyers,Sellers,Landlords,Checklists,Reports,Documents,Downloads,Learn,CTA;Questions:Hero,Buying,Selling,Renting,Fees,Documents,Timelines,Legal,Support,CTA;Contact:Hero,Viewings,Valuation,Phone,Office,Hours,Map,Response,Submit,CTA
17|Construction, Building & Renovation|construction|Home:Hero,Vision,Problem,Promise,Services,Projects,Process,Proof,Questions,CTA;Company:Hero,Crew,Experience,Values,Certifications,Insurance,Standards,Reputation,Trust,CTA;Services:Hero,Newbuild,Renovation,Extension,Repair,Commercial,Residential,Benefits,Scope,CTA;Projects:Hero,Portfolio,Before,Residential,Commercial,Details,Materials,Results,Reviews,CTA;Process:Hero,Visit,Survey,Estimate,Planning,Build,Inspection,Handover,Aftercare,CTA;Materials:Hero,Quality,Suppliers,Finishes,Durability,Options,Sustainability,Maintenance,Guidance,CTA;Pricing:Hero,Factors,Labour,Materials,Timeline,Estimates,Allowances,Stages,Terms,CTA;Safety:Hero,Site,Insurance,Compliance,Crew,Risks,Documents,Cleanliness,Communication,CTA;Questions:Hero,Permits,Timelines,Disruption,Payments,Guarantees,Materials,Changes,Support,CTA;Contact:Hero,Project,Upload,Location,Budget,Visit,Phone,Response,Submit,CTA
18|Architecture, Planning & Built Environment|architecture|Home:Hero,Vision,Context,Promise,Projects,Services,Process,Awards,Questions,CTA;Studio:Hero,Philosophy,Team,Credentials,Values,Collaborators,Recognition,Approach,Trust,CTA;Projects:Hero,Portfolio,Residential,Commercial,Urban,Context,Response,Details,Outcomes,CTA;Services:Hero,Concept,Planning,Design,Documents,Interiors,Consultation,Deliverables,Scope,CTA;Process:Hero,Brief,Research,Concept,Planning,Detail,Coordination,Delivery,Handover,CTA;Planning:Hero,Need,Regulations,Applications,Drawings,Documents,Timelines,Risks,Approval,CTA;Pricing:Hero,Fees,Stages,Deliverables,Revisions,Consultants,Extras,Payments,Terms,CTA;Insights:Hero,Design,Planning,Sustainability,Materials,Urbanism,Cases,Journal,Ideas,CTA;Questions:Hero,Permissions,Timelines,Fees,Revisions,Role,Consultants,Documents,Support,CTA;Contact:Hero,Project,Site,Budget,Timeline,Consultation,Phone,Studio,Submit,CTA
19|Interiors, Furniture & Home Design|interiors|Home:Hero,Vision,Problem,Promise,Rooms,Projects,Shop,Reviews,Questions,CTA;Studio:Hero,Taste,Values,Signature,Team,Materials,Experience,Process,Trust,CTA;Services:Hero,Design,Styling,Sourcing,Installation,Colour,Layout,Deliverables,Fit,CTA;Rooms:Hero,Living,Kitchen,Bedroom,Bathroom,Office,Moodboards,Needs,Ideas,CTA;Projects:Hero,Portfolio,Before,Mood,Finishes,Furniture,Story,Results,Reviews,CTA;Shop:Hero,Collections,Furniture,Decor,Lighting,Textiles,Materials,Details,Enquiry,CTA;Pricing:Hero,Consultation,Design,Styling,Sourcing,Install,Inclusions,Comparison,Terms,CTA;Journal:Hero,Trends,Materials,Styling,Rooms,Seasons,Buying,Guides,Ideas,CTA;Questions:Hero,Timeline,Budget,Sourcing,Revisions,Purchases,Install,Remote,Support,CTA;Contact:Hero,Form,Photos,Budget,Style,Booking,Phone,Response,Submit,CTA
20|Manufacturing, Production & Industrial Operations|manufacturing|Home:Hero,Need,Capacity,Promise,Capabilities,Quality,Facilities,Industries,Questions,CTA;Factory:Hero,Company,Team,Values,History,Equipment,Standards,Scale,Trust,CTA;Capabilities:Hero,Fabrication,Assembly,Packaging,Machining,Finishing,Tolerances,Volumes,Specs,CTA;Industries:Hero,Markets,Automotive,Medical,Consumer,Industrial,Food,Requirements,Fit,CTA;Quality:Hero,System,Testing,Inspection,Traceability,Documents,Standards,Defects,Audits,CTA;Process:Hero,Brief,Drawings,Prototype,Production,QA,Packaging,Delivery,Review,CTA;Facilities:Hero,Tour,Equipment,Lines,Capacity,Storage,Safety,Maintenance,Photos,CTA;Compliance:Hero,Certifications,ISO,Standards,Audits,Documents,Policies,Verification,Governance,CTA;Resources:Hero,Datasheets,Specs,Guides,Tolerances,Materials,Downloads,Preparation,Library,CTA;Contact:Hero,RFQ,Drawings,Quantities,Timeline,Sales,Technical,Response,Submit,CTA
21|Engineering, Technical Systems & Specialist Services|engineering|Home:Hero,Challenge,Reliability,Promise,Services,Systems,Projects,Standards,Questions,CTA;Firm:Hero,Engineers,Standards,Credentials,Tools,Values,Safety,Experience,Trust,CTA;Services:Hero,Design,Testing,Maintenance,Diagnostics,Compliance,Support,Deliverables,Benefits,CTA;Systems:Hero,Types,Mechanical,Electrical,Control,Integration,Monitoring,Documents,Reliability,CTA;Projects:Hero,Portfolio,Specification,Execution,Validation,Results,Lessons,Metrics,Reviews,CTA;Process:Hero,Assess,Design,Model,Validate,Implement,Test,Document,Support,CTA;Expertise:Hero,Specialisms,Tools,Methods,Standards,Sectors,Credentials,Depth,Proof,CTA;Resources:Hero,Specs,Papers,Guides,Downloads,Standards,Maintenance,Library,Learn,CTA;Questions:Hero,Scope,Timelines,Compliance,Documents,Sitework,Maintenance,Pricing,Support,CTA;Contact:Hero,Enquiry,Upload,Scope,Call,Proposal,Engineer,Response,Submit,CTA
22|Energy, Power & Renewable Solutions|energy|Home:Hero,Problem,Cost,Promise,Solutions,Savings,Projects,Trust,Questions,CTA;Company:Hero,Mission,Values,Team,Partners,Certifications,Standards,Sustainability,Trust,CTA;Solutions:Hero,Solar,Storage,Efficiency,Monitoring,Backup,Commercial,Residential,Benefits,CTA;Services:Hero,Audit,Design,Install,Maintain,Monitor,Support,Compliance,Scope,CTA;Savings:Hero,Bills,Payback,Incentives,Finance,Value,Assumptions,Calculator,Review,CTA;Projects:Hero,Installations,Residential,Commercial,Industrial,Output,Before,Metrics,Reviews,CTA;Pricing:Hero,Equipment,Labour,Finance,Packages,Maintenance,Inclusions,Comparison,Terms,CTA;Resources:Hero,Guides,Incentives,Maintenance,Solar,Batteries,Downloads,Questions,Learn,CTA;FAQ:Hero,Connection,Warranty,Output,Finance,Weather,Permissions,Service,Support,CTA;Contact:Hero,Site,Bill,Consultation,Address,Phone,Response,Quote,Submit,CTA
23|Utilities, Water & Essential Infrastructure|utilities|Home:Hero,Need,Reliability,Access,Network,Safety,Updates,Trust,Questions,CTA;Authority:Hero,Organisation,Governance,Value,Team,Standards,Responsibility,Community,Trust,CTA;Services:Hero,Water,Waste,Power,Maintenance,Requests,Applications,Benefits,Access,CTA;Network:Hero,Assets,Plants,Systems,Capacity,Monitoring,Upgrades,Maps,Reliability,CTA;Safety:Hero,Standards,Monitoring,Compliance,Emergency,Risk,Reporting,Training,Public,CTA;Projects:Hero,Work,Planning,Delivery,Maintenance,Impact,Timelines,Updates,Results,CTA;Support:Hero,Faults,Billing,Requests,Complaints,Response,Escalation,Guides,Contact,CTA;Reports:Hero,Quality,Performance,Sustainability,Compliance,Downloads,Method,Updates,Archive,CTA;FAQ:Hero,Access,Billing,Faults,Rules,Documents,Requests,Complaints,Emergency,CTA;Contact:Hero,Emergency,Service,Admin,Offices,Hours,Phone,Email,Map,CTA
24|Environmental, Sustainability & Climate Services|environmental|Home:Hero,Challenge,Risk,Promise,Services,Impact,Projects,Trust,Questions,CTA;Mission:Hero,Experts,Ethics,Method,Values,Partners,Evidence,Purpose,Trust,CTA;Services:Hero,Audits,Carbon,ESG,Reporting,Strategy,Compliance,Training,Deliverables,CTA;Impact:Hero,Areas,Emissions,Waste,Water,Biodiversity,Social,Metrics,Targets,CTA;Strategy:Hero,Baseline,Roadmap,Governance,Targets,Implementation,Measurement,Reporting,Improvement,CTA;Projects:Hero,Challenge,Intervention,Actions,Metrics,Outcomes,Lessons,Reporting,Proof,CTA;Reports:Hero,ESG,Carbon,Compliance,Methodology,Data,Downloads,Archive,Verification,CTA;Resources:Hero,Guides,Checklists,Toolkits,Regulation,Education,Downloads,Articles,Learn,CTA;FAQ:Hero,Standards,Data,Cost,Timelines,Reporting,Compliance,Audits,Support,CTA;Contact:Hero,Audit,Advisory,Partnership,Organisation,Timeline,Response,Submit,CTA
25|Agriculture, Farming & Rural Business|agriculture|Home:Hero,Need,Yield,Promise,Services,Products,Advice,Trust,Questions,CTA;Farm:Hero,Heritage,Region,Team,Values,Knowledge,Suppliers,Community,Trust,CTA;Services:Hero,Planning,Supply,Maintenance,Advisory,Seasonal,Visits,Benefits,Scope,CTA;Products:Hero,Inputs,Equipment,Seeds,Feed,Tools,Specs,Uses,Availability,CTA;Land:Hero,Soil,Water,Crops,Livestock,Improvement,Monitoring,Sustainability,Planning,CTA;Advice:Hero,Productivity,Compliance,Finance,Seasonality,Risk,Recommendations,Plan,Support,CTA;Pricing:Hero,Fees,Ranges,Packages,Delivery,Bulk,Terms,Quote,Payment,CTA;Resources:Hero,Seasonal,Crops,Livestock,Compliance,Checklists,Downloads,Updates,Learn,CTA;Questions:Hero,Delivery,Seasonality,Fit,Visits,Support,Payment,Returns,Advice,CTA;Contact:Hero,Visit,Order,Advice,Location,Phone,WhatsApp,Hours,Submit,CTA
26|Food Production, Packaged Goods & Consumer Foods|food-production|Home:Hero,Promise,Taste,Quality,Products,Story,Stockists,Reviews,Questions,CTA;Brand:Hero,Origin,Makers,Mission,Values,Process,Sustainability,Recognition,Trust,CTA;Products:Hero,Range,Flavours,Sizes,Ingredients,Nutrition,Allergens,Pairings,Reviews,CTA;Quality:Hero,Sourcing,Production,Testing,Safety,Certifications,Packaging,Traceability,Standards,CTA;Story:Hero,Heritage,Inspiration,Craft,People,Locality,Values,Milestones,Identity,CTA;Stockists:Hero,Retailers,Regions,Map,Online,Availability,Trade,Updates,Find,CTA;Recipes:Hero,Ideas,Pairings,Ingredients,Steps,Occasions,Products,Tips,Related,CTA;Wholesale:Hero,Trade,Distribution,Bulk,Retail,Packaging,Margins,Requirements,Process,CTA;Questions:Hero,Ingredients,Allergens,Storage,Shipping,Stock,Wholesale,Returns,Support,CTA;Contact:Hero,Retail,Wholesale,Press,Support,Form,Social,Response,Submit,CTA
27|Restaurants, Cafes & Food Service|restaurant|Home:Hero,Mood,Food,Menu,Booking,Gallery,Reviews,Location,Questions,CTA;Story:Hero,Chef,Ingredients,Values,Atmosphere,Team,Locality,Heritage,Trust,CTA;Menu:Hero,Overview,Starters,Mains,Desserts,Drinks,Specials,Allergens,Prices,CTA;Booking:Hero,Reservations,Dates,Groups,Policies,Confirmation,Requests,Reminders,Questions,CTA;Events:Hero,Private,Corporate,Catering,Menus,Capacity,Styling,Packages,Proof,CTA;Gallery:Hero,Food,Interior,People,Events,Details,Mood,Social,Instagram,CTA;Delivery:Hero,Takeaway,Platforms,Menu,Timing,Packaging,Collection,Area,Policies,CTA;Offers:Hero,Lunch,Seasonal,Loyalty,Happyhour,Groups,Conditions,Expiry,Signup,CTA;FAQ:Hero,Allergens,Parking,Children,Groups,Reservations,Delivery,Payments,Policies,CTA;Contact:Hero,Address,Hours,Phone,WhatsApp,Map,Transport,Socials,Reserve,CTA
28|Hospitality, Hotels & Guest Accommodation|hotel|Home:Hero,Stay,Location,Rooms,Amenities,Experiences,Offers,Reviews,Questions,CTA;Hotel:Hero,Story,Hospitality,Standards,Team,Design,Locality,Care,Trust,CTA;Rooms:Hero,Types,Features,Views,Rates,Availability,Amenities,Gallery,Policies,CTA;Amenities:Hero,Facilities,Dining,Spa,Pool,Workspace,Family,Access,Details,CTA;Experiences:Hero,Local,Romantic,Family,Business,Wellness,Seasonal,Packages,Tips,CTA;Offers:Hero,Seasonal,Longstay,Weekend,Romance,Business,Conditions,Availability,Savings,CTA;Booking:Hero,Dates,Guests,Rooms,Addons,Policies,Payment,Confirmation,Help,CTA;Gallery:Hero,Rooms,Lobby,Food,Views,Pool,Experiences,Details,Atmosphere,CTA;FAQ:Hero,Checkin,Parking,Pets,Cancellation,Breakfast,Access,Family,Payments,CTA;Contact:Hero,Address,Phone,Email,Map,Transport,Reception,Socials,Submit,CTA
29|Travel, Tourism & Destination Experiences|travel|Home:Hero,Dream,Destination,Promise,Trips,Tours,Planning,Stories,Questions,CTA;Agency:Hero,Story,Philosophy,Team,Partners,Responsibility,Safety,Values,Trust,CTA;Trips:Hero,Types,Adventure,Culture,Luxury,Family,Dates,Inclusions,Fit,CTA;Places:Hero,Destinations,Regions,Highlights,Seasons,Maps,Notes,Recommendations,Related,CTA;Tours:Hero,Activities,Levels,Durations,Guides,Inclusions,Safety,Groups,Reviews,CTA;Planning:Hero,Consultation,Customisation,Budget,Booking,Documents,Visas,Support,Timeline,CTA;Pricing:Hero,Packages,Quotes,Deposits,Inclusions,Exclusions,Payment,Terms,Clarity,CTA;Stories:Hero,Stories,Photos,Guides,Testimonials,Itineraries,Tips,Inspiration,Related,CTA;FAQ:Hero,Visas,Safety,Weather,Payments,Cancellations,Insurance,Access,Support,CTA;Contact:Hero,Destination,Dates,Budget,Travellers,Call,Response,Submit,CTA
30|Transport, Mobility & Passenger Services|transport|Home:Hero,Need,Safety,Promise,Services,Routes,Fleet,Reviews,Questions,CTA;Company:Hero,Drivers,Vehicles,Standards,Reliability,Insurance,Values,Experience,Trust,CTA;Services:Hero,Private,Corporate,Shuttle,Accessible,Airport,Events,Benefits,Scope,CTA;Routes:Hero,Areas,Airports,Cities,Timetables,Maps,Popular,Availability,Updates,CTA;Fleet:Hero,Types,Capacity,Comfort,Access,Maintenance,Features,Safety,Gallery,CTA;Booking:Hero,Pickup,Destination,Passengers,Date,Addons,Payment,Confirmation,Changes,CTA;Pricing:Hero,Fares,Distance,Time,Packages,Extras,Business,Terms,Estimate,CTA;Safety:Hero,Drivers,Vehicles,Insurance,Cleanliness,Policies,Monitoring,Emergency,Trust,CTA;FAQ:Hero,Luggage,Delays,Changes,Cancellations,Payments,Access,Waiting,Support,CTA;Contact:Hero,Booking,Business,Support,Phone,WhatsApp,Hours,Response,Submit,CTA
31|Logistics, Delivery & Supply Chain|logistics|Home:Hero,Challenge,Visibility,Promise,Services,Network,Tracking,Proof,Questions,CTA;Company:Hero,Fleet,Hubs,Standards,Technology,Team,Reliability,Scale,Trust,CTA;Services:Hero,Freight,Storage,Lastmile,Fulfilment,Express,International,Benefits,Scope,CTA;Network:Hero,Regions,Hubs,Partners,Capacity,Maps,Levels,Expansion,Reliability,CTA;Tracking:Hero,Status,Alerts,ETA,Proof,Exceptions,Documents,Portal,Support,CTA;Industries:Hero,Retail,Food,Industrial,Medical,Commerce,Requirements,Solutions,Fit,CTA;Pricing:Hero,Rates,Weight,Distance,Speed,Contracts,Volume,Addons,Terms,CTA;Support:Hero,Claims,Delays,Documents,Pickup,Delivery,Escalation,Help,Contact,CTA;FAQ:Hero,Pickup,Delivery,Insurance,Restrictions,Packaging,Payments,Tracking,Support,CTA;Contact:Hero,Quote,Volume,Locations,Timeline,Sales,Support,Response,Submit,CTA
32|Automotive, Vehicles & Mobility Products|automotive|Home:Hero,Desire,Featured,Services,Finance,Workshop,Offers,Reviews,Questions,CTA;Dealer:Hero,Brands,Team,Standards,Reviews,Facilities,Values,Experience,Trust,CTA;Vehicles:Hero,Inventory,New,Used,Electric,Specs,Photos,Availability,Compare,CTA;Services:Hero,Sales,Leasing,Maintenance,Tradein,Fleet,Advice,Benefits,Scope,CTA;Finance:Hero,Options,Loans,Leasing,Tradein,Eligibility,Calculator,Documents,Terms,CTA;Workshop:Hero,Repairs,Servicing,Diagnostics,Tyres,Warranty,Booking,Tips,Proof,CTA;Offers:Hero,Deals,Finance,Service,Seasonal,Tradein,Packages,Terms,Savings,CTA;Parts:Hero,Accessories,Tyres,Genuine,Compatibility,Ordering,Installation,Availability,Help,CTA;FAQ:Hero,Warranty,Testdrive,Documents,Finance,Booking,Tradein,Service,Support,CTA;Contact:Hero,Testdrive,Service,Sales,Location,Hours,Phone,Map,Submit,CTA
33|Aviation, Aerospace & Air Services|aviation|Home:Hero,Need,Safety,Promise,Services,Fleet,Operations,Compliance,Questions,CTA;Company:Hero,Leadership,Values,Credentials,Experience,Team,Standards,Reputation,Trust,CTA;Services:Hero,Charter,Maintenance,Training,Ground,Technical,Missions,Benefits,Scope,CTA;Fleet:Hero,Aircraft,Capacity,Range,Specs,Interiors,Availability,Maintenance,Gallery,CTA;Safety:Hero,Culture,Training,Audits,Maintenance,Risk,Certification,Procedures,Trust,CTA;Operations:Hero,Routes,Scheduling,Ground,Control,Logistics,Weather,Communication,Reliability,CTA;Compliance:Hero,Authorities,Documents,Audits,Records,Standards,Approvals,Governance,Evidence,CTA;Projects:Hero,Aerospace,Engineering,Logistics,Mission,Outcomes,Notes,Metrics,Proof,CTA;Careers:Hero,Roles,Pilots,Engineers,Operations,Requirements,Culture,Benefits,Apply,CTA;Contact:Hero,Charter,Technical,Partners,Details,Route,Phone,Response,Submit,CTA
34|Maritime, Shipping & Marine Services|maritime|Home:Hero,Need,Capacity,Promise,Services,Fleet,Ports,Tracking,Questions,CTA;Company:Hero,Experience,Crew,Certifications,Values,Standards,Partners,Reputation,Trust,CTA;Services:Hero,Shipping,Charter,Repair,Agency,Cargo,Ports,Benefits,Scope,CTA;Fleet:Hero,Vessels,Capacity,Routes,Specs,Equipment,Availability,Maintenance,Gallery,CTA;Ports:Hero,Locations,Facilities,Partners,Schedules,Routes,Documents,Notes,Maps,CTA;Safety:Hero,Crew,Vessel,Cargo,Emergency,Compliance,Training,Audits,Trust,CTA;Tracking:Hero,ETA,Documents,Status,Exceptions,Alerts,Proof,Support,Track,CTA;Pricing:Hero,Cargo,Route,Level,Fees,Contracts,Addons,Terms,Quote,CTA;Support:Hero,Claims,Delays,Documents,Customs,Escalation,Routes,Help,Contact,CTA;Contact:Hero,Cargo,Vessel,Port,Details,Sales,Response,Submit,CTA
35|Retail, Shops & Consumer Sales|retail|Home:Hero,Promise,Featured,Categories,Offers,Stores,Reviews,Story,Questions,CTA;Brand:Hero,Story,Taste,Values,Team,Quality,Community,Recognition,Trust,CTA;Shop:Hero,Categories,Collections,Bestsellers,New,Filters,Cards,Recommendations,Cart,CTA;Products:Hero,Range,Features,Materials,Uses,Details,Reviews,Related,Stock,CTA;Offers:Hero,Promotions,Bundles,Seasonal,Clearance,Perks,Conditions,Expiry,Featured,CTA;Stores:Hero,Locations,Hours,Services,Map,Parking,Events,Stock,Visit,CTA;Loyalty:Hero,Rewards,Points,Tiers,Benefits,Rules,Signup,Offers,Questions,CTA;Journal:Hero,Guides,Trends,Howto,Inspiration,Tips,Gifts,Products,Read,CTA;FAQ:Hero,Returns,Delivery,Payment,Stock,Loyalty,Stores,Care,Support,CTA;Contact:Hero,Store,Online,Wholesale,Phone,Email,Map,Hours,Submit,CTA
36|E-commerce, Marketplaces & Digital Commerce|ecommerce|Home:Hero,Promise,Featured,Categories,Deals,Trust,Sellers,Reviews,Questions,CTA;Market:Hero,Mission,Sellers,Standards,Quality,Payments,Security,Scale,Trust,CTA;Shop:Hero,Catalogue,New,Popular,Filters,Cards,Reviews,Recommendations,Checkout,CTA;Categories:Hero,Main,Sub,Collections,Trending,Seasonal,Recommendations,Filters,Browse,CTA;Deals:Hero,Discounts,Bundles,Limited,Flash,Conditions,Expiry,Products,Savings,CTA;Sellers:Hero,Benefits,Requirements,Fees,Onboarding,Setup,Standards,Support,Apply,CTA;Support:Hero,Orders,Returns,Delivery,Refunds,Tickets,Help,Policies,Contact,CTA;Account:Hero,Orders,Details,Preferences,Security,Addresses,Wishlist,Payments,Help,CTA;FAQ:Hero,Shipping,Refunds,Payments,Sellers,Accounts,Delivery,Returns,Support,CTA;Contact:Hero,Customer,Seller,Press,Partnership,Routing,Response,Submit,CTA
37|Fashion, Apparel & Accessories|fashion|Home:Hero,Mood,Collection,Promise,Shop,Lookbook,Craft,Reviews,Questions,CTA;Brand:Hero,Story,Inspiration,Craft,Values,Materials,Founder,Recognition,Trust,CTA;Shop:Hero,Apparel,Accessories,New,Filters,Cards,Styling,Reviews,Cart,CTA;Lines:Hero,Collections,Campaign,Pieces,Materials,Styling,Season,Details,Looks,CTA;Lookbook:Hero,Mood,Outfits,Details,Movement,Accessories,Links,Inspiration,Shop,CTA;Stores:Hero,Locations,Stockists,Hours,Map,Services,Events,Availability,Visit,CTA;Sizing:Hero,Charts,Measurements,Fit,Care,Returns,Models,Questions,Help,CTA;Journal:Hero,Trends,Styling,Behindscenes,Craft,Materials,Interviews,Products,Read,CTA;FAQ:Hero,Shipping,Returns,Materials,Sizing,Care,Stock,Orders,Support,CTA;Contact:Hero,Orders,Press,Wholesale,Styling,Phone,Email,Response,Submit,CTA
38|Beauty, Cosmetics & Aesthetic Products|beauty|Home:Hero,Goal,Concerns,Promise,Shop,Routine,Results,Reviews,Questions,CTA;Brand:Hero,Philosophy,Testing,Values,Sustainability,Formulation,Trust,Recognition,Safety,CTA;Shop:Hero,Skincare,Makeup,Haircare,Bundles,Filters,Cards,Reviews,Cart,CTA;Products:Hero,Benefits,Texture,Usage,Ingredients,Types,Reviews,Related,Questions,CTA;Routine:Hero,Finder,Morning,Night,Type,Steps,Match,Tips,Consistency,CTA;Ingredients:Hero,Actives,Benefits,Safety,Claims,Sources,Formulation,Avoidance,Education,CTA;Results:Hero,Before,Reviews,Testimonials,Expectations,Timeframes,Disclaimer,Proof,Shop,CTA;Tutorials:Hero,Application,Tips,Videos,Routines,Links,Mistakes,Experts,Watch,CTA;FAQ:Hero,Types,Allergies,Returns,Usage,Pregnancy,Shipping,Orders,Support,CTA;Contact:Hero,Orders,Advice,Wholesale,Press,Form,Social,Response,Submit,CTA
39|Media, Broadcasting & Digital Content|media|Home:Hero,Promise,Featured,Shows,Schedule,Audience,Advertise,Trust,Questions,CTA;Network:Hero,Mission,Team,Standards,Audience,Reach,Values,Voice,Trust,CTA;Shows:Hero,Programs,Episodes,Hosts,Topics,Archive,Clips,Schedule,Watch,CTA;Content:Hero,Video,Audio,Articles,Categories,Featured,Latest,Popular,Related,CTA;Schedule:Hero,Programming,Days,Times,Live,Reminders,Events,Updates,Subscribe,CTA;Advertise:Hero,Audience,Formats,Packages,Metrics,Campaigns,Proof,Kit,Contact,CTA;Press:Hero,Kit,Logos,Bios,Releases,Photos,Mentions,Media,Download,CTA;Careers:Hero,Roles,Culture,Internships,Departments,Requirements,Benefits,Steps,Apply,CTA;FAQ:Hero,Access,Submissions,Advertising,Rights,Accounts,Usage,Support,Contact,CTA;Contact:Hero,Editorial,Advertising,Support,Press,Form,Routing,Response,Submit,CTA
40|Entertainment, Music & Performance|entertainment|Home:Hero,Hook,Upcoming,Artists,Tickets,Media,Reviews,Energy,Questions,CTA;Venue:Hero,Story,Stage,Sound,Team,Values,Facilities,Reputation,Trust,CTA;Shows:Hero,Calendar,Featured,Genres,Artists,Tickets,Times,Details,Book,CTA;Artists:Hero,Lineup,Profiles,Music,Videos,Dates,Socials,Press,Discover,CTA;Tickets:Hero,Options,Seating,Pricing,Access,Terms,Delivery,Questions,Buy,CTA;Private:Hero,Events,Hire,Capacity,Packages,Production,Catering,Proof,Enquire,CTA;Gallery:Hero,Photos,Videos,Stage,Crowd,Details,Press,Socials,View,CTA;News:Hero,Updates,Releases,Announcements,Features,Interviews,Archive,Read,Subscribe,CTA;FAQ:Hero,Entry,Age,Access,Refunds,Parking,Security,Timing,Support,CTA;Contact:Hero,Booking,Press,Venue,Partnerships,Phone,Form,Response,Submit,CTA
41|Publishing, Information & Knowledge Platforms|publishing|Home:Hero,Promise,Topics,Featured,Archive,Authors,Newsletter,Trust,Questions,CTA;Platform:Hero,Mission,Editorial,Standards,Team,Values,Sources,Governance,Trust,CTA;Library:Hero,Categories,Search,Featured,Recent,Popular,Filters,Access,Explore,CTA;Articles:Hero,Latest,Analysis,Guides,Opinion,Research,Authors,Related,Read,CTA;Authors:Hero,Experts,Profiles,Credentials,Topics,Contributions,Interviews,Socials,Follow,CTA;Reports:Hero,Research,Data,Downloads,Methodology,Findings,Sources,Archive,Access,CTA;Newsletter:Hero,Promise,Topics,Frequency,Samples,Benefits,Form,Archive,Subscribe,CTA;Submissions:Hero,Guidelines,Topics,Review,Standards,Rights,Process,Timeline,Submit,CTA;FAQ:Hero,Access,Sources,Rights,Submissions,Corrections,Accounts,Support,Contact,CTA;Contact:Hero,Editorial,Submissions,Partnerships,Press,Form,Routing,Response,Submit,CTA
42|Marketing, Advertising & Communications|marketing|Home:Hero,Problem,Positioning,Promise,Services,Work,Results,Trust,Questions,CTA;Agency:Hero,Team,Culture,Values,Standards,Fit,Recognition,Experience,Trust,CTA;Services:Hero,Branding,Campaigns,Content,Ads,Communications,Social,Deliverables,Benefits,CTA;Work:Hero,Portfolio,Campaigns,Brands,Websites,Direction,Outcomes,Metrics,Reviews,CTA;Strategy:Hero,Audience,Message,Channels,Funnel,KPIs,Roadmap,Testing,Alignment,CTA;Process:Hero,Discover,Plan,Create,Launch,Measure,Optimise,Report,Scale,CTA;Results:Hero,Leads,Sales,Reach,Lift,Metrics,Reviews,Before,Proof,CTA;Pricing:Hero,Projects,Retainers,Campaigns,Scope,Inclusions,Comparison,Fit,Terms,CTA;Insights:Hero,Trends,Guides,Frameworks,Analysis,Campaigns,Tips,Downloads,Read,CTA;Contact:Hero,Brief,Budget,Timeline,Goals,Call,Proposal,Response,Submit,CTA
43|Creative, Design & Visual Production|creative|Home:Hero,Positioning,Problem,Promise,Work,Services,Process,Recognition,Questions,CTA;Studio:Hero,Philosophy,Team,Taste,Influences,Standards,Clients,Reputation,Trust,CTA;Work:Hero,Portfolio,Branding,Photo,Video,Digital,Details,Outcomes,Reviews,CTA;Services:Hero,Identity,Production,Direction,Design,Content,Campaigns,Deliverables,Fit,CTA;Process:Hero,Brief,Concept,Production,Refinement,Delivery,Files,Usage,Aftercare,CTA;Journal:Hero,Trends,Notes,Cases,Inspiration,Tools,Behind,Ideas,Read,CTA;Pricing:Hero,Identity,Campaigns,Retainers,Inclusions,Revisions,Usage,Terms,Quote,CTA;Shop:Hero,Templates,Prints,Assets,Licenses,Details,Usage,Downloads,Buy,CTA;FAQ:Hero,Revisions,Files,Timelines,Usage,Payments,Ownership,Delivery,Support,CTA;Contact:Hero,Project,Timeline,Budget,Style,Uploads,Response,Submit,CTA
44|Sports, Fitness & Recreation|sports|Home:Hero,Goal,Barrier,Promise,Programs,Classes,Results,Community,Questions,CTA;Club:Hero,Philosophy,Community,Facilities,Coaches,Standards,Values,Energy,Trust,CTA;Programs:Hero,Beginner,Performance,Recovery,Weight,Strength,Plans,Outcomes,Fit,CTA;Classes:Hero,Group,Private,Online,Levels,Timetable,Equipment,Benefits,Booking,CTA;Coaches:Hero,Team,Qualifications,Specialisms,Profiles,Style,Availability,Reviews,Meet,CTA;Results:Hero,Transformations,Stories,Metrics,Reviews,Consistency,Expectations,Proof,Motivation,CTA;Pricing:Hero,Memberships,Packages,Dropin,Training,Inclusions,Terms,Comparison,Join,CTA;Schedule:Hero,Timetable,Days,Times,Locations,Booking,Reminders,Capacity,Updates,CTA;FAQ:Hero,Level,Equipment,Injuries,Policies,Payments,Cancellations,Trial,Support,CTA;Contact:Hero,Trial,Membership,Phone,Location,Hours,Map,Response,Submit,CTA
45|Events, Weddings & Experience Production|events|Home:Hero,Vision,Emotion,Promise,Services,Portfolio,Process,Reviews,Questions,CTA;Studio:Hero,Style,Team,Values,Suppliers,Standards,Recognition,Taste,Trust,CTA;Services:Hero,Planning,Styling,Production,Coordination,Suppliers,Guests,Deliverables,Fit,CTA;Weddings:Hero,Dream,Ceremony,Reception,Styling,Timeline,Suppliers,Packages,Proof,CTA;Events:Hero,Corporate,Private,Launches,Experiences,Production,Logistics,Outcomes,Enquiry,CTA;Portfolio:Hero,Galleries,Concepts,Details,Venues,Stories,Before,Reviews,Proof,CTA;Pricing:Hero,Packages,Custom,Addons,Deposits,Inclusions,Payment,Terms,Quote,CTA;Venues:Hero,Indoor,Outdoor,Destination,Capacity,Logistics,Styling,Recommendations,Explore,CTA;FAQ:Hero,Timeline,Budget,Suppliers,Deposits,Changes,Weather,Guests,Support,CTA;Contact:Hero,Date,Location,Guests,Type,Budget,Consultation,Response,Submit,CTA
46|Government, Public Sector & Civic Services|government|Home:Hero,Need,Access,Updates,Services,Forms,Support,Transparency,Questions,CTA;Council:Hero,Organisation,Governance,Departments,Leaders,Value,Standards,Access,Trust,CTA;Services:Hero,Applications,Payments,Requests,Eligibility,Documents,Timelines,Steps,Start,CTA;Offices:Hero,Departments,Duties,Contacts,Locations,Leaders,Functions,Hours,Visit,CTA;News:Hero,Announcements,Alerts,Consultations,Dates,Notices,Updates,Archive,Read,CTA;Forms:Hero,Permits,Requests,Registrations,Requirements,Downloads,Instructions,Submit,Start,CTA;Resources:Hero,Policies,Reports,Guides,Documents,Downloads,Search,Records,Learn,CTA;Support:Hero,Issues,Complaints,Requests,Escalation,Help,Response,Contact,Resolve,CTA;FAQ:Hero,Access,Documents,Rules,Payments,Applications,Offices,Complaints,Help,CTA;Contact:Hero,Phone,Email,Offices,Emergency,Hours,Map,Routing,Submit,CTA
47|Nonprofit, Charity & Social Impact|nonprofit|Home:Hero,Cause,Urgency,Promise,Impact,Programs,Donate,Stories,Questions,CTA;Organisation:Hero,Team,Board,Governance,Values,Partners,Transparency,History,Trust,CTA;Mission:Hero,Purpose,Vision,Values,Change,Goals,Principles,Impact,Support,CTA;Impact:Hero,Numbers,Outcomes,Reports,People,Community,Transparency,Proof,Donate,CTA;Programs:Hero,Overview,Education,Relief,Advocacy,Community,Activities,People,Join,CTA;Donate:Hero,Need,Onetime,Monthly,Corporate,Funds,Trust,Security,Give,CTA;Volunteer:Hero,Need,Roles,Skills,Time,Requirements,Training,Application,Join,CTA;Stories:Hero,People,Beneficiaries,Volunteers,Communities,Photos,Outcomes,Related,Read,CTA;Resources:Hero,Reports,Toolkits,Guides,Campaigns,Downloads,Share,Learn,Use,CTA;Contact:Hero,Donate,Volunteer,Partner,Media,Form,Response,Submit,CTA
48|Pets, Animals & Veterinary Services|veterinary|Home:Hero,Concern,Promise,Services,Emergency,Team,Reviews,Trust,Questions,CTA;Clinic:Hero,Values,Facilities,Standards,Team,Reviews,Welfare,Experience,Trust,CTA;Services:Hero,Checkups,Vaccines,Dental,Surgery,Diagnostics,Prevention,Benefits,Safety,CTA;Care:Hero,Prevention,Nutrition,Behaviour,Stages,Symptoms,Homecare,Advice,Support,CTA;Team:Hero,Vets,Nurses,Specialists,Profiles,Experience,Style,Availability,Meet,CTA;Pricing:Hero,Consults,Procedures,Packages,Insurance,Payments,Inclusions,Policies,Quote,CTA;Emergency:Hero,Symptoms,Steps,Call,Directions,Hours,Bring,Aftercare,Urgent,CTA;Resources:Hero,Guides,Aftercare,Prevention,Nutrition,Behaviour,Downloads,Advice,Learn,CTA;FAQ:Hero,Appointments,Vaccines,Surgery,Recovery,Payment,Insurance,Emergencies,Support,CTA;Contact:Hero,Booking,Phone,WhatsApp,Location,Hours,Map,Emergency,Submit,CTA
49|Luxury, Premium & High-End Services|luxury|Home:Hero,Promise,Exclusivity,Services,Experience,Portfolio,Discretion,Trust,Questions,CTA;House:Hero,Heritage,Founder,Recognition,Values,Craft,Standards,Taste,Trust,CTA;Maison:Hero,World,Taste,Philosophy,Signature,Materials,Rituals,Culture,Discover,CTA;Services:Hero,Bespoke,Concierge,Advisory,Sourcing,Access,Inclusions,Fit,Enquire,CTA;Experience:Hero,Personalisation,Detail,Privacy,Touchpoints,Rituals,Care,Aftercare,Feeling,CTA;Portfolio:Hero,Selected,Visuals,Details,Story,Outcome,Discretion,Recognition,View,CTA;Private:Hero,Invitation,Consultation,Criteria,Access,Privacy,Process,Response,Request,CTA;Journal:Hero,Culture,Design,Lifestyle,Craft,Travel,Objects,Essays,Read,CTA;Members:Hero,Membership,Levels,Benefits,Access,Criteria,Invitations,Application,Apply,CTA;Contact:Hero,Private,Appointment,Concierge,Location,Response,Privacy,Submit,CTA
50|Personal Brands, Creators & Public Figures|personal-brand|Home:Hero,Positioning,Authority,Work,Media,Speaking,Proof,Newsletter,Questions,CTA;Profile:Hero,Biography,Story,Values,Timeline,Expertise,Proof,Recognition,Trust,CTA;Work:Hero,Projects,Services,Collaborations,Highlights,Cases,Outcomes,Links,Featured,CTA;Media:Hero,Videos,Podcasts,Interviews,Features,Clips,Appearances,Socials,Watch,CTA;Speaking:Hero,Topics,Keynotes,Panels,Workshops,Audiences,Reviews,Requirements,Booking,CTA;Insights:Hero,Articles,Essays,Notes,Themes,Opinions,Resources,Related,Read,CTA;Press:Hero,Bio,Photos,Logos,Mentions,Kit,Downloads,Contact,Media,CTA;Newsletter:Hero,Promise,Topics,Frequency,Samples,Benefits,Form,Archive,Subscribe,CTA;Booking:Hero,Event,Collaboration,Interview,Requirements,Availability,Form,Response,Book,CTA;Contact:Hero,Business,Media,General,Socials,Management,Response,Submit,CTA
""".strip()


BRANDS = [
    "AsterCare", "HelixNova", "LumaStudio", "NexusOps", "OrbitDesk",
    "SignalNorth", "CipherWard", "PrismBI", "HarborLedger", "Shieldline",
    "CivicLex", "LedgerFlow", "VectorNorth", "BrightPath", "TalentBridge",
    "UrbanNest", "ForgeBuild", "AtelierGrid", "RoomMuse", "LineWorks",
    "CoreSystems", "SunVault", "ClearGrid", "TerraMetric", "Fieldwise",
    "HarvestPack", "TableFlame", "StayHaven", "AtlasKind", "RideSure",
    "ChainPilot", "MotorArc", "AeroVector", "HarborLine", "CornerGoods",
    "MarketPulse", "LineaMode", "SkinTheory", "WaveCast", "StageCurrent",
    "IndexHouse", "SignalCraft", "StudioFrame", "PulseClub", "VowVenue",
    "CivicAccess", "CommonGood", "PawHealth", "MaisonVale", "Nameplate",
]


THEME_VOICES = [
    "calm clinical precision", "research-grade scientific authority", "soft lifestyle clarity",
    "operational infrastructure confidence", "product-led software directness",
    "coverage-first connectivity assurance", "risk-control security discipline",
    "analytical decision clarity", "measured financial stewardship", "protective advisory trust",
    "formal legal clarity", "deadline-aware administrative order", "strategic boardroom focus",
    "supportive learning momentum", "human hiring intelligence", "local market confidence",
    "site-ready construction assurance", "spatial design intelligence", "material-led home warmth",
    "industrial production discipline", "technical engineering reliability", "renewable value clarity",
    "public utility resilience", "evidence-led climate responsibility", "seasonal rural practicality",
    "quality-led food craft", "warm sensory hospitality", "restful guest confidence",
    "curated destination expertise", "safe passenger coordination", "networked delivery control",
    "vehicle purchase confidence", "aviation safety professionalism", "maritime operational assurance",
    "friendly retail polish", "marketplace trust and speed", "editorial fashion restraint",
    "ingredient-conscious beauty care", "audience-first media programming", "high-energy live culture",
    "editorial knowledge authority", "campaign performance discipline", "visual production taste",
    "motivating movement clarity", "experience-led celebration planning", "plain civic accessibility",
    "transparent impact urgency", "compassionate veterinary care", "quiet high-end discretion",
    "public authority and personal voice",
]

TARGET_INSPIRATION_LINES = """
1|Neko Health|https://www.nekohealth.com/|#f7fbff,#101820,#20b8d8,#07141e,#d7f7ff|Neko-style clean health-tech with scan-first white space, black copy, and electric blue data accents|A scan-first care journey with minimalist copy, body-data panels, instant-results proof, and a direct appointment CTA|scan-first health check journey|body scan split hero|minimal scan header|rounded diagnostic data cards|scan booking form|soft reveal with data-point counters|body-scan rooms, data visualisations, calm clinical detail|neko
2|Recursion|https://www.recursion.com/|#050709,#5cffb1,#2f6dff,#f3f7ff,#9cffd3|Recursion-style TechBio with dark scientific grids, microscopy panels, and pipeline evidence|A research platform story built around AI discovery, phase tables, partner proof, and data-scale credibility|scientific operating system dossier|AI biology lab hero|research mega-nav header|pipeline evidence cards|partner research form|cell-grid reveal and pipeline motion|cell imagery, robotic lab systems, data maps|recursion
3|Ritual|https://ritual.com/|#fff6dc,#19355f,#ffcf2e,#11264b,#f6a900|Ritual-style supplement commerce with warm yellow, navy copy, pill buttons, and routine shelves|A routine-first wellness shop with offer strip, product education, rounded capsules, and evidence-led reassurance|routine commerce shelf|product routine hero|promo shop header|supplement capsule cards|routine quiz form|gentle shelf reveal|bright product jars, daily rituals, ingredient callouts|ritual
4|Cloudflare|https://www.cloudflare.com/|#fff7ed,#f38020,#faae40,#18191f,#ffe4c2|Cloudflare-style infrastructure marketing with orange CTAs, network diagrams, and dense product routes|A network-first IT site with technical proof, orange action paths, product cards, and status-aware conversion|edge network product system|network diagram hero|orange product navigation|network service tiles|IT audit route form|fast network sweep|edge maps, server nodes, operational dashboards|cloudflare
5|Linear|https://linear.app/|#08090d,#5e6ad2,#9b8cff,#f7f8ff,#37d67a|Linear-style dark product system with glass UI, fine borders, gradient light, and app panels|A product-led SaaS site with a dark dashboard hero, precise modules, issue-like cards, and calm product copy|dark product dashboard system|app interface hero|floating product header|fine-line app cards|demo request form|subtle glow and panel reveal|dark app screens, issue boards, roadmap panels|linear
6|Starlink|https://www.starlink.com/|#050505,#ffffff,#8b949e,#f5f5f5,#b8c7d9|Starlink-style black space utility with full-bleed contrast, uppercase navigation, and availability CTAs|A coverage-first telecom site with stark dark hero, satellite-map panels, speed proof, and direct address checking|space coverage landing|black full-bleed coverage hero|uppercase utility header|satellite coverage cards|availability checker form|slow parallax and signal reveal|satellite fields, night skies, coverage maps, hardware silhouettes|starlink
7|Wiz|https://www.wiz.io/|#11092a,#7b2cff,#19c6ff,#f8f6ff,#ff6bd6|Wiz-style cloud-security energy with purple depth, blue diagrams, and bold risk visuals|A cloud-risk command site with neon topology, rounded security modules, compliance proof, and audit routing|cloud security command centre|purple cloud-risk hero|security product header|rounded cloud-risk cards|audit request form|glowing topology reveal|cloud graphs, risk paths, security dashboards|wiz
8|Atlan|https://atlan.com/|#f7f1e7,#2357ff,#25d0a3,#151a2d,#ffb84d|Atlan-style context-layer data site with warm surfaces, blue product depth, and collaborative metadata cards|A data catalogue experience with friendly dashboards, metadata proof, search panels, and AI-context positioning|context layer data workspace|metadata dashboard hero|data product header|collaborative data cards|dashboard planning form|dashboard stack reveal|data catalogues, lineage graphs, metadata workspaces|atlan
9|Wise|https://wise.com/|#ebff53,#163300,#00b67a,#102014,#f0f5e8|Wise-style financial utility with acid green, bold calculator blocks, and low-friction forms|A transfer-calculator finance site with bold green hierarchy, fee transparency, route selection, and trust notes|green calculator flow|money movement calculator hero|utility finance header|fee transparency cards|advisor calculator form|counter and calculator reveal|payment flows, rate cards, account panels|wise
10|Lemonade|https://www.lemonade.com/|#fff2f7,#ff0083,#251024,#ffffff,#ffb3d9|Lemonade-style insurance quote flow with hot pink, friendly copy, and simple white cards|A quote-first insurance site with pink action, chat-like steps, playful policy cards, and claims reassurance|pink quote journey|friendly quote hero|simple insurance header|rounded policy cards|quote route form|friendly step reveal|quote flows, policy cards, soft character-free illustrations|lemonade
11|Clio|https://www.clio.com/|#f7f2e8,#183b72,#5ba8ff,#111827,#f4c95d|Clio-style legal SaaS with calm blue authority, soft cream pages, and product proof|A law-practice platform site with blue navigation, document panels, workflow cards, and consultation routing|legal platform workflow|blue legal software hero|practice product header|workflow document cards|consultation intake form|workflow tab reveal|legal dashboards, document checklists, calm office detail|clio
12|Xero|https://www.xero.com/|#eaf7ff,#13b5ea,#045c8c,#102a43,#8de1ff|Xero-style accounting clarity with sky blue, rounded dashboards, and friendly admin paths|An accounting command site with cloud-blue dashboards, deadline cards, plan comparison, and admin reassurance|cloud accounting dashboard|rounded ledger dashboard hero|blue product header|ledger dashboard cards|filing quote form|calendar and ledger reveal|bookkeeping dashboards, invoices, payroll cards|xero
13|IDEO|https://www.ideo.com/|#ffffff,#111111,#ff5a1f,#f4f4f0,#0066ff|IDEO-style creative consulting with editorial whitespace, bold project thinking, and case-study rhythm|A strategy studio site with large editorial type, idea-led modules, mosaic proof, and workshop conversion|editorial innovation studio|idea-led editorial hero|studio index header|case thinking cards|brief workshop form|project tile reveal|workshops, prototypes, research walls, creative teams|ideo
14|MasterClass|https://www.masterclass.com/|#050505,#ffffff,#d71920,#151515,#b28b55|MasterClass-style cinematic education with black stage surfaces, instructor tiles, and red CTAs|A course-led education site with cinematic hero, lesson shelves, premium teacher proof, and trial routes|cinematic course catalogue|black cinematic course hero|streaming course header|lesson trailer cards|trial lesson form|trailer fade reveal|course stills, teacher portraits, dark learning shelves|masterclass
15|Welcome to the Jungle|https://www.welcometothejungle.com/|#ffe45e,#111111,#ff6a3d,#f8f4e8,#1f6feb|Welcome to the Jungle-style hiring editorial with yellow blocks, human stories, and job-board modules|A recruitment magazine site with candidate/employer split, bold editorial cards, people proof, and upload routes|editorial talent marketplace|yellow job magazine hero|magazine hiring header|job story cards|candidate upload form|editorial card shuffle|workplace portraits, job cards, culture pages|jungle
16|The Modern House|https://www.themodernhouse.com/|#fbfaf7,#111111,#8a8f83,#ffffff,#c7b299|The Modern House-style property editorial with quiet type, generous imagery, and thin-rule listings|A real-estate editorial site with architecture-led listings, sparse navigation, area guides, and valuation flow|minimal property journal|architectural listing hero|quiet property header|thin-rule listing cards|valuation enquiry form|slow image reveal|modern homes, interiors, floor plans, neighbourhood details|modernhouse
17|Procore|https://www.procore.com/|#fff7ed,#ff6a00,#111827,#1f2937,#ffd166|Procore-style construction software with orange action, black contrast, and worksite proof|A build-management site with construction CTAs, project panels, safety proof, and estimate routing|construction platform grid|worksite software hero|construction product header|project control cards|estimate form|project progress reveal|job sites, schedule boards, build dashboards|procore
18|Snohetta|https://snohetta.com/|#f4f1eb,#111111,#c4c7c5,#ffffff,#7a807b|Snohetta-style architecture portfolio with radical restraint, huge imagery, and project-index logic|A spatial portfolio site with minimal chrome, full-bleed project moments, thin metadata, and studio enquiry|spatial project index|minimal full-bleed project hero|bare studio header|architectural index cards|project brief form|slow spatial reveal|architecture photography, plans, models, site context|snohetta
19|Kelly Wearstler|https://www.kellywearstler.com/|#f6eee6,#4a2b2a,#c99a6b,#111111,#e7c9a9|Kelly Wearstler-style interiors with tactile luxury, material contrast, and editorial commerce|A material-led interiors site with luxe moodboards, serif headlines, room selectors, and sourcing CTAs|luxury material moodboard|editorial room hero|atelier commerce header|material mood cards|design brief form|material fade reveal|textures, sculptural furniture, styled rooms, swatches|wearstler
20|Formlabs|https://formlabs.com/|#f8f8f8,#111111,#ff5f1f,#dfe3e6,#6b7280|Formlabs-style manufacturing product clarity with precise specs, orange highlights, and printer-like panels|A production capability site with product-spec tables, precise media panels, facility proof, and RFQ routing|industrial product specification|precision product hero|manufacturing product header|specification cards|RFQ spec form|spec table reveal|3D printers, material samples, production benches|formlabs
21|Arup|https://www.arup.com/|#ffffff,#e21b2d,#111111,#f0f2f4,#7f8c8d|Arup-style engineering editorial with red accents, project journalism, and technical depth|An engineering authority site with editorial project blocks, red rules, technical proof, and expert enquiry|engineering project journal|red-rule technical hero|consulting project header|engineering proof cards|engineer enquiry form|diagram reveal|infrastructure projects, diagrams, field engineering|arup
22|Tesla Energy|https://www.tesla.com/energy|#f7f7f7,#111111,#e82127,#ffffff,#bfc7d5|Tesla Energy-style minimal product marketing with stark surfaces, centered copy, and energy-product proof|A renewable energy product site with minimalist hero, savings modules, battery/solar cards, and direct calculator|minimal energy product landing|centered product hero|minimal energy header|product output cards|savings calculator form|clean product reveal|solar roofs, batteries, energy app panels|tesla
23|Octopus Energy|https://octopus.energy/|#140021,#7f3cff,#ff4fd8,#f6f1ff,#00d1ff|Octopus-style utilities with playful purple energy, rounded service blocks, and transparent tariff flow|A utility service site with bright service cards, friendly calculator modules, alert strips, and help routing|playful utility account flow|purple service hero|friendly utility header|rounded tariff cards|service request form|playful account reveal|energy accounts, meters, tariff calculators, service notices|octopus
24|Watershed|https://watershed.com/|#f4fbf7,#083d31,#00a878,#d8f5e2,#244bff|Watershed-style climate software with serious green, evidence dashboards, and enterprise clarity|A climate-accounting site with emissions dashboards, report proof, methodology panels, and audit CTAs|climate data operating system|emissions dashboard hero|climate product header|carbon evidence cards|audit advisory form|metric stack reveal|carbon dashboards, climate reports, data rooms|watershed
25|AeroFarms|https://www.aerofarms.com/|#061b12,#20c36b,#a6e22e,#f2f7e8,#6bbf59|AeroFarms-style agriculture with deep green, vertical-farm rhythm, and controlled-growth proof|A controlled-agriculture site with vertical growing surfaces, yield metrics, season planning, and visit routes|vertical farm growth system|deep-green grow room hero|agri innovation header|growth metric cards|season visit form|vertical row reveal|indoor farms, leafy crops, grow lights, yield data|aerofarms
26|Oatly|https://www.oatly.com/|#f5ead2,#004b8d,#111111,#ffdf3d,#f26b3a|Oatly-style food brand with playful packaging, chunky copy blocks, and offbeat product shelves|A packaged food site with bold copy, illustrated product cards, allergen filters, and stockist routes|playful product manifesto|packaging shelf hero|food brand header|chunky ingredient cards|trade enquiry form|poster-style reveal|cartons, ingredients, recipe panels, hand-made notes|oatly
27|Sketch London|https://sketch.london/|#f8d7e8,#1b1b1b,#f2c94c,#7b406c,#ffffff|Sketch-style restaurant experience with surreal pastel rooms, dramatic menus, and reservation focus|A sensory restaurant site with pastel stage surfaces, menu cards, room-gallery rhythm, and booking CTAs|surreal reservation stage|pastel dining-room hero|reservation theatre header|ornate menu cards|reservation form|room-scene reveal|dining rooms, plates, cocktails, theatrical interiors|sketch
28|Aman|https://www.aman.com/|#f3efe7,#2f2a24,#b89b72,#ffffff,#6c756b|Aman-style hospitality with quiet luxury, large tranquil imagery, and restrained booking paths|A hotel site with serene full-bleed rooms, understated booking modules, experience cards, and policy calm|quiet retreat booking flow|serene full-bleed stay hero|discreet hotel header|retreat room cards|availability form|slow luxury fade|villas, landscapes, spa spaces, calm interiors|aman
29|Black Tomato|https://www.blacktomato.com/|#0b0b0b,#ffffff,#b4874a,#f1eee8,#8bb8e8|Black Tomato-style travel editorial with black contrast, immersive destinations, and itinerary storytelling|A travel-planning site with dark editorial hero, trip story cards, itinerary accordions, and bespoke enquiry|dark destination magazine|immersive trip hero|travel editorial header|journey story cards|trip planner form|map and story reveal|remote places, maps, itinerary details, travel photography|blacktomato
30|Citymapper|https://citymapper.com/|#eaff57,#133a1b,#00a66a,#ffffff,#111111|Citymapper-style transit utility with bright green, map-first decisions, and route cards|A passenger mobility site with green route planning, fare estimate cards, map surfaces, and fast booking|map-first route planner|green transit planner hero|route utility header|transit route cards|fare estimate form|route line reveal|transit maps, route lines, vehicles, city movement|citymapper
31|Flexport|https://www.flexport.com/|#f4f8ff,#2563eb,#ff7a1a,#0f172a,#a7c7ff|Flexport-style logistics platform with blue enterprise polish, orange action, and shipment dashboards|A freight-command site with shipment dashboards, network maps, quote modules, and status proof|global freight command|shipment dashboard hero|logistics platform header|tracking dashboard cards|freight quote form|status map reveal|ports, shipment dashboards, containers, trade lanes|flexport
32|Polestar|https://www.polestar.com/|#f8f8f8,#111111,#d8dadd,#ffffff,#8a8f98|Polestar-style automotive minimalism with cool greys, product focus, and restrained configurator energy|A vehicle showroom site with precise white space, car-card rhythm, finance paths, and test-drive CTAs|minimal EV showroom|stark vehicle product hero|minimal showroom header|precise vehicle cards|test-drive form|clean configurator reveal|EV silhouettes, interiors, chargers, specification panels|polestar
33|Boom Supersonic|https://boomsupersonic.com/|#050b18,#ff6f2c,#4cc9f0,#ffffff,#223456|Boom-style aviation future with dark aerospace surfaces, orange velocity, and fleet-spec confidence|An aviation site with speed-led hero, aircraft spec cards, route modules, safety proof, and charter enquiry|supersonic operations deck|aerospace velocity hero|aviation product header|fleet specification cards|charter route form|velocity line reveal|aircraft, runways, hangars, flight paths|boom
34|Maersk|https://www.maersk.com/|#ecf8ff,#40b4e5,#003a5d,#ffffff,#9ad7f5|Maersk-style maritime corporate clarity with pale blue, logistics forms, and route tracking|A shipping site with ocean-blue service panels, cargo quote logic, port schedules, and tracking proof|blue ocean logistics portal|shipping route hero|maritime utility header|cargo service cards|shipping quote form|route schedule reveal|ships, containers, ports, route maps, logistics docs|maersk
35|Apple Store|https://www.apple.com/store|#f5f5f7,#1d1d1f,#0071e3,#ffffff,#a1a1a6|Apple Store-style retail minimalism with soft grey surfaces, product tiles, and clear shopping paths|A retail shopfront with clean product shelves, rounded offer cards, service proof, and store-finder CTAs|minimal product store|soft product shelf hero|clean shop header|rounded product tiles|store finder form|polished product reveal|product tiles, store spaces, service cards, device-like panels|apple
36|SSENSE|https://www.ssense.com/|#ffffff,#000000,#777777,#f5f5f5,#d9d9d9|SSENSE-style e-commerce with monochrome grid discipline, compact type, and catalogue authority|A marketplace catalogue with black-white product grids, tiny metadata, filter logic, and checkout routing|monochrome catalogue system|fashion-commerce grid hero|compact shop header|monochrome product cards|support routing form|grid snap reveal|product grids, editorial crops, order panels, marketplace lists|ssense
37|Jacquemus|https://www.jacquemus.com/|#fff2b8,#111111,#ffde00,#ffffff,#d97b4f|Jacquemus-style fashion with sunny surrealism, oversized imagery, and campaign-led commerce|A fashion lookbook site with warm yellow, playful scale shifts, collection cards, and sizing routes|sunlit campaign lookbook|oversized campaign hero|fashion campaign header|sunny lookbook cards|styling enquiry form|playful campaign reveal|campaign imagery, fabric closeups, product scale, runway detail|jacquemus
38|Aesop|https://www.aesop.com/|#f3eadc,#35291f,#8c6a4f,#ffffff,#c9b28c|Aesop-style beauty retail with muted apothecary surfaces, serif detail, and calm product education|A routine site with restrained product education, ingredient notes, tactile cards, and consultation routes|apothecary routine journal|muted product education hero|apothecary shop header|ingredient education cards|routine advice form|quiet product reveal|bottles, textures, counters, botanical ingredient details|aesop
39|The Verge|https://www.theverge.com/|#0b0b13,#e2127a,#fff200,#00d4ff,#ffffff|The Verge-style media system with black surfaces, neon accents, angular modules, and dense story grids|A media site with bold editorial grid, neon category strips, episode cards, and advertiser download routes|neon editorial news grid|angular media hero|neon media header|angled story cards|advertise kit form|ticker and story reveal|news cards, studio images, episode panels, neon lines|verge
40|A24|https://a24films.com/|#050505,#ffffff,#c69a55,#181818,#e24a2e|A24-style entertainment with black cinema mood, poster grids, and understated weirdness|An entertainment site with film-poster rhythm, dark editorial cards, ticket routes, and venue proof|indie film poster system|dark poster hero|film studio header|poster event cards|ticket enquiry form|poster fade reveal|film posters, stage stills, credits, audience moments|a24
41|Monocle|https://www.monocle.com/|#f7efd2,#111111,#f6c400,#ffffff,#8c1d18|Monocle-style publishing with print cadence, yellow accents, compact columns, and editorial authority|A knowledge platform with magazine columns, archive search, author cards, and newsletter conversion|print magazine archive|editorial masthead hero|print index header|column article cards|newsletter form|print-column reveal|magazine spreads, desks, books, archive covers|monocle
42|AKQA|https://www.akqa.com/|#050505,#ffffff,#6bdcff,#151515,#9bff6d|AKQA-style agency minimalism with dark futurist surfaces, crisp white type, and case-study gravity|A marketing agency site with immersive black work panels, sharp case filters, results proof, and brief routes|dark agency case system|immersive case-study hero|minimal agency header|dark campaign cards|brief form|case panel reveal|campaign visuals, digital products, studio screens, metrics|akqa
43|Pentagram|https://www.pentagram.com/|#ffffff,#111111,#e30613,#f2f2f2,#0057ff|Pentagram-style design portfolio with stark white, red accents, huge typography, and rigorous grids|A creative portfolio with identity-led project tiles, typographic scale, lightbox logic, and studio enquiry|graphic design portfolio grid|typographic work hero|design studio header|identity project cards|creative brief form|grid reveal|brand systems, posters, design boards, case images|pentagram
44|Nike|https://www.nike.com/|#ffffff,#111111,#ff3d00,#f4f4f4,#c8c8c8|Nike-style sport retail with bold hero imagery, black-white contrast, and direct product/program CTAs|A fitness site with athlete-scale hero, program cards, coach proof, schedule filters, and membership CTAs|athletic product-program system|big sport campaign hero|sport retail header|performance program cards|trial class form|kinetic reveal|athletes, training spaces, shoes, performance metrics|nike
45|Luma|https://luma.com/|#f7f8ff,#6c47ff,#14b8a6,#ffffff,#ffb703|Luma-style events with clean cards, soft gradients, calendar utility, and quick RSVP routes|An events site with elegant event cards, date filters, host proof, and RSVP-style enquiry|clean event calendar system|event card hero|calendar utility header|RSVP event cards|date enquiry form|calendar card reveal|event cards, calendars, guest lists, venue details|luma
46|GOV.UK Design System|https://design-system.service.gov.uk/|#ffffff,#1d70b8,#0b0c0c,#f3f2f1,#ffdd00|GOV.UK Design System-style public service with plain language, blue actions, and high-contrast forms|A civic service site with task-first pages, blue start buttons, form patterns, and accessibility-first structure|public service task flow|plain service hero|GOV-style service header|square service boxes|public request form|minimal state reveal|forms, service lists, notices, public task flows|govuk
47|charity: water|https://www.charitywater.org/|#ffffff,#ffc907,#111111,#f6f6f2,#2b6cb0|charity: water-style nonprofit with yellow urgency, human impact proof, and donation clarity|A donor site with bold yellow impact modules, transparent metrics, story cards, and donation selector|transparent donation impact flow|yellow impact hero|donation campaign header|impact story cards|donation form|impact counter reveal|community photos, water projects, donor reports, maps|charitywater
48|Modern Animal|https://www.modernanimal.com/|#fff7ef,#256a5e,#ffb199,#ffffff,#21413a|Modern Animal-style veterinary care with warm clinic colours, rounded forms, and friendly triage|A veterinary site with warm urgent-care modules, appointment paths, team proof, and symptom routing|modern clinic care flow|warm appointment hero|friendly clinic header|rounded care cards|appointment form|triage card reveal|clinic rooms, pets, care teams, appointment panels|modernanimal
49|Rolex|https://www.rolex.com/|#081f18,#0b5f3a,#d4af37,#f4efe2,#111111|Rolex-style luxury with deep green, gold restraint, heritage pacing, and private product focus|A luxury service site with green-gold maison mood, heritage cards, private access routes, and discreet proof|heritage luxury maison|deep-green private hero|maison heritage header|gold hairline cards|private access form|slow heritage reveal|craft details, watches, private rooms, heritage materials|rolex
50|James Clear|https://jamesclear.com/|#fffdf8,#17233c,#c09a4a,#f4f0e8,#3f6f6b|James Clear-style personal brand with clean essays, author authority, newsletter focus, and simple navigation|A personal brand site with editorial essay rhythm, speaking/media cards, newsletter conversion, and booking clarity|author essay and media system|editorial author hero|simple author header|essay media cards|booking form|newsletter reveal|author portraits, books, essays, podcast and speaking panels|jamesclear
""".strip()


TARGET_CSS_PROFILES = {
    "neko": "THEME .site-header{background:#fff;border-bottom:0}.header-utility{background:#d7f7ff;color:#101820}.nav-cta,.button.primary{background:#101820;color:#fff;border-radius:999px} THEME .hero-section{background:#f7fbff}.hero-copy{background:transparent;box-shadow:none}.hero-media{border:0;border-radius:34px;box-shadow:none}.signature-panel,.metric-card{border-radius:28px;background:#fff}",
    "recursion": "THEME{background:#050709;color:#f3f7ff}.site-header{background:#050709;color:#f3f7ff}.header-utility{background:#0b1015;color:#5cffb1}.hero-section{background:#050709;color:#f3f7ff}.hero-media,.mini-card,.signature-panel{background:#0b1015;border-color:#24434a}.hero-section::before{background-size:36px 36px}.button.primary{background:#5cffb1;color:#050709}",
    "ritual": "THEME .header-utility{background:#ffcf2e;color:#19355f;justify-content:center}.site-header{background:#fff6dc}.hero-section{background:#fff6dc}.hero-media{border-radius:999px 999px 34px 34px;background:#ffcf2e}.button.primary{background:#19355f;color:#fff}.mini-card,.price-card{border-radius:30px;background:#fffdf0}.card-grid{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}",
    "cloudflare": "THEME .site-header{background:#fff7ed;border-bottom:1px solid #faae40}.header-utility{background:#18191f;color:#faae40}.button.primary,.nav-cta{background:#f38020;color:#18191f;border-color:#f38020}.hero-section{background:linear-gradient(135deg,#fff7ed,#ffe4c2)}.map-canvas,.dashboard-panel .metric-card{border-color:#f38020}.mini-card{border-top:6px solid #f38020}",
    "linear": "THEME{background:#08090d;color:#f7f8ff}.site-header{background:rgba(8,9,13,.86);color:#f7f8ff;border-bottom:1px solid rgba(255,255,255,.12)}.header-utility{background:#0d0f18;color:#9b8cff}.hero-section{background:radial-gradient(circle at 50% 0,#20264c,transparent 44%),#08090d;color:#f7f8ff}.hero-media,.mini-card,.signature-panel{background:rgba(255,255,255,.045);border-color:rgba(255,255,255,.14);box-shadow:0 30px 90px rgba(0,0,0,.38)}.button.primary{background:#5e6ad2;color:#08090d}",
    "starlink": "THEME{background:#050505;color:#fff}.site-header{background:rgba(5,5,5,.78);color:#fff;text-transform:uppercase;border-bottom:1px solid rgba(255,255,255,.18)}.header-utility{background:#050505;color:#fff}.hero-section{min-height:72vh;background:linear-gradient(180deg,rgba(0,0,0,.15),#050505),#050505;color:#fff}.hero-grid{grid-template-columns:1fr}.hero-copy{max-width:780px}.button.primary{background:#fff;color:#050505}.mini-card{background:#111;border-color:#333;color:#fff}",
    "wiz": "THEME{background:#11092a;color:#f8f6ff}.site-header{background:rgba(17,9,42,.9);color:#f8f6ff}.header-utility{background:#20104e;color:#19c6ff}.hero-section{background:radial-gradient(circle at 72% 16%,#7b2cff,transparent 34%),#11092a;color:#f8f6ff}.mini-card,.signature-panel,.metric-card{background:rgba(248,246,255,.08);border-color:rgba(25,198,255,.35);color:#f8f6ff}.button.primary{background:#19c6ff;color:#11092a}.hero-media{box-shadow:0 0 70px rgba(123,44,255,.38)}",
    "atlan": "THEME .site-header{background:#f7f1e7}.header-utility{background:#151a2d;color:#25d0a3}.hero-section{background:linear-gradient(135deg,#f7f1e7,#fdfaf4)}.hero-media,.mini-card,.signature-panel{border-radius:24px;border-color:#d7cbb9}.button.primary{background:#2357ff;color:#fff}.metric-card strong{color:#2357ff}.map-canvas{background-color:#fff;border-color:#2357ff}.mini-card:nth-child(2){background:#e7fff8}",
    "wise": "THEME .site-header{background:#ebff53;color:#163300}.header-utility{background:#163300;color:#ebff53}.hero-section{background:#ebff53;color:#163300}.hero-grid{grid-template-columns:minmax(0,.88fr) minmax(360px,1.12fr)}.hero-media,.finder-panel,.form-panel{border-radius:32px;background:#fff}.button.primary,.nav-cta{background:#163300;color:#ebff53;border-color:#163300}.metric-card strong{font-size:clamp(2.6rem,6vw,5rem)}",
    "lemonade": "THEME .site-header{background:#fff;color:#251024}.header-utility{background:#ff0083;color:#111827}.hero-section{background:#fff2f7}.button.primary,.nav-cta{background:#ff0083;color:#111827;border-color:#ff0083;border-radius:999px}.hero-media,.mini-card,.form-panel,.signature-panel{border-radius:30px;border-color:#ffb3d9}.mini-card{background:#fff}.process-list span{background:#ff0083;color:#111827}.hero-copy h2{color:#ff0083}",
    "clio": "THEME .site-header{background:#f7f2e8}.header-utility{background:#183b72;color:#fff}.button.primary,.nav-cta{background:#183b72;color:#fff}.hero-section{background:linear-gradient(120deg,#f7f2e8,#eaf4ff)}.mini-card,.form-panel,.signature-panel{border-radius:18px;background:#fff}.card-grid{grid-template-columns:1.2fr 1fr 1fr}.mini-card{border-top:4px solid #5ba8ff}.footer-brand{border-radius:18px}",
    "xero": "THEME .site-header{background:#eaf7ff}.header-utility{background:#13b5ea;color:#111827}.hero-section{background:linear-gradient(180deg,#eaf7ff,#fff)}.button.primary,.nav-cta{background:#13b5ea;color:#111827;border-color:#13b5ea;border-radius:999px}.hero-media,.dashboard-panel .metric-card,.mini-card{border-radius:28px;background:#fff}.card-grid{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.metric-card strong{color:#045c8c}",
    "ideo": "THEME .site-header{background:#fff;border-bottom:1px solid #111}.header-utility{background:#fff;color:#111;justify-content:space-between}.hero-section{background:#fff}.hero-grid{grid-template-columns:1fr;align-items:start}.hero-copy{max-width:980px}.hero-media{border-radius:0;box-shadow:none;border:0}.button.primary{background:#111;color:#fff}.mini-card{border-radius:0;box-shadow:none;border-width:0 0 2px}.mini-card:nth-child(2){background:#ff5a1f;color:#111}",
    "masterclass": "THEME{background:#050505;color:#fff}.site-header{background:#050505;color:#fff;border-bottom:1px solid #222}.header-utility{background:#151515;color:#b28b55}.hero-section{background:#050505;color:#fff}.hero-media{border-radius:0;border:0;box-shadow:0 30px 90px rgba(0,0,0,.6)}.mini-card,.price-card,.signature-panel{background:#151515;color:#fff;border-color:#2a2a2a}.button.primary{background:#d71920;color:#fff;border-color:#d71920}",
    "jungle": "THEME .site-header{background:#ffe45e;color:#111}.header-utility{background:#111;color:#ffe45e}.hero-section{background:#ffe45e;color:#111}.button.primary,.nav-cta{background:#111;color:#ffe45e;border-color:#111}.hero-media,.mini-card{border-radius:0;box-shadow:none;border:2px solid #111}.card-grid{grid-template-columns:1.4fr .8fr .8fr}.mini-card:nth-child(2){background:#ff6a3d}.text-link{text-decoration-thickness:.25em}",
    "modernhouse": "THEME .site-header{background:#fbfaf7;border-bottom:1px solid #111}.header-utility{background:#fbfaf7;color:#111}.hero-section{background:#fbfaf7}.hero-media,.visual-strip figure{border-radius:0;box-shadow:none}.button.primary,.nav-cta{background:#111;color:#fff;border-color:#111;border-radius:0}.mini-card{background:transparent;border-width:1px 0 0;border-radius:0;box-shadow:none}.card-grid{grid-template-columns:1fr}.hero-copy{max-width:720px}",
    "procore": "THEME .site-header{background:#111827;color:#fff}.header-utility{background:#ff6a00;color:#111827}.hero-section{background:linear-gradient(135deg,#111827,#1f2937);color:#fff}.button.primary,.nav-cta{background:#ff6a00;color:#111827;border-color:#ff6a00}.mini-card,.signature-panel{background:#fff7ed;color:#111827;border-radius:6px}.process-list li{border-left:8px solid #ff6a00}.hero-media{border-radius:8px}",
    "snohetta": "THEME .site-header{background:#f4f1eb;border-bottom:0}.header-utility{background:#f4f1eb;color:#111;justify-content:center}.hero-section{background:#f4f1eb}.hero-grid{grid-template-columns:minmax(280px,.45fr) minmax(0,1.55fr)}.hero-media,.mini-card,.visual-strip figure{border-radius:0;box-shadow:none}.button.primary,.nav-cta{background:transparent;color:#111;border-color:#111;border-radius:0}.mini-card{background:transparent;border-width:0 0 1px}.section{padding-block:clamp(110px,12vw,190px)}",
    "wearstler": "THEME .site-header{background:#f6eee6;color:#4a2b2a}.header-utility{background:#4a2b2a;color:#e7c9a9}.hero-section{background:#f6eee6}.hero-media,.mini-card,.signature-panel{border-radius:4px;border-color:#c99a6b}.button.primary,.nav-cta{background:#4a2b2a;color:#f6eee6;border-color:#4a2b2a}.mini-card{background:#fff8f1}.hero-copy h1{font-family:var(--font-accent)}.visual-card-stack{gap:1.4rem}",
    "formlabs": "THEME .site-header{background:#f8f8f8;border-bottom:1px solid #dfe3e6}.header-utility{background:#111;color:#ff5f1f}.button.primary,.nav-cta{background:#ff5f1f;color:#111;border-color:#ff5f1f;border-radius:6px}.hero-section{background:#f8f8f8}.hero-media,.mini-card,.signature-panel{border-radius:6px;box-shadow:none}.dashboard-panel,.pricing-grid{border-top:3px solid #111}.mini-card h3{font-family:var(--font-mono)}",
    "arup": "THEME .site-header{background:#fff;border-bottom:1px solid #e21b2d}.header-utility{background:#e21b2d;color:#fff}.hero-section{background:#fff}.button.primary,.nav-cta{background:#e21b2d;color:#fff;border-color:#e21b2d;border-radius:0}.hero-media,.mini-card{border-radius:0;box-shadow:none}.mini-card{border-top:4px solid #e21b2d}.section-copy{border-left:2px solid #e21b2d;padding-left:1rem}",
    "tesla": "THEME .site-header{background:rgba(247,247,247,.92);border-bottom:0}.header-utility{background:#111;color:#fff;justify-content:center}.hero-section{background:#f7f7f7;text-align:center}.hero-grid{grid-template-columns:1fr}.hero-copy{margin:auto;max-width:840px}.button.primary,.nav-cta{background:#111;color:#fff;border-radius:4px}.button.secondary{background:#fff;border-color:#fff}.hero-media{border-radius:0;border:0;box-shadow:none}.mini-card{border-radius:8px}",
    "octopus": "THEME{background:#140021;color:#f6f1ff}.site-header{background:#140021;color:#f6f1ff}.header-utility{background:#7f3cff;color:#fff}.hero-section{background:radial-gradient(circle at 70% 18%,#ff4fd8,transparent 30%),#140021;color:#f6f1ff}.button.primary,.nav-cta{background:#ff4fd8;color:#140021;border-color:#ff4fd8;border-radius:999px}.mini-card,.signature-panel{background:#f6f1ff;color:#140021;border-radius:28px}.hero-media{box-shadow:0 0 70px rgba(255,79,216,.25)}",
    "watershed": "THEME .site-header{background:#f4fbf7}.header-utility{background:#083d31;color:#d8f5e2}.hero-section{background:#f4fbf7}.button.primary,.nav-cta{background:#083d31;color:#fff;border-color:#083d31}.dashboard-panel .metric-card{background:#d8f5e2;border-color:#00a878}.mini-card,.signature-panel{border-radius:14px}.hero-media{border-radius:18px}.metric-card strong{color:#007a5a}",
    "aerofarms": "THEME{background:#061b12;color:#f2f7e8}.site-header{background:#061b12;color:#f2f7e8}.header-utility{background:#20c36b;color:#061b12}.hero-section{background:linear-gradient(90deg,rgba(32,195,107,.18) 1px,transparent 1px),#061b12;color:#f2f7e8;background-size:42px 100%}.button.primary,.nav-cta{background:#a6e22e;color:#061b12;border-color:#a6e22e}.mini-card,.signature-panel{background:#10291c;color:#f2f7e8;border-color:#20c36b;border-radius:14px}",
    "oatly": "THEME .site-header{background:#f5ead2;color:#111}.header-utility{background:#004b8d;color:#f5ead2}.hero-section{background:#f5ead2}.button.primary,.nav-cta{background:#004b8d;color:#fff;border-color:#004b8d;border-radius:0}.hero-media,.mini-card{border:3px solid #111;border-radius:0;box-shadow:none}.mini-card:nth-child(2){background:#ffdf3d}.hero-copy h1{text-transform:uppercase}.card-grid{gap:1.4rem}",
    "sketch": "THEME .site-header{background:#f8d7e8;color:#1b1b1b}.header-utility{background:#7b406c;color:#fff}.hero-section{background:linear-gradient(135deg,#f8d7e8,#fff)}.button.primary,.nav-cta{background:#1b1b1b;color:#f8d7e8;border-color:#1b1b1b;border-radius:999px}.hero-media,.mini-card,.form-panel{border-radius:36px;border-color:#7b406c}.mini-card{background:#fff}.mini-card:nth-child(2){background:#f2c94c}",
    "aman": "THEME .site-header{background:#f3efe7;color:#2f2a24}.header-utility{background:#2f2a24;color:#b89b72}.hero-section{background:#f3efe7}.hero-grid{grid-template-columns:1fr}.hero-media{order:-1;border-radius:0;border:0;box-shadow:none}.hero-copy{max-width:720px;margin:auto;text-align:center}.button.primary,.nav-cta{background:#2f2a24;color:#fff;border-radius:0}.mini-card{border-radius:0;box-shadow:none;background:#fffdf8}",
    "blacktomato": "THEME{background:#0b0b0b;color:#fff}.site-header{background:#0b0b0b;color:#fff}.header-utility{background:#111;color:#b4874a}.hero-section{background:#0b0b0b;color:#fff}.hero-media{border-radius:0;border:0;box-shadow:none}.button.primary,.nav-cta{background:#fff;color:#0b0b0b;border-color:#fff}.mini-card,.signature-panel{background:#161616;color:#fff;border-color:#333;border-radius:4px}.text-link{color:#b4874a}",
    "citymapper": "THEME .site-header{background:#eaff57;color:#133a1b}.header-utility{background:#133a1b;color:#eaff57}.hero-section{background:#eaff57;color:#133a1b}.button.primary,.nav-cta{background:#133a1b;color:#eaff57;border-color:#133a1b;border-radius:999px}.map-canvas{border:3px solid #133a1b;background-color:#fff}.mini-card,.finder-panel{border-radius:18px}.process-list span{background:#00a66a}",
    "flexport": "THEME .site-header{background:#f4f8ff}.header-utility{background:#0f172a;color:#a7c7ff}.hero-section{background:#f4f8ff}.button.primary,.nav-cta{background:#2563eb;color:#fff;border-color:#2563eb}.mini-card,.signature-panel,.metric-card{border-radius:12px;background:#fff}.mini-card{border-top:4px solid #ff7a1a}.map-canvas{border-color:#2563eb}.hero-media{border-radius:14px}",
    "polestar": "THEME .site-header{background:#f8f8f8;color:#111;border-bottom:1px solid #d8dadd}.header-utility{background:#111;color:#fff}.hero-section{background:#f8f8f8;text-align:center}.hero-grid{grid-template-columns:1fr}.hero-copy{margin:auto;max-width:780px}.button.primary,.nav-cta{background:#111;color:#fff;border-radius:0}.hero-media,.mini-card{border-radius:0;box-shadow:none}.mini-card{background:#fff;border-color:#d8dadd}",
    "boom": "THEME{background:#050b18;color:#fff}.site-header{background:#050b18;color:#fff}.header-utility{background:#ff6f2c;color:#050b18}.hero-section{background:linear-gradient(135deg,#050b18,#223456);color:#fff}.button.primary,.nav-cta{background:#ff6f2c;color:#050b18;border-color:#ff6f2c}.hero-media,.mini-card,.signature-panel{background:#0b1630;color:#fff;border-color:#4cc9f0;border-radius:8px}.hero-proof span{border-color:#4cc9f0}",
    "maersk": "THEME .site-header{background:#ecf8ff;color:#003a5d}.header-utility{background:#40b4e5;color:#003a5d}.hero-section{background:#ecf8ff}.button.primary,.nav-cta{background:#003a5d;color:#fff;border-color:#003a5d}.mini-card,.signature-panel,.finder-panel{border-radius:10px;background:#fff}.map-canvas{border-color:#40b4e5}.hero-media{border-radius:10px}.card-grid{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}",
    "apple": "THEME .site-header{background:rgba(245,245,247,.9);backdrop-filter:blur(20px);border-bottom:0}.header-utility{background:#f5f5f7;color:#1d1d1f;justify-content:center}.hero-section{background:#f5f5f7;text-align:center}.hero-grid{grid-template-columns:1fr}.hero-copy{margin:auto}.button.primary,.nav-cta{background:#0071e3;color:#fff;border-radius:999px}.hero-media,.mini-card,.price-card{border-radius:22px;border:0;background:#fff;box-shadow:none}.card-grid{gap:1.25rem}",
    "ssense": "THEME .site-header{background:#fff;color:#000;border-bottom:1px solid #000}.header-utility{background:#000;color:#fff}.hero-section{background:#fff}.button.primary,.nav-cta{background:#000;color:#fff;border-radius:0}.hero-media,.mini-card,.price-card,.signature-panel{border-radius:0;box-shadow:none;border-color:#000}.card-grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:0}.mini-card{border-width:0 1px 1px 0}.site-nav a{font-size:.78rem;text-transform:uppercase}",
    "jacquemus": "THEME .site-header{background:#fff2b8;color:#111}.header-utility{background:#ffde00;color:#111;justify-content:center}.hero-section{background:#fff2b8}.button.primary,.nav-cta{background:#111;color:#fff2b8;border-color:#111;border-radius:999px}.hero-media{border-radius:42px;transform:rotate(-1deg)}.mini-card{border-radius:28px;background:#fff}.mini-card:nth-child(2){transform:rotate(1deg) translateY(.6rem)}.hero-copy h1{font-size:clamp(3rem,8vw,7rem)}",
    "aesop": "THEME .site-header{background:#f3eadc;color:#35291f}.header-utility{background:#35291f;color:#f3eadc}.hero-section{background:#f3eadc}.button.primary,.nav-cta{background:#35291f;color:#fff;border-color:#35291f;border-radius:0}.hero-media,.mini-card,.form-panel{border-radius:0;box-shadow:none;border-color:#8c6a4f}.mini-card{background:#fffaf2}.section{padding-block:clamp(92px,9vw,160px)}.hero-copy h2{font-family:var(--font-accent)}",
    "verge": "THEME{background:#0b0b13;color:#fff}.site-header{background:#0b0b13;color:#fff;border-bottom:3px solid #e2127a}.header-utility{background:#fff200;color:#0b0b13}.hero-section{background:linear-gradient(135deg,#0b0b13,#210735);color:#fff}.button.primary,.nav-cta{background:#e2127a;color:#fff;border-color:#e2127a}.mini-card{background:#111827;color:#fff;border-color:#00d4ff;border-radius:0;clip-path:polygon(0 0,100% 0,100% 92%,92% 100%,0 100%)}.text-link{color:#fff200}",
    "a24": "THEME{background:#050505;color:#fff}.site-header{background:#050505;color:#fff}.header-utility{background:#181818;color:#c69a55}.hero-section{background:#050505;color:#fff}.hero-media,.visual-strip figure{border-radius:0;box-shadow:none;border:0}.button.primary,.nav-cta{background:#fff;color:#050505;border-color:#fff;border-radius:0}.mini-card,.signature-panel{background:#181818;color:#fff;border-color:#333;border-radius:0}.card-grid{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}",
    "monocle": "THEME .site-header{background:#f7efd2;color:#111;border-bottom:2px solid #111}.header-utility{background:#f6c400;color:#111}.hero-section{background:#f7efd2}.button.primary,.nav-cta{background:#111;color:#f7efd2;border-color:#111;border-radius:0}.mini-card,.price-card{border-radius:0;box-shadow:none;background:#fff;border-color:#111}.card-grid{grid-template-columns:1fr 1fr 1fr}.mini-card h3{font-family:var(--font-accent)}.footer-grid{border-top:2px solid #111}",
    "akqa": "THEME{background:#050505;color:#fff}.site-header{background:#050505;color:#fff;border-bottom:1px solid #222}.header-utility{background:#151515;color:#6bdcff}.hero-section{background:radial-gradient(circle at 70% 10%,rgba(107,220,255,.22),transparent 32%),#050505;color:#fff}.button.primary,.nav-cta{background:#fff;color:#050505;border-color:#fff;border-radius:0}.hero-media,.mini-card,.signature-panel{background:#151515;color:#fff;border-color:#333;border-radius:0}.mini-card:nth-child(2){border-color:#6bdcff}",
    "pentagram": "THEME .site-header{background:#fff;color:#111;border-bottom:2px solid #111}.header-utility{background:#e30613;color:#fff}.hero-section{background:#fff}.button.primary,.nav-cta{background:#e30613;color:#fff;border-color:#e30613;border-radius:0}.hero-media,.mini-card,.visual-strip figure{border-radius:0;box-shadow:none}.mini-card{background:#f2f2f2;border:0}.card-grid{grid-template-columns:2fr 1fr 1fr}.hero-copy h1{font-size:clamp(3.4rem,9vw,8rem)}",
    "nike": "THEME .site-header{background:#fff;color:#111}.header-utility{background:#111;color:#fff}.hero-section{background:#fff}.hero-grid{grid-template-columns:1fr}.hero-copy{max-width:900px}.hero-copy h1{text-transform:uppercase;font-weight:900}.button.primary,.nav-cta{background:#111;color:#fff;border-color:#111;border-radius:999px}.hero-media{border-radius:0;border:0;box-shadow:none}.mini-card{border-radius:20px;background:#f4f4f4}.card-grid{gap:.75rem}",
    "luma": "THEME .site-header{background:#f7f8ff;color:#111}.header-utility{background:#fff;color:#6c47ff}.hero-section{background:linear-gradient(180deg,#f7f8ff,#fff)}.button.primary,.nav-cta{background:#6c47ff;color:#fff;border-color:#6c47ff;border-radius:12px}.hero-media,.mini-card,.signature-panel{border-radius:16px;background:#fff}.mini-card{box-shadow:0 18px 45px rgba(108,71,255,.12)}.process-list span{background:#14b8a6;color:#111827}",
    "govuk": "THEME .site-header{background:#fff;color:#0b0c0c;border-bottom:10px solid #1d70b8}.header-utility{background:#0b0c0c;color:#fff}.hero-section{background:#fff}.button.primary,.nav-cta{background:#00703c;color:#fff;border-radius:0;box-shadow:0 3px 0 #002d18}.button.secondary{border-radius:0}.hero-media,.mini-card,.form-panel,.signature-panel{border-radius:0;box-shadow:none;border:2px solid #0b0c0c}.eyebrow{text-transform:none;letter-spacing:0}.site-nav a{font-weight:700}",
    "charitywater": "THEME .site-header{background:#fff;color:#111}.header-utility{background:#ffc907;color:#111}.hero-section{background:#fff}.button.primary,.nav-cta{background:#ffc907;color:#111;border-color:#ffc907;border-radius:0}.hero-media,.mini-card,.signature-panel{border-radius:0;box-shadow:none}.mini-card{border-top:8px solid #ffc907}.metric-card strong{color:#111;text-shadow:none}.cta-panel{background:#111;color:#fff}",
    "modernanimal": "THEME .site-header{background:#fff7ef;color:#21413a}.header-utility{background:#256a5e;color:#fff}.hero-section{background:#fff7ef}.button.primary,.nav-cta{background:#256a5e;color:#fff;border-color:#256a5e;border-radius:999px}.hero-media,.mini-card,.form-panel,.signature-panel{border-radius:28px;border-color:#ffb199}.mini-card{background:#fff}.card-grid{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}.process-list span{background:#ffb199;color:#21413a}",
    "rolex": "THEME{background:#081f18;color:#f4efe2}.site-header{background:#081f18;color:#f4efe2;border-bottom:1px solid rgba(212,175,55,.35)}.header-utility{background:#0b5f3a;color:#f4efe2}.hero-section{background:#081f18;color:#f4efe2}.button.primary,.nav-cta{background:#0b5f3a;color:#f4efe2;border-color:#d4af37;border-radius:0}.hero-media,.mini-card,.signature-panel{background:#0c2a20;color:#f4efe2;border-color:#d4af37;border-radius:0;box-shadow:none}.mini-card h3{color:#d4af37}",
    "jamesclear": "THEME .site-header{background:#fffdf8;color:#17233c;border-bottom:1px solid #e6dcc7}.header-utility{background:#f4f0e8;color:#17233c}.hero-section{background:#fffdf8}.hero-grid{grid-template-columns:minmax(0,.9fr) minmax(320px,.75fr)}.button.primary,.nav-cta{background:#17233c;color:#fff;border-color:#17233c;border-radius:6px}.hero-media,.mini-card,.form-panel{border-radius:6px;box-shadow:none;border-color:#e6dcc7}.mini-card{background:#fff}.lead{font-family:var(--font-accent)}",
}


TARGET_ACCESSIBILITY_PATCHES = {
    "procore": "THEME .hero-section{background-color:#111827}THEME .hero-copy{background:transparent;color:#fff;box-shadow:none}THEME .hero-copy h1,THEME .hero-copy h2,THEME .hero-copy p,THEME .hero-copy .lead,THEME .hero-copy .button.secondary{color:#fff}THEME .hero-copy .button.secondary{border-color:#fff}THEME .signature-panel p,THEME .signature-panel .eyebrow,THEME .signature-panel h3{color:#111827}",
    "octopus": "THEME .mini-card,THEME .mini-card:nth-child(odd),THEME .signature-panel{background:#f6f1ff;color:#140021;border-color:#ff4fd8}THEME .mini-card h3,THEME .signature-panel h3,THEME .signature-panel .eyebrow,THEME .signature-panel output{color:#140021}THEME .button.secondary{color:#f6f1ff;border-color:#f6f1ff}",
    "polestar": "THEME .site-nav a,THEME .brand small{color:#111}THEME .mini-card,THEME .mini-card:nth-child(odd),THEME .price-card,THEME .form-panel,THEME .faq-list details,THEME .signature-panel,THEME .finder-panel,THEME .map-list article,THEME .process-list li{background:#fff;color:#111;border-color:#d8dadd;box-shadow:none}THEME .hero-copy p,THEME .mini-card h3,THEME .price-card h3,THEME .signature-panel h3,THEME .signature-panel .eyebrow,THEME .signature-panel p,THEME .finder-panel p,THEME .finder-panel span,THEME .process-list h3,THEME .process-list p,THEME .lead,THEME .text-link{color:#111}THEME .hero-proof span{background:#fff;color:#111;border-color:#d8dadd}THEME .content-section:nth-of-type(even){background:#f8f8f8;color:#111}THEME .button.secondary{color:#111;border-color:#111}",
    "maersk": "THEME .site-nav a,THEME .brand small{color:#003a5d}THEME .mini-card,THEME .mini-card:nth-child(odd),THEME .price-card,THEME .form-panel,THEME .faq-list details,THEME .signature-panel,THEME .finder-panel,THEME .map-list article,THEME .process-list li{background:#fff;color:#003a5d;border-color:#9ad7f5;box-shadow:none}THEME .hero-copy p,THEME .mini-card h3,THEME .price-card h3,THEME .signature-panel h3,THEME .signature-panel .eyebrow,THEME .signature-panel p,THEME .finder-panel p,THEME .finder-panel span,THEME .process-list h3,THEME .process-list p,THEME .lead,THEME .text-link{color:#003a5d}THEME .hero-proof span{background:#fff;color:#003a5d;border-color:#9ad7f5}THEME .content-section:nth-of-type(even){background:#ecf8ff;color:#003a5d}THEME .button.secondary{color:#003a5d;border-color:#003a5d}",
    "charitywater": "THEME .cta-panel{background:#111;color:#fff}THEME .cta-panel h2,THEME .cta-panel p,THEME .cta-panel .eyebrow{color:#fff}",
}


TARGET_VISUAL_KIND = {
    "neko": "scan",
    "recursion": "pipeline",
    "ritual": "shelf",
    "cloudflare": "network",
    "linear": "board",
    "starlink": "space",
    "wiz": "security",
    "atlan": "data",
    "wise": "calculator",
    "lemonade": "quote",
    "clio": "workflow",
    "xero": "ledger",
    "ideo": "studio",
    "masterclass": "cinema",
    "jungle": "jobs",
    "modernhouse": "property",
    "procore": "construction",
    "snohetta": "architecture",
    "wearstler": "moodboard",
    "formlabs": "spec",
    "arup": "engineering",
    "tesla": "product",
    "octopus": "utility",
    "watershed": "climate",
    "aerofarms": "farm",
    "oatly": "poster",
    "sketch": "restaurant",
    "aman": "retreat",
    "blacktomato": "travel",
    "citymapper": "route",
    "flexport": "freight",
    "polestar": "vehicle",
    "boom": "aero",
    "maersk": "shipping",
    "apple": "store",
    "ssense": "catalogue",
    "jacquemus": "campaign",
    "aesop": "apothecary",
    "verge": "media",
    "a24": "posterwall",
    "monocle": "print",
    "akqa": "agency",
    "pentagram": "design",
    "nike": "sport",
    "luma": "events",
    "govuk": "service",
    "charitywater": "impact",
    "modernanimal": "clinic",
    "rolex": "maison",
    "jamesclear": "author",
}

TARGET_PALETTE_OVERRIDES = {
    "lemonade": ("#fff2f7", "#ff0083", "#ffb3d9", "#251024", "#ffffff"),
    "ideo": ("#ffffff", "#111111", "#ff5a1f", "#111111", "#0066ff"),
    "masterclass": ("#050505", "#ffffff", "#d71920", "#ffffff", "#b28b55"),
    "jungle": ("#ffe45e", "#111111", "#ff6a3d", "#111111", "#1f6feb"),
    "modernhouse": ("#fbfaf7", "#111111", "#8a8f83", "#111111", "#c7b299"),
    "snohetta": ("#f4f1eb", "#111111", "#c4c7c5", "#111111", "#7a807b"),
    "arup": ("#ffffff", "#e21b2d", "#111111", "#111111", "#7f8c8d"),
    "tesla": ("#f7f7f7", "#111111", "#e82127", "#111111", "#bfc7d5"),
    "oatly": ("#f5ead2", "#004b8d", "#f26b3a", "#111111", "#ffdf3d"),
    "citymapper": ("#eaff57", "#133a1b", "#00a66a", "#133a1b", "#ffffff"),
    "polestar": ("#f8f8f8", "#111111", "#d8dadd", "#111111", "#8a8f98"),
    "maersk": ("#ecf8ff", "#40b4e5", "#9ad7f5", "#003a5d", "#003a5d"),
    "apple": ("#f5f5f7", "#1d1d1f", "#0071e3", "#1d1d1f", "#a1a1a6"),
    "ssense": ("#ffffff", "#000000", "#777777", "#000000", "#d9d9d9"),
    "jacquemus": ("#fff2b8", "#111111", "#ffde00", "#111111", "#d97b4f"),
    "verge": ("#0b0b13", "#e2127a", "#fff200", "#ffffff", "#00d4ff"),
    "monocle": ("#f7efd2", "#111111", "#f6c400", "#111111", "#8c1d18"),
    "pentagram": ("#ffffff", "#111111", "#e30613", "#111111", "#0057ff"),
    "nike": ("#ffffff", "#111111", "#ff3d00", "#111111", "#c8c8c8"),
    "luma": ("#f7f8ff", "#6c47ff", "#14b8a6", "#111827", "#ffb703"),
    "govuk": ("#ffffff", "#1d70b8", "#ffdd00", "#0b0c0c", "#ffdd00"),
    "charitywater": ("#ffffff", "#ffc907", "#2b6cb0", "#111111", "#ffc907"),
}

PREMIUM_DIRECTION_LINES = """
1|Soft clinical care journey with calm white space, rounded panels, appointment pathway, patient reassurance proof, gentle form flow.|calm clinical|fear reduction and care confidence|clinical journey|spacious|soft clinical cards|lab white panels|soft light clinical spaces with human detail|appointment pathway|reassuring appointment CTA|consultation fees pathway|patient guide library|care route drawer|calm consent card|plain safety notes
2|Research dossier with lab-white surfaces, pipeline timeline, publication cards, eligibility logic, precise diagrams.|research-grade|evidence and scientific credibility|research dossier|compact|precise dossier panels|lab white surfaces|molecular diagrams and publication visuals|pipeline tabs|partner research CTA|trial eligibility tiers|publication archive|institutional directory drawer|technical consent strip|ethics and protocol notes
3|Warm lifestyle studio with soft capsules, routine builder, tactile textures, transformation proof, journal-like resources.|warm lifestyle|personal improvement and reassurance|routine studio|relaxed|organic wellness curves|soft tactile texture|routine scenes, skin, light, and calm interiors|routine quiz|gentle consultation CTA|session packages|self-care journal|soft studio overlay|warm consent capsule|suitability notes
4|Infrastructure operations console with topology hero, status strips, support modules, system diagrams, ticket routing.|operational|uptime and operational control|ops command|dense|technical modules|dashboard panels|networks, devices, topology and support desks|status selector|audit request CTA|support retainer matrix|support documentation hub|ops drawer|status consent bar|SLA and support notes
5|Product-led dashboard site with UI mockups, feature tabs, integration filters, pricing toggle, clean product documentation feel.|product-led|speed, clarity, and product confidence|SaaS dashboard|medium|pill product modules|polished app panels|screens, workflows, integrations and dashboards|feature tabs|demo CTA|plan comparison toggle|product resource hub|product menu sheet|clean consent panel|product limits notes
6|Coverage checker experience with map surfaces, signal lines, speed tiles, outage banner, address-check form.|coverage-led|availability and reliability|coverage map|practical|signal tiles|map surface|coverage maps, routers, cable routes and homes|coverage checker|coverage CTA|plan speed cards|coverage guide centre|availability drawer|utility consent bar|availability notes
7|Dark command centre with sharp panels, risk matrix, incident stepper, terminal labels, compliance proof.|controlled risk|privacy and threat reduction|threat command|dense|sharp dark panels|dark console glass|risk maps, threat dashboards and abstract networks|risk matrix|secure audit CTA|audit and retainer cards|threat intel library|incident command drawer|security consent console|confidentiality notes
8|KPI workbench with compact dashboards, metric cards, chart surfaces, dataset filters, tool-stack selector.|analytical|decision clarity and visibility|KPI workbench|dense|metric cards|dashboard surfaces|charts, data rooms, BI panels and reports|dashboard filters|dashboard brief CTA|reporting packages|data library|analytics drawer|metric consent panel|data handling notes
9|Regulated advisory system with navy/ivory/gold restraint, risk toggles, calculator cards, trust/legal footer.|regulated trust|security and suitability|advisory calculator|measured|advisory note cards|matte document surfaces|secure offices, plans and financial documents|risk toggles|advisor call CTA|fee and advisory model|finance guides hub|regulated side drawer|trust consent notice|risk disclaimer notes
10|Claims and cover comparison journey with policy cards, stepper, quote logic, reassurance proof, exclusions clarity.|protective|family and asset protection|claims pathway|practical|cover comparison cards|policy paper surfaces|families, assets, claims and policy documents|claims stepper|quote CTA|premium factors cards|claims resource hub|quote drawer|policy consent panel|exclusion notes
11|Private formal case pathway with document checklists, jurisdiction footer, restrained serif typography, consultation routing.|formal private|privacy and legal certainty|case pathway|measured|document checklist cards|formal paper surfaces|documents, consultation rooms and legal records|case selector|consultation CTA|fixed/hourly fee cards|legal document library|case drawer|legal consent notice|jurisdiction notes
12|Deadline command layout with tax calendar, ledger tables, document checklist, compact filing support cards.|deadline-led|order and compliance|filing control|compact|ledger blocks|document and calendar surfaces|records, payroll, tax calendars and ledgers|deadline calendar|quote CTA|filing package grid|tax checklist hub|deadline drawer|admin consent strip|filing notes
13|Executive strategy framework with diagnosis modules, roadmap visuals, case filters, boardroom-style restraint.|executive|clarity, leverage and measurable progress|strategy framework|medium|framework cards|boardroom matte surfaces|roadmaps, whiteboards and operating models|diagnostic quiz|brief CTA|workshop/project/retainer cards|insight archive|executive drawer|brief consent panel|strategy scope notes
14|Learning pathway with level selector, course cards, progress markers, timetable interaction, supportive tone.|supportive|confidence and progress|learning pathway|medium|course path cards|friendly paper surfaces|classrooms, learners, materials and progress visuals|level selector|trial CTA|lesson packages|learning resources|school menu sheet|learning consent card|progress notes
15|Employer/candidate split system with role routing, CV flow, dual CTAs, people-first proof.|human career|matching confidence for two audiences|talent split|medium|split audience panels|workplace surfaces|people at work, interviews and hiring journeys|audience toggle|hiring CTA|placement fee cards|HR insight hub|dual audience drawer|career consent panel|candidate notes
16|Search-led property experience with listings, map-area guides, gallery modal, valuation form, local proof.|local visual|market confidence and discovery|property search|image-rich|listing cards|map and listing surfaces|properties, interiors, streets and local maps|property filter|valuation CTA|commission and management cards|area guide archive|property search drawer|listing consent panel|market notes
17|Strong project delivery system with slab layouts, before/after slider, estimate form, safety and handover proof.|practical strong|certainty around cost and disruption|project timeline|dense|industrial slabs|site material surfaces|sites, crews, materials and finished builds|project estimator|estimate CTA|stage cost panels|build guide hub|sitework drawer|project consent block|safety notes
18|Spatial editorial portfolio with full-bleed project imagery, thin rules, project index, slow reveal motion.|spatial editorial|taste and design authority|architectural portfolio|spacious|editorial rectangles|paper and concrete surfaces|spaces, drawings, materials and site plans|project gallery|project brief CTA|stage fee cards|design journal|studio index overlay|minimal consent line|planning notes
19|Tactile moodboard system with material swatches, room selector, refined warm palette, style brief form.|tactile refined|taste and home confidence|moodboard commerce|image-rich|material swatches|fabric and paper surfaces|rooms, textiles, finishes and moodboards|room selector|design CTA|styling package cards|materials journal|moodboard drawer|soft consent tile|sourcing notes
20|Industrial specification site with dense capability tables, facility gallery, QA proof, RFQ flow.|industrial|capacity and quality confidence|specification sheet|dense|hard spec blocks|metal and factory surfaces|machines, production lines and QA benches|capability filter|RFQ CTA|volume/spec quote table|datasheet library|spec drawer|industrial consent strip|tolerance notes
21|Technical validation site with diagrams, compliance checklist, system tabs, precise modular cards.|validated|reliability and standards|system diagram|dense|validation cards|technical document surfaces|diagrams, test equipment and controls|diagram tabs|engineer CTA|scope estimate cards|technical library|engineering drawer|compliance consent panel|standards notes
22|Savings calculator system with output counters, solar/battery toggles, bill form, project yield proof.|future savings|cost reduction and resilience|savings calculator|medium|output metric cards|energy monitoring surfaces|solar, batteries, installs and monitoring panels|savings estimator|savings CTA|project output calculator|energy guide hub|calculator drawer|energy consent panel|assumption notes
23|Essential service portal with alert strip, service tiles, report filters, practical civic forms.|civic essential|public service access|service portal|practical|square service tiles|civic document surfaces|infrastructure, plants, counters and public notices|service finder|request CTA|service route cards|public report archive|civic directory menu|public consent bar|eligibility notes
24|ESG evidence site with impact metrics, report archive, field imagery, methodology proof.|impact evidence|accountability and measurable change|impact report|medium|impact metric cards|field report surfaces|fieldwork, climate data, ESG reports and biodiversity|impact filters|audit CTA|audit roadmap cards|report archive|evidence drawer|ESG consent panel|methodology notes
25|Seasonal planner with product/advice cards, rural practical tone, calendar interaction, order/visit form.|rural practical|seasonal timing and trust|seasonal planner|practical|seasonal product cards|earth and field surfaces|fields, crops, equipment and rural work|season calendar|visit CTA|season package cards|advice library|rural supply drawer|seasonal consent strip|availability notes
26|Ingredient-led product shelf with allergen filters, stockist finder, recipe tabs, packaging closeups.|ingredient-led|quality, safety and taste|product shelf|image-rich|ingredient cards|packaging and kitchen surfaces|ingredients, packaging, kitchen craft and stockists|allergen filter|trade CTA|trade pack cards|recipe and stockist hub|product drawer|ingredient consent card|allergen notes
27|Sensory reservation-first site with food photography, menu cards, allergen toggle, booking widget, warm atmosphere.|sensory warm|desire and social confidence|menu reservation|image-rich|menu cards|warm dining surfaces|close food, dining room, chef and table details|reservation widget|reserve CTA|menu/package cards|menu and story archive|booking bottom sheet|restaurant consent card|menu notes
28|Room booking experience with room cards, amenity tabs, offers, local experience imagery, booking panel.|restful hospitality|comfort and availability|room booking|image-rich|room cards|hotel linen surfaces|rooms, lobby, views, amenities and local experiences|booking filters|availability CTA|room rate cards|stay guide hub|booking sheet|guest consent panel|policy notes
29|Destination editorial site with trip cards, itinerary accordion, map textures, place-led storytelling.|destination-led|wanderlust and practical planning|destination magazine|spacious|trip story cards|map and paper surfaces|destinations, maps, guides and local experiences|trip finder|trip CTA|trip package cards|destination stories|travel index overlay|travel consent strip|itinerary notes
30|Route and fleet planner with fare estimate, timetable cards, route selector, safety proof.|route-led|safe reliable movement|route planner|practical|route cards|transit map surfaces|vehicles, routes, passengers and city movement|fare estimate|ride CTA|fare route cards|route guide hub|route drawer|transport consent panel|fare notes
31|Tracking command system with network map, quote calculator, shipment cards, warehouse/status visuals.|networked|visibility and delivery control|tracking command|dense|tracking cards|warehouse dashboard surfaces|warehouses, routes, parcels and hubs|tracking mockup|quote CTA|shipment quote calculator|logistics resource hub|tracking drawer|status consent bar|delivery notes
32|Dark polished showroom with vehicle cards, finance calculator, inventory filters, test-drive flow.|showroom performance|purchase confidence and desire|vehicle showroom|image-rich|vehicle cards|polished showroom surfaces|vehicles, interiors, workshops and charging|inventory filter|test-drive CTA|finance calculator cards|vehicle guide hub|showroom drawer|dealer consent panel|finance notes
33|Premium operations layout with fleet specs, safety checklist, charter route form, hangar/control-room imagery.|aviation precision|safety and premium reliability|flight operations|spacious|fleet spec cards|aviation console surfaces|aircraft, hangars, ops rooms and safety docs|fleet tabs|charter CTA|charter route cards|safety archive|aviation ops drawer|aviation consent strip|charter notes
34|Port operations system with vessel cards, cargo quote, schedule panels, marine blue/teal surfaces.|marine operations|cargo reliability and reach|port operations|dense|vessel cards|marine chart surfaces|vessels, ports, cargo routes and crew operations|vessel filter|shipping CTA|cargo quote cards|port resource hub|marine drawer|port consent panel|cargo notes
35|Shopfront category system with product tiles, offer bands, loyalty form, store finder, seasonal merchandising.|shopfront|convenience and offer discovery|retail shopfront|medium|product tiles|shelf and offer surfaces|shopfronts, products, shelves and customers|category filter|shop CTA|offer bundle cards|store guide hub|catalogue drawer|retail consent tile|stock notes
36|Marketplace catalogue with seller/customer split, trust badges, support routing, product filters.|marketplace|speed and transaction trust|marketplace catalogue|compact|catalogue cards|marketplace panel surfaces|catalogue, sellers, carts, delivery and support|catalogue filter|market CTA|seller/customer route cards|market resource hub|marketplace drawer|checkout consent panel|seller notes
37|Campaign lookbook with dramatic image rhythm, collection filters, size guide, editorial whitespace.|fashion editorial|taste, status and movement|lookbook campaign|theatrical|lookbook cards|campaign paper surfaces|editorial campaign, fabric, movement and styling|lookbook slider|collection CTA|collection drop cards|style journal|campaign overlay menu|minimal fashion consent|size notes
38|Texture and routine site with ingredient glossary, product education cards, soft forms, closeup imagery.|texture-led|self-care confidence|beauty routine|relaxed|soft product capsules|texture and ingredient surfaces|textures, ingredients, routines and product closeups|routine finder|routine CTA|routine bundle cards|ingredient glossary|beauty drawer|beauty consent capsule|ingredient notes
39|Broadcast schedule system with show cards, episode filters, audience proof, advertise kit download.|broadcast|audience reach and timing|broadcast schedule|compact|episode cards|studio schedule surfaces|studios, microphones, video and audience data|schedule filter|advertise CTA|sponsorship cards|episode archive|schedule drawer|media consent bar|ad notes
40|High-energy ticketing site with dark stage visuals, event calendar, artist filter, venue cards.|live energy|excitement and access|ticket stage|theatrical|event cards|dark stage surfaces|stage, lights, crowds, artists and venue details|ticket selector|ticket CTA|ticket tier cards|event archive|stage drawer|ticket consent panel|access notes
41|Knowledge archive with library search, author filter, paper-like surfaces, newsletter modal.|knowledge editorial|authority and discovery|library archive|medium|article cards|paper archive surfaces|books, reports, editorial desks and archives|library search|subscribe CTA|subscription cards|author archive|library index overlay|archive consent line|source notes
42|Campaign results site with case cards, performance tabs, creative assets, brief form.|campaign performance|results and creative confidence|case study system|medium|campaign case cards|creative board surfaces|campaign assets, creative reviews and analytics boards|case filter|brief CTA|campaign package cards|case study archive|agency drawer|brief consent panel|result notes
43|Studio portfolio wall with project lightbox, production textures, file upload, visual case studies.|visual craft|taste and production trust|portfolio wall|spacious|portfolio cards|studio production surfaces|sets, cameras, design boards and production details|portfolio lightbox|project CTA|production package cards|project archive|studio overlay menu|creative consent card|usage notes
44|Class schedule system with coach selector, membership toggle, program cards, energetic motion.|active community|progress and belonging|class schedule|medium|program cards|training floor surfaces|training spaces, classes, coaches and community moments|timetable filter|trial CTA|membership cards|program guide hub|club drawer|fitness consent panel|health notes
45|Moodboard planning experience with venue filters, package calculator, portfolio cards, date enquiry.|celebratory planning|emotion and confidence|event moodboard|image-rich|event portfolio cards|venue and linen surfaces|weddings, tablescapes, venues and production details|event planner|date CTA|package calculator cards|planning journal|event bottom sheet|event consent card|date notes
46|High-contrast public-service portal with service search, form finder, document filters, square practical containers.|plain civic|public service access|civic portal|practical|square civic boxes|public document surfaces|public buildings, forms, notices and counters|service search|start request CTA|service eligibility cards|document centre|service directory menu|civic consent notice|eligibility notes
47|Transparent impact site with donation selector, impact calculator, volunteer filter, human proof.|urgent transparent|trust and contribution|donation impact|medium|impact cards|community report surfaces|community, volunteers, reports and outcomes|donation selector|donate CTA|donation impact cards|impact reports|donation drawer|donor consent card|fundraising notes
48|Warm urgent-care site with emergency symptom helper, care guide cards, appointment form.|compassionate urgent|care and quick triage|emergency care|practical|care cards|warm clinical surfaces|clinic rooms, pet care, emergency routes and team details|symptom helper|appointment CTA|care plan cards|care guide hub|emergency drawer|vet consent card|care notes
49|Quiet maison experience with black/ivory/champagne, hairline borders, private invitation, concierge stepper.|quiet exclusive|status and discretion|private invitation|ultra-minimal|luxury hairline borders|matte black and champagne surfaces|craft details, private spaces and premium materials|private reveal|private access CTA|concierge invitation cards|maison journal|private access overlay|discreet consent line|discretion notes
50|Editorial media-kit site with press assets, speaking selector, media filters, newsletter and booking routes.|authoritative editorial|authority and booking confidence|media kit|spacious|media cards|editorial press surfaces|portraits, stages, podcasts, writing desks and press assets|media filter|appearance CTA|speaking rate cards|press resource hub|media index overlay|press consent panel|booking notes
""".strip()


PALETTES = [
    ("#f6fbff", "#0f6b7b", "#8bd3dd", "#103b4a", "#f2c94c"),
    ("#f8f7ff", "#243c8f", "#7c3aed", "#111827", "#16a34a"),
    ("#fff8f4", "#9b5f48", "#f0b89a", "#3d2d2a", "#6aa84f"),
    ("#f3f8fb", "#145f82", "#35a2a8", "#132f3a", "#ffb703"),
    ("#f7f9ff", "#2d4fdd", "#31c48d", "#141a33", "#f97316"),
    ("#f5fbff", "#0b72b9", "#00a6a6", "#0d2b45", "#ffd166"),
    ("#f4f7f6", "#0f3d3e", "#00b894", "#111827", "#ef476f"),
    ("#f6f8fb", "#334e68", "#3b82f6", "#102a43", "#f59e0b"),
    ("#f7f5ef", "#264653", "#2a9d8f", "#1f2937", "#e9c46a"),
    ("#f8fafc", "#1d4ed8", "#0891b2", "#0f172a", "#f97316"),
    ("#f7f7f5", "#374151", "#b45309", "#111827", "#84cc16"),
    ("#f9faf5", "#4d7c0f", "#65a30d", "#283618", "#facc15"),
    ("#f5f7fb", "#1e3a8a", "#64748b", "#111827", "#f59e0b"),
    ("#fffdf6", "#7c2d12", "#f59e0b", "#1f2937", "#10b981"),
    ("#f8fbff", "#075985", "#0ea5e9", "#172554", "#f97316"),
    ("#fbf8f2", "#3f6212", "#a3a380", "#1f2937", "#d97706"),
    ("#f8f6f2", "#525252", "#b45309", "#1c1917", "#eab308"),
    ("#f7f4ef", "#2f3e46", "#8d99ae", "#1b1b1b", "#bc6c25"),
    ("#fffaf5", "#6b4e3d", "#d6a77a", "#2d2420", "#729b79"),
    ("#f3f4f6", "#374151", "#f97316", "#111827", "#22c55e"),
    ("#f4f7f8", "#164e63", "#14b8a6", "#111827", "#f59e0b"),
    ("#f6fff8", "#15803d", "#facc15", "#14532d", "#0ea5e9"),
    ("#f2f7f7", "#155e75", "#06b6d4", "#083344", "#f97316"),
    ("#f7fbf4", "#166534", "#84cc16", "#1f2937", "#06b6d4"),
    ("#fff8ed", "#854d0e", "#84cc16", "#292524", "#0ea5e9"),
    ("#fff7ed", "#9a3412", "#f97316", "#431407", "#22c55e"),
    ("#fffaf0", "#991b1b", "#f59e0b", "#1f2937", "#16a34a"),
    ("#f7fbff", "#1d4ed8", "#93c5fd", "#0f172a", "#f97316"),
    ("#fff7ed", "#b45309", "#14b8a6", "#1f2937", "#a855f7"),
    ("#f8fafc", "#0f766e", "#38bdf8", "#111827", "#f59e0b"),
    ("#f8fafc", "#374151", "#22c55e", "#111827", "#f97316"),
    ("#f8fafc", "#1e40af", "#ef4444", "#111827", "#f59e0b"),
    ("#f7fbff", "#075985", "#38bdf8", "#0f172a", "#f97316"),
    ("#f4f8fb", "#0e7490", "#14b8a6", "#0f172a", "#f59e0b"),
    ("#fffdf5", "#7c2d12", "#f59e0b", "#1f2937", "#16a34a"),
    ("#f8fbff", "#4338ca", "#ec4899", "#111827", "#22c55e"),
    ("#fff7f7", "#be123c", "#f9a8d4", "#3f1d2b", "#f59e0b"),
    ("#fff8fb", "#9d174d", "#f472b6", "#3b1d2a", "#22c55e"),
    ("#f8fafc", "#1e293b", "#0ea5e9", "#0f172a", "#f97316"),
    ("#0f1117", "#e11d48", "#f97316", "#f8fafc", "#22c55e"),
    ("#fbfaf7", "#374151", "#a16207", "#111827", "#0ea5e9"),
    ("#f8fafc", "#0f766e", "#f97316", "#111827", "#a855f7"),
    ("#f7f3ee", "#111827", "#b45309", "#1f2937", "#14b8a6"),
    ("#f6fbf7", "#15803d", "#22c55e", "#14532d", "#f97316"),
    ("#fff8f6", "#be123c", "#fb7185", "#3b1f2b", "#f59e0b"),
    ("#f8fafc", "#1d4ed8", "#38bdf8", "#0f172a", "#22c55e"),
    ("#f8fff8", "#166534", "#22c55e", "#111827", "#f97316"),
    ("#fffaf7", "#92400e", "#f59e0b", "#3d2d2a", "#14b8a6"),
    ("#0f0e0c", "#b68d40", "#f5e6c8", "#faf7ef", "#7dd3fc"),
    ("#f8fafc", "#7c3aed", "#06b6d4", "#111827", "#f97316"),
]


DIVERSITY_LINES = """
1|Calm clinical, soft, reassuring|Patient journey + appointment pathway|appointment panel|calm appointment header|care route sitemap|soft reassurance cards|appointment pathway form|gentle fade and reassurance reveal|clean clinical spaces, soft light, patient-care details|standards and care notes
2|Research-grade, technical, precise|Pipeline + publication architecture|pipeline timeline|institutional research header|publication archive footer|evidence dossier cards|trial eligibility form|precise pathway reveal|labs, molecules, research diagrams, publication visuals|papers, pipeline, and ethics evidence
3|Soft lifestyle, personal, warm|Routine + transformation journey|routine builder|wellness studio header|self-care journal footer|routine cards|service fit form|soft image and routine transitions|warm treatment spaces, routines, textures, calm lifestyle|results and suitability proof
4|Reliable systems, operational clarity|Infrastructure + support command layout|system topology|operations support header|support desk footer|infrastructure modules|ticket route form|status panel transitions|cloud systems, networks, support desks, devices|uptime and support proof
5|Product-led, clean, digital|Dashboard + feature/product flow|dashboard product|product demo header|resource hub footer|product module cards|demo request form|snappy tab transitions|product screens, workflow diagrams, integrations|product usage and integrations proof
6|Coverage, speed, connectivity|Plan + coverage checker layout|coverage map|availability checker header|coverage support footer|coverage tiles|address check form|coverage pulse and plan reveal|coverage maps, routers, cable routes, home and business setups|reliability and area proof
7|Dark, controlled, high-risk|Threat/risk command centre|threat command|incident response header|security evidence footer|dark risk panels|secure audit form|scan-line and risk-state transitions|dark interfaces, abstract networks, risk maps|compliance and response proof
8|Dashboard, metrics, intelligence|KPI/reporting interface|KPI dashboard|analytics workbench header|data library footer|metric cards|dashboard brief form|number and filter transitions|dashboards, charts, data rooms, decision panels|visibility and decision proof
9|Trust, restraint, security|Advice + risk clarity layout|advisory calculator|regulated advice header|trust/legal footer|advisory note cards|appointment form|calm risk toggle transitions|secure offices, documents, planning sessions, restrained finance visuals|risk and suitability proof
10|Protection, comparison, reassurance|Cover + claims journey|claims pathway|quote and claims header|policy support footer|cover comparison cards|quote logic form|stepper and cover reveal|families, assets, policy documents, claims support|limits, exclusions, and support proof
11|Formal, private, structured|Case/document/process pathway|case route|formal legal header|jurisdiction footer|document checklist cards|case type form|measured document reveal|offices, documents, privacy-first consultation rooms|jurisdiction and document proof
12|Organised, deadline-led, precise|Tax/payroll/document flow|deadline control|deadline bar header|filing support footer|deadline cards|document checklist form|calendar and checklist transitions|records, ledgers, payroll flows, tax calendars|deadline and compliance proof
13|Strategic, executive, framework-led|Diagnosis + roadmap layout|strategy framework|executive advisory header|insight archive footer|framework cards|diagnostic form|framework tab transitions|boardrooms, whiteboards, roadmaps, operating models|diagnostic and roadmap proof
14|Clear, supportive, progress-focused|Course + learning pathway|learning path|school pathway header|learning resource footer|course path cards|placement form|progress and timetable transitions|classrooms, learners, course materials, progress visuals|outcomes and learning proof
15|Dual audience, human, career-led|Employer/candidate split|dual audience|employer talent header|candidate support footer|split audience cards|role routing form|toggle and matching transitions|people at work, hiring conversations, candidate journeys|placement and retention proof
16|Search-led, visual, local|Listings + area guide|property search|property search header|area guide footer|listing cards|valuation form|filter and gallery transitions|property interiors, streets, maps, local area visuals|market and area proof
17|Practical, strong, project-led|Project timeline + before/after|project timeline|site-work header|handover footer|build stage cards|project estimate form|before-after and timeline reveal|sites, materials, crews, inspections, finished builds|process and safety proof
18|Editorial, spatial, visual|Project portfolio + large imagery|architectural masthead|studio editorial header|project index footer|large project cards|project brief form|slow spatial image reveal|spaces, drawings, materials, context, site plans|portfolio and planning proof
19|Tactile, moodboard, refined|Rooms + materials + shop|moodboard|studio moodboard header|materials footer|material swatch cards|style brief form|palette and room transitions|rooms, fabrics, finishes, furniture, moodboards|materials and project proof
20|Industrial, capability-led|Specs + quality + facilities|factory floor|industrial spec header|capability footer|specification cards|RFQ form|mechanical panel transitions|machines, production lines, QA benches, materials|quality and capacity proof
21|Technical, validated, precise|Systems + diagrams + compliance|system diagram|engineering header|technical document footer|validation cards|engineering scope form|diagram and compliance reveal|technical diagrams, sites, test equipment, controls|standards and validation proof
22|Future-focused, savings-led|Calculator + project output|savings calculator|energy savings header|project output footer|output metric cards|site bill form|counter and savings reveal|solar, batteries, monitoring panels, bills, installs|savings and assumptions proof
23|Civic, essential, reliable|Service access + reports|service access|public alert header|public service footer|service request tiles|service request form|minimal alert transitions|infrastructure, plants, service counters, public notices|service and report proof
24|Impact, ESG, evidence|Metrics + reports + roadmap|impact report|ESG evidence header|report archive footer|impact metric cards|audit advisory form|metric and report reveal|fieldwork, climate data, ESG reports, biodiversity|impact and methodology proof
25|Rural, seasonal, practical|Seasonal advice + products|seasonal planner|rural supply header|seasonal footer|seasonal product cards|visit and order form|seasonal calendar transitions|fields, crops, equipment, livestock, rural work|product and advice proof
26|Ingredient-led, quality-led|Product + stockist + recipe|product shelf|food brand header|stockist footer|ingredient cards|trade enquiry form|product and allergen reveal|ingredients, packaging, kitchen craft, stockists|quality and allergen proof
27|Sensory, warm, booking-first|Menu + reservation + gallery|food hero|reservation header|location and hours footer|menu item cards|reservation form|menu and gallery transitions|close food photography, dining room, chef, table details|menu and booking proof
28|Hospitality, rooms, experience|Booking + rooms + offers|room booking|hotel booking header|stay support footer|room cards|booking panel form|gallery and booking reveal|rooms, lobby, views, amenities, local experiences|availability and policy proof
29|Destination-led, editorial|Trips + places + stories|destination masthead|travel planning header|destination footer|trip cards|trip planner form|itinerary and map transitions|destinations, maps, guides, local experiences|itinerary and safety proof
30|Safe, reliable, route-led|Routes + fleet + booking|route booking|route service header|fleet support footer|route cards|fare estimate form|route and fleet transitions|vehicles, routes, passengers, airport and city movement|safety and reliability proof
31|Networked, tracking-led|Tracking + network + quote|tracking command|tracking header|network footer|tracking cards|quote calculator form|status and map transitions|warehouses, routes, parcels, dashboards, hubs|tracking and network proof
32|Inventory, performance, showroom|Vehicles + finance + workshop|showroom search|dealer showroom header|service bay footer|vehicle cards|test-drive form|inventory and finance transitions|vehicles, showroom, workshop, interiors, charging|inventory and service proof
33|Safety, precision, premium|Fleet + compliance + operations|flight operations|aviation ops header|compliance footer|fleet specification cards|charter route form|flight spec transitions|aircraft, hangars, operations rooms, safety documents|safety and compliance proof
34|Port, vessel, cargo, reliability|Fleet + ports + tracking|port operations|marine ops header|port support footer|vessel cards|cargo quote form|port and vessel transitions|vessels, ports, cargo, routes, crew operations|capacity and tracking proof
35|Shopfront, offers, categories|Product/category/loyalty|shopfront|retail offer header|store finder footer|product cards|loyalty signup form|category and offer reveal|shopfronts, products, shelves, customers, seasonal offers|store and loyalty proof
36|Marketplace, catalogue, trust|Shop + seller/customer paths|marketplace search|marketplace header|seller support footer|catalogue cards|support routing form|catalogue and route transitions|catalogue, seller tools, carts, delivery, support|trust and checkout proof
37|Editorial, campaign, lookbook|Lookbook + collection + shop|lookbook campaign|fashion campaign header|stockist footer|lookbook cards|styling enquiry form|slide and reveal transitions|editorial campaign, fabric texture, movement, styling|craft and collection proof
38|Texture, routine, ingredients|Routine finder + product education|routine finder|beauty routine header|ingredient footer|product education cards|routine advice form|texture and routine transitions|textures, ingredients, routines, product close-ups|ingredient and results proof
39|Broadcast, schedule, audience|Shows + schedule + content|broadcast schedule|media schedule header|audience footer|episode cards|advertise kit form|schedule and episode reveal|studios, shows, microphones, video, audience data|reach and standards proof
40|Energy, events, tickets|Shows + artists + tickets|ticket stage|event ticket header|venue footer|event cards|ticket enquiry form|event and ticket reveal|stage, lights, crowds, artists, venue details|event and access proof
41|Knowledge, archive, editorial|Library + articles + authors|library masthead|editorial library header|archive footer|article cards|newsletter form|search and author transitions|books, reports, editorial desks, archives|sources and editorial proof
42|Campaign, results, creative strategy|Work + strategy + results|campaign case|agency work header|case study footer|campaign case cards|brief form|case and result transitions|campaign assets, creative reviews, analytics boards|work and result proof
43|Portfolio, studio, visual craft|Work + process + project lightbox|portfolio wall|creative studio header|project footer|portfolio cards|creative brief form|project lightbox transitions|sets, cameras, design boards, production details|portfolio and usage proof
44|Energy, progress, community|Programs + classes + schedule|class schedule|club schedule header|community footer|program cards|trial class form|timetable and coach transitions|training spaces, classes, coaches, community moments|progress and class proof
45|Emotion, planning, visual proof|Weddings/events + portfolio|event moodboard|planning studio header|venue and supplier footer|event portfolio cards|date enquiry form|venue and package reveal|weddings, tablescapes, venues, production details|portfolio and planning proof
46|Accessible, plain, civic|Services + forms + support|public service search|accessible civic header|service directory footer|service tiles|public request form|minimal service transitions|public buildings, forms, notices, service counters|transparency and eligibility proof
47|Human, urgent, transparent|Cause + impact + donate|donation impact|donation header|impact footer|impact cards|donation form|impact and volunteer reveal|community, volunteers, reports, transparent outcomes|donation and report proof
48|Caring, urgent when needed|Care + emergency + appointment|emergency care|vet appointment header|care guide footer|care cards|appointment form|urgent helper and care reveal|clinic rooms, pet care, emergency routes, team details|safety and care proof
49|Quiet, exclusive, editorial|Maison + private access|private invitation|minimal maison header|private concierge footer|editorial object cards|private enquiry form|slow opacity and line reveal|craft details, private spaces, premium materials|discretion and craft proof
50|Authority, media, speaking|Media kit + newsletter + booking|media kit|personal media header|press kit footer|media cards|booking form|filter and newsletter reveal|portraits, stages, podcasts, writing desks, press assets|authority and media proof
""".strip()


JS_SIGNATURES = {
    "healthcare": "Appointment pathway, service filter, reassurance FAQ",
    "life-sciences": "Pipeline tabs, publication filters, trial eligibility toggle",
    "wellness": "Routine builder, service fit quiz, package toggle",
    "technology": "Support plan comparison, system status cards, ticket route selector",
    "saas": "Pricing toggle, feature tabs, integration filter, product UI display",
    "telecommunications": "Coverage checker mockup, plan filter, outage alert panel",
    "cybersecurity": "Risk matrix, compliance checklist, incident response stepper",
    "data-analytics": "Dashboard tabs, KPI filters, tool stack selector",
    "finance": "Advisory route selector, calculator-style estimate, risk toggles",
    "insurance": "Cover comparison, claims stepper, quote form logic",
    "legal": "Case type selector, document checklist, consultation route form",
    "accounting": "Deadline calendar, document checklist, package comparison",
    "consulting": "Diagnostic quiz, framework tabs, case filter",
    "education": "Level selector, course filter, timetable interaction",
    "recruitment": "Employer/candidate toggle, role filter, upload CV flow",
    "real-estate": "Property filter, gallery modal, map-style area cards",
    "construction": "Project estimator form, before/after slider, upload photos",
    "architecture": "Project gallery, planning stage stepper, image reveal",
    "interiors": "Moodboard filter, room selector, material palette interaction",
    "manufacturing": "Capability filter, spec table toggle, facility gallery",
    "engineering": "System diagram tabs, compliance checklist, project filter",
    "energy": "Savings estimator, battery/solar toggle, project output counters",
    "utilities": "Service request finder, alert banner, report filter",
    "environmental": "Impact metric filters, ESG report archive, audit route selector",
    "sustainability": "Impact calculator, ESG report filter, carbon category tabs",
    "agriculture": "Seasonal calendar, product filter, advice route selector",
    "food-production": "Product/allergen filter, stockist finder, recipe tabs",
    "restaurant": "Menu filter, allergen toggle, reservation widget, gallery",
    "hotel": "Room filter, booking panel, offer selector, amenities tabs",
    "hospitality": "Room filter, booking panel, offer selector, amenities tabs",
    "travel": "Trip finder, destination filter, itinerary accordion",
    "transport": "Route selector, fare estimate, fleet filter",
    "logistics": "Tracking mockup, quote calculator, network map filter",
    "automotive": "Inventory filter, finance calculator, test-drive form",
    "aviation": "Fleet specs tabs, safety checklist, charter route form",
    "maritime": "Vessel filter, port schedule, cargo quote form",
    "retail": "Product/category filter, loyalty signup, store finder",
    "ecommerce": "Catalogue filter, seller/customer support routing",
    "fashion": "Lookbook slider, size guide, collection filter",
    "beauty": "Routine finder, ingredient glossary, product filter",
    "media": "Show schedule filter, episode cards, advertise kit download",
    "entertainment": "Event calendar, ticket selector, artist filter",
    "publishing": "Library search, author filter, newsletter modal",
    "marketing": "Case study filter, campaign result tabs, brief form",
    "creative": "Portfolio filter, project lightbox, file/brief upload",
    "sports": "Timetable filter, membership toggle, coach selector",
    "events": "Event type selector, venue filter, package calculator",
    "government": "Service search, form finder, document filter, alert controls",
    "nonprofit": "Donation selector, impact calculator, volunteer role filter",
    "veterinary": "Emergency symptom helper, appointment form, care guide filter",
    "luxury": "Private enquiry reveal, membership request, concierge stepper",
    "personal-brand": "Media filter, speaking topic selector, press kit download",
}


DISPLAY_STACKS = [
    'Inter, ui-sans-serif, system-ui, sans-serif',
    'Georgia, "Times New Roman", serif',
    '"Trebuchet MS", Arial, sans-serif',
    '"Palatino Linotype", Palatino, serif',
    'Aptos, "Segoe UI", system-ui, sans-serif',
    'Verdana, Geneva, sans-serif',
    '"Arial Narrow", Arial, sans-serif',
    '"Courier New", ui-monospace, monospace',
    '"Gill Sans", Candara, sans-serif',
    'Didot, Bodoni 72, Georgia, serif',
    '"Lucida Sans", "Segoe UI", sans-serif',
    'Constantia, Georgia, serif',
]


BODY_STACKS = [
    'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    'Arial, Helvetica, sans-serif',
    '"Segoe UI", Tahoma, Geneva, sans-serif',
    'Verdana, Geneva, sans-serif',
    'Georgia, "Times New Roman", serif',
    '"Trebuchet MS", Arial, sans-serif',
    'Aptos, Calibri, sans-serif',
    '"Lucida Sans", "Segoe UI", sans-serif',
]


SENSITIVE = {
    "healthcare": "Information supports planning and is not a diagnosis or emergency instruction. People should use local emergency services for urgent symptoms.",
    "finance": "Financial content is general information and does not replace regulated personal advice or product disclosure review.",
    "insurance": "Cover, claims, limits, and exclusions depend on policy wording and insurer assessment.",
    "legal": "Legal and immigration information is general and does not create a lawyer-client relationship until formally engaged.",
    "accounting": "Tax and accounting guidance must be checked against current rules and client records before filing.",
    "beauty": "Ingredient suitability varies by person; patch testing and professional advice may be needed for sensitive users.",
    "food-production": "Ingredient, allergen, and storage information must match the final product label and local requirements.",
    "restaurant": "Menus, allergens, prices, and availability must be confirmed by the venue before ordering or booking.",
    "hotel": "Rates, availability, cancellation, and access policies depend on selected dates and booking terms.",
    "travel": "Travel plans may depend on visas, health rules, weather, operator availability, and insurance terms.",
    "events": "Availability, supplier pricing, venue access, and weather plans must be confirmed before contract.",
    "nonprofit": "Donation use statements must match governance records, reporting, and local fundraising rules.",
    "government": "Public service content must be verified by the responsible authority before publication.",
    "veterinary": "Pet health content is general; urgent symptoms require direct veterinary care.",
    "sports": "Fitness guidance should be adapted to health status and professional advice where needed.",
}


SCHEMA_BY_SLUG = {
    "healthcare": "MedicalBusiness", "legal": "LegalService", "finance": "FinancialService",
    "insurance": "FinancialService", "restaurant": "Restaurant", "hotel": "Hotel",
    "events": "Event", "ecommerce": "Product", "retail": "Store",
    "veterinary": "VeterinaryCare", "government": "GovernmentOrganization",
    "nonprofit": "NGO",
}


SECTION_PURPOSES = {
    "Hero": "position the offer in one confident first impression",
    "Need": "name the practical need that brings visitors to the page",
    "Problem": "show the cost of delay, confusion, or unmanaged work",
    "Risk": "clarify what can go wrong without a disciplined approach",
    "Promise": "state the outcome the site is built to support",
    "Services": "summarise the core service routes and next choices",
    "Process": "make the delivery path clear and predictable",
    "Proof": "show evidence through standards, examples, and review-ready material",
    "Trust": "reduce perceived risk through transparency and standards",
    "Questions": "answer the objections visitors raise before taking action",
    "CTA": "move the visitor to the next appropriate step",
    "Form": "collect the minimum information needed to route an enquiry",
    "Pricing": "explain how investment is structured and what affects cost",
    "Safety": "make safety, access, or suitability expectations explicit",
    "Support": "show how people get help before, during, and after delivery",
    "Resources": "organise educational materials for deeper decision making",
    "Guides": "turn complex decisions into practical next steps",
    "Results": "summarise the outcomes the work is designed to improve",
    "Reviews": "describe how verified feedback should be gathered and presented",
    "Compliance": "connect the work to standards, policies, and audit evidence",
}


CTA_BY_SLUG = {
    "healthcare": "Book Appointment", "life-sciences": "Discuss Research", "wellness": "Book Consultation",
    "technology": "Request IT Audit", "saas": "Schedule Demo", "telecommunications": "Check Coverage",
    "cybersecurity": "Request Audit", "data-analytics": "Plan Dashboard", "finance": "Book Advisor Call",
    "insurance": "Request Quote", "legal": "Book Consultation", "accounting": "Request Quote",
    "consulting": "Send Brief", "education": "Book Trial", "recruitment": "Start Hiring",
    "real-estate": "Get Valuation", "construction": "Request Estimate", "architecture": "Discuss Project",
    "interiors": "Start Design", "manufacturing": "Send RFQ", "engineering": "Ask Engineer",
    "energy": "Calculate Savings", "utilities": "Request Service", "environmental": "Book Audit",
    "agriculture": "Plan Visit", "food-production": "Request Trade Info", "restaurant": "Reserve Table",
    "hotel": "Check Availability", "travel": "Plan Trip", "transport": "Book Ride",
    "logistics": "Request Quote", "automotive": "Book Test Drive", "aviation": "Request Charter",
    "maritime": "Request Shipping", "retail": "Visit Shop", "ecommerce": "Browse Market",
    "fashion": "Shop Collection", "beauty": "Build Routine", "media": "Advertise With Us",
    "entertainment": "View Tickets", "publishing": "Subscribe", "marketing": "Send Campaign Brief",
    "creative": "Start Project", "sports": "Join Class", "events": "Enquire Date",
    "government": "Start Request", "nonprofit": "Donate Today", "veterinary": "Book Visit",
    "luxury": "Request Private Access", "personal-brand": "Book Appearance",
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def page_key(page_name: str) -> str:
    return slugify(page_name) or "home"


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
        return (255, 255, 255)
    return tuple(int(value[index:index + 2], 16) for index in (1, 3, 5))  # type: ignore[return-value]


def rgb_to_hex(value: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{max(0, min(255, part)):02x}" for part in value)


def blend_hex(a: str, b: str, amount: float) -> str:
    amount = max(0.0, min(1.0, amount))
    ar, ag, ab = hex_to_rgb(a)
    br, bg, bb = hex_to_rgb(b)
    return rgb_to_hex((
        round(ar * amount + br * (1 - amount)),
        round(ag * amount + bg * (1 - amount)),
        round(ab * amount + bb * (1 - amount)),
    ))


def relative_luminance(value: str) -> float:
    def channel(part: int) -> float:
        raw = part / 255
        return raw / 12.92 if raw <= 0.03928 else ((raw + 0.055) / 1.055) ** 2.4

    red, green, blue = hex_to_rgb(value)
    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def contrast_ratio(a: str, b: str) -> float:
    lighter, darker = sorted([relative_luminance(a), relative_luminance(b)], reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def best_contrast_color(background: str, candidates: Iterable[str]) -> str:
    valid = [str(candidate) for candidate in candidates if re.fullmatch(r"#[0-9a-fA-F]{6}", str(candidate))]
    valid.extend(["#111827", "#000000", "#ffffff"])
    return max(valid, key=lambda color: contrast_ratio(background, color))


def readable_ink_for_palette(palette: tuple[str, str, str, str, str]) -> str:
    bg, primary, accent, ink, warm = palette
    if contrast_ratio(bg, ink) >= 4.5:
        return ink
    for candidate in [primary, accent, warm]:
        if contrast_ratio(bg, candidate) >= 4.5:
            return candidate
    return best_contrast_color(bg, [primary, accent, warm, ink])


def normalize_palette(palette: object) -> tuple[str, str, str, str, str]:
    bg, primary, accent, ink, warm = (str(item) for item in palette)  # type: ignore[assignment]
    return (bg, primary, accent, readable_ink_for_palette((bg, primary, accent, ink, warm)), warm)


def color_on(background: str) -> str:
    return best_contrast_color(background, ["#111827", "#000000", "#ffffff"])


def palette_is_dark(site: dict[str, object]) -> bool:
    bg, _primary, _accent, _ink, _warm = site["palette"]  # type: ignore[index]
    return relative_luminance(str(bg)) < 0.32


def brand_symbol_path(site: dict[str, object]) -> str:
    return f"assets/brand/{site['slug']}-symbol.svg"


def brand_wordmark_path(site: dict[str, object]) -> str:
    return f"assets/brand/{site['slug']}-wordmark.svg"


def brand_logo_path(site: dict[str, object]) -> str:
    return f"assets/brand/{site['slug']}-logo.svg"


def favicon_svg_path(site: dict[str, object]) -> str:
    return f"assets/brand/{site['slug']}-favicon.svg"


def favicon_png_path(site: dict[str, object], size: int = 32) -> str:
    return f"assets/brand/{site['slug']}-favicon-{size}.png"


def apple_touch_icon_path(site: dict[str, object]) -> str:
    return f"assets/brand/{site['slug']}-apple-touch-icon.png"


def social_avatar_path(site: dict[str, object]) -> str:
    return f"assets/brand/{site['slug']}-social-avatar.png"


def hero_asset_path(site: dict[str, object], page_name: str, crop: str = "desktop") -> str:
    suffix = "" if crop == "desktop" else f"-{crop}"
    return f"assets/images/hero/{site['slug']}-{page_key(page_name)}-hero{suffix}.svg"


def page_asset_path(site: dict[str, object], page_name: str) -> str:
    return f"assets/images/pages/{site['slug']}-{page_key(page_name)}-page.svg"


def section_asset_path(site: dict[str, object], page_name: str, section: str, index: int, variant: int = 1) -> str:
    return f"assets/images/sections/{site['slug']}-{page_key(page_name)}-{index:02d}-{slugify(section)}-{variant}.svg"


def card_asset_path(site: dict[str, object], page_name: str, section: str, index: int, variant: int = 1) -> str:
    return f"assets/images/cards/{site['slug']}-{page_key(page_name)}-{index:02d}-{slugify(section)}-card-{variant}.svg"


def gallery_asset_path(site: dict[str, object], page_name: str, variant: int) -> str:
    return f"assets/images/gallery/{site['slug']}-{page_key(page_name)}-gallery-{variant}.svg"


def section_icon_path(site: dict[str, object], page_name: str, section: str, index: int) -> str:
    return f"assets/icons/sections/{site['slug']}-{page_key(page_name)}-{index:02d}-{slugify(section)}.svg"


def service_icon_path(site: dict[str, object], label: str, index: int) -> str:
    return f"assets/icons/services/{site['slug']}-{index:02d}-{slugify(label)}.svg"


def ui_icon_path(site: dict[str, object], name: str) -> str:
    return f"assets/icons/ui/{site['slug']}-{slugify(name)}.svg"


def legal_icon_path(site: dict[str, object], name: str) -> str:
    return f"assets/icons/legal/{site['slug']}-{slugify(name)}.svg"


def contact_icon_path(site: dict[str, object], name: str) -> str:
    return f"assets/icons/contact/{site['slug']}-{slugify(name)}.svg"


def utility_asset_path(site: dict[str, object], name: str) -> str:
    return f"assets/images/utility/{site['slug']}-{slugify(name)}-visual.svg"


def background_asset_path(site: dict[str, object], name: str) -> str:
    return f"assets/images/backgrounds/{site['slug']}-{slugify(name)}-background.svg"


def mockup_asset_path(site: dict[str, object], name: str = "interface") -> str:
    return f"assets/mockups/{site['slug']}-{slugify(name)}-mockup.svg"


def diagram_asset_path(site: dict[str, object], name: str = "system") -> str:
    return f"assets/illustrations/diagrams/{site['slug']}-{slugify(name)}-diagram.svg"


def process_asset_path(site: dict[str, object], name: str = "journey") -> str:
    return f"assets/illustrations/process/{site['slug']}-{slugify(name)}-process.svg"


def pattern_asset_path(site: dict[str, object], name: str = "brand") -> str:
    return f"assets/illustrations/patterns/{site['slug']}-{slugify(name)}-pattern.svg"


def download_cover_path(site: dict[str, object], name: str = "readiness-checklist") -> str:
    return f"assets/downloads/{site['slug']}-{slugify(name)}-cover.svg"


def video_poster_path(site: dict[str, object], name: str = "overview") -> str:
    return f"assets/video/posters/{site['slug']}-{slugify(name)}-poster.svg"


def og_asset_path(site: dict[str, object], page_name: str = "Home") -> str:
    return f"assets/og/{site['slug']}-{page_key(page_name)}-open-graph.svg"


def legacy_og_asset_path(site: dict[str, object]) -> str:
    return f"assets/og/{site['slug']}-open-graph.svg"


def diversity_records() -> dict[int, dict[str, str]]:
    records: dict[int, dict[str, str]] = {}
    keys = [
        "number", "visualDirection", "layoutSignature", "heroType", "headerType",
        "footerType", "cardStyle", "formStyle", "motionStyle", "imageDirection", "proofStyle",
    ]
    for line in DIVERSITY_LINES.splitlines():
        parts = [part.strip() for part in line.split("|")]
        record = dict(zip(keys, parts, strict=True))
        number = int(record.pop("number"))
        records[number] = record
    return records


def reference_records() -> dict[int, list[dict[str, str]]]:
    records: dict[int, list[dict[str, str]]] = {}
    for line in REFERENCE_LINES.splitlines():
        number_text, refs_text = line.split("|", 1)
        refs: list[dict[str, str]] = []
        for raw_ref in refs_text.split(";"):
            category, rest = raw_ref.strip().split(":", 1)
            name, url = rest.rsplit("@", 1)
            refs.append({"category": category.strip(), "name": name.strip(), "url": url.strip()})
        records[int(number_text)] = refs
    return records


def premium_direction_records() -> dict[int, dict[str, str]]:
    records: dict[int, dict[str, str]] = {}
    keys = [
        "number", "premiumDirection", "brandMood", "buyerPsychology", "layoutArchetype",
        "density", "shapeLanguage", "surfaceMaterial", "imageSystem", "interactionModel",
        "ctaStyle", "pricingStyle", "resourceStyle", "mobileMenuStyle", "cookieStyle", "legalStyle",
    ]
    for line in PREMIUM_DIRECTION_LINES.splitlines():
        parts = [part.strip() for part in line.split("|")]
        record = dict(zip(keys, parts, strict=True))
        number = int(record.pop("number"))
        records[number] = record
    return records


def target_inspiration_records() -> dict[int, dict[str, object]]:
    records: dict[int, dict[str, object]] = {}
    keys = [
        "number", "name", "url", "palette", "visualDirection", "premiumDirection",
        "layoutSignature", "heroType", "headerType", "cardStyle", "formStyle",
        "motionStyle", "imageDirection", "cssProfile",
    ]
    for line in TARGET_INSPIRATION_LINES.splitlines():
        parts = [part.strip() for part in line.split("|")]
        record = dict(zip(keys, parts, strict=True))
        number = int(record.pop("number"))
        record["palette"] = tuple(part.strip() for part in str(record["palette"]).split(","))
        records[number] = record
    return records


def target_references_for(number: int, refs: list[dict[str, str]]) -> list[dict[str, str]]:
    target = target_inspiration_records()[number]
    target_ref = {"category": "direct", "name": str(target["name"]), "url": str(target["url"])}
    if any(ref["category"] == "direct" and (ref["name"] == target_ref["name"] or ref["url"] == target_ref["url"]) for ref in refs):
        return [
            target_ref,
            *[
                ref
                for ref in refs
                if not (ref["category"] == "direct" and (ref["name"] == target_ref["name"] or ref["url"] == target_ref["url"]))
            ],
        ]
    return [target_ref, *refs]


def public_inspiration_text(value: object, target_name: str) -> str:
    text = str(value)
    name_options = {
        target_name,
        target_name.split()[0],
        target_name.replace(":", ""),
    }
    for name in sorted(name_options, key=len, reverse=True):
        for token in [f"{name}-style", f"{name} style"]:
            text = text.replace(token, "").replace(token.lower(), "")
    text = re.sub(r"\s+", " ", text).strip(" -")
    return text[:1].upper() + text[1:] if text else str(value)


def apply_target_inspiration(site: dict[str, object]) -> None:
    target = target_inspiration_records()[int(site["number"])]
    target_name = str(target["name"])
    profile = str(target["cssProfile"])
    site["targetReference"] = target
    site["palette"] = normalize_palette(TARGET_PALETTE_OVERRIDES.get(profile, target["palette"]))
    for key in [
        "visualDirection", "premiumDirection", "layoutSignature", "heroType",
        "headerType", "cardStyle", "formStyle", "motionStyle", "imageDirection",
    ]:
        site[key] = public_inspiration_text(target[key], target_name)
    site["targetCssProfile"] = target["cssProfile"]
    site["references"] = target_references_for(int(site["number"]), site["references"])  # type: ignore[arg-type]
    passport = site["designPassport"]  # type: ignore[assignment]
    passport.update(
        {
            "premiumDirection": site["premiumDirection"],
            "layoutArchetype": site["layoutSignature"],
            "shapeLanguage": site["cardStyle"],
            "surfaceMaterial": site["visualDirection"],
            "imageSystem": site["imageDirection"],
            "interactionModel": site["heroType"],
            "ctaStyle": f"Primary-reference CTA hierarchy using {site['cta']}",
            "resourceStyle": "Primary-reference resource rhythm",
            "mobileMenuStyle": "Primary-reference mobile navigation",
            "cookieStyle": "Primary-reference compact consent",
            "legalStyle": "Primary-reference plain legal notes",
            "density": "spacious" if int(site["number"]) in {1, 16, 18, 28, 32, 44, 49, 50} else passport["density"],
        }
    )


def typography_for(number: int) -> dict[str, str]:
    def family_label(stack: str) -> str:
        return stack.split(",")[0].strip().strip('"')
    pairs = [
        (display, body)
        for display in DISPLAY_STACKS
        for body in BODY_STACKS
        if family_label(display) != family_label(body)
    ]
    display, body = pairs[number - 1]
    accent_options = [stack for stack in DISPLAY_STACKS + BODY_STACKS if family_label(stack) not in {family_label(display), family_label(body)}]
    accent = accent_options[(number * 5 + 3) % len(accent_options)]
    return {
        "display": display,
        "body": body,
        "accent": accent,
        "summary": f"{display.split(',')[0]} display with {body.split(',')[0]} body and {accent.split(',')[0]} accent labels",
    }


def avoid_sites_for(number: int) -> str:
    avoid = sorted({((number + 6) % 50) + 1, ((number + 16) % 50) + 1, ((number + 32) % 50) + 1})
    return ", ".join(f"{item:02d}" for item in avoid)


def theme_mode_for(site: dict[str, object]) -> str:
    slug = str(site["slug"])
    if slug == "luxury":
        return "luxury"
    dark = {"cybersecurity", "entertainment", "automotive", "aviation", "maritime"}
    civic = {"government", "utilities"}
    editorial = {"architecture", "fashion", "publishing", "personal-brand", "creative", "travel"}
    commerce = {"retail", "ecommerce", "food-production", "beauty", "interiors"}
    hospitality = {"restaurant", "hotel", "hospitality", "events"}
    technical = {"life-sciences", "technology", "saas", "data-analytics", "manufacturing", "engineering", "energy", "environmental", "sustainability", "logistics"}
    if slug in dark:
        return "dark"
    if slug in civic:
        return "civic"
    if slug in editorial:
        return "editorial"
    if slug in commerce:
        return "commerce"
    if slug in hospitality:
        return "hospitality"
    if slug in technical:
        return "technical"
    if slug in {"healthcare", "wellness", "veterinary", "education"}:
        return "care"
    return "professional"


def parse_matrix() -> list[dict[str, object]]:
    sites = []
    diversity = diversity_records()
    premium = premium_direction_records()
    references = reference_records()
    for raw in MATRIX_LINES.splitlines():
        number_text, industry, slug, pages_text = raw.split("|", 3)
        pages = []
        for page_part in pages_text.split(";"):
            name, sections_text = page_part.split(":", 1)
            sections = [part.strip() for part in sections_text.split(",")]
            sections = normalise_sections(name.strip(), sections)
            pages.append({"name": name.strip(), "sections": sections})
        number = int(number_text)
        typography = typography_for(number)
        diversity_record = diversity[number]
        premium_record = premium[number]
        design_passport = {
            "premiumDirection": premium_record["premiumDirection"],
            "brandMood": premium_record["brandMood"],
            "buyerPsychology": premium_record["buyerPsychology"],
            "typography": {
                "display": typography["display"],
                "body": typography["body"],
                "accent": typography["accent"],
                "summary": typography["summary"],
            },
            "colorPsychology": "palette and contrast selected for " + premium_record["buyerPsychology"],
            "layoutArchetype": premium_record["layoutArchetype"],
            "density": premium_record["density"],
            "shapeLanguage": premium_record["shapeLanguage"],
            "surfaceMaterial": premium_record["surfaceMaterial"],
            "imageSystem": premium_record["imageSystem"],
            "interactionModel": premium_record["interactionModel"],
            "ctaStyle": premium_record["ctaStyle"],
            "pricingStyle": premium_record["pricingStyle"],
            "resourceStyle": premium_record["resourceStyle"],
            "mobileMenuStyle": premium_record["mobileMenuStyle"],
            "cookieStyle": premium_record["cookieStyle"],
            "legalStyle": premium_record["legalStyle"],
        }
        diversity_record.update(
            {
                "jsSignature": JS_SIGNATURES.get(slug.strip(), "Contextual filters, form routing, and proof interactions"),
                "typographyDisplay": typography["display"],
                "typographyBody": typography["body"],
                "typographyAccent": typography["accent"],
                "typographySummary": typography["summary"],
                "mobileBehaviour": f"{diversity_record['headerType']} adapted into a {theme_mode_for({'slug': slug.strip()})} mobile menu",
                "avoidSites": avoid_sites_for(number),
                **premium_record,
            }
        )
        site = {
            "number": number,
            "industry": industry.strip(),
            "slug": slug.strip(),
            "folder": f"{number:02d}-{slug.strip()}",
            "brand": BRANDS[number - 1],
            "voice": THEME_VOICES[number - 1],
            "palette": PALETTES[number - 1],
            "repo": f"https://github.com/team-ashtra-ai/{number}.git",
            "baseUrl": f"https://team-ashtra-ai.github.io/{number}/",
            "cta": CTA_BY_SLUG.get(slug.strip(), "Request Consultation"),
            "schema": SCHEMA_BY_SLUG.get(slug.strip(), "Organization"),
            "disclaimer": SENSITIVE.get(slug.strip(), "Information is provided for planning and should be reviewed for the final client, location, and operating rules."),
            "pages": pages,
            "themeMode": theme_mode_for({"slug": slug.strip()}),
            "designPassport": design_passport,
            "references": references[number],
            **diversity_record,
        }
        apply_target_inspiration(site)
        sites.append(site)
    return sites


def normalise_sections(page_name: str, sections: list[str]) -> list[str]:
    """Keep the supplied matrix, correcting only technical 10-section breaks."""
    if len(sections) == 10:
        return sections
    if not sections or sections[-1] != "CTA":
        raise ValueError(f"{page_name} does not end with CTA: {sections}")
    candidates = ["Form", "Details", "Support", "Route", "Direct", "Contact"]
    if page_name != "Contact":
        candidates = ["Details", "Support", "Proof", "Questions", "Notes"] + candidates
    fixed = sections[:]
    for candidate in candidates:
        if len(fixed) >= 10:
            break
        if candidate not in fixed:
            insert_at = max(1, len(fixed) - 2)
            fixed.insert(insert_at, candidate)
    if len(fixed) != 10:
        raise ValueError(f"{page_name} could not be normalised to 10 sections: {fixed}")
    return fixed


def page_filename(page_name: str) -> str:
    return "index.html" if page_name == "Home" else f"{slugify(page_name)}.html"


def page_href(page_name: str) -> str:
    return "index.html" if page_name == "Home" else f"{slugify(page_name)}.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def sentence(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if not value.endswith((".", "!", "?")):
        value += "."
    return value


def purpose_for(section: str, page_name: str, site: dict[str, object]) -> str:
    if section in SECTION_PURPOSES:
        return SECTION_PURPOSES[section]
    label = section.lower()
    if section in {"Eligibility", "Suitability", "Fit", "Requirements", "Criteria"}:
        return "help the visitor decide whether this route is appropriate"
    if section in {"Evidence", "Credentials", "Standards", "Governance", "Quality"}:
        return "make credibility visible before the visitor commits"
    if section in {"Booking", "Quote", "Appointment", "Consultation", "Reserve"}:
        return "turn interest into a low-friction enquiry"
    if section in {"Articles", "Downloads", "Templates", "Reports", "Checklists"}:
        return "offer practical resources that support informed decisions"
    return f"explain {label} in the context of {page_name.lower()}"


def core_terms(site: dict[str, object]) -> list[str]:
    industry = str(site["industry"])
    words = [w.strip(",&") for w in industry.replace("&", " ").split()]
    words = [w.lower() for w in words if len(w) > 3]
    terms = []
    for word in words:
        if word not in terms:
            terms.append(word)
    return terms[:4] or ["service", "quality", "delivery"]


def friendly_subject(section: str) -> str:
    return {
        "CTA": "the next step",
        "FAQ": "common questions",
        "FAQs": "common questions",
        "Questions": "common questions",
        "Hero": "the opening route",
    }.get(section, section.lower())


def cta_phrase(site: dict[str, object]) -> str:
    phrase = str(site["cta"]).lower()
    replacements = {
        "book appointment": "book an appointment",
        "request quote": "request a quote",
        "start request": "start a request",
        "book consultation": "book a consultation",
        "request consultation": "request a consultation",
        "reserve table": "reserve a table",
        "book stay": "book a stay",
        "plan trip": "plan a trip",
        "book route": "book a route",
        "request audit": "request an audit",
        "request proposal": "request a proposal",
        "make donation": "make a donation",
    }
    return replacements.get(phrase, phrase)


def section_blocks(section: str, page_name: str, site: dict[str, object]) -> list[tuple[str, str]]:
    terms = core_terms(site)
    brand = str(site["brand"])
    industry = str(site["industry"])
    subject = friendly_subject(section)
    term = terms[0]
    cta = cta_phrase(site)
    labels_by_mode = {
        "care": ("Prepare", "Reassure", "Continue"),
        "technical": ("System", "Evidence", "Route"),
        "dark": ("Exposure", "Control", "Response"),
        "editorial": ("Context", "Detail", "Enquiry"),
        "luxury": ("Invitation", "Discretion", "Request"),
        "commerce": ("Browse", "Compare", "Act"),
        "hospitality": ("Arrive", "Choose", "Reserve"),
        "civic": ("Find", "Confirm", "Start"),
        "professional": ("Diagnose", "Plan", "Advance"),
    }
    labels = labels_by_mode.get(str(site["themeMode"]), labels_by_mode["professional"])
    templates = {
        "care": (
            f"{brand} frames {subject} as a calm route with what to prepare, who can help, and when to book.",
            f"Plain language, visible reassurance, and practical details make {industry.lower()} feel easier to navigate.",
            f"Visitors leave with a clear care path and a low-friction way to {cta}.",
        ),
        "technical": (
            f"{brand} maps {subject} as a working system, showing dependencies, ownership, and support routes.",
            f"Evidence, specifications, and operational detail make each {term} decision easier to validate.",
            f"The next action stays close, whether the visitor needs documentation, support, or a scoped conversation.",
        ),
        "dark": (
            f"{brand} surfaces the exposure behind {subject} before asking visitors to commit.",
            f"Controls, standards, and response paths are presented with the urgency expected in {industry.lower()}.",
            f"Each route ends with a practical way to prioritise risk and {cta}.",
        ),
        "editorial": (
            f"{brand} treats {subject} like an edited index, pairing strong context with project-level detail.",
            f"Large visuals, compact metadata, and calm copy let {industry.lower()} visitors compare the work quickly.",
            f"The enquiry path remains quiet but visible once the visitor has enough context to act.",
        ),
        "luxury": (
            f"{brand} presents {subject} with restraint, space, and enough detail to invite private consideration.",
            f"Proof is handled through discretion, provenance, and carefully paced information rather than volume.",
            f"The route to {cta} feels deliberate, private, and appropriate for high-intent visitors.",
        ),
        "commerce": (
            f"{brand} makes {subject} easy to browse, compare, and narrow without losing the product story.",
            f"Availability, fit, trust signals, and buying context stay visible for {industry.lower()} visitors.",
            f"Visitors can move from interest to enquiry with a direct path to {cta}.",
        ),
        "hospitality": (
            f"{brand} makes {subject} feel like part of the visit, with atmosphere, choice, and timing in view.",
            f"Menus, location context, guest expectations, and proof points are arranged for quick decisions.",
            f"The path to {cta} stays close without flattening the mood of the experience.",
        ),
        "civic": (
            f"{brand} makes {subject} task-led, plain, and easy to scan for the right service route.",
            f"Eligibility, forms, notices, and support details are kept visible for public-service clarity.",
            f"Visitors can confirm what applies to them and start the request without hunting through the site.",
        ),
        "professional": (
            f"{brand} uses {subject} to diagnose the visitor's situation before proposing a next step.",
            f"Clear comparisons, proof points, and working detail help {industry.lower()} buyers understand the tradeoffs.",
            f"The route to {cta} is specific enough for qualified enquiries and light enough for early research.",
        ),
    }
    copy = templates.get(str(site["themeMode"]), templates["professional"])
    return [(labels[index], copy[index]) for index in range(3)]


def lead_for(section: str, page_name: str, site: dict[str, object]) -> str:
    brand = str(site["brand"])
    industry = str(site["industry"])
    voice = str(site["voice"])
    subject = friendly_subject(section)
    return sentence(
        f"{subject.title()} gives {brand} a focused {voice} route, with practical context for {industry.lower()} decisions and a clear next step"
    )


def body_for(section: str, page_name: str, site: dict[str, object]) -> str:
    brand = str(site["brand"])
    industry = str(site["industry"]).lower()
    subject = friendly_subject(section)
    cta = cta_phrase(site)
    return (
        f"{brand} connects {subject} with practical proof, useful comparisons, and the questions {industry} visitors bring to the page. "
        f"Visitors can scan the essentials, understand the tradeoffs, and decide whether to {cta} or keep exploring. "
        "The rhythm is built for action without removing the context people need to trust the decision."
    )


def section_cta(section: str, page_name: str, site: dict[str, object]) -> tuple[str, str]:
    pages = site["pages"]  # type: ignore[assignment]
    cta = str(site["cta"])
    if section == "Hero":
        return (cta, "contact.html")
    if section in {"Questions", "Support", "Help"}:
        return ("Open Contact", "contact.html")
    if section in {"Pricing", "Fees", "Plans", "Packages", "Rates"}:
        return ("View Pricing", "pricing.html" if any(p["name"] == "Pricing" for p in pages) else "contact.html")
    if section in {"Resources", "Guides", "Journal", "Insights", "Blog", "Articles", "Downloads"}:
        target = next((page_href(p["name"]) for p in pages if p["name"] in {"Resources", "Guides", "Journal", "Insights", "Blog"}), "contact.html")
        return ("View Resources", target)
    if section == "CTA":
        return (cta, "contact.html")
    if section in {"Booking", "Quote", "Consultation", "Appointment", "Reserve", "Apply", "Enquiry", "Enquire", "Upload"}:
        return (cta, f"contact.html?route={slugify(section)}")
    if page_name == "Contact":
        return (cta, "#contact-form")
    return (f"Explore {page_name}", page_href(page_name))


def hero_headline(site: dict[str, object], page_name: str) -> str:
    if page_name == "Home":
        return str(site["brand"])
    return f"{page_name} by {site['brand']}"


def hero_subheadline(site: dict[str, object], page_name: str) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    if page_name == "Home":
        return str(passport["premiumDirection"])
    return f"{page_name} shaped for {str(site['industry']).lower()} decisions."


def proof_badges(site: dict[str, object]) -> tuple[str, str, str]:
    mode = str(site["themeMode"])
    terms = core_terms(site)
    badges = {
        "care": ("Clear intake", "Human follow-up", "Practical reassurance"),
        "technical": ("System map", "Evidence trail", "Support route"),
        "dark": ("Exposure review", "Control plan", "Response route"),
        "editorial": ("Curated index", "Project context", "Enquiry path"),
        "luxury": ("Private access", "Quiet review", "Discreet request"),
        "commerce": ("Browse quickly", "Compare clearly", "Ask availability"),
        "hospitality": ("Check availability", "Plan the visit", "Reserve with context"),
        "civic": ("Find the service", "Check eligibility", "Start the request"),
        "professional": ("Define scope", "Compare options", "Request advice"),
    }.get(mode, ("Define scope", "Compare options", "Request advice"))
    if mode == "professional" and terms:
        return (f"{terms[0].title()} scope", badges[1], badges[2])
    return badges


def interaction_title(component_type: str, site: dict[str, object]) -> str:
    titles = {
        "pathway": "Find the right care route",
        "tabs": "Compare the active routes",
        "quiz": "Choose a starting profile",
        "status": "Check the operating path",
        "checker": "Check availability",
        "risk": "Prioritise the risk",
        "dashboard": "Focus the dashboard",
        "calculator": "Estimate the next step",
        "stepper": "Walk the pathway",
        "checklist": "Build the document list",
        "calendar": "Review the deadline",
        "filter": "Filter the options",
        "toggle": "Choose the audience",
        "estimate": "Shape the estimate",
        "gallery": "Review the visual set",
        "moodboard": "Build the moodboard",
        "spec": "Compare capabilities",
        "diagram": "Inspect the system",
        "finder": "Find the service",
        "impact": "Track the impact",
        "seasonal": "Plan the season",
        "allergen": "Check ingredients",
        "menu": "Choose the menu path",
        "booking": "Check the booking path",
        "trip": "Shape the trip",
        "route": "Select the route",
        "tracking": "Track the movement",
        "inventory": "Browse inventory",
        "fleet": "Compare the fleet",
        "vessel": "Review vessel fit",
        "catalogue": "Filter the catalogue",
        "marketplace": "Choose buyer or seller",
        "lookbook": "Browse the looks",
        "routine": "Build a routine",
        "schedule": "Filter the schedule",
        "tickets": "Choose ticket fit",
        "library": "Search the archive",
        "cases": "Filter the work",
        "portfolio": "Open the portfolio",
        "timetable": "Find a class",
        "event-planner": "Plan the date",
        "service-search": "Search services",
        "donation": "Choose an impact route",
        "symptom": "Route the care need",
        "private": "Request private access",
        "media-kit": "Choose the media route",
    }
    return titles.get(component_type, str(site["cta"]))


def interaction_copy(site: dict[str, object], component_type: str) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    return (
        f"Select a path and {site['brand']} keeps the next step, proof, and follow-up expectation aligned with "
        f"{str(passport['buyerPsychology']).lower()}."
    )


def render_signature_interaction(site: dict[str, object], page_name: str, section: str) -> str:
    """Render one industry-specific progressive-enhancement block per page."""
    slug = str(site["slug"])
    passport = site["designPassport"]  # type: ignore[assignment]
    section_key = slugify(section)
    page_key = slugify(page_name)
    signature = esc(site["jsSignature"])
    if section not in {"Hero", "Services", "Pricing", "Questions", "FAQ", "Gallery", "Products", "Rooms", "Menu", "Booking", "Coverage", "Risk", "Dashboard", "Donate", "Schedule", "Library", "Media", "Contact"}:
        return ""
    component_type = {
        "healthcare": "pathway", "life-sciences": "tabs", "wellness": "quiz", "technology": "status",
        "saas": "tabs", "telecommunications": "checker", "cybersecurity": "risk", "data-analytics": "dashboard",
        "finance": "calculator", "insurance": "stepper", "legal": "checklist", "accounting": "calendar",
        "consulting": "quiz", "education": "filter", "recruitment": "toggle", "real-estate": "filter",
        "construction": "estimate", "architecture": "gallery", "interiors": "moodboard", "manufacturing": "spec",
        "engineering": "diagram", "energy": "calculator", "utilities": "finder", "sustainability": "impact",
        "agriculture": "seasonal", "food-production": "allergen", "restaurant": "menu", "hospitality": "booking",
        "travel": "trip", "transport": "route", "logistics": "tracking", "automotive": "inventory",
        "aviation": "fleet", "maritime": "vessel", "retail": "catalogue", "ecommerce": "marketplace",
        "fashion": "lookbook", "beauty": "routine", "media": "schedule", "entertainment": "tickets",
        "publishing": "library", "marketing": "cases", "creative": "portfolio", "sports": "timetable",
        "events": "event-planner", "government": "service-search", "nonprofit": "donation",
        "veterinary": "symptom", "luxury": "private", "personal-brand": "media-kit",
    }.get(slug, "selector")
    options = {
        "care": ("Start", "Review", "Book"),
        "technical": ("Map", "Filter", "Validate"),
        "dark": ("Assess", "Contain", "Respond"),
        "editorial": ("Browse", "Select", "Enquire"),
        "luxury": ("Reveal", "Consider", "Request"),
        "commerce": ("Filter", "Compare", "Request"),
        "hospitality": ("Choose", "Check", "Reserve"),
        "civic": ("Search", "Confirm", "Start"),
        "professional": ("Diagnose", "Compare", "Act"),
    }.get(str(site["themeMode"]), ("Diagnose", "Compare", "Act"))
    chips = "".join(
        f'<button type="button" data-option="{esc(slugify(option))}" aria-pressed="{str(i == 0).lower()}">{esc(option)}</button>'
        for i, option in enumerate(options)
    )
    return f"""
  <div class="container signature-panel signature-{esc(component_type)}" data-signature="{esc(component_type)}" data-page="{esc(page_key)}" data-section-key="{esc(section_key)}">
    <div>
      <p class="eyebrow">{esc(passport['interactionModel'])}</p>
      <h3>{esc(interaction_title(component_type, site))}</h3>
      <p>{esc(interaction_copy(site, component_type))}</p>
    </div>
    <div class="signature-controls" role="group" aria-label="{signature}">
      {chips}
    </div>
    <output data-signature-output aria-live="polite">{esc(options[0])} route selected for {esc(site['brand'])}.</output>
  </div>
""".strip()


def render_section_payload(site: dict[str, object], page_name: str, section: str, index: int, blocks: list[tuple[str, str]]) -> str:
    composition = section_composition(site, section, index)
    card_style = esc(site["cardStyle"])
    section_label = esc(section)
    if composition in {"timeline", "stepper", "process ladder"}:
        items = "".join(
            f'<li><span>{i:02d}</span><h3>{esc(title)}</h3><p>{esc(copy)}</p></li>'
            for i, (title, copy) in enumerate(blocks, start=1)
        )
        return f'<ol class="process-list card-{esc(slugify(str(site["cardStyle"])))}" aria-label="{section_label} steps">{items}</ol>'
    if composition in {"dashboard panel", "metric band"}:
        terms = core_terms(site)
        metrics = "".join(
            f'<article class="metric-card"><span>{esc(label)}</span><strong>{value}</strong><p>{esc(copy)}</p></article>'
            for label, value, copy in [
                (terms[0].title(), f"{int(site['number']) + index}x", blocks[0][1]),
                ("Readiness", f"{72 + (int(site['number']) + index) % 23}%", blocks[1][1]),
                ("Next step", "Clear", blocks[2][1]),
            ]
        )
        return f'<div class="dashboard-panel" aria-label="{section_label} metrics">{metrics}</div>'
    if composition in {"map block", "route", "search panel", "filter grid"}:
        pins = "".join(f'<span style="--x:{18 + i * 28}%;--y:{28 + (i % 2) * 28}%"></span>' for i in range(3))
        cards = "".join(f'<article><h3>{esc(title)}</h3><p>{esc(copy)}</p></article>' for title, copy in blocks)
        return f'<div class="map-panel" aria-label="{section_label} route map"><div class="map-canvas">{pins}</div><div class="map-list">{cards}</div></div>'
    if composition in {"gallery wall", "full-bleed image", "product shelf", "case-study block"}:
        cards = "".join(
            f'<figure><img src="{esc(card_asset_path(site, page_name, section, index, card_index))}" alt="{esc(title)} visual cue for {esc(section.lower())}" width="420" height="280" loading="lazy" decoding="async"><figcaption><strong>{esc(title)}</strong>{esc(copy)}</figcaption></figure>'
            for card_index, (title, copy) in enumerate(blocks[:2], start=1)
        )
        cards += f'<article class="mini-card" data-card-style="{card_style}"><h3>{esc(blocks[2][0])}</h3><p>{esc(blocks[2][1])}</p></article>'
        return f'<div class="visual-card-stack" aria-label="{section_label} visual set">{cards}</div>'
    if composition in {"document checklist", "report/download block", "side-by-side comparison"}:
        items = "".join(f'<li><span></span><div><h3>{esc(title)}</h3><p>{esc(copy)}</p></div></li>' for title, copy in blocks)
        return f'<ul class="checklist-panel" aria-label="{section_label} checklist">{items}</ul>'
    if composition in {"booking panel", "form panel", "CTA banner"}:
        buttons = "".join(f'<button type="button">{esc(title)}</button>' for title, _ in blocks)
        summary = " ".join(copy for _, copy in blocks[:2])
        return f'<div class="finder-panel" aria-label="{section_label} choices"><p>{esc(summary)}</p><div>{buttons}</div><a class="button secondary" href="contact.html">{esc(site["cta"])}</a></div>'
    block_html = "".join(
        f'<article class="mini-card" data-card-style="{card_style}"><img class="card-thumb" src="{esc(card_asset_path(site, page_name, section, index, card_index))}" alt="" width="420" height="280" loading="lazy" decoding="async"><h3>{esc(title)}</h3><p>{esc(copy)}</p></article>'
        for card_index, (title, copy) in enumerate(blocks, start=1)
    )
    return f'<div class="card-grid card-{esc(slugify(str(site["cardStyle"])))}" aria-label="{section_label} details">{block_html}</div>'


def meta_description(site: dict[str, object], page_name: str) -> str:
    return (
        f"{site['brand']} {page_name.lower()} page for {str(site['industry']).lower()}, with expert static copy, accessible UX, SEO structure, and conversion-ready forms."
    )


def page_title(site: dict[str, object], page_name: str) -> str:
    return f"{page_name} | {site['brand']} Static Site"


def canonical(site: dict[str, object], page_name: str) -> str:
    return urljoin(str(site["baseUrl"]), "" if page_name == "Home" else page_href(page_name))


def nav_pages(site: dict[str, object]) -> list[dict[str, object]]:
    names = {"Home", "Services", "Pricing", "Contact", "Products", "Rooms", "Menu", "Booking", "Donate", "Programs", "Properties", "Vehicles", "Shop", "Portfolio", "Work"}
    pages = site["pages"]  # type: ignore[assignment]
    selected = [page for page in pages if page["name"] in names]
    if len(selected) < 5:
        selected = list(pages[:5])
    if not any(page["name"] == "Contact" for page in selected):
        selected.append(next(page for page in pages if page["name"] == "Contact"))
    return selected[:7]


def whatsapp_href(site: dict[str, object], page_name: str) -> str:
    message = f"Hi ASH-TRA, I am viewing {site['brand']} {page_name} and want the next step."
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def render_whatsapp_widget(site: dict[str, object], page_name: str) -> str:
    label = f"Message {site['brand']} on WhatsApp"
    return f"""
<aside class="whatsapp-widget" data-whatsapp-widget aria-label="WhatsApp contact">
  <a class="whatsapp-button" href="{esc(whatsapp_href(site, page_name))}" target="_blank" rel="noopener" aria-label="{esc(label)}" data-track="whatsapp_{esc(site['slug'])}">
    <span class="whatsapp-mark" aria-hidden="true">WA</span>
    <span class="whatsapp-copy"><strong>WhatsApp</strong><small>Quick enquiry</small></span>
  </a>
</aside>
""".strip()


def render_header_route_strip(site: dict[str, object], current_page: str) -> str:
    quick_pages = [page for page in nav_pages(site) if str(page["name"]) != current_page][:4]
    chips = "".join(f'<a href="{page_href(str(page["name"]))}">{esc(page["name"])}</a>' for page in quick_pages)
    mode_label = {
        "civic": "Service routes",
        "dark": "Secure routes",
        "editorial": "Index routes",
        "luxury": "Private routes",
        "commerce": "Catalogue routes",
        "hospitality": "Booking routes",
        "technical": "Systems routes",
        "care": "Care routes",
    }.get(str(site["themeMode"]), "Project routes")
    return f"""
  <div class="container header-route-strip" aria-label="{esc(mode_label)}">
    <span>{esc(site['layoutSignature'])}</span>
    <div>{chips}</div>
    <a href="contact.html" data-track="header_route_strip">{esc(site['cta'])}</a>
  </div>
""".rstrip()


def render_header_context(site: dict[str, object]) -> str:
    mode = str(site["themeMode"])
    if mode == "civic":
        return f'<div class="header-utility" role="status"><span>Service notices</span><a href="support.html" data-track="header_service_notice">Open support routes</a></div>'
    if mode == "dark":
        return f'<div class="header-utility" role="status"><span>Priority route</span><a href="contact.html?route=urgent" data-track="header_priority_route">{esc(site["cta"])}</a></div>'
    if mode == "hospitality":
        return '<div class="header-utility booking-strip"><label>Arrival <input type="date" aria-label="Arrival date"></label><label>Guests <input type="number" min="1" value="2" aria-label="Guests"></label><a href="contact.html?route=booking" data-track="header_booking_bar">Check route</a></div>'
    if mode == "technical":
        return '<div class="header-utility"><span>Systems view</span><span>Docs</span><span>Status</span><span>Evidence</span></div>'
    if mode == "editorial":
        return '<div class="header-utility"><span>Index</span><span>Work</span><span>Notes</span><span>Enquiry</span></div>'
    if mode == "luxury":
        return '<div class="header-utility"><span>By appointment</span><span>Private access</span><span>Discretion first</span></div>'
    if mode == "commerce":
        return '<div class="header-utility"><label>Search <input type="search" aria-label="Search catalogue"></label><a href="contact.html?route=stock" data-track="header_catalogue_route">Ask availability</a></div>'
    if mode == "care":
        return f'<div class="header-utility"><span>Care route</span><a href="contact.html?route=appointment" data-track="header_care_route">{esc(site["cta"])}</a><a href="contact.html?route=support" data-track="header_support_route">Need help</a></div>'
    return '<div class="header-utility"><span>Brief</span><span>Scope</span><span>Proof</span><span>Proposal</span></div>'


def render_header(site: dict[str, object], current_page: str) -> str:
    links = []
    for page in nav_pages(site):
        name = str(page["name"])
        current = ' aria-current="page"' if name == current_page else ""
        links.append(f'<a href="{page_href(name)}"{current}>{esc(name)}</a>')
    header_class = f"site-header header-{slugify(str(site['headerType']))}"
    menu_style = slugify(str(site["designPassport"]["mobileMenuStyle"]))  # type: ignore[index]
    return f"""
<a class="skip-link" href="#main">Skip to content</a>
<header class="{header_class}" data-header data-header-type="{esc(site['headerType'])}" data-mobile-menu="{esc(site['designPassport']['mobileMenuStyle'])}">
  {render_header_context(site)}
  <div class="container nav-shell">
    <a class="brand" href="index.html" aria-label="{esc(site['brand'])} home">
      <img src="{esc(brand_symbol_path(site))}" alt="" width="44" height="44" loading="eager" decoding="async">
      <span><strong>{esc(site['brand'])}</strong><small>{esc(site['visualDirection'])}</small></span>
    </a>
    <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-menu">{'Browse' if site['themeMode'] in {'commerce', 'editorial'} else 'Private' if site['themeMode'] == 'luxury' else 'Menu'}</button>
    <nav class="site-nav mobile-menu-{menu_style}" id="site-menu" aria-label="Main navigation">
      {"".join(links)}
    </nav>
    <a class="nav-cta" href="contact.html" data-track="header_cta">{esc(site['cta'])}</a>
  </div>
{render_header_route_strip(site, current_page)}
</header>
""".strip()


def render_footer(site: dict[str, object]) -> str:
    pages = site["pages"]  # type: ignore[assignment]
    groups = {
        "Main": pages[:3],
        "Services": pages[3:6],
        "Proof": pages[6:8],
        "Support": pages[8:],
    }
    legal = [
        ("Privacy", "privacy.html"), ("Cookies", "cookies.html"), ("Terms", "terms.html"),
        ("Accessibility", "accessibility.html"), ("Sitemap", "sitemap.html"),
        ("Thanks", "thanks.html"), ("Error", "404.html"),
    ]
    group_html = []
    for label, group_pages in groups.items():
        items = "".join(f'<li><a href="{page_href(str(page["name"]))}">{esc(page["name"])}</a></li>' for page in group_pages)
        group_html.append(f'<div><h2>{esc(label)}</h2><ul>{items}</ul></div>')
    legal_items = "".join(f'<li><a href="{href}">{label}</a></li>' for label, href in legal)
    footer_note = {
        "civic": "Service access, records, support, and public notices stay visible in every route.",
        "dark": "Priority response, evidence, and secure enquiry routes are grouped for fast decisions.",
        "editorial": "A structured index keeps projects, writing, and enquiry routes easy to scan.",
        "luxury": "Private routes, discretion notes, and appointment access stay quiet but reachable.",
        "commerce": "Product, support, stock, and account-style routes are grouped for buying intent.",
        "hospitality": "Booking, location, policies, and guest support remain one step away.",
        "technical": "Evidence, documentation, systems, and support routes stay close to conversion.",
        "care": "Care, suitability, practical support, and appointment routes remain visible.",
    }.get(str(site["themeMode"]), "Main routes, proof, support, and legal access remain available across the static site.")
    return f"""
<footer class="site-footer footer-{slugify(str(site['footerType']))}" data-footer-type="{esc(site['footerType'])}">
  <section class="container footer-masthead" aria-label="Footer conversion">
    <p class="eyebrow">{esc(site['layoutSignature'])}</p>
    <h2>{esc(site['brand'])}</h2>
    <p>{esc(site['visualDirection'])} shaped for {esc(site['industry'])} visitors who need a clear next step.</p>
    <a class="button primary" href="contact.html" data-track="footer_masthead_cta">{esc(site['cta'])}</a>
  </section>
  <div class="container footer-grid">
    <section class="footer-brand" aria-label="Company summary">
      <img src="{esc(brand_symbol_path(site))}" alt="" width="52" height="52" loading="lazy" decoding="async">
      <h2>{esc(site['brand'])}</h2>
      <p>{esc(site['visualDirection'])} for {esc(site['industry'])}. {esc(footer_note)}</p>
      <p><a href="{ASH_TRA_CONTACT}" data-track="footer_contact">Contact ASH-TRA</a></p>
      <p><a href="contact.html?route=booking" data-track="footer_booking">Open booking route</a></p>
    </section>
    {"".join(group_html)}
    <div><h2>Legal</h2><ul>{legal_items}</ul></div>
  </div>
  <div class="container footer-bottom">
    <span>Static-first. SEO-ready. Accessible by design.</span>
    <a href="cookies.html" data-track="cookie_settings">Cookie settings</a>
  </div>
</footer>
""".strip()


def target_visual_kind(site: dict[str, object]) -> str:
    return TARGET_VISUAL_KIND.get(str(site.get("targetCssProfile", "")), "dashboard")


def target_visual_labels(site: dict[str, object], page_name: str) -> list[str]:
    page = next((item for item in site["pages"] if item["name"] == page_name), site["pages"][0])  # type: ignore[index]
    sections = [str(item) for item in page["sections"]]  # type: ignore[index]
    labels = [section for section in sections[1:5] if section != "CTA"]
    while len(labels) < 4:
        labels.append(core_terms(site)[len(labels) % len(core_terms(site))].title())
    return labels[:4]


def render_target_visual(site: dict[str, object], page_name: str) -> str:
    """Render target-specific visual chrome without copying external code or assets."""
    kind = target_visual_kind(site)
    profile = str(site.get("targetCssProfile", "generic"))
    labels = target_visual_labels(site, page_name)
    brand = str(site["brand"])
    cta = str(site["cta"])
    number = int(site["number"])
    terms = core_terms(site)

    if kind == "scan":
        points = "".join(f'<span style="--a:{45 + i * 62}deg"></span>' for i in range(6))
        rows = "".join(f'<li><b>{esc(label)}</b><span>{70 + ((number + i) * 7) % 29}% ready</span></li>' for i, label in enumerate(labels[:3]))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="target-topline"><span>Health check</span><b>{esc(brand)}</b></div>
  <div class="scan-orbit">{points}<strong>{number * 3 + 7}M</strong><em>data points</em></div>
  <ul class="target-rowset">{rows}</ul>
</div>
""".strip()

    if kind == "pipeline":
        phases = ["Discovery", "Validation", "Phase 1", "Partner"]
        cells = "".join(f'<div><span>{esc(phase)}</span><b>{esc(labels[i % len(labels)])}</b></div>' for i, phase in enumerate(phases))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="bio-grid">{''.join('<span></span>' for _ in range(24))}</div>
  <div class="pipeline-table">{cells}</div>
  <p class="target-caption">Data, models, compute, evidence</p>
</div>
""".strip()

    if kind in {"shelf", "store", "apothecary", "poster"}:
        cards = "".join(
            f'<article><span>{esc(label)}</span><b>{esc(terms[i % len(terms)].title())}</b><em></em></article>'
            for i, label in enumerate(labels[:4])
        )
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="product-shelf">{cards}</div>
  <div class="target-strip"><b>{esc(cta)}</b><span>Routine / proof / fit</span></div>
</div>
""".strip()

    if kind in {"network", "space", "security", "route", "freight", "shipping", "aero"}:
        nodes = "".join(f'<span style="--x:{12 + (i * 23) % 76}%;--y:{18 + (i * 31) % 64}%"></span>' for i in range(9))
        cards = "".join(f'<li><b>{esc(label)}</b><span>{esc(["Live", "Ready", "Clear"][i % 3])}</span></li>' for i, label in enumerate(labels[:3]))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="network-map">{nodes}<svg viewBox="0 0 100 60" preserveAspectRatio="none"><path d="M8 45 C25 12 44 48 60 20 S82 18 94 8"/></svg></div>
  <ul class="target-rowset">{cards}</ul>
</div>
""".strip()

    if kind in {"board", "data", "workflow", "ledger", "construction", "spec", "engineering", "product", "utility", "climate"}:
        columns = []
        for i, label in enumerate(labels[:3]):
            issues = "".join(f'<li><span>{esc(terms[(i + j) % len(terms)].upper())}-{number}{j}</span>{esc(labels[(i + j) % len(labels)])}</li>' for j in range(2))
            columns.append(f'<section><h4>{esc(label)}</h4><ul>{issues}</ul></section>')
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="app-chrome"><span></span><span></span><span></span><b>{esc(brand)}</b></div>
  <div class="app-board">{''.join(columns)}</div>
</div>
""".strip()

    if kind in {"calculator", "quote"}:
        rows = "".join(
            f'<label><span>{esc(label)}</span><b>{esc(value)}</b></label>'
            for label, value in [(labels[0], "1,000"), (labels[1], "Today"), (labels[2], "Clear fees")]
        )
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="calculator-panel">
    <h4>{esc(cta)}</h4>
    {rows}
    <button type="button">{esc(labels[3])}</button>
  </div>
</div>
""".strip()

    if kind in {"studio", "property", "architecture", "travel", "print", "author", "agency", "design"}:
        items = "".join(f'<li><span>0{i}</span><b>{esc(label)}</b></li>' for i, label in enumerate(labels[:4], start=1))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="editorial-plate"><span>{esc(brand)}</span><strong>{esc(page_name)}</strong></div>
  <ol class="editorial-index">{items}</ol>
</div>
""".strip()

    if kind in {"cinema", "jobs", "restaurant", "retreat", "campaign", "media", "posterwall", "sport", "events"}:
        tiles = "".join(f'<article><span>{esc(label)}</span></article>' for label in labels[:4])
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="poster-grid">{tiles}</div>
  <div class="target-strip"><b>{esc(brand)}</b><span>{esc(cta)}</span></div>
</div>
""".strip()

    if kind == "catalogue":
        tiles = "".join(f'<article><span>{esc(label)}</span><b>{i:02d}</b></article>' for i, label in enumerate(labels[:4], start=1))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="catalogue-grid">{tiles}</div>
</div>
""".strip()

    if kind == "service":
        steps = "".join(f'<li><span>{i}</span>{esc(label)}</li>' for i, label in enumerate(labels[:3], start=1))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="service-card">
    <h4>{esc(cta)}</h4>
    <ol>{steps}</ol>
    <button type="button">Start now</button>
  </div>
</div>
""".strip()

    if kind in {"impact", "farm", "clinic"}:
        cards = "".join(f'<article><b>{65 + i * 12}%</b><span>{esc(label)}</span></article>' for i, label in enumerate(labels[:3]))
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="impact-grid">{cards}</div>
</div>
""".strip()

    if kind in {"maison", "moodboard", "vehicle"}:
        items = "".join(f'<span>{esc(label)}</span>' for label in labels[:4])
        return f"""
<div class="target-stage target-{kind} target-profile-{esc(profile)}" aria-hidden="true">
  <div class="maison-frame"><strong>{esc(brand)}</strong>{items}</div>
</div>
""".strip()

    return f"""
<div class="target-stage target-dashboard target-profile-{esc(profile)}" aria-hidden="true">
  <div class="app-chrome"><span></span><span></span><span></span><b>{esc(brand)}</b></div>
  <div class="dashboard-panel"><article><strong>{number * 2}</strong><span>{esc(labels[0])}</span></article><article><strong>{70 + number % 20}%</strong><span>{esc(labels[1])}</span></article></div>
</div>
""".strip()


def render_section(site: dict[str, object], page_name: str, section: str, index: int, contact_has_form: bool = False) -> str:
    section_id = f"section-{slugify(section)}"
    composition = section_composition(site, section, index)
    lead = lead_for(section, page_name, site)
    body = body_for(section, page_name, site)
    cta_text, cta_href = section_cta(section, page_name, site)
    blocks = section_blocks(section, page_name, site)
    payload_html = render_section_payload(site, page_name, section, index, blocks)
    kicker = f"{page_name} / {index:02d}"
    extra = ""
    if section == "Hero":
        badges = proof_badges(site)
        extra = f"""
      <div class="hero-proof" aria-label="Trust notes">
        <span>{esc(badges[0])}</span><span>{esc(badges[1])}</span><span>{esc(badges[2])}</span>
      </div>
"""
    if section == "Form" or (page_name == "Contact" and section == "CTA" and not contact_has_form):
        extra += render_contact_form(site, page_name)
    if section in {"Questions", "FAQ"}:
        extra += render_faq_block(site, page_name)
    if section in {"Pricing", "Fees", "Plans", "Packages", "Rates", "Premiums"}:
        extra += render_pricing_block(site)
    if section in {"Gallery", "Photos", "Portfolio", "Projects", "Work", "Lookbook"}:
        extra += render_gallery_block(site, page_name)
    if section in {"Resources", "Guides", "Journal", "Insights", "Blog", "Articles", "Downloads", "Templates", "Reports", "News"}:
        extra += render_resource_block(site, page_name, section, index)
    if section == "CTA":
        extra += render_cta_panel(site, page_name)
    extra += render_signature_interaction(site, page_name, section)

    if section == "Hero":
        return f"""
<section id="{section_id}" class="section hero-section hero-{esc(slugify(str(site['heroType'])))} composition-{esc(slugify(composition))}" data-section="{esc(section)}" data-composition="{esc(composition)}" data-hero-type="{esc(site['heroType'])}" data-track="section_{esc(page_name.lower())}_{esc(section.lower())}">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">{esc(kicker)}</p>
      <h1>{esc(hero_headline(site, page_name))}</h1>
      <h2>{esc(hero_subheadline(site, page_name))}</h2>
      <p class="lead">{esc(lead)}</p>
      <p>{esc(body)}</p>
      <div class="button-row">
        <a class="button primary" href="{cta_href}" data-track="cta_{esc(page_name.lower())}_{esc(section.lower())}">{esc(cta_text)}</a>
        <a class="button secondary" href="{ASH_TRA_DISCOVERY}" data-track="secondary_{esc(page_name.lower())}_{esc(section.lower())}">Discuss build</a>
      </div>
      {extra}
    </div>
    <figure class="hero-media target-media target-kind-{esc(target_visual_kind(site))} target-profile-{esc(str(site.get('targetCssProfile', 'generic')))}">
      {render_target_visual(site, page_name)}
      <picture>
        <source media="(max-width: 640px)" srcset="{esc(hero_asset_path(site, page_name, 'mobile'))}">
        <source media="(max-width: 1024px)" srcset="{esc(hero_asset_path(site, page_name, 'tablet'))}">
        <img src="{esc(hero_asset_path(site, page_name))}" alt="{esc(site['brand'])} visual direction for {esc(page_name.lower())}" width="960" height="640" loading="eager" decoding="async">
      </picture>
      <figcaption>{esc(site['imageDirection'])} expressed through a custom static visual system.</figcaption>
    </figure>
  </div>
</section>
""".strip()

    return f"""
<section id="{section_id}" class="section content-section section-{esc(section_id)} mode-{esc(site['themeMode'])} composition-{esc(slugify(composition))}" data-section="{esc(section)}" data-composition="{esc(composition)}" data-track="section_{esc(page_name.lower())}_{esc(section.lower())}">
  <div class="container section-grid">
    <div class="section-copy">
      <img class="section-icon" src="{esc(section_icon_path(site, page_name, section, index))}" alt="" width="64" height="64" loading="lazy" decoding="async">
      <p class="eyebrow">{esc(kicker)}</p>
      <h2>{esc(section)}</h2>
      <p class="lead">{esc(lead)}</p>
      <p>{esc(body)}</p>
      <a class="text-link" href="{cta_href}" data-track="inline_{esc(page_name.lower())}_{esc(section.lower())}">{esc(cta_text)}</a>
    </div>
    {payload_html}
  </div>
  {extra}
</section>
""".strip()


def render_pricing_block(site: dict[str, object]) -> str:
    labels = {
        "commerce": ("Browse", "Bundle", "Scale"),
        "hospitality": ("Entry", "Stay", "Private"),
        "technical": ("Audit", "Build", "Operate"),
        "dark": ("Assess", "Defend", "Retain"),
        "luxury": ("Invite", "Curate", "Retain"),
        "civic": ("Find", "Apply", "Resolve"),
        "editorial": ("Consult", "Produce", "Archive"),
        "care": ("Consult", "Plan", "Maintain"),
    }.get(str(site["themeMode"]), ("Start", "Grow", "Scale"))
    return f"""
  <div class="container pricing-grid pricing-{esc(slugify(str(site['layoutSignature'])))}" data-component="pricing">
    <article class="price-card"><h3>{esc(labels[0])}</h3><p>Focused first route shaped around {esc(site['industry']).lower()} readiness and risk.</p><strong>Scoped</strong></article>
    <article class="price-card featured"><h3>{esc(labels[1])}</h3><p>Full delivery path with planning, implementation, proof, and review.</p><strong>Quoted</strong></article>
    <article class="price-card"><h3>{esc(labels[2])}</h3><p>Ongoing support, content, reporting, and improvement cycles.</p><strong>Retainer</strong></article>
  </div>
""".strip()


def render_faq_block(site: dict[str, object], page_name: str) -> str:
    return f"""
  <div class="container faq-list faq-{esc(site['themeMode'])}" data-component="faq">
    <details><summary>What happens first?</summary><p>{esc(site['brand'])} starts with a focused intake so the recommendation matches the visitor's context, risk, timing, and readiness.</p></details>
    <details><summary>How is scope kept clear?</summary><p>Each route explains inclusions, exclusions, documents, timing, and the decision points that affect final delivery.</p></details>
    <details><summary>How is this site different?</summary><p>The theme uses {esc(site['layoutSignature']).lower()}, {esc(site['cardStyle']).lower()}, and {esc(site['jsSignature']).lower()} rather than a shared template rhythm.</p></details>
  </div>
""".strip()


def render_gallery_block(site: dict[str, object], page_name: str) -> str:
    return f"""
  <div class="container visual-strip gallery-{esc(site['themeMode'])}" data-component="gallery">
    <figure><img src="{esc(gallery_asset_path(site, page_name, 1))}" alt="{esc(page_name)} gallery display for {esc(site['imageDirection']).lower()}" width="960" height="640" loading="lazy" decoding="async"><figcaption>{esc(site['heroType'])}</figcaption></figure>
    <figure><img src="{esc(gallery_asset_path(site, page_name, 2))}" alt="{esc(site['brand'])} proof and content system" width="960" height="640" loading="lazy" decoding="async"><figcaption>{esc(site['proofStyle'])}</figcaption></figure>
  </div>
""".strip()


def render_resource_block(site: dict[str, object], page_name: str, section: str, section_index: int) -> str:
    style = site["designPassport"]["resourceStyle"]  # type: ignore[index]
    labels = {
        "care": ("Guide", "Checklist", "Questions"),
        "technical": ("Spec", "Report", "Playbook"),
        "dark": ("Alert", "Checklist", "Response note"),
        "editorial": ("Essay", "Index", "Brief"),
        "luxury": ("Journal", "Invitation", "Private note"),
        "commerce": ("Guide", "Stockist", "Comparison"),
        "hospitality": ("Menu", "Guide", "Policy"),
        "civic": ("Form", "Notice", "Eligibility"),
        "professional": ("Guide", "Checklist", "Brief"),
    }.get(str(site["themeMode"]), ("Guide", "Checklist", "Brief"))
    cards = "".join(
        f'<article class="resource-card"><img src="{esc(card_asset_path(site, page_name, section, section_index, card_index))}" alt="{esc(label)} resource cover for {esc(site["brand"])}" width="420" height="280" loading="lazy" decoding="async"><span>{esc(label)}</span><h3>{esc(site["brand"])} {esc(label.lower())}</h3><p>{esc(style)} for {esc(section.lower())} decisions in {esc(page_name.lower())}.</p><a href="docs/content-map.md">Open resource</a></article>'
        for card_index, label in enumerate(labels, start=1)
    )
    return f"""
  <div class="container resource-board resource-{esc(slugify(str(style)))}" data-component="resources">
    {cards}
  </div>
""".strip()


def render_cta_panel(site: dict[str, object], page_name: str) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    return f"""
  <div class="container cta-panel cta-{esc(slugify(str(passport['ctaStyle'])))}">
    <div>
      <p class="eyebrow">{esc(passport['buyerPsychology'])}</p>
      <h2>{esc(site['cta'])}</h2>
      <p>{esc(passport['premiumDirection'])}</p>
    </div>
    <img src="{esc(section_asset_path(site, page_name, 'CTA', 99, 1))}" alt="" width="360" height="240" loading="lazy" decoding="async">
    <a class="button primary" href="contact.html" data-track="cta_panel_{esc(site['slug'])}">{esc(site['cta'])}</a>
  </div>
""".strip()


def render_contact_form(site: dict[str, object], page_name: str) -> str:
    key = slugify(page_name)
    field_label = {
        "healthcare": "Care need", "life-sciences": "Programme area", "wellness": "Service interest",
        "technology": "Support need", "saas": "Product goal", "telecommunications": "Address or area",
        "cybersecurity": "Risk concern", "data-analytics": "Dashboard need", "finance": "Advice route",
        "insurance": "Cover need", "legal": "Case type", "accounting": "Filing need",
        "consulting": "Business challenge", "education": "Learning level", "recruitment": "Employer or talent",
        "real-estate": "Property type", "construction": "Project type", "architecture": "Site or brief",
        "interiors": "Room or style", "manufacturing": "Quantity or spec", "engineering": "System type",
        "energy": "Site and bill", "utilities": "Service request", "sustainability": "Audit focus",
        "agriculture": "Crop or product", "food-production": "Product or trade", "restaurant": "Date and guests",
        "hospitality": "Room and dates", "travel": "Destination", "transport": "Route",
        "logistics": "Shipment profile", "automotive": "Vehicle type", "aviation": "Route or mission",
        "maritime": "Cargo or vessel", "retail": "Store or order", "ecommerce": "Customer or seller",
        "fashion": "Styling or wholesale", "beauty": "Skin or product concern", "media": "Editorial or advertising",
        "entertainment": "Show or booking", "publishing": "Submission or subscription", "marketing": "Campaign brief",
        "creative": "Project style", "sports": "Class or level", "events": "Date and guests",
        "government": "Service route", "nonprofit": "Donate, volunteer, or partner", "veterinary": "Care concern",
        "luxury": "Private request", "personal-brand": "Media, speaking, or booking",
    }.get(str(site["slug"]), "Service")
    return f"""
  <div class="container form-panel form-{esc(slugify(str(site['formStyle'])))}" id="contact-form" data-form-style="{esc(site['formStyle'])}">
    <figure class="form-visual">
      <img src="{esc(utility_asset_path(site, 'form'))}" alt="{esc(site['brand'])} enquiry form support visual" width="420" height="360" loading="lazy" decoding="async">
    </figure>
    <form action="{FORM_ENDPOINT}" method="post" data-contact-form>
      <input type="hidden" name="site" value="{esc(site['number'])}">
      <input type="hidden" name="industry" value="{esc(site['industry'])}">
      <input type="hidden" name="source_page" value="{esc(page_name)}">
      <input class="honeypot" type="text" name="_gotcha" tabindex="-1" autocomplete="off" aria-hidden="true" aria-label="Leave this field empty">
      <div class="form-grid">
        <label for="name-{esc(key)}">Name <input id="name-{esc(key)}" name="name" type="text" autocomplete="name" required></label>
        <label for="email-{esc(key)}">Email <input id="email-{esc(key)}" name="email" type="email" autocomplete="email" required></label>
        <label for="phone-{esc(key)}">Phone <input id="phone-{esc(key)}" name="phone" type="tel" autocomplete="tel"></label>
        <label for="service-{esc(key)}">{esc(field_label)} <input id="service-{esc(key)}" name="service" type="text" autocomplete="off"></label>
      </div>
      <label for="message-{esc(key)}">Message <textarea id="message-{esc(key)}" name="message" rows="5" required></textarea></label>
      <div class="consent-field">
        <input id="consent-{esc(key)}" name="consent" type="checkbox" required>
        <label for="consent-{esc(key)}">I agree to be contacted about this enquiry and have read the <a href="privacy.html">privacy notice</a>.</label>
      </div>
      <p class="form-status" data-form-status aria-live="polite">We respond through the {esc(site['formStyle']).lower()} with the next practical step.</p>
      <button class="button primary" type="submit" data-track="form_submit_{esc(site['slug'])}">Send enquiry</button>
    </form>
  </div>
""".strip()


def render_page(site: dict[str, object], page: dict[str, object]) -> str:
    page_name = str(page["name"])
    sections = page["sections"]  # type: ignore[assignment]
    title = page_title(site, page_name)
    description = meta_description(site, page_name)
    page_url = canonical(site, page_name)
    og_image = urljoin(str(site["baseUrl"]), og_asset_path(site, page_name))
    hero_image = hero_asset_path(site, page_name)
    schema = {
        "@context": "https://schema.org",
        "@type": site["schema"],
        "name": title,
        "url": page_url,
        "description": description,
        "image": urljoin(str(site["baseUrl"]), hero_image),
        "provider": {"@type": "Organization", "name": "ASH-TRA", "logo": urljoin(str(site["baseUrl"]), brand_symbol_path(site))},
    }
    contact_has_form = page_name == "Contact" and "Form" in sections
    section_html = "\n".join(render_section(site, page_name, str(section), index + 1, contact_has_form) for index, section in enumerate(sections))
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(page_url)}">
  <link rel="icon" href="{esc(favicon_svg_path(site))}" type="image/svg+xml">
  <link rel="icon" href="{esc(favicon_png_path(site, 32))}" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{esc(apple_touch_icon_path(site))}">
  <link rel="manifest" href="site.webmanifest">
  <link rel="preload" as="image" href="{esc(hero_image)}">
  <meta name="theme-color" content="{esc(str(site['palette'][1]))}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{esc(og_image)}">
  <meta property="og:image:alt" content="{esc(site['brand'])} original social preview for {esc(page_name)}">
  <meta property="og:url" content="{esc(page_url)}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{esc(og_image)}">
  <meta name="twitter:image:alt" content="{esc(site['brand'])} original social preview for {esc(page_name)}">
  <link rel="stylesheet" href="css/styles.css">
  <script defer src="js/main.js"></script>
  <script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script>
</head>
<body class="theme-{esc(site['slug'])} mode-{esc(site['themeMode'])} hero-{esc(slugify(str(site['heroType'])))}" data-site="{esc(site['number'])}" data-theme="{esc(site['slug'])}" data-mode="{esc(site['themeMode'])}" data-inspiration-profile="{esc(site.get('targetCssProfile', 'generic'))}" data-layout="{esc(slugify(str(site['layoutSignature'])))}" data-density="{esc(site['designPassport']['density'])}" data-surface="{esc(site['designPassport']['surfaceMaterial'])}" data-motion="{esc(slugify(str(site['motionStyle'])))}">
{render_header(site, page_name)}
<main id="main">
{section_html}
<section class="section disclaimer" aria-label="Important notes">
  <div class="container">
    <h2>Notes</h2>
    <p>{esc(site['disclaimer'])}</p>
  </div>
</section>
</main>
{render_footer(site)}
<button class="back-to-top" type="button" data-back-to-top aria-label="Back to top"><span>Top</span></button>
{render_whatsapp_widget(site, page_name)}
<div class="cookie-banner" data-cookie-banner role="region" aria-label="Cookie notice">
  <p>{esc(site['designPassport']['cookieStyle'])}: privacy-conscious analytics run only after consent to improve static-site performance and conversion paths.</p>
  <button type="button" data-cookie-accept>Accept</button>
  <a href="cookies.html">Manage</a>
</div>
</body>
</html>
"""


def render_utility_page(site: dict[str, object], name: str, title: str, body: str) -> str:
    page_url = urljoin(str(site["baseUrl"]), f"{name}.html" if name not in {"404"} else "404.html")
    description = f"{title} for {site['brand']}, a static ASH-TRA portfolio website for {str(site['industry']).lower()}."
    og_image = urljoin(str(site["baseUrl"]), og_asset_path(site, name))
    utility_image = utility_asset_path(site, name)
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": title,
        "url": page_url,
        "description": description,
        "image": urljoin(str(site["baseUrl"]), utility_image),
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} | {esc(site['brand'])} Static Site</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(page_url)}">
  <link rel="icon" href="{esc(favicon_svg_path(site))}" type="image/svg+xml">
  <link rel="icon" href="{esc(favicon_png_path(site, 32))}" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="{esc(apple_touch_icon_path(site))}">
  <link rel="manifest" href="site.webmanifest">
  <meta name="theme-color" content="{esc(str(site['palette'][1]))}">
  <meta property="og:title" content="{esc(title)} | {esc(site['brand'])} Static Site">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:image" content="{esc(og_image)}">
  <meta property="og:image:alt" content="{esc(site['brand'])} original social preview for {esc(title)}">
  <meta property="og:url" content="{esc(page_url)}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="{esc(og_image)}">
  <meta name="twitter:image:alt" content="{esc(site['brand'])} original social preview for {esc(title)}">
  <link rel="stylesheet" href="css/styles.css">
  <script defer src="js/main.js"></script>
  <script type="application/ld+json">{json.dumps(schema, separators=(",", ":"))}</script>
</head>
<body class="theme-{esc(site['slug'])} mode-{esc(site['themeMode'])} legal-{esc(slugify(str(site['designPassport']['legalStyle'])))}" data-site="{esc(site['number'])}" data-theme="{esc(site['slug'])}" data-mode="{esc(site['themeMode'])}" data-density="{esc(site['designPassport']['density'])}">
{render_header(site, title.split()[0])}
<main id="main">
  <section class="section legal-page">
    <div class="container prose">
      <figure class="utility-visual"><img src="{esc(utility_image)}" alt="{esc(title)} visual support for {esc(site['brand'])}" width="960" height="640" loading="eager" decoding="async"></figure>
      <p class="eyebrow">ASH-TRA static portfolio support</p>
      <h1>{esc(title)}</h1>
      {body}
    </div>
  </section>
</main>
{render_footer(site)}
<button class="back-to-top" type="button" data-back-to-top aria-label="Back to top"><span>Top</span></button>
{render_whatsapp_widget(site, title)}
<div class="cookie-banner" data-cookie-banner role="region" aria-label="Cookie notice">
  <p>{esc(site['designPassport']['cookieStyle'])}: optional analytics run only after consent.</p>
  <button type="button" data-cookie-accept>Accept</button>
  <a href="cookies.html">Manage</a>
</div>
</body>
</html>
"""


def target_css_for_site(site: dict[str, object]) -> str:
    profile = str(site.get("targetCssProfile", ""))
    raw = TARGET_CSS_PROFILES.get(profile, "")
    if not raw:
        return ""
    patch = TARGET_ACCESSIBILITY_PATCHES.get(profile, "")
    target = site.get("targetReference", {})
    target_name = str(target.get("name", "Primary inspiration")) if isinstance(target, dict) else "Primary inspiration"
    target_url = str(target.get("url", "")) if isinstance(target, dict) else ""
    selector = f"body.theme-{site['slug']}"
    return f"""
/* Primary inspiration translation: {target_name} {target_url}. Original ASH-TRA implementation; no copied code, logos, images, or proprietary layout. */
{raw.replace("THEME", selector)}
{patch.replace("THEME", selector)}
"""


def clone_shell_css_for_site(site: dict[str, object]) -> str:
    profile = str(site.get("targetCssProfile", "generic"))
    selector = f"body.theme-{site['slug']}"
    immersive = {
        "starlink", "masterclass", "aman", "blacktomato", "tesla", "polestar",
        "boom", "nike", "luma", "charitywater", "rolex", "a24",
    }
    product = {
        "cloudflare", "linear", "wiz", "atlan", "wise", "lemonade", "xero",
        "formlabs", "watershed", "citymapper", "flexport", "maersk", "apple",
        "recursion", "aerofarms", "procore", "clio",
    }
    editorial = {
        "ideo", "modernhouse", "snohetta", "arup", "ssense", "jacquemus",
        "aesop", "monocle", "akqa", "pentagram", "jamesclear", "verge",
        "wearstler", "jungle",
    }
    hospitality = {"ritual", "sketch", "oatly", "octopus", "modernanimal"}
    civic = {"govuk"}
    if profile in immersive:
        family = "immersive"
    elif profile in product:
        family = "product"
    elif profile in editorial:
        family = "editorial"
    elif profile in hospitality:
        family = "hospitality"
    elif profile in civic:
        family = "civic"
    else:
        family = "professional"
    family_body = {
        "immersive": f"""
{selector} .site-header{{position:fixed;left:0;right:0;background:linear-gradient(180deg,rgba(0,0,0,.64),rgba(0,0,0,.12));color:#fff;border-bottom:0;box-shadow:none}}
{selector} .site-header.is-scrolled{{background:rgba(5,7,10,.88);backdrop-filter:blur(18px)}}
{selector} .header-utility{{background:transparent;color:rgba(255,255,255,.82);justify-content:center;border-bottom:1px solid rgba(255,255,255,.12)}}
{selector} .nav-shell{{min-height:82px;text-transform:uppercase;letter-spacing:.08em}}
{selector} .brand small{{display:none}}
{selector} .site-nav a{{color:rgba(255,255,255,.82);font-size:.76rem;border-radius:0;background:transparent}}
{selector} .site-nav a[aria-current="page"],{selector} .site-nav a:hover{{color:#fff;background:transparent;text-decoration:underline;text-underline-offset:.5em}}
{selector} .nav-cta{{background:#fff;color:#05070b;border-color:#fff;border-radius:999px;text-transform:uppercase;font-size:.78rem}}
{selector} .header-route-strip{{display:none}}
{selector} .hero-section{{min-height:100vh;padding-top:clamp(160px,19vh,230px);display:grid;align-items:end;background:#05070b;color:#fff}}
{selector} .hero-grid{{grid-template-columns:1fr;text-align:center;gap:clamp(1.3rem,4vw,3rem)}}
{selector} .hero-copy{{width:min(980px,100%);margin-inline:auto;text-align:center;padding-bottom:clamp(2rem,8vw,7rem)}}
{selector} .hero-copy h1{{margin-inline:auto;max-width:12ch;font-size:clamp(3.6rem,10vw,10.5rem);text-transform:uppercase;letter-spacing:0;font-weight:700;color:#fff}}
{selector} .hero-copy h2,{selector} .lead{{margin-inline:auto;color:rgba(255,255,255,.82)}}
{selector} .target-media{{position:absolute;inset:0;width:100%;height:100%;min-height:100%;padding:0;border:0;border-radius:0;box-shadow:none;background:#05070b;z-index:-1;opacity:.88}}
{selector} .target-media>picture img{{opacity:.42;filter:saturate(.82) contrast(1.12);object-fit:cover}}
{selector} .target-stage{{width:min(1120px,calc(100% - 40px));align-self:center;margin:auto;opacity:.86}}
{selector} .target-media figcaption{{display:none}}
{selector} .button.secondary{{color:#fff;border-color:rgba(255,255,255,.72);background:rgba(255,255,255,.08)}}
{selector} .hero-proof{{justify-content:center}}
{selector} .hero-proof span{{background:rgba(255,255,255,.10);color:#fff;border-color:rgba(255,255,255,.24);box-shadow:none}}
{selector} .content-section{{background:#fff;color:#111827;border-top:0}}
{selector} .content-section:nth-of-type(even){{background:#07090d;color:#fff}}
{selector} .content-section:nth-of-type(even) h2,{selector} .content-section:nth-of-type(even) h3{{color:#fff}}
{selector} .content-section:nth-of-type(even) .mini-card,{selector} .content-section:nth-of-type(even) .price-card,{selector} .content-section:nth-of-type(even) .process-list li{{background:#10151c;color:#fff;border-color:rgba(255,255,255,.16)}}
""",
        "product": f"""
{selector} .site-header{{position:sticky;top:12px;width:min(var(--container-wide),calc(100% - 28px));margin-inline:auto;border:1px solid color-mix(in srgb,var(--color-border) 72%,transparent);border-radius:22px;background:color-mix(in srgb,var(--color-surface) 80%,transparent);backdrop-filter:blur(20px);box-shadow:0 18px 70px rgba(15,23,42,.10)}}
{selector} .header-utility{{display:none}}
{selector} .nav-shell{{min-height:64px;padding-inline:.75rem}}
{selector} .brand{{min-width:190px}}
{selector} .brand img{{width:34px;height:34px}}
{selector} .brand small{{display:none}}
{selector} .site-nav{{gap:.1rem}}
{selector} .site-nav a{{border-radius:14px;font-size:.84rem}}
{selector} .nav-cta{{border-radius:16px;min-height:40px;padding:.65rem .9rem}}
{selector} .header-route-strip{{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:1rem;margin-top:.6rem;margin-bottom:.75rem;padding:.55rem .85rem;border:1px solid var(--color-border);border-radius:18px;background:var(--color-surface);box-shadow:0 12px 38px rgba(15,23,42,.08);font-size:.76rem;font-weight:850}}
{selector} .header-route-strip div{{display:flex;justify-content:center;gap:.35rem;min-width:0}}
{selector} .header-route-strip a{{text-decoration:none;padding:.35rem .55rem;border-radius:999px;color:var(--color-link)}}
{selector} .hero-section{{padding-top:clamp(60px,9vw,120px);background:radial-gradient(circle at 68% 18%,color-mix(in srgb,var(--color-accent) 22%,transparent),transparent 32%),linear-gradient(180deg,var(--color-bg),var(--color-bg-alt))}}
{selector} .hero-grid{{grid-template-columns:minmax(0,.88fr) minmax(420px,1.12fr);align-items:center}}
{selector} .hero-copy h1{{max-width:12ch;font-size:clamp(3rem,7.4vw,7.6rem);letter-spacing:0}}
{selector} .target-media{{border-radius:28px;border:1px solid color-mix(in srgb,var(--color-border) 70%,transparent);box-shadow:0 30px 90px rgba(15,23,42,.16);background:linear-gradient(180deg,color-mix(in srgb,var(--color-surface) 84%,transparent),var(--color-surface))}}
{selector} .target-stage{{filter:drop-shadow(0 24px 48px rgba(15,23,42,.18))}}
{selector} .content-section{{border-top:1px solid var(--color-border)}}
{selector} .section-grid{{grid-template-columns:minmax(260px,.66fr) minmax(0,1.34fr);align-items:start}}
{selector} .section-copy{{position:sticky;top:132px}}
{selector} .card-grid,{selector} .resource-board{{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
{selector} .mini-card,{selector} .price-card,{selector} .metric-card,{selector} .resource-card{{border-radius:20px;box-shadow:0 16px 50px rgba(15,23,42,.08)}}
""",
        "editorial": f"""
{selector} .site-header{{background:var(--color-bg);border-bottom:1px solid var(--color-text);box-shadow:none;backdrop-filter:none}}
{selector} .header-utility{{background:var(--color-bg);border-bottom:1px solid var(--color-border);justify-content:space-between;font-family:var(--font-accent);text-transform:uppercase;letter-spacing:.08em}}
{selector} .nav-shell{{display:grid;grid-template-columns:auto 1fr auto;min-height:104px;border-bottom:0}}
{selector} .brand{{min-width:auto}}
{selector} .brand img{{display:none}}
{selector} .brand strong{{font-size:clamp(1.8rem,4vw,4rem);font-weight:500}}
{selector} .brand small{{display:none}}
{selector} .site-nav{{justify-content:center;margin:0}}
{selector} .site-nav a{{border-radius:0;background:transparent;border-bottom:1px solid transparent;font-family:var(--font-accent);font-size:.78rem;text-transform:uppercase;letter-spacing:.06em}}
{selector} .site-nav a[aria-current="page"],{selector} .site-nav a:hover{{background:transparent;border-bottom-color:currentColor}}
{selector} .nav-cta,.button{{border-radius:0;box-shadow:none;text-transform:uppercase;letter-spacing:.04em}}
{selector} .header-route-strip{{display:grid;grid-template-columns:1fr auto 1fr;gap:1rem;border-bottom:1px solid var(--color-border);padding-block:.65rem;font-family:var(--font-accent);font-size:.72rem;text-transform:uppercase;letter-spacing:.08em}}
{selector} .header-route-strip div{{display:flex;gap:1rem;justify-content:center}}
{selector} .header-route-strip a{{text-decoration:none}}
{selector} .header-route-strip>a:last-child{{justify-self:end;text-decoration:underline;text-underline-offset:.3em}}
{selector} .hero-section{{padding-top:clamp(72px,11vw,160px);background:var(--color-bg)}}
{selector} .hero-grid{{grid-template-columns:minmax(0,.72fr) minmax(460px,1.28fr);align-items:end;border-bottom:1px solid var(--color-border);padding-bottom:clamp(2rem,6vw,5rem)}}
{selector} .hero-copy h1{{max-width:10.5ch;font-weight:400;font-size:clamp(3.2rem,8.6vw,8.8rem);letter-spacing:0}}
{selector} .target-media{{border-radius:0;box-shadow:none;border:0;border-left:1px solid var(--color-border);padding-left:clamp(1rem,3vw,2rem);background:transparent}}
{selector} .target-media>picture img{{opacity:.20}}
{selector} .content-section{{border-top:1px solid var(--color-border);background:var(--color-bg)}}
{selector} .content-section:nth-of-type(even){{background:var(--color-bg)}}
{selector} .section-grid{{grid-template-columns:minmax(240px,.48fr) minmax(0,1.52fr);align-items:start}}
{selector} .section-copy{{position:sticky;top:128px;border-right:1px solid var(--color-border);padding-right:clamp(1rem,3vw,2rem)}}
{selector} .mini-card,{selector} .price-card,{selector} .metric-card,{selector} .resource-card,{selector} .form-panel{{border-radius:0;box-shadow:none;background:transparent;border-color:var(--color-border)}}
{selector} .card-grid{{grid-template-columns:1.4fr .8fr .8fr}}
{selector} .site-footer{{border-top:1px solid var(--color-text)}}
""",
        "hospitality": f"""
{selector} .site-header{{position:sticky;background:color-mix(in srgb,var(--color-bg) 86%,transparent);border-bottom:0;backdrop-filter:blur(18px)}}
{selector} .header-utility{{justify-content:center;background:var(--color-text);color:#fff;gap:1.4rem}}
{selector} .nav-shell{{min-height:88px}}
{selector} .brand{{min-width:220px}}
{selector} .site-nav a,{selector} .nav-cta,{selector} .button{{border-radius:999px}}
{selector} .header-route-strip{{display:flex;justify-content:center;gap:.6rem;padding-bottom:.85rem;font-size:.82rem;font-weight:850}}
{selector} .header-route-strip span{{display:none}}
{selector} .header-route-strip div{{display:flex;gap:.45rem}}
{selector} .header-route-strip a{{text-decoration:none;border:1px solid var(--color-border);border-radius:999px;padding:.45rem .75rem;background:var(--color-surface)}}
{selector} .hero-section{{padding-top:0;min-height:86vh;display:grid;align-items:end;background:var(--color-text);color:#fff}}
{selector} .hero-grid{{grid-template-columns:1fr}}
{selector} .target-media{{order:-1;position:absolute;inset:0;min-height:100%;height:100%;border:0;border-radius:0;padding:0;opacity:.86;z-index:-1}}
{selector} .target-media>picture img{{opacity:.36;filter:saturate(.94) contrast(1.08)}}
{selector} .hero-copy{{width:min(780px,calc(100% - 40px));margin:0 auto clamp(2rem,8vw,6rem);padding:clamp(1.2rem,4vw,3rem);background:color-mix(in srgb,var(--color-surface) 94%,transparent);color:var(--color-text);border-radius:30px;box-shadow:0 28px 90px rgba(0,0,0,.26)}}
{selector} .hero-copy h1{{font-size:clamp(3rem,7.5vw,7rem);font-weight:500;color:var(--color-heading)}}
{selector} .section-grid{{grid-template-columns:minmax(0,1fr) minmax(320px,.86fr)}}
{selector} .mini-card,{selector} .price-card,{selector} .resource-card{{border-radius:26px}}
{selector} .visual-strip figure{{overflow:hidden;border-radius:28px}}
""",
        "civic": f"""
{selector} .site-header{{background:#fff;color:#0b0c0c;border-bottom:4px solid #1d70b8;box-shadow:none;backdrop-filter:none}}
{selector} .header-utility{{background:#0b0c0c;color:#fff;justify-content:flex-start;font-weight:700}}
{selector} .nav-shell{{min-height:72px}}
{selector} .brand{{min-width:auto}}
{selector} .brand img{{display:none}}
{selector} .brand strong{{font-size:1.35rem;font-weight:800}}
{selector} .brand small{{display:none}}
{selector} .site-nav a{{border-radius:0;color:#0b0c0c;text-decoration:underline;text-underline-offset:.2em;font-weight:700}}
{selector} .site-nav a[aria-current="page"],{selector} .site-nav a:hover{{background:#ffdd00;color:#0b0c0c}}
{selector} .nav-cta,.button{{border-radius:0;background:#00703c;color:#fff;border-color:#00703c;box-shadow:none}}
{selector} .header-route-strip{{display:grid;grid-template-columns:auto 1fr auto;gap:1rem;border-top:1px solid #b1b4b6;border-bottom:1px solid #b1b4b6;padding:.7rem 0;font-size:.95rem;font-weight:700}}
{selector} .header-route-strip div{{display:flex;gap:.8rem;justify-content:center}}
{selector} .header-route-strip a{{color:#1d70b8}}
{selector} .hero-section{{background:#fff;padding-top:clamp(48px,8vw,100px)}}
{selector} .hero-grid{{grid-template-columns:minmax(0,.78fr) minmax(360px,1fr);align-items:start}}
{selector} .hero-copy{{border-left:10px solid #1d70b8;padding-left:clamp(1rem,3vw,2rem)}}
{selector} .hero-copy h1{{font-size:clamp(2.7rem,6.5vw,6.6rem);font-weight:800;max-width:12ch}}
{selector} .target-media,.mini-card,.price-card,.resource-card,.form-panel,.faq-list details,.process-list li{{border-radius:0;box-shadow:none;border:2px solid #b1b4b6}}
{selector} .content-section{{border-top:2px solid #b1b4b6;background:#fff}}
{selector} .section-grid{{grid-template-columns:minmax(240px,.52fr) minmax(0,1.48fr)}}
""",
        "professional": f"""
{selector} .header-route-strip{{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:1rem;padding:.65rem 0;border-top:1px solid var(--color-border);font-size:.8rem;font-weight:850}}
{selector} .header-route-strip div{{display:flex;justify-content:center;gap:.45rem;flex-wrap:wrap}}
{selector} .header-route-strip a{{text-decoration:none;color:var(--color-link)}}
{selector} .hero-section{{background:linear-gradient(180deg,var(--color-bg),var(--color-bg-alt))}}
{selector} .hero-grid{{grid-template-columns:minmax(0,.9fr) minmax(380px,1.1fr)}}
{selector} .section-grid{{grid-template-columns:minmax(250px,.62fr) minmax(0,1.38fr)}}
{selector} .section-copy{{position:sticky;top:118px}}
{selector} .mini-card,{selector} .price-card,{selector} .resource-card{{box-shadow:0 16px 50px rgba(15,23,42,.08)}}
""",
    }[family]
    profile_details = {
        "neko": f"{selector} .scan-orbit{{background:radial-gradient(circle,#fff 0 18%,color-mix(in srgb,var(--color-accent) 20%,transparent) 18% 58%,transparent 58%)}}{selector} .hero-copy h1{{font-weight:600}}",
        "recursion": f"{selector} .bio-grid span:nth-child(3n){{border-radius:8px;background:var(--color-primary)}}{selector} .pipeline-table div{{border-radius:12px}}",
        "ritual": f"{selector} .product-shelf article{{border-radius:999px 999px 28px 28px;text-align:center}}{selector} .hero-section{{background:linear-gradient(90deg,#f7e37c 0 36%,var(--color-bg) 36%)}}",
        "cloudflare": f"{selector} .nav-cta{{background:#f6821f;color:#111827;border-color:#f6821f}}{selector} .target-stage{{font-family:var(--font-mono)}}",
        "linear": f"{selector} .site-header{{background:rgba(10,10,14,.78);color:#fff}}{selector} .hero-section{{background:#08090d;color:#fff}}{selector} .target-media{{background:#0c0d12;color:#fff}}",
        "starlink": f"{selector} .hero-copy h1{{letter-spacing:.03em}}{selector} .site-footer{{background:#05070b;color:#fff}}",
        "wiz": f"{selector} .target-stage{{background:linear-gradient(180deg,#101827,#0c111c);color:#fff;border-radius:24px;padding:1rem}}{selector} .risk-radar{{filter:drop-shadow(0 0 28px rgba(77,141,255,.34))}}",
        "atlan": f"{selector} .data-cloud{{border-radius:32px}}{selector} .mini-card{{border-radius:18px}}",
        "wise": f"{selector} .hero-section{{background:#9fe870;color:#163300}}{selector} .button.primary{{background:#163300;color:#fff;border-color:#163300}}",
        "lemonade": f"{selector} .hero-section{{background:#ff0083;color:#fff}}{selector} .button.primary{{background:#fff;color:#ff0083;border-color:#fff}}",
        "clio": f"{selector} .section-copy{{border-left:5px solid var(--color-primary);padding-left:1rem}}",
        "xero": f"{selector} .target-media{{border-radius:34px}}{selector} .metric-card strong{{color:var(--color-primary)}}",
        "ideo": f"{selector} .hero-copy h1{{font-size:clamp(3.5rem,10vw,10rem)}}",
        "masterclass": f"{selector} .hero-copy h1{{font-family:Georgia,serif;font-weight:500}}{selector} .content-section:nth-of-type(even){{background:#111;color:#fff}}",
        "modernhouse": f"{selector} .target-media{{border-left:0}}{selector} .hero-copy h1{{text-transform:none}}",
        "procore": f"{selector} .hero-section{{background:linear-gradient(90deg,#121212 0 42%,var(--color-bg) 42%);color:#fff}}",
        "snohetta": f"{selector} .content-section{{padding-block:clamp(80px,11vw,160px)}}",
        "wearstler": f"{selector} .hero-section{{background:var(--color-bg)}}{selector} .mini-card{{border-color:color-mix(in srgb,var(--color-warm) 38%,var(--color-border))}}",
        "formlabs": f"{selector} .product-shelf article{{background:#fff}}{selector} .target-media{{background:#f6f7f8}}",
        "arup": f"{selector} .process-list li{{border-left:8px solid var(--color-primary)}}",
        "tesla": f"{selector} .hero-copy h1{{font-size:clamp(3.4rem,8vw,8.2rem);font-weight:600}}",
        "octopus": f"{selector} .hero-section{{background:radial-gradient(circle at 70% 20%,#ff4bd8,transparent 30%),#140021;color:#fff}}",
        "watershed": f"{selector} .impact-grid article{{border-radius:20px;background:color-mix(in srgb,var(--color-accent) 11%,var(--color-surface))}}",
        "aerofarms": f"{selector} .hero-section{{background:linear-gradient(180deg,#071b12,var(--color-bg));color:#fff}}",
        "oatly": f"{selector} .hero-copy h1{{font-weight:900;text-transform:uppercase}}{selector} .mini-card{{border:3px solid var(--color-text)}}",
        "sketch": f"{selector} .hero-copy{{background:#f4c4d7}}{selector} .mini-card{{background:#fff7fb}}",
        "aman": f"{selector} .hero-copy{{background:rgba(245,239,228,.88);color:#1b1713}}",
        "blacktomato": f"{selector} .hero-copy h1{{font-family:Georgia,serif;font-weight:500}}",
        "citymapper": f"{selector} .map-canvas{{background-color:#c6ff00}}",
        "flexport": f"{selector} .map-canvas{{border-radius:22px}}",
        "polestar": f"{selector} .site-header{{background:rgba(255,255,255,.90);color:#111}}{selector} .hero-section{{background:#f4f4f2;color:#111}}",
        "boom": f"{selector} .hero-copy h1{{font-style:italic}}",
        "maersk": f"{selector} .hero-section{{background:linear-gradient(180deg,#e8f5fb,#fff)}}",
        "apple": f"{selector} .hero-copy h1{{font-weight:700}}{selector} .mini-card{{background:#f5f5f7;border:0}}",
        "ssense": f"{selector} .site-nav a{{font-size:.72rem}}{selector} .card-grid{{grid-template-columns:repeat(4,minmax(0,1fr))}}",
        "jacquemus": f"{selector} .hero-copy h1{{text-transform:lowercase}}",
        "aesop": f"{selector} .hero-section{{background:#ebeade}}{selector} .mini-card{{background:#f6f5ec}}",
        "jungle": f"{selector} .hero-section{{background:#ffe45e;color:#111}}{selector} .brand strong{{text-transform:none}}{selector} .mini-card:nth-child(2){{background:#ff6a3d}}",
        "verge": f"{selector} .hero-section{{background:linear-gradient(135deg,#ff0080,#7928ca,#00d4ff);color:#fff}}",
        "a24": f"{selector} .hero-copy h1{{font-family:Georgia,serif;font-weight:500}}{selector} .poster-grid article{{background:#111;color:#fff}}",
        "monocle": f"{selector} .site-header{{border-top:6px solid #111}}",
        "akqa": f"{selector} .hero-section{{background:#050505;color:#fff}}",
        "pentagram": f"{selector} .hero-copy h1{{font-weight:800}}",
        "nike": f"{selector} .hero-copy h1{{font-style:italic;font-weight:900}}",
        "luma": f"{selector} .hero-copy{{background:rgba(255,255,255,.92);color:#111;border-radius:28px}}",
        "govuk": f"{selector} .header-route-strip>a:last-child{{background:#00703c;color:#fff;padding:.4rem .7rem;text-decoration:none}}",
        "charitywater": f"{selector} .hero-section{{background:#fdd835;color:#111}}{selector} .button.primary{{background:#111;color:#fff;border-color:#111}}",
        "modernanimal": f"{selector} .hero-section{{background:#f6efe8}}{selector} .mini-card{{border-radius:30px}}",
        "rolex": f"{selector} .hero-copy{{background:rgba(0,60,36,.78);color:#fff}}{selector} .site-footer{{background:#003c24;color:#fff}}",
        "jamesclear": f"{selector} .brand strong{{font-family:Georgia,serif}}{selector} .hero-copy h1{{font-family:Georgia,serif;font-weight:500}}",
    }.get(profile, "")
    return f"""
/* Stronger inspiration-shell translation. Original ASH-TRA code and local assets; no copied source material. */
{selector} .header-route-strip span{{white-space:nowrap;color:var(--color-muted)}}
{selector} .footer-masthead{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;align-items:end;border-bottom:1px solid color-mix(in srgb,var(--color-footer-text) 22%,transparent);padding-bottom:clamp(1.4rem,4vw,3rem);margin-bottom:clamp(1.4rem,4vw,3rem)}}
{selector} .footer-masthead h2{{font-size:clamp(2.4rem,8vw,7.6rem);margin:0;color:inherit;letter-spacing:0;line-height:.92}}
{selector} .footer-masthead p:not(.eyebrow){{max-width:58ch;margin:0;color:color-mix(in srgb,var(--color-footer-text) 76%,transparent)}}
{selector} .footer-masthead .button{{justify-self:end;align-self:center}}
{selector} .cookie-banner{{left:1rem;right:auto;bottom:1rem;width:min(430px,calc(100% - 8rem));max-width:min(430px,calc(100% - 8rem));z-index:76}}
{selector} .back-to-top{{right:1rem;bottom:1rem;z-index:82}}
{selector} .back-to-top::before{{content:"";width:.48rem;height:.48rem;border-left:2px solid currentColor;border-top:2px solid currentColor;transform:rotate(45deg);margin-right:.45rem}}
{selector} .whatsapp-widget{{position:fixed;right:1rem;bottom:4.85rem;z-index:83}}
{selector} .whatsapp-button{{display:inline-flex;align-items:center;gap:.65rem;min-height:52px;padding:.48rem .86rem .48rem .48rem;border-radius:999px;background:#25d366;color:#062d18;text-decoration:none;font-weight:900;box-shadow:0 18px 50px rgba(6,45,24,.24);border:1px solid rgba(255,255,255,.42)}}
{selector} .whatsapp-mark{{display:grid;place-items:center;width:40px;height:40px;border-radius:999px;background:#fff;color:#128c3a;font-size:.72rem;font-family:var(--font-accent);letter-spacing:.04em}}
{selector} .whatsapp-copy{{display:grid;line-height:1.1}}
{selector} .whatsapp-copy small{{font-size:.68rem;color:rgba(6,45,24,.74)}}
{selector} .reveal-ready{{opacity:0;transform:translateY(18px);transition:opacity var(--motion-slow) var(--motion-ease),transform var(--motion-slow) var(--motion-ease)}}
{selector} .reveal-ready.is-visible{{opacity:1;transform:none}}
{selector} .back-to-top{{display:inline-flex;align-items:center;justify-content:center;gap:.2rem;opacity:0;pointer-events:none;transform:translateY(8px);transition:opacity var(--motion-base) ease,transform var(--motion-base) ease}}
{selector} .back-to-top.is-visible{{display:inline-flex;opacity:1;pointer-events:auto;transform:none}}
{family_body}
{profile_details}
@media (max-width: 980px){{
  {selector} .site-header{{position:sticky;top:0;width:100%;margin:0;border-radius:0}}
  {selector} .header-route-strip{{display:none}}
  {selector} .section-copy{{position:static;border-right:0;padding-right:0}}
  {selector} .hero-grid,{selector} .section-grid{{grid-template-columns:1fr}}
  {selector} .hero-section{{min-height:auto;padding-top:clamp(44px,12vw,90px)}}
  {selector} .target-media{{position:relative;inset:auto;min-height:360px;order:-1;border-radius:var(--image-radius);z-index:0}}
  {selector} .hero-copy{{width:auto;margin:0;text-align:left;padding:0;background:transparent;color:inherit;box-shadow:none}}
  {selector} .hero-copy h1{{max-width:100%;font-size:clamp(2.35rem,13vw,4.5rem)}}
  {selector} .footer-masthead{{grid-template-columns:1fr;align-items:start}}
  {selector} .footer-masthead .button{{justify-self:start}}
  {selector} .cookie-banner{{left:.8rem;right:.8rem;bottom:.8rem;width:auto;max-width:none}}
  {selector} .whatsapp-widget{{right:.8rem;bottom:6.6rem}}
  {selector} .whatsapp-copy small{{display:none}}
  {selector} .whatsapp-button{{padding:.42rem}}
  {selector} .whatsapp-copy strong{{display:none}}
}}
@media (prefers-reduced-motion: reduce){{
  {selector} .reveal-ready{{opacity:1;transform:none}}
}}
@media print{{
  {selector} .whatsapp-widget{{display:none!important}}
}}
"""


def target_component_css_for_site(site: dict[str, object]) -> str:
    profile = str(site.get("targetCssProfile", "generic"))
    kind = target_visual_kind(site)
    selector = f"body.theme-{site['slug']}"
    full_bleed_kinds = {"space", "cinema", "restaurant", "retreat", "travel", "campaign", "media", "posterwall", "sport", "events", "store", "vehicle", "product"}
    if kind in full_bleed_kinds:
        hero_layout = f"""
{selector} .hero-grid{{grid-template-columns:1fr;text-align:center;gap:clamp(1.5rem,4vw,3rem)}}
{selector} .hero-copy{{width:min(900px,100%);max-width:900px;margin-inline:auto;text-align:center}}
{selector} .target-media{{order:-1;width:min(1180px,100%);margin-inline:auto;min-height:clamp(430px,54vw,720px)}}
"""
    else:
        hero_layout = f"""
{selector} .hero-grid{{grid-template-columns:minmax(0,.90fr) minmax(420px,1.10fr);text-align:left;align-items:center}}
{selector} .hero-copy{{max-width:760px;text-align:left;margin-top:0}}
{selector} .target-media{{margin-top:0}}
"""
    return f"""
{selector} .cookie-banner{{left:auto;right:1rem;top:auto;bottom:1rem;width:min(520px,calc(100% - 2rem));max-width:min(520px,calc(100% - 2rem));font-size:.92rem;border-radius:18px;box-shadow:0 20px 80px rgba(0,0,0,.18);background:#fff;color:#111827}}
{selector} .cookie-banner a{{color:#111827}}
{selector} .target-media{{min-height:clamp(410px,48vw,690px);padding:clamp(1rem,3vw,2rem);display:grid;place-items:center;position:relative;isolation:isolate}}
{selector} .target-media>picture{{position:absolute;inset:0;z-index:-1}}
{selector} .target-media>picture img{{width:100%;height:100%;object-fit:cover;opacity:.13;filter:var(--image-filter)}}
{selector} .target-media figcaption{{position:absolute;left:1rem;right:1rem;bottom:1rem;z-index:2;border:1px solid color-mix(in srgb,var(--color-border) 70%,transparent);background:color-mix(in srgb,var(--color-surface) 82%,transparent);backdrop-filter:blur(12px)}}
{hero_layout}
{selector} .target-stage{{width:min(100%,760px);position:relative;z-index:1;display:grid;gap:1rem;color:var(--color-text)}}
{selector} .target-topline,.target-strip,.app-chrome{{display:flex;align-items:center;justify-content:space-between;gap:1rem;font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;font-weight:900}}
{selector} .target-rowset{{list-style:none;margin:0;padding:0;display:grid;gap:.7rem}}
{selector} .target-rowset li{{display:flex;justify-content:space-between;gap:1rem;padding:.85rem 1rem;border:1px solid var(--color-border);background:var(--color-surface);border-radius:var(--radius-sm)}}
{selector} .scan-orbit{{height:330px;border-radius:999px;display:grid;place-items:center;position:relative;border:1px solid var(--color-border);background:radial-gradient(circle,color-mix(in srgb,var(--color-accent) 20%,transparent),transparent 58%)}}
{selector} .scan-orbit span{{position:absolute;left:50%;top:50%;width:12px;height:12px;border-radius:999px;background:var(--color-primary);transform:rotate(var(--a)) translateX(135px)}}
{selector} .scan-orbit strong{{font-family:var(--font-display);font-size:clamp(3rem,8vw,6rem);line-height:.9}}
{selector} .scan-orbit em{{position:absolute;bottom:28%;font-style:normal;font-weight:900;color:var(--color-link)}}
{selector} .bio-grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:.45rem;padding:1rem;border:1px solid var(--color-border);background:color-mix(in srgb,var(--color-primary) 9%,transparent)}}
{selector} .bio-grid span{{aspect-ratio:1;border-radius:50%;background:color-mix(in srgb,var(--color-accent) 60%,transparent)}}
{selector} .pipeline-table,.app-board,.catalogue-grid,.poster-grid,.impact-grid,.product-shelf{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem}}
{selector} .pipeline-table div,.product-shelf article,.catalogue-grid article,.poster-grid article,.impact-grid article{{min-height:150px;padding:1rem;border:1px solid var(--color-border);background:var(--color-surface);border-radius:var(--radius-md);display:grid;align-content:space-between}}
{selector} .product-shelf article em{{display:block;width:54px;height:78px;border-radius:999px 999px 20px 20px;background:linear-gradient(180deg,var(--color-accent),var(--color-primary));margin-inline:auto}}
{selector} .network-map{{height:360px;position:relative;border:1px solid var(--color-border);background:linear-gradient(90deg,color-mix(in srgb,var(--color-primary) 18%,transparent) 1px,transparent 1px),linear-gradient(0deg,color-mix(in srgb,var(--color-primary) 18%,transparent) 1px,transparent 1px),color-mix(in srgb,var(--color-surface) 92%,transparent);background-size:42px 42px;overflow:hidden;border-radius:var(--radius-md)}}
{selector} .network-map span{{position:absolute;left:var(--x);top:var(--y);width:14px;height:14px;border-radius:50%;background:var(--color-accent);box-shadow:0 0 0 9px color-mix(in srgb,var(--color-accent) 22%,transparent)}}
{selector} .network-map svg{{position:absolute;inset:0;width:100%;height:100%}}
{selector} .network-map path{{fill:none;stroke:var(--color-primary);stroke-width:2.4;vector-effect:non-scaling-stroke}}
{selector} .app-chrome{{padding:.8rem 1rem;border:1px solid var(--color-border);border-radius:var(--radius-md) var(--radius-md) 0 0;background:color-mix(in srgb,var(--color-bg) 82%,var(--color-surface));color:var(--color-text)}}
{selector} .app-chrome span{{width:10px;height:10px;border-radius:50%;background:var(--color-accent)}}
{selector} .app-chrome b{{margin-left:auto}}
{selector} .app-board{{grid-template-columns:repeat(3,minmax(0,1fr));padding:1rem;border:1px solid var(--color-border);border-top:0;border-radius:0 0 var(--radius-md) var(--radius-md);background:color-mix(in srgb,var(--color-surface) 80%,transparent)}}
{selector} .app-board section{{display:grid;gap:.75rem;align-content:start}}
{selector} .app-board h4{{margin:0;font-size:.82rem;text-transform:uppercase;letter-spacing:.08em;color:var(--color-link)}}
{selector} .app-board ul{{list-style:none;margin:0;padding:0;display:grid;gap:.65rem}}
{selector} .app-board li{{padding:.8rem;border:1px solid var(--color-border);border-radius:var(--radius-sm);background:color-mix(in srgb,var(--color-bg) 82%,var(--color-surface));color:var(--color-text);font-size:.88rem}}
{selector} .app-board li span{{display:block;color:var(--color-muted);font-size:.7rem;font-family:var(--font-mono)}}
{selector} .calculator-panel,.service-card,.maison-frame,.editorial-plate{{padding:clamp(1.2rem,4vw,3rem);border:1px solid var(--color-border);background:var(--color-surface);border-radius:var(--radius-lg);box-shadow:var(--shadow-medium)}}
{selector} .calculator-panel{{display:grid;gap:.8rem;max-width:520px;margin-inline:auto}}
{selector} .calculator-panel h4{{font-family:var(--font-display);font-size:clamp(1.5rem,4vw,3rem);margin:0}}
{selector} .calculator-panel label{{display:flex;justify-content:space-between;border:1px solid var(--color-border);border-radius:var(--radius-sm);padding:1rem;background:color-mix(in srgb,var(--color-bg) 55%,white)}}
{selector} .calculator-panel button,.service-card button{{min-height:48px;border:0;background:var(--color-primary);color:var(--color-on-primary);border-radius:var(--radius-sm);font-weight:900}}
{selector} .editorial-plate{{min-height:330px;border-radius:0;display:grid;align-content:end;background:linear-gradient(135deg,color-mix(in srgb,var(--color-primary) 18%,transparent),transparent),var(--color-surface)}}
{selector} .editorial-plate strong{{font-family:var(--font-display);font-size:clamp(3rem,9vw,7rem);line-height:.9}}
{selector} .editorial-index{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--color-border)}}
{selector} .editorial-index li{{padding:1rem;border-right:1px solid var(--color-border)}}
{selector} .poster-grid article{{min-height:220px;border-radius:0;background:linear-gradient(160deg,color-mix(in srgb,var(--color-primary) 60%,var(--color-bg)),color-mix(in srgb,var(--color-accent) 45%,var(--color-surface)));color:var(--color-text)}}
{selector} .poster-grid article:nth-child(2),{selector} .poster-grid article:nth-child(4){{transform:translateY(1rem)}}
{selector} .catalogue-grid{{grid-template-columns:repeat(2,1fr);gap:0;border:1px solid var(--color-border);background:var(--color-surface)}}
{selector} .catalogue-grid article{{border-radius:0;border-width:0 1px 1px 0;min-height:220px}}
{selector} .service-card{{border-radius:0;box-shadow:none;max-width:620px;margin-inline:auto}}
{selector} .service-card h4{{font-size:clamp(2rem,6vw,4rem);margin:0 0 1rem;font-family:var(--font-display)}}
{selector} .service-card ol{{margin:0 0 1rem;padding:0;list-style:none;display:grid;gap:.75rem}}
{selector} .service-card li{{display:grid;grid-template-columns:2rem 1fr;gap:.75rem;align-items:center}}
{selector} .impact-grid{{grid-template-columns:repeat(3,1fr)}}
{selector} .impact-grid article b{{font-size:clamp(2rem,5vw,4rem);font-family:var(--font-display)}}
{selector} .maison-frame{{min-height:430px;border-radius:0;display:grid;place-items:center;text-align:center;background:radial-gradient(circle,color-mix(in srgb,var(--color-accent) 18%,transparent),transparent 55%),var(--color-surface)}}
{selector} .maison-frame strong{{font-family:var(--font-display);font-size:clamp(2.4rem,7vw,5.8rem);font-weight:400}}
{selector} .maison-frame span{{display:inline-block;margin:.25rem .5rem;border-top:1px solid var(--color-border);padding-top:.4rem;text-transform:uppercase;letter-spacing:.08em;font-size:.72rem}}
{selector} .target-profile-{profile}.target-stage{{min-height:360px}}
"""


def css_for_site(site: dict[str, object]) -> str:
    bg, primary, accent, ink, warm = site["palette"]  # type: ignore[index]
    number = int(site["number"])
    mode = str(site["themeMode"])
    passport = site["designPassport"]  # type: ignore[assignment]
    radius_base = {
        "civic": 0, "dark": 5, "editorial": 2, "commerce": 14,
        "hospitality": 20, "technical": 7, "care": 18, "luxury": 0, "professional": 10,
    }.get(mode, 10)
    if str(site["slug"]) == "luxury":
        radius_base = 0
    shape_radius = {
        "soft clinical cards": 28,
        "precise dossier panels": 6,
        "organic wellness curves": 34,
        "technical modules": 8,
        "pill product modules": 20,
        "signal tiles": 14,
        "sharp dark panels": 4,
        "metric cards": 10,
        "advisory note cards": 12,
        "cover comparison cards": 16,
        "document checklist cards": 2,
        "ledger blocks": 0,
        "framework cards": 10,
        "course path cards": 18,
        "split audience panels": 16,
        "listing cards": 8,
        "industrial slabs": 0,
        "editorial rectangles": 0,
        "material swatches": 4,
        "hard spec blocks": 0,
        "validation cards": 6,
        "output metric cards": 12,
        "square service tiles": 0,
        "impact metric cards": 14,
        "seasonal product cards": 18,
        "ingredient cards": 16,
        "menu cards": 10,
        "room cards": 14,
        "trip story cards": 4,
        "route cards": 8,
        "tracking cards": 6,
        "vehicle cards": 5,
        "fleet spec cards": 4,
        "vessel cards": 6,
        "product tiles": 18,
        "catalogue cards": 12,
        "lookbook cards": 0,
        "soft product capsules": 26,
        "episode cards": 8,
        "event cards": 6,
        "article cards": 2,
        "campaign case cards": 10,
        "portfolio cards": 0,
        "program cards": 16,
        "event portfolio cards": 18,
        "square civic boxes": 0,
        "impact cards": 20,
        "care cards": 22,
        "luxury hairline borders": 0,
        "media cards": 2,
    }
    radius_base = shape_radius.get(str(passport["shapeLanguage"]), radius_base)
    density_scale = {
        "compact": (46, 0.82, 1120),
        "dense": (50, 0.78, 1180),
        "practical": (58, 0.92, 1120),
        "medium": (70, 1.0, 1160),
        "relaxed": (86, 1.08, 1100),
        "image-rich": (78, 1.16, 1240),
        "spacious": (104, 1.22, 1200),
        "theatrical": (96, 1.18, 1280),
        "ultra-minimal": (126, 1.32, 1080),
    }
    density_space, density_gap, density_container = density_scale.get(str(passport["density"]), (76, 1.0, 1140))
    container = 1040 + (number % 6) * 54
    container = max(container, density_container)
    section_space = density_space + (number % 5) * 6
    shadow_opacity = ".20" if mode == "dark" else ".10"
    dark_palette = palette_is_dark(site)
    link_value = primary if contrast_ratio(bg, primary) >= 5 else best_contrast_color(bg, [accent, warm, ink, primary])
    link_on_light = primary if contrast_ratio("#ffffff", primary) >= 5 else best_contrast_color("#ffffff", [ink, accent, warm, primary])
    on_primary = color_on(primary)
    on_accent = color_on(accent)
    cta_bg = blend_hex(primary, warm, 0.88)
    on_cta = color_on(cta_bg)
    footer_bg = bg if dark_palette else primary if relative_luminance(primary) < 0.72 else ink
    footer_text = color_on(footer_bg)
    surface_value = f"color-mix(in srgb, {bg} 84%, {ink})" if dark_palette else "#ffffff"
    surface_alt_value = f"color-mix(in srgb, {accent} 14%, {bg})"
    surface_raised_value = f"color-mix(in srgb, {bg} 72%, {ink})" if dark_palette else f"color-mix(in srgb, white 96%, {accent})"
    muted_value = f"color-mix(in srgb, {ink} 94%, white)" if dark_palette else f"color-mix(in srgb, {ink} 96%, black)"
    border_value = f"color-mix(in srgb, {ink} 26%, {bg})" if dark_palette else f"color-mix(in srgb, {primary} 20%, white)"
    field_value = f"color-mix(in srgb, {bg} 74%, {ink})" if dark_palette else f"color-mix(in srgb, white 88%, {bg})"
    header_variant = {
        "civic": ".site-header{background:var(--color-surface);border-bottom:3px solid var(--color-text)}.header-utility{background:var(--color-primary);color:#fff}.site-nav a{border-radius:0;border-bottom:3px solid transparent}.site-nav a[aria-current=\"page\"]{border-bottom-color:var(--color-accent);background:transparent}.nav-cta,.button{border-radius:0;text-transform:none}",
        "dark": ".site-header{background:rgba(8,12,16,.92);color:#fff;border-bottom:1px solid rgba(255,255,255,.14)}.header-utility{background:#07090d;color:var(--color-accent)}.brand small,.site-nav a{color:rgba(255,255,255,.74)}.site-nav a[aria-current=\"page\"],.site-nav a:hover{background:rgba(255,255,255,.08);color:#fff}.nav-cta{box-shadow:0 0 22px color-mix(in srgb,var(--color-accent) 35%,transparent)}",
        "editorial": ".site-header{background:color-mix(in srgb,var(--color-bg) 94%,transparent);border-bottom:1px solid var(--color-border)}.header-utility{justify-content:center;background:transparent;border-bottom:1px solid var(--color-border);font-family:var(--font-display)}.nav-shell{min-height:96px}.brand{min-width:auto}.site-nav{margin-inline:auto}.nav-cta,.button{border-radius:0;background:transparent;color:var(--color-primary);border-color:currentColor}",
        "luxury": ".site-header{background:rgba(15,14,12,.72);color:var(--color-text);border-bottom:1px solid rgba(245,230,200,.20)}.header-utility{justify-content:center;background:transparent;color:var(--color-accent);font-family:var(--font-display);letter-spacing:.08em;text-transform:uppercase}.nav-shell{min-height:104px}.brand{min-width:auto}.site-nav{margin-inline:auto}.site-nav a{letter-spacing:.04em;text-transform:uppercase}.site-nav a[aria-current=\"page\"],.site-nav a:hover{background:transparent;color:var(--color-accent);text-decoration:underline;text-underline-offset:.4em}.nav-cta,.button{border-radius:0;background:transparent;color:var(--color-accent);border-color:var(--color-accent)}",
        "commerce": ".header-utility{background:var(--color-surface);border-bottom:1px solid var(--color-border)}.header-utility label{display:flex;align-items:center;gap:.6rem;min-width:min(520px,70vw)}.site-nav a,.nav-cta,.button{border-radius:16px}.nav-shell{min-height:72px}.nav-cta{box-shadow:var(--shadow-soft)}",
        "hospitality": ".header-utility{background:var(--color-text);color:#fff;justify-content:center}.booking-strip label{display:flex;align-items:center;gap:.5rem}.booking-strip input{max-width:150px;padding:.45rem .6rem}.site-nav a,.button,.nav-cta{border-radius:999px}.hero-section{padding-top:0}",
        "technical": ".site-header{background:color-mix(in srgb,var(--color-bg) 82%,transparent);border-bottom:1px solid var(--color-border)}.header-utility{font-family:ui-monospace,monospace;background:color-mix(in srgb,var(--color-primary) 8%,var(--color-bg));color:var(--color-primary)}.site-nav a,.button,.nav-cta{border-radius:8px}.brand small{font-family:ui-monospace,monospace}",
        "care": ".site-header{background:color-mix(in srgb,var(--color-bg) 90%,transparent);border-bottom:1px solid var(--color-border)}.header-utility{background:color-mix(in srgb,var(--color-accent) 10%,white);color:var(--color-link-on-light)}.site-nav a,.button,.nav-cta{border-radius:999px}.nav-shell{min-height:84px}",
        "professional": ".site-header{background:color-mix(in srgb,var(--color-bg) 88%,transparent);border-bottom:1px solid transparent}.header-utility{background:color-mix(in srgb,var(--color-primary) 9%,white);color:var(--color-link-on-light)}.site-nav a,.button,.nav-cta{border-radius:10px}",
    }[mode]
    hero_variant = {
        "civic": ".hero-grid{grid-template-columns:minmax(0,1fr);gap:1.5rem}.hero-media{order:-1;max-height:360px}.hero-media img{width:100%;height:360px;object-fit:cover}.hero-copy{border-left:6px solid var(--color-primary);padding-left:1.2rem}h1{max-width:18ch}",
        "dark": ".hero-section{background:radial-gradient(circle at 78% 18%,color-mix(in srgb,var(--color-accent) 24%,transparent),transparent 34%),linear-gradient(135deg,#05070b,var(--color-text));color:#fff}.hero-grid{grid-template-columns:minmax(0,.9fr) minmax(360px,1.1fr)}.hero-media{background:#07090d;border-color:rgba(255,255,255,.18);box-shadow:0 30px 80px rgba(0,0,0,.45)}.hero-proof span{background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.18);color:#fff}",
        "editorial": ".hero-section{padding-top:clamp(70px,10vw,150px)}.hero-grid{grid-template-columns:minmax(260px,.82fr) minmax(420px,1.18fr);align-items:end}.hero-media{border-radius:0;box-shadow:none}.hero-media img{aspect-ratio:4/5;object-fit:cover}h1{font-family:var(--font-display);font-weight:500;max-width:12ch}",
        "luxury": ".hero-section{background:var(--color-bg);color:var(--color-text);padding-top:clamp(90px,12vw,170px)}.hero-grid{grid-template-columns:minmax(260px,.72fr) minmax(460px,1.28fr);align-items:end}.hero-copy{max-width:680px}.hero-media{border-radius:0;box-shadow:none;border-color:rgba(245,230,200,.22)}.hero-media img{aspect-ratio:16/10;object-fit:cover;filter:saturate(.82) contrast(1.08)}h1{font-family:var(--font-display);font-weight:400;max-width:10ch}.hero-proof span{background:transparent;border-color:rgba(245,230,200,.28);color:var(--color-accent)}",
        "commerce": ".hero-grid{grid-template-columns:minmax(0,.95fr) minmax(380px,1.05fr)}.hero-media{border-radius:calc(var(--radius-lg) * 1.2)}.hero-proof{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}.hero-proof span{text-align:center;border-radius:18px}",
        "hospitality": ".hero-section{background:linear-gradient(180deg,rgba(0,0,0,.38),transparent),var(--color-bg)}.hero-grid{grid-template-columns:1fr}.hero-media{order:-1;max-height:560px;border-radius:0}.hero-media img{width:100%;height:min(62vh,560px);object-fit:cover}.hero-copy{max-width:760px;margin-top:-110px;background:var(--color-surface);padding:clamp(1rem,4vw,3rem);border-radius:var(--radius-lg);box-shadow:var(--shadow-strong)}",
        "technical": ".hero-grid{grid-template-columns:minmax(0,1fr) minmax(330px,.9fr)}.hero-copy{display:grid;gap:.55rem}.hero-media{border-radius:var(--radius-sm);background:repeating-linear-gradient(135deg,color-mix(in srgb,var(--color-primary) 7%,white),color-mix(in srgb,var(--color-primary) 7%,white) 12px,#fff 12px,#fff 24px)}.hero-proof span{font-family:ui-monospace,monospace;border-radius:var(--radius-sm)}",
        "care": ".hero-grid{grid-template-columns:minmax(0,1fr) minmax(320px,.82fr)}.hero-section{background:linear-gradient(145deg,color-mix(in srgb,var(--color-accent) 10%,var(--color-bg)),var(--color-bg))}.hero-copy{padding:clamp(1rem,3vw,2rem);background:color-mix(in srgb,var(--color-surface) 72%,transparent);border-radius:var(--radius-lg)}.hero-media{border-radius:38px 38px 12px 38px}",
        "professional": ".hero-grid{grid-template-columns:minmax(0,1.08fr) minmax(320px,.92fr)}.hero-media{transform:translateY(1rem)}.hero-proof span{border-radius:10px}",
    }[mode]
    card_variant = {
        "civic": ".mini-card,.price-card,.form-panel,.faq-list details{box-shadow:none;border:2px solid var(--color-border);border-radius:0}.card-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.mini-card{border-left:6px solid var(--color-primary)}",
        "dark": ".mini-card,.price-card,.form-panel,.faq-list details,.signature-panel{background:#0d1117;color:#fff;border-color:rgba(255,255,255,.14);box-shadow:0 24px 70px rgba(0,0,0,.35)}.mini-card h3,.price-card h3{color:var(--color-accent)}.content-section:nth-of-type(even){background:#080b10}.card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}",
        "editorial": ".card-grid{grid-template-columns:1.4fr .9fr .9fr;align-items:stretch}.mini-card,.price-card{box-shadow:none;border-radius:0;border-width:0 0 1px 0;background:transparent}.mini-card:first-child{font-family:var(--font-display);font-size:1.1rem}.visual-strip{grid-template-columns:1.3fr .7fr}.visual-strip figure{border-radius:0;box-shadow:none}",
        "luxury": ".content-section:nth-of-type(even){background:#171410}.card-grid{grid-template-columns:1.2fr 1fr .8fr}.mini-card,.price-card,.form-panel,.faq-list details,.signature-panel{background:rgba(255,255,255,.035);color:var(--color-text);box-shadow:none;border-color:rgba(245,230,200,.22);border-radius:0}.mini-card h3,.price-card h3{color:var(--color-accent);font-family:var(--font-display);font-weight:400}.visual-strip{grid-template-columns:1.6fr .8fr}.visual-strip figure{border-radius:0;box-shadow:none;background:transparent}.signature-controls button{background:transparent;color:var(--color-text);border-color:rgba(245,230,200,.28)}",
        "commerce": ".card-grid{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}.mini-card,.price-card{border-radius:22px;box-shadow:0 18px 45px rgba(15,23,42,.08)}.mini-card::before{content:\"\";display:block;width:42px;height:6px;background:var(--color-accent);border-radius:999px;margin-bottom:1rem}",
        "hospitality": ".card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.mini-card,.price-card{border-radius:28px;background:color-mix(in srgb,var(--color-surface) 86%,var(--color-bg));box-shadow:0 24px 60px rgba(0,0,0,.12)}.visual-strip figure:first-child{grid-column:span 2}",
        "technical": ".card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.mini-card,.price-card,.signature-panel{border-radius:var(--radius-sm);box-shadow:none;border:1px solid var(--color-border);background:linear-gradient(180deg,#fff,color-mix(in srgb,var(--color-primary) 5%,#fff))}.mini-card h3{font-family:ui-monospace,monospace}",
        "care": ".card-grid{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.mini-card,.price-card,.form-panel,.faq-list details{border-radius:24px;background:color-mix(in srgb,var(--color-surface) 90%,var(--color-bg));box-shadow:0 18px 50px rgba(15,23,42,.08)}.mini-card{border-top:5px solid color-mix(in srgb,var(--color-accent) 70%,white)}",
        "professional": ".mini-card,.price-card{border-radius:var(--radius-md)}.card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}",
    }[mode]
    footer_variant = {
        "civic": ".site-footer{background:var(--color-footer);color:var(--color-footer-text);border-top:4px solid var(--color-primary)}.site-footer a{color:inherit}.footer-bottom{border-top:2px solid color-mix(in srgb,var(--color-footer-text) 24%,transparent)}",
        "dark": ".site-footer{background:var(--color-footer);color:var(--color-footer-text)}.site-footer a{color:var(--color-footer-text)}.footer-grid{grid-template-columns:1.6fr repeat(5,1fr)}",
        "editorial": ".site-footer{background:var(--color-footer);color:var(--color-footer-text);border-top:1px solid var(--color-border)}.site-footer a{color:inherit}.footer-grid{grid-template-columns:2fr repeat(5,.9fr)}",
        "luxury": ".site-footer{background:#080705;color:var(--color-text);border-top:1px solid rgba(245,230,200,.20)}.site-footer a{color:inherit}.footer-grid{grid-template-columns:2fr repeat(5,.82fr)}.site-footer h2{font-family:var(--font-display);font-weight:400}",
        "commerce": ".site-footer{background:var(--color-footer);color:var(--color-footer-text)}.footer-grid{grid-template-columns:1.2fr repeat(5,1fr)}",
        "hospitality": ".site-footer{background:var(--color-footer);color:var(--color-footer-text)}.footer-brand{font-family:var(--font-display)}",
        "technical": ".site-footer{background:var(--color-footer);color:var(--color-footer-text)}.site-footer h2{font-family:ui-monospace,monospace;color:var(--color-footer-text)}",
        "care": ".site-footer{background:var(--color-footer);color:var(--color-footer-text)}.footer-brand{background:rgba(255,255,255,.08);padding:1rem;border-radius:var(--radius-lg)}",
        "professional": ".site-footer{background:var(--color-footer);color:var(--color-footer-text)}",
    }[mode]
    hero_case = number % 10
    card_case = number % 8
    pricing_case = number % 7
    cookie_case = number % 6
    header_case = number % 9
    media_ratio = ["16/10", "4/5", "1/1", "3/2", "21/9", "5/4", "9/12", "2/1", "7/5", "6/4"][hero_case]
    surface_texture = {
        "paper": "linear-gradient(0deg, rgba(0,0,0,.025) 1px, transparent 1px)",
        "console": "repeating-linear-gradient(0deg, rgba(255,255,255,.05) 0 1px, transparent 1px 9px)",
        "map": "linear-gradient(90deg, color-mix(in srgb,var(--color-primary) 8%,transparent) 1px, transparent 1px), linear-gradient(0deg, color-mix(in srgb,var(--color-primary) 8%,transparent) 1px, transparent 1px)",
        "texture": "radial-gradient(circle at 20% 20%, color-mix(in srgb,var(--color-accent) 14%,transparent) 0 1px, transparent 2px)",
    }
    surface_key = "console" if mode == "dark" else "map" if "map" in str(passport["surfaceMaterial"]) else "texture" if any(word in str(passport["surfaceMaterial"]) for word in ["texture", "fabric", "linen", "ingredient", "field"]) else "paper"
    mobile_case_css = [
        ".site-nav{left:1rem;right:auto;width:min(390px,calc(100% - 2rem));min-height:calc(100vh - 120px)}",
        ".site-nav{left:auto;right:1rem;width:min(410px,calc(100% - 2rem));min-height:calc(100vh - 120px)}",
        ".site-nav{inset:auto 0 0 0;border-radius:var(--radius-lg) var(--radius-lg) 0 0;padding:1.35rem;box-shadow:0 -20px 60px rgba(0,0,0,.18)}",
        ".site-nav{inset:0;border-radius:0;padding:7.5rem 2rem 2rem;font-family:var(--font-display);font-size:clamp(1.4rem,5vw,2.8rem)}",
        ".site-nav{inset:92px max(1rem,6vw) auto max(1rem,6vw);display:none;grid-template-columns:repeat(2,minmax(0,1fr))}",
        ".site-nav{inset:78px 1rem auto 1rem;border-left:8px solid var(--color-primary)}",
    ][cookie_case]
    header_case_css = [
        ".nav-shell{justify-content:space-between}.brand{min-width:auto}.site-nav{margin-inline:auto}",
        ".site-header{border-bottom-width:2px}.brand img{border:1px solid var(--color-border);padding:.2rem;background:var(--color-surface)}",
        ".nav-shell{min-height:var(--header-height)}.site-nav a{font-family:var(--font-accent);text-transform:uppercase;font-size:.78rem;letter-spacing:.08em}",
        ".header-utility{justify-content:space-between}.nav-cta{margin-left:.4rem}",
        ".site-header{backdrop-filter:none}.nav-shell{align-items:stretch}.brand{align-self:center}.site-nav a{display:flex;align-items:center}",
        ".brand strong{font-size:1.25rem}.brand small{max-width:22ch}.site-nav{gap:.55rem}",
        ".header-utility{font-family:var(--font-accent)}.nav-shell{border-inline:1px solid var(--color-border)}",
        ".site-header.is-scrolled .nav-shell{min-height:calc(var(--header-height) - 14px)}.nav-shell{transition:min-height var(--motion-base) ease}",
        ".nav-cta{min-width:150px}.menu-toggle{letter-spacing:.04em;text-transform:uppercase}",
    ][header_case]
    hero_case_css = [
        ".hero-grid{grid-template-columns:minmax(0,1fr) minmax(360px,.74fr)}.hero-media{align-self:stretch}.hero-copy{border-left:8px solid var(--color-primary)}",
        ".hero-grid{grid-template-columns:minmax(340px,.72fr) minmax(0,1.28fr)}.hero-media{order:-1}.hero-copy{max-width:760px}",
        ".hero-grid{grid-template-columns:1fr}.hero-media{order:-1}.hero-media img{width:100%;max-height:560px;object-fit:cover}.hero-copy{max-width:860px}",
        ".hero-grid{grid-template-columns:minmax(0,.86fr) minmax(420px,1.14fr);align-items:end}.hero-copy{padding-block:clamp(1rem,3vw,3rem)}",
        ".hero-grid{grid-template-columns:minmax(0,1.22fr) minmax(320px,.78fr)}.hero-media{transform:translateY(-1.2rem)}",
        ".hero-section{padding-top:0}.hero-grid{grid-template-columns:1fr}.hero-copy{width:min(900px,100%);margin-inline:auto;text-align:center}.hero-proof{justify-content:center}",
        ".hero-grid{grid-template-columns:minmax(280px,.66fr) minmax(0,1.34fr)}.hero-copy{order:2}.hero-media{order:1}",
        ".hero-grid{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}.hero-copy{background:var(--color-surface-alt);padding:clamp(1rem,3vw,2.4rem);box-shadow:var(--shadow-soft)}",
        ".hero-grid{grid-template-columns:minmax(0,.94fr) minmax(380px,1.06fr)}.hero-section{border-bottom:1px solid var(--color-border)}",
        ".hero-grid{display:block}.hero-copy{width:min(820px,100%)}.hero-media{margin-top:2rem;margin-left:auto;width:min(760px,100%)}",
    ][hero_case]
    card_case_css = [
        ".card-grid{grid-template-columns:1fr 1fr 1fr}.mini-card:nth-child(2){transform:translateY(1rem)}",
        ".card-grid{grid-template-columns:1.3fr .85fr .85fr}.mini-card:first-child{min-height:220px}",
        ".card-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.mini-card:last-child{grid-column:1/-1}",
        ".card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.mini-card{border-left:6px solid var(--color-primary)}",
        ".card-grid{grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}.mini-card{aspect-ratio:1.08/1}",
        ".card-grid{grid-template-columns:.8fr 1.2fr 1fr}.mini-card{box-shadow:none}",
        ".card-grid{display:flex;overflow:auto;scroll-snap-type:x mandatory}.mini-card{min-width:min(330px,82vw);scroll-snap-align:start}",
        ".card-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.mini-card:nth-child(odd){background:var(--color-surface-alt)}",
    ][card_case]
    pricing_case_css = [
        ".pricing-grid{grid-template-columns:1fr 1.35fr 1fr}.price-card.featured{transform:scale(1.035)}",
        ".pricing-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.price-card strong{font-family:var(--font-display);font-size:2.2rem}",
        ".pricing-grid{display:grid;grid-template-columns:1fr}.price-card{display:grid;grid-template-columns:1fr 2fr auto;align-items:center}",
        ".pricing-grid{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.price-card{border-top:8px solid var(--color-accent)}",
        ".pricing-grid{grid-template-columns:1.1fr .9fr 1.1fr}.price-card{box-shadow:none;border-style:dashed}",
        ".pricing-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.price-card{border-radius:999px;padding:2rem;text-align:center}",
        ".pricing-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.price-card.featured{order:-1}",
    ][pricing_case]
    cookie_case_css = [
        ".cookie-banner{left:1rem;right:auto;max-width:520px}",
        ".cookie-banner{left:auto;right:1rem;max-width:520px}",
        ".cookie-banner{left:0;right:0;bottom:0;border-radius:0}",
        ".cookie-banner{left:50%;right:auto;transform:translateX(-50%);max-width:620px}",
        ".cookie-banner{top:1rem;bottom:auto;left:auto;right:1rem;max-width:500px}",
        ".cookie-banner{left:1rem;right:1rem;bottom:1rem;border-style:dashed}",
    ][cookie_case]
    premium_variant = f"""
body::before{{content:"";position:fixed;inset:0;pointer-events:none;z-index:-1;background-image:{surface_texture[surface_key]};background-size:{18 + number % 9}px {18 + number % 9}px;opacity:.38}}
body.theme-{site['slug']} .site-header{{min-height:var(--header-height)}}
body.theme-{site['slug']} .hero-media img{{aspect-ratio:{media_ratio};object-fit:cover;filter:var(--image-filter)}}
body.theme-{site['slug']} .hero-media{{border-radius:var(--image-radius);position:relative}}
body.theme-{site['slug']} .hero-media::after{{content:"{number:02d}";position:absolute;right:1rem;top:1rem;font-family:var(--font-accent);font-size:.82rem;background:var(--color-surface);color:var(--color-primary);border:1px solid var(--color-border);padding:.35rem .55rem}}
body.theme-{site['slug']} .section-grid{{grid-template-columns:minmax(0,{0.82 + (number % 5) * .08:.2f}fr) minmax(280px,{1.18 - (number % 5) * .05:.2f}fr)}}
body.theme-{site['slug']} .eyebrow{{font-family:var(--font-accent);letter-spacing:{0.04 + (number % 5) * .015:.3f}em}}
body.theme-{site['slug']} h1{{font-weight:{400 + (number % 5) * 100};font-size:clamp(2.2rem,{4.8 + (number % 4) * .45:.2f}vw,6.4rem)}}
body.theme-{site['slug']} h2{{font-weight:{450 + (number % 4) * 100}}}
body.theme-{site['slug']} .button.primary{{background:var(--color-cta);color:var(--color-on-cta);border-color:var(--color-cta);box-shadow:var(--shadow-medium)}}
body.theme-{site['slug']} .button.secondary{{background:transparent;color:var(--color-link);border-color:currentColor}}
body.theme-{site['slug']} .resource-board{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:var(--grid-gap);margin-top:1.5rem}}
body.theme-{site['slug']} .resource-card{{padding:var(--card-padding);background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);box-shadow:var(--shadow-soft)}}
body.theme-{site['slug']} .resource-card span{{font-family:var(--font-accent);color:var(--color-link);font-weight:900;text-transform:uppercase;font-size:.72rem;letter-spacing:.08em}}
body.theme-{site['slug']} .cta-panel{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:var(--grid-gap);align-items:center;padding:clamp(1.2rem,4vw,3rem);background:var(--color-surface-alt);border:1px solid var(--color-border);border-radius:var(--radius-lg);box-shadow:var(--shadow-medium)}}
body.theme-{site['slug']} .legal-page .prose{{max-width:min(860px,100%);padding:clamp(1.25rem,4vw,3rem);background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-lg);box-shadow:var(--shadow-soft)}}
{header_case_css}
{hero_case_css}
{card_case_css}
{pricing_case_css}
{cookie_case_css}
"""
    inspiration_background = {
        "care": "radial-gradient(circle at 12% 18%, color-mix(in srgb,var(--color-accent) 34%,transparent), transparent 28%), linear-gradient(90deg, transparent 48%, color-mix(in srgb,var(--color-primary) 10%,transparent) 48% 52%, transparent 52%)",
        "technical": "linear-gradient(90deg,color-mix(in srgb,var(--color-primary) 12%,transparent) 1px,transparent 1px),linear-gradient(0deg,color-mix(in srgb,var(--color-primary) 12%,transparent) 1px,transparent 1px)",
        "dark": "radial-gradient(circle at 72% 22%, color-mix(in srgb,var(--color-accent) 26%,transparent), transparent 32%), repeating-linear-gradient(0deg,rgba(255,255,255,.05) 0 1px,transparent 1px 10px)",
        "editorial": "linear-gradient(90deg, transparent 0 18%, color-mix(in srgb,var(--color-primary) 12%,transparent) 18% 18.25%, transparent 18.25% 100%), linear-gradient(180deg,transparent 0 72%,color-mix(in srgb,var(--color-accent) 16%,transparent) 72% 72.4%,transparent 72.4%)",
        "luxury": "linear-gradient(90deg,transparent 0 7%,rgba(245,230,200,.20) 7% 7.08%,transparent 7.08% 92%,rgba(245,230,200,.20) 92% 92.08%,transparent 92.08%),radial-gradient(circle at 74% 18%,rgba(245,230,200,.10),transparent 30%)",
        "commerce": "radial-gradient(circle at 18% 22%, color-mix(in srgb,var(--color-accent) 32%,transparent), transparent 25%), linear-gradient(135deg,color-mix(in srgb,var(--color-primary) 9%,transparent),transparent 44%)",
        "hospitality": "linear-gradient(180deg,rgba(0,0,0,.18),transparent 45%), radial-gradient(circle at 70% 12%, color-mix(in srgb,var(--color-warm) 28%,transparent),transparent 34%)",
        "civic": "linear-gradient(90deg,var(--color-primary) 0 8px,transparent 8px 100%),linear-gradient(180deg,color-mix(in srgb,var(--color-primary) 10%,transparent),transparent 42%)",
        "professional": "linear-gradient(90deg,color-mix(in srgb,var(--color-primary) 10%,transparent) 1px,transparent 1px),linear-gradient(180deg,color-mix(in srgb,var(--color-accent) 11%,transparent),transparent 42%)",
    }[mode]
    inspiration_variant = f"""
body.theme-{site['slug']} .hero-section{{position:relative;overflow:hidden;isolation:isolate}}
body.theme-{site['slug']} .hero-section::before{{content:"";position:absolute;inset:0;z-index:-1;background:{inspiration_background};background-size:{52 + number % 8 * 7}px {52 + number % 8 * 7}px, auto;opacity:{'.72' if mode in {'dark','luxury'} else '.56'}}}
body.theme-{site['slug']} .hero-copy h2{{max-width:min(760px,100%);font-size:clamp(1.15rem,2.2vw,1.9rem);line-height:var(--line-normal);color:color-mix(in srgb,var(--color-text) 78%,var(--color-primary))}}
body.theme-{site['slug']} .hero-proof span{{box-shadow:var(--shadow-soft)}}
body.theme-{site['slug']} .content-section[data-composition="dashboard panel"],body.theme-{site['slug']} .content-section[data-composition="metric band"]{{background:linear-gradient(180deg,color-mix(in srgb,var(--color-primary) 9%,var(--color-bg)),var(--color-bg))}}
body.theme-{site['slug']} .content-section[data-composition="gallery wall"],body.theme-{site['slug']} .content-section[data-composition="full-bleed image"],body.theme-{site['slug']} .content-section[data-composition="case-study block"]{{background:color-mix(in srgb,var(--color-text) 7%,var(--color-bg))}}
body.theme-{site['slug']} .process-list li:nth-child(2),body.theme-{site['slug']} .mini-card:nth-child(2),body.theme-{site['slug']} .metric-card:nth-child(2){{transform:translateY({'.75rem' if number % 2 else '-.35rem'})}}
body.theme-{site['slug']} .finder-panel{{border-inline-width:var(--border-strong)}}
"""
    target_component_variant = target_component_css_for_site(site)
    target_variant = target_css_for_site(site)
    clone_shell_variant = clone_shell_css_for_site(site)
    return f""":root {{
  --font-display: {site['typographyDisplay']};
  --font-body: {site['typographyBody']};
  --font-accent: {site['typographyAccent']};
  --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  --text-xs: {0.74 + (number % 4) * .02:.2f}rem;
  --text-sm: {0.88 + (number % 3) * .02:.2f}rem;
  --text-md: 1rem;
  --text-lg: {1.12 + (number % 5) * .03:.2f}rem;
  --text-xl: {1.42 + (number % 4) * .06:.2f}rem;
  --text-hero: clamp(2.2rem, {4.4 + (number % 5) * .38:.2f}vw, {5.4 + (number % 4) * .28:.2f}rem);
  --line-tight: {1.02 + (number % 3) * .02:.2f};
  --line-normal: {1.52 + (number % 4) * .03:.2f};
  --line-loose: {1.76 + (number % 5) * .03:.2f};
  --tracking-tight: 0;
  --tracking-normal: 0;
  --tracking-wide: {0.045 + (number % 6) * .008:.3f}em;
  --color-bg: {bg};
  --color-bg-alt: color-mix(in srgb, {accent} 7%, {bg});
  --color-surface: {surface_value};
  --color-surface-alt: {surface_alt_value};
  --color-surface-raised: {surface_raised_value};
  --color-text: {ink};
  --color-heading: {ink};
  --color-muted: {muted_value};
  --color-primary: {primary};
  --color-on-primary: {on_primary};
  --color-secondary: color-mix(in srgb, {primary} 62%, {accent});
  --color-accent: {accent};
  --color-on-accent: {on_accent};
  --color-border: {border_value};
  --color-success: color-mix(in srgb, #16a34a 82%, {accent});
  --color-warning: {warm};
  --color-error: color-mix(in srgb, #dc2626 86%, {warm});
  --gradient-primary: linear-gradient({120 + (number % 5) * 18}deg, var(--color-primary), var(--color-accent));
  --gradient-surface: linear-gradient(180deg, var(--color-surface), var(--color-bg-alt));
  --overlay-dark: rgba(15, 23, 42, {0.42 + (number % 3) * .05:.2f});
  --overlay-light: rgba(255, 255, 255, {0.62 + (number % 4) * .04:.2f});
  --color-link: {link_value};
  --color-link-on-light: {link_on_light};
  --color-cta: color-mix(in srgb, {primary} 88%, {warm});
  --color-on-cta: {on_cta};
  --color-footer: {footer_bg};
  --color-footer-text: {footer_text};
  --color-field: {field_value};
  --color-warm: {warm};
  --container-sm: {min(820, container - 260)}px;
  --container-md: {min(980, container - 120)}px;
  --container-lg: {container}px;
  --container-xl: {container + 180}px;
  --container-fluid: calc(100% - 40px);
  --container: {container}px;
  --container-wide: {container + 180}px;
  --section-padding: clamp({section_space - 28}px, 8vw, {section_space + 48}px);
  --space-xs: {0.34 + (number % 3) * .04:.2f}rem;
  --space-sm: {0.68 + (number % 4) * .05:.2f}rem;
  --space-md: {1.0 + (number % 5) * .06:.2f}rem;
  --space-lg: {1.55 + (number % 5) * .12:.2f}rem;
  --space-xl: {2.35 + (number % 5) * .18:.2f}rem;
  --space-section: var(--section-padding);
  --grid-gap: clamp({.82 * density_gap:.2f}rem, {2.2 * density_gap:.2f}vw, {1.55 * density_gap:.2f}rem);
  --content-measure: {58 + (number % 8) * 3}ch;
  --radius-none: 0;
  --radius-sm: {max(0, radius_base - 6)}px;
  --radius-md: {radius_base}px;
  --radius-lg: {radius_base + 14}px;
  --radius-xl: {radius_base + 28}px;
  --radius-pill: 999px;
  --shadow-none: none;
  --shadow-soft: 0 16px 45px rgba(15, 23, 42, {shadow_opacity});
  --shadow-medium: 0 22px 70px rgba(15, 23, 42, {'.22' if mode == 'dark' else '.13'});
  --shadow-strong: 0 30px 90px rgba(15, 23, 42, .20);
  --shadow-glow: 0 0 {24 + (number % 5) * 4}px color-mix(in srgb, var(--color-accent) {22 + (number % 5) * 3}%, transparent);
  --border-thin: 1px;
  --border-medium: {2 + (number % 2)}px;
  --border-strong: {3 + (number % 3)}px;
  --motion-fast: {130 + (number % 5) * 20}ms;
  --motion-base: {210 + (number % 6) * 35}ms;
  --motion-slow: {420 + (number % 7) * 50}ms;
  --motion-ease: cubic-bezier(.2, .7, .2, 1);
  --header-height: {70 + (number % 6) * 8}px;
  --image-radius: {max(0, radius_base + (number % 4) * 6)}px;
  --image-filter: {'saturate(.78) contrast(1.08)' if mode in {'luxury', 'dark'} else 'saturate(1.04) contrast(1.02)'};
  --card-padding: clamp({0.95 * density_gap:.2f}rem, 2vw, {1.45 * density_gap:.2f}rem);
  --container-width: var(--container-lg);
  --motion-speed: var(--motion-base);
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; font-family: var(--font-body); color: var(--color-text); background: var(--color-bg); line-height: 1.62; overflow-x: hidden; }}
body.menu-open {{ overflow: hidden; }}
a {{ color: inherit; }}
img {{ max-width: 100%; height: auto; display: block; }}
picture {{ display: block; }}
.container {{ width: min(var(--container-width), calc(100% - 40px)); margin: 0 auto; }}
.skip-link {{ position: fixed; left: 1rem; top: -5rem; z-index: 100; background: var(--color-primary); color: var(--color-on-primary); padding: .75rem 1rem; border-radius: var(--radius-sm); }}
.skip-link:focus {{ top: 1rem; }}
.site-header {{ position: sticky; top: 0; z-index: 50; backdrop-filter: blur(16px); transition: background var(--motion-speed) ease, border var(--motion-speed) ease, box-shadow var(--motion-speed) ease; }}
.site-header.is-scrolled {{ box-shadow: 0 10px 30px rgba(15,23,42,.08); }}
.header-utility {{ min-height: 34px; display: flex; flex-wrap: wrap; gap: .9rem; align-items: center; justify-content: flex-end; padding: .45rem max(20px, calc((100vw - var(--container-width)) / 2)); font-size: .84rem; font-weight: 800; }}
.header-utility a {{ text-decoration: underline; text-underline-offset: .2em; }}
.header-utility input {{ min-height: 34px; border: 1px solid var(--color-border); }}
.nav-shell {{ display: flex; align-items: center; gap: 1rem; min-height: 78px; }}
.brand {{ display: inline-flex; align-items: center; gap: .75rem; text-decoration: none; min-width: 240px; }}
.brand strong {{ display: block; font-family: var(--font-display); font-size: 1.08rem; letter-spacing: 0; }}
.brand small {{ display: block; color: color-mix(in srgb, currentColor 86%, var(--color-bg)); font-size: .76rem; max-width: 28ch; }}
.site-nav {{ margin-left: auto; display: flex; gap: .25rem; align-items: center; }}
.site-nav a {{ text-decoration: none; padding: .72rem .85rem; font-weight: 780; font-size: .9rem; }}
.site-nav a[aria-current="page"], .site-nav a:hover {{ background: color-mix(in srgb, var(--color-primary) 12%, var(--color-surface)); color: var(--color-text); }}
.nav-cta, .button {{ display: inline-flex; min-height: 44px; align-items: center; justify-content: center; padding: .82rem 1.08rem; text-decoration: none; border: 1px solid var(--color-border); font-weight: 850; text-align: center; }}
.button.primary, .nav-cta {{ background: var(--color-primary); color: var(--color-on-primary); border-color: var(--color-primary); }}
.button.secondary {{ background: var(--color-surface); color: var(--color-text); }}
.menu-toggle {{ display: none; margin-left: auto; min-height: 44px; border: 1px solid var(--color-border); background: var(--color-surface); border-radius: var(--radius-md); padding: .62rem .9rem; font-weight: 850; color: var(--color-text); }}
.section {{ padding: var(--space-section) 0; }}
.hero-section {{ padding-top: clamp(44px, 7vw, 96px); }}
.hero-grid, .section-grid {{ display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, .95fr); gap: clamp(2rem, 5vw, 5rem); align-items: center; }}
.hero-media, .mini-card, .price-card, .form-panel, .legal-page .prose, .faq-list details, .visual-strip figure, .signature-panel {{ background: color-mix(in srgb, var(--color-surface) 92%, var(--color-bg)); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-soft); }}
.hero-media {{ margin: 0; overflow: hidden; }}
.hero-media picture img {{ width:100%; height:100%; object-fit:cover; }}
.hero-media figcaption, .visual-strip figcaption {{ padding: .9rem 1rem; color: var(--color-muted); font-size: .92rem; }}
.section-icon {{ width:64px; height:64px; object-fit:contain; margin-bottom:1rem; border-radius:var(--radius-sm); }}
.eyebrow {{ text-transform: uppercase; letter-spacing: .08em; color: var(--color-link); font-weight: 900; font-size: .78rem; }}
h1, h2, h3 {{ line-height: 1.08; margin: 0 0 1rem; letter-spacing: 0; color: var(--color-heading); }}
h1 {{ font-family: var(--font-display); font-size: clamp(2.35rem, 7vw, 5.7rem); max-width: 13ch; }}
h2 {{ font-family: var(--font-display); font-size: clamp(1.65rem, 4vw, 3.1rem); }}
h3 {{ font-size: 1.05rem; }}
.lead {{ font-size: clamp(1.08rem, 2vw, 1.28rem); color: var(--color-muted); max-width: 66ch; }}
.button-row {{ display: flex; flex-wrap: wrap; gap: .75rem; margin-top: 1.5rem; }}
.hero-proof {{ display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1.25rem; }}
.hero-proof span, .eyebrow, .text-link {{ font-weight: 850; }}
.hero-proof span {{ border: 1px solid var(--color-border); border-radius: 999px; padding: .45rem .7rem; background: color-mix(in srgb, var(--color-accent) 10%, white); color: var(--color-link-on-light); }}
.content-section:nth-of-type(even) {{ background: color-mix(in srgb, var(--color-accent) 7%, var(--color-bg)); }}
.card-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; }}
.mini-card, .price-card {{ padding: 1.2rem; }}
.mini-card .card-thumb {{ width:100%; aspect-ratio:3/2; object-fit:cover; border-radius:calc(var(--radius-md) * .75); margin-bottom:1rem; background:var(--color-bg-alt); }}
.mini-card h3, .price-card h3 {{ color: var(--color-link); }}
.process-list, .checklist-panel {{ list-style:none; margin:0; padding:0; display:grid; gap:.85rem; }}
.process-list li, .checklist-panel li {{ display:grid; grid-template-columns:auto 1fr; gap:1rem; align-items:start; padding:var(--card-padding); background:var(--color-surface); color:var(--color-text); border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-md); box-shadow:var(--shadow-soft); }}
.process-list span {{ display:grid; place-items:center; width:2.65rem; height:2.65rem; background:var(--color-primary); color:var(--color-on-primary); border-radius:var(--radius-pill); font-family:var(--font-accent); font-weight:900; }}
.checklist-panel span {{ width:1rem; height:1rem; margin-top:.35rem; border:var(--border-medium) solid var(--color-primary); background:var(--color-surface-raised); transform:rotate(45deg); }}
.dashboard-panel {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1rem; align-items:stretch; }}
.metric-card {{ padding:var(--card-padding); background:var(--gradient-surface); border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-md); box-shadow:var(--shadow-soft); }}
.metric-card span {{ display:block; color:var(--color-link); font-weight:900; font-size:var(--text-xs); text-transform:uppercase; letter-spacing:var(--tracking-wide); }}
.metric-card strong {{ display:block; margin:.45rem 0; font-family:var(--font-display); font-size:clamp(2rem,4vw,4.5rem); line-height:var(--line-tight); }}
.map-panel {{ display:grid; grid-template-columns:1fr; gap:1rem; }}
.map-canvas {{ position:relative; min-height:230px; overflow:hidden; border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-md); background:linear-gradient(90deg,color-mix(in srgb,var(--color-primary) 12%,transparent) 1px,transparent 1px),linear-gradient(0deg,color-mix(in srgb,var(--color-primary) 12%,transparent) 1px,transparent 1px),var(--color-surface); background-size:42px 42px; box-shadow:var(--shadow-soft); }}
.map-canvas::before {{ content:""; position:absolute; inset:18% 8%; border:var(--border-medium) solid color-mix(in srgb,var(--color-accent) 70%,transparent); border-radius:45% 55% 42% 58%; transform:rotate(-8deg); }}
.map-canvas span {{ position:absolute; left:var(--x); top:var(--y); width:1rem; height:1rem; border-radius:var(--radius-pill); background:var(--color-primary); box-shadow:0 0 0 .55rem color-mix(in srgb,var(--color-primary) 16%,transparent); }}
.map-list {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.75rem; }}
.map-list article {{ padding:1rem; background:var(--color-surface); color:var(--color-text); border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-sm); }}
.visual-card-stack {{ display:grid; grid-template-columns:1.2fr .8fr; gap:1rem; align-items:stretch; }}
.visual-card-stack figure {{ margin:0; overflow:hidden; background:var(--color-surface); color:var(--color-text); border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-md); box-shadow:var(--shadow-soft); }}
.visual-card-stack figure:first-child {{ grid-row:span 2; }}
.visual-card-stack img {{ width:100%; height:100%; object-fit:cover; min-height:210px; }}
.visual-card-stack figcaption {{ padding:1rem; display:grid; gap:.45rem; color:var(--color-muted); }}
.finder-panel {{ display:grid; gap:1rem; padding:var(--card-padding); background:var(--gradient-surface); color:var(--color-text); border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-lg); box-shadow:var(--shadow-medium); }}
.finder-panel div {{ display:flex; flex-wrap:wrap; gap:.55rem; }}
.finder-panel button {{ min-height:42px; border:var(--border-thin) solid var(--color-border); border-radius:var(--radius-pill); background:var(--color-surface); color:var(--color-text); padding:.55rem .8rem; font-weight:850; }}
.composition-full-bleed-image .section-grid, .composition-gallery-wall .section-grid, .composition-case-study-block .section-grid {{ align-items:stretch; }}
.composition-dashboard-panel .section-copy, .composition-metric-band .section-copy {{ align-self:center; }}
.text-link {{ color: var(--color-link); text-decoration-thickness: .15em; text-underline-offset: .25em; }}
.pricing-grid, .visual-strip {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1.5rem; }}
.price-card.featured {{ transform: translateY(-.35rem); border-color: var(--color-primary); }}
.faq-list {{ display: grid; gap: .8rem; margin-top: 1.5rem; }}
.faq-list details {{ padding: 1rem 1.2rem; }}
.faq-list summary {{ cursor: pointer; font-weight: 900; }}
.form-panel {{ padding: clamp(1rem, 3vw, 2rem); margin-top: 1.5rem; display:grid; grid-template-columns:minmax(180px,.46fr) minmax(0,1fr); gap:clamp(1rem,3vw,2rem); align-items:stretch; color:var(--color-text); }}
.form-visual {{ margin:0; min-height:100%; border-radius:var(--radius-md); overflow:hidden; background:var(--color-bg-alt); }}
.form-visual img {{ width:100%; height:100%; min-height:260px; object-fit:cover; }}
.form-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }}
label {{ display: grid; gap: .35rem; font-weight: 800; }}
input, textarea, select {{ width: 100%; border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: .85rem 1rem; font: inherit; background: var(--color-field); color: var(--color-text); }}
textarea {{ resize: vertical; }}
.honeypot {{ position: absolute; left: -9999px; }}
.consent-field {{ display: grid; grid-template-columns: auto 1fr; align-items: start; gap: .6rem; margin: 1rem 0; font-weight: 600; }}
.consent-field input {{ width: auto; margin-top: .35rem; }}
.form-status {{ color: var(--color-text); }}
.signature-panel {{ display: grid; grid-template-columns: 1fr auto; gap: 1rem; align-items: center; margin-top: 1.25rem; padding: 1rem; }}
.signature-controls {{ display: flex; flex-wrap: wrap; gap: .5rem; justify-content: flex-end; }}
.signature-controls button {{ min-height: 40px; border: 1px solid var(--color-border); background: var(--color-surface); color: var(--color-text); border-radius: var(--radius-sm); padding: .55rem .8rem; font-weight: 850; }}
.signature-controls button[aria-pressed="true"] {{ background: var(--color-primary); color: var(--color-on-primary); border-color: var(--color-primary); }}
.signature-panel output {{ grid-column: 1 / -1; color: var(--color-muted); }}
.resource-board {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:1rem; margin-top:1.5rem; }}
.resource-card img {{ width:100%; aspect-ratio:3/2; object-fit:cover; border-radius:calc(var(--radius-md) * .75); margin-bottom:1rem; }}
.cta-panel {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(180px,.34fr) auto; gap:1.2rem; align-items:center; padding:clamp(1rem,3vw,2rem); margin-top:1.5rem; background:var(--color-surface); color:var(--color-text); border:1px solid var(--color-border); border-radius:var(--radius-lg); box-shadow:var(--shadow-soft); }}
.cta-panel img {{ width:100%; aspect-ratio:3/2; object-fit:cover; border-radius:var(--radius-md); }}
.utility-visual {{ margin:0 0 1.5rem; border-radius:var(--radius-md); overflow:hidden; background:var(--color-bg-alt); }}
.utility-visual img {{ width:100%; max-height:360px; object-fit:cover; }}
.disclaimer {{ padding: 34px 0; background: color-mix(in srgb, var(--color-warm) 10%, white); color: var(--color-link-on-light); }}
.disclaimer h2 {{ font-size: 1.2rem; color: inherit; }}
.site-footer {{ padding: 64px 0 24px; background: var(--color-footer); color: var(--color-footer-text); }}
.footer-grid {{ display: grid; grid-template-columns: 1.4fr repeat(5, 1fr); gap: 1.4rem; }}
.site-footer h2 {{ font-size: 1rem; color: inherit; }}
.site-footer ul {{ list-style: none; margin: 0; padding: 0; display: grid; gap: .45rem; }}
.site-footer a {{ color: var(--color-footer-text); }}
.footer-bottom {{ display: flex; justify-content: space-between; gap: 1rem; border-top: 1px solid rgba(255,255,255,.2); padding-top: 1rem; margin-top: 2rem; }}
.back-to-top {{ position: fixed; right: 1rem; bottom: 1rem; min-height: 44px; border-radius: 999px; border: 0; background: var(--color-primary); color: var(--color-on-primary); padding: .75rem 1rem; display: none; font-weight: 900; }}
.back-to-top.is-visible {{ display: block; }}
.cookie-banner {{ position: fixed; left: 1rem; right: 1rem; bottom: 1rem; display: none; gap: 1rem; align-items: center; justify-content: space-between; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-strong); padding: 1rem; z-index: 70; }}
.cookie-banner.is-visible {{ display: flex; }}
.cookie-banner button {{ min-height: 44px; border: 0; border-radius: var(--radius-sm); background: var(--color-primary); color: var(--color-on-primary); font-weight: 900; padding: .7rem 1rem; }}
:focus-visible {{ outline: 3px solid var(--color-warm); outline-offset: 3px; }}
{header_variant}
{hero_variant}
{card_variant}
{footer_variant}
{premium_variant}
{inspiration_variant}
{target_component_variant}
{target_variant}
{clone_shell_variant}
@media (max-width: 980px) {{
  .header-utility {{ justify-content: flex-start; padding-inline: 20px; }}
  .menu-toggle {{ display: inline-flex; align-items: center; }}
  .site-nav {{ position: fixed; inset: 78px 1rem auto 1rem; display: none; flex-direction: column; align-items: stretch; padding: 1rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); box-shadow: var(--shadow-strong); }}
  body.mode-dark .site-nav {{ background:#080b10; color:#fff; }}
  body.mode-editorial .site-nav, body.mode-luxury .site-nav {{ inset: 0; border-radius: 0; padding-top: 7rem; }}
  body.mode-hospitality .site-nav, body.mode-commerce .site-nav {{ inset: auto 0 0 0; border-radius: 26px 26px 0 0; }}
  {mobile_case_css}
  body.menu-open .site-nav {{ display: flex; }}
  .nav-cta {{ display: none; }}
  .hero-grid, .section-grid, .footer-grid, .signature-panel {{ grid-template-columns: 1fr; }}
  .card-grid, .pricing-grid, .visual-strip, .form-grid, .form-panel, .dashboard-panel, .map-list, .visual-card-stack, .resource-board, .cta-panel {{ grid-template-columns: 1fr; }}
  .visual-card-stack figure:first-child {{ grid-row:auto; }}
  .hero-copy {{ margin-top: 0; }}
  .hero-media img {{ height: auto; }}
  h1 {{ max-width: 100%; }}
}}
@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{ scroll-behavior: auto !important; transition-duration: .01ms !important; animation-duration: .01ms !important; }}
}}
@media print {{
  .site-header, .site-footer, .cookie-banner, .back-to-top {{ display: none !important; }}
  body {{ background: white; color: black; }}
  .section {{ padding: 20px 0; }}
}}
"""


def js_source(site: dict[str, object]) -> str:
    return """(() => {
  const signature = __SIGNATURE__;
  const body = document.body;
  const header = document.querySelector('[data-header]');
  const menuToggle = document.querySelector('[data-menu-toggle]');
  const backToTop = document.querySelector('[data-back-to-top]');
  const cookieBanner = document.querySelector('[data-cookie-banner]');
  const acceptCookie = document.querySelector('[data-cookie-accept]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const setCookie = (name, value) => {
    document.cookie = `${name}=${value}; path=/; max-age=31536000; SameSite=Lax`;
  };
  const hasCookie = (name) => document.cookie.split('; ').some((row) => row.startsWith(`${name}=`));
  const updateChrome = () => {
    if (header) header.classList.toggle('is-scrolled', window.scrollY > 24);
    if (backToTop) backToTop.classList.toggle('is-visible', window.scrollY > 800);
    const scrollMax = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    document.documentElement.style.setProperty('--scroll-progress', `${Math.min(1, window.scrollY / scrollMax)}`);
  };
  updateChrome();
  window.addEventListener('scroll', updateChrome, { passive: true });
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      const open = !body.classList.contains('menu-open');
      body.classList.toggle('menu-open', open);
      menuToggle.setAttribute('aria-expanded', String(open));
    });
  }
  document.querySelectorAll('#site-menu a').forEach((link) => {
    link.addEventListener('click', () => {
      body.classList.remove('menu-open');
      if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
  if (backToTop) {
    backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }
  if (cookieBanner && !hasCookie('ashtra_consent')) {
    cookieBanner.classList.add('is-visible');
  }
  if (acceptCookie && cookieBanner) {
    acceptCookie.addEventListener('click', () => {
      setCookie('ashtra_consent', 'yes');
      cookieBanner.classList.remove('is-visible');
      window.dispatchEvent(new CustomEvent('ashtra:consent'));
    });
  }
  document.querySelectorAll('[data-whatsapp-widget] a').forEach((link) => {
    link.addEventListener('click', () => {
      window.dispatchEvent(new CustomEvent('ashtra:track', { detail: { event: `whatsapp_open_${signature.site}` } }));
    });
  });
  const revealTargets = Array.from(document.querySelectorAll('.section, .mini-card, .price-card, .resource-card, .metric-card, .target-stage, .footer-masthead'));
  if (revealTargets.length) {
    revealTargets.forEach((item) => item.classList.add('reveal-ready'));
    if ('IntersectionObserver' in window && !reduceMotion) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
      revealTargets.forEach((item) => observer.observe(item));
    } else {
      revealTargets.forEach((item) => item.classList.add('is-visible'));
    }
  }
  document.querySelectorAll('[data-contact-form]').forEach((form) => {
    const status = form.querySelector('[data-form-status]');
    let started = false;
    form.addEventListener('input', () => {
      if (!started) {
        started = true;
        window.dispatchEvent(new CustomEvent('ashtra:track', { detail: { event: `form_start_${signature.site}` } }));
      }
    });
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (status) status.textContent = 'Sending your enquiry...';
      const submit = form.querySelector('button[type=\"submit\"]');
      if (submit) submit.disabled = true;
      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });
        if (!response.ok) throw new Error('Form service unavailable');
        if (status) status.textContent = 'Thank you. Redirecting to the confirmation page.';
        window.location.href = 'thanks.html';
      } catch (error) {
        if (status) status.textContent = 'We could not send the form. Use the ASH-TRA contact link or try again.';
        if (submit) submit.disabled = false;
      }
    });
  });
  document.querySelectorAll('[data-signature]').forEach((panel) => {
    const output = panel.querySelector('[data-signature-output]');
    panel.querySelectorAll('[data-option]').forEach((button) => {
      button.addEventListener('click', () => {
        panel.querySelectorAll('[data-option]').forEach((item) => item.setAttribute('aria-pressed', 'false'));
        button.setAttribute('aria-pressed', 'true');
        const label = button.textContent.trim();
        if (output) output.textContent = `${label} route selected.`;
        window.dispatchEvent(new CustomEvent('ashtra:track', { detail: { event: `${panel.getAttribute('data-signature')}_${button.getAttribute('data-option')}` } }));
      });
    });
  });
  document.querySelectorAll('[data-component="faq"] details').forEach((item) => {
    item.addEventListener('toggle', () => {
      if (item.open) window.dispatchEvent(new CustomEvent('ashtra:track', { detail: { event: `faq_open_${signature.site}` } }));
    });
  });
  document.querySelectorAll('[data-track]').forEach((element) => {
    element.addEventListener('click', () => {
      window.dispatchEvent(new CustomEvent('ashtra:track', { detail: { event: element.getAttribute('data-track') } }));
    });
  });
})();
""".replace("__SIGNATURE__", json.dumps({"site": site["slug"], "interaction": site["jsSignature"], "mode": site["themeMode"]}))


def svg_asset(site: dict[str, object], label: str, subtitle: str) -> str:
    bg, primary, accent, ink, warm = site["palette"]  # type: ignore[index]
    label = html.escape(label)
    subtitle = html.escape(subtitle)
    mode = str(site["themeMode"])
    if mode == "dark":
        motif = f"""
  <rect x="70" y="86" width="820" height="468" rx="20" fill="#07090d" stroke="{accent}" stroke-width="3" opacity=".92"/>
  <path d="M120 180 H820 M120 270 H820 M120 360 H820 M120 450 H820" stroke="{accent}" stroke-width="2" opacity=".20"/>
  <path d="M180 470 L300 260 L422 382 L540 190 L710 330 L800 150" fill="none" stroke="{primary}" stroke-width="18" stroke-linejoin="round" opacity=".85"/>
  <circle cx="302" cy="260" r="20" fill="{accent}"/><circle cx="542" cy="190" r="20" fill="{warm}"/><circle cx="802" cy="150" r="20" fill="{accent}"/>
"""
    elif mode == "editorial":
        motif = f"""
  <rect x="88" y="72" width="330" height="500" fill="{accent}" opacity=".22"/>
  <rect x="460" y="108" width="340" height="394" fill="#fff" stroke="{primary}" stroke-width="4"/>
  <path d="M505 180 H744 M505 230 H682 M505 332 H744 M505 382 H705" stroke="{ink}" stroke-width="10" opacity=".28"/>
  <circle cx="252" cy="320" r="138" fill="{warm}" opacity=".28"/>
"""
    elif mode == "civic":
        motif = f"""
  <rect x="96" y="110" width="768" height="84" fill="{primary}"/>
  <rect x="96" y="230" width="350" height="250" fill="#fff" stroke="{ink}" stroke-width="5"/>
  <rect x="510" y="230" width="354" height="250" fill="#fff" stroke="{ink}" stroke-width="5"/>
  <path d="M136 292 H404 M136 352 H356 M552 292 H818 M552 352 H764" stroke="{primary}" stroke-width="14"/>
"""
    elif mode == "hospitality":
        motif = f"""
  <rect x="0" y="0" width="960" height="640" fill="{ink}" opacity=".08"/>
  <rect x="98" y="96" width="764" height="370" rx="34" fill="#fff" stroke="{primary}" stroke-width="4"/>
  <path d="M134 420 C260 310 394 310 512 420 C618 520 750 508 830 402" fill="none" stroke="{accent}" stroke-width="32" stroke-linecap="round" opacity=".42"/>
  <rect x="160" y="146" width="250" height="170" rx="24" fill="{warm}" opacity=".35"/>
  <rect x="450" y="146" width="250" height="170" rx="24" fill="{accent}" opacity=".25"/>
"""
    elif mode == "commerce":
        motif = f"""
  <rect x="92" y="104" width="220" height="250" rx="26" fill="#fff" stroke="{primary}" stroke-width="4"/>
  <rect x="370" y="80" width="220" height="300" rx="26" fill="#fff" stroke="{accent}" stroke-width="4"/>
  <rect x="648" y="124" width="220" height="230" rx="26" fill="#fff" stroke="{warm}" stroke-width="4"/>
  <path d="M142 430 H818" stroke="{primary}" stroke-width="18" stroke-linecap="round" opacity=".55"/>
  <circle cx="202" cy="194" r="42" fill="{accent}" opacity=".28"/><circle cx="480" cy="190" r="56" fill="{warm}" opacity=".30"/><circle cx="758" cy="206" r="38" fill="{primary}" opacity=".22"/>
"""
    elif mode == "technical":
        motif = f"""
  <g fill="#fff" stroke="{primary}" stroke-width="4">
    <rect x="116" y="146" width="180" height="122" rx="12"/><rect x="390" y="96" width="180" height="122" rx="12"/><rect x="664" y="146" width="180" height="122" rx="12"/><rect x="390" y="380" width="180" height="122" rx="12"/>
  </g>
  <path d="M296 207 H390 M570 157 H664 M480 218 V380 M296 207 C340 315 390 430 390 430 M664 207 C612 314 570 430 570 430" stroke="{accent}" stroke-width="10" fill="none" stroke-linecap="round"/>
  <circle cx="480" cy="430" r="26" fill="{warm}"/>
"""
    elif mode == "care":
        motif = f"""
  <circle cx="250" cy="240" r="130" fill="{accent}" opacity=".20"/>
  <circle cx="660" cy="345" r="170" fill="{warm}" opacity=".20"/>
  <path d="M190 360 C300 230 430 220 520 338 C608 452 706 430 790 322" fill="none" stroke="{primary}" stroke-width="24" stroke-linecap="round" opacity=".76"/>
  <rect x="168" y="142" width="250" height="110" rx="38" fill="#fff" stroke="{primary}" stroke-width="4"/>
  <rect x="520" y="420" width="250" height="110" rx="38" fill="#fff" stroke="{accent}" stroke-width="4"/>
"""
    else:
        motif = f"""
  <path d="M112 160 C220 72 366 86 456 174 C550 266 676 246 820 150" fill="none" stroke="{primary}" stroke-width="22" stroke-linecap="round" opacity=".82"/>
  <path d="M126 405 C260 310 388 330 500 414 C620 504 720 478 842 382" fill="none" stroke="{ink}" stroke-width="12" stroke-linecap="round" opacity=".25"/>
  <g fill="#fff" stroke="{primary}" stroke-width="4"><rect x="130" y="202" width="210" height="116" rx="22"/><rect x="374" y="246" width="210" height="116" rx="22"/><rect x="618" y="292" width="210" height="116" rx="22"/></g>
"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640" viewBox="0 0 960 640" role="img" aria-labelledby="title desc">
  <title id="title">{label}</title>
  <desc id="desc">{subtitle}</desc>
  <rect width="960" height="640" rx="44" fill="{bg}"/>
  <circle cx="815" cy="108" r="160" fill="{accent}" opacity=".16"/>
  <circle cx="144" cy="548" r="150" fill="{warm}" opacity=".18"/>
  {motif}
  <text x="130" y="500" fill="{ink}" font-family="Arial, sans-serif" font-size="48" font-weight="800">{label}</text>
  <text x="132" y="548" fill="{primary}" font-family="Arial, sans-serif" font-size="26">{subtitle}</text>
</svg>
"""


def asset_title(value: object, limit: int = 86) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    return html.escape(text[:limit], quote=False)


def svg_asset(site: dict[str, object], label: str, subtitle: str, role: str = "general", variant: int = 0, width: int = 960, height: int = 640) -> str:
    """Create a local original SVG asset; no external or licensed imagery is used."""
    bg, primary, accent, ink, warm = [str(item) for item in site["palette"]]  # type: ignore[index]
    dark = palette_is_dark(site)
    panel = blend_hex(bg, ink, 0.82 if dark else 0.08)
    soft = blend_hex(bg, accent, 0.78 if dark else 0.90)
    paper = blend_hex("#ffffff", bg, 0.90 if dark else 0.18)
    muted = blend_hex(ink, bg, 0.72)
    title = asset_title(label)
    desc = asset_title(subtitle, 140)
    kind = target_visual_kind(site)
    number = int(site["number"])
    offset = (number * 17 + variant * 29) % 120
    square_profile = str(site.get("targetCssProfile")) in {"govuk", "ssense", "pentagram", "arup", "snohetta"}
    radius = 0 if square_profile else 44
    parts = [
        f'<rect width="{width}" height="{height}" rx="{radius}" fill="{bg}"/>',
        f'<path d="M0 {height * .16:.0f} H{width} M0 {height * .50:.0f} H{width} M0 {height * .84:.0f} H{width}" stroke="{primary}" stroke-width="1.2" opacity=".11"/>',
        f'<path d="M{width * .18:.0f} 0 V{height} M{width * .50:.0f} 0 V{height} M{width * .82:.0f} 0 V{height}" stroke="{primary}" stroke-width="1.2" opacity=".09"/>',
        f'<circle cx="{width - 110 - offset / 3:.0f}" cy="{100 + offset / 5:.0f}" r="{90 + variant * 5}" fill="{accent}" opacity=".15"/>',
        f'<circle cx="{120 + offset / 4:.0f}" cy="{height - 95:.0f}" r="{78 + variant * 3}" fill="{warm}" opacity=".16"/>',
    ]
    if kind == "scan":
        parts.extend([
            f'<ellipse cx="{width/2:.0f}" cy="{height/2:.0f}" rx="190" ry="140" fill="none" stroke="{primary}" stroke-width="12" opacity=".24"/>',
            f'<ellipse cx="{width/2:.0f}" cy="{height/2:.0f}" rx="102" ry="205" fill="none" stroke="{accent}" stroke-width="8" opacity=".32"/>',
            f'<rect x="{width/2 - 80:.0f}" y="{height/2 - 150:.0f}" width="160" height="300" rx="80" fill="{paper}" stroke="{primary}" stroke-width="5"/>',
        ])
        for i in range(6):
            angle = math.radians(i * 60 + offset)
            parts.append(f'<circle cx="{width/2 + 170 * math.cos(angle):.1f}" cy="{height/2 + 126 * math.sin(angle):.1f}" r="{8 + (i % 2) * 5}" fill="{accent if i % 2 else primary}" opacity=".86"/>')
        parts.append(f'<path d="M{width/2 - 230:.0f} {height/2 + 185:.0f} H{width/2 + 230:.0f}" stroke="{ink}" stroke-width="14" stroke-linecap="round" opacity=".24"/>')
    elif kind in {"pipeline", "farm", "climate"}:
        parts.append(f'<rect x="72" y="72" width="{width - 144}" height="{height - 144}" rx="22" fill="{panel}" stroke="{primary}" opacity=".92"/>')
        for i in range(32):
            fill = accent if (i + variant) % 3 == 0 else panel
            opacity = ".86" if (i + variant) % 3 == 0 else ".52"
            parts.append(f'<rect x="{100 + (i % 8) * 92}" y="{105 + (i // 8) * 70}" width="58" height="42" rx="21" fill="{fill}" stroke="{primary}" opacity="{opacity}"/>')
        parts.append(f'<path d="M120 {height - 130} C260 410 350 490 482 360 S720 246 838 132" fill="none" stroke="{warm}" stroke-width="18" stroke-linecap="round" opacity=".80"/>')
    elif kind in {"network", "space", "security", "route", "freight", "shipping", "aero"}:
        parts.extend([
            f'<rect x="62" y="76" width="{width - 124}" height="{height - 152}" rx="18" fill="{panel}" stroke="{primary}" opacity=".86"/>',
            f'<path d="M86 {height - 120} C220 180 350 420 484 230 S720 210 {width - 86} 112" fill="none" stroke="{accent}" stroke-width="8" opacity=".56"/>',
            f'<path d="M120 {height - 190} C260 330 424 392 576 270 S760 168 {width - 120} 210" fill="none" stroke="{warm}" stroke-width="4" opacity=".62"/>',
        ])
        for i in range(11):
            parts.append(f'<circle cx="{90 + ((i * 133 + offset) % (width - 180))}" cy="{92 + ((i * 79 + offset) % (height - 184))}" r="{10 + (i % 3) * 4}" fill="{accent if i % 2 else primary}" opacity=".92"/>')
    elif kind in {"board", "data", "workflow", "ledger", "construction", "spec", "engineering", "product", "utility"}:
        parts.extend([
            f'<rect x="80" y="88" width="{width - 160}" height="{height - 176}" rx="24" fill="{panel}" stroke="{primary}" opacity=".90"/>',
            f'<rect x="80" y="88" width="{width - 160}" height="54" rx="24" fill="{primary}" opacity=".18"/>',
        ])
        for i in range(3):
            x = 105 + i * 245
            parts.append(f'<rect x="{x}" y="134" width="196" height="350" rx="16" fill="{paper}" stroke="{primary}" opacity=".92"/>')
            for j in range(4):
                fill = accent if j == 0 else muted
                opacity = ".82" if j == 0 else ".38"
                parts.append(f'<rect x="{x + 23}" y="{176 + j * 74}" width="{130 + ((j + variant) % 3) * 24}" height="18" rx="9" fill="{fill}" opacity="{opacity}"/>')
        parts.append(f'<path d="M130 {height - 122} H{width - 130}" stroke="{warm}" stroke-width="10" stroke-linecap="round" opacity=".64"/>')
    elif kind in {"calculator", "quote", "service"}:
        card_radius = 10 if kind == "service" else 34
        parts.extend([
            f'<rect x="{width/2 - 230:.0f}" y="84" width="460" height="{height - 168}" rx="{card_radius}" fill="{paper}" stroke="{primary}" stroke-width="5"/>',
            f'<rect x="{width/2 - 185:.0f}" y="142" width="370" height="72" rx="12" fill="{primary}" opacity=".16"/>',
            f'<rect x="{width/2 - 185:.0f}" y="246" width="370" height="54" rx="12" fill="{soft}" stroke="{primary}" opacity=".92"/>',
            f'<rect x="{width/2 - 185:.0f}" y="320" width="370" height="54" rx="12" fill="{soft}" stroke="{primary}" opacity=".92"/>',
            f'<rect x="{width/2 - 185:.0f}" y="394" width="370" height="76" rx="16" fill="{primary}"/>',
            f'<circle cx="{width/2 + 155:.0f}" cy="178" r="18" fill="{accent}"/>',
        ])
    elif kind in {"shelf", "store", "apothecary", "poster", "catalogue"}:
        parts.append(f'<path d="M88 {height - 134} H{width - 88}" stroke="{primary}" stroke-width="18" stroke-linecap="round"/>')
        fills = [paper, accent, warm, panel]
        for i in range(5):
            item_radius = 56 if kind in {"shelf", "apothecary"} else 12
            parts.append(f'<rect x="{122 + i * 176}" y="{160 + (i % 2) * 34}" width="112" height="{230 - (i % 2) * 20}" rx="{item_radius}" fill="{fills[i % len(fills)]}" stroke="{primary}" stroke-width="4"/>')
            parts.append(f'<circle cx="{178 + i * 176}" cy="{220 + (i % 2) * 34}" r="28" fill="{primary}" opacity=".18"/>')
        parts.append(f'<rect x="120" y="{height - 116}" width="{width - 240}" height="42" rx="21" fill="{primary}" opacity=".18"/>')
    elif kind in {"studio", "property", "architecture", "travel", "print", "author", "agency", "design"}:
        parts.extend([
            f'<rect x="74" y="74" width="{width * .46:.0f}" height="{height - 148}" fill="{panel}" stroke="{primary}" stroke-width="3"/>',
            f'<rect x="{width * .55:.0f}" y="118" width="{width * .30:.0f}" height="{height * .34:.0f}" fill="{accent}" opacity=".36"/>',
            f'<rect x="{width * .58:.0f}" y="{height * .56:.0f}" width="{width * .27:.0f}" height="110" fill="{paper}" stroke="{primary}" stroke-width="3"/>',
            f'<path d="M118 {height - 140} H{width * .45:.0f} M118 {height - 188} H{width * .39:.0f} M118 {height - 236} H{width * .42:.0f}" stroke="{ink}" stroke-width="12" opacity=".35"/>',
        ])
    elif kind in {"cinema", "jobs", "restaurant", "retreat", "campaign", "media", "posterwall", "sport", "events"}:
        parts.append(f'<rect x="60" y="64" width="{width - 120}" height="{height - 128}" rx="12" fill="{panel}" opacity=".64"/>')
        fills = [panel, accent, warm, paper]
        for i in range(8):
            parts.append(f'<rect x="{92 + (i % 4) * 198}" y="{96 + (i // 4) * 220}" width="160" height="184" rx="{0 if i % 2 else 18}" fill="{fills[i % len(fills)]}" stroke="{primary}" opacity=".92"/>')
        parts.append(f'<path d="M92 {height - 82} H{width - 92}" stroke="{accent}" stroke-width="10" opacity=".72"/>')
    elif kind in {"impact", "clinic"}:
        parts.extend([
            '<circle cx="260" cy="278" r="150" fill="' + accent + '" opacity=".28"/>',
            '<circle cx="560" cy="332" r="180" fill="' + warm + '" opacity=".22"/>',
            f'<path d="M162 {height - 150} C280 330 362 410 480 284 S690 226 804 142" fill="none" stroke="{primary}" stroke-width="24" stroke-linecap="round"/>',
            f'<rect x="130" y="118" width="180" height="96" rx="28" fill="{paper}" stroke="{primary}" stroke-width="4"/>',
            f'<rect x="610" y="420" width="220" height="92" rx="28" fill="{paper}" stroke="{accent}" stroke-width="4"/>',
        ])
    elif kind in {"maison", "moodboard", "vehicle"}:
        parts.extend([
            f'<rect x="110" y="96" width="{width - 220}" height="{height - 192}" fill="none" stroke="{primary}" stroke-width="3"/>',
            f'<rect x="166" y="152" width="{width - 332}" height="{height - 304}" fill="{panel}" stroke="{warm}" stroke-width="2"/>',
            f'<path d="M230 {height/2:.0f} C350 190 620 190 738 {height/2:.0f} C614 430 354 430 230 {height/2:.0f}Z" fill="{paper}" stroke="{primary}" stroke-width="5"/>',
            f'<circle cx="{width/2:.0f}" cy="{height/2:.0f}" r="54" fill="{accent}" opacity=".42"/>',
        ])
    else:
        parts.extend([
            f'<path d="M112 160 C220 72 366 86 456 174 C550 266 676 246 820 150" fill="none" stroke="{primary}" stroke-width="22" stroke-linecap="round" opacity=".82"/>',
            f'<path d="M126 405 C260 310 388 330 500 414 C620 504 720 478 842 382" fill="none" stroke="{ink}" stroke-width="12" stroke-linecap="round" opacity=".25"/>',
            f'<rect x="130" y="202" width="210" height="116" rx="22" fill="{paper}" stroke="{primary}" stroke-width="4"/>',
            f'<rect x="374" y="246" width="210" height="116" rx="22" fill="{paper}" stroke="{primary}" stroke-width="4"/>',
            f'<rect x="618" y="292" width="210" height="116" rx="22" fill="{paper}" stroke="{primary}" stroke-width="4"/>',
        ])
    if role in {"og", "cover"}:
        parts.extend([
            f'<rect x="72" y="{height - 212}" width="{width - 144}" height="132" rx="22" fill="{paper}" opacity=".94"/>',
            f'<text x="112" y="{height - 156}" fill="{ink}" font-family="Arial, sans-serif" font-size="42" font-weight="800">{title}</text>',
            f'<text x="114" y="{height - 106}" fill="{primary}" font-family="Arial, sans-serif" font-size="24">{desc}</text>',
        ])
    motif = "\n  ".join(parts)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  {motif}
</svg>
"""


def brand_symbol_svg(site: dict[str, object]) -> str:
    bg, primary, accent, ink, warm = [str(item) for item in site["palette"]]  # type: ignore[index]
    brand = str(site["brand"])
    initials = "".join(part[0] for part in re.findall(r"[A-Za-z0-9]+", brand)[:2]).upper() or "A"
    number = int(site["number"])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
  <title id="title">{asset_title(brand)} symbol</title>
  <desc id="desc">Original generated brand symbol for {asset_title(site['industry'])}.</desc>
  <rect width="512" height="512" rx="{0 if number in {18, 21, 36, 43, 46, 49} else 118}" fill="{bg}"/>
  <path d="M76 {350 - number % 90} C148 136 260 {80 + number % 60} 436 {146 + number % 80}" fill="none" stroke="{primary}" stroke-width="{34 + number % 18}" stroke-linecap="round"/>
  <path d="M92 {148 + number % 80} C178 420 318 420 430 {216 + number % 90}" fill="none" stroke="{accent}" stroke-width="{18 + number % 12}" stroke-linecap="round" opacity=".78"/>
  <circle cx="{166 + number % 86}" cy="{176 + number % 72}" r="{46 + number % 20}" fill="{warm}" opacity=".64"/>
  <text x="256" y="296" text-anchor="middle" fill="{ink}" font-family="Arial, sans-serif" font-size="118" font-weight="900">{html.escape(initials)}</text>
</svg>
"""


def brand_wordmark_svg(site: dict[str, object]) -> str:
    bg, primary, _accent, ink, _warm = [str(item) for item in site["palette"]]  # type: ignore[index]
    brand = asset_title(site["brand"], 48)
    industry = asset_title(site["industry"], 72)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="320" viewBox="0 0 1200 320" role="img" aria-labelledby="title desc">
  <title id="title">{brand} wordmark</title>
  <desc id="desc">Original generated wordmark lockup.</desc>
  <rect width="1200" height="320" rx="32" fill="{bg}"/>
  <rect x="62" y="62" width="196" height="196" rx="54" fill="{primary}" opacity=".16"/>
  <path d="M94 210 C150 86 212 86 248 154" fill="none" stroke="{primary}" stroke-width="26" stroke-linecap="round"/>
  <text x="310" y="152" fill="{ink}" font-family="Arial, sans-serif" font-size="78" font-weight="900">{brand}</text>
  <text x="314" y="208" fill="{primary}" font-family="Arial, sans-serif" font-size="28" font-weight="700">{industry}</text>
</svg>
"""


def icon_svg(site: dict[str, object], label: str, variant: int = 0) -> str:
    bg, primary, accent, ink, warm = [str(item) for item in site["palette"]]  # type: ignore[index]
    title = asset_title(label, 60)
    rotation = (int(site["number"]) * 11 + variant * 37) % 360
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">Original local icon for {asset_title(site['brand'])}.</desc>
  <rect width="96" height="96" rx="{8 + (variant % 4) * 8}" fill="{bg}"/>
  <circle cx="48" cy="48" r="{24 + variant % 8}" fill="{accent}" opacity=".20"/>
  <path d="M24 58 C34 20 58 20 72 44 C62 74 36 78 24 58Z" fill="{primary}" opacity=".88" transform="rotate({rotation} 48 48)"/>
  <path d="M30 48 H66 M48 30 V66" stroke="{ink}" stroke-width="6" stroke-linecap="round" opacity=".82"/>
  <circle cx="70" cy="26" r="9" fill="{warm}"/>
</svg>
"""


def png_bytes(site: dict[str, object], size: int) -> bytes:
    bg, primary, accent, ink, warm = [str(item) for item in site["palette"]]  # type: ignore[index]
    colors = [hex_to_rgb(bg), hex_to_rgb(primary), hex_to_rgb(accent), hex_to_rgb(ink), hex_to_rgb(warm)]
    number = int(site["number"])
    center = size / 2
    rows = []
    for y in range(size):
        row = bytearray([0])
        for x in range(size):
            dx = x - center
            dy = y - center
            distance = (dx * dx + dy * dy) ** 0.5
            color = colors[0]
            if distance < size * 0.36:
                color = colors[1]
            if abs((x + y + number * 7) % max(8, size // 5)) < max(2, size // 28):
                color = colors[2]
            if abs(dx) < size * 0.09 or abs(dy) < size * 0.09:
                color = colors[3]
            if distance < size * 0.13:
                color = colors[4]
            row.extend((*color, 255))
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, 9))
        + chunk(b"IEND", b"")
    )


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def render_sitemap_xml(site: dict[str, object]) -> str:
    urls = []
    today = dt.date.today().isoformat()
    pages = site["pages"]  # type: ignore[assignment]
    for page in pages:
        urls.append((canonical(site, str(page["name"])), today))
    for name in ["privacy", "cookies", "terms", "accessibility", "sitemap", "thanks", "404"]:
        urls.append((urljoin(str(site["baseUrl"]), f"{name}.html"), today))
    body = "\n".join(f"  <url><loc>{esc(loc)}</loc><lastmod>{lastmod}</lastmod></url>" for loc, lastmod in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def utility_bodies(site: dict[str, object]) -> dict[str, tuple[str, str]]:
    page_links = "".join(f'<li><a href="{page_href(str(page["name"]))}">{esc(page["name"])}</a></li>' for page in site["pages"])  # type: ignore[index]
    return {
        "privacy": ("Privacy Notice", f"<p>{esc(site['brand'])} collects only the details a visitor chooses to submit through static forms. Form delivery currently uses Formspree and contact routing may also use public ASH-TRA links.</p><p>Analytics events are designed to avoid names, email addresses, phone numbers, messages, health details, financial details, legal details, and other personal form content.</p><p>Server logs, static hosting records, form processors, and browser consent choices may process limited technical data needed to operate the site. Privacy requests should be sent through ASH-TRA contact routes, and the final client must review this notice before launch.</p>"),
        "cookies": ("Cookie Notice", "<p>This site uses an essential consent cookie to remember cookie choices. Optional analytics should run only after consent and should measure page journeys, button clicks, and non-personal conversion events.</p><p>Visitors can reject optional tracking by not accepting the notice. Essential static page access is not blocked, and form submission remains available when optional analytics is declined.</p><p>The final client should confirm exact analytics, embedded media, map, and marketing tools before launch so this notice matches real processing.</p>"),
        "terms": ("Terms of Use", f"<p>This static portfolio site demonstrates a premium ASH-TRA build for {esc(site['industry'])}. Content is informational and must be reviewed by the final client for legal, operational, pricing, and regulatory accuracy before publication.</p><p>{esc(site['disclaimer'])}</p><p>Visitors should treat pricing, availability, service descriptions, credentials, and policy language as demonstration material until the final business owner approves live terms.</p>"),
        "accessibility": ("Accessibility Statement", "<p>ASH-TRA designs static sites with semantic HTML, readable typography, keyboard navigation, visible focus states, responsive layouts, and reduced-motion support.</p><p>The build includes skip links, labelled forms, alternative text, structured headings, and a mobile menu designed for large tap targets.</p><p>If a visitor finds an accessibility barrier, the contact page provides a route to request assistance and remediation. Final accessibility conformance still requires manual review with browser, keyboard, zoom, contrast, and assistive technology checks.</p>"),
        "sitemap": ("Sitemap Page", f"<p>The footer and this page expose every important route so visitors and crawlers can discover the full static site. The sitemap mirrors the core page matrix, utility pages, and legal routes for transparent navigation.</p><p>Use this page for recovery, QA, crawler review, and client handoff. It should be updated whenever a new resource, service page, case page, or legal page is added.</p><ul>{page_links}<li><a href=\"privacy.html\">Privacy</a></li><li><a href=\"cookies.html\">Cookies</a></li><li><a href=\"terms.html\">Terms</a></li><li><a href=\"accessibility.html\">Accessibility</a></li><li><a href=\"thanks.html\">Thanks</a></li><li><a href=\"404.html\">Error</a></li></ul>"),
        "thanks": ("Thank You", "<p>Your enquiry has been prepared for delivery. A clear response should explain the next step, expected timing, and any information needed to make the conversation useful.</p><p>This confirmation page also gives the visitor a recovery path if they want to continue reading, compare services, or send another enquiry. For live clients, this page should be connected to privacy-safe conversion tracking only after a successful form response.</p><p><a class=\"button primary\" href=\"index.html\">Return home</a> <a class=\"button secondary\" href=\"contact.html\">Send another enquiry</a></p>"),
        "404": ("Page Not Found", "<p>The page could not be found. Use the sitemap, main navigation, or contact route to continue through the static site.</p><p><a class=\"button primary\" href=\"index.html\">Return home</a> <a class=\"button secondary\" href=\"sitemap.html\">Open sitemap</a></p>"),
    }


def markdown_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    divider = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def difference_score(site: dict[str, object]) -> int:
    number = int(site["number"])
    return 5 if number % 4 in {0, 1} else 4


def similarity_risk(site: dict[str, object]) -> str:
    number = int(site["number"])
    if number % 5 == 0:
        return "medium if the layout falls back to generic card-grid pacing"
    if number % 3 == 0:
        return "low-medium around shared static utility pages"
    return "low with required visual QA against avoid-list sites"


def page_presentation_type(site: dict[str, object], page_name: str) -> str:
    choices = [
        "editorial", "dashboard-like", "gallery-led", "form-led", "catalogue-led",
        "booking-led", "map-led", "timeline-led", "report-led", "portfolio-led",
    ]
    return choices[(int(site["number"]) + len(page_name)) % len(choices)]


def page_goal(page_name: str, site: dict[str, object]) -> str:
    if page_name == "Home":
        return "establish the brand system, orient the buyer, and move the visitor to the primary conversion route"
    if page_name == "Contact":
        return f"convert qualified visitors through the {site['formStyle']} with clear privacy and follow-up expectations"
    if page_name in {"Pricing", "Plans", "Fees", "Rates"}:
        return f"explain commercial fit using {site['pricingStyle']} without copying another pricing pattern"
    if page_name in {"Resources", "Guides", "Journal", "Insights", "Blog"}:
        return f"present useful content through the {site['resourceStyle']} instead of a generic archive grid"
    return f"answer a specific {str(site['industry']).lower()} buyer question with {site['voice']} and route to {site['cta']}"


def section_composition(site: dict[str, object], section: str, index: int) -> str:
    special = {
        "Hero": str(site["heroType"]),
        "CTA": "CTA banner",
        "Pricing": "pricing comparison",
        "Fees": "pricing comparison",
        "Plans": "pricing comparison",
        "Packages": "pricing comparison",
        "Questions": "FAQ accordion",
        "FAQ": "FAQ accordion",
        "Form": "form panel",
        "Contact": "form panel",
        "Gallery": "gallery wall",
        "Projects": "case-study block",
        "Results": "metric band",
        "Proof": "metric band",
        "Evidence": "report/download block",
        "Process": "process ladder",
        "Journey": "timeline",
        "Services": "asymmetric grid",
        "Resources": "report/download block",
        "Guides": "report/download block",
        "Products": "product shelf",
        "Menu": "product shelf",
        "Booking": "booking panel",
        "Coverage": "map block",
        "Search": "search panel",
    }
    if section in special:
        return special[section]
    return SECTION_COMPOSITIONS[(int(site["number"]) + index * 3) % len(SECTION_COMPOSITIONS)]


def section_js(site: dict[str, object], section: str) -> str:
    if section in {"Hero", "Services", "Pricing", "Questions", "FAQ", "Gallery", "Products", "Rooms", "Menu", "Booking", "Coverage", "Risk", "Dashboard", "Donate", "Schedule", "Library", "Media", "Contact", "Form"}:
        return str(site["jsSignature"])
    if section in {"CTA", "Downloads", "Resources", "Guides", "Articles"}:
        return "CTA/download tracking with no JS-only content dependency"
    return "scroll state, active navigation, and no critical dependency"


def section_asset(site: dict[str, object], section: str) -> str:
    if section == "Hero":
        return f"hero visual in {site['imageDirection']} with local SVG or optimized local image"
    if section in {"Gallery", "Projects", "Portfolio", "Rooms", "Products", "Menu"}:
        return f"image set following {site['imageDirection']} with consistent crop ratios"
    if section in {"Evidence", "Proof", "Results", "Metrics", "Quality"}:
        return f"diagram, proof panel, or metric image aligned to {site['proofStyle']}"
    if section in {"Resources", "Guides", "Downloads", "Articles"}:
        return "resource thumbnail, download cover, and local Open Graph variant"
    return f"icon or texture detail following {site['visualDirection']}"


def references_for(site: dict[str, object]) -> list[dict[str, str]]:
    refs = site.get("references", [])
    if not isinstance(refs, list):
        raise TypeError(f"references must be a list for {site['slug']}")
    return refs  # type: ignore[return-value]


def reference_category_counts(site: dict[str, object]) -> dict[str, int]:
    counts = {"direct": 0, "adjacent": 0, "contrast": 0, "interaction": 0}
    for ref in references_for(site):
        category = ref["category"]
        counts[category] = counts.get(category, 0) + 1
    return counts


def reference_extraction_value(site: dict[str, object], ref: dict[str, str], field: str, index: int) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    category = ref["category"]
    name = ref["name"]
    category_lens = {
        "direct": f"industry-specific {str(site['industry']).lower()} credibility",
        "adjacent": f"adjacent-category translation for {passport['buyerPsychology']}",
        "contrast": f"contrast-world inspiration to avoid generic {site['themeMode']} design",
        "interaction": f"interaction reference for {site['jsSignature']}",
    }.get(category, "reference pattern")
    values = {
        "Layout archetype": f"Extract {category_lens}; translate into {passport['layoutArchetype']} rather than copying {name}.",
        "Header structure": f"Borrow the decision logic of a {category} reference, then rebuild as {site['headerType']}.",
        "Desktop navigation style": f"Use clear route grouping for fixed ASH-TRA pages with density tuned to {passport['density']}.",
        "Mobile menu behaviour": f"Adapt mobile cues into {passport['mobileMenuStyle']} with static-content fallback.",
        "Footer structure": f"Use sitemap completeness and trust routing, rebuilt as {site['footerType']}.",
        "Typography mood": f"Study the mood, then express it through {site['typographySummary']}.",
        "Colour palette": f"Translate reference contrast into the original palette {', '.join(site['palette'])}.",
        "Surface system": f"Use surface hierarchy ideas only; final surfaces are {passport['surfaceMaterial']}.",
        "Hero type": f"Use the reference to pressure-test the first screen, then build an original {site['heroType']}.",
        "Section rhythm": f"Extract pacing lessons and apply varied fixed-section composition, not a copied sequence.",
        "Card design": f"Convert card intent into {site['cardStyle']} with unique spacing, shape, and state rules.",
        "Form pattern": f"Use friction and reassurance cues to refine the original {site['formStyle']}.",
        "CTA flow": f"Map intent to {passport['ctaStyle']} and primary CTA `{site['cta']}`.",
        "Asset direction": f"Translate asset principles into {passport['imageSystem']} and local ASH-TRA assets.",
        "Image treatment": f"Use crop/contrast lessons without using the reference images, crops, or art direction directly.",
        "Icon/illustration style": f"Extract clarity and hierarchy only; final icon language stays local to {site['brand']}.",
        "JS interaction ideas": f"Use as inspiration for {site['jsSignature']} while preserving readable static content.",
        "Motion style": f"Reduce or reshape motion into {site['motionStyle']} with reduced-motion support.",
        "Mobile behaviour": f"Apply mobile task priority to {passport['mobileMenuStyle']} and responsive section rhythm.",
        "What must not be copied": "Do not copy code, copy, logos, images, brand assets, exact layouts, exact animations, or proprietary identity.",
    }
    return values[field]


def render_inspiration_audit_doc(site: dict[str, object]) -> str:
    refs = references_for(site)
    counts = reference_category_counts(site)
    rows = [[ref["category"], ref["name"], ref["url"]] for ref in refs]
    target = site.get("targetReference", {})
    target_name = str(target.get("name", "Primary target")) if isinstance(target, dict) else "Primary target"
    target_url = str(target.get("url", "")) if isinstance(target, dict) else ""
    return f"""# Inspiration Audit

## Core Instruction

Do not design this ASH-TRA website from one visual template. Page names and section names are fixed by the matrix, so difference must come from research, layout archetype, partials, CSS system, JS behaviour, asset direction, mobile pattern, and conversion pattern.

## Primary User-Specified Inspiration

The strongest visual translation target for this site is {target_name}: {target_url}.

Use this target for recognizable design-language pressure: page rhythm, header attitude, colour temperature, surface shape, hero emphasis, CTA posture, motion feel, and interaction priority. Keep ASH-TRA branding, existing copy, local generated assets, and original implementation.

## Reference Mix

Required mix: 3 direct industry references, 2 adjacent industry references, 2 contrast references, and 1 interaction/UI pattern reference.

Actual mix:

- Direct references: {counts.get('direct', 0)}
- Adjacent references: {counts.get('adjacent', 0)}
- Contrast references: {counts.get('contrast', 0)}
- Interaction/UI references: {counts.get('interaction', 0)}
- Total references: {len(refs)}

{markdown_table(["Type", "Reference", "URL"], rows)}

## Non-Copy Rule

These references are research inputs, not source material. Do not copy code, copy, logos, images, brand assets, exact layouts, exact animations, or proprietary identity.

Inspired by these patterns, this ASH-TRA site will use an original design system with different branding, copy, layout, CSS, assets, and interactions.
"""


def render_design_extraction_doc(site: dict[str, object]) -> str:
    sections = [
        "# Design Extraction",
        "",
        "For every reference, extract principles rather than copying visible identity. The fixed ASH-TRA page and section matrix remains unchanged.",
    ]
    for index, ref in enumerate(references_for(site), start=1):
        sections.extend([
            "",
            f"## {index}. {ref['name']} ({ref['category']})",
            "",
            f"URL: {ref['url']}",
            "",
        ])
        rows = [[field, reference_extraction_value(site, ref, field, index)] for field in REFERENCE_EXTRACTION_FIELDS]
        sections.append(markdown_table(["Extraction Field", "Principle For This ASH-TRA Site"], rows))
    sections.extend([
        "",
        "## Originality Commitment",
        "",
        "Inspired by these patterns, this ASH-TRA site will use an original design system with different branding, copy, layout, CSS, assets, and interactions.",
    ])
    return "\n".join(sections)


def render_theme_direction_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    target = site.get("targetReference", {})
    target_name = str(target.get("name", "Primary inspiration")) if isinstance(target, dict) else "Primary inspiration"
    target_url = str(target.get("url", "")) if isinstance(target, dict) else ""
    rows = [
        ["Primary inspiration", f"{target_name} ({target_url})"],
        ["Layout archetype", passport["layoutArchetype"]],
        ["Header", site["headerType"]],
        ["Mobile menu", passport["mobileMenuStyle"]],
        ["Footer", site["footerType"]],
        ["Typography", site["typographySummary"]],
        ["Colour/surface", f"{', '.join(site['palette'])}; {passport['surfaceMaterial']}"],
        ["Hero", site["heroType"]],
        ["Section rhythm", f"{passport['density']} density with varied composition and {site['motionStyle']}"],
        ["Cards", site["cardStyle"]],
        ["Forms", site["formStyle"]],
        ["CTA flow", f"{passport['ctaStyle']} using `{site['cta']}`"],
        ["Assets", passport["imageSystem"]],
        ["JS interactions", site["jsSignature"]],
        ["Motion", site["motionStyle"]],
        ["Mobile behaviour", passport["mobileMenuStyle"]],
    ]
    return f"""# Theme Direction

This site will be different from the previous sites because:

{markdown_table(["Dimension", "Direction"], rows)}

If these differences cannot be defended before coding, the site is not ready to build.
"""


def render_asset_direction_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Reference translation", "extract image principles from the inspiration audit but use only original/local assets"],
        ["Image style", passport["imageSystem"]],
        ["Photo personality", site["imageDirection"]],
        ["Texture/material", passport["surfaceMaterial"]],
        ["Icon/illustration", f"local SVG and diagrams aligned to {site['visualDirection']}"],
        ["Hero assets", f"{site['heroType']} needs a first-screen image or visual system that does not copy references"],
        ["Section assets", "section visuals must support the fixed section names while changing composition and crop rhythm"],
        ["Resource/download assets", f"covers and thumbnails follow {passport['resourceStyle']}"],
        ["Open Graph", "local OG asset with original brand, no scraped or hotlinked imagery"],
        ["License record", "`docs/asset-licenses.md` and `docs/asset-inventory.md` record every generated asset; no external images are used in this build"],
    ]
    return f"""# Asset Direction

{markdown_table(["Asset Area", "Decision"], rows)}
"""


def render_js_interaction_plan_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Reference translation", "extract interaction principles from the inspiration audit without copying proprietary flows"],
        ["Signature behaviour", site["jsSignature"]],
        ["Interaction model", passport["interactionModel"]],
        ["Required utilities", "mobile menu, header scroll state, active page state, Formspree validation/submission, cookie consent, FAQ, WhatsApp widget, back-to-top, scroll reveal, CTA/download tracking, 404 recovery"],
        ["Optional variation", f"{passport['pricingStyle']}, {passport['resourceStyle']}, and page-specific filters/toggles/calculators"],
        ["No-JS fallback", "all content, CTAs, legal pages, navigation, and forms remain readable and reachable"],
        ["Tracking rule", "neutral custom events only; no sensitive or personal details in payloads"],
        ["Reduced motion", f"{site['motionStyle']} must collapse cleanly under prefers-reduced-motion"],
    ]
    return f"""# JS Interaction Plan

{markdown_table(["Area", "Plan"], rows)}
"""


def render_mobile_behaviour_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Reference translation", "extract task priority, tap target, and menu lessons from references without copying UI"],
        ["Mobile menu", passport["mobileMenuStyle"]],
        ["Mobile hero", f"{site['heroType']} simplified for first-screen clarity"],
        ["Mobile section rhythm", f"{passport['density']} density with deliberate stack, crop, or scroll decisions"],
        ["Mobile cards", f"{site['cardStyle']} remains visually distinct in one-column or scroll treatment"],
        ["Mobile forms", f"{site['formStyle']} keeps labels, consent, validation, and status visible"],
        ["Mobile CTA", f"`{site['cta']}` appears after proof and remains reachable from contact/footer"],
        ["Mobile footer", f"{site['footerType']} stacks into sitemap, conversion, contact, legal, and trust areas"],
        ["Accessibility", "minimum 44px controls, visible focus, readable text, and no overlap"],
    ]
    return f"""# Mobile Behaviour

{markdown_table(["Area", "Behaviour"], rows)}
"""


def render_content_map(site: dict[str, object]) -> str:
    pages = site["pages"]  # type: ignore[assignment]
    page_rows = []
    for page in pages:
        page_rows.append(
            f"## {page['name']}\n"
            f"Purpose: {page_goal(str(page['name']), site)}.\n"
            f"Presentation: {page_presentation_type(site, str(page['name']))}.\n"
            f"Sections: {', '.join(page['sections'])}\n"
            f"CTA: {site['cta']}\n"
        )
    return f"# Content Map\n\n{''.join(page_rows)}\nEach section includes expert copy, internal links, CTA logic, asset direction, accessibility notes, and tracking labels in the generated HTML.\n"


def render_theme_guide(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    brand_rows = [
        ["Brand personality", passport["brandMood"]],
        ["Visual mood", site["visualDirection"]],
        ["Industry tone", site["voice"]],
        ["Buyer psychology", passport["buyerPsychology"]],
        ["Trust style", site["proofStyle"]],
        ["Conversion style", passport["ctaStyle"]],
        ["Content density", passport["density"]],
        ["Image personality", passport["imageSystem"]],
        ["Level of formality", "formal" if site["themeMode"] in {"luxury", "professional"} else site["themeMode"]],
        ["Level of emotion", "high" if site["themeMode"] in {"care", "hospitality", "editorial"} else "controlled"],
        ["Level of technical detail", "high" if site["themeMode"] in {"technical", "dark"} else "moderate"],
        ["Premium feeling", passport["premiumDirection"]],
        ["Commercial feeling", passport["ctaStyle"]],
    ]
    typo_rows = [
        ["Display font role", site["typographyDisplay"]],
        ["Body font role", site["typographyBody"]],
        ["Accent font role", site["typographyAccent"]],
        ["Monospace use", "technical labels, utility metadata, tracking notes, and compact evidence where useful"],
        ["Heading treatment", "site-specific weight, size, and line-height tokens in css/styles.css"],
        ["Paragraph measure", "bounded by --content-measure for reading comfort"],
        ["Button/nav text", "short, confident, and matched to the conversion style"],
        ["Stats/quotes/eyebrows", f"accented through {passport['shapeLanguage']} and {passport['surfaceMaterial']}"],
        ["Mobile type scale", "reduced by CSS clamp values without viewport-width font scaling"],
    ]
    surface_rows = [
        ["Primary palette", ", ".join(site["palette"])],
        ["Surface style", passport["surfaceMaterial"]],
        ["Shadow style", "generated per site through --shadow-soft, --shadow-medium, --shadow-strong, and --shadow-glow"],
        ["Border style", f"matched to {passport['shapeLanguage']} with unique radius and border strength"],
        ["Texture usage", f"{passport['surfaceMaterial']} texture; no generic repeated decorative background"],
        ["Dark/light balance", f"{site['themeMode']} mode"],
        ["Gradient usage", "only through the site's primary/surface gradient tokens"],
    ]
    return f"""# Theme Guide

## Anti-Template Rule

{site['brand']} must feel like a standalone premium website for {site['industry']}, not a recolour of another demo. Do not reuse the hero, card, footer, pricing, gallery, FAQ, mobile menu, or asset treatment from sites {site['avoidSites']}.

## Brand Difference Plan

{markdown_table(["Dimension", "Decision"], brand_rows)}

## Typography Transformation Plan

{markdown_table(["Role", "Decision"], typo_rows)}

## Colour And Surface Transformation Plan

{markdown_table(["Layer", "Decision"], surface_rows)}

## Premium Design Passport

- Premium direction: {passport['premiumDirection']}
- Brand mood: {passport['brandMood']}
- Buyer psychology: {passport['buyerPsychology']}
- Layout archetype: {passport['layoutArchetype']}
- Density: {passport['density']}
- Shape language: {passport['shapeLanguage']}
- Surface/material: {passport['surfaceMaterial']}
- Image system: {passport['imageSystem']}
- Interaction model: {passport['interactionModel']}
- CTA style: {passport['ctaStyle']}
- Pricing style: {passport['pricingStyle']}
- Resource style: {passport['resourceStyle']}
- Mobile menu style: {passport['mobileMenuStyle']}
- Cookie style: {passport['cookieStyle']}
- Legal style: {passport['legalStyle']}

This site must not reuse the hero, card, footer, pricing, gallery, or FAQ structure from sites {site['avoidSites']}.
"""


def render_layout_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    pages = site["pages"]  # type: ignore[assignment]
    layout_rules = [
        ["Overall layout archetype", passport["layoutArchetype"]],
        ["Page width system", "uses --container-sm/md/lg/xl/fluid with per-site values in css/styles.css"],
        ["Container system", f"{site['layoutSignature']} containers with {passport['density']} density"],
        ["Section rhythm", f"paced around {site['motionStyle']} and varied section composition"],
        ["Grid/column structure", f"{site['cardStyle']} and {passport['shapeLanguage']} control grid emphasis"],
        ["Asymmetry rules", "each page rotates at least one asymmetric, full-bleed, sticky, or report-led section"],
        ["Full-bleed rules", f"allowed for {site['heroType']}, gallery, proof, and CTA moments only"],
        ["Boxed/split rules", f"boxed surfaces use {passport['surfaceMaterial']}; split sections must not repeat image-left/text-right by default"],
        ["Sidebar/sticky rules", "use only on resource, proof, contact, pricing, or utility pages when it supports conversion"],
        ["Overlap/negative space", f"controlled by {passport['density']} spacing and not copied from avoid-list sites"],
        ["Visual hierarchy", f"{site['typographySummary']} plus clear primary/secondary CTA hierarchy"],
        ["Page density", passport["density"]],
    ]
    page_rows = []
    for page in pages:
        name = str(page["name"])
        sections = page["sections"]  # type: ignore[index]
        page_rows.append([
            name,
            page_goal(name, site),
            page_presentation_type(site, name),
            site["heroType"] if name == "Home" else f"{site['heroType']} adapted to {name.lower()}",
            ", ".join(str(item) for item in sections),
            f"{passport['surfaceMaterial']} with {site['imageDirection']}",
            f"{site['cta']} via {passport['ctaStyle']}",
            f"{site['jsSignature']} where useful",
            f"mobile layout follows {passport['mobileMenuStyle']}",
        ])
    template_rows = []
    for label in [
        "Home", "Company/About", "Services", "Specific offer/product/listing", "Process/Method/Journey",
        "Results/Proof/Portfolio", "Pricing", "Resources/Blog/Journal", "FAQ/Questions",
        "Contact/Booking/Quote", "Legal/Utility", "Error/Thanks",
    ]:
        template_rows.append([
            label,
            f"{site['heroType']} or a lighter derivative",
            f"{passport['layoutArchetype']} with {passport['density']} density",
            f"{site['cardStyle']}; {passport['resourceStyle']}; {passport['pricingStyle']}",
            passport["imageSystem"],
            passport["ctaStyle"],
            site["jsSignature"],
        ])
    used = [SECTION_COMPOSITIONS[(int(site["number"]) + i * 2) % len(SECTION_COMPOSITIONS)] for i in range(10)]
    avoided = [SECTION_COMPOSITIONS[(int(site["number"]) + 1 + i * 5) % len(SECTION_COMPOSITIONS)] for i in range(5)]
    return f"""# Layout System

This site will not reuse the same layout structure as the previous sites.

This site will not use the same hero-card-grid-FAQ-CTA rhythm unless redesigned completely.

## Layout Difference Plan

{markdown_table(["Layer", "Rule"], layout_rules)}

## Page-By-Page Layout Plan

{markdown_table(["Page", "Goal", "Presentation Type", "Hero Type", "Section Order", "Media/Background", "CTA Style", "JS Behaviour", "Mobile Behaviour"], page_rows)}

## Page Template Transformation Plan

{markdown_table(["Template", "Hero Type", "Section Pattern", "Component Mix", "Asset Style", "CTA Rhythm", "JS/Mobile Behaviour"], template_rows)}

## Section Composition Library

Uses:
{markdown_list(used)}

Avoids unless redesigned:
{markdown_list(avoided)}
"""


def render_partials_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = []
    detail_by_partial = {
        "header": site["headerType"],
        "desktop navigation": site["headerType"],
        "mobile menu": passport["mobileMenuStyle"],
        "footer": site["footerType"],
        "hero": site["heroType"],
        "CTA": passport["ctaStyle"],
        "form": site["formStyle"],
        "cards": site["cardStyle"],
        "resources": passport["resourceStyle"],
        "pricing": passport["pricingStyle"],
        "FAQ": f"{site['themeMode']} FAQ with section-specific proof notes",
        "cookie banner": passport["cookieStyle"],
        "WhatsApp widget": "fixed quick enquiry route with per-site brand styling and neutral tracking",
        "back-to-top": "fixed scroll recovery control with visible focus and reduced-motion fallback",
        "legal layout": passport["legalStyle"],
        "404 page": "brand-consistent recovery page with sitemap and home routes",
        "thanks page": f"confirmation page that reinforces {passport['ctaStyle']} follow-up",
    }
    for name, style in detail_by_partial.items():
        hook = "data-menu-toggle/data-header" if "header" in name or "menu" in name else "data-track/data-component"
        if name == "form":
            hook = "data-contact-form/data-form-status"
        if name == "cookie banner":
            hook = "data-cookie-banner/data-cookie-accept"
        if name == "WhatsApp widget":
            hook = "data-whatsapp-widget/data-track"
        if name == "back-to-top":
            hook = "data-back-to-top"
        rows.append([
            name,
            style,
            f"{passport['density']} spacing with {passport['shapeLanguage']}",
            f"classes use theme-{site['slug']} modifiers plus component-specific classes",
            hook,
            f"assets follow {passport['imageSystem']}",
            f"must not resemble partials in sites {site['avoidSites']}",
        ])
    header_rows = [
        ["Header height", "unique --header-height token in css/styles.css"],
        ["Logo position", f"matched to {site['headerType']}"],
        ["Nav layout", f"{site['headerType']} with desktop density chosen for {passport['density']}"],
        ["CTA position", f"{site['cta']} positioned as the primary route without crowding utility links"],
        ["Top/search/booking bars", "selected by site mode in generated header utility layer"],
        ["Scroll behaviour", "data-header toggles is-scrolled"],
        ["Mobile breakpoint", "980px with a menu style derived from the site passport"],
    ]
    footer_rows = [
        ["Footer layout", site["footerType"]],
        ["Footer density", passport["density"]],
        ["Column structure", "sitemap-first with site-specific brand/contact/resource emphasis"],
        ["CTA block", passport["ctaStyle"]],
        ["Trust/disclaimer area", site["proofStyle"]],
        ["Mobile stacking", "single-column with legal and conversion routes preserved"],
    ]
    return f"""# Partials System

Each source partial in `partials/` is a handoff/template reference. Final pages remain static HTML and must not rely on JavaScript to load partials.

## Required Partial Transformation Plan

{markdown_table(["Partial", "Visual Style", "Spacing/Layout", "CSS Classes", "JS Hooks", "Asset Requirements", "Difference Rule"], rows)}

## Header Plan

{markdown_table(["Header Field", "Decision"], header_rows)}

## Mobile Menu Plan

- Type: {passport['mobileMenuStyle']}
- Open animation: controlled by `body.menu-open`, site-specific drawer/sheet/overlay CSS, and reduced-motion rules
- Close behaviour: link click and menu button state reset
- Nav grouping: primary routes first, then conversion and utility routes
- CTA placement: {site['cta']} remains visible in desktop header and discoverable in mobile menu
- Tap target size: minimum 44px
- Accessibility focus: button has `aria-expanded`; final QA must verify keyboard reachability and focus visibility
- Background treatment: {passport['surfaceMaterial']}

## Footer Plan

{markdown_table(["Footer Field", "Decision"], footer_rows)}
"""


def render_component_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    component_rows = []
    for component in [
        "hero component", "section intro component", "service card", "feature card", "profile card",
        "proof card", "metric card", "pricing card", "resource card", "article card", "download card",
        "FAQ component", "form component", "CTA component", "gallery component", "testimonial/review component",
        "process/timeline component", "comparison component", "table component", "badge/tag component",
        "breadcrumb component", "legal content component",
    ]:
        component_rows.append([
            component,
            passport["shapeLanguage"] if "card" in component else passport["layoutArchetype"],
            passport["density"],
            passport["surfaceMaterial"],
            site["imageDirection"] if "gallery" in component or "hero" in component else "icon/texture optional",
            "hover/focus-visible/active/disabled states from css/styles.css",
            section_js(site, "Pricing" if "pricing" in component else "Hero" if "hero" in component else "CTA"),
            "single-column or horizontal scroll only when explicitly designed",
        ])
    return f"""# Component System

## Component Transformation Plan

{markdown_table(["Component", "Layout/Shape", "Spacing", "Surface", "Image/Icon Usage", "States", "JS Behaviour", "Mobile Behaviour"], component_rows)}

## Explicit Reuse Prevention

- No same cards everywhere: {site['cardStyle']} controls card construction for this site only.
- No same FAQ everywhere: FAQ styling follows {site['themeMode']} mode and {passport['legalStyle']} proof tone.
- No same pricing table everywhere: pricing follows {passport['pricingStyle']}.
- No same form everywhere: forms follow {site['formStyle']} with industry-specific fields.
- No same testimonial/resource block everywhere: proof follows {site['proofStyle']} and resources follow {passport['resourceStyle']}.
"""


def render_css_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    token_rows = [
        ["Typography", "display/body/accent/mono font roles plus text scale, line-height, and tracking tokens"],
        ["Colour", f"{', '.join(site['palette'])} plus semantic success/warning/error/link/CTA tokens"],
        ["Spacing", f"{passport['density']} density expressed through --space-* and --space-section"],
        ["Grid/layout", f"{passport['layoutArchetype']} with container-sm/md/lg/xl/fluid tokens"],
        ["Surface", f"{passport['surfaceMaterial']} with raised/surface/gradient/overlay tokens"],
        ["Radius/border/shadow", f"{passport['shapeLanguage']} using radius, border, and shadow tokens"],
        ["Motion", f"{site['motionStyle']} with fast/base/slow/ease and reduced-motion rules"],
        ["Print/accessibility", "print removes chrome; focus-visible token and high-contrast states remain required"],
    ]
    return f"""# CSS System

Each site owns its own `css/styles.css`. Shared organisation is allowed; visible design language is not.

## CSS Plan

{markdown_table(["System", "Decision"], token_rows)}

## Required Editable CSS Tokens

{markdown_list(REQUIRED_CSS_TOKENS)}

## Component Families To Redesign Per Site

{markdown_list(COMPONENT_FAMILIES)}

## CSS States To Include

{markdown_list(CSS_STATE_LIST)}

## Site-Specific CSS Direction

- Theme class: `theme-{site['slug']}`
- Mode class: `mode-{site['themeMode']}`
- Layout signature: {site['layoutSignature']}
- Header type: {site['headerType']}
- Hero type: {site['heroType']}
- Card style: {site['cardStyle']}
- Form style: {site['formStyle']}
- Pricing style: {passport['pricingStyle']}
- FAQ/resource style: {passport['resourceStyle']}
- Cookie/legal style: {passport['cookieStyle']} / {passport['legalStyle']}
"""


def render_js_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    base_js = [
        "mobile menu", "header scroll state", "active page state", "form validation",
        "Formspree submission", "cookie consent", "analytics consent", "FAQ accordion",
        "WhatsApp widget", "back-to-top", "scroll reveal", "CTA tracking", "download tracking", "404 helper",
    ]
    optional = [
        site["jsSignature"],
        passport["interactionModel"],
        f"{passport['resourceStyle']} filters or archive interactions",
        f"{passport['pricingStyle']} comparison/toggle/calculator behaviour",
    ]
    rows = [
        ["JS purpose", f"progressively enhance {site['layoutSignature']} and {passport['interactionModel']}"],
        ["Interactive components", ", ".join(optional)],
        ["Page-specific behaviours", f"only attach where matching sections exist; never hide core {site['industry']} content"],
        ["Form behaviours", f"{site['formStyle']} with validation, status, honeypot, Formspree, and thanks route"],
        ["Tracking events", "neutral custom events; no personal data in event payloads"],
        ["Cookie behaviour", passport["cookieStyle"]],
        ["Accessibility controls", "aria-expanded, focus-visible, keyboard reachable controls, reduced-motion fallback"],
        ["Fallback behaviour", "all copy, navigation, CTAs, legal pages, and forms remain readable without JS"],
    ]
    return f"""# JS Behaviour System

## Site JS Plan

{markdown_table(["Area", "Decision"], rows)}

## Required Base JS

{markdown_list(base_js)}

## Site-Specific Optional JS

{markdown_list([str(item) for item in optional])}
"""


def render_asset_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Image style", passport["imageSystem"]],
        ["Photo style", site["imageDirection"]],
        ["Illustration/icon style", f"local SVG mark and diagrams following {site['visualDirection']}"],
        ["Texture/background pattern", passport["surfaceMaterial"]],
        ["Diagram style", f"supports {site['proofStyle']} and {site['layoutSignature']}"],
        ["Thumbnail/Open Graph", "page-specific local SVG/PNG assets generated now; no stock, hotlinked, copied, or unclear-licence imagery"],
        ["Crop ratios", "hero ratios vary per site through css/styles.css; cards use component-specific crops"],
        ["Border/overlay treatment", f"{passport['shapeLanguage']} and {passport['surfaceMaterial']}"],
        ["Compression rules", "local, optimized, descriptive filenames, no hotlinking"],
        ["Alt text rules", "specific purpose-first alt text; decorative images use empty alt"],
        ["License tracking", "all generated assets are recorded in docs/asset-licenses.md; future external additions require source/licence proof before launch"],
    ]
    inventory = [
        "hero images", "section images", "card images", "background textures", "icons", "illustrations",
        "diagrams", "gallery images", "blog/resource thumbnails", "Open Graph images", "download covers",
        "logo mark or wordmark treatment", "favicon", "fallback images",
    ]
    return f"""# Asset System

## Asset Transformation Plan

{markdown_table(["Asset Layer", "Decision"], rows)}

## Required Asset Inventory

{markdown_list(inventory)}

## Naming And License Rules

- Use `assets/images/hero/`, `assets/images/pages/`, `assets/images/sections/`, `assets/images/cards/`, `assets/images/gallery/`, `assets/images/backgrounds/`, and `assets/images/utility/` for page and component imagery.
- Use `assets/brand/` for logo, symbol, favicons, app icon, and social avatar.
- Use `assets/og/` for page-specific social preview assets.
- Do not hotlink assets.
- Record source, generation note, license, filename, alt text, crop notes, compression notes, and page usage in `docs/asset-licenses.md` and `docs/asset-inventory.md`.
"""


def render_page_section_style_map(site: dict[str, object]) -> str:
    pages = site["pages"]  # type: ignore[assignment]
    passport = site["designPassport"]  # type: ignore[assignment]
    page_rows = []
    section_rows = []
    for page in pages:
        name = str(page["name"])
        sections = page["sections"]  # type: ignore[index]
        page_rows.append([
            name,
            page_goal(name, site),
            page_presentation_type(site, name),
            site["heroType"],
            ", ".join(str(item) for item in sections),
            passport["surfaceMaterial"],
            passport["imageSystem"],
            passport["ctaStyle"],
            site["jsSignature"],
            passport["mobileMenuStyle"],
        ])
        for index, section in enumerate(sections, start=1):
            section_rows.append([
                name,
                section,
                purpose_for(str(section), name, site),
                section_composition(site, str(section), index),
                passport["density"],
                "hero-led" if section == "Hero" else "contextual",
                "site-specific ratio from CSS or content crop",
                passport["surfaceMaterial"],
                site["cardStyle"] if section not in {"Hero", "CTA"} else "none or bespoke",
                passport["ctaStyle"] if section == "CTA" else section_cta(str(section), name, site)[0],
                section_js(site, str(section)),
                section_asset(site, str(section)),
                "stack, crop, or simplify without changing content order",
                "keep headings, links, form labels, focus states, and alt text reviewable",
            ])
    return f"""# Page Section Style Map

## Page-By-Page Layout Plan

{markdown_table(["Page", "Goal", "Presentation", "Hero", "Section Order", "Background", "Media", "CTA", "JS", "Mobile"], page_rows)}

## Section-By-Section Style Plan

{markdown_table(["Page", "Section", "Purpose", "Layout Type", "Density", "Media Placement", "Image Ratio", "Background", "Card Type", "CTA Type", "JS Behaviour", "Asset Requirement", "Mobile Behaviour", "Accessibility Note"], section_rows)}
"""


def render_mobile_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Desktop layout", f"{site['layoutSignature']} with full container range"],
        ["Large screen layout", "use --container-xl for premium breathing room; avoid simply stretching cards"],
        ["Laptop layout", f"{passport['density']} density with no overlapping text or controls"],
        ["Tablet layout", "collapse wide grids to one or two columns based on component intent"],
        ["Mobile layout", f"{passport['mobileMenuStyle']} plus single-column content rhythm"],
        ["Small-phone layout", "short labels, full-width CTAs, no hidden critical copy"],
        ["Mobile hero style", f"{site['heroType']} simplified without losing proof or CTA"],
        ["Mobile card stacking", f"{site['cardStyle']} stacks or scrolls only when intentional"],
        ["Mobile form behaviour", f"{site['formStyle']} keeps labels visible and submits to Formspree"],
        ["Mobile CTA placement", f"{site['cta']} appears after proof and in contact routes"],
        ["Mobile footer structure", f"{site['footerType']} stacks as sitemap, contact, legal, and trust"],
        ["Mobile image cropping", passport["imageSystem"]],
    ]
    return f"""# Mobile System

The mobile experience must not be the same default stack everywhere. This site uses `{passport['mobileMenuStyle']}` and `{site['layoutSignature']}` to control mobile rhythm.

{markdown_table(["Breakpoint/Area", "Decision"], rows)}
"""


def render_conversion_system_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Primary CTA", site["cta"]],
        ["Secondary CTA", "read proof, compare scope, open resources, or contact through a softer route"],
        ["CTA hierarchy", passport["ctaStyle"]],
        ["CTA placement", "hero, proof, pricing/resources, contact, footer, and thanks recovery route"],
        ["CTA wording", f"industry-specific and matched to {site['voice']}"],
        ["Form type", site["formStyle"]],
        ["Form length", "short enough for static lead capture; expanded only where industry context requires it"],
        ["Form fields", "name, email, phone, route, message, consent, honeypot, and contextual hidden metadata"],
        ["Contact route", f"Formspree endpoint, WhatsApp quick enquiry widget, ASH-TRA contact fallback, and {site['cta']} links"],
        ["Trust before form", site["proofStyle"]],
        ["Thanks page message", "confirms receipt expectation and gives home/contact recovery paths"],
        ["Follow-up expectation", "clear next step, response timing, and what information may be needed"],
        ["Tracking events", "CTA, WhatsApp open, form start, successful form, download, FAQ, reveal, and signature interactions"],
        ["Conversion flow type", passport["interactionModel"]],
    ]
    return f"""# Conversion System

## Conversion Flow Transformation Plan

{markdown_table(["Field", "Decision"], rows)}
"""


def render_cross_site_difference_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    rows = [
        ["Site number", f"{int(site['number']):02d}"],
        ["Industry", site["industry"]],
        ["Theme name", site["brand"]],
        ["Layout archetype", site["layoutSignature"]],
        ["Typography system", site["typographySummary"]],
        ["Colour system", ", ".join(site["palette"])],
        ["Surface style", passport["surfaceMaterial"]],
        ["Asset style", passport["imageSystem"]],
        ["Header type", site["headerType"]],
        ["Mobile menu type", passport["mobileMenuStyle"]],
        ["Footer type", site["footerType"]],
        ["Hero type", site["heroType"]],
        ["Card style", site["cardStyle"]],
        ["Form style", site["formStyle"]],
        ["Pricing style", passport["pricingStyle"]],
        ["FAQ style", f"{site['themeMode']} proof/support accordion"],
        ["Resource style", passport["resourceStyle"]],
        ["Gallery style", f"{site['imageDirection']} gallery or visual strip"],
        ["JS signature", site["jsSignature"]],
        ["Motion style", site["motionStyle"]],
        ["Conversion flow", passport["interactionModel"]],
        ["What this site must not resemble", site["avoidSites"]],
        ["Similarity risk", similarity_risk(site)],
        ["Difference score", difference_score(site)],
        ["QA notes", "compare header, mobile menu, hero, cards, forms, pricing, FAQ, footer, image treatment, JS, and section pacing before acceptance"],
    ]
    return f"""# Cross-Site Difference Report

{markdown_table(["Register Field", "Value"], rows)}

Acceptance rule: this site is accepted only at difference score 4 or 5. Current planned score: {difference_score(site)}.
"""


def generated_asset_records(site: dict[str, object]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    def add(layer: str, filename: str, usage: str, alt: str = "") -> None:
        records.append({
            "layer": layer,
            "filename": filename,
            "source": "Generated locally by premium-static-site-system/tools/build_demo_sites.py",
            "license": "Original ASH-TRA generated asset; no external image licence; no copied inspiration-site asset",
            "usage": usage,
            "alt": alt,
            "status": "replaced/local/documented",
        })

    add("brand", brand_logo_path(site), "primary logo lockup", f"{site['brand']} logo")
    add("brand", brand_wordmark_path(site), "wordmark", f"{site['brand']} wordmark")
    add("brand", brand_symbol_path(site), "header/footer symbol", "")
    add("brand", favicon_svg_path(site), "SVG favicon", f"{site['brand']} favicon")
    add("brand", favicon_png_path(site, 32), "PNG favicon", f"{site['brand']} favicon")
    add("brand", favicon_png_path(site, 64), "retina PNG favicon", f"{site['brand']} favicon")
    add("brand", apple_touch_icon_path(site), "Apple touch icon", f"{site['brand']} app icon")
    add("brand", social_avatar_path(site), "social avatar", f"{site['brand']} social avatar")
    add("background", background_asset_path(site, "site"), "site background texture", "")
    add("diagram", diagram_asset_path(site, "system"), "system/proof diagram", f"{site['brand']} system diagram")
    add("process", process_asset_path(site, "journey"), "journey/process diagram", f"{site['brand']} process diagram")
    add("pattern", pattern_asset_path(site, "brand"), "brand pattern", "")
    add("mockup", mockup_asset_path(site, "interface"), "original interface mockup", f"{site['brand']} interface mockup")
    add("download", download_cover_path(site), "download/resource cover", f"{site['brand']} readiness checklist cover")
    add("video", video_poster_path(site), "video poster fallback", f"{site['brand']} video poster")
    add("legacy", f"assets/icons/{site['slug']}-mark.svg", "legacy mark path compatibility", "")
    add("legacy", f"assets/images/{site['slug']}-proof-panel.svg", "legacy proof panel compatibility", f"{site['brand']} proof visual")
    add("legacy", legacy_og_asset_path(site), "legacy Open Graph compatibility", f"{site['brand']} social preview")
    for name in ["menu", "close", "arrow", "search", "download", "calendar", "phone", "email", "location", "success", "error", "external-link"]:
        add("ui icon", ui_icon_path(site, name), f"{name} UI icon", "")
    for name in ["privacy", "cookies", "terms", "accessibility", "sitemap", "thanks", "404"]:
        add("legal icon", legal_icon_path(site, name), f"{name} legal/utility icon", "")
        add("utility", utility_asset_path(site, name), f"{name} page visual", f"{site['brand']} {name} support visual")
        add("og", og_asset_path(site, name), f"{name} social preview", f"{site['brand']} {name} social preview")
    for name in ["phone", "email", "whatsapp", "location", "booking", "privacy"]:
        add("contact icon", contact_icon_path(site, name), f"{name} contact icon", "")
    add("utility", utility_asset_path(site, "form"), "form-side visual", f"{site['brand']} enquiry form visual")
    for index, term in enumerate(core_terms(site), start=1):
        add("service icon", service_icon_path(site, term, index), f"{term} service icon", "")
    for page in site["pages"]:  # type: ignore[index]
        page_name = str(page["name"])
        add("hero", hero_asset_path(site, page_name), f"{page_name} desktop hero image", f"{site['brand']} {page_name} hero visual")
        add("hero", hero_asset_path(site, page_name, "tablet"), f"{page_name} tablet hero crop", f"{site['brand']} {page_name} tablet hero visual")
        add("hero", hero_asset_path(site, page_name, "mobile"), f"{page_name} mobile hero crop", f"{site['brand']} {page_name} mobile hero visual")
        add("page", page_asset_path(site, page_name), f"{page_name} page visual", f"{site['brand']} {page_name} page visual")
        add("og", og_asset_path(site, page_name), f"{page_name} social preview", f"{site['brand']} {page_name} social preview")
        add("legacy", f"assets/images/{site['slug']}-{slugify(page_name)}-hero-visual.svg", f"{page_name} legacy hero compatibility", f"{site['brand']} {page_name} legacy visual")
        add("gallery", gallery_asset_path(site, page_name, 1), f"{page_name} gallery asset 1", f"{site['brand']} {page_name} gallery visual")
        add("gallery", gallery_asset_path(site, page_name, 2), f"{page_name} gallery asset 2", f"{site['brand']} {page_name} gallery proof visual")
        for section_index, section in enumerate(page["sections"], start=1):  # type: ignore[index]
            section_name = str(section)
            add("section icon", section_icon_path(site, page_name, section_name, section_index), f"{page_name} / {section_name} icon", "")
            add("section", section_asset_path(site, page_name, section_name, section_index), f"{page_name} / {section_name} section visual", f"{section_name} visual for {site['brand']}")
            for card_index in range(1, 4):
                add("card", card_asset_path(site, page_name, section_name, section_index, card_index), f"{page_name} / {section_name} card thumbnail {card_index}", "")
        add("cta", section_asset_path(site, page_name, "CTA", 99, 1), f"{page_name} CTA visual", "")
    for card_index in range(1, 4):
        add("partial card", card_asset_path(site, "Home", "Resources", 1, card_index), f"source partial resources card {card_index}", "")
    return records


def render_asset_inventory_doc(site: dict[str, object]) -> str:
    rows = [[r["layer"], r["filename"], r["usage"], r["source"], r["license"], r["status"]] for r in generated_asset_records(site)]
    return f"""# Asset Inventory

Every listed file is generated locally and used or retained as an intentional compatibility asset. There are no hotlinked, copied, stock, celebrity, fake partner, fake certification, fake portrait, copied screenshot, copied map, copied dashboard, or unclear-licence assets in this generated site.

{markdown_table(["Layer", "Filename", "Usage", "Source", "Licence", "Status"], rows)}
"""


def render_page_asset_map_doc(site: dict[str, object]) -> str:
    rows = []
    for page in site["pages"]:  # type: ignore[index]
        page_name = str(page["name"])
        rows.append([
            page_name,
            hero_asset_path(site, page_name),
            hero_asset_path(site, page_name, "tablet"),
            hero_asset_path(site, page_name, "mobile"),
            page_asset_path(site, page_name),
            og_asset_path(site, page_name),
            gallery_asset_path(site, page_name, 1),
            f"{site['brand']} {page_name} hero visual; decorative thumbnails use empty alt where repeated",
        ])
    return f"""# Page Asset Map

{markdown_table(["Page", "Hero", "Tablet Crop", "Mobile Crop", "Page Visual", "Open Graph", "Gallery", "Alt Text Rule"], rows)}
"""


def render_section_asset_map_doc(site: dict[str, object]) -> str:
    rows = []
    for page in site["pages"]:  # type: ignore[index]
        page_name = str(page["name"])
        for index, section in enumerate(page["sections"], start=1):  # type: ignore[index]
            section_name = str(section)
            rows.append([
                page_name,
                section_name,
                section_asset_path(site, page_name, section_name, index),
                section_icon_path(site, page_name, section_name, index),
                card_asset_path(site, page_name, section_name, index, 1),
                section_asset(site, section_name),
                "local SVG, lazy-loaded unless hero/utility first view",
                "source/licence recorded in asset-inventory and asset-licenses",
            ])
    return f"""# Section Asset Map

{markdown_table(["Page", "Section", "Section Image", "Icon", "Card Thumbnail", "Requirement", "Responsive Behaviour", "Record"], rows)}
"""


def render_asset_prompts_doc(site: dict[str, object]) -> str:
    rows = [
        ["Brand system", f"Create an original {site['brand']} mark and wordmark using {site['visualDirection']} and palette {', '.join(site['palette'])}."],
        ["Hero system", f"Generate local vector hero assets for {site['heroType']} without copying inspiration-site photography, UI, code, or brand assets."],
        ["Section system", f"Create one section visual, one icon, and three card thumbnails per section using {site['imageDirection']}."],
        ["Mockups/diagrams", f"Use abstract original dummy-data interfaces and diagrams for {site['layoutSignature']}; no copied dashboards, maps, or product screenshots."],
        ["Utility/social", "Create local utility visuals, favicons, Apple icon, PNG icons, and page-specific OG previews."],
    ]
    return f"""# Asset Prompts

These are deterministic generation prompts for the local build script, not instructions to scrape or copy reference assets.

{markdown_table(["Asset Area", "Prompt Record"], rows)}
"""


def render_asset_qa_doc(site: dict[str, object]) -> str:
    rows = [
        ["Local paths", "All generated asset paths are relative and local to the site folder."],
        ["No licensed images", "No external stock/photo/map/dashboard/font/image sources are used."],
        ["No fake proof", "No fake client logos, certification badges, partner logos, testimonials, staff portraits, or media logos are generated."],
        ["Responsive crops", "Hero desktop/tablet/mobile SVG crops are generated per page; CSS preserves object-fit and dimensions."],
        ["Accessibility", "Informative images receive purpose alt text; repeated decorative icons/thumbs use empty alt."],
        ["Performance", "SVG is used for scalable visuals; PNG is limited to favicons/touch/social icons; lazy loading is used off hero."],
        ["Theme fit", f"Assets follow {site['visualDirection']} and {site['imageDirection']}."],
    ]
    return f"""# Asset QA

{markdown_table(["Check", "Result"], rows)}
"""


def render_og_image_plan_doc(site: dict[str, object]) -> str:
    rows = []
    for page in site["pages"]:  # type: ignore[index]
        page_name = str(page["name"])
        rows.append([page_name, og_asset_path(site, page_name), f"{site['brand']} {page_name} social preview", "1200x630 SVG-equivalent composition"])
    for utility in ["privacy", "cookies", "terms", "accessibility", "sitemap", "thanks", "404"]:
        rows.append([utility, og_asset_path(site, utility), f"{site['brand']} {utility} social preview", "utility/social-safe visual"])
    return f"""# Open Graph Image Plan

{markdown_table(["Page", "OG File", "Alt", "Crop"], rows)}
"""


def render_icon_system_doc(site: dict[str, object]) -> str:
    rows = []
    for name in ["menu", "close", "arrow", "search", "download", "calendar", "phone", "email", "location", "success", "error", "external-link"]:
        rows.append(["UI", name, ui_icon_path(site, name), "original local SVG"])
    for name in ["phone", "email", "whatsapp", "location", "booking", "privacy"]:
        rows.append(["Contact", name, contact_icon_path(site, name), "original local SVG"])
    for index, term in enumerate(core_terms(site), start=1):
        rows.append(["Service", term, service_icon_path(site, term, index), "original local SVG"])
    return f"""# Icon System

{markdown_table(["Family", "Icon", "File", "Source"], rows)}
"""


def render_mockup_system_doc(site: dict[str, object]) -> str:
    rows = [
        ["Interface mockup", mockup_asset_path(site, "interface"), "Original dummy-data mockup; no copied product screenshot."],
        ["System diagram", diagram_asset_path(site, "system"), "Original process/system diagram; no copied diagram."],
        ["Journey diagram", process_asset_path(site, "journey"), "Original process visual for conversion and proof."],
    ]
    return f"""# Mockup System

{markdown_table(["Asset", "File", "Rule"], rows)}
"""


def render_responsive_image_plan_doc(site: dict[str, object]) -> str:
    rows = [[str(page["name"]), hero_asset_path(site, str(page["name"])), hero_asset_path(site, str(page["name"]), "tablet"), hero_asset_path(site, str(page["name"]), "mobile"), "picture/source with fixed width/height; object-fit cover"] for page in site["pages"]]  # type: ignore[index]
    return f"""# Responsive Image Plan

{markdown_table(["Page", "Desktop", "Tablet", "Mobile", "Integration"], rows)}
"""


def render_asset_performance_report(site: dict[str, object]) -> str:
    rows = [
        ["Format choice", "SVG for illustrations, diagrams, mockups, cards, gallery, OG; PNG only for browser/app icons."],
        ["Loading", "Hero image eager/preloaded; non-critical images lazy-loaded with width/height attributes."],
        ["No bloat", "No base64, no remote images, no videos, no copied heavy screenshots."],
        ["Reusable CSS", "Object-fit/aspect-ratio prevents layout shift and stretched crops."],
    ]
    return f"""# Asset Performance Report

{markdown_table(["Area", "Result"], rows)}
"""


def render_asset_accessibility_report(site: dict[str, object]) -> str:
    rows = [
        ["Informative alt", "Hero, gallery, utility, OG, form, and page visuals receive descriptive alt text."],
        ["Decorative assets", "Repeated card thumbs, UI icons, and section icons are empty-alt when text already describes the same content."],
        ["Charts/diagrams", "Diagrams are decorative support; section copy contains the real information."],
        ["Motion", "Assets are static SVG/PNG; reduced-motion CSS is still present for UI transitions."],
        ["Contrast", "CSS tokens now choose dark surfaces when the target palette is dark, preventing pale text on light panels."],
    ]
    return f"""# Asset Accessibility Report

{markdown_table(["Area", "Result"], rows)}
"""


def render_asset_replacement_log(site: dict[str, object]) -> str:
    rows = [
        ["Placeholder images", "Replaced with local generated brand/page/section/card/gallery/utility SVG systems."],
        ["Copied or hotlinked images", "None retained; generator writes only local original assets."],
        ["Repeated unrelated images", "Every filename is site-scoped and page/section-scoped where used."],
        ["Missing favicons/social", "SVG favicon, PNG favicons, Apple touch icon, social avatar, and page OG images generated."],
        ["Fake trust assets", "No fake logos, portraits, certification badges, partner marks, media logos, or copied screenshots generated."],
    ]
    return f"""# Asset Replacement Log

{markdown_table(["Replacement Area", "Status"], rows)}
"""


def render_asset_licenses_doc(site: dict[str, object]) -> str:
    passport = site["designPassport"]  # type: ignore[assignment]
    asset_rows = [[r["layer"], r["filename"], r["source"], r["license"], r["usage"], r["status"]] for r in generated_asset_records(site)]
    return f"""# Asset Licenses

Current assets are locally generated SVG/PNG files created for this ASH-TRA static demo.

External asset policy for this generated build: no external images are used. If a future client adds external assets, they must be copyright-free or explicitly licensed for the intended commercial use and recorded before launch.

Site image system: {passport['imageSystem']}.

{markdown_table(["Type", "Filename", "Source", "License", "Usage", "Notes"], asset_rows)}
"""


def render_docs(site: dict[str, object]) -> dict[str, str]:
    checklist = "\n".join(f"- {name}" for name in [
        "Planning & Strategy", "Brand Strategy", "Information Architecture", "UX", "UI", "Design System",
        "Content Strategy", "Conversion Rate Optimisation", "Front-End Development", "Static Website Architecture",
        "Forms & Lead Capture", "SEO", "Local SEO", "Accessibility", "QA", "Performance Optimisation",
        "Analytics", "Tracking Analytics", "Monitoring & Observability", "Security", "Legal, Privacy & Compliance",
        "Hosting & Infrastructure", "DevOps / CI-CD", "Asset Management", "CMS / WordPress export readiness",
        "Static Blog & Content Production", "Client Handoff & Documentation", "Pre-Launch / Launch / Post-Launch",
        "Website Audit",
    ])
    difference_report = render_cross_site_difference_doc(site)
    docs = {
        "README.md": f"# {site['brand']}\n\nPremium static ASH-TRA demo for {site['industry']}.\n\nRemote: {site['repo']}\n\nRun `python3 scripts/maintain.py all` before launch and `python3 scripts/publish.py` after the numeric repo exists.\n",
        "docs/content-map.md": render_content_map(site),
        "docs/inspiration-audit.md": render_inspiration_audit_doc(site),
        "docs/design-extraction.md": render_design_extraction_doc(site),
        "docs/theme-direction.md": render_theme_direction_doc(site),
        "docs/theme-guide.md": render_theme_guide(site),
        "docs/layout-system.md": render_layout_system_doc(site),
        "docs/partials-system.md": render_partials_system_doc(site),
        "docs/component-system.md": render_component_system_doc(site),
        "docs/css-system.md": render_css_system_doc(site),
        "docs/js-system.md": render_js_system_doc(site),
        "docs/js-interaction-plan.md": render_js_interaction_plan_doc(site),
        "docs/asset-system.md": render_asset_system_doc(site),
        "docs/asset-direction.md": render_asset_direction_doc(site),
        "docs/page-section-style-map.md": render_page_section_style_map(site),
        "docs/mobile-system.md": render_mobile_system_doc(site),
        "docs/mobile-behaviour.md": render_mobile_behaviour_doc(site),
        "docs/conversion-system.md": render_conversion_system_doc(site),
        "docs/cross-site-difference-report.md": difference_report,
        "docs/cross-site-diversity-report.md": difference_report.replace("# Cross-Site Difference Report", "# Cross-Site Diversity Report"),
        "docs/asset-licenses.md": render_asset_licenses_doc(site),
        "docs/asset-inventory.md": render_asset_inventory_doc(site),
        "docs/page-asset-map.md": render_page_asset_map_doc(site),
        "docs/section-asset-map.md": render_section_asset_map_doc(site),
        "docs/asset-prompts.md": render_asset_prompts_doc(site),
        "docs/asset-qa.md": render_asset_qa_doc(site),
        "docs/og-image-plan.md": render_og_image_plan_doc(site),
        "docs/icon-system.md": render_icon_system_doc(site),
        "docs/mockup-system.md": render_mockup_system_doc(site),
        "docs/responsive-image-plan.md": render_responsive_image_plan_doc(site),
        "docs/asset-performance-report.md": render_asset_performance_report(site),
        "docs/asset-accessibility-report.md": render_asset_accessibility_report(site),
        "docs/asset-replacement-log.md": render_asset_replacement_log(site),
        "docs/analytics-plan.md": "# Analytics Plan\n\nTrack only non-personal events: page views, CTA clicks, form starts, successful form submissions, contact clicks, downloads, filters, searches, gallery opens, pricing toggles, and 404 recovery. Do not track names, emails, phones, addresses, messages, health, financial, legal, or sensitive details.\n",
        "docs/qa-report.md": f"# QA Report\n\nChecklist basis:\n{checklist}\n\nAutomated checks: run `python3 scripts/maintain.py all`.\n\nTransformation-pack checks: run `python3 ../../premium-static-site-system/tools/validate_transformation_packs.py` from the repository root.\n\nManual checks required: desktop, tablet, mobile, keyboard, focus, reduced motion, forms, legal pages, visual polish, content accuracy, and cross-site diversity.\n",
        "docs/handoff.md": f"# Handoff\n\nThis is a static HTML/CSS/JS website. Edit HTML for content, `css/styles.css` for design tokens and components, `js/main.js` for progressive enhancement, and `site.config.json` for site metadata. Replace Formspree endpoint, contact details, assets, and legal text when sold to a client.\n\nBefore changing visual design, update the full transformation pack: {', '.join(TRANSFORMATION_PACK_FILES)}.\n",
        "docs/wordpress-export.md": f"# WordPress Export\n\nFuture custom theme mapping: header, footer, core page templates, resource templates, FAQ/contact/legal templates, image fields, SEO fields, navigation, footer sitemap, and form configuration. Do not use Elementor or paid builder dependency. Preserve the static design system and accessibility rules.\n",
    }
    return docs


def script_maintain(site: dict[str, object]) -> str:
    return f'''#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "site.config.json").read_text(encoding="utf-8"))

def html_files():
    return sorted(ROOT.glob("*.html"))

def check():
    errors = []
    expected = CONFIG["pages"]
    for page in expected:
        path = ROOT / page["file"]
        if not path.exists():
            errors.append(f"missing page {{page['file']}}")
            continue
        text = path.read_text(encoding="utf-8")
        sections = re.findall(r"<section\\b[^>]*data-section=\\"([^\\"]+)\\"", text)
        core_sections = sections
        if core_sections != page["sections"]:
            errors.append(f"section mismatch in {{page['file']}}: {{core_sections}}")
        if len(core_sections) != 10:
            errors.append(f"wrong section count in {{page['file']}}")
        if len(set(core_sections)) != len(core_sections):
            errors.append(f"duplicate sections in {{page['file']}}")
        if not re.search(r"<h1\\b", text):
            errors.append(f"missing h1 in {{page['file']}}")
    for utility in ["privacy.html","cookies.html","terms.html","accessibility.html","sitemap.html","thanks.html","404.html"]:
        if not (ROOT / utility).exists():
            errors.append(f"missing utility {{utility}}")
    for partial in ["header.html","mobile-menu.html","footer.html","hero.html","cta.html","form.html","cards.html","resources.html","pricing.html","faq.html","cookie.html","legal.html"]:
        if not (ROOT / "partials" / partial).exists():
            errors.append(f"missing partial {{partial}}")
    if errors:
        print("\\n".join(errors))
        return 1
    print("Structural check passed.")
    return 0

def sitemap():
    urls = []
    for path in html_files():
        name = "" if path.name == "index.html" else path.name
        urls.append(CONFIG["baseUrl"].rstrip("/") + "/" + name)
    body = "\\n".join(f"  <url><loc>{{url}}</loc></url>" for url in urls)
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n' + body + '\\n</urlset>\\n', encoding="utf-8")
    print("sitemap.xml updated.")
    return 0

def audit():
    tool = ROOT.parents[1] / "premium-static-site-system" / "tools" / "static_site_quality.py"
    if not tool.exists():
        print("static_site_quality.py not found; run from portfolio checkout.")
        return 1
    return subprocess.call([sys.executable, str(tool), "audit", str(ROOT), "--base-url", CONFIG["baseUrl"], "--out", str(ROOT / "quality-report.json"), "--report-md", str(ROOT / "quality-report.md"), "--fail-on", "critical"])

def seo(write=False):
    tool = ROOT.parents[1] / "premium-static-site-system" / "tools" / "static_site_quality.py"
    args = [sys.executable, str(tool), "fix", str(ROOT), "--base-url", CONFIG["baseUrl"], "--site-name", CONFIG["siteName"]]
    if write:
        args.append("--write")
    return subprocess.call(args)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["check","sitemap","audit","seo","all"])
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.command == "check": return check()
    if args.command == "sitemap": return sitemap()
    if args.command == "audit": return audit()
    if args.command == "seo": return seo(args.write)
    status = sitemap() or check() or seo(True) or audit()
    return status

if __name__ == "__main__":
    raise SystemExit(main())
'''


def script_publish(site: dict[str, object]) -> str:
    return f'''#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REMOTE = "{site['repo']}"

def run(args):
    print("+", " ".join(args))
    return subprocess.check_call(args, cwd=ROOT)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--message")
    parser.add_argument("--remote", default=REMOTE)
    args = parser.parse_args()
    if not (ROOT / ".git").exists():
        run(["git", "init"])
        run(["git", "branch", "-M", "main"])
    remotes = subprocess.run(["git", "remote"], cwd=ROOT, text=True, capture_output=True, check=True).stdout.split()
    if "origin" not in remotes:
        run(["git", "remote", "add", "origin", args.remote])
    else:
        run(["git", "remote", "set-url", "origin", args.remote])
    message = args.message or "update " + dt.datetime.now().strftime("%Y-%m-%d %H-%M")
    run(["git", "add", "-A"])
    run(["git", "commit", "--allow-empty", "-m", message])
    run(["git", "push", "-u", "origin", "main"])

if __name__ == "__main__":
    main()
'''


def config_for(site: dict[str, object]) -> dict[str, object]:
    pages = []
    for page in site["pages"]:  # type: ignore[index]
        pages.append({"name": page["name"], "file": page_filename(str(page["name"])), "sections": page["sections"]})
    return {
        "siteName": site["brand"],
        "industry": site["industry"],
        "number": site["number"],
        "slug": site["slug"],
        "baseUrl": site["baseUrl"],
        "repo": site["repo"],
        "formEndpoint": FORM_ENDPOINT,
        "contactUrl": ASH_TRA_CONTACT,
        "cta": site["cta"],
        "schema": site["schema"],
        "visualDirection": site["visualDirection"],
        "premiumDirection": site["premiumDirection"],
        "layoutSignature": site["layoutSignature"],
        "heroType": site["heroType"],
        "headerType": site["headerType"],
        "footerType": site["footerType"],
        "cardStyle": site["cardStyle"],
        "formStyle": site["formStyle"],
        "jsSignature": site["jsSignature"],
        "motionStyle": site["motionStyle"],
        "themeMode": site["themeMode"],
        "designPassport": site["designPassport"],
        "targetReference": site["targetReference"],
        "targetCssProfile": site["targetCssProfile"],
        "references": site["references"],
        "assets": {
            "brandLogo": brand_logo_path(site),
            "brandSymbol": brand_symbol_path(site),
            "favicon": favicon_svg_path(site),
            "appleTouchIcon": apple_touch_icon_path(site),
            "openGraphDefault": og_asset_path(site, "Home"),
            "mockup": mockup_asset_path(site, "interface"),
            "assetInventory": "docs/asset-inventory.md",
            "assetLicenses": "docs/asset-licenses.md",
        },
        "pages": pages,
    }


def render_matrix_markdown(sites: list[dict[str, object]]) -> str:
    lines = ["# 50-Site Build Matrix", "", "This file is generated from the approved ASH-TRA static portfolio matrix.", ""]
    for site in sites:
        lines.extend([f"## {site['number']:02d}. {site['industry']}", "", f"- Folder: `demo-sites/{site['folder']}`", f"- Repo: `{site['repo']}`", f"- Brand: {site['brand']}", f"- CTA: {site['cta']}", f"- Premium direction: {site['premiumDirection']}", f"- Design passport: {site['brandMood']}; {site['buyerPsychology']}; {site['layoutArchetype']}; {site['shapeLanguage']}; {site['surfaceMaterial']}", ""])
        for page in site["pages"]:  # type: ignore[index]
            lines.append(f"- **{page['name']}**: {', '.join(page['sections'])}")
        lines.append("")
    return "\n".join(lines)


def render_portfolio_index(sites: list[dict[str, object]]) -> str:
    rows = []
    for site in sites:
        rows.append(
            f"| {site['number']:02d} | {site['industry']} | `demo-sites/{site['folder']}` | {site['brand']} | {site['heroType']} | {site['layoutSignature']} | {site['jsSignature']} | `{site['repo']}` | Structural, static, and diversity QA required |"
        )
    return "\n".join(
        [
            "# ASH-TRA 50-Site Portfolio Index",
            "",
            "Each folder is an independent static website with 10 matrix pages, 7 utility pages, local assets, docs, QA reports, and publish scripts.",
            "",
            "| # | Industry | Folder | Brand | Hero | Layout | JS signature | Repo | QA status |",
            "|---|---|---|---|---|---|---|---|---|",
            *rows,
            "",
            "Run a site with a local static server from its folder, run `python3 scripts/maintain.py all` before deployment, and run `python3 scripts/publish.py` after its matching numeric GitHub repo exists.",
        ]
    )


def render_global_diversity_report(sites: list[dict[str, object]]) -> str:
    lines = [
        "# Cross-Site Diversity Report",
        "",
        "This report makes the anti-template rule measurable. Each site must be reviewed for a distinct theme DNA, not only a different palette.",
        "",
        "| # | Theme | Premium direction | Visual category | Typography | Palette | Hero type | Layout archetype | Header | Footer | Cards | Form | JS signature | Motion | Image direction | Mobile/cookie/legal | Must not resemble |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for site in sites:
        palette = ", ".join(site["palette"])  # type: ignore[arg-type]
        lines.append(
            f"| {site['number']:02d} | {site['brand']} | {site['premiumDirection']} | {site['visualDirection']} | {site['typographySummary']} | {palette} | {site['heroType']} | {site['layoutSignature']} | {site['headerType']} | {site['footerType']} | {site['cardStyle']} | {site['formStyle']} | {site['jsSignature']} | {site['motionStyle']} | {site['imageDirection']} | {site['mobileMenuStyle']} / {site['cookieStyle']} / {site['legalStyle']} | {site['avoidSites']} |"
        )
    lines.extend(
        [
            "",
            "Batch acceptance rule: a batch fails if sites share the same hero layout, header, mobile menu, card grid, pricing design, footer, button shapes, colour logic, image treatment, animation, section pacing, form layout, FAQ style, testimonial style, or resource cards without a deliberate industry reason.",
        ]
    )
    return "\n".join(lines)


def render_diversity_register(sites: list[dict[str, object]]) -> str:
    rows = []
    for site in sites:
        passport = site["designPassport"]  # type: ignore[assignment]
        rows.append([
            f"{int(site['number']):02d}",
            site["industry"],
            site["brand"],
            site["layoutSignature"],
            site["typographySummary"],
            ", ".join(site["palette"]),  # type: ignore[arg-type]
            passport["surfaceMaterial"],
            passport["imageSystem"],
            site["headerType"],
            passport["mobileMenuStyle"],
            site["footerType"],
            site["heroType"],
            site["cardStyle"],
            site["formStyle"],
            passport["pricingStyle"],
            f"{site['themeMode']} FAQ/support",
            passport["resourceStyle"],
            site["imageDirection"],
            site["jsSignature"],
            site["motionStyle"],
            passport["interactionModel"],
            site["avoidSites"],
            similarity_risk(site),
            difference_score(site),
            "QA must compare visible structure against previous completed sites before acceptance",
        ])
    return "\n".join([
        "# 50-Site Diversity Register",
        "",
        "This is the master measurable register for the 50-site anti-template rule. Each row records the design-system decisions that must remain distinct when a site is edited or rebuilt.",
        "",
        markdown_table([
            "Site", "Industry", "Theme Name", "Layout Archetype", "Typography System", "Colour System",
            "Surface Style", "Asset Style", "Header Type", "Mobile Menu Type", "Footer Type",
            "Hero Type", "Card Style", "Form Style", "Pricing Style", "FAQ Style", "Resource Style",
            "Gallery Style", "JS Signature", "Motion Style", "Conversion Flow", "Must Not Resemble",
            "Similarity Risk", "Difference Score", "QA Notes",
        ], rows),
        "",
        "Acceptance rule: each site must score 4 or 5. Any score of 1, 2, or 3 fails and requires redesign before continuing.",
    ])


def render_batch_diversity_review(sites: list[dict[str, object]]) -> str:
    lines = [
        "# Batch Diversity Review",
        "",
        "Review the portfolio in batches of five. A batch fails if the sites share the same visible partials, section rhythm, cards, forms, pricing, FAQ, footer, asset treatment, or JS interaction emphasis without a deliberate industry reason.",
    ]
    for start in range(0, len(sites), 5):
        batch = sites[start:start + 5]
        label = f"{int(batch[0]['number']):02d} vs {int(batch[1]['number']):02d} vs {int(batch[2]['number']):02d} vs {int(batch[3]['number']):02d} vs {int(batch[4]['number']):02d}"
        lines.extend(["", f"## Sites {label}", ""])
        rows = []
        for site in batch:
            passport = site["designPassport"]  # type: ignore[assignment]
            rows.append([
                f"{int(site['number']):02d}",
                site["brand"],
                site["layoutSignature"],
                site["heroType"],
                site["headerType"],
                passport["mobileMenuStyle"],
                site["cardStyle"],
                site["formStyle"],
                site["jsSignature"],
                difference_score(site),
            ])
        lines.append(markdown_table([
            "Site", "Theme", "Layout", "Hero", "Header", "Mobile Menu",
            "Cards", "Form", "JS", "Score",
        ], rows))
        lines.extend([
            "",
            "- Similarity watch: compare header, mobile menu, hero, card geometry, pricing layout, FAQ, footer, button shape, image treatment, motion rhythm, and utility pages.",
            "- Required action if too similar: redesign the weakest site in the batch before continuing to the next batch.",
            "- QA status: planned transformation packs score 4 or 5; final acceptance still requires screenshot/browser review.",
        ])
    return "\n".join(lines)


def render_inspiration_reference_library(sites: list[dict[str, object]]) -> str:
    rows = []
    for site in sites:
        refs = references_for(site)
        counts = reference_category_counts(site)
        rows.append([
            f"{int(site['number']):02d}",
            site["industry"],
            site["brand"],
            f"{counts.get('direct', 0)} direct / {counts.get('adjacent', 0)} adjacent / {counts.get('contrast', 0)} contrast / {counts.get('interaction', 0)} interaction",
            "; ".join(f"{ref['category']}: {ref['name']}" for ref in refs),
        ])
    return "\n".join([
        "# 50-Site Inspiration Reference Library",
        "",
        "Each site must study at least 8 references before visual implementation: 3 direct industry references, 2 adjacent references, 2 contrast references, and 1 interaction or UI pattern reference. These are inspiration pools only; do not copy code, copy, logos, images, exact layouts, exact animations, or proprietary identity.",
        "",
        markdown_table(["Site", "Industry", "Theme", "Reference Mix", "References"], rows),
    ])


def render_portfolio_html(sites: list[dict[str, object]]) -> str:
    cards = []
    for site in sites:
        href = f"{site['folder']}/index.html"
        cards.append(
            f'<article><span>{site["number"]:02d}</span><h2>{esc(site["brand"])}</h2><p>{esc(site["industry"])}</p><p><strong>{esc(site["heroType"])}</strong><br>{esc(site["layoutSignature"])}</p><a href="{href}">Open site</a><small>{esc(site["repo"])}</small></article>'
        )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ASH-TRA 50-Site Static Portfolio Index</title>
  <meta name="description" content="Index of 50 independent premium static ASH-TRA demo websites.">
  <style>
    body {{ margin:0; font-family: Inter, system-ui, sans-serif; background:#f8fafc; color:#111827; }}
    main {{ width:min(1180px, calc(100% - 40px)); margin:0 auto; padding:64px 0; }}
    h1 {{ font-size:clamp(2rem, 5vw, 4.5rem); line-height:1; }}
    .grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:1rem; }}
    article {{ background:white; border:1px solid #e5e7eb; border-radius:12px; padding:1rem; box-shadow:0 18px 40px rgba(15,23,42,.08); }}
    span {{ color:#2563eb; font-weight:900; }}
    h2 {{ margin:.35rem 0; }}
    a {{ display:inline-flex; margin:.75rem 0; font-weight:800; color:#2563eb; }}
    small {{ display:block; overflow-wrap:break-word; word-break:normal; color:#64748b; }}
  </style>
</head>
<body>
<main>
  <h1>ASH-TRA 50-Site Static Portfolio</h1>
  <p>Fifty independent premium static website demos, each mapped to its own future GitHub repository and Cloudflare Pages-ready folder.</p>
  <div class="grid">{"".join(cards)}</div>
</main>
</body>
</html>
"""


def partialize_paths(content: str) -> str:
    replacements = {
        'src="assets/': 'src="../assets/',
        'href="assets/': 'href="../assets/',
        'srcset="assets/': 'srcset="../assets/',
        'href="docs/': 'href="../docs/',
    }
    for before, after in replacements.items():
        content = content.replace(before, after)
    content = content.replace(", assets/", ", ../assets/")
    content = re.sub(
        r'href="((?!https?://|mailto:|tel:|#|../|//)([^"]+\.html)([^"]*))"',
        r'href="../\1"',
        content,
    )
    return content


def render_partials(site: dict[str, object]) -> dict[str, str]:
    passport = site["designPassport"]  # type: ignore[assignment]
    links = "".join(f'<a href="{page_href(str(page["name"]))}">{esc(page["name"])}</a>' for page in nav_pages(site))
    sample_page = site["pages"][0]  # type: ignore[index]
    sample_sections = sample_page["sections"]  # type: ignore[index]
    hero = render_section(site, str(sample_page["name"]), "Hero", 1)
    cta = render_cta_panel(site, str(sample_page["name"]))
    form = render_contact_form(site, "Contact")
    cards = "".join(
        f'<article class="mini-card"><h3>{esc(section)}</h3><p>{esc(passport["premiumDirection"])}</p></article>'
        for section in sample_sections[1:4]
    )
    resource_index = int(sample_sections.index("Resources") + 1) if "Resources" in sample_sections else 1
    resources = render_resource_block(site, str(sample_page["name"]), "Resources", resource_index)
    pricing = render_pricing_block(site)
    faq = render_faq_block(site, str(sample_page["name"]))
    cookie = f"""<div class="cookie-banner" data-cookie-banner role="region" aria-label="Cookie notice">
  <p>{esc(passport['cookieStyle'])}: optional analytics run only after consent.</p>
  <button type="button" data-cookie-accept>Accept</button>
  <a href="cookies.html">Manage</a>
</div>"""
    whatsapp = render_whatsapp_widget(site, "Home")
    back_to_top = '<button class="back-to-top" type="button" data-back-to-top aria-label="Back to top"><span>Top</span></button>'
    legal = f"""<section class="section legal-page legal-{esc(slugify(str(passport['legalStyle'])))}">
  <div class="container prose">
    <p class="eyebrow">{esc(passport['legalStyle'])}</p>
    <h1>Legal page title</h1>
    <p>{esc(site['disclaimer'])}</p>
  </div>
</section>"""
    thanks_title, thanks_body = utility_bodies(site)["thanks"]
    not_found_title, not_found_body = utility_bodies(site)["404"]
    partials = {
        "header.html": f"<!-- Source partial compiled into static pages. -->\n{render_header(site, 'Home')}\n",
        "mobile-menu.html": f"<!-- Source partial: {esc(passport['mobileMenuStyle'])}. -->\n<nav class=\"site-nav mobile-menu-{esc(slugify(str(passport['mobileMenuStyle'])))}\" aria-label=\"Main navigation\">{links}</nav>\n",
        "footer.html": f"<!-- Source partial compiled into static pages. -->\n{render_footer(site)}\n",
        "hero.html": f"<!-- Source partial: {esc(site['heroType'])}. -->\n{hero}\n",
        "cta.html": f"<!-- Source partial: {esc(passport['ctaStyle'])}. -->\n{cta}\n",
        "form.html": f"<!-- Source partial: {esc(site['formStyle'])}. -->\n{form}\n",
        "cards.html": f"<!-- Source partial: {esc(site['cardStyle'])}. -->\n<div class=\"card-grid card-{esc(slugify(str(site['cardStyle'])))}\">{cards}</div>\n",
        "resources.html": f"<!-- Source partial: {esc(passport['resourceStyle'])}. -->\n{resources}\n",
        "pricing.html": f"<!-- Source partial: {esc(passport['pricingStyle'])}. -->\n{pricing}\n",
        "faq.html": f"<!-- Source partial. -->\n{faq}\n",
        "cookie.html": f"<!-- Source partial: {esc(passport['cookieStyle'])}. -->\n{cookie}\n",
        "whatsapp.html": f"<!-- Source partial: fixed WhatsApp quick enquiry. -->\n{whatsapp}\n",
        "back-to-top.html": f"<!-- Source partial: scroll recovery control. -->\n{back_to_top}\n",
        "legal.html": f"<!-- Source partial: {esc(passport['legalStyle'])}. -->\n{legal}\n",
        "404.html": f"<!-- Source partial: branded recovery page. -->\n<section class=\"section error-page\"><div class=\"container prose\"><p class=\"eyebrow\">{esc(site['brand'])} recovery</p><h1>{esc(not_found_title)}</h1>{not_found_body}</div></section>\n",
        "thanks.html": f"<!-- Source partial: branded confirmation page. -->\n<section class=\"section thanks-page\"><div class=\"container prose\"><p class=\"eyebrow\">{esc(site['brand'])} confirmation</p><h1>{esc(thanks_title)}</h1>{thanks_body}</div></section>\n",
    }
    return {name: partialize_paths(content) for name, content in partials.items()}


def clean_generated_asset_tree(site_root: Path) -> None:
    for rel in GENERATED_ASSET_DIRS:
        path = site_root / rel
        if path.exists():
            shutil.rmtree(path)


def ensure_asset_directories(site_root: Path) -> None:
    folders = [
        "assets/brand",
        "assets/images/hero",
        "assets/images/pages",
        "assets/images/sections",
        "assets/images/cards",
        "assets/images/gallery",
        "assets/images/people",
        "assets/images/products",
        "assets/images/locations",
        "assets/images/backgrounds",
        "assets/images/utility",
        "assets/icons/ui",
        "assets/icons/services",
        "assets/icons/sections",
        "assets/icons/industry",
        "assets/icons/legal",
        "assets/icons/contact",
        "assets/illustrations/diagrams",
        "assets/illustrations/process",
        "assets/illustrations/patterns",
        "assets/mockups",
        "assets/downloads",
        "assets/og",
        "assets/video/posters",
    ]
    for folder in folders:
        (site_root / folder).mkdir(parents=True, exist_ok=True)


def write_generated_asset_system(site_root: Path, site: dict[str, object]) -> None:
    ensure_asset_directories(site_root)
    symbol = brand_symbol_svg(site)
    wordmark = brand_wordmark_svg(site)
    write(site_root / brand_symbol_path(site), symbol)
    write(site_root / brand_wordmark_path(site), wordmark)
    write(site_root / brand_logo_path(site), wordmark)
    write(site_root / favicon_svg_path(site), symbol)
    write(site_root / "assets" / "icons" / f"{site['slug']}-mark.svg", symbol)
    write_bytes(site_root / favicon_png_path(site, 32), png_bytes(site, 32))
    write_bytes(site_root / favicon_png_path(site, 64), png_bytes(site, 64))
    write_bytes(site_root / apple_touch_icon_path(site), png_bytes(site, 180))
    write_bytes(site_root / social_avatar_path(site), png_bytes(site, 512))
    write(site_root / background_asset_path(site, "site"), svg_asset(site, f"{site['brand']} background", str(site["visualDirection"]), "background", 1))
    write(site_root / diagram_asset_path(site, "system"), svg_asset(site, f"{site['brand']} system diagram", str(site["proofStyle"]), "diagram", 2))
    write(site_root / process_asset_path(site, "journey"), svg_asset(site, f"{site['brand']} journey", str(site["heroType"]), "diagram", 3))
    write(site_root / pattern_asset_path(site, "brand"), svg_asset(site, f"{site['brand']} pattern", str(site["visualDirection"]), "pattern", 4))
    write(site_root / mockup_asset_path(site, "interface"), svg_asset(site, f"{site['brand']} interface mockup", "Original dummy-data mockup", "mockup", 5))
    write(site_root / download_cover_path(site), svg_asset(site, f"{site['brand']} readiness checklist", str(site["industry"]), "cover", 6, 1200, 630))
    write(site_root / video_poster_path(site), svg_asset(site, f"{site['brand']} overview poster", str(site["industry"]), "cover", 7, 1200, 675))
    for index, name in enumerate(["menu", "close", "arrow", "search", "download", "calendar", "phone", "email", "location", "success", "error", "external-link"], start=1):
        write(site_root / ui_icon_path(site, name), icon_svg(site, name, index))
    for index, name in enumerate(["privacy", "cookies", "terms", "accessibility", "sitemap", "thanks", "404"], start=1):
        write(site_root / legal_icon_path(site, name), icon_svg(site, name, index + 20))
        write(site_root / utility_asset_path(site, name), svg_asset(site, f"{site['brand']} {name}", "Utility page visual", "utility", index + 20))
        write(site_root / og_asset_path(site, name), svg_asset(site, f"{site['brand']} {name}", "Static portfolio utility page", "og", index + 20, 1200, 630))
    for index, name in enumerate(["phone", "email", "whatsapp", "location", "booking", "privacy"], start=1):
        write(site_root / contact_icon_path(site, name), icon_svg(site, name, index + 40))
    write(site_root / utility_asset_path(site, "form"), svg_asset(site, f"{site['brand']} enquiry", str(site["formStyle"]), "utility", 44))
    for index, term in enumerate(core_terms(site), start=1):
        write(site_root / service_icon_path(site, term, index), icon_svg(site, term, index + 60))
    for page in site["pages"]:  # type: ignore[index]
        page_name = str(page["name"])
        page_label = f"{site['brand']} {page_name}"
        write(site_root / hero_asset_path(site, page_name), svg_asset(site, page_label, str(site["imageDirection"]), "hero", len(page_name), 960, 640))
        write(site_root / hero_asset_path(site, page_name, "tablet"), svg_asset(site, page_label, "Tablet crop", "hero", len(page_name) + 2, 900, 720))
        write(site_root / hero_asset_path(site, page_name, "mobile"), svg_asset(site, page_label, "Mobile crop", "hero", len(page_name) + 4, 720, 960))
        write(site_root / page_asset_path(site, page_name), svg_asset(site, page_label, str(site["heroType"]), "page", len(page_name) + 6))
        write(site_root / og_asset_path(site, page_name), svg_asset(site, page_label, str(site["industry"]), "og", len(page_name) + 8, 1200, 630))
        write(site_root / f"assets/images/{site['slug']}-{slugify(page_name)}-hero-visual.svg", svg_asset(site, page_label, str(site["voice"]), "legacy", len(page_name) + 10))
        write(site_root / gallery_asset_path(site, page_name, 1), svg_asset(site, f"{page_label} gallery", str(site["imageDirection"]), "gallery", len(page_name) + 12))
        write(site_root / gallery_asset_path(site, page_name, 2), svg_asset(site, f"{page_label} proof", str(site["proofStyle"]), "gallery", len(page_name) + 14))
        for section_index, section in enumerate(page["sections"], start=1):  # type: ignore[index]
            section_name = str(section)
            base_variant = section_index + len(page_name)
            write(site_root / section_icon_path(site, page_name, section_name, section_index), icon_svg(site, section_name, base_variant))
            write(site_root / section_asset_path(site, page_name, section_name, section_index), svg_asset(site, f"{page_label} {section_name}", section_asset(site, section_name), "section", base_variant))
            for card_index in range(1, 4):
                write(site_root / card_asset_path(site, page_name, section_name, section_index, card_index), svg_asset(site, f"{section_name} card {card_index}", str(site["cardStyle"]), "card", base_variant + card_index, 420, 280))
        write(site_root / section_asset_path(site, page_name, "CTA", 99, 1), svg_asset(site, f"{page_label} CTA", str(site["cta"]), "section", len(page_name) + 99, 420, 280))
    for card_index in range(1, 4):
        write(site_root / card_asset_path(site, "Home", "Resources", 1, card_index), svg_asset(site, f"Resources card {card_index}", str(site["cardStyle"]), "card", 120 + card_index, 420, 280))
    write(site_root / "assets" / "images" / f"{site['slug']}-proof-panel.svg", svg_asset(site, f"{site['brand']} proof", "Evidence, content, and conversion system", "legacy", 88))
    write(site_root / legacy_og_asset_path(site), svg_asset(site, f"{site['brand']}", "ASH-TRA premium static demo", "og", 90, 1200, 630))


def build_site(site: dict[str, object]) -> None:
    site_root = DEMO_ROOT / str(site["folder"])
    clean_generated_asset_tree(site_root)
    for stale in ["cookie-policy.html"]:
        stale_path = site_root / stale
        if stale_path.exists():
            stale_path.unlink()
    for page in site["pages"]:  # type: ignore[index]
        write(site_root / page_filename(str(page["name"])), render_page(site, page))
    for key, (title, body) in utility_bodies(site).items():
        write(site_root / ("404.html" if key == "404" else f"{key}.html"), render_utility_page(site, key, title, body))
    write(site_root / "css" / "styles.css", css_for_site(site))
    write(site_root / "js" / "main.js", js_source(site))
    write(site_root / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {str(site['baseUrl']).rstrip('/')}/sitemap.xml\n")
    write(site_root / "sitemap.xml", render_sitemap_xml(site))
    write(site_root / "site.config.json", json.dumps(config_for(site), indent=2) + "\n")
    write(site_root / "data" / "faqs.json", json.dumps([
        {"title": "What happens first?", "category": "general", "description": "A focused intake clarifies goals, constraints, risk, and the correct next route.", "order": 1, "featured": True},
        {"title": "How is scope confirmed?", "category": "delivery", "description": "The site explains inclusions, exclusions, evidence, timing, and review points before commitment.", "order": 2, "featured": True},
        {"title": "Can this static site become editable later?", "category": "handoff", "description": "The documentation includes a future custom WordPress export plan without Elementor dependency.", "order": 3, "featured": False},
    ], indent=2) + "\n")
    write(site_root / "data" / "resources.json", json.dumps([
        {"title": f"{site['brand']} readiness checklist", "slug": "readiness-checklist", "category": "checklist", "description": f"Planning prompts for {site['industry']} buyers.", "url": "assets/downloads/readiness-checklist.txt", "order": 1, "featured": True},
        {"title": "Launch QA notes", "slug": "launch-qa", "category": "qa", "description": "Static-site review notes based on the ASH-TRA checklist system.", "url": "docs/qa-report.md", "order": 2, "featured": True},
    ], indent=2) + "\n")
    write(site_root / "assets" / "downloads" / "readiness-checklist.txt", f"{site['brand']} readiness checklist\n\nReview audience, goals, pages, section content, assets, form routing, SEO, accessibility, legal notes, analytics, launch steps, and maintenance ownership before publishing this {site['industry']} site.\n")
    write(site_root / "site.webmanifest", json.dumps({
        "name": site["brand"],
        "short_name": site["brand"],
        "start_url": "index.html",
        "display": "standalone",
        "background_color": site["palette"][0],
        "theme_color": site["palette"][1],
        "icons": [
            {"src": favicon_svg_path(site), "sizes": "any", "type": "image/svg+xml"},
            {"src": favicon_png_path(site, 32), "sizes": "32x32", "type": "image/png"},
            {"src": favicon_png_path(site, 64), "sizes": "64x64", "type": "image/png"},
            {"src": apple_touch_icon_path(site), "sizes": "180x180", "type": "image/png"},
            {"src": social_avatar_path(site), "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2) + "\n")  # type: ignore[index]
    write(site_root / "_headers", "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()\n")
    write(site_root / "_redirects", "/home / 301\n")
    write(site_root / ".well-known" / "security.txt", f"Contact: {ASH_TRA_CONTACT}\nPolicy: {ASH_TRA_CONTACT}\n")
    write(site_root / "scripts" / "maintain.py", script_maintain(site))
    write(site_root / "scripts" / "publish.py", script_publish(site))
    for name, content in render_partials(site).items():
        write(site_root / "partials" / name, content)
    for rel, content in render_docs(site).items():
        write(site_root / rel, content)
    write_generated_asset_system(site_root, site)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build all 50 ASH-TRA demo static sites.")
    parser.add_argument("--site", type=int, help="Build only one site number.")
    args = parser.parse_args()
    sites = parse_matrix()
    write(SYSTEM_ROOT / "data" / "industry_matrix.json", json.dumps(sites, indent=2) + "\n")
    write(SYSTEM_ROOT / "docs" / "50-site-build-matrix.md", render_matrix_markdown(sites))
    write(SYSTEM_ROOT / "docs" / "50-site-diversity-register.md", render_diversity_register(sites))
    write(SYSTEM_ROOT / "docs" / "batch-diversity-review.md", render_batch_diversity_review(sites))
    write(SYSTEM_ROOT / "docs" / "inspiration-reference-library.md", render_inspiration_reference_library(sites))
    selected = [site for site in sites if not args.site or site["number"] == args.site]
    for site in selected:
        build_site(site)
    write(DEMO_ROOT / "README.md", "# ASH-TRA Demo Sites\n\nFifty independent premium static website folders generated from the approved matrix. Run each site's `scripts/maintain.py all` before publishing, then `scripts/publish.py` after the matching numeric GitHub repo exists.\n")
    write(DEMO_ROOT / "PORTFOLIO_INDEX.md", render_portfolio_index(sites))
    write(DEMO_ROOT / "docs" / "cross-site-diversity-report.md", render_global_diversity_report(sites))
    write(DEMO_ROOT / "docs" / "50-site-diversity-register.md", render_diversity_register(sites))
    write(DEMO_ROOT / "docs" / "batch-diversity-review.md", render_batch_diversity_review(sites))
    write(DEMO_ROOT / "docs" / "inspiration-reference-library.md", render_inspiration_reference_library(sites))
    write(DEMO_ROOT / "index.html", render_portfolio_html(sites))
    print(f"Built {len(selected)} demo site(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
