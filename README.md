# Hackaviz-2024: Les épreuves des Jeux Olympiques et Paralympiques de Paris 2024

![](images/clipboard-1507555475.png)

Nous vous proposons cette année un jeu de données sur les épreuves des Jeux de Paris 2024.\
Le jeu de donnée principal est agrémenté d'un jeu subsidiaire sur les lieux de restauration à proximité des épreuves.

Retrouvez les règles et les modes d’évaluation sur la page des [règles de l’Hackaviz](https://toulouse-dataviz.fr/hackaviz/2024-contest/) de l’association [Toulouse DataViz (TDV)](http://toulouse-dataviz.fr/).

N’hésitez pas à nous contacter sur [le salon Discord](https://discord.gg/XSDEKX7thr) du Toulouse DataViz pour discuter entre participants, si vous avez besoin d’aide à propos des données ou pour rapporter des erreurs dans le jeu de données.

Bonne chance !

## Format des données

Chaque jeu de donnée est disponible dans plusieurs formats à votre convenance:

-   xlsx

-   csv

-   parquet

Une aide à la lecture du format parquet  peut être trouvée [sur cette page](https://toulouse-dataviz.github.io/hackaviz-2024/chargement_des_donnees.html).

## Description des données `paris_2024`

Le jeu de données `paris_2024` contient chacune des sessions programmées aux jeux 2024

| Nom de colonne      | Description                                                                                        | Exemple                           |
|------------------|------------------------------------|------------------|
| Jeux                | Jeux Olympiques ou Paralympique                                                                    | Paralympiques                     |
| Discipline          | La discipline olympique                                                                            | Para Taekwondo                    |
| Épreuve             | description de l'épreuve                                                                           | K44 +80 kg                        |
| Phase               | phase de l'épreuve                                                                                 | Matchs pour la médaille de bronze |
| Genre               | épreuve Mixte, Femmes ou Hommes                                                                    | Femmes                            |
| Début               | date et heure de démarrage de l'épreuve                                                            | 2024-08-09 18:15:00.00            |
| Fin                 | date et heure de fin de l'épreuve                                                                  | 2024-08-09 22:00:00.00            |
| Lieu                | le site ou le stade de l'épreuve                                                                   | Arena Champ-de-Mars               |
| Session             | le code de la session pour acheter vos billets                                                     | PTKW06                            |
| latitude            | la latitude géographique du `Lieu`                                                                 | 48.866                            |
| longitude           | la latitude géographique du `Lieu`                                                                 | 2.3124                            |
| ville               | la ville accueillant l'épreuve et son code de département                                          | Paris (75)                        |
| capacité            | la capacité d'accueil du public du `Lieu`                                                          | 3349                              |
| Enjeu               | l'enjeu de l'épreuve, parmi Cérémonie, Médailles ou Qualifications.                                | Qualifications                    |
| Catégorie_First     | Le prix des places pour la catégorie "First" (€).                                                  | 100                               |
| Catégorie_A         | Le prix des places pour la catégorie A (€).                                                        | 80                                |
| Catégorie_B         | Le prix des places pour la catégorie B (€).                                                        | 65                                |
| Catégorie_C         | Le prix des places pour la catégorie C (€).                                                        | 50                                |
| Catégorie_D         | Le prix des places pour la catégorie D (€).                                                        | 35                                |
| Catégorie_E+        | Le prix des places pour la catégorie E+ (€).                                                       | 250                               |
| Catégorie_E         | Le prix des places pour la catégorie E (€).                                                        | 90                                |
| Catégorie_First_PFR | Le prix des places pour la catégorie "First" des publics en fauteuil roulant et accompagnants (€). | 55                                |
| Catégorie_A_PFR     | Le prix des places pour la catégorie A des publics en fauteuil roulant et accompagnants (€).       | 25                                |
| Catégorie_B_PFR     | Le prix des places pour la catégorie B des publics en fauteuil roulant et accompagnants (€).       | 15                                |

*Dictionnaire de données de `Paris_2024`*

## Description des données `restaurants_proximité`

Le jeu de données `restaurants_proximité` est une liste de restaurants avec leur distance à un des site des jeux de Paris.

| Nom de colonne    | Description                                                                                                                    | Exemple                        |
|------------------|------------------------------------|------------------|
| Etablissement     | le nom de l'établissement                                                                                                      | LE CAFE DU MARCHE              |
| création          | la date de création de l'établissement                                                                                         | 2016-12-31                     |
| premiere_activité | la date de première activité                                                                                                   | 2018-06-16                     |
| adresse           | son adresse                                                                                                                    | 59 Rue de Ponthieu 75008 Paris |
| Type              | Le type d'établissement dans la base SIREN, parmi Restauration traditionnelle, Restauration de type rapide, Débits de boissons | Restauration traditionnelle    |
| latitude          | la latitude de l'établissement  (hors format geoparquet)                                                                                               | 2.318                          |
| longitude         | la longitude de l'établissement  (hors format geoparquet)                                                                       | 48.86                          |
| coordonnées         | le point de coordonnée (latitude longitude)  (format geoparquet uniquement) |                          |
| distance          | la distance de l'établissement au stade ou au site des Jeux de Paris (m).                                                      | 1090                           |
| Lieu              | le site ou le stade de l'épreuve des Jeux                                                                                      | Arena Champ-de-Mars            |
| ville             | la ville accueillant l'épreuve et son code de département                                                                      | Paris (75)                     |
| capacité          | la capacité d'accueil du public du `Lieu`                                                                                      | 3349                           |

*Dictionnaire de donnée de `restaurants_proximité`*

## Description des formats de fichiers

Pour chaque jeu de données, nous avons tenté de vous faciliter la tâche
en vous fournissant les fichiers sous plusieurs formats :

| Extension du fichier | Format                          | Outils de prédilection                                                       |
|----------------------|---------------------------------|------------------------------------------------------------------------------|
| parquet              | parquet, un format binaire compressé | langages de programmation:  R, python, observable.hq, … |
| geoparquet              | parquet, un parquet supportant le format geospatial | langages de programmation:  R, python, observable.hq, … |
| xlsx                 | Office Open XML pour tableurs   | Libre Office Calc, Open Office Calc, Microsoft Excel, …                                |
| csv             | CSV, avec séparateur `,` et décimales `.` | tous les autres outils |


# Télécharger les données

## Ensemble des données
Toutes les données sont dans le répertoire `/data/` de l'archive zip si vous cliquez sur [télécharger Hackaviz_2024.zip](https://github.com/Toulouse-Dataviz/hackaviz-2024/archive/refs/heads/main.zip)

