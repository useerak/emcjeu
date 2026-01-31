# -*- coding: utf-8 -*-

# -------------------------------------------------
#  Déclarations de base
# -------------------------------------------------
# Définition de la transformation de flou
transform blur(v):
    mesh True
    blur v

init:
    python:
        import math

    
    transform shake_disturbed:
        linear 0.1 xoffset -2 yoffset 2
        linear 0.1 xoffset 3 yoffset -3
        linear 0.1 xoffset -3 yoffset -1
        linear 0.1 xoffset 0 yoffset 0
        repeat
# Personnages
define narrator = Character(None)
define simone   = Character("Simone", color="#c04f8a")
define milou    = Character("Milou",  color="#4f83c0")
define yvonne   = Character("Yvonne", color="#6aa84f")
define antoine  = Character("Antoine", color="#ff9900")
define stenia   = Character("Stenia", color="#aa0000")

# -------------------------------------------------

image bg_nice               = "images//bg_nice.jpg"
image bg_arrestation        = "images//bg_arrestation.jpg"
image bg_convoi             = "images//bg_convoi.jpg"
image bg_bobrek             = "images//bg_bobrek.jpg"
image bg_marche_mort        = "images//bg_marche.jpg"
image bg_bergen_belsen      = "images//bg_bergen.jpg"
image bg_paris_jeune        = "images//bg_parispw.jpg"
image bg_antoine            = "images//bg_antoine.jpg"
image bg_ministere          = "images//bg_ministere.jpg"
image bg_parlement_europeen = "images//bg_parlement.jpg"
image bg_paris              = "images//bg_paris.jpg"
image simoneopen            = "images//simoneopen.png"
image simoneclose           = "images//simoneclose.png"
image stenia                = "images//stenia.png"
image simonefatigue        = "images//simonefatigue.png"
image simonejeunetrauma   = "images//simonejeunetrauma.png"
image simonejeunedeter  = "images//simonejeunedeter.png"
image yvonneopen           = "images//yvonneopen.png"
image yvonneclose          = "images//yvonneclose.png"
image milouopen            = "images//milouopen.png"
image milouclose           = "images//milouclose.png"
image antoineclose         = "images//antoineclose.png"
image antoineopen          = "images//antoineopen.png"
image simonejeuneopen     = "images//simonejeuneopen.png"
image simonejeuneclose    = "images//simonejeuneclose.png"
image icon_qte_marche = "images/icon_qte_marche.png"



image fatigue_scene        = Solid("#000000")
image flashback_scene      = Solid("#FFFFFF")
image determination_scene  = Solid("#FFFFFF")


#  Variables globales

default fatigue       = 0        
default trauma        = 0        
default determination = 50       
default ending        = ""
default vu_fatigue = False
default vu_flashback = False
default vu_determination = False
default persistent.show_stats = True

default a_carnet = False
default a_peluche = False

default collectibles = []


screen bouton_survie():
    
    default temps_max = 1.5
    default temps_actuel = 1.5

    timer 0.05 repeat True action If(temps_actuel > 0, 
        true=SetScreenVariable("temps_actuel", temps_actuel - 0.05), 
        false=Return("fail"))

    
    vbox:
        align (0.5, 0.5)
        spacing 30
        
        imagebutton:
            idle "icon_qte_marche"
            hover "icon_qte_marche"
            action Return("success")
            at shake_disturbed 
            xalign 0.5
           
            at transform:
                zoom 0.5

        vbox:
            xalign 0.5
            text "SURVIE" size 20 bold True color "#fff" xalign 0.5
            bar:
                value temps_actuel
                range temps_max
                xsize 400
                ysize 15
                left_bar Frame(Solid("#ff0000"), 4, 4)
                right_bar Frame(Solid("#333333"), 4, 4)


