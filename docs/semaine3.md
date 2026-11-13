# Semaine 3 : l'API, notes du binôme

> Deux questions, quelques phrases chacune. Répondez avec ce que vous avez observé, pas avec le cours.

## 1. Pourquoi l'API refuse-t-elle de démarrer sans `models/sentiment.joblib`, plutôt que de démarrer et de répondre 503 ?

Le chargement est fait dans le `lifespan` : si `models/sentiment.joblib` manque, `charger_modele()` lève une `FileNotFoundError` et le démarrage échoue. Ainsi, le service ne se présente pas comme prêt alors qu'il ne peut traiter aucune prédiction ; `/health` ne renvoie 200 qu'une fois le modèle chargé. Le 503 de `_classifier()` couvre plutôt le cas où l'application tourne sans classifier disponible.

## 2. Un texte vide est refusé deux fois : par Pydantic, puis par `predict()`. Est-ce redondant ?

Pour une requête HTTP, la validation Pydantic rejette le texte vide avant d'appeler le modèle et renvoie 422. La vérification de `predict()` est néanmoins utile comme garde indépendante, car cette fonction peut aussi être appelée directement hors de l'API ; elle garantit alors la même règle d'entrée. Les deux contrôles protègent donc deux frontières différentes.
