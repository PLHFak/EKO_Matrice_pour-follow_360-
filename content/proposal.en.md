# EKO listens, the truck programs nothing

Installation proposal for the EKO Nano and the EKO Mini: ask the truck only for signals it can already provide, and put the complexity in EKO. The timecode comes from the LSM itself, and the right mic is the one the sound engineer opened during the live broadcast.

## The proposal in brief

- **Nothing to program in the truck, at base level.** EKO asks only for ordinary feeds: a PGM with the international sound, the LSM outputs, the reference. No router rules, no custom embedding, no taking control of any machine.
- **The timecode comes from the LSM, not from the router.** On the EKO Mini, it is read from the SDI output of each play channel. On the EKO Nano, it arrives through the LTC output of each server, on XLR, directly into EKO.
- **The tally says which LSM is on air.** It is the same kind of request as hooking up a multiviewer, far simpler than a follow rule in the router.
- **The right mic is the one the sound engineer chose during the live broadcast.** EKO records the mics pre-fader and logs which faders were open. In the replay, it plays back the same mics, on time.
- **Layers that add up.** On the Mini, the cables alone already give the international sound for every replay. The tally, the console, the LSM protocol and tracking are added one by one, and any of them can be missing without blocking the rest. On the Nano, the tally is part of the base.

## What we ask of the truck

| Request | From whom | What it is for | Level |
|---|---|---|---|
| A PGM feed with the international sound embedded | EIC | Programme picture, international sound | Base |
| EKO Mini: one SDI output from each play channel. EKO Nano: the LTC output of each server, on XLR | EIC, EVS operator | Original timecode of the replayed pictures | Base |
| The truck reference | EIC | EKO clock | Base |
| An SDI return from EKO to the console | Sound engineer (A1) | The EKO sounds | Base |
| The tally, as TSL UMD over IP or as GPI contacts | EIC | Knowing which LSM is on air | Recommended on Mini, base on Nano |
| The pitch mics pre-fader, over MADI | Sound engineer (A1) | Playing back a specific mic | Option |
| The fader state of these mics, or failing that a "pitch effects" sub-group | Sound engineer (A1) | Choosing the right mic | Option |

## EKO Mini: eight connectors, seven inputs and one output

{{diagram:mini}}