screen stats_overlay():
    if persistent.show_stats:
        frame:
            background Frame(Solid("#00000066"), 4, 4) 
            align (0.02, 0.02)
            padding (15, 15)
            xsize 350

            vbox:
                spacing 12
                vbox:
                    text "DÉTERMINATION" size 14 bold True color "#ffffff"
                    bar value AnimatedValue(determination, range=100, delay=1.0):
                        xsize 300 ysize 15
                        left_bar Frame(Solid("#005b7a"), 4, 4)
                        right_bar Frame(Solid("#333333"), 4, 4)

                vbox:
                    text "FATIGUE" size 14 bold True color "#ffffff"
                    bar value AnimatedValue(fatigue, range=100, delay=1.0):
                        xsize 300 ysize 15
                        left_bar Frame(Solid("#005b7a"), 4, 4)
                        right_bar Frame(Solid("#333333"), 4, 4)

                vbox:
                    text "TRAUMA" size 14 bold True color "#ffffff"
                    bar value AnimatedValue(trauma, range=100, delay=1.0):
                        xsize 300 ysize 15
                        left_bar Frame(Solid("#005b7a"), 4, 4)
                        right_bar Frame(Solid("#333333"), 4, 4)

                null height 15 # Un petit espace vide pour séparer
                
                vbox:
                    spacing 5
                    text "OBJETS MÉMORIELS" size 14 bold True color "#ffffff"
                    
                    hbox:
                        spacing 15
                        if a_carnet:
                            add "images/icon_carnet.png" zoom 0.15
                        
                        if a_peluche:
                            add "images/icon_peluche.png" zoom 0.15
                        
                        if not a_carnet and not a_peluche:
                            text "Aucun objet trouvé" size 12 italic True color "#aaaaaa"


#  Avant le menu principal

label before_main_menu:
    show screen stats_overlay
    return


label feedback_scene:

    if fatigue >= 50 and not vu_fatigue:
        $ vu_fatigue = True
        scene fatigue_scene
        with dissolve
        show simonefatigue at center with dissolve
        simone "Je… je sens que mon corps cède. Mes jambes me portent à peine."
        simone "Chaque pas me rappelle que je ne suis qu’un numéro pour eux, mais je refuse de l’accepter."

        menu:
            "Prendre discrètement quelques instants pour reprendre des forces":
                $ fatigue = max(fatigue - 15, 0)
                narrator "Simone ralentit, ajuste sa marche pour se fondre dans le groupe et reprendre un peu son souffle."
                simone "(pensée) Si je tombe, je ne pourrai plus protéger personne. Tenir, mais autrement."
            "Poursuivre coûte que coûte, sans rien laisser paraître":
                $ determination = min(determination + 7, 100)
                $ fatigue = min(fatigue + 5, 100)
                simone "Je n’ai pas le droit de m’arrêter. Pas maintenant."
                narrator "Elle avance, les traits tendus, transformant sa douleur en obstination silencieuse."

    elif trauma >= 50 and not vu_flashback:
        $ vu_flashback = True
        scene flashback_scene
        with dissolve
        show simonejeunetrauma at center with dissolve
        simone "(pensée) Les images reviennent… les cris, les coups, les visages disparus."
        simone "(pensée) Si je me laisse engloutir, je n’arriverai plus à bouger."

        menu:
            "Se concentrer sur la respiration, revenir au présent":
                $ trauma = max(trauma - 15, 0)
                $ determination = min(determination + 5, 100)
                simone "*Inspire… expire…*"
                simone "Je suis ici, maintenant. Je dois rester lucide pour celles qui ne le peuvent plus."
                narrator "Peu à peu, le vacarme intérieur recule et laisse place à un calme fragile."
            "Accepter la vague de peur et de chagrin pour la laisser passer":
                $ trauma = max(trauma - 8, 0)
                $ fatigue = min(fatigue + 7, 100)
                simone "Je ne peux pas faire semblant que tout cela n’existe pas."
                narrator "Elle laisse les larmes couler un instant, puis sèche son visage et se redresse."
                simone "(pensée) La douleur est là, mais elle ne décidera pas seule de ma vie."

    elif determination >= 70 and not vu_determination:
        $ vu_determination = True
        scene determination_scene
        with dissolve
        show simonejeunedeter at center with dissolve
        simone "(pensée) Ils ont voulu nous réduire au silence."
        simone "(pensée) Mais tant que je respire, je peux choisir : protéger, résister, témoigner."
        narrator "Sa force intérieure ne se voit pas toujours, mais elle guide chacun de ses gestes."

    return


