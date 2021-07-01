# testEaseDeploy
Platforme Web pour automatiser les déploiements

Problématique

De nos jours, les projets ont tendance à devenir de plus en plus imposants, avec parfois de nombreux intervenants. Il est donc nécessaire de développer des méthodes qui permettent de faciliter le travail de chacun des membres du groupe, mais aussi de simplifier les étapes d’intégration des nouveaux composants dans le projet.
En plus, une des difficultés majeures dans la qualité d'un projet est le fait de pouvoir détecter que le code comporte des erreurs ou des dysfonctionnements, plus communément appelés « bogues ». 
Un des challenges pour assurer un certain niveau de qualité est de détecter au plus tôt ces anomalies. Plus une erreur est identifiée rapidement, plus le temps nécessaire pour la corriger est court. Il serait donc nécessaire de passer un temps extrêmement important pour écrire les tests contrôlant ces lignes de code.

C’est dans ce contexte que l’utilisation du processus de l’intégration continue entre en jeu afin d’avoir un regard permanent sur l’état des développements ainsi que sur la qualité du code et automatiser les tests et la fusion des modifications dans un référentiel partagé. En effet, le but est de détecter au plus vite l’ajout d’éventuels problèmes ou erreurs au code existant, ainsi que de contrôler la qualité du code. Cela passe par la détection d’erreurs, la vérification des résultats des tests, la vérification de leur couverture, ou encore la détection de code dupliqué. 

Un projet doit passer par une phase finale avant d’être utilisé par les utilisateurs. C’est une phase, à la fois, importante et critique dans le cycle de vie du logiciel. Elle permet de livrer le logiciel aux utilisateurs et ainsi avoir des retours d’expérience d’utilisation. Elle est critique et le risque qu’il y ait des problèmes est toujours présent. 

Les pipelines CI/CD

Afin de rendre cette phase plus maîtrisable, il a eu recours au déploiement continue « CD ». Ce processus permet la mise à disposition automatique des évolutions ou des correctifs directement depuis le référentiel vers l'environnement de production, où elles seront utilisées par les utilisateurs finaux. Il permet aussi de réduire les charges de test, d’exploitation et de pilotage afférents à l'étape de mise en production.

Critique de l'existant

Le problème des solutions existantes est que certaines d’entre-elles sont payantes ce qui limite l’accès aux entreprises et à ceux pouvant supporter de payer pour le déploiement de leurs codes.
Certes, il y a de nombreux outils parmi ceux proposés qui sont Open Source et ont prouvé leurs efficacités dans le domaine du DevOps. Cependant, ces outils requièrent que l’utilisateur les installe proprement sur sa machine, les maîtrise et exigent parfois que l'utilisateur connaisse les commandes nécessaires pour cet outil. 
Pour un développeur, ceci pourrait lui coûter du temps et d’effort supplémentaires à préparer l’environnement de l’outil qu’il utilise ou à apprendre à l’utiliser.

Solution proposée

C'est dans ce cadre qu'est né le projet de mettre à disposition des développeurs une plateforme sur laquelle ils peuvent automatiser leurs builds et leurs déploiements avec un pipeline d’intégration et de déploiement continue (CI/CD).
L'objectif étant de soulager les développeurs de toutes les tâches d'administration système et réseau (authentification, sauvegarde, mises à jour de sécurité, etc.) en leur offrant un service clés en main.

Étant connectée à des outils Open Source du DevOps, cette plateforme permet à l'utilisateur de faire passer le code source venu d’un système de contrôle de versions (Git) par toutes les étapes du pipeline d’automatisation qui sont :

La création : compilation de l'application

Lancement des tests : tests unitaires et tests d'intégration

Mesure de la qualité de code

Déploiement : déploiement du code en production



Technologies utilisées
*Python et Flask
*Outil de gestion de version : Git  GitHub
*Outil d’orchestration : Jenkins
*Technologie de conteneurisation : Docker
*Outil de mesure de la qualité du code : SonarQube
*Technologie de configuration d’ordinateurs : Ansible



