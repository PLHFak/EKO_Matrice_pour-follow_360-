"""Inline SVG diagrams for the EKO router dossier (French and English).

Colours come from CSS custom properties defined in assets/style.css, so the
diagrams follow the light and dark themes. Arrowhead markers are defined once
per page (see MARKERS) and referenced by every diagram.
"""
from html import escape as esc

MARKERS = (
    '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
    + "".join(
        f'<marker id="ah-{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path class="ah {c}" d="M2 1L8 5L2 9"/></marker>'
        for c in ("v", "a", "l", "c", "n")
    )
    + "</defs></svg>"
)


def box(x, y, w, h, title, sub=None, sub2=None, cls=""):
    lines = [l for l in (title, sub, sub2) if l]
    cy = y + h / 2
    if len(lines) == 1:
        ys = [cy]
    elif len(lines) == 2:
        ys = [cy - 10, cy + 10]
    else:
        ys = [cy - 20, cy, cy + 19]
    out = f'<rect class="bx {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
    for i, (l, yy) in enumerate(zip(lines, ys)):
        out += f'<text class="{"t" if i == 0 else "s"} {cls}" x="{x + w / 2}" y="{yy}">{esc(l)}</text>'
    return out


def arrow(d, cls):
    return f'<path class="ln {cls}" d="{d}" marker-end="url(#ah-{cls})"/>'


def label(x, y, text, anchor="middle"):
    return f'<text class="s lb" x="{x}" y="{y}" style="text-anchor:{anchor}">{esc(text)}</text>'


def legend(y, items):
    out, x = "", 20
    for cls, text in items:
        out += f'<path class="ln {cls}" d="M{x} {y} H{x + 28}"/>'
        out += f'<text class="s lb" x="{x + 36}" y="{y}" style="text-anchor:start">{esc(text)}</text>'
        x += 36 + int(len(text) * 6.6) + 28
    return out


def wrap(w, h, title, desc, body):
    return (
        f'<svg class="dg" viewBox="0 0 {w} {h}" role="img">'
        f"<title>{esc(title)}</title><desc>{esc(desc)}</desc>{body}</svg>"
    )


T = {
    "fr": {
        "video": "Vidéo et ancillaire", "audio": "Audio", "ltc": "LTC", "ctrl": "Contrôle",
        "eko": "EKO", "sdi_src": "Sources SDI", "sdi_src_s": "caméras, LSM",
        "is": "Son international", "ltc3": "LTC des LSM 1, 2, 3", "ltc3_s": "sorties analogiques",
        "bcast": "diffusion",
    },
    "en": {
        "video": "Video and ancillary", "audio": "Audio", "ltc": "LTC", "ctrl": "Control",
        "eko": "EKO", "sdi_src": "SDI sources", "sdi_src_s": "cameras, LSM",
        "is": "International sound", "ltc3": "LTC of LSM 1, 2, 3", "ltc3_s": "analogue outputs",
        "bcast": "broadcast",
    },
}