image simone_parle: 
    "images/simoneopen.png"  
    pause 0.2                
    "images/simoneclose.png"
    pause 0.2
    repeat         

image yvonne_parle: 
    "images/yvonneopen.png"
    pause 0.2
    "images/yvonneclose.png"
    pause 0.2
    repeat

image milou_parle:
    "images/milouopen.png"
    pause 0.2
    "images/milouclose.png"
    pause 0.2
    repeat 

image antoine_parle:
    "images/antoineopen.png"
    pause 0.2
    "images/antoineclose.png"
    pause 0.2
    repeat

image simonejeune_parle:
        "images/simonejeuneclose.png"
        pause 0.2
        "images/simonejeuneopen.png"
        pause 0.2
        repeat
 
label start:
    play music "audio/nice_theme.mp3" fadein 2.0
    show screen stats_overlay
    

    # Chapitre 1 : Nice
    scene bg_nice with fade:
        zoom 1.20
        align (0.5, 0.5)

    narrator "Chapitre 1 : Nice, avant l’Occupation."
    narrator "Simone Jacob grandit à Nice, dans une famille aimante et cultivée, attachée à l’école et à la République."
    narrator "Mais les lois antisémites et la guerre resserrent peu à peu leur étau."

    show simonejeuneclose at left with dissolve
    simone "(pensée) Il y a encore le lycée, les amis, la mer… tout semble presque normal."
    simone "(pensée) Et pourtant, chaque nouvelle mesure nous rappelle que nous sommes devenus des citoyens à part."
    
    show yvonne_parle at right with dissolve
    yvonne "Simone, promets-moi une chose : continue à travailler à l’école."
    yvonne "Personne ne pourra t’enlever ce que tu porteras dans ta tête."
    hide yvonne_parle   
    show yvonneclose at right

    show simonejeune_parle at left with dissolve
    simone "Je te le promets, maman. Mais j’ai peur pour toi, pour papa, pour Milou et Jean."
    $ a_carnet = True
    show icon_carnet at truecenter with dissolve
    narrator "Les doigts de Simone glissent sur la couverture du carnet. C'est plus qu'un recueil de notes..."
    simone "{i}Chaque page blanche est un territoire que personne ne pourra m'enlever.{/i}"
    simone "{i}Mes pensées, mes rêves, mes leçons... Tout ce qui fait de moi 'Simone' est ici.{/i}"
    hide icon_carnet with fade
    show simonejeuneclose at left with dissolve
    hide simonejeune_parle

    menu:
        "S’accrocher aux études comme acte de résistance silencieuse":
            $ determination = min(determination + 7, 100)
            show simonejeune_parle at left with dissolve
            simone "Si je continue d’apprendre, c’est ma façon de dire qu’ils n’ont pas gagné."
            hide simonejeune_parle
            show simonejeuneclose at left 

            show yvonne_parle at right with dissolve
            yvonne "Tu as raison. Le savoir sera une force pour l’avenir."
            hide yvonne_parle
            show yvonneclose at right with dissolve
        "Observer les dangers et surveiller chaque signe de menace":
            $ trauma = min(trauma + 5, 100)
            $ determination = min(determination + 3, 100)
            show simonejeune_parle at left with dissolve
            simone "Je vais rester attentive aux rumeurs, aux visites, aux contrôles… Nous devons être prêts à réagir."
            hide simonejeune_parle
            show simonejeuneclose at left 
            yvonne "Tu es encore jeune, mais tu vois déjà clair. Fais juste attention à toi."
            show yvonne_parle at right with dissolve
            hide yvonne_parle
            show yvonneclose at right 
            stop music fadeout 2.0
    # Chapitre 2 : Arrestation
    scene bg_arrestation with fade:
        zoom 1.20
        align (0.5, 0.5)
    play music "audio/tension_conv.mp3" fadein 1.5

    narrator "Chapitre 2 : Mars 1944 – Arrestation."
    narrator "Le lendemain de son baccalauréat, Simone est arrêtée avec sa mère Yvonne et sa sœur Milou."
    narrator "En quelques heures, leur quotidien est balayé."
    show simonejeuneclose at left 
    simone "(pensée) Hier, je pensais à mes études. Aujourd’hui, je pense seulement à ne pas être séparée d’elles."

    menu:
        "Se concentrer sur sa propre survie pour rester solide":
            $ determination = min(determination + 6, 100)
            simone "(pensée) Si je m’effondre, je ne pourrai aider personne."
            simone "(bas) Je dois garder mon sang-froid, observer, comprendre ce qui se passe."
            show yvonne_parle at right with dissolve
            yvonne "Tu restes étonnamment calme, Simone. Cette force nous aide toutes."
            hide yvonne_parle
            show yvonneclose at right 
        "Rassurer sa mère et sa sœur avant tout":
            $ trauma = min(trauma + 5, 100)
            $ fatigue = min(fatigue + 5, 100)
            show simonejeune_parle at left with dissolve
            simone "Maman, Milou… quoi qu’il arrive, on reste ensemble, d’accord ?"
            hide simonejeune_parle
            show simonejeuneclose at left with dissolve
            show milou_parle at right with dissolve
            milou "Ta voix m’apaise, même si j’ai très peur."
            hide milou_parle
            show yvonne_parle at right with dissolve
            yvonne "Ta force me rappelle que je dois tenir, moi aussi."
            hide yvonne_parle
            $ a_peluche = True
            show icon_peluche at truecenter with dissolve
            narrator "Un petit ours en peluche, un peu usé par le temps, passe des mains de Milou à celles de Simone."
            simone "{cps=15}C'est un morceau de notre enfance qui s'accroche à nous...{/cps}"
            simone "{i}Un dernier rempart de douceur avant que le monde ne devienne de fer et de glace.{/i}"
            hide icon_peluche with fade
            narrator "Les soldats frappent à la porte. C'est le chaos, tout va trop vite !"


    menu:
        "Cacher le carnet dans la doublure du manteau (VITE !)" if a_carnet:
            $ determination += 5
            narrator "D'un geste vif, vous sauvez vos écrits."
        
        "{color=#f00}Paniquer...{/color}" (timeout=3.0, default=True):
            $ trauma += 10
            narrator "La peur vous paralyse. Les soldats vous bousculent violemment."

    
    # Chapitre 3 : Convoi
    scene bg_convoi with fade:
        zoom 1.20
        align (0.5, 0.5)
    

    narrator "Chapitre 3 : Le convoi vers Auschwitz-Birkenau."
    narrator "Le 13 avril 1944, Simone, sa mère et sa sœur sont déportées dans le convoi 71."
    narrator "Le voyage dure des jours, dans un wagon à bestiaux, où le temps se dissout dans la faim, la soif et la peur."

    menu:
        "Parler pour maintenir un lien humain malgré la peur":
            $ determination = min(determination + 5, 100)
            $ trauma = min(trauma + 3, 100)
            show simonejeune_parle at left with dissolve
            simone "Vous vous souvenez de la mer, à Nice ? Du soleil sur la Promenade des Anglais ?"
            hide simonejeune_parle
            show simonejeuneclose at left 
            show yvonne_parle at right with dissolve
            yvonne "Oui… C’était notre liberté."
            hide yvonne_parle
            show milou_parle at right with dissolve
            milou "Si on arrive à se souvenir de tout ça, peut-être qu’on peut encore croire à un après."
            hide milou_parle
        "Se taire pour observer, économiser ses forces et comprendre la situation":
            $ determination = min(determination + 3, 100)
            $ fatigue = min(fatigue + 5, 100)
            show simonejeuneclose at left with dissolve
            simone "(pensée) Chaque parole des gardes, chaque arrêt du train… tout peut avoir une importance."
            simone "(pensée) Je dois garder mon énergie. Il y aura un moment où il faudra décider très vite."
            hide simonejeuneclose

    $ fatigue = min(fatigue + 10, 100)
    $ trauma = min(trauma + 10, 100)
    call feedback_scene from _call_feedback_scene
    # Chapitre 4 : Bobrek
    scene bg_bobrek with fade:
        zoom 1.20
        align (0.5, 0.5)
    

    narrator "Chapitre 4 : Bobrek et le travail forcé."

    narrator "Quelques semaines plus tard, Stenia, une Kapo réputée pour sa cruauté, s’arrête devant Simone et lui prononce des paroles qui changerent  son destin."

    show stenia at right with dissolve
    stenia "Tu es trop belle et trop jeune pour mourir ici. Je vais t’envoyer à Bobrek."
    hide stenia

    show simonejeune_parle at left with dissolve
    simone "À condition que ma mère et ma sœur puissent se joindre à moi !"
    hide simonejeune_parle
    show simonejeuneclose at left

    narrator "Elles quittent alors toutes les trois Auschwitz pour Bobrek."

    narrator "Là-bas, Simone est affectée d’abord aux travaux de terrassement, puis à l’usine Siemens. Les journées sont épuisantes et la survie reste un combat quotidien."

    menu:
        "Insister pour protéger sa mère et sa sœur malgré les risques":
            $ determination = min(determination + 6, 100)
            $ fatigue = min(fatigue + 5, 100)
            show simonejeune_parle at left with dissolve
            simone "Je travaillerai autant qu’il le faudra, mais je ne les laisserai pas derrière moi."
            hide simonejeune_parle
            show simonejeuneclose at left
            narrator "Ce courage discret devient une forme de résistance intérieure."

        "Se montrer docile face à Stenia afin d’éviter des brutalités supplémentaires":
            $ trauma = min(trauma + 4, 100)
            show simonejeuneclose at left with dissolve
            simone "(pensée) Provoquer la violence ici pourrait nous coûter trop cher."
            hide simonejeuneclose
            show simonejeune_parle at left with dissolve
            simone "Je ferai ce que vous demandez."
            hide simonejeune_parle
            show simonejeuneclose at left
            show stenia at right with dissolve
            stenia "C’est mieux ainsi."
            narrator "Ce n’est pas de la faiblesse : c’est une stratégie de survie dans un système sans pitié."

    narrator "Les jours à Bobrek s’enchaînent, mêlant faim, froid et travail exténuant."
    $ fatigue = min(fatigue + 10, 100)

    call feedback_scene from _call_feedback_scene_1

   # -------------------------------------------------
