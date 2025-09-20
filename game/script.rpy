# Ren'Py script: Simone Veil – Mémoire et Dignité

define narrator = Character(None)
define simone = Character("Simone", color="#c04f8a")
define milou = Character("Milou", color="#4f83c0")
define yvonne = Character("Yvonne", color="#6aa84f")
define antoine = Character("Antoine", color="#ff9900")
define stenia = Character("Stenia", color="#aa0000")

# --- Variables globales ---
default fatigue = 0        # 0 = reposée, 100 = épuisée
default trauma = 0         # 0 = calme, 100 = traumatisée
default determination = 50 # 0 = découragée, 100 = très résolue
default ending = ""

# --- Screen pour stats ---
screen stats_overlay():
    frame align (0.01, 0.01):
        has vbox
        text "Fatigue: [fatigue]" size 20 color "#ffffff"
        text "Trauma: [trauma]" size 20 color "#ffffff"
        text "Détermination: [determination]" size 20 color "#ffffff"

default persistent.show_stats = True

label before_main_menu:
    if persistent.show_stats:
        show screen stats_overlay
    return

# --- Label de feedback dynamique ---
label feedback_scene:

    if fatigue >= 50:
        scene fatigue_scene
        simone "Je… je n’en peux plus… mes jambes brûlent et mon dos me fait mal…"

        menu:
            "Prendre une pause":
                $ fatigue -= 10
                narrator "Simone respire quelques minutes et reprend un peu de force."
            "Continuer malgré tout":
                $ determination += 5
                simone "Je ne peux pas m'arrêter… il faut avancer, quoi qu’il arrive."
                narrator "Elle serre les dents, mais ses jambes tremblent sous l’effort."

    elif trauma >= 50:
        scene flashback_scene
        simone "(pensée) Je revois Auschwitz… les cris, les peurs, les visages perdus…"

        menu:
            "Se concentrer pour respirer et se calmer":
                $ trauma -= 10
                $ determination += 5
                simone "Il faut que je tienne… pour moi et pour ma sœur."
            "Laisser éclater la peur quelques instants":
                $ trauma -= 5
                $ fatigue += 5
                simone "Je… je ne peux pas oublier… tout est encore là."

    elif determination >= 70:
        scene determination_scene
        simone "(pensée) Je dois continuer… pour tous ceux qui comptent sur moi."
        narrator "Sa force intérieure semble irradier autour d'elle, inspirant ceux qui l'entourent."

    return

