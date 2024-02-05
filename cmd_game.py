import random
import sys

def start_game():
    global card_deck
    card_deck = []
    for x in range(4):
        for y in range(2, 15):
            card_deck.append(Card(v=y, s=x))
    random.shuffle(card_deck)

    for card in card_deck:
        print(f"{Card.value[card.value]} of {Card.suit[card.suit]}")
    print("\n")
    name = input("Your name: ")
    global bot
    bot = Player(name = "botus", n = 0)
    global player
    player = Player(name = name, n = 0)
    print(f"{bot.name}: Pleasure to play with you, {player.name}.")
    print(f"{bot.name}: Deck is shuffled already.")


    draw_cards(card_deck, bot, 4)
    draw_cards(card_deck, player, 4)
    print(f"{bot.name}: Our hands are full of cards. Please start")
    turn_number = 0
    while(1):
        if turn_number % 2 == 0:
            player_turn()
        else:
            enemy_turn()
        turn_number += 1

def player_turn():
    while(1):
        line = input(f"{player.name}: ")
        if line == "hand": player.show_hand()
        elif line == "guess":
            guess_card(player, bot)
            break
        elif line == "exit": exit()
        else: print(f"{bot.name}: I don't understand you. Try again")

def enemy_turn():
    random.shuffle(bot.hand)
    v = Card.value[bot.hand[0].value]
    temp = [card for card in bot.hand if Card.value[card.value] == v]
    temp_suit_of_v = [card.suit for card in temp]
    player_suit_list = [suit for suit in Card.suit if suit not in temp_suit_of_v]

    a = len(temp)
    ar = random.randrange(1, 5-a)
    print(f"{bot.name}: Do you have {v}'s?")
    correct_answer = any(Card.value[card.value] == v for card in player.hand)
    while(1):
        answer = input(f"{player.name}: ")
        if answer == "yes" and correct_answer == 1:
            print(f"{bot.name}: Good.")
            break
        elif answer == "no" and correct_answer == 1:
            print(f"{bot.name}: LIAR!")
            for i in range (len((player.hand)/2)):
                steal_cards(bot, player, Card.value[player.hand[0]])
            print(f"Half of your cards goes to {bot.name}")
            return
        elif answer == "yes" and correct_answer == 0:
            print(f"{bot.name}: You lied.")
            steal_cards(bot, player, Card.value[player.hand[0].value])
            print(f"One of your cards goes to {bot.name}")
            return
        elif answer == "no" and correct_answer == 0:
            print(f"{bot.name}: Okay. Your turn.")
            draw_cards(card_deck, bot, 1)
            return
        else: print(f"{bot.name}: I didn't understand ypu. Try again.")

    if a == 3:
        print(f"{bot.name}: I know your card. It's {v} of {player_suit_list.pop()}")
    else:
        for x in range(4-a):
            if x == 4-a:
                print(f"{bot.name}: And last card. {Card.value[v.value]} of {temp_suit_of_v.pop()}")
            else:
                temp1 = temp_suit_of_v.pop()
                print(f"{bot.name}: One of suits is {temp1}?")
                correct_answer = any(Card.suit[card.suit] == 1 and Card.value[card.value] == v for card in player.hand)
                while (1):
                    answer = input(f"{player.name}: ")
                    if answer == "yes" and correct_answer == 1:
                        print(f"{bot.name}: Good.")
                        break
                    elif answer == "no" and correct_answer == 1:
                        print(f"{bot.name}: LIAR!")
                        for i in range(len((player.hand) / 2)):
                            steal_cards(bot, player, Card.value[player.hand[0]])
                            #доделать проверку на сундучки
                        print(f"Half of your cards goes to {bot.name}")
                        return
                    elif answer == "yes" and correct_answer == 0:
                        print(f"{bot.name}: You lied.")
                        steal_cards(bot, player, Card.value[player.hand[0].value])
                        print(f"One of your cards goes to {bot.name}")
                        if sum(1 for card in bot.hand if Card.value[card.value] == Card.value[bot.hand[-1]]) == 4:
                            bot.chest_number += 1
                            bot.hand = [card for card in bot.hand if not Card.value[card.value] == Card.value[bot.hand[-1]]]
                        return
                    elif answer == "no" and correct_answer == 0:
                        print(f"{bot.name}: Okay. Your turn.")
                        draw_cards(deck, bot, 1)
                        if sum(1 for card in player.hand if Card.value[card.value] == Card.value[player.hand[-1]]) == 4:
                            player.chest_number += 1
                            player.hand = [card for card in player.hand if not Card.value[card.value] == Card.value[player.hand[-1]]]
                        return
                    else:
                        print(f"{bot.name}: I didn't understand ypu. Try again.")

