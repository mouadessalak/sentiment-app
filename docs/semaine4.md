# Semaine 4 : tests approfondis et qualité, notes du binôme

> Une à deux pages. Uniquement des chiffres issus de VOS exécutions.

## 1. Couverture

- Avant (étape A) : 91 %, lignes jamais exécutées : `api/main.py:49,77-79,85-87`.
- Ligne 49 : le cas 503 d'un modèle retiré de `app.state` n'était pas testé. Lignes 77-79 : une panne du modèle n'était pas simulée. Lignes 85-87 : le bloc de lancement direct `uvicorn` n'est pas exécuté par les tests.
- Après (étape D) : 98 % ; aucune ligne exclue par `# pragma: no cover`. Le bloc `if __name__ == "__main__"` reste le seul bloc non exécuté par la suite, car les tests utilisent le démarrage ASGI réel.

## 2. Défauts trouvés

| Symptôme | Test qui l'a révélé | Correction |
| --- | --- | --- |
| `{"text":"   "}` était accepté alors que `{"text":""}` était refusé | `test_propriete_texte_blanc` et les cas limites | `field_validator` Pydantic avec la règle `text.strip()` |
| Les deux formes de 422 étaient possibles : texte vide Pydantic ou exception du modèle | `test_frontieres_du_contrat` | validation dans le schéma ; toute exception de prédiction retourne 500 |
| Texte hors vocabulaire reçu une étiquette avec faible confiance | `test_propriete_texte_contractuel` | seuil `SEUIL_ABSTENTION = 0.60` et verdict `INDETERMINE` |
| `.upper()` masquait les classes du modèle dans un contrat faiblement typé | mypy sur le contrat explicité | `Literal` et correspondance explicite des classes |
| Modèle avec une classe inconnue pouvait démarrer | `test_classes_inattendues_refusent_de_demarrer` | vérification exacte des classes attendues au démarrage |
| Modèle absent ou non chargé pouvait produire des états différents | tests d'intégration T20 et modèle non chargé | cache vidé au test absent ; `_classifier` retourne 503 |

## 3. Seuil d'abstention

- Courbe sur le jeu de démonstration : seuil 0.55, 47 avis sur 58 (81 %), exactitude 91.5 % ; seuil 0.60, 42 avis (72 %), exactitude 95.2 % ; seuil 0.65, 41 avis (71 %), exactitude 97.6 %.
- Seuil retenu : 0.60. Il envoie 16 avis sur 58 (27.6 %) vers un humain et évite 5 des 7 erreurs du modèle sans aller à 0.65 avec une réduction supplémentaire limitée. Sur ces 58 avis, la sélection à 0.60 conserve 42 réponses et fait passer l'exactitude de 87.9 % à 95.2 %.

## 4. Jeu d'or

- Bilan : 7 avis justes, 11 abstentions et 2 erreurs franches déclarées avec leur raison.
- Les deux erreurs franches sont conservées au lieu d'être retirées : `Très déçu...` est déclarée pour la calibration négative, et `Le livre...` pour le mélange entre avis livre et livraison.
- Ces chiffres montrent que le seuil protège contre plusieurs cas ambigus, tout en laissant les erreurs connues visibles au modèle maintenu.

## 5. Outils statiques

- Remarques au départ : 23 erreurs Ruff ; mypy : aucune remarque sur les 4 fichiers API.
- Ruff a relevé notamment les exceptions mal chaînées, les imports et quelques variables ambiguës. Mypy ne pouvait pas vérifier les étiquettes tant que `predict()` retournait un dictionnaire non typé ; après ajout des `TypedDict`, `Literal` et vérification des classes, il reste muet sur 4 fichiers.
- Les défauts comportementaux ont surtout été trouvés par pytest/hypothesis et l'intégration ; les outils statiques ont complété les garde-fous mais n'ont pas remplacé les tests.
