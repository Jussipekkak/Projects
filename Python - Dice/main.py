import random


#Kysytään panos
def get_bet(balance):
    while True:
        #Tallennetaan käyttäjän syöte
        amount = input("Paljonko lyöt vetoa?: ")
        #Varmistetaan että syöte on numero
        if amount.isdigit():
            amount = int(amount)
            if 1<= amount <= balance:
                return amount
            else:
                print(f"Summan pitää olla 1 - {balance}.")
        else:
            print("Syötä summa numeroina: ")


#Nopan heitto
def roll_dice(balance):
    winnings = 0
    while True:
        #Kysytään käyttäjältä veikkausta
        quess = (input("Mitä numeroa veikkaat? (1 - 6) : "))
        if quess.isdigit():
            quess = int(quess)
            if 1 <= quess <= 6:
                bet = get_bet(balance)
                #Arvotaan nopan arvo väliltä 1 - 6 
                number = random.randint(1,6) 
          
               
                print(f"Veikkaat että noppa saa arvon {quess}")
                print("=====================================")
                print(f"Nopan arvo on {number}")
                # Jos käyttäjän arvaus ja nopan arvo ovat samat, Käyttäjä saa panoksen kaksinkertaisena
                if quess == number: 
                    winnings = bet*2
                    balance += winnings
                    print(f"Voitit {winnings}$")
                else:
                    # Hävitessä käyttäjä menettää panoksen
                    balance -= bet 
                    print("Hävisit")
                print(f"Tilin saldosi on nyt {balance}$")
                print()
                return balance
            else:
                print("Valitse numero 1 - 6")        
        else:
            print("Syötä numero.")

   
#Logiikka rahan tallennukseen
def deposit():
    while True:
        #Kysytään paljonko käyttäjä haluaa tallettaa
        amount = input("Paljonko rahaa talletetaan? $: ") 
        print()
        #Varmistetaan että syöte on numero
        if amount.isdigit(): 
            amount = int(amount)
            if amount > 0:
                return amount
            else:
                print("Summan pitää olla enemmäin kuin 0")
        else:
            print("Syötä numero")



def main():
    print("Tervetuloa kasinolle!")
    nimi = input("Syötä nimesi niin pääset eteenpäin: ")
    print(f"Terve {nimi}! Talleta rahaa niin päästään heittämään noppaa.")
    # Talletetaan aloitussumma
    balance = deposit()
    while True:
        # Näytetään saldo
        print(f"\nTilisi saldo on {balance}$.")
        # Tarkistetaan onko saldo nolla
        if balance == 0:
            print("Rahat loppu. Parempi onni ensi kerralla!")
            user_input = input("Jos haluat jatkaa, kirjoita talletettava summa. Painamalla enter lopetat pelin: ")
            if user_input.isdigit() and int(user_input) > 0:
                balance += int(user_input)
                continue
            else:
                print("Kiitos pelistä!")
                break
        # Kysytään haluaako pelaaja jatkaa
        answer = input("Paina enter, jos haluat pelata. Paina Q, jos haluat lopettaa: ").upper()
        if answer == "Q":
            print(f"Kiitos pelistä! Sinulle jäi {balance}$.")
            break
        # Heitetään noppaa ja päivitetään saldo
        balance = roll_dice(balance)

main()