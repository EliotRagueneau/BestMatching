import random


class Membre:
    def __init__(self, nom: str, liste_ordonnee_choix: str):
        self.nom = nom
        self.liste = [int(choix) - 1 for choix in liste_ordonnee_choix.split('>')]

        self.sadness = 0
        self.current_choice = self.liste[0]

    def next_choice(self) -> int:
        self.sadness += 1
        self.current_choice = self.liste[self.sadness]
        return self.current_choice

    def is_last_choice(self):
        return self.sadness + 1 == len(self.liste)

    def __repr__(self):
        return "{} : projet n°{}".format(self.nom, self.current_choice + 1)


class Projet:
    def __init__(self, nom: str):
        self.membres = []
        self.nom = nom

    def add_member(self, member: Membre) -> Membre:
        self.membres.append(member)
        if len(self.membres) > 5:
            return self.__downgrade_one__()

    def __downgrade_one__(self) -> Membre:
        to_remove = random.choice(self.membres)
        if not to_remove.is_last_choice():
            self.membres.remove(to_remove)
            return to_remove
        else:
            self.__downgrade_one__()

    def __repr__(self):
        return "{} :\n\t-".format(self.nom) + "\n\t-".join([str(membre) for membre in self.membres])


class Matching:
    def __init__(self):
        self.list_projets = [Projet("1. Il y a un ver au plafond !!! "),
                             Projet("2. Visualisation de données pour améliorer l'exploration de résultat génomiques"),
                             Projet("3. Modélisation de terrain 3D pour l'impression 3D et la navigation"),
                             Projet("4. Développement d'une application web de visualisation et de manipulation "
                                    "fragments de documents ancients"),
                             Projet("5. Pipeline de pré-traitement de jeu de données d’images IRM pour "
                                    "le deep learning"),
                             Projet("6. Neomics : nouvelle méthode pour l'intégration et la fouille "
                                    "de données (data mining) de données multi-omiques représentées dans une "
                                    "base de données orientée graphe (neo4j)"),
                             Projet("7. Mini Jeux Sérieux"),
                             Projet("8. Développement d’un modèle computationnel du sommeil paradoxal chez le rongeur")]

        self.list_membres = []

        with open("data.txt", 'r') as input_file:
            for line in input_file:
                line.strip()
                splitted_line = line.split()
                self.list_membres.append(Membre(" ".join(splitted_line[:-1]), splitted_line[-1]))

        for people in self.list_membres:
            self.add_membre(people)

        self.score_abs = sum([membre.sadness for membre in self.list_membres])
        max_sadness = sum([len(membre.liste) - 1 for membre in self.list_membres])
        self.score_rel = (max_sadness - self.score_abs) * 100 / max_sadness

    def add_membre(self, people: Membre):
        deleted_membre = self.list_projets[people.current_choice].add_member(people)
        if deleted_membre:
            deleted_membre.next_choice()
            self.add_membre(deleted_membre)

    def __repr__(self):
        return "\n".join(str(projet) for projet in self.list_projets) + "\n SCORE = {} => {}% satisfaction".format(
            self.score_abs, self.score_rel)


liste_matchings = [Matching() for x in range(100)]

print(min(liste_matchings, key=lambda matching: matching.score_abs))
