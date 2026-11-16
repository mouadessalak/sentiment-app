# Fiche de cadrage : Priorisation des avis négatifs

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Une marque veut classer par priorité les avis clients négatifs publiés en ligne afin que l'équipe relation client traite d'abord les plus urgents (tonalité forte, risque de viralité, problème grave).

## Utilisateur final (obligatoire)
L'équipe relation client / modération de la marque, qui consulte une file d'avis triée et décide du traitement (réponse, escalade, contact privé)

## Approche retenue (obligatoire)

Cocher une seule case :

- [x] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
Les données étiquetées (a) existent ou sont construites facilement : historique d'avis avec priorité attribuée par l'équipe (urgent / non urgent), ce qui permet d'apprendre un classifieur de priorité. Le coût par requête (c) est faible une fois le modèle entraîné, et le volume d'avis est élevé, ce qui rend une automatisation rentable. La vérifiabilité (b) est partielle : on peut expliquer les facteurs (mots-clés, tonalité, note) mais pas garantir une décision « juste » ; c'est pourquoi l'humain garde la main. La conséquence d'une erreur (d) est modérée : un avis urgent mal classé peut être traité en retard (risque de viralité), mais rien n'est publié automatiquement — d'où un classifieur d'aide au tri, pas de décision autonome.

## Données nécessaires et leur origine (obligatoire)
Historique des avis clients (texte, note, date, canal) et étiquettes de priorité issues du traitement passé par l'équipe relation client (délai de réponse, escalade, résolution). Enrichissement possible : indicateurs de gravité (mots-clés de problème grave, ancienneté du client, récurrence). Les données doivent être anonymisées et le jeu d'entraînement validé par l'équipe.

## Métrique de succès et seuil d'acceptation (obligatoire)
Mesurer le rappel sur les avis urgents (ne pas manquer un avis prioritaire) et la précision (ne pas saturer la file d'avis non urgents). Seuils : rappel urgent ≥ 90 % et précision ≥ 80 % sur un jeu de test tenu à l'écart ; à défaut, l'outil reste en mode suggestion.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un avis urgent classé non urgent retarde la réponse (image, viralité) ; un avis non urgent classé urgent consomme du temps. Le système propose un ordre de priorité avec les facteurs explicatifs, mais un agent valide ou corrige avant traitement ; les corrections alimentent le réentraînement.

## Risques éthiques ou de confidentialité (obligatoire)
Données personnelles des clients (avis nominatifs, coordonnées) : minimisation, anonymisation pour l'entraînement, pas de profilage sensible. Risque de biais (sous-priorisation de certaines formulations, langues, clients) et de dérive vers un tri opaque : journaliser les décisions, auditer régulièrement, garder l'humain décisionnaire.

## Approche écartée et pourquoi (facultatif)
Règles métier seules écartées : la priorité dépend de signaux combinés (ton, gravité, récurrence) que des seuils fixes capturent mal. Modèle génératif seul écarté : coûteux par requête et non déterministe pour une simple tâche de tri. RAG écarté : il n'y a pas de corpus documentaire à citer, mais un classement à produire