# --- Début du jeu ---
label start:
    show screen stats_overlay

    narrator "Chapitre 1 : Nice, avant l’Occupation"
    narrator "Simone Jacob grandit dans une famille aimante. Tout semble normal… mais le vent de la guerre approche."
    simone "(pensée) Tout était si simple avant… et maintenant, tout est menacé."

    yvonne "Simone, fais attention. La situation devient dangereuse pour nous tous."
    simone "Je sais, maman… mais vivre dans la peur ne me semble pas juste."

    menu:
        "Se concentrer sur les études et rester optimiste":
            $ determination += 5
            simone "Je vais continuer mes études et garder espoir."
            yvonne "Courage ma chérie… ton optimisme est notre force."
        "Observer les dangers et aider la famille à se protéger":
            $ trauma += 5
            $ determination += 2
            simone "Je vais surveiller la situation… il faut protéger tout le monde."
            yvonne "Merci, ma fille… mais fais attention à toi aussi."

    narrator "Chapitre 2 : Mars 1944 – Arrestation"
    narrator "La vie de Simone bascule le lendemain de son bac. Elle est arrêtée avec sa mère Yvonne et sa sœur Milou."

    menu:
        "Se concentrer sur sa propre survie":
            $ determination += 5
            simone "(pensée) Je dois rester forte, pour ne pas céder à la peur."
            yvonne "Simone… tu sembles calme, ma chérie…"
        "Veiller sur sa mère et sa sœur avant tout":
            $ trauma += 5
            $ fatigue += 5
            simone "Je ne vous laisserai pas seules, quoi qu’il arrive."
            milou "Merci, Simone… c’est rassurant d’avoir ta force."

    narrator "Chapitre 3 : Le convoi vers Auschwitz"
    narrator "13 avril 1944. Elles embarquent dans le convoi 71."

    menu:
        "Rassurer Milou et Yvonne malgré la peur":
            $ determination += 5
            simone "(sourire forcé) Pensez à nos souvenirs heureux à Nice."
            yvonne "Tes mots m’apaisent un peu…"
            milou "Oui… je me sens moins seule."
            $ trauma += 2
        "Se concentrer sur la survie personnelle":
            $ determination += 2
            simone "(pensée) Je dois rester forte… pour moi et pour elles."
            yvonne "Simone… tu sembles si calme…"
            simone "(détachée) Je dois… je ne peux pas céder à la panique."
            $ fatigue += 5

    $ fatigue += 10
    $ trauma += 10
    call feedback_scene

    narrator "Chapitre 4 : Bobrek et travail forcé"
    narrator "Quelques semaines plus tard, la Kapo Stenia décide du sort de Simone."

    stenia "Tu es trop belle et trop jeune pour mourir ici. Je vais t’envoyer à Bobrek."
    simone "(déterminée) À condition que ma mère et ma sœur m’accompagnent."

    narrator "Simone est affectée aux travaux de terrassement puis à l’usine Siemens."
    $ fatigue += 10
    call feedback_scene

    narrator "Chapitre 5 : Janvier 1945 – La marche de la mort"
    narrator "Le 18 janvier 1945, la marche de la mort commence."

    $ fatigue += 15
    $ trauma += 15
    simone "(pensée) Mes jambes brûlent… mais il faut avancer."
    call feedback_scene

    narrator "Chapitre 6 : Bergen-Belsen"
    narrator "30 janvier 1945. Elles arrivent à Bergen-Belsen, dans des conditions terribles."

    $ fatigue += 10
    $ trauma += 10
    call feedback_scene

    narrator "Après la libération, Simone reprend ses études à la faculté de droit puis à Sciences-Po."
    menu:
        "Se consacrer aux études et reconstruction personnelle":
            $ determination += 5
            simone "Je dois reconstruire ma vie et continuer malgré tout."
        "S’engager dans les associations de survivants":
            $ trauma += 5
            $ determination += 2
            simone "Je veux que personne n’oublie ce qui s’est passé."

    narrator "1946. Simone rencontre Antoine Veil et se marie."
    menu:
        "Équilibrer vie familiale et témoignage":
            $ determination += 3
            $ trauma -= 3
            simone "Je vais aimer ma famille tout en transmettant la mémoire."
        "Se consacrer pleinement à la mémoire et aux survivants":
            $ determination += 5
            $ trauma += 2
            simone "Je dois partager mon expérience pour le bien des autres."

    narrator "1974. Simone devient ministre de la Santé et défend la loi sur l’IVG."
    menu:
        "Répondre avec fermeté aux opposants":
            $ determination += 5
            simone "Je ne peux reculer devant l’injustice."
        "Chercher la conciliation et alliances politiques":
            $ determination += 2
            $ trauma -= 2
            simone "Il faut convaincre sans renoncer."

    narrator "1979. Simone est élue députée européenne, première présidente du Parlement européen."
    menu:
        "Prioriser la mémoire et la réconciliation":
            $ determination += 2
            $ trauma -= 2
            simone "Il faut que la mémoire guide nos choix."
        "Prioriser les droits des femmes et législation européenne":
            $ determination += 5
            simone "Les droits humains doivent être défendus partout."

    if determination >= 70:
        $ ending = "politique"
    elif trauma >= 50:
        $ ending = "mémoire"
    else:
        $ ending = "équilibre"

    jump epilogue

# --- Épilogue riche et émotionnel ---
label epilogue:
    scene bg_paris
    with fade
    narrator "Les années ont passé. Simone Veil s’éteint en 2017, laissant derrière elle un monde transformé par son courage et son engagement."
    narrator "Ses cendres, et celles de son mari Antoine, sont transférées au Panthéon en 2018, symbole d’une vie consacrée à la mémoire, aux droits humains et à la justice."

    if ending == "politique":
        narrator "À travers ses combats politiques, elle a façonné des lois et ouvert des chemins de liberté et de dignité. Chaque décision témoigne de sa détermination à construire une société juste."
        narrator "Le Parlement européen garde le souvenir d’une femme qui a su transformer la douleur en force et inspirer des générations à poursuivre le combat pour l’égalité et la justice."

    elif ending == "mémoire":
        narrator "Mais c’est surtout par sa mémoire et ses témoignages que Simone Veil laisse une empreinte indélébile. Survivante des camps, elle a porté la voix des disparus et des victimes, transformant l’horreur vécue en leçon pour l’humanité."
        narrator "Chaque mot qu’elle a partagé continue d’éveiller les consciences, rappelant que l’oubli est l’ennemi de la dignité."

    else:
        narrator "Simone Veil a trouvé un équilibre précieux entre vie familiale et engagement pour les autres. Elle a aimé, transmis, lutté et protégé ceux qui lui étaient chers, tout en construisant un héritage qui dépasse le temps."

    narrator "Aujourd’hui, en écoutant son histoire, nous sentons encore sa présence : une femme qui a transformé la douleur en action, la peur en détermination, et qui continue d’inspirer chacun à se lever pour la justice et la mémoire."

    return
