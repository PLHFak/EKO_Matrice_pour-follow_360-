# La matrice au service d'EKO

Recevoir de la matrice du car une sortie dédiée portant le PGM, le son international et le LTC des trois LSM en audio, sans toucher au PGM de diffusion : comment le faire, avec quelles matrices, à quel coût et avec quelles limites.

## L'essentiel

- **Faisable sur la plupart des cars documentés, garanti nulle part sans essai.** L'embedding se fait sortie par sortie : le PGM qui part à l'antenne n'est pas modifié.
- **Trois conditions pratiques** : une sortie « embedder » libre et licenciée, une entrée pour trois LTC analogiques, et une règle de suivi si l'on veut le PGM Follow.
- **Conversion du LTC** : de 249 € TTC à environ 1 024 € HT pour un embedder externe à quatre entrées analogiques (prix vus le 11 octobre 2026).
- **Carte analogique de matrice** : aucun prix public trouvé. Le soupçon d'un surcoût par rapport à une entrée numérique n'est ni confirmé ni réfuté. Sirius 800, NVISION 8500, Ultrix, MicroN et .edge n'ont pas d'entrée analogique documentée.
- **À tester avant tout** : la tenue de l'ATC sur la sortie ré-embeddée, le LTC des serveurs EVS hors vitesse nominale, et le retard du suivi.

## Le signal demandé

{{diagram:signal}}

La matrice traite trois essences séparément :

- la vidéo et son ancillaire, qui suivent la source ;
- le son international, fixe ;
- les trois LTC, fixes, transportés comme des canaux audio PCM ordinaires.

