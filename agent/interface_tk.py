"""Maquette Tkinter de la bibliothèque : interface visuelle et navigation, sans logique métier."""

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

COULEURS = {
    "fond": "#f5f5f5",
    "menu": "#ecf0f1",
    "entete": "#2c3e50",
    "texte": "#2c3e50",
    "gris": "#7f8c8d",
    "bleu": "#3498db",
    "bleu_clair": "#d6eaf8",
    "vert": "#27ae60",
    "rouge": "#c0392b",
    "bordure": "#d5d9e0",
    "statut": "#bdbdbd",
}

LIVRES_MAQUETTE = [
    ("001", "Le Petit Prince", "Antoine de Saint-Exupéry", "Disponible"),
    ("002", "L'Étranger", "Albert Camus", "Emprunté"),
    ("003", "Germinal", "Émile Zola", "Disponible"),
    ("004", "Les Misérables", "Victor Hugo", "Disponible"),
    ("005", "Candide", "Voltaire", "Emprunté"),
    ("006", "Madame Bovary", "Gustave Flaubert", "Disponible"),
    ("007", "Notre-Dame de Paris", "Victor Hugo", "Disponible"),
]

UTILISATEURS_MAQUETTE = [
    ("USR001", "Marie Dubois", "9782253096337"),
    ("USR002", "Jean Martin", "9782070413119"),
    ("USR003", "Sophie Lemaire", "9782253004226"),
    ("USR004", "Pierre Durand", "9782070323087"),
    ("USR005", "Claire Bernard", "9782253005070"),
]

MENU = (
    ("LIVRES", (
        ("ajouter_livre", "Ajouter un livre"),
        ("supprimer_livre", "Supprimer un livre"),
        ("rechercher_titre", "Rechercher par titre"),
        ("rechercher_auteur", "Rechercher par auteur"),
        ("tous_les_livres", "Tous les livres"),
        ("livres_disponibles", "Livres disponibles"),
    )),
    ("UTILISATEURS", (
        ("ajouter_utilisateur", "Ajouter un utilisateur"),
        ("tous_les_utilisateurs", "Tous les utilisateurs"),
    )),
    ("EMPRUNTS", (
        ("emprunter_livre", "Emprunter un livre"),
        ("retourner_livre", "Retourner un livre"),
    )),
    ("DONNEES", (
        ("statistiques", "Statistiques"),
        ("sauvegarder", "Sauvegarder"),
        ("creer_sauvegarde", "Créer une sauvegarde"),
    )),
)

TITRES_PAGES = {
    "ajouter_livre": "Ajouter un livre",
    "supprimer_livre": "Supprimer un livre",
    "rechercher_titre": "Rechercher par titre",
    "rechercher_auteur": "Rechercher par auteur",
    "tous_les_livres": "Tous les livres",
    "livres_disponibles": "Livres disponibles",
    "ajouter_utilisateur": "Ajouter un utilisateur",
    "tous_les_utilisateurs": "Tous les utilisateurs",
    "emprunter_livre": "Emprunter un livre",
    "retourner_livre": "Retourner un livre",
    "statistiques": "Statistiques de la bibliothèque",
    "sauvegarder": "Sauvegarder les données",
    "creer_sauvegarde": "Créer une sauvegarde",
}

STATUTS_PAGES = {
    "tous_les_livres": "Tous les livres  |  7 livres  |  5 disponibles",
    "livres_disponibles": "Livres disponibles  |  5 livres",
    "tous_les_utilisateurs": "Tous les utilisateurs  |  5 utilisateurs",
}


def choisir_police(*candidates):
    familles = tkfont.families()
    return next((famille for famille in candidates if famille in familles), "DejaVu Sans")


class BibliothequeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Bibliothèque Personnelle")
        self.root.geometry("1200x760")
        self.root.minsize(1000, 650)
        self.root.configure(bg=COULEURS["fond"])

        famille = choisir_police("Segoe UI", "DejaVu Sans")
        self.police = (famille, 10)
        self.police_petite = (famille, 9)
        self.police_gras = (famille, 10, "bold")
        self.police_titre = (famille, 14, "bold")
        self.police_entete = (famille, 15, "bold")
        self.police_chiffre = (famille, 24, "bold")

        self.items_menu = {}
        self._configurer_styles()
        self._creer_entete()
        self._creer_barre_statut()
        self._creer_corps()
        self.afficher_page("tous_les_livres")

    def _configurer_styles(self):
        style = ttk.Style()
        style.configure(
            "Bibliotheque.Treeview",
            background="white",
            fieldbackground="white",
            foreground=COULEURS["texte"],
            rowheight=34,
            font=self.police,
        )
        style.configure(
            "Bibliotheque.Treeview.Heading",
            background=COULEURS["bordure"],
            foreground="#34495e",
            font=self.police_gras,
            relief="flat",
        )
        style.map(
            "Bibliotheque.Treeview",
            background=[("selected", COULEURS["bleu_clair"])],
            foreground=[("selected", COULEURS["texte"])],
        )

    def _creer_entete(self):
        entete = tk.Frame(self.root, bg=COULEURS["entete"], height=62)
        entete.pack(side="top", fill="x")
        entete.pack_propagate(False)
        tk.Label(
            entete,
            text="SYSTÈME DE GESTION DE BIBLIOTHÈQUE PERSONNELLE",
            bg=COULEURS["entete"],
            fg="white",
            font=self.police_entete,
        ).pack(side="left", padx=25)

    def _creer_barre_statut(self):
        barre = tk.Frame(self.root, bg=COULEURS["statut"], height=26)
        barre.pack(side="bottom", fill="x")
        barre.pack_propagate(False)
        self.statut_label = tk.Label(
            barre,
            text="",
            bg=COULEURS["statut"],
            fg=COULEURS["texte"],
            font=self.police_petite,
        )
        self.statut_label.pack(side="left", padx=12)

    def _creer_corps(self):
        corps = tk.Frame(self.root, bg=COULEURS["fond"])
        corps.pack(side="top", fill="both", expand=True)
        self._creer_menu(corps)
        contenu = tk.Frame(corps, bg=COULEURS["fond"])
        contenu.pack(side="left", fill="both", expand=True)
        self.titre_label = tk.Label(
            contenu, text="", bg=COULEURS["fond"], fg=COULEURS["texte"],
            font=self.police_titre, anchor="w",
        )
        self.titre_label.pack(fill="x", padx=28, pady=(12, 48))
        self.page = tk.Frame(contenu, bg=COULEURS["fond"])
        self.page.pack(fill="both", expand=True, padx=28)

    def _section(self, parent, titre):
        tk.Label(
            parent, text=titre, bg=COULEURS["menu"], fg=COULEURS["gris"],
            font=self.police_petite + ("bold",), anchor="w",
        ).pack(fill="x", padx=18, pady=(11, 3))

    def _item(self, parent, texte, cle):
        label = tk.Label(
            parent, text=texte, bg=COULEURS["menu"], fg=COULEURS["texte"],
            font=self.police, anchor="w", padx=22, pady=6, cursor="hand2",
        )
        label.bind("<Button-1>", lambda _event, c=cle: self.afficher_page(c))
        label.pack(fill="x")
        self.items_menu[cle] = label

    def _creer_menu(self, parent):
        menu = tk.Frame(parent, bg=COULEURS["menu"], width=250)
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)
        for titre_section, entrees in MENU:
            self._section(menu, titre_section)
            for cle, texte in entrees:
                self._item(menu, texte, cle)

    def afficher_page(self, cle):
        titre = TITRES_PAGES[cle]
        for cle_item, label in self.items_menu.items():
            actif = cle_item == cle
            label.config(
                bg=COULEURS["bleu"] if actif else COULEURS["menu"],
                fg="white" if actif else COULEURS["texte"],
            )
        self.titre_label.config(text=titre)
        self.statut_label.config(text=STATUTS_PAGES.get(cle, titre))
        for enfant in self.page.winfo_children():
            enfant.destroy()
        getattr(self, "_page_" + cle)()

    def _champ(self, parent, libelle, placeholder=""):
        ligne = tk.Frame(parent, bg=COULEURS["fond"])
        ligne.pack(fill="x", pady=7)
        tk.Label(
            ligne, text=libelle, width=16, anchor="w",
            bg=COULEURS["fond"], fg=COULEURS["texte"], font=self.police_gras,
        ).pack(side="left")
        entree = tk.Entry(
            ligne, font=self.police, bg="white", relief="solid", bd=1,
            highlightthickness=0,
        )
        if placeholder:
            entree.insert(0, placeholder)
            entree.config(fg=COULEURS["gris"])
        entree.pack(side="left", fill="x", expand=True, ipady=7)
        return entree

    def _bouton(self, parent, texte, couleur, largeur=16, active=None):
        return tk.Button(
            parent, text=texte, bg=couleur, fg="white",
            activebackground=active or couleur, activeforeground="white",
            relief="flat", font=self.police_gras, width=largeur,
        )

    def _actions(self, *boutons):
        cadre = tk.Frame(self.page, bg=COULEURS["fond"])
        cadre.pack(fill="x", pady=(42, 0))
        for bouton in reversed(boutons):
            bouton.pack(side="right", padx=(12, 0), ipady=8, in_=cadre)
        return cadre

    def _tableau(self, colonnes, lignes, selection=None, hauteur=7):
        tableau = ttk.Treeview(
            self.page, columns=[c[0] for c in colonnes], show="headings",
            style="Bibliotheque.Treeview", height=hauteur, selectmode="browse",
        )
        for cle, titre, largeur in colonnes:
            tableau.heading(cle, text=titre, anchor="w")
            tableau.column(cle, width=largeur, anchor="w", stretch=False)
        tableau.tag_configure("disponible", foreground=COULEURS["vert"])
        tableau.tag_configure("emprunte", foreground=COULEURS["rouge"])
        for values in lignes:
            tag = None
            if values[-1] == "Disponible":
                tag = "disponible"
            elif values[-1] == "Emprunté":
                tag = "emprunte"
            tableau.insert("", "end", iid=values[0], values=values, tags=(tag,) if tag else ())
        if selection:
            tableau.selection_set(selection)
            tableau.focus(selection)
        tableau.pack(fill="x", pady=(18, 0))
        return tableau

    def _panneau(self, titre, lignes):
        cadre = tk.Frame(self.page, bg="white", highlightbackground=COULEURS["bordure"], highlightthickness=1)
        cadre.pack(fill="x", pady=(8, 0))
        tk.Label(
            cadre, text=titre, bg="white", fg=COULEURS["texte"],
            font=self.police_gras, anchor="w",
        ).pack(fill="x", padx=18, pady=(16, 8))
        for ligne in lignes:
            tk.Label(
                cadre, text=ligne, bg="white", fg=COULEURS["gris"],
                font=self.police, anchor="w", justify="left",
            ).pack(fill="x", padx=18, pady=3)
        tk.Frame(cadre, height=14, bg="white").pack(fill="x")
        return cadre

    def _colonne_livres(self):
        return (
            ("id", "ID", 90),
            ("titre", "Titre", 290),
            ("auteur", "Auteur", 260),
            ("statut", "Statut", 240),
        )

    def _page_tous_les_livres(self):
        recherche = tk.Frame(self.page, bg=COULEURS["fond"])
        recherche.pack(fill="x")
        champ = tk.Entry(
            recherche, font=self.police, bg="white", fg=COULEURS["gris"],
            relief="solid", bd=1, highlightthickness=0,
        )
        champ.insert(0, "Rechercher un titre, un auteur...")
        champ.pack(side="left", fill="x", expand=True, ipady=8)
        self._bouton(recherche, "Rechercher", COULEURS["bleu"], 12, "#2980b9").pack(
            side="left", padx=(8, 0), ipady=8,
        )
        self._tableau(self._colonne_livres(), LIVRES_MAQUETTE, selection="002")
        self._actions(
            self._bouton(self.page, "Emprunter", COULEURS["vert"], 14, "#229954"),
            self._bouton(self.page, "Supprimer", COULEURS["rouge"], 13, "#a93226"),
        )

    def _page_livres_disponibles(self):
        disponibles = [livre for livre in LIVRES_MAQUETTE if livre[3] == "Disponible"]
        self._panneau(
            "5 livres peuvent être empruntés",
            ["La liste ci-dessous présente uniquement les livres actuellement disponibles."],
        )
        self._tableau(self._colonne_livres(), disponibles)

    def _page_ajouter_livre(self):
        self._champ(self.page, "Titre", "Entrez le titre du livre")
        self._champ(self.page, "Auteur", "Entrez l'auteur du livre")
        self._champ(self.page, "ISBN", "Entrez l'ISBN du livre")
        self._actions(self._bouton(self.page, "Ajouter le livre", COULEURS["bleu"], 16, "#2980b9"))

    def _page_supprimer_livre(self):
        self._champ(self.page, "ISBN", "Entrez l'ISBN du livre à supprimer")
        self._actions(self._bouton(self.page, "Supprimer le livre", COULEURS["rouge"], 16, "#a93226"))
        self._tableau(self._colonne_livres(), LIVRES_MAQUETTE)

    def _page_rechercher_titre(self):
        self._champ(self.page, "Titre", "Entrez le titre à rechercher")
        self._actions(self._bouton(self.page, "Rechercher", COULEURS["bleu"], 16, "#2980b9"))
        self._tableau(self._colonne_livres(), LIVRES_MAQUETTE)

    def _page_rechercher_auteur(self):
        self._champ(self.page, "Auteur", "Entrez l'auteur à rechercher")
        self._actions(self._bouton(self.page, "Rechercher", COULEURS["bleu"], 16, "#2980b9"))
        self._tableau(self._colonne_livres(), LIVRES_MAQUETTE)

    def _page_ajouter_utilisateur(self):
        self._champ(self.page, "Nom", "Entrez le nom de l'utilisateur")
        self._champ(self.page, "ID", "Entrez l'ID de l'utilisateur")
        self._actions(self._bouton(self.page, "Ajouter l'utilisateur", COULEURS["bleu"], 18, "#2980b9"))

    def _page_tous_les_utilisateurs(self):
        colonnes = (
            ("id", "ID", 200),
            ("nom", "Nom", 360),
            ("livres", "Livres empruntés", 320),
        )
        self._tableau(colonnes, UTILISATEURS_MAQUETTE)

    def _page_emprunter_livre(self):
        self._champ(self.page, "ISBN", "Entrez l'ISBN du livre à emprunter")
        self._champ(self.page, "ID utilisateur", "Entrez l'ID de l'utilisateur")
        self._actions(self._bouton(self.page, "Emprunter", COULEURS["vert"], 16, "#229954"))
        self._tableau(
            self._colonne_livres(),
            [livre for livre in LIVRES_MAQUETTE if livre[3] == "Disponible"],
        )

    def _page_retourner_livre(self):
        self._champ(self.page, "ISBN", "Entrez l'ISBN du livre à retourner")
        self._actions(self._bouton(self.page, "Retourner le livre", COULEURS["vert"], 16, "#229954"))
        self._tableau(
            self._colonne_livres(),
            [livre for livre in LIVRES_MAQUETTE if livre[3] == "Emprunté"],
        )

    def _page_statistiques(self):
        cartes = tk.Frame(self.page, bg=COULEURS["fond"])
        cartes.pack(fill="x")
        donnees = (
            ("Total des livres", "7", COULEURS["bleu"]),
            ("Livres disponibles", "5", COULEURS["vert"]),
            ("Livres empruntés", "2", COULEURS["rouge"]),
            ("Total des utilisateurs", "5", COULEURS["entete"]),
        )
        for index, (titre, valeur, couleur) in enumerate(donnees):
            carte = tk.Frame(
                cartes, bg="white",
                highlightbackground=COULEURS["bordure"], highlightthickness=1,
            )
            carte.pack(side="left", fill="both", expand=True, padx=(0 if index == 0 else 12, 0))
            tk.Label(
                carte, text=titre, bg="white", fg=COULEURS["gris"],
                font=self.police_petite, anchor="w",
            ).pack(fill="x", padx=16, pady=(16, 2))
            tk.Label(
                carte, text=valeur, bg="white", fg=couleur,
                font=self.police_chiffre, anchor="w",
            ).pack(fill="x", padx=16, pady=(0, 18))

    def _page_sauvegarder(self):
        self._panneau(
            "Sauvegarde des données",
            [
                "Les fichiers books.txt et users.txt seront enregistrés dans le dossier de données.",
                "Dernière sauvegarde : aucune dans cette session.",
            ],
        )
        self._actions(self._bouton(self.page, "Sauvegarder", COULEURS["bleu"], 16, "#2980b9"))

    def _page_creer_sauvegarde(self):
        self._panneau(
            "Copie de sécurité",
            [
                "Crée books.txt.backup et users.txt.backup à côté des fichiers de données.",
                "Une sauvegarde existante doit être remplacée avant d'en créer une nouvelle.",
            ],
        )
        self._actions(self._bouton(self.page, "Créer une sauvegarde", COULEURS["vert"], 18, "#229954"))


def main():
    racine = tk.Tk()
    BibliothequeUI(racine)
    racine.mainloop()


if __name__ == "__main__":
    main()