def d_signal(lang):
    L = {
        "fr": dict(a="Vidéo et ancillaire (ATC)", a_s="suit la source à l'antenne",
                   b="Son international", b_s="fixe",
                   c="LTC des LSM 1, 2, 3", c_s="fixes, transportés en audio",
                   d="Destination dédiée de la matrice", d_s="composée sur cette sortie seulement",
                   strip="Les 16 canaux audio embedded de cette sortie",
                   l1="son inter", l2="libres ou conservés", l3="LTC 1 · 2 · 3",
                   title="Le signal demandé par EKO",
                   desc="Une destination dédiée de la matrice réunit la vidéo et son ancillaire, le son international et les LTC des trois LSM sur les canaux 14, 15 et 16."),
        "en": dict(a="Video and ancillary (ATC)", a_s="follows the on-air source",
                   b="International sound", b_s="fixed",
                   c="LTC of LSM 1, 2, 3", c_s="fixed, carried as audio",
                   d="Dedicated router destination", d_s="composed on this output only",
                   strip="The 16 embedded audio channels of this output",
                   l1="int. sound", l2="free or passed through", l3="LTC 1 · 2 · 3",
                   title="The signal EKO asks for",
                   desc="One dedicated router destination combines video and its ancillary data, the international sound and the LTC of the three LSMs on channels 14, 15 and 16."),
    }[lang]
    b = box(20, 20, 250, 54, L["a"], L["a_s"], cls="v")
    b += box(20, 92, 250, 54, L["b"], L["b_s"], cls="a")
    b += box(20, 164, 250, 54, L["c"], L["c_s"], cls="l")
    b += box(350, 92, 260, 54, L["d"], L["d_s"])
    b += box(690, 92, 56, 54, "EKO", cls="eko")
    b += arrow("M270 47 H310 V104 H346", "v")
    b += arrow("M270 119 H346", "a")
    b += arrow("M270 191 H310 V134 H346", "l")
    b += arrow("M610 119 H686", "n")
    b += label(60, 250, L["strip"], "start")
    for i in range(16):
        n = i + 1
        cls = "a" if n <= 2 else ("l" if n >= 14 else "")
        x = 60 + i * 40
        b += f'<rect class="bx cell {cls}" x="{x}" y="264" width="40" height="30" rx="3"/>'
        b += f'<text class="s {cls}" x="{x + 20}" y="279">{n}</text>'
    b += label(100, 310, L["l1"])
    b += label(360, 310, L["l2"])
    b += label(640, 310, L["l3"])
    return wrap(766, 326, L["title"], L["desc"], b)


def d_hybrid(lang):
    t = T[lang]
    L = {
        "fr": dict(xv="Crosspoint vidéo", xv_s="vidéo et ancillaire",
                   os="Sortie standard", os_s="PGM de diffusion, intact",
                   oe="Sortie embedder", oe_s="16 canaux mono",
                   xa="Crosspoint audio TDM", xa_s="routage au niveau mono",
                   is_s="console, en MADI", cv="Conversion A/N", cv_s="vers MADI ou AES",
                   title="Matrice hybride baseband",
                   desc="Le crosspoint audio route le son international et les trois LTC, convertis en numérique, vers une carte de sortie embedder. Le PGM de diffusion sort par une sortie standard, sans traitement."),
        "en": dict(xv="Video crosspoint", xv_s="video and ancillary",
                   os="Standard output", os_s="broadcast PGM, untouched",
                   oe="Embedder output", oe_s="16 mono channels",
                   xa="Audio TDM crosspoint", xa_s="mono-level routing",
                   is_s="console, as MADI", cv="A/D conversion", cv_s="to MADI or AES",
                   title="Baseband hybrid router",
                   desc="The audio crosspoint routes the international sound and the three LTCs, once digitised, to an embedder output card. The broadcast PGM leaves through a standard output, unprocessed."),
    }[lang]
    b = box(20, 20, 170, 54, t["sdi_src"], t["sdi_src_s"], cls="v")
    b += box(400, 20, 180, 54, L["xv"], L["xv_s"])
    b += box(600, 20, 170, 54, L["os"], L["os_s"])
    b += box(600, 120, 170, 54, L["oe"], L["oe_s"])
    b += box(796, 120, 56, 54, "EKO", cls="eko")
    b += box(400, 220, 180, 54, L["xa"], L["xa_s"])
    b += box(20, 184, 170, 54, t["is"], L["is_s"], cls="a")
    b += box(20, 262, 170, 54, t["ltc3"], t["ltc3_s"], cls="l")
    b += box(220, 262, 150, 54, L["cv"], L["cv_s"])
    b += arrow("M190 47 H396", "v")
    b += arrow("M580 47 H596", "v")
    b += arrow("M490 74 V147 H596", "v")
    b += arrow("M770 147 H792", "n")
    b += arrow("M770 47 H852", "v")
    b += label(812, 32, t["bcast"])
    b += arrow("M190 211 H300 V238 H396", "a")
    b += arrow("M190 289 H216", "l")
    b += arrow("M370 289 H385 V256 H396", "l")
    b += arrow("M580 247 H685 V178", "a")
    b += legend(346, [("v", t["video"]), ("a", t["audio"]), ("l", t["ltc"])])
    return wrap(860, 364, L["title"], L["desc"], b)


