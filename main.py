import requests
class jeu:
    def __init__(self):
        self.url="https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=fr&country=FR&allowCountries=FR"
        self.image=""
        self.webook="https://discord.com/api/webhooks/1492185961776550068/kAzbOeRIxjDNGIke2hs7jD53gNwsQh5-6SOnIp_ELO7Wq1ooK4TZNtqkGPz8rkO86PnG"
    def test(self):
        re=requests.get(self.url)
        print(re.status_code)
        donnees=re.json()
        liste_jeu=donnees['data']['Catalog']['searchStore']['elements']
        print(len(liste_jeu))
        for item in liste_jeu:
            nom_du_jeu=item['title']
            prix=item['price']['totalPrice']['discountPrice']
            if item['keyImages']: # Si la liste contient quelque chose
                self.image = item['keyImages'][0]['url']
            else:
                self.image = "https://fr.wikipedia.org/wiki/Epic_Games"
            if prix==0:
                self.notifier(f"Jeu gratuit trouvé : {nom_du_jeu} \n {self.image}")
    def notifier(self,message):
        payload = {"content": message}
        requests.post(self.webook, json=payload)
mon_robot=jeu()
mon_robot.test()