class Card:
    suit = ["spades",
                "hearts",
                "diamonds",
                "clubs"]

    value = [None, None, "2", "3",
                 "4", "5", "6", "7",
                 "8", "9", "10",
                 "Jack", "Queen",
                 "King", "Ace"]

    def __init__(self, v, s):
        self.value = v
        self.suit = s




def draw_cards(deck, player, n):
    for x in range(n):
        if deck:
                card_from_deck = deck.pop()
                player.add_card_to_hand(card_from_deck)
        else:
            print("empty")
class Player:
    def __init__(self, name, n):
        self.name = name
        self.hand = []
        self.chest_number = n

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def show_hand(self):
        print(len(bot.hand))
        print(f"{self.name}'s рука карт:")

        for card in self.hand:
            print(f"Карта: {Card.value[card.value]} {Card.suit[card.suit]}")

def guess_card(guesser, guessed):
    g_value = input("(value)Do you have ")
    if not any(Card.value[card.value] == g_value for card in guessed.hand):
       print(f"{bot.name}: No. My turn.")
       draw_cards(card_deck, player, 1)
       print(f"You took a {Card.value[player.hand[-1].value]} of {Card.suit[player.hand[-1].suit]}")
       return
    print("yes")
    g_amount = int(input("in amount of "))

    if not g_amount == sum(1 for card in guessed.hand if Card.value[card.value] == g_value):
        print(f"nah, {sum(1 for card in guessed.hand if Card.value[card.value] == g_value)}")
        draw_cards(card_deck, player, 1)
        print(f"You took a {Card.value[player.hand[-1].value]} of {Card.suit[player.hand[-1].suit]}")
        if sum(1 for card in player.hand if Card.value[card.value] == Card.value[player.hand[-1]]) == 4:
            player.chest_number += 1
            player.hand = [card for card in player.hand if not Card.value[card.value] == Card.value[player.hand[-1]]]
        return
    if g_amount == 3:
        print("take it all")
        return
    temp_card_list = [card for card in guessed.hand if Card.value[card.value] == g_value]

    for i in temp_card_list:
        print(f"{Card.value[i.value]} of {Card.suit[i.suit]}")
        temp = 0
    for i in temp_card_list:
        temp += 1
        x = input(f"{temp}/{len(temp_card_list)} suit is ")
        if not any(Card.suit[i.suit] == x for i in temp_card_list):
            print(f"{bot.name}: No. My turn.")
            draw_cards(card_deck, player, 1)
            print(f"You took a {Card.value[player.hand[-1].value]} of {Card.suit[player.hand[-1].suit]}")
            if sum(1 for card in player.hand if Card.value[card.value] == Card.value[player.hand[-1]]) == 4:
                player.chest_number += 1
                player.hand = [card for card in player.hand if not Card.value[card.value] == Card.value[player.hand[-1]]]
            return
        if temp == len(temp_card_list):
            print("okay, take it")
            steal_cards(stealer = guesser, stealed = guessed, value = g_value)
            if sum(1 for card in player.hand if Card.value[card.value] == g_value) == 4:
                player.chest_number += 1
                player.hand = [card for card in player.hand if not Card.value[card.value] == g_value]
        else:
            print("okay, next")

def steal_cards(stealer, stealed, value):
    cards = [card for card in stealed.hand if Card.value[card.value] == value]
    stealer.hand += cards
    stealed.hand = [card for card in stealed.hand if card not in cards]
def show_rules():
    print("Hello, Player.")
    print("This game is simple. There is regular deck of cards.")
    print("Each player got 4 cards. Game is turnbased, you start.")
    print("On your turn you try to steal opponent card by guessing value, amount and suits.")
    print("If you fail - take a card from deck.")
    print("Goal is to collect as many \"chests\"(pack of 4 cards of same value) as possible untill deck is ended.")
    print("Nobody is allowed to lie.")
    print("[hand] to check your hand and amount of cards of opponent.")
    print("[guess] to start guessing.")
    print("[exit] to end a game and forget it all.")


print("Welcome.")
while (1):
    print("[rules], [start], [exit].")
    line = input("me: ")
    if line == "rules": show_rules()
    elif line == "start": start_game()
    elif line == "exit": exit()
    else: print("I don't understand you, try again.")







