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
        self.card_images = []  # Keep references to card images

        self.canvas_player = tk.Canvas(master, width=600, height=200)
        self.canvas_player.pack()

        self.canvas_dealer = tk.Canvas(master, width=600, height=200)
        self.canvas_dealer.pack()

        self.player_score_label = tk.Label(master, text="Player Score: 0")
        self.dealer_score_label = tk.Label(master, text="")

        self.hit_button = tk.Button(master, text="Hit", command=self.hit)
        self.stand_button = tk.Button(master, text="Stand", command=self.stand)
        self.new_game_button = tk.Button(master, text="New Game", command=self.new_game)

        self.player_score_label.pack()
        self.dealer_score_label.pack()
        self.hit_button.pack(side=tk.LEFT)
        self.stand_button.pack(side=tk.LEFT)
        self.new_game_button.pack(side=tk.RIGHT)

        self.game_over = False  # Initialize game_over attribute

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

    def draw_card(self, card, canvas, x, y):
        if canvas == self.canvas_dealer and not self.game_over:
            image_path = "images/card_back.png"  # Face down card for the dealer
        else:
            image_path = f"images/{card['rank']}_{card['suit']}.png"
        card_image = tk.PhotoImage(file=image_path)
        canvas.create_image(x, y, anchor=tk.NW, image=card_image)
        self.card_images.append(card_image)  # Keep a reference to the card image

    def hit(self):
        if self.game_over:
            self.new_game()
        else:
            card = self.deal_card(self.player_hand)
            self.draw_card(card, self.canvas_player, len(self.player_hand) * 70, 0)
            self.output_player_hand()
            self.update_score_labels()

            if self.calculate_score(self.player_hand) > 21:
                self.end_game("You went over. You lose!")
            elif self.calculate_score(self.player_hand) == 21:
                self.end_game("Blackjack! You win!")

    def stand(self):
        while self.calculate_score(self.dealer_hand) < 17:
            self.deal_card(self.dealer_hand)

        # Clear the dealer's canvas before displaying all cards
        self.canvas_dealer.delete("all")

        # Display all dealer's cards
        offset = 0
        for card in self.dealer_hand:
            self.draw_card(card, self.canvas_dealer, offset, 0)
            offset += 70  # Adjust the offset to space the cards

        self.update_score_labels()
        self.output_player_hand()  # Output player's hand before determining the winner
        self.output_dealer_hand()
        self.determine_winner()

    def output_player_hand(self):
        print("Player's Hand:")
        for card in self.player_hand:
            print(f"{card['rank']} of {card['suit']}")
        print(f"Player Score: {self.calculate_score(self.player_hand)}\n")

    def output_dealer_hand(self):
        print("Dealer's Hand:")
        for card in self.dealer_hand:
            print(f"{card['rank']} of {card['suit']}")
        print(f"Dealer Score: {self.calculate_score(self.dealer_hand)}")

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
        self.output_player_hand()
        self.output_dealer_hand()
        messagebox.showinfo("Game Over", message)
        self.game_over = True

    def new_game(self):
        self.deck = self.create_deck()
        self.player_hand = [self.deal_card(self.player_hand), self.deal_card(self.player_hand)]
        self.dealer_hand = [self.deal_card(self.dealer_hand), self.deal_card(self.dealer_hand)]

        # Clear the canvases before displaying new cards
        self.canvas_player.delete("all")
        self.canvas_dealer.delete("all")

        # Display all player's cards side by side
        offset = 0
        for card in self.player_hand:
            self.draw_card(card, self.canvas_player, offset, 0)
            offset += 70  # Adjust the offset to space the cards

        # Display the initial dealer's card face down
        self.draw_card(self.dealer_hand[0], self.canvas_dealer, 0, 0)

        self.update_score_labels()
        self.game_over = False

        if self.calculate_score(self.player_hand) == 21:
            self.end_game("Blackjack! You win!")

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
