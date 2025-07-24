from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Iterator
import random

# =============================
# Enums for Suit and Rank
# =============================
class CardSuit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4

class CardRank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

# =============================
# Custom Exception
# =============================
class DeckCheatingError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

# =============================
# Decorator to ensure fair deck
# =============================
def fair_deck(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list) and len(result) != len(set(result)):
            raise DeckCheatingError("Duplicate cards detected!")
        return result
    return wrapper

# =============================
# Interface Contracts
# =============================
class ICard(ABC):
    @property
    @abstractmethod
    def suit(self): pass

    @property
    @abstractmethod
    def rank(self): pass

    @abstractmethod
    def get_display_name(self) -> str: pass

class IDeck(ABC):
    @abstractmethod
    def draw(self): pass

    @abstractmethod
    def add_card(self, card): pass

    @abstractmethod
    def shuffle(self): pass

# =============================
# Card Class
# =============================
class Card(ICard):
    def __init__(self, suit: CardSuit, rank: CardRank):
        self._suit = suit
        self._rank = rank

    @property
    def suit(self): return self._suit

    @property
    def rank(self): return self._rank

    def get_display_name(self) -> str:
        return f"{self._rank.name.title()} of {self._suit.name.title()}"

    def __eq__(self, other):
        return isinstance(other, Card) and self._rank == other._rank and self._suit == other._suit

    def __lt__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return (self._rank.value, self._suit.value) < (other._rank.value, other._suit.value)

    def __gt__(self, other):
        if not isinstance(other, Card): return NotImplemented
        return (self._rank.value, self._suit.value) > (other._rank.value, other._suit.value)

    def __hash__(self):
        return hash((self._rank, self._suit))

    def __str__(self):
        return self.get_display_name()

    def __repr__(self):
        return f"Card({self._rank}, {self._suit})"

# =============================
# Deck Class
# =============================
class Deck(IDeck):
    def __init__(self, shuffle=True):
        self._cards: List[Card] = [Card(s, r) for s in CardSuit for r in CardRank]
        if shuffle:
            random.shuffle(self._cards)
        self._index = 0

    @property
    @fair_deck
    def cards(self):
        return self._cards.copy()

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self):
        if self._cards:
            return self._cards.pop(0)
        return None

    @fair_deck
    def add_card(self, card: Card):
        self._cards.append(card)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, index):
        return self._cards[index]

    def __iter__(self) -> Iterator[Card]:
        self._index = 0
        return self

    def __next__(self) -> Card:
        if self._index >= len(self._cards):
            raise StopIteration
        result = self._cards[self._index]
        self._index += 1
        return result

# =============================
# Demonstration
# =============================
def main():
    print("Creating a shuffled deck:")
    deck = Deck()
    print(deck.cards[:5])

    print("\nDrawing a card:")
    card = deck.draw()
    print(f"Drawn card: {card}")

    print("\nAdding a new card:")
    new_card = Card(CardSuit.HEARTS, CardRank.ACE)
    deck.add_card(new_card)
    print(f"Added: {new_card}")

    print("\nAccessing cards directly by index:")
    for i in range(5):
        print(f"Card at index {i}: {deck[i]}")

    print("\nIterating through remaining cards:")
    for c in deck:
        print(c)

if __name__ == "__main__":
    main()