def d_ip(lang):
    t = T[lang]
    L = {
        "fr": dict(t1="Source à l'antenne", t1_s="flux -20 vidéo et -40 ANC", t2_s="flux -30",
                   t3_s="entrées ligne, puis flux -30",
                   gw="Passerelle ST 2110 vers SDI", gw_s="récepteurs -20, -30 et -40", gw_s2="shuffler 16 canaux mono",
                   ct="Système de contrôle", ct_s="repointe -20 et -40 ensemble",
                   title="Car ST 2110",
                   desc="La passerelle reconstruit la sortie SDI à partir de récepteurs indépendants. Le contrôle repointe la vidéo et l'ancillaire ; le shuffler audio reste fixe sur le son international et les trois LTC."),
        "en": dict(t1="On-air source", t1_s="-20 video and -40 ANC flows", t2_s="-30 flow",
                   t3_s="line inputs, then -30 flow",
                   gw="ST 2110 to SDI gateway", gw_s="-20, -30 and -40 receivers", gw_s2="16-channel mono shuffler",
                   ct="Control system", ct_s="re-points -20 and -40 together",
                   title="ST 2110 truck",
                   desc="The gateway rebuilds the SDI output from independent receivers. Control re-points video and ancillary; the audio shuffler stays fixed on the international sound and the three LTCs."),
    }[lang]
    b = box(20, 20, 230, 54, L["t1"], L["t1_s"], cls="v")
    b += box(20, 114, 230, 54, t["is"], L["t2_s"], cls="a")
    b += box(20, 208, 230, 54, t["ltc3"], L["t3_s"], cls="l")
    b += box(340, 10, 280, 54, L["ct"], L["ct_s"])
    b += box(340, 106, 280, 84, L["gw"], L["gw_s"], L["gw_s2"])
    b += box(710, 121, 56, 54, "EKO", cls="eko")
    b += arrow("M250 47 H295 V126 H336", "v")
    b += arrow("M250 141 H280 V148 H336", "a")
    b += arrow("M250 235 H295 V170 H336", "l")
    b += arrow("M480 64 V102", "c")
    b += arrow("M620 148 H706", "n")
    b += legend(292, [("v", t["video"]), ("a", t["audio"]), ("l", t["ltc"]), ("c", t["ctrl"])])
    return wrap(786, 310, L["title"], L["desc"], b)


def d_transparent(lang):
    t = T[lang]
    L = {
        "fr": dict(mx="Matrice transparente", mx_s="Videohub, KUMO", pgm="PGM de diffusion, intact",
                   em="Embedder externe", em_s="4 entrées analogiques", ded="sortie dédiée",
                   title="Matrice transparente et embedder externe",
                   desc="La matrice route sans traitement. Un embedder externe, placé entre la sortie dédiée et EKO, insère les trois LTC. Le PGM de diffusion n'est pas concerné."),
        "en": dict(mx="Transparent router", mx_s="Videohub, KUMO", pgm="broadcast PGM, untouched",
                   em="External embedder", em_s="4 analogue inputs", ded="dedicated output",
                   title="Transparent router and external embedder",
                   desc="The router passes signals unprocessed. An external embedder between the dedicated output and EKO inserts the three LTCs. The broadcast PGM is not involved."),
    }[lang]
    b = box(20, 20, 170, 54, t["sdi_src"], t["sdi_src_s"], cls="v")
    b += box(250, 20, 200, 54, L["mx"], L["mx_s"])
    b += box(20, 130, 170, 54, t["ltc3"], t["ltc3_s"], cls="l")
    b += box(520, 130, 200, 54, L["em"], L["em_s"])
    b += box(790, 130, 56, 54, "EKO", cls="eko")
    b += arrow("M190 47 H246", "v")
    b += arrow("M450 47 H852", "v")
    b += label(650, 33, L["pgm"])
    b += arrow("M350 74 V104 H620 V126", "v")
    b += label(485, 92, L["ded"])
    b += arrow("M190 157 H516", "l")
    b += arrow("M720 157 H786", "n")
    b += legend(214, [("v", t["video"]), ("l", t["ltc"])])
    return wrap(860, 232, L["title"], L["desc"], b)


