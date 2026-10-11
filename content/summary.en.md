# The router at EKO's service

Getting from the truck's router one dedicated output carrying the PGM, the international sound and the LTC of the three LSMs as audio, without touching the broadcast PGM: how to do it, with which routers, at what cost and within which limits.

## Key points

- **Feasible on most documented trucks, guaranteed nowhere without a test.** Embedding is done output by output: the PGM going to air is not modified.
- **Three practical conditions**: a free, licensed "embedder" output, an input for three analogue LTC signals, and a follow rule if PGM Follow is wanted.
- **LTC conversion**: from €249 incl. VAT to about €1,024 excl. VAT for an external embedder with four analogue inputs (prices seen on 11 October 2026).
- **Analogue input card in the router**: no public price found. The suspicion that it costs more than a digital input is neither confirmed nor refuted. Sirius 800, NVISION 8500, Ultrix, MicroN and .edge have no documented analogue input.
- **To test first**: whether ATC survives on the re-embedded output, what the EVS servers' LTC does away from nominal speed, and the delay of the follow.

## The signal requested

{{diagram:signal}}

The router handles three essences separately:

- video and its ancillary data, which follow the source;
- the international sound, fixed;
- the three LTCs, fixed, carried as ordinary PCM audio channels.

Detail and sources: [report, section 2](report.html#s2).

## Three ways to build it

### Baseband hybrid router

{{diagram:hybrid}}

- **Principle**: a mono route from the audio crosspoint to an embedder output card, 16 channels per output.
- **Families**: Evertz EQX and NEXX, Grass Valley Sirius 800 (AHP modules) and NVISION 8500 Hybrid, Imagine Platinum IP3, Utah UTAH-400 Series 2, Ross Ultrix (Ultrimix).
- **Hard point**: embedder outputs are usually a subset of the outputs, under licence. The question on site is "is there a free embedder destination?".
- **Implementation**: an engineering setup done once, then stored as a salvo or a virtual destination.

### ST 2110 truck

{{diagram:ip}}

- **Principle**: the gateway rebuilds the SDI output from independent receivers. Fixed audio while video follows is a standard breakaway there.
- **Documented shuffler**: Lawo .edge, Grass Valley IQUCP25, Nevion Virtuoso, Sony with the NXLL-AM50 option.
- **Hard point**: the three LTCs must first exist in a 2110-30 flow, and the -40 receiver must follow the video receiver to keep the source's ATC.

### Transparent router and external embedder

{{diagram:transparent}}

- **Principle**: the router cannot embed (Blackmagic Videohub, AJA KUMO). An embedder in front of EKO inserts the three LTCs.
- **Advantage**: the solution is identical in every truck and can ship with the machine.
- **Hard point**: only the AJA 3G-AMA and the Lynx PDM 1383 document the choice of the channels written. For the Blackmagic unit, this needs a bench check.

Detail and sources: [report, section 3](report.html#s3) and [section 5](report.html#s5) for the router tables.

## Following the programme bus

{{diagram:follow}}

- **No function named "PGM Follow"** was found in the public documentation of the control systems.
- **Through control**: rules of the form "if the PGM bus is on source n, route source n", limited to the video and ancillary level. The documented building blocks are the GPIO and crosspoint logic of Lawo VSM and the "Virtual Tally Router" of TSL TallyMan.
- **Inside the vision mixer**: Bus Linking (K-Frame) or Auto Follow (Ross Acuity). Timing is tighter, but an Aux output is a processed output: ancillary pass-through is documented only at Ross.
- **Bus status, not tally**: tally lights several sources during a mix. The rule must read the PGM bus crosspoint.
- **Delay**: no manufacturer publishes a figure. The reasoned budget is one to a few frames.

Detail and sources: [report, sections 3.4 and 3.5](report.html#s3-4) and [section 6](report.html#s6).

## Getting the three LTCs in

| Option | Price seen on 11 October 2026 | Remark |
|---|---|---|
| Free line inputs on the console or a stagebox | 0 | Unverified assumption; risk of audio processing on the path |
| Blackmagic Mini Converter Audio to SDI, 4 inputs | $275 ([Markertek](https://www.markertek.com/product/bmd-convmcauds2/blackmagic-convmcauds2-mini-converter-audio-to-sdi-embedder)); €249 incl. VAT ([Thomann](https://www.thomann.fr/blackmagic_design_mini_converter_audio_to_sdi.htm)) | Channels written not confirmed; 3G-SDI only |
| Lynx Yellobrik PDM 1383, 4 inputs | $885.40 ([Markertek](https://www.markertek.com/product/lnx-pdm-1383/lynx-technik-yellobrik-pdm-1383-analog-audio-embedder-de-embedder)); £760 excl. VAT ([Canford](https://canford.co.uk/LYNX-YELLOBRIK-AUDIO-EMBEDDERS-AND-DE-EMBEDDERS)) | Group selection documented |
| AJA 3G-AMA, 4 inputs | $1,118 ([Markertek](https://www.markertek.com/product/aja-3g-ama/aja-3g-ama-3g-sdi-analog-audio-embedder-disembedder)); €1,023.97 excl. VAT ([Vocas](https://en.vocas.nl/aja-3g-ama-3g-sdi-analog-audio-embed-disembed.html)) | Per-pair selection documented |
| Audinate Dante AVIO, 2 inputs | $229 each ([Markertek](https://www.markertek.com/product/adn-adpdai-au2x0/audinate-adp-dai-au-2x0-dante-avio-analog-input-adapter-with-rj45-and-2-xlr-female-2-channel-version)) | Two units; useful if the truck's Dante already reaches the router |
| Analogue input card in the router | No public price | Documented at Evertz (EMR frame), Utah, Imagine and FOR-A; rarely justified for three signals |

LTC travels safely on a linear 48 kHz PCM channel, provided the path stays unprocessed: no dynamics, no filter, no sample-rate conversion.

Detail and sources: [report, section 4](report.html#s4).

## Within reach of which truck?

| Type of truck | Assessment | Hard point |
|---|---|---|
| Baseband hybrid router | Within reach; most favourable case | A free, licensed embedder output |
| Riedel MediorNet network | Plausible, to be confirmed with Riedel | Mono granularity and ancillary handling not confirmed; neither analogue nor AES3 listed on MicroN, entry through MADI |
| ST 2110 with SDI gateways | Within reach | LTC to be brought into 2110-30; a free gateway output |
| Transparent router (Videohub, KUMO) | Within reach with an external embedder | One more box in EKO's path |
| Software-defined production (GV AMPP) | Not established | No classic router output |

Detail and sources: [report, section 8](report.html#s8).

## What the providers have in their trucks

- **Mediapro**: OB52 (2019) runs a SAM Sirius 830 under Lawo VSM. Router and control are not published for the Spanish UHD units or for Mediapro Belgium.
- **AMP Visual TV**: no classic router, but a decentralised Riedel MediorNet network (68 MicroN on Millenium Signature 12). The control system is not published.
- **EMG / Gravity Media**: Nova 103 and 104 run Grass Valley Sirius 840 under EVS Cerebrum; the diPloy platform is ST 2110.
- **NEP**: Lawo V__matrix IP cores on US, Australian and Belgian trucks; proprietary TFC control in the United States; NEP Belgium Units 14 to 18 under Lawo VSM.
- **France Télévisions**: UM1 and UM2 are hybrid SDI and ST 2110 (Sony XVS, Imagine SNP gateways). Router and control are not published.
- **RTBF**: the 2020 twins are full ST 2110 (Arista, Lawo V__matrix, VSM) and keep 32 baseband outputs.
- **ZDF**: only MP-6, from the HD era, is documented (NVision 8500 under VSM). Nothing was found on the current trucks.
- **Trend**: in continental Europe, baseband (mostly Sirius), MediorNet or hybrid, under Lawo VSM in 19 of the 25 inventory rows where control is named. In the English-speaking sample, 33 rows out of 53 are IP. These counts cover publicised trucks, not the installed base.

Detail and sources, truck by truck: [report, section 7](report.html#s7).

## What to test first

1. **ATC on the re-embedded output.** Route the PGM to the embedder destination, replace channels 14 to 16, check ATC on an analyser, clean switch on then off.
2. **EVS server LTC away from nominal speed.** Slow motion at 33%, jog, reverse, still frame. No public document read describes this behaviour.
3. **Delay of the follow.** Cut, mix, wipe, still store, M/E re-entry.
4. **Audio-versus-video offset.** It must be constant and calibrated once per truck; frame sync is to be disabled on the EKO destination.
5. **LTC path.** Unprocessed, with the same delay on all three channels.

Detail: [report, section 9](report.html#s9). The checklist of questions for the truck's engineer-in-charge is in [section 10](report.html#s10).

## Limits of this research

- **Research interrupted**: the web-search budget ran out part-way. The absences below are absences of research, not findings.
- **ZDF**: a single truck, from the HD era.
- **EVS**: the manuals of the VIA generation could not be opened.
- **Prices**: no public price for router audio cards and licences.
- **Providers not studied**: VRT, Videohouse, RAI, NEP Germany and Nordics, TopVision, the ARD trucks, among others.

The full list is in the [report, section 11](report.html#s11).
