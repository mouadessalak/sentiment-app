# Fiche de cadrage : Ordonnances incomplètes en pharmacie

> Remplir chaque rubrique en une à trois phrases. Les rubriques marquées (obligatoire) sont vérifiées par `pytest`.

## Besoin en une phrase (obligatoire)
Une pharmacie d'officine veut détecter, à la saisie d'une ordonnance, les mentions réglementaires manquantes (prescripteur, date, posologie, durée, identité du patient) avant de délivrer le médicament.

## Utilisateur final (obligatoire)
Le pharmacien d'officine et son préparateur, au comptoir, au moment de la réception de l'ordonnance et avant la délivrance.

## Approche retenue (obligatoire)

Cocher une seule case :

- [X] Règles métier
- [ ] Machine learning
- [ ] RAG
- [ ] Modèle génératif seul

## Justification (obligatoire, citer au moins deux critères de la grille : (a) données étiquetées, (b) vérifiabilité, (c) coût par requête, (d) conséquence d'une erreur)
Les mentions obligatoires d'une ordonnance sont fixées par le Code de la santé publique : la liste est finie, connue et vérifiable (b) — on peut contrôler chaque champ de façon déterministe et expliquer précisément pourquoi l'ordonnance est refusée. Les données étiquetées (a) sont inutiles ici : il n'y a pas de vérité à apprendre, seulement des champs à contrôler. Le coût par requête (c) est quasi nul (règles locales), ce qui compte pour une officine à fort volume. Enfin, la conséquence d'une erreur (d) est grave et asymétrique (délivrance sur ordonnance invalide, risque juridique et sanitaire), ce qui plaide pour un contrôle déterministe et explicable plutôt qu'une prédiction probabiliste.

## Données nécessaires et leur origine (obligatoire)
La liste réglementaire des mentions obligatoires (Code de la santé publique, arrêtés) constitue la base de règles. En entrée : les champs saisis ou scannés de l'ordonnance (identité patient, prescripteur, date, médicament, posologie, durée). Aucune donnée d'entraînement n'est requise ; un jeu de test d'ordonnances complètes/incomplètes, anonymisées, suffit pour valider.

## Métrique de succès et seuil d'acceptation (obligatoire)
Taux de détection des mentions manquantes (rappel) et taux de fausses alertes (précision). Seuil : rappel ≥ 99 % sur les mentions obligatoires (ne jamais laisser passer une ordonnance invalide) et précision ≥ 95 % pour ne pas bloquer abusivement les ordonnances valides ; l'outil ne bloque jamais seul, il alerte.

## Conséquence d'une erreur et validation humaine prévue (obligatoire)
Un faux négatif (mention manquante non signalée) peut conduire à une délivrance irrégulière : conséquence juridique et sanitaire. Un faux positif ralentit le comptoir. Le système alerte et liste les champs manquants, mais la décision de refuser ou de demander une régularisation reste au pharmacien, qui valide et documente son choix.

## Risques éthiques ou de confidentialité (obligatoire)
Données de santé et données personnelles (identité patient, prescripteur, traitement) : traitement local, minimisation, pas de transfert vers un tiers sans base légale. Risque de sur-blocage d'ordonnances valides (patients chroniques, prescriptions particulières) et de pression sur le pharmacien ; prévoir une revue des alertes et une procédure de dérogation tracée.

## Approche écartée et pourquoi (facultatif)
Modèle génératif seul écarté : il pourrait inventer une mention ou mal interpréter une posologie, sans garantie de vérifiabilité, pour un coût par requête et un risque d'erreur injustifiés face à une liste de règles finie. RAG écarté également : la base de connaissances réglementaire est stable et structurée, un simple référentiel de règles suffit, sans recherche sémantique.
# Fiche de cadrage : Ordonnances incomplètes en pharmacie

## Approche retenue
- [x] Référentiel de règles