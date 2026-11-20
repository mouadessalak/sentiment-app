# Semaine 5 : l'interface, notes du binôme

> Trois questions, quelques phrases chacune. Répondez avec ce que vous avez observé.

## 1. Pourquoi l'interface n'importe-t-elle jamais `predict()` ni le fichier `.joblib` ?

L'interface envoie les textes à `POST /predict` avec `ui.client`. Le modèle reste ainsi dans le service API : on peut le réentraîner ou le remplacer sans dupliquer sa logique ni modifier la page. Les tests de TP5 ont utilisé l'API en mémoire et confirmé les réponses attendues sans charger le modèle depuis l'interface.

## 2. Que montre l'interface quand le modèle hésite, et pourquoi est-ce mieux qu'un verdict forcé ?

Pour « xqzvb wlkptr grombu », l'interface affiche « Je ne sais pas : à faire vérifier par un humain », une confiance de 52 %, puis précise que la confiance est sous le seuil d'abstention. L'API retourne `INDETERMINE` en dessous de 0,60. Ce message évite de présenter une prédiction peu fiable comme une certitude et indique à l'agent du service client quoi faire.

## 3. Que voit l'utilisateur quand l'API tombe ? Et le fichier `data/avis_exemple.csv` : combien d'avis partent vers un humain ?

Quand l'API est injoignable, la page affiche « API injoignable : lancez d'abord uvicorn api.main:app » ; le test de page confirme ce message. L'analyse de `data/avis_exemple.csv` via l'API donne 3 avis positifs, 2 négatifs et 1 `INDETERMINE` : un avis part donc vers un humain.