def d_follow(lang):
    t = T[lang]
    L = {
        "fr": dict(vm="Mélangeur", vm_s="état du bus PGM",
                   cs="Système de contrôle", cs_s="si bus PGM = source n,", cs_s2="router la source n",
                   rt="Matrice", rt_s="niveau vidéo et ANC seul",
                   dst="Destination « EKO »", fx="Audio de la destination : fixe",
                   title="Suivi du bus programme par le système de contrôle",
                   desc="Le système de contrôle lit l'état du bus PGM du mélangeur et commande la matrice sur le seul niveau vidéo et ancillaire. L'audio de la destination reste fixe."),
        "en": dict(vm="Vision mixer", vm_s="PGM bus status",
                   cs="Control system", cs_s="if PGM bus = source n,", cs_s2="route source n",
                   rt="Router", rt_s="video and ANC level only",
                   dst="“EKO” destination", fx="Destination audio: fixed",
                   title="Programme-bus follow by the control system",
                   desc="The control system reads the vision mixer's PGM bus status and drives the router on the video and ancillary level only. The destination's audio stays fixed."),
    }[lang]
    b = box(20, 26, 220, 64, L["vm"], L["vm_s"])
    b += box(320, 20, 240, 76, L["cs"], L["cs_s"], L["cs_s2"])
    b += box(640, 26, 200, 64, L["rt"], L["rt_s"])
    b += box(640, 140, 200, 46, L["dst"], cls="eko")
    b += box(320, 140, 240, 46, L["fx"], cls="a")
    b += arrow("M240 58 H316", "c")
    b += arrow("M560 58 H636", "c")
    b += arrow("M740 90 V136", "v")
    b += arrow("M560 163 H636", "a")
    b += legend(216, [("c", t["ctrl"]), ("v", t["video"]), ("a", t["audio"])])
    return wrap(860, 234, L["title"], L["desc"], b)


CAPTIONS = {
    "fr": {
        "signal": "Une destination, trois essences indépendantes : la vidéo suit, le son international et les LTC restent fixes.",
        "hybrid": "Matrice hybride : le composite est fabriqué sur une carte de sortie embedder ; la sortie de diffusion n'est pas traitée.",
        "ip": "ST 2110 : la sortie SDI est reconstruite dans la passerelle ; l'audio fixe y est un breakaway standard.",
        "transparent": "Matrice transparente : un embedder externe devant EKO insère les trois LTC.",
        "follow": "PGM Follow : des règles lisent l'état du bus PGM et ne commutent que le niveau vidéo et ancillaire.",
    },
    "en": {
        "signal": "One destination, three independent essences: video follows, international sound and LTC stay fixed.",
        "hybrid": "Hybrid router: the composite is built on an embedder output card; the broadcast output is unprocessed.",
        "ip": "ST 2110: the SDI output is rebuilt in the gateway; fixed audio is a standard breakaway there.",
        "transparent": "Transparent router: an external embedder in front of EKO inserts the three LTCs.",
        "follow": "PGM Follow: rules read the PGM bus status and switch the video and ancillary level only.",
    },
}

DIAGRAMS = {
    "signal": d_signal,
    "hybrid": d_hybrid,
    "ip": d_ip,
    "transparent": d_transparent,
    "follow": d_follow,
}


def figure(name, lang):
    return (
        f'<figure class="dg-fig">{DIAGRAMS[name](lang)}'
        f"<figcaption>{esc(CAPTIONS[lang][name])}</figcaption></figure>"
    )
