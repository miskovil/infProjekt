import tkinter as tk
from tkinter import messagebox
import random

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []

        self.player_score_label = tk.Label(master, text="Player Score: 0")
        self.dealer_score_label = tk.Label(master, text="Dealer Score: 0")

        self.hit_button = tk.Button(master, text="Hit", command=self.hit)
        self.stand_button = tk.Button(master, text="Stand", command=self.stand)
        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game)

        self.player_score_label.pack()
        self.dealer_score_label.pack()
        self.hit_button.pack(side=tk.LEFT)
        self.stand_button.pack(side=tk.LEFT)
        self.new_game_button.pack(side=tk.RIGHT)

        self.new_game()

    def create_deck(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def deal_card(self, hand):
        card = self.deck.pop()
        hand.append(card)
        return card

    def calculate_score(self, hand):
        score = sum(self.card_value(card) for card in hand)
        if score > 21 and 'A' in [card['rank'] for card in hand]:
            score -= 10  # Convert Ace from 11 to 1
        return score

    def card_value(self, card):
        if card['rank'] in ['K', 'Q', 'J']:
            return 10
        elif card['rank'] == 'A':
            return 11
        else:
            return int(card['rank'])

    def update_score_labels(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        self.player_score_label.config(text=f"Player Score: {player_score}")
        self.dealer_score_label.config(text=f"Dealer Score: {dealer_score}")

    def hit(self):
        self.deal_card(self.player_hand)
        self.update_score_labels()

        if self.calculate_score(self.player_hand) > 21:
            self.end_game("You went over. You lose!")

    def stand(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)
        self.update_score_labels()
        self.determine_winner()

    def determine_winner(self):
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if player_score > 21:
            self.end_game("You went over. You lose!")
        elif dealer_score > 21 or player_score > dealer_score:
            self.end_game("You win!")
        elif dealer_score > player_score:
            self.end_game("You lose!")
        else:
            self.end_game("It's a draw!")

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.new_game()

    def new_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(self.player_hand), self.deal_card(self.player_hand)]
        self.dealer_hand = [self.deal_card(self.dealer_hand), self.deal_card(self.dealer_hand)]
        self.update_score_labels()

        if self.calculate_score(self.player_hand) == 21:
            self.end_game("Blackjack! You win!")

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