# Chapitre 5 : Marche de la mort
# -------------------------------------------------

label chapitre_5:
    play music "audio/winterwind.mp3" loop
    scene bg_marche_mort with fade:
        zoom 1.20
        align (0.5, 0.5)

    narrator "Chapitre 5 : Janvier 1945 – La marche de la mort."
    
    show simonefatigue at center with dissolve
    simone "(pensée) Un pied devant l'autre. Le rythme de la mort est régulier, mais mon cœur bat plus fort que leurs bottes dans la neige. Je ne serai pas un chiffre de plus dans ce fossé."

    hide simonefatigue with dissolve
    call qte_marche from _call_qte_marche 
    
    scene bg_marche_mort with fade:
        zoom 1.20
        align (0.5, 0.5)
    
    show simonejeuneclose at left with dissolve
    simone "(pensée) Chaque pas est une décision... Mais si je tombe, que deviendront maman et Milou ?"

    menu:
        "Se fixer un but mental pour continuer à avancer":
            $ determination = min(determination + 10, 100)
            show simonejeune_parle at left with dissolve
            simone "J’imagine la mer à Nice... le soleil. Ils n'ont pas de prise sur mes souvenirs."
            hide simonejeune_parle

        "Soutenir une autre détenue au risque d’augmenter sa fatigue":
            $ fatigue = min(fatigue + 12, 100)
            $ determination = min(determination + 15, 100)
            hide simoneclose
            show simonejeune_parle at left
            simone "Tiens mon bras... On avance ensemble."
            hide simonejeune_parle
            show simonejeuneclose at left
            narrator "Dans l'inhumanité la plus totale, vous choisissez de rester humaine."

    call feedback_scene from _call_feedback_scene_2

    # Chapitre 6 : Bergen-Belsen
    scene bg_bergen_belsen with fade:
        zoom 1.20
        align (0.5, 0.5)
    play music "audio/determination_theme.mp3" fadein 2.0

    narrator "Chapitre 6 : Bergen-Belsen."
    narrator "Le 30 janvier 1945, Simone et sa sœur arrivent à Bergen-Belsen, un camp ravagé par la faim, la maladie et la promiscuité."
    narrator "La mort est partout, mais l’idée de survivre pour témoigner grandit."

    $ fatigue = min(fatigue + 10, 100)
    $ trauma  = min(trauma + 10, 100)

    menu:
        "Se promettre de témoigner si elle survit":
            $ determination = min(determination + 8, 100)
            show simonejeuneclose at left with dissolve
            simone "(pensée) Si je sors d’ici vivante, je parlerai. Il faudra que le monde sache."
            narrator "Cette promesse devient un fil invisible qui la relie à l’avenir."
        "Se concentrer uniquement sur le présent pour ne pas s’effondrer":
            $ trauma = min(trauma + 3, 100)
            show simonejeuneclose at left with dissolve
            simone "(pensée) Penser trop loin fait mal. Aujourd’hui, je dois seulement passer la prochaine heure."
            narrator "Survivre, ici, est déjà un acte immense."

    call feedback_scene from _call_feedback_scene_3

    # Après la libération
    scene bg_paris_jeune with fade:
        zoom 1.20
        align (0.5, 0.5)
    play music "audio/tristesse_camp.mp3" fadein 3.0
   


    narrator "Après la libération, Simone revient en France. Elle reprend ses études à la faculté de droit puis à l’Institut d’études politiques de Paris."
    narrator "Recommencer une vie n’efface pas le passé, mais permet de le transformer."

    menu:
        "Se consacrer d’abord à ses études et à sa reconstruction personnelle":
            $ determination = min(determination + 6, 100)
            $ trauma = max(trauma - 3, 0)
            show simonejeune_parle at left with dissolve
            simone "Je dois redevenir une étudiante, une femme libre, pour pouvoir porter ensuite ce passé."
            hide simonejeune_parle
            show simonejeuneclose at left
        "S’engager rapidement dans les associations de survivants":
            $ trauma = min(trauma + 5, 100)
            $ determination = min(determination + 4, 100)
            show simonejeune_parle at left with dissolve
            simone "Je ne peux pas me taire. Parler sera douloureux, mais c’est une responsabilité."
            hide simonejeune_parle
            show simonejeuneclose at left

    # Rencontre d’Antoine
    scene bg_antoine with fade:
        zoom 1.20
        align (0.5, 0.5)
   

    narrator "En 1946, Simone rencontre Antoine Veil. Ils se marient et construisent une famille."
    narrator "L’amour, la vie familiale et le travail coexistent avec la mémoire des camps."

    menu:
        "Chercher un équilibre entre vie familiale, carrière et mémoire":
            $ determination = min(determination + 4, 100)
            $ trauma = max(trauma - 4, 0)
            show simonejeune_parle at left with dissolve
            simone "Je veux aimer, travailler, et témoigner. Tout cela fait partie de qui je suis."
            hide simonejeune_parle
            show simonejeuneclose at left
            show antoine_parle at right with dissolve
            antoine "Nous porterons ce passé ensemble, Simone. Tu n’es plus seule."
            hide antoine_parle
            show antoineclose at right
        "Se consacrer fortement à la mémoire des déportés, quitte à moins se préserver":
            $ determination = min(determination + 6, 100)
            $ trauma = min(trauma + 3, 100)
            show simonejeune_parle at left with dissolve
            simone "Si nous nous taisons, d’autres parleront à notre place et déformeront l’histoire."
            hide simonejeune_parle
            show simonejeuneclose at left
            show antoine_parle at right with dissolve
            antoine "Alors je serai là pour t’aider à supporter ce poids."
            hide antoine_parle
            show antoineclose at right

    # Ministre de la Santé
    scene bg_ministere with fade:
        zoom 1.20
        align (0.5, 0.5)
    

    narrator "En 1974, Simone Veil devient ministre de la Santé. Elle porte le projet de loi légalisant l’interruption volontaire de grossesse."
    narrator "Face à des attaques violentes et à des propos odieux, elle garde une dignité inflexible."

    menu:
        "Répondre avec une fermeté calme face aux attaques":
            $ determination = min(determination + 7, 100)
            show simone_parle at left with dissolve
            simone "Messieurs, vos cris ne couvrent pas le silence de détresse des femmes que vous refusez d'entendre. Je n'ai pas survécu au pire pour reculer devant vos injures."
            $ determination = min(determination + 4, 100)
            $ trauma = max(trauma - 3, 0)
            show simone_parle at left with dissolve
            simone "Il faut convaincre, même ceux qui ont peur du changement. Je resterai ferme, mais je ne ferai de personne un ennemi."
            hide simone_parle
            show simoneclose at left

    # Parlement 
    scene bg_parlement_europeen with fade:
        zoom 1.20
        align (0.5, 0.5)

    narrator "En 1979, Simone Veil est élue députée européenne et devient la première présidente du Parlement européen élu au suffrage universel direct."
    narrator "Son histoire personnelle et ses combats inspirent une vision de l’Europe fondée sur la paix, la mémoire et les droits humains."

    menu:
        "Mettre l’accent sur la mémoire et la réconciliation entre les peuples":
            $ determination = min(determination + 3, 100)
            $ trauma = max(trauma - 3, 0)
            show simone_parle at left with dissolve
            simone "L’Europe doit se souvenir de ce qui a conduit aux camps, de cette nuit qui a failli engloutir toute trace d'humanité."
            simone "L'oubli est le meilleur allié de la barbarie. Si nous ne transmettons pas cette mémoire, la paix que nous avons bâtie ne sera qu'une parenthèse fragile."
            simone "Nous ne témoignons pas pour nous-mêmes, mais pour que les générations futures n'aient jamais à connaître le poids des barbelés et le silence des consciences éteintes."
        "Mettre l’accent sur les droits fondamentaux et l’égalité partout en Europe":
            $ determination = min(determination + 7, 100)
            show simone_parle at left with dissolve
            simone "Les droits des femmes, la dignité humaine, la justice sociale : ce sont les fondations d’une Europe solide."
            simone "La dignité humaine n'est pas un concept abstrait que l'on agite dans les salons ; c'est une exigence de chaque instant qui ne souffre aucune frontière."
            simone "Une Europe qui tolérerait l'injustice sociale ou l'asservissement des femmes renierait l'idéal même sur lequel elle a été bâtie après l'horreur des camps."
            simone "Nous ne construisons pas seulement un marché commun ou une monnaie ; nous forgeons un bouclier pour les droits fondamentaux."
            simone "Le droit des femmes à disposer d'elles-mêmes, l'égalité devant la loi, la protection des plus faibles... Voilà les seules fondations capables de résister au retour de l'arbitraire."
            simone "Tant que je porterai cette parole, je rappellerai que la liberté n'est jamais acquise : elle est un combat qui doit être mené au nom de toutes."
            hide simone_parle
            show simoneclose at left

    # Choix de la fin
    if determination >= 75:
        $ ending = "politique"
    elif trauma >= 55:
        $ ending = "mémoire"
    else:
        $ ending = "équilibre"
    play music "audio/pantheon_theme.mp3" fadein 1.0
    jump epilogue