- **Connector split**: one PGM, up to six play channels and one output. Blackmagic describes the card as "8 x 3G-SDI mini DIN connections independently configurable as Input or Output", with 16 embedded audio channels per SDI and a reference input ([Blackmagic, DeckLink Quad 2](https://www.blackmagicdesign.com/products/decklink/techspecs/W-DLK-30)).
- **One setting to make**: the card ships configured as four input and output pairs. The eight connectors become independent once each pair is switched from the "SDI 1 & SDI 2" mode to the "SDI 1" mode (and likewise for the other three pairs), in Desktop Video Setup or through the SDK's half-duplex profile ([Blackmagic, developer FAQ](https://www.blackmagicdesign.com/developer/support/faq/desktop-video-developer-support-faqs); [Blackmagic, SDK profiles](https://sdk-doc.blackmagicdesign.com/decklink-sdk/HighLevel/profiles.html)).
- **Timecode**: each HD output of an EVS server can insert timecode as HANC LTC and HANC VITC; it is a per-channel setting, documented in the XSnano 12.02 manual, from the same software generation as the XT3. The DeckLink SDK returns the RP188 timecode of each captured frame, in HD only on this card ([EVS, XSnano Configuration Manual 12.02](https://www.manualslib.com/manual/1421853/Evs-Xsnano.html?page=126); [Blackmagic, timecode in the SDK](https://sdk-doc.blackmagicdesign.com/decklink-sdk/HighLevel/timecode.html)).
- **LSM on air**: the tally if it is available. Otherwise EKO compares the PGM picture with those of the play channels it receives. When both exist, they cross-check each other.
- **Replayed camera**: for a clip, it is the letter in the ID (111A, 111B) ([EVS, LSM-VIA User Manual 1.4](https://www.manualslib.com/manual/2596542/Evs-Lsm-Via.html?page=73)). The on-screen display (OSD) of the monitoring output shows the clip ID; for a live train, only the name of the record channel, as free text, is documented ([EVS, Multicam Operating Manual 11.00](https://www.manualsdir.com/manuals/254262/evs-multicamlsm-version-1100-operating-manual.html?page=21)). Reading it through the LinX API is an assumption to be checked with EVS.
- **A single output per play channel**: the monitoring output, wired today, carries the OSD, so the image comparison must avoid the OSD lines. Whether HANC timecode is present on that output remains to be confirmed; if it is missing, the clean output must be used and reading the OSD abandoned.
- **Output**: a single SDI carries the 16 channels to the console.

For the Mini, this is today's wiring, simplified: the PGM stays a standard PGM, and the tally replaces the follow rule in the router.

## EKO Nano: one input, one output, two connections

{{diagram:nano}}

- **SDI**: the PGM with the international sound as input, the EKO sounds as output.
- **LSM timecode**: the LTC output of each server, on XLR, into a small four-input USB audio interface, for example a Behringer UMC404HD at €98 incl. VAT (Thomann Belgium, seen on 12 October 2026). EKO decodes the LTC itself ([Thomann](https://www.thomann.de/be/behringer_umc404hd.htm); [libltc](https://github.com/x42/libltc)).
- **LSM on air**: the tally is required, as TSL UMD over IP or as GPI contacts.
- **No conversion in the truck**: the analogue conversion is done in EKO. The router has nothing to embed.

The limits of the Nano:

- **One LTC per server.** The LTC output of an XT3 is single, on XLR, and corresponds to PGM1. A server that puts PGM1 and PGM2 on air therefore has only one LTC ([EVS, XT3 brochure](https://cvp.com/pdf/evs_xt3_brch.pdf); [EVS, XT3 Technical Reference 16.6](https://www.manualslib.com/manual/3607735/Evs-Xt-3.html?page=60)).
- **Still frame.** LTC cannot, in principle, be read when stopped: EKO holds the last timecode read.
- **No LSM pictures.** The camera letter can only come from the protocol, and a clip recorded from the PGM can only be checked against the PGM picture.

Variant when the truck can do it: the router's PGM Follow output, already described in the installation note. The timecode then arrives in the SDI, without XLR.

## The sound engineer's three sounds

| Sound requested | How EKO finds it | What it needs |
|---|---|---|
| International sound | The recorded international sound, played back at the picture's original time | The base |
| Sound of the camera on screen | The mic associated with the replayed camera, via a camera-to-mic table entered once | The mics over MADI and the camera letter |
| Sound of the action | The mics the sound engineer had open at that moment, taken pre-fader | The mics over MADI and the fader state |

As an option, the mic closest to the ball can be deduced from the ball position and the mic plan. This requires a tracking feed, and therefore an agreement with the league, or image analysis done by EKO.

### The four mic bricks

Each brick picks a mic; its name says who decides. "Follow" means automatic, "Select" means human.

| Brick | Who decides the mic | Mode |
|---|---|---|
| **CAM FOLLOW** | The replayed camera, by its letter A, B, C or D | Automatic |
| **MIX FOLLOW** | The faders the sound engineer opened during the live broadcast, played back early in the replay | Automatic |
| **BALL FOLLOW** | The position of the ball or the action, from tracking or image analysis | Automatic |
| **MIC SELECT** | The operator | Human |

EKO output tracks: EKO INT · CAM FOLLOW · MIX FOLLOW · BALL FOLLOW · MIC SELECT · EKO CLIP · BOOST · MONITOR 1–6.

These sounds already exist as separate elements in sports production. At Euro 2020, the objects of the immersive mix were the commentary, the "close ball" effects and the "audio follow video" effects ([SVG Europe, 8 July 2021](https://www.svgeurope.org/blog/headlines/roar-of-the-crowd-telegenic-on-running-a-sound-operation-for-uefa-at-euro-2020/)).

### Replaying the sound engineer's decision

{{diagram:fader}}

The problem as posed: EKO records all the mics, but does not know which one to put on air. My answer: someone already decided that during the live broadcast.

- **During the live broadcast**, the sound engineer follows the action and opens the closest mic, often slightly late.
- **EKO logs that choice**: which fader was open, and at what time.
- **In the replay**, EKO plays back that mic from its pre-fader recording. The mic that opened late in the live broadcast is on time in the replay.

This route avoids two obstacles:

- **Mic positions**: none of the console documentation read contains any mic position. Only an add-on such as Lawo KICK knows it.
- **Ball tracking**: it exists, but under contract with the league. In the Bundesliga, TRACAB produces the feed and Sportec Solutions, a DFL subsidiary, distributes it ([Live-Production](https://www.live-production.tv/news/sports/dfl-and-chyronhego-sign-new-tracab%E2%84%A2-contract-bundesliga-and-bundesliga-2.html)). No source consulted shows an OB provider receiving it by default.

Three ways to know the faders, from the simplest to the most detailed:

1. **A post-fader "pitch effects" sub-group.** One more feed to EKO. EKO receives the sound engineer's mix, without the crowd or the commentary.
2. **Each mic pre-fader and post-fader.** Calrec consoles provide up to four direct outputs per channel, each selectable pre- or post-fader. EKO deduces whether the fader is open by comparing the two. This is an inference to be checked, particularly when a group or a VCA controls the channels ([Calrec, Artemis Operator's Manual](https://www.manualslib.com/manual/1341453/Calrec-Artemis.html?page=115)).
3. **The console protocol.** Calrec's CSCP provides, for up to 192 faders, the position, the Cut or On state and the channel name, over TCP/IP ([Calrec, Apollo Installation Manual](https://www.manualslib.com/manual/1314128/Calrec-Apollo.html?page=62)). Lawo announces control of all channel parameters over Ember+; channel names are attested there, but fader position and mute are not detailed in any public document ([Lawo, mc²56](https://lawo.com/products/mc%C2%B256-audio-production-console/)).

The console can also work for EKO in the other direction. Its "audio follow video" functions open a channel on a tally: 256 Autofaders on a Calrec Artemis, 128 events on a Lawo mc²96. Triggered by an LSM tally, they would open the EKO channel by themselves on every replay. No source describes this set-up: it needs to be tried ([Calrec, Artemis Operator's Manual](https://www.manualslib.com/manual/1341453/Calrec-Artemis.html?page=90); [Lawo, mc²96 Audio Follow Video](https://docs.lawo.com/audio-production-mc-mixing-consoles/mc96/mc96-operation/mc96-channel-operations/mc96-audio-follow-video)).

### Getting the mics in

- **The mic plan**: the historical baseline is 12 mics around the pitch; Sportcast went to 17 in the Bundesliga ([SVG Europe, 26 March 2018](https://www.svgeurope.org/blog/headlines/sky-sport-summit-in-cooperation-with-svg-europe-the-future-of-audio-in-sports/); [Sennheiser, 16 October 2025](https://newsroom.sennheiser.com/broadcast-production-partner-topvision-ensures-authenticity-in-football-broadcasting)).
- **Transport**: a MADI stream of direct outputs, which consoles can route to an external recorder ([Lawo, mc²96 Direct Out](https://docs.lawo.com/audio-production-mc-mixing-consoles/mc96/mc96-operation/mc96-channel-operations/mc96-direct-out)).
- **In EKO**: a 64-channel USB MADI interface, for example the RME MADIface USB at €717 incl. VAT (Thomann Austria, seen on 12 October 2026) ([Thomann](https://www.thomann.at/rme_madiface_usb_reviews.htm?rating=5)).

## What I rule out at base level, and why

| Route | Why it fails the "simple to install" criterion |
|---|---|
| LSM LTC embedded by the router | Three analogue conversions, a free embedder output and a custom channel map, to be redone in every truck |
| PGM Follow through rules in the router | No function of that name was found in the public documentation of control systems; it is an engineering job per truck. It remains a variant for the Nano |
| LSM timecode carried in the PGM by the vision mixer | Passing ancillary data through a vision mixer output is documented, in the manuals consulted, only by Ross |
| The LSM protocol as the timecode source | A serial link per channel with a licence, or the LinX API on the truck network, whose terms are not public, for information already present in the SDI. I keep it for the camera letter only |
| Ball tracking | Depends on a league contract. I keep it as an option, along the lines of Lawo KICK |

Lawo KICK makes exactly this choice of the closest mic from TRACAB tracking; the Bundesliga adopted it for the 2017/18 season. Salsa Sound MIXaiR does it from the mic signals alone ([SVG, 20 December 2018](https://www.sportsvideo.org/2018/12/20/lawo-develops-hockey-version-of-kick-action-following-audio-system/); [SVG Europe, 2 November 2017](https://www.svgeurope.org/blog/headlines/bundesliga-is-worlds-first-league-to-use-automated-audio-mixing/); [SVC Online, 3 November 2021](https://www.svconline.com/the-wire/salsa-sound-launches-software-defined-and-cloud-compatible-version-of-ai-based-audio-mixing-engine-mixair-2-0)).

## What this requires of EKO

1. **Mini on eight channels**: configurable input and output split, from 4 + 4 to 7 + 1.
2. **Tally listening**: TSL UMD v3.1 and v5, over UDP and TCP, with an index table and bit polarity configurable per truck. A GPI input serves as fallback ([TSL, protocol specification](https://tslproducts.com/wp-content/uploads/TSL-UMD-protocol.pdf)).
3. **Image comparison** between the PGM and the play channels received, to cross-check the tally and replace it when it is missing.
4. **Nano**: LTC input through a USB audio interface.
5. **Multitrack input** over MADI.
6. **Timestamped fader log**: CSCP for the documented UHD trucks of AMP Visual TV (Millenium Signature 12, Millenium 3, 4 and 6), which run on Calrec; the older trucks are on Studer Vista ([AMP Visual TV, Millenium](https://www.ampvisualtv.tv/en/our-production-resources/mobile-resources/132-millenium.html)).
7. **Camera letter**: reading the LSM OSD, then the LinX API if EVS confirms it.

## To validate before development

1. **On a real LSM**: the timecode insertion setting and how it holds up in slow motion and when stopped. The "No" and "TC 0" values would break the follow ([EVS, XSnano Configuration Manual 12.02](https://www.manualslib.com/manual/1421853/Evs-Xsnano.html?page=126)).
2. **The monitoring output**: HANC timecode present or not; an OSD that the operator can switch off with the F5 key, and whose full layout is not documented.
3. **The Quad 2 card**: reading RP188 timecode on seven inputs at once, particularly in 1080p50.
4. **AMP on EVS servers**: AMP does not appear in any EVS document found. The Cerebrum protocol list (V2.01, May 2021) gives AMP for the Grass Valley K2 and the LinX API for the XT and XT-VIA. To be checked on a server before any AMP development ([EVS, Cerebrum protocol list](https://evs.com/sites/default/files/2021-05/Cerebrum%20protocol%20list%20V2.01%20%28May21%29.pdf)).
5. **The tally**: TSL output is documented for Ross vision mixers and for TSL TallyMan, listed without a public procedure for EVS Cerebrum, and not confirmed for Lawo VSM. Bit polarity varies from one manufacturer to another, and behaviour during a dissolve is not documented.
6. **The console**: the sound engineer's agreement to having the faders read. No read-only mode is documented, and Lawo drops external Ember+ connections on every production load ([Lawo, mc² 12.0.0 release notes](https://docs.lawo.com/audio-production-mc-mixing-consoles/audio-production-software-versions/mc-release-notes-12-0-0)).
7. **The servers' LTC**, for the Nano: its behaviour away from nominal speed is not described in any public document, and the existence of an analogue LTC output on the XT-VIA is not confirmed.
8. **The DeckLink SDI Micro**: one fixed input and one fixed output according to resellers; the manufacturer's data sheet could not be read, and the number of embedded audio channels is not confirmed.

## Proposed test order

1. **Mini, cables only**: one PGM and the play channel outputs, on one match.
2. **Mini with tally**: compare the tally against the image comparison.
3. **Nano**: LTC on XLR and tally.
4. **Mics over MADI** and the "pitch effects" sub-group.
5. **Fader log** on a Calrec console.
6. **Camera letter** and the camera-to-mic table.
