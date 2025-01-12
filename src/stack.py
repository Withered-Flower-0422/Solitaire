from typing import Literal

Card = tuple[
    Literal["heart", "diamond", "club", "spade"],
    Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
]


class Stack:
    def __init__(self, cards: list[Card]):
        self.cards = cards
        self.visible_index = len(cards) - 2

    def is_empty(self) -> bool:
        return len(self.cards) == 0

    def can_pick(self, card_idx: int) -> bool:
        if card_idx <= self.visible_index:
            return False
        suit, value = self.cards[card_idx]
        rest = self.cards[card_idx:]
        return rest == list((suit, i) for i in range(value, 0, -1))[: len(rest)]

    def can_put(self, card: Card) -> bool:
        if self.is_empty():
            return True
        return self.cards[-1][1] == card[1] + 1

    def check_done(self) -> bool:
        for i, card in enumerate(self.cards):
            suit, value = card
            if (
                i > self.visible_index
                and value == 13
                and self.cards[i:] == list((suit, i) for i in range(13, 0, -1))
            ):
                self.cards = self.cards[:i]
                return True
        return False

    def update_visiblity(self):
        if len(self.cards) == self.visible_index + 1:
            self.visible_index -= 1


if __name__ == "__main__":
    stack = Stack(list(("spade", i) for i in range(13, 0, -1)))

    for card in stack.cards:
        print(card)