# -------------------------------------------------
#  Épilogue
# -------------------------------------------------

label epilogue:
    scene bg_paris with fade:
        zoom 1.20
        align (0.5, 0.5)
    

    narrator "Les années ont passé. Simone Veil s’éteint en 2017, après une vie consacrée à la justice, à la mémoire et à la dignité humaine."
    narrator "En 2018, Simone et Antoine Veil entrent au Panthéon. C’est la reconnaissance d’une existence qui, partie de l’horreur des camps, a contribué à transformer la société."

    if ending == "politique":
        narrator "Par ses combats politiques, elle a inscrit dans la loi la protection de droits essentiels, en particulier ceux des femmes."
        narrator "Au Parlement, en France comme en Europe, elle a montré qu’une survivante des camps pouvait transformer son expérience en volonté de bâtir une société plus juste."
        narrator "Son héritage politique rappelle que les droits conquis doivent sans cesse être défendus."

    elif ending == "mémoire":
        narrator "Par son témoignage, Simone Veil a laissé une marque profonde."
        narrator "Elle a parlé avec sobriété, sans pathos, mais avec une exigence inflexible de vérité."
        narrator "Ses mots continuent d’alerter contre la haine, le racisme et l’antisémitisme, rappelant que l’oubli ouvre toujours la porte aux mêmes dérives."

    else:
        narrator "Simone Veil a trouvé un équilibre rare : construire une famille, mener une carrière exigeante et porter la mémoire des disparus."
        narrator "Elle a montré qu’une vie marquée par le tragique peut aussi être faite d’amour, de travail, de rires, de projets et de victoires."
        narrator "Son parcours invite à ne pas réduire une personne à son trauma, mais à reconnaître la richesse de toute une existence."

    narrator "En retraçant son histoire, nous sommes invités à protéger les droits conquis, à refuser la banalisation de la haine et à faire de la mémoire un levier pour l’avenir."


    hide screen stats_overlay

    call screen ecran_fin(determination, fatigue, trauma, a_carnet, a_peluche)
    
    
    return

