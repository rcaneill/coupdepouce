# Création et utilisation d'un compte professeur

## Création du compte

Afin de créer un compte professeur il suffit de se rendre sur la page suivante :
[création compte professeur](/account/create-account-admin). *Attention, la page
n'est pas la même que pour la création d'un compte élève !*

![create account admin](/static/create-account-admin.png)

Une adresse email valide est demandée afin de valider votre compte et de
réinitialiser votre mot de passe si nécessaire.
**Aucun email commercial ne vous sera envoyé et votre adresse email ne
sera jamais diffusée.**

Une fois le compte créé, il faut cliquer sur le lien envoyé par email afin
de valider votre adresse. Vous pouvez ensuite vous connecter.

## Vue générale

Nous allons ici utiliser le compte virtuel de *Edmond Dantès*
(plus connu sous le nom du comte de Monte Cristo).
Il faut maintenant cliquer sur l'onglet `Espace professeur` de la
barre de navigation située en haut de la page.
Vous tomberez sur la page d'intérêt principal pour vous.

![](/static/admin.png)

Trois sections sont disponibles pour vous:

1. La section *élèves* regroupe tous vos élèves. Un élève peut vous être associé
tous seul, ou bien aussi appartenir à une ou plusieurs classes.
2. La section *classes* contient vos classe. Une classe contient des élèves,
et des activités associées.
3. La section *activités* contient vos activités. Une activité correspond
à une activité documentaire, un DM, une feuille d'exercices, etc. Chaque
activité contient elle des questions, et des coups de pouce associés aux questions.

### Section élèves

Nous n'avons pour le moment aucun élève. Pour ajouter des élèves, deux solutions.
Si l'élève possède déjà un compte, vous pouvez cliquer sur `Ajouter un élève`
et renseigner l'adresse mail qu'il utilise pour se connecter au site.
Sinon vous pouvez créer le compte pour votre élève en cliquant sur
`Créer des comptes pour vos élèves`.
Ajoutons ici un élève virtuel pour s'entrainer (cet élève est accessible
à tous, vous pouvez l'ajouter vous aussi si vous le souhaitez).
Cet élève s'appelle Merlin L'Enchanteur, et son nom d'utilisateur est
*merlin*. Si l'on clique sur le nom d'un de ses élèves, il est possible
de l'ajouter ou l'enlever d'une classe ainsi que d'accéder à l'historique
de son utilisation des coups de pouce. Ici nous n'avons pas encore créé de classe,
tout est donc vide.

![](/static/student.png)


### Section classes

Cette section contient vos classes, les élèves qu'elles contiennent et les
coups de pouce associés. Créons une classe appelée *La Classe de Monte Cristo*
et cliquons dessus pour ouvrir son onglet.

![](/static/classe.png)

Vous pouvez ajouter l'élève Merlin par deux moyens : en cliquant sur `Ajouter des élèves`
dans la classe, ou bien via la section élèves. Nous ajoutons donc Merlin à cette
classe.


### Section activités

Le fonctionnement de cette section est très similaire aux deux sections
précédentes : il est possible de créér des activités et de voir
les activités déjà existantes.

#### Création d'une activité

Lorsque l'on clique sur créer une activité, nous arrivons sur l'éditeur.
Celui ci est basé sur trois principes :

1. Toute activité a un titre
2. Une activité contient plusieurs questions
3. Chaque question contient un ou plusieurs coups de pouce

Créons une activité sur les propriétés de l'eau. Le titre de l'activité
est donc : *Les propriétés de l'eau*. En cliquant sur le bouton `+Question` nous créons
une question. Appelons la : *1.3 Quels sont les changements d'état de l'eau ?*
(évidemment, nommez les question en accord avec les question de votre activité).
Nous créons maintenant un premier coup de pouce pour cette question,
rappelant dans quel section du cours l'élève doit se référer : *Voir cours,
chapitre N, paragraphe P*. Il est possible de créer un coup de pouce plus avancé
pour les élèves ayant encore besoin d'aide : *Définition de la fusion : [...]*.
Et ainsi de suite pour chaque question de l'activité nécesitant un coup de pouce.
Il ne reste plus qu'à cliquer sur `Éditer l'activité`.

Maintenant si l'on affiche les activités, notre nouvelle activité est affichée.
Il est possible de l'ajouter à une ou plusieurs classes. Elle devient donc
accessibles aux élèves desdites classes.

![](/static/activity.png)

Il est possible d'éditer une activité tant qu'aucun élève n'a demandé de coup de pouce.
La fonction d'édition des activités est en cours de programmation et n'est pas encore
terminée.

Vous pouvez afficher l'historique d'accès d'une activité en cliquant sur
`Afficher les logs`. L'horaire exact n'est pas indiqué afin de ne pas
créer de discrimination involontaire de la part des professeurs,
mais la plage horaire est indiquée (matin : de minuit à midi, après-midi : de midi à minuit)
ainsi que la date.