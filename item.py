


from math import fabs
from random import gauss, randint, shuffle, random

from utils import debug


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
        self.price = price
        self.weight = int(weight)
        self.name = Item.NAMES[randint(0, len(Item.NAMES) - 1)]
    
    def __repr__(self) -> str:
        return f"{self.name} {self.price}$ {self.weight}Kg"

    @staticmethod
    def dispatch(item_number, factor=1.0):
        debug(f"price factor: {factor}")
        items = []
        for i in range(item_number):
            item = Item(price=round(fabs(gauss(mu=0, sigma=1))*factor, 2), weight=10)
            items.append(item)
        return items

    @staticmethod
    def split_items(items: list, room_number, max_factor=0.20):
        debug(f"rooms: {room_number}, max_factor: {max_factor}, items: {len(items)}")
        indexes = [0 for _ in range(room_number)]
        item_number = len(items)
        acc = 0
        for i in range(room_number):
            if acc >= item_number: break
            items_in_current_room = int(random() * max_factor * item_number)
            if acc + items_in_current_room > item_number:
                items_in_current_room = item_number - acc
            acc +=items_in_current_room
            indexes[i] = items_in_current_room
        remain = item_number - sum(indexes)
        if remain > 0:
            try:
                indexes[indexes.index(0)] = remain
            except ValueError:
                indexes[randint(0, len(indexes) - 1)] += remain
        shuffle(indexes)
        splitted_items = []
        acc = 0
        for i in indexes:
            splitted_items.append(items[acc:acc + i])
            acc += i
        debug(indexes)
        debug(f"sum of indexes {sum(indexes)}, len {len(indexes)}")
        return splitted_items
