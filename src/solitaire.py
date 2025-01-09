import random

from stack import Stack


class Solitaire:
    def __init__(self):
        # cache
        self.caches: list[tuple[tuple[tuple[int]], tuple[int], tuple[int], int]] = []

        # prepare 8 shuffled decks of cards
        self.cards = list(range(13, 0, -1)) * 8
        random.shuffle(self.cards)

        # create 10 stacks of cards, index 0-3 contain 6 cards, index 4-9 contain 5 cards
        self.stacks = [
            Stack([self.cards.pop() for _ in range(6 if i < 4 else 5)])
            for i in range(10)
        ]

        # no cards are held at the beginning
        self.holdding: list[int] | None = None

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

            # check if the deck is done, if so, remove the done deck
            if self.stacks[stack_idx].check_done():
                self.done_decks += 1
                can_done = True

            for stack in self.stacks:
                stack.update_visiblity()

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
            )
        )

    # return true if undo is successful, false otherwise
    def undo(self) -> bool:
        if len(self.caches) < 2:
            return False
        self.caches.pop()
        stk, vis, crds, dne = self.caches[-1]
        for i, stack in enumerate(self.stacks):
            stack.cards = list(stk[i])
            stack.visible_index = vis[i]
        self.cards = list(crds)
        self.done_decks = dne
        return True


if __name__ == "__main__":
    Solitaire()
