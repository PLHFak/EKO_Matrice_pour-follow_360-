# EKO écoute, le car ne programme rien

Proposition d'installation pour l'EKO Nano et l'EKO Mini : ne demander au car que des signaux qu'il sait déjà fournir, et placer la complexité dans EKO. Le timecode vient du LSM lui-même, et le bon micro est celui que l'ingénieur du son a ouvert pendant le direct.

## La proposition en bref

- **Rien à programmer dans le car, au niveau de base.** EKO ne demande que des départs ordinaires : un PGM avec le son international, les sorties des LSM, la référence. Aucune règle de matrice, aucun embedding sur mesure, aucune prise de contrôle d'une machine.
- **Le timecode vient du LSM, pas de la matrice.** Sur l'EKO Mini, il est lu dans la sortie SDI de chaque canal de lecture. Sur l'EKO Nano, il arrive par la sortie LTC de chaque serveur, en XLR, directement dans EKO.
- **Le tally dit quel LSM est à l'antenne.** C'est une demande du même type que le raccordement d'un multiviewer, bien plus simple qu'une règle de suivi dans la matrice.
- **Le bon micro est celui que l'ingénieur du son a choisi pendant le direct.** EKO enregistre les micros avant fader et note quels faders étaient ouverts. Au ralenti, il rejoue les mêmes micros, à l'heure.
- **Des étages qui s'ajoutent.** Sur le Mini, les câbles seuls donnent déjà le son international de tous les ralentis. Le tally, la console, le protocole du LSM et le tracking s'ajoutent un par un, et chacun peut manquer sans bloquer le reste. Sur le Nano, le tally fait partie de la base.

## Ce qu'on demande au car

| Demande | À qui | À quoi elle sert | Niveau |
|---|---|---|---|
| Un départ PGM avec le son international embedded | Chef de car | Image du programme, son international | Base |
| EKO Mini : une sortie SDI de chaque canal de lecture. EKO Nano : la sortie LTC de chaque serveur, en XLR | Chef de car, opérateur EVS | Timecode d'origine des images rejouées | Base |
| La référence du car | Chef de car | Horloge d'EKO | Base |
| Un retour SDI d'EKO vers la console | Ingénieur du son | Les sons EKO | Base |
| Le tally, en TSL UMD sur IP ou en contacts GPI | Chef de car | Savoir quel LSM est à l'antenne | Recommandé sur Mini, base sur Nano |
| Les micros de terrain avant fader, en MADI | Ingénieur du son | Rejouer un micro précis | Option |
| L'état des faders de ces micros, ou à défaut un sous-groupe « effets terrain » | Ingénieur du son | Choisir le bon micro | Option |

## EKO Mini : huit connecteurs, sept entrées et une sortie

{{diagram:mini}}

