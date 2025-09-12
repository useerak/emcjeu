# Ren'Py visual novel script: "Reflets d'Après"
# Inspiré de la vie de Gisèle Guillemot.
# Prototype simplifié, images optionnelles.

# --- Déclarations de personnages ---
define narrator = Character(None)
define g = Character("Giselle", color="#c04f8a")
define m = Character("Marie", color="#4f83c0")
define p = Character("Pierre", color="#6aa84f")

image bg_paris = im.Scale("bg_paris.jpg", 1920, 1080)

# --- Variables globales ---
default trust = 50        # Confiance de la société envers Giselle (0-100)
default resolve = 60      # Force intérieure de Giselle (0-100)
default trauma = 60       # Intensité des souvenirs douloureux (0-100)

default met_association = False
default gave_testimony = False
default ending = ""

# --- Screen pour afficher les stats ---
screen stats_overlay():
    frame align (0.01, 0.01):
        has vbox
        text "Confiance: [trust]" size 20 color "#ffffff"
        text "Force: [resolve]" size 20 color "#ffffff"
        text "Trauma: [trauma]" size 20 color "#ffffff"

# Activer l'écran des stats en permanence
default persistent.show_stats = True

label before_main_menu:
    if persistent.show_stats:
        show screen stats_overlay
    return

label start:
    show screen stats_overlay
    scene bg_paris
    # show giselle_neutral
    # with dissolve

    narrator "Automne 1945. Le monde est rentré dans une paix fragile. Pour Giselle, la guerre n'est pas finie : elle revient avec des souvenirs qui ne s'effacent pas."

    g "Je pensais que rentrer suffirait. Mais comment expliquer l'inexprimable ?"

    menu:
        "Tenter de retrouver des proches":
            jump reunite_family
        "Chercher des camarades et des groupes de résistants":
            jump seek_association

label reunite_family:
    scene bg_paris
    # show giselle_tired
    # with fade

    narrator "Tu retrouves quelques membres de ta famille. Ils sont heureux de te revoir mais peinent à comprendre l'ampleur de ce que tu as vécu."

    m "C'est incroyable que tu aies survécu... mais es-tu sûre de ne pas dramatiser un peu ?"
    $ trust -= 10
    g "Je... je n'invente rien."
    $ trauma += 5

    menu:
        "Répondre avec colère":
            $ resolve -= 5
            g "Ce n'est pas à moi de convaincre. Ce sont les faits qui parlent."
            jump after_first_contacts
        "Essayer d'expliquer calmement":
            $ trust -= 5
            g "Je vais essayer de raconter, doucement."
            jump after_first_contacts

label after_first_contacts:
    narrator "Tu réalises vite que la famille, malgré l'affection, n'a pas toujours les mots."

    menu:
        "Persévérer à témoigner":
            $ resolve += 5
            jump seek_association
        "Se replier pour un temps":
            $ resolve -= 10
            jump quiet_life

label quiet_life:
    scene bg_paris
    # show giselle_tired
    narrator "Tu choisis le silence temporaire. La douleur reste, mais tu évites la confrontation."
    $ ending = "retrait"
    jump epilogue

label seek_association:
    # scene association_room
    # show giselle_resolved
    # with fade

    narrator "Tu retrouves des camarades et des associations d'anciens résistants et déportés. Ici, on te croit."
    $ met_association = True

    p "Enfin quelqu'un qui comprend. Raconte-nous ce que tu peux."

    menu:
        "Raconter sans s'arrêter":
            $ gave_testimony = True
            $ resolve += 10
            $ trauma += 5
            g "Je vais tout dire, pour que personne n'oublie."
            jump testimony_event
        "Commencer petit à petit":
            $ gave_testimony = True
            $ resolve += 5
            g "Je ne peux pas tout aujourd'hui, mais j'aimerais partager ce que je peux."
            jump testimony_event

label testimony_event:
    # scene bg_camp
    # with dissolve

    narrator "Les récits reviennent, pesants, mais ils sont accueillis ici par une oreille compréhensive."

    menu:
        "Accepter de témoigner publiquement (école, mairie)":
            $ gave_testimony = True
            $ trauma += 10
            $ resolve += 5
            jump public_testimony
        "Se limiter aux réunions d'anciens":
            $ gave_testimony = True
            $ resolve += 3
            jump private_meetings

label private_meetings:
    # scene association_room

    narrator "Dans les réunions, ta parole trouve un écho. Tu retrouves un sens en transmettant."
    $ trust += 5

    menu:
        "Organiser des rencontres scolaires":
            $ trust -= 5
            $ trauma += 5
            jump public_testimony
        "Rester sur des cercles d'anciens":
            $ ending = "communaute"
            jump epilogue

label public_testimony:
    # scene bg_city
    # show crowd_skeptical

    narrator "Tu acceptes de témoigner devant des civils et des jeunes. L'accueil est mitigé : certains pleurent, d'autres te regardent comme si tu exagérais."

    if trust >= 50:
        narrator "Malgré tout, certaines personnes comprennent. Des enseignants remercient, des jeunes posent des questions."
        $ resolve += 5
        $ ending = "transmission"
    else:
        narrator "Beaucoup semblent incapables de concevoir l'horreur. On te dit que tu dramatises. Tu sens la solitude à nouveau."
        $ resolve -= 10
        $ ending = "incompris"

    jump epilogue

label arrest_flashback:
    # scene bg_prison
    # with fade

    narrator "Tu te souviens des arrestations, des cellules, de la peur constante. Ces souvenirs viennent parfois sans prévenir."
    $ trauma += 5
    return

label epilogue:
    scene bg_paris
    # show giselle_neutral
    # with dissolve

    narrator "Les années passent. Ta réintégration est un chemin en zigzag, entre réparation et blessures qui ne se referment pas."

    if ending == "retrait":
        narrator "Tu as choisi la discrétion. La société n'a pas su te donner l'écoute que tu méritais. Tu trouves une paix relative dans l'intimité."
    elif ending == "communaute":
        narrator "Tu trouves refuge dans la communauté des anciens. Là, ta parole est une pierre posée sur le sillon de la mémoire."
    elif ending == "transmission":
        narrator "Ton témoignage trouve des oreilles. Certaines semences germent : de jeunes gens s'engagent, des écoles programment des rencontres. Ta souffrance trouve une utilité morale."
    elif ending == "incompris":
        narrator "Les incompréhensions persistent. Tu n'as pas obtenu le réconfort espéré. Mais ton action silencieuse a porté malgré tout quelques fruits, souvent insoupçonnés."
    else:
        narrator "La vérité est que la réintégration n'est jamais complète. Mais tu as cherché des refuges moraux et tu as transmis, parfois en silence."

    narrator "-- Éléments de bilan --"
    $ stat_text = "Confiance sociale: [trust]\\nForce intérieure: [resolve]\\nTraumatisme résiduel: [trauma]"
    narrator "[stat_text]"

    return