label qte_marche:
    show layer master at blur(4)
    
    call screen bouton_survie
    $ _qte_result = _return

    show layer master at blur(0)

    if _qte_result == "success":
        $ determination = min(determination + 10, 100)
        # On ne montre rien ici pour laisser le chapitre 5 gérer les sprites
    else:
        $ fatigue = min(fatigue + 20, 100)
        $ trauma = min(trauma + 10, 100)
        with hpunch
        scene fatigue_scene with dissolve
        # On s'assure que TOUT est caché pendant l'écran noir
        hide simonefatigue
        hide simoneclose
        narrator "Vos forces vous abandonnent. La neige devient votre seul linceul..."
        pause 1.0
    
    return

screen ecran_fin(determination_finale, fatigue_finale, trauma_final, carnet_trouve, peluche_trouvee):
    add Solid("#000")
    
    vbox:
        align (0.5, 0.4)
        spacing 40
        
        text "FIN DU PARCOURS" size 60 color "#fff" xalign 0.5
        
        hbox:
            spacing 100
            xalign 0.5
    
            vbox:
                spacing 15
                text "BILAN" size 30 color "#c04f8a" xalign 0.5
                text "Détermination : [determination_finale]%" size 22 color "#fff"
                text "Fatigue accumulée : [fatigue_finale]%" size 22 color "#fff"
                text "Traumatisme : [trauma_final]%" size 22 color "#fff"
            
            vbox:
                spacing 15
                text "MÉMOIRE" size 30 color "#c04f8a" xalign 0.5
                hbox:
                    spacing 20
                    if carnet_trouve:
                        add "images/icon_carnet.png" zoom 0.3
                    if peluche_trouvee:
                        add "images/icon_peluche.png" zoom 0.3
                    if not carnet_trouve and not peluche_trouvee:
                        text "Aucun objet n'a survécu." size 18 italic True color "#aaa"
        
    textbutton "RETOURNER AU MENU PRINCIPAL":
        align (0.5, 0.85)
        text_size 25
        text_color "#fff"
        text_hover_color "#c04f8a"
        action MainMenu()