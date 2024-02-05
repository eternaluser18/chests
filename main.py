import random
import tkinter as tk

def start_game():


    global return_button
    start_button.pack_forget()
    exit_button.pack_forget()

    return_button = tk.Button(root, text="Вернуться в главное меню", command=return_to_main_menu)
    return_button.pack(pady=0)

    global input_entry
    input_entry = tk.Entry(root, width=40)
    input_entry.pack(pady=10)
    global send_button
    send_button = tk.Button(root, text="send", command=send_text)
    send_button.pack(pady=10)

    global game_text
    game_text = tk.Text(root, height=30, width=60, bg="white", fg="black", font=("Tahoma", 12), bd=0)
    game_text.pack(pady=10)
    game_text.config(state=tk.DISABLED)


    global output_label
    output_label = tk.Label(root, text="", bg="white", fg="black", font=("Tahoma", 10), anchor="sw")
    output_label.pack(side="left", anchor="sw", padx=10, pady=10)

    for card in card_deck:
        print(f"{Card.value[card.value]} of {Card.suit[card.suit]}")
    print("\n")
    global bot
    global player
    bot = Player(name = "botus")
    player = Player(name = "me")

    draw_cards(card_deck, bot, 48)
    draw_cards(card_deck, player, 4)

    player.show_hand()
    print("s\n")
    #guess_card(guesser = player, guessed = bot)


def send_text():
    game_text.config(state=tk.NORMAL)
    game_text.delete(1.0, tk.END)
    Player.show_hand(player)
    game_text.config(state=tk.DISABLED)

    guess_card(player, bot)




def update_output_window(message):
    output_label.config(text=message)
def return_to_main_menu():
    # Показываем все элементы
    start_button.pack(pady=0)
    exit_button.pack(pady=0)
    # Скрываем кнопку "Вернуться в главное меню"
    return_button.pack_forget()
    input_entry.pack_forget()
    game_text.pack_forget()
    send_button.pack_forget()
    output_label.pack_forget()
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


card_deck = []
for x in range(4):
        for y in range(2, 15):
            card_deck.append(Card(v = y, s = x))
random.shuffle(card_deck)

def draw_cards(deck, player, n):
    for x in range(n):
        if deck:
                card_from_deck = deck.pop()
                player.add_card_to_hand(card_from_deck)
        else:
            entered_text = "empty"
            game_text.config(state=tk.NORMAL, fg="black", font=("Tahoma", 12))
            game_text.insert(tk.END, f"{entered_text}\n")
            game_text.config(state=tk.DISABLED)
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card_to_hand(self, card):
        self.hand.append(card)

    def show_hand(self):
        game_text.config(state=tk.NORMAL)
        game_text.insert(tk.END, f"{self.name}'s рука карт:\n\n")

        for card in self.hand:
            game_text.insert(tk.END, f"Карта: {Card.value[card.value]} {Card.suit[card.suit]}\n")
        print("\n")
        game_text.config(state=tk.DISABLED)
def guess_card(guesser, guessed):
    g_value = input("(value)Do you have ")
    if not any(Card.value[card.value] == g_value for card in guessed.hand):
       return False
    print("yes")
    g_amount = int(input("in amount of "))

    if not g_amount == sum(1 for card in guessed.hand if Card.value[card.value] == g_value):
        return f"nah, {sum(1 for card in guessed.hand if Card.value[card.value] == g_value)}"
    if g_amount == 3:
        print("take it all")
        return 1
    temp_card_list = [card for card in guessed.hand if Card.value[card.value] == g_value]

    for i in temp_card_list:
        print(f"{Card.value[i.value]} of {Card.suit[i.suit]}")
        temp = 0
    for i in temp_card_list:
        temp += 1
        x = input(f"{temp}/{len(temp_card_list)} suit is ")
        if not any(Card.suit[i.suit] == x for i in temp_card_list):
            return False
        if temp == len(temp_card_list):
            print("okay, take it")
            steal_cards(stealer = guesser, stealed = guessed, value = g_value)
        else:
            print("okay, next")

def steal_cards(stealer, stealed, value):
    cards = [card for card in stealed.hand if Card.value[card.value] == value]
    stealer.hand += stealer.hand + cards
    stealed.hand = [card for card in stealed.hand if card not in cards]



def exit_game():
    root.destroy()
root = tk.Tk()
root.title("Ваша игра")
root.geometry("700x550")  # Устанавливаем размеры окна
root.configure(bg="white")

# Создаем кнопку для начала игры
start_button = tk.Button(root, text="Начать игру", command=start_game)
start_button.pack(pady=10)




# Создаем кнопку для выхода из игры
exit_button = tk.Button(root, text="EXIT", command=exit_game)
exit_button.pack(pady=10)

# Запускаем главный цикл
root.mainloop()