Détail et sources : [rapport, section 2](rapport.html#s2).

## Trois façons de le construire

### Matrice hybride baseband

{{diagram:hybrid}}

- **Principe** : une route mono du crosspoint audio vers une carte de sortie embedder, 16 canaux par sortie.
- **Familles** : Evertz EQX et NEXX, Grass Valley Sirius 800 (modules AHP) et NVISION 8500 Hybrid, Imagine Platinum IP3, Utah UTAH-400 Series 2, Ross Ultrix (Ultrimix).
- **Point dur** : les sorties embedder sont le plus souvent un sous-ensemble des sorties, sous licence. La question sur site est « reste-t-il une destination embedder libre ? ».
- **Mise en œuvre** : un réglage d'ingénierie fait une fois, puis mémorisé en salvo ou en destination virtuelle.

### Car ST 2110

{{diagram:ip}}

- **Principe** : la passerelle reconstruit la sortie SDI à partir de récepteurs indépendants. L'audio fixe pendant que la vidéo suit y est un breakaway standard.
- **Shuffler documenté** : Lawo .edge, Grass Valley IQUCP25, Nevion Virtuoso, Sony avec l'option NXLL-AM50.
- **Point dur** : les trois LTC doivent d'abord exister dans un flux 2110-30, et le récepteur -40 doit suivre le récepteur vidéo pour garder l'ATC de la source.

### Matrice transparente et embedder externe

{{diagram:transparent}}

- **Principe** : la matrice ne sait pas embedder (Blackmagic Videohub, AJA KUMO). Un embedder placé devant EKO insère les trois LTC.
- **Avantage** : la solution est identique dans tous les cars et peut être livrée avec la machine.
- **Point dur** : seuls l'AJA 3G-AMA et le Lynx PDM 1383 documentent le choix des canaux écrits. Pour le Blackmagic, c'est à valider sur table.

Détail et sources : [rapport, section 3](rapport.html#s3) et [section 5](rapport.html#s5) pour le tableau des matrices.

## Faire suivre le bus programme

{{diagram:follow}}

- **Aucune fonction nommée « PGM Follow »** n'a été trouvée dans la documentation publique des systèmes de contrôle.
- **Par le contrôle** : des règles « si le bus PGM est sur la source n, router la source n », limitées au niveau vidéo et ancillaire. Les briques documentées sont la logique GPIO et crosspoints de Lawo VSM et le « Virtual Tally Router » de TSL TallyMan.
- **Dans le mélangeur** : Bus Linking (K-Frame) ou Auto Follow (Ross Acuity). Le timing est plus serré, mais une sortie Aux est une sortie traitée : le passage de l'ancillaire n'est documenté que chez Ross.
- **État de bus, pas tally** : le tally allume plusieurs sources pendant un mix. La règle doit lire le crosspoint du bus PGM.
- **Retard** : aucun constructeur ne publie de chiffre. Le budget raisonné est d'une à quelques images.

Détail et sources : [rapport, sections 3.4 et 3.5](rapport.html#s3-4) et [section 6](rapport.html#s6).

## Faire entrer les trois LTC

| Option | Prix relevé le 11 octobre 2026 | Remarque |
|---|---|---|
| Entrées ligne libres de la console ou d'une stagebox | 0 | Hypothèse non vérifiée ; risque de traitement audio sur le chemin |
| Blackmagic Mini Converter Audio to SDI, 4 entrées | 275 $ ([Markertek](https://www.markertek.com/product/bmd-convmcauds2/blackmagic-convmcauds2-mini-converter-audio-to-sdi-embedder)) ; 249 € TTC ([Thomann](https://www.thomann.fr/blackmagic_design_mini_converter_audio_to_sdi.htm)) | Canaux écrits non confirmés ; 3G-SDI seulement |
| Lynx Yellobrik PDM 1383, 4 entrées | 885,40 $ ([Markertek](https://www.markertek.com/product/lnx-pdm-1383/lynx-technik-yellobrik-pdm-1383-analog-audio-embedder-de-embedder)) ; 760 £ HT ([Canford](https://canford.co.uk/LYNX-YELLOBRIK-AUDIO-EMBEDDERS-AND-DE-EMBEDDERS)) | Choix du groupe documenté |
| AJA 3G-AMA, 4 entrées | 1 118 $ ([Markertek](https://www.markertek.com/product/aja-3g-ama/aja-3g-ama-3g-sdi-analog-audio-embedder-disembedder)) ; 1 023,97 € HT ([Vocas](https://en.vocas.nl/aja-3g-ama-3g-sdi-analog-audio-embed-disembed.html)) | Choix par paire documenté |
| Audinate Dante AVIO, 2 entrées | 229 $ pièce ([Markertek](https://www.markertek.com/product/adn-adpdai-au2x0/audinate-adp-dai-au-2x0-dante-avio-analog-input-adapter-with-rj45-and-2-xlr-female-2-channel-version)) | Deux unités ; utile si le Dante du car rejoint déjà la matrice |
| Carte d'entrée analogique de matrice | Aucun prix public | Documentée chez Evertz (châssis EMR), Utah, Imagine et FOR-A ; rarement justifiée pour trois signaux |

Le LTC passe sans dommage sur un canal PCM linéaire à 48 kHz, à condition que le chemin reste sans traitement : ni dynamique, ni filtre, ni conversion de fréquence d'échantillonnage.

Détail et sources : [rapport, section 4](rapport.html#s4).

## À la portée de quel car ?

| Type de car | Appréciation | Point dur |
|---|---|---|
| Matrice hybride baseband | À portée ; cas le plus favorable | Une sortie embedder libre et licenciée |
| Réseau Riedel MediorNet | Plausible, à confirmer avec Riedel | Granularité mono et ancillaire non confirmés ; ni analogique ni AES3 listés sur MicroN, entrée par MADI |
| ST 2110 avec passerelles SDI | À portée | LTC à amener en 2110-30 ; une sortie de passerelle libre |
| Matrice transparente (Videohub, KUMO) | À portée avec un embedder externe | Un boîtier de plus dans le chemin d'EKO |
| Production software-defined (GV AMPP) | Non établi | Pas de sortie de matrice classique |

Détail et sources : [rapport, section 8](rapport.html#s8).

## Ce que les prestataires ont dans leurs cars

- **Mediapro** : l'OB52 (2019) est en SAM Sirius 830 sous Lawo VSM. Matrice et contrôle ne sont pas publiés pour les unités UHD espagnoles ni pour Mediapro Belgium.
- **AMP Visual TV** : pas de matrice classique, mais un réseau décentralisé Riedel MediorNet (68 MicroN sur le Millenium Signature 12). Le système de contrôle n'est pas publié.
- **EMG / Gravity Media** : Nova 103 et 104 en Grass Valley Sirius 840 sous EVS Cerebrum ; la plate-forme diPloy est en ST 2110.
- **NEP** : cœurs IP Lawo V__matrix sur des cars américains, australiens et belges ; contrôle propriétaire TFC aux États-Unis ; Units 14 à 18 de NEP Belgium sous Lawo VSM.
- **France Télévisions** : UM1 et UM2 sont hybrides SDI et ST 2110 (Sony XVS, passerelles Imagine SNP). Matrice et contrôle ne sont pas publiés.
- **RTBF** : les jumeaux de 2020 sont en ST 2110 complet (Arista, Lawo V__matrix, VSM) et gardent 32 sorties baseband.
- **ZDF** : seul le MP-6, de l'ère HD, est documenté (NVision 8500 sous VSM). Rien n'a été trouvé sur les cars actuels.
- **Tendance** : en Europe continentale, baseband (surtout Sirius), MediorNet ou hybride, sous Lawo VSM dans 19 des 25 lignes de l'inventaire où le contrôle est nommé. Dans l'échantillon anglo-saxon, 33 lignes sur 53 sont IP. Ces décomptes portent sur les cars médiatisés, pas sur le parc.

Détail et sources, car par car : [rapport, section 7](rapport.html#s7).

## À tester en premier

1. **ATC sur la sortie ré-embeddée.** Router le PGM vers la destination embedder, remplacer les canaux 14 à 16, vérifier l'ATC à l'analyseur, clean switch activé puis désactivé.
2. **LTC des serveurs EVS hors vitesse nominale.** Ralenti à 33 %, jog, marche arrière, arrêt sur image. Aucun document public lu ne décrit ce comportement.
3. **Retard du suivi.** Cut, mix, volet, still store, ré-entrée de M/E.
4. **Décalage audio contre vidéo.** Il doit être constant et calibré une fois par car ; le frame sync est à désactiver sur la destination EKO.
5. **Chemin des LTC.** Sans traitement, et avec le même retard sur les trois canaux.

Détail : [rapport, section 9](rapport.html#s9). La liste des questions à poser au chef de car est en [section 10](rapport.html#s10).

## Limites de cette recherche

- **Recherche interrompue** : le budget de recherches web s'est épuisé en cours de route. Les absences ci-dessous sont des absences de recherche, non des constats.
- **ZDF** : un seul car, de l'ère HD.
- **EVS** : les manuels de la génération VIA n'ont pas pu être ouverts.
- **Prix** : aucun prix public pour les cartes et licences audio des matrices.
- **Prestataires non étudiés** : VRT, Videohouse, RAI, NEP Germany et Nordics, TopVision, les cars de l'ARD, entre autres.

La liste complète est dans le [rapport, section 11](rapport.html#s11).
