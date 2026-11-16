# Fiche de cadrage : Questions sur le règlement intérieur

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Une université veut un assistant qui répond aux questions des étudiants et du personnel sur le règlement intérieur (assiduité, discipline, examens, sanctions) à partir du texte officiel en vigueur.

## Utilisateur final (obligatoire)
Les étudiants et le personnel administratif, sur le portail web de l'université, en libre-service ; le service de scolarité pour relire les cas litigieux.

## Approche retenue (obligatoire)

Cocher une seule case :

- [ ] Règles métier
- [ ] Machine learning
- [x] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
La vérifiabilité (b) est décisive : chaque réponse doit citer l'article du règlement et sa version, ce que le RAG permet en ancrant la génération dans le texte retrouvé. Les données étiquetées (a) ne sont pas nécessaires : le règlement lui-même constitue la base documentaire, sans corpus de questions/réponses annotées. Le coût par requête (c) reste modéré (un petit modèle + recherche sur un corpus restreint), et la conséquence d'une erreur (d) est réelle — une réponse fausse sur une sanction ou une assiduité peut induire l'étudiant en erreur — ce qui justifie l'ancrage documentaire plutôt qu'un modèle génératif libre.

## Données nécessaires et leur origine (obligatoire)
Le règlement intérieur officiel en vigueur (PDF/DOCX du service juridique), ses annexes et ses versions antérieures datées. Éventuellement, une foire aux questions validée par la scolarité pour couvrir les formulations fréquentes. Aucune donnée personnelle n'est nécessaire en base documentaire.

## Métrique de succès et seuil d'acceptation (obligatoire)
Taux de réponses correctement ancrées (citation d'un article existant et pertinent) et taux de refus explicite quand le corpus ne couvre pas la question. Seuils : exactitude de l'article cité ≥ 95 % sur un jeu de test de questions validées par la scolarité, et 0 % de réponse inventée acceptée (toute réponse sans source doit être refusée).

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Une réponse erronée sur une règle (sanction, absence, fraude) peut avoir des conséquences pour l'étudiant. Le système affiche toujours l'article source et sa date ; en cas de doute ou d'absence de source, il renvoie vers le service de scolarité au lieu de répondre. Une revue périodique des questions non couvertes alimente la mise à jour du corpus.

## Risques éthiques ou de confidentialité (obligatoire)
Risque d'hallucination sur un texte réglementaire (atténué par l'ancrage et le refus sans source) ; risque de version obsolète si le corpus n'est pas mis à jour (prévoir un versionnage daté). Les questions des utilisateurs peuvent contenir des données personnelles (situation individuelle) : ne pas les conserver en clair, ne pas les utiliser pour entraîner le modèle, et orienter les cas individuels vers un humain.

## Approche écartée et pourquoi (facultatif)
Modèle génératif seul écarté : sans ancrage, il peut inventer un article ou une sanction, avec un risque inacceptable sur un texte réglementaire. Règles métier écartées : les questions sont en langage libre et varié, un simple arbre de décision ne couvre pas la formulation des usagers ; les règles servent seulement à filtrer les cas individuels.
