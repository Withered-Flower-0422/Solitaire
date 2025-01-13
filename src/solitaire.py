import random
from time import time
from typing import Literal

from stack import Stack, Card


class Solitaire:
    def __init__(self, suit_num: Literal[1, 2, 4] = 1):
        # variables
        self.score = 500
        self.movements = 0
        self.start_time = time()
        self.end_time = None

        # cache
        self.caches: list[
            # stacks, visible indexes, remaining cards, done decks, score
            tuple[tuple[tuple[Card]], tuple[int], tuple[Card], int, int]
        ] = []

        # prepare 8 shuffled suits of cards
        self.cards: list[Card]
        match suit_num:
            case 1:
                self.cards = [("spade", i) for i in range(1, 14)] * 8
            case 2:
                self.cards = (
                    [("spade", i) for i in range(1, 14)]
                    + [("heart", i) for i in range(1, 14)]
                ) * 4
            case 4:
                self.cards = (
                    [("spade", i) for i in range(1, 14)]
                    + [("heart", i) for i in range(1, 14)]
                    + [("diamond", i) for i in range(1, 14)]
                    + [("club", i) for i in range(1, 14)]
                ) * 2
        random.shuffle(self.cards)

        # create 10 stacks of cards, index 0-3 contain 6 cards, index 4-9 contain 5 cards
        self.stacks = [
            Stack([self.cards.pop() for _ in range(6 if i < 4 else 5)])
            for i in range(10)
        ]

        # no cards are held at the beginning
        self.holdding: list[Card] | None = None

        # no deck is done at the beginning
        self.done_decks = 0

        self.cache()

    def remaining_heaps(self) -> int:
        return len(self.cards) // 10

    def hold_cards(self, stack_idx: int, card_idx: int) -> bool:
        """return true if any card can be held, false otherwise"""
        if self.stacks[stack_idx].can_pick(card_idx):
            self.holdding = self.stacks[stack_idx].cards[card_idx:]
            self.stacks[stack_idx].cards = self.stacks[stack_idx].cards[:card_idx]
        return bool(self.holdding)

    def put_cards(self, stack_idx: int, origin_stack_idx: int) -> bool:
        """return true if any deck can be done, false otherwise"""
        can_done = False

        if self.holdding is None:
            return False

        if stack_idx != origin_stack_idx and self.stacks[stack_idx].can_put(
            self.holdding[0]
        ):
            self.stacks[stack_idx].cards.extend(self.holdding)
            s = -1

            # check if the deck is done, if so, remove the done deck
            if self.stacks[stack_idx].check_done():
                self.done_decks += 1
                s = 100
                can_done = True
                if self.done_decks == 8:
                    self.end_time = time()

            for stack in self.stacks:
                stack.update_visiblity()

            self.score += s
            self.movements += 1
            self.cache()
        else:
            self.stacks[origin_stack_idx].cards.extend(self.holdding)

        self.holdding = None

        return can_done

    def has_vacancies(self) -> bool:
        return any(stack.is_empty() for stack in self.stacks)

    def deal(self):
        if self.has_vacancies():
            return
        if not self.cards:
            return
        for stack in self.stacks:
            stack.cards.append(self.cards.pop())
        self.movements += 1
        self.score -= 1
        self.cache()

    def cache(self):
        self.caches.append(
            (
                # stacks
                tuple(tuple(stack.cards) for stack in self.stacks),
                # visible indexes
                tuple(stack.visible_index for stack in self.stacks),
                # remaining cards
                tuple(self.cards),
                # done decks
                self.done_decks,
                # score
                self.score,
            )
        )

    # return true if undo is successful, false otherwise
    def undo(self) -> bool:
        if len(self.caches) < 2:
            return False
        self.caches.pop()
        stk, vis, crds, dne, sco = self.caches[-1]
        for i, stack in enumerate(self.stacks):
            stack.cards = list(stk[i])
            stack.visible_index = vis[i]
        self.cards = list(crds)
        self.done_decks = dne
        self.score = sco
        self.movements += 1
        return True


if __name__ == "__main__":
    Solitaire()
