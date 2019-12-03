class Vuz:
    def __init__(self, kapacita, spz, motor):
        self.kapacita = kapacita
        self.spz = spz
        self.motor = motor
        
    def __str__(self):
        return self.spz


class Vozovy_park():
    def __init__(self):
        self.vozovy_park = []

    def __str__(self):
        seznam_spz = []
        for i in self.vozovy_park:
            seznam_spz.append(str(i))
        return ", ".join(seznam_spz)

    def pridej_vuz(self, vuz):
        self.vozovy_park.append(vuz)

    def odeber_vuz(self, spz):
        for vuz in self.vozovy_park:
            if vuz.spz == spz:
                self.vozovy_park.remove(vuz)
        return self.vozovy_park

    def najdi_vozy_podle_kapacity(self, pozadovana_kapacita):
        vhodne_vozy = []
        for i in self.vozovy_park:
            if i.kapacita >= pozadovana_kapacita:
                vhodne_vozy.append(i)
        return vhodne_vozy

    def najdi_vozy_podle_paliva(self, pozadovana_kapacita, vzdalenost):
        vhodne_vozy = self.najdi_vozy_podle_kapacity(pozadovana_kapacita)
        vhodne_vozy_podle_dojezdu = []
        for i in vhodne_vozy:
            if isinstance(i.motor, Elektromotor):
                if vzdalenost <= i.motor.dojezd:
                    vhodne_vozy_podle_dojezdu.append(i)
            else:
                vhodne_vozy_podle_dojezdu.append(i)
        return vhodne_vozy_podle_dojezdu

    def najdi_vozy_podle_spotreby(self, pozadovana_kapacita, vzdalenost):
        vhodne_vozy = self.najdi_vozy_podle_paliva(pozadovana_kapacita, vzdalenost)
        nejnizsi = 0
        for i in vhodne_vozy:
            naklady = i.motor.realne_naklady(vzdalenost)
            if nejnizsi == 0:
                nejnizsi = naklady
                vuz_s_nejnizsi_spotrebou = i
                continue
            if naklady < nejnizsi:
                nejnizsi = naklady
                vuz_s_nejnizsi_spotrebou = i
        return vuz_s_nejnizsi_spotrebou


class Motor():
    def __init__(self, naklady):
        # náklady v l/100km
        self.naklady = naklady
    
    def realne_naklady(self, vzdalenost):
        realne_naklady = self.naklady*vzdalenost/100
        return realne_naklady

class Spalovaci_motor(Motor):
    pass

class Elektromotor(Motor):
    def __init__(self, naklady, dojezd):
        super().__init__(naklady)
        self.dojezd = dojezd

class Hybrid(Motor):
    def __init__(self, naklady, dojezd):
        super().__init__(naklady)
        self.dojezd = dojezd
    
    def realne_naklady(self, vzdalenost):
        realne_naklady = (self.naklady*self.dojezd + (vzdalenost-self.dojezd)*self.naklady*1.6)/100
        return realne_naklady


cena = int(input("Jaká je cena paliva za 1l: "))

vuz1 = Vuz(kapacita = 50, spz = "7P2 8745", motor = Spalovaci_motor(naklady = 36))
vuz2 = Vuz(kapacita = 30, spz = "3T6 9864", motor = Elektromotor(naklady = 23, dojezd = 120))
vuz3 = Vuz(kapacita = 10, spz = "TD 97GV0", motor = Elektromotor(naklady = 12, dojezd = 150))
vozy = [vuz1, vuz2, vuz3]

vozovy_park = Vozovy_park()
for vuz in vozy:
    vozovy_park.pridej_vuz(vuz)

# přijde mi nový vůz:
vuz4 = Vuz(kapacita = 40, spz = "G99 LV60", motor = Hybrid(naklady = 24, dojezd = 80))
vozovy_park.pridej_vuz(vuz4) 

pozadovana_kapacita = 20
vzdalenost = int(input("Jak dlouhá bude cesta (v km)? "))

vuz_s_nejnizsi_spotrebou = vozovy_park.najdi_vozy_podle_spotreby(pozadovana_kapacita, vzdalenost)
print(vuz_s_nejnizsi_spotrebou)