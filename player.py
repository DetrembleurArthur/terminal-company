from random import randint

class Item:

    NAMES = [
    "Lunettes de réalité virtuelle",
    "Clé USB magnétique",
    "Tasse intelligente",
    "Lampe holographique",
    "Scanner biométrique",
    "Gant de traduction instantanée",
    "Crayon 3D",
    "Casque anti-bruit intelligent",
    "Chargeur solaire portable",
    "Imprimante 4D",
    "Robot domestique",
    "Sac à dos anti-gravité",
    "Oreiller connecté",
    "Pinceau numérique",
    "Montre holographique",
    "Haut-parleur intelligent",
    "Brosse à dents ultrasonique",
    "Écouteurs de traduction",
    "Stylo scanner",
    "Cahier électronique",
    "Téléphone holographique",
    "Chaussures intelligentes",
    "Porte-monnaie électronique",
    "Tablette tactile flexible",
    "Thermos intelligent",
    "Gants chauffants",
    "Ceinture connectée",
    "Horloge atomique de poche",
    "Sac à dos intelligent",
    "Tapis de yoga intelligent",
    "Bouteille d'eau intelligente",
    "Parapluie anti-vent",
    "Porte-clés GPS",
    "Miroir intelligent",
    "Cadre photo numérique",
    "Poubelle automatique",
    "Ventilateur USB",
    "Globe terrestre holographique",
    "Boussole GPS",
    "Disque dur nuage",
    "Lunettes de lecture électroniques",
    "Bracelet de santé",
    "Pèse-personne intelligent",
    "Écouteurs sans fil",
    "Cadenas biométrique",
    "Chargeur sans fil",
    "Souris ergonomique",
    "Stylo numérique",
    "Plateau de charge solaire",
    "Tapis de souris chauffant",
    "Brosse à cheveux vibrante",
    "Ventilateur de bureau USB",
    "Bouilloire intelligente",
    "Sac à main chauffant",
    "Lampe de poche rechargeable",
    "Ouvre-bouteille électronique",
    "Épluche-légumes automatique",
    "Pommeau de douche LED",
    "Horloge murale connectée",
    "Garde-robe intelligente",
    "Chapeau de soleil avec panneau solaire",
    "Câble de charge rétractable",
    "Rasoir électrique waterproof",
    "Pantoufles chauffantes",
    "Carnet de notes électronique",
    "Réveil olfactif",
    "Pèse-bagages numérique",
    "Support pour smartphone pliable",
    "Hamac portable",
    "Garde-boue magnétique pour vélo",
    "Répulsif à moustiques ultrasonique",
    "Thermomètre intelligent",
    "Poubelle tri-sélective automatique",
    "Stylo à encre électronique",
    "Balle de fitness connectée",
    "Épluche-pommes automatique",
    "Papier toilette chauffant",
    "Casquette ventilée",
    "Brosse à dents sonique",
    "Sacoche de vélo avec chargeur solaire",
    "Chaise de bureau ergonomique",
    "Bouteille d'eau filtrante",
    "Chargeur de voiture USB",
    "Stylo à gel infrarouge",
    "Brosse à ongles électrique",
    "Lampe de lecture à LED",
    "Sac isotherme intelligent",
    "Coussin de massage chauffant",
    "Câble USB lumineux",
    "Chargeur de batterie solaire",
    "Étagère flottante magnétique",
    "Lampe UV désinfectante",
    "Cintre chauffant",
]

    def __init__(self, price, weight) -> None:
        self.price = int(price)
        self.weight = int(weight)
        self.name = Item.NAMES[randint(0, len(Item.NAMES) - 1)]
    
    def __repr__(self) -> str:
        return f"[{self.name}] {self.price}$ {self.weight}Kg"


class Player:

    def __init__(self) -> None:
        self.items = []
    
    def show(self):
        print("\nItems:")
        for item in self.items:
            print(item)
        print(f"Total price: {sum(map(lambda item: item.price, self.items))}$")
        print(f"Total weight: {sum(map(lambda item: item.weight, self.items))}Kg")