- **Partage des connecteurs** : un PGM, jusqu'à six canaux de lecture et une sortie. Blackmagic décrit la carte comme « 8 x 3G-SDI mini DIN connections independently configurable as Input or Output », avec 16 canaux audio embedded par SDI et une entrée de référence ([Blackmagic, DeckLink Quad 2](https://www.blackmagicdesign.com/products/decklink/techspecs/W-DLK-30)).
- **Un réglage à faire** : la carte sort d'usine en quatre paires entrée et sortie. Les huit connecteurs deviennent indépendants une fois chaque paire passée du mode « SDI 1 & SDI 2 » au mode « SDI 1 » (et de même pour les trois autres paires), dans Desktop Video Setup ou par le profil half-duplex du SDK ([Blackmagic, FAQ développeur](https://www.blackmagicdesign.com/developer/support/faq/desktop-video-developer-support-faqs) ; [Blackmagic, profils du SDK](https://sdk-doc.blackmagicdesign.com/decklink-sdk/HighLevel/profiles.html)).
- **Timecode** : chaque sortie HD d'un serveur EVS peut insérer le timecode en HANC LTC et HANC VITC ; c'est un réglage par canal, documenté dans le manuel XSnano 12.02, de la même génération logicielle que le XT3. Le SDK DeckLink rend le timecode RP188 de chaque image capturée, en HD seulement sur cette carte ([EVS, XSnano Configuration Manual 12.02](https://www.manualslib.com/manual/1421853/Evs-Xsnano.html?page=126) ; [Blackmagic, timecode dans le SDK](https://sdk-doc.blackmagicdesign.com/decklink-sdk/HighLevel/timecode.html)).
- **LSM à l'antenne** : le tally s'il est disponible. Sinon EKO compare l'image du PGM à celles des canaux de lecture qu'il reçoit. Quand les deux existent, ils se recoupent.
- **Caméra rejouée** : pour un clip, c'est la lettre de l'identifiant (111A, 111B) ([EVS, LSM-VIA User Manual 1.4](https://www.manualslib.com/manual/2596542/Evs-Lsm-Via.html?page=73)). L'affichage de la sortie monitoring montre l'identifiant du clip ; pour un train en direct, seul le nom du canal d'enregistrement, en texte libre, est documenté ([EVS, Multicam Operating Manual 11.00](https://www.manualsdir.com/manuals/254262/evs-multicamlsm-version-1100-operating-manual.html?page=21)). La lecture par l'API LinX est une hypothèse à vérifier avec EVS.
- **Une seule sortie par canal de lecture** : la sortie monitoring, câblée aujourd'hui, porte l'affichage, et la comparaison d'images doit alors éviter les lignes de l'affichage. La présence du timecode HANC sur cette sortie est à confirmer ; si elle manque, il faut prendre la sortie propre et renoncer à lire l'affichage.
- **Sortie** : un seul SDI porte les 16 canaux vers la console.

Pour le Mini, c'est le câblage d'aujourd'hui, simplifié : le PGM reste un PGM classique, et le tally remplace la règle de suivi dans la matrice.

## EKO Nano : une entrée, une sortie, deux prises

{{diagram:nano}}

- **SDI** : le PGM avec le son international en entrée, les sons EKO en sortie.
- **Timecode des LSM** : la sortie LTC de chaque serveur, en XLR, vers une petite interface audio USB à quatre entrées, par exemple une Behringer UMC404HD à 98 € TTC (Thomann Belgique, vu le 12 octobre 2026). EKO décode le LTC lui-même ([Thomann](https://www.thomann.de/be/behringer_umc404hd.htm) ; [libltc](https://github.com/x42/libltc)).
- **LSM à l'antenne** : le tally est nécessaire, en TSL UMD sur IP ou en contacts GPI.
- **Pas de conversion dans le car** : la conversion analogique se fait dans EKO. La matrice n'a rien à embedder.

Les limites du Nano :

- **Un LTC par serveur.** La sortie LTC d'un XT3 est unique, sur XLR, et correspond au PGM1. Un serveur qui met PGM1 et PGM2 à l'antenne n'a donc qu'un LTC ([EVS, brochure XT3](https://cvp.com/pdf/evs_xt3_brch.pdf) ; [EVS, XT3 Technical Reference 16.6](https://www.manualslib.com/manual/3607735/Evs-Xt-3.html?page=60)).
- **Arrêt sur image.** Un LTC ne se lit pas, en principe, à l'arrêt : EKO garde le dernier timecode lu.
- **Pas d'image des LSM.** La lettre de caméra ne peut venir que du protocole, et un clip enregistré depuis le PGM ne se vérifie que sur l'image du PGM.

Variante quand le car sait le faire : la sortie PGM Follow de la matrice, déjà décrite dans la note d'installation. Le timecode arrive alors dans le SDI, sans XLR.

## Les trois sons de l'ingénieur du son

| Son demandé | Comment EKO le trouve | Ce qu'il faut |
|---|---|---|
| Son international | Le son international enregistré, relu à l'heure d'origine de l'image | La base |
| Son de la caméra à l'image | Le micro associé à la caméra rejouée, par une table caméra et micro saisie une fois | Les micros en MADI et la lettre de caméra |
| Son de l'action | Les micros que l'ingénieur du son avait ouverts à cet instant, pris avant fader | Les micros en MADI et l'état des faders |

En option, le micro le plus proche du ballon se déduit de la position du ballon et du plan des micros. Il faut pour cela un flux de tracking, donc un accord avec la ligue, ou une analyse d'image faite par EKO.

### Les quatre briques micro

Chaque brique choisit un micro ; son nom dit qui décide. « Follow » veut dire automatique, « Select » veut dire humain. Les noms restent en anglais dans toutes les langues.

| Brique | Qui décide du micro | Mode |
|---|---|---|
| **CAM FOLLOW** | La caméra rejouée, par sa lettre A, B, C ou D | Automatique |
| **MIX FOLLOW** | Les faders ouverts par l'ingénieur du son pendant le direct, rejoués en avance au ralenti | Automatique |
| **BALL FOLLOW** | La position du ballon ou de l'action, par tracking ou analyse d'image | Automatique |
| **MIC SELECT** | L'opérateur | Humain |

Pistes de sortie d'EKO : EKO INT · CAM FOLLOW · MIX FOLLOW · BALL FOLLOW · MIC SELECT · EKO CLIP · BOOST · MONITOR 1–6.

Ces sons existent déjà comme éléments séparés dans la production sportive. À l'Euro 2020, les objets du mix immersif étaient le commentaire, les effets « close ball » et les effets « audio follow video » ([SVG Europe, 8 juillet 2021](https://www.svgeurope.org/blog/headlines/roar-of-the-crowd-telegenic-on-running-a-sound-operation-for-uefa-at-euro-2020/)).

### Rejouer la décision de l'ingénieur du son

{{diagram:fader}}

Le problème posé est : EKO enregistre tous les micros, mais ne sait pas lequel mettre à l'antenne. Ma réponse : quelqu'un l'a déjà décidé pendant le direct.

- **Pendant le direct**, l'ingénieur du son suit l'action et ouvre le micro le plus proche, souvent avec un peu de retard.
- **EKO note ce choix** : quel fader était ouvert, à quelle heure.
- **Au ralenti**, EKO rejoue ce micro à partir de son enregistrement avant fader. Le micro qui s'ouvrait en retard dans le direct est à l'heure dans le ralenti.

Cette voie évite deux obstacles :

- **La position des micros** : aucune des documentations de console lues ne contient de position de micro. Seul un ajout comme Lawo KICK la connaît.
- **Le tracking du ballon** : il existe, mais par contrat avec la ligue. En Bundesliga, TRACAB produit le flux et Sportec Solutions, filiale de la DFL, le distribue ([Live-Production](https://www.live-production.tv/news/sports/dfl-and-chyronhego-sign-new-tracab%E2%84%A2-contract-bundesliga-and-bundesliga-2.html)). Aucune source consultée ne montre un prestataire de car qui le reçoit par défaut.

Trois façons de connaître les faders, de la plus simple à la plus fine :

1. **Un sous-groupe « effets terrain » après fader.** Un départ de plus vers EKO. EKO reçoit le mélange de l'ingénieur du son, sans la foule ni le commentaire.
2. **Chaque micro avant et après fader.** Les consoles Calrec donnent jusqu'à quatre sorties directes par voie, au choix avant ou après fader. EKO déduit l'ouverture du fader en comparant les deux. C'est une inférence à vérifier, en particulier quand un groupe ou un VCA commande les voies ([Calrec, Artemis Operator's Manual](https://www.manualslib.com/manual/1341453/Calrec-Artemis.html?page=115)).
3. **Le protocole de la console.** Le CSCP de Calrec donne, pour 192 faders au plus, la position, l'état Cut ou On et le nom de la voie, sur TCP/IP ([Calrec, Apollo Installation Manual](https://www.manualslib.com/manual/1314128/Calrec-Apollo.html?page=62)). Lawo annonce le contrôle de tous les paramètres de voie en Ember+ ; les noms de voie y sont attestés, la position du fader et le mute ne sont pas détaillés dans un document public ([Lawo, mc²56](https://lawo.com/products/mc%C2%B256-audio-production-console/)).

La console peut aussi travailler pour EKO dans l'autre sens. Ses fonctions « audio follow video » ouvrent une voie sur un tally : 256 Autofaders sur une Calrec Artemis, 128 événements sur une Lawo mc²96. Déclenchées par le tally d'un LSM, elles ouvriraient la voie EKO toute seule à chaque ralenti. Aucune source ne décrit ce montage : il est à essayer ([Calrec, Artemis Operator's Manual](https://www.manualslib.com/manual/1341453/Calrec-Artemis.html?page=90) ; [Lawo, mc²96 Audio Follow Video](https://docs.lawo.com/audio-production-mc-mixing-consoles/mc96/mc96-operation/mc96-channel-operations/mc96-audio-follow-video)).

### Faire entrer les micros

- **Le plan de micros** : la base historique est de 12 micros autour du terrain ; Sportcast est passé à 17 en Bundesliga ([SVG Europe, 26 mars 2018](https://www.svgeurope.org/blog/headlines/sky-sport-summit-in-cooperation-with-svg-europe-the-future-of-audio-in-sports/) ; [Sennheiser, 16 octobre 2025](https://newsroom.sennheiser.com/broadcast-production-partner-topvision-ensures-authenticity-in-football-broadcasting)).
- **Le transport** : un flux MADI de sorties directes, que les consoles savent router vers un enregistreur externe ([Lawo, mc²96 Direct Out](https://docs.lawo.com/audio-production-mc-mixing-consoles/mc96/mc96-operation/mc96-channel-operations/mc96-direct-out)).
- **Dans EKO** : une interface MADI USB à 64 canaux, par exemple la RME MADIface USB à 717 € TTC (Thomann Autriche, vu le 12 octobre 2026) ([Thomann](https://www.thomann.at/rme_madiface_usb_reviews.htm?rating=5)).

## Ce que j'écarte en base, et pourquoi

| Voie | Pourquoi elle ne passe pas le critère « simple à installer » |
|---|---|
| Le LTC des LSM embeddé par la matrice | Trois conversions analogiques, une sortie embedder libre et une carte de canaux sur mesure, à refaire dans chaque car |
| Le PGM Follow par des règles dans la matrice | Aucune fonction de ce nom n'a été trouvée dans la documentation publique des systèmes de contrôle ; c'est un travail d'ingénierie par car. Il reste une variante pour le Nano |
| Le timecode du LSM transporté dans le PGM par le mélangeur | Le passage de l'ancillaire sur une sortie de mélangeur n'est documenté, dans les manuels consultés, que chez Ross |
| Le protocole du LSM comme source du timecode | Une liaison série par canal avec une licence, ou l'API LinX sur le réseau du car, dont les conditions ne sont pas publiques, pour une information déjà présente dans le SDI. Je le garde pour la lettre de caméra seulement |
| Le tracking du ballon | Dépend d'un contrat de ligue. Je le garde comme option, sur le modèle de Lawo KICK |

Lawo KICK fait exactement ce choix du micro le plus proche à partir du tracking TRACAB ; la Bundesliga l'a adopté pour la saison 2017/18. Salsa Sound MIXaiR le fait à partir des seuls signaux des micros ([SVG, 20 décembre 2018](https://www.sportsvideo.org/2018/12/20/lawo-develops-hockey-version-of-kick-action-following-audio-system/) ; [SVG Europe, 2 novembre 2017](https://www.svgeurope.org/blog/headlines/bundesliga-is-worlds-first-league-to-use-automated-audio-mixing/) ; [SVC Online, 3 novembre 2021](https://www.svconline.com/the-wire/salsa-sound-launches-software-defined-and-cloud-compatible-version-of-ai-based-audio-mixing-engine-mixair-2-0)).

## Ce que cela demande à EKO

1. **Mini en huit canaux** : partage entrées et sorties réglable, de 4 + 4 à 7 + 1.
2. **Écoute du tally** : TSL UMD v3.1 et v5, en UDP et en TCP, avec une table d'index et un sens des bits réglables par car. Une entrée GPI sert de repli ([TSL, spécification du protocole](https://tslproducts.com/wp-content/uploads/TSL-UMD-protocol.pdf)).
3. **Comparaison d'images** entre le PGM et les canaux de lecture reçus, pour recouper le tally et le remplacer quand il manque.
4. **Nano** : entrée LTC par interface audio USB.
5. **Entrée multipiste** en MADI.
6. **Journal des faders** horodaté : CSCP pour les cars UHD d'AMP Visual TV documentés (Millenium Signature 12, Millenium 3, 4 et 6), qui travaillent sur Calrec ; les cars plus anciens sont sur Studer Vista ([AMP Visual TV, Millenium](https://www.ampvisualtv.tv/en/our-production-resources/mobile-resources/132-millenium.html)).
7. **Lettre de caméra** : lecture de l'affichage du LSM, puis API LinX si EVS le confirme.

## À valider avant de développer

1. **Sur un LSM réel** : le réglage d'insertion du timecode et sa tenue en ralenti et à l'arrêt. Les valeurs « No » et « TC 0 » couperaient le suivi ([EVS, XSnano Configuration Manual 12.02](https://www.manualslib.com/manual/1421853/Evs-Xsnano.html?page=126)).
2. **La sortie monitoring** : timecode HANC présent ou non ; affichage que l'opérateur peut éteindre avec la touche F5, et dont la mise en page complète n'est pas documentée.
3. **La carte Quad 2** : lecture du timecode RP188 sur sept entrées à la fois, en particulier en 1080p50.
4. **AMP sur les serveurs EVS** : AMP n'apparaît dans aucun document EVS trouvé. La liste des protocoles de Cerebrum (V2.01, mai 2021) donne AMP pour le Grass Valley K2 et l'API LinX pour les XT et XT-VIA. À vérifier sur un serveur avant tout développement AMP ([EVS, liste des protocoles Cerebrum](https://evs.com/sites/default/files/2021-05/Cerebrum%20protocol%20list%20V2.01%20%28May21%29.pdf)).
5. **Le tally** : l'envoi en TSL est documenté pour les mélangeurs Ross et pour TSL TallyMan, listé sans procédure publique pour EVS Cerebrum, et non confirmé pour Lawo VSM. Le sens des bits varie d'un constructeur à l'autre, et le comportement pendant un fondu n'est pas documenté.
6. **La console** : l'accord de l'ingénieur du son pour une lecture des faders. Aucun mode en lecture seule n'est documenté, et Lawo coupe les connexions Ember+ externes à chaque chargement de production ([Lawo, notes de version mc² 12.0.0](https://docs.lawo.com/audio-production-mc-mixing-consoles/audio-production-software-versions/mc-release-notes-12-0-0)).
7. **Le LTC des serveurs**, pour le Nano : son comportement hors vitesse nominale n'est décrit dans aucun document public, et l'existence d'une sortie LTC analogique sur XT-VIA n'est pas confirmée.
8. **La DeckLink SDI Micro** : une entrée et une sortie fixes selon les revendeurs ; la fiche du constructeur n'a pas pu être lue, et le nombre de canaux audio embedded n'est pas confirmé.

## Ordre d'essai proposé

1. **Mini, câbles seuls** : un PGM et les sorties des canaux de lecture, sur un match.
2. **Mini avec tally** : comparer le tally et la comparaison d'images.
3. **Nano** : LTC en XLR et tally.
4. **Micros en MADI** et sous-groupe « effets terrain ».
5. **Journal des faders** sur une console Calrec.
6. **Lettre de caméra** et table caméra et micro.
