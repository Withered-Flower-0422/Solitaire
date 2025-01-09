import sys
import pygame

from solitaire import Solitaire

from source import src_path


class Display:
    def __init__(
        self,
        pos: tuple[int, int],
        img_path: str,
        size: tuple[int, int] = (80, 35),
    ):
        self.pos = pos
        self.size = size
        self.img = pygame.image.load(img_path)
        self.rect = self.img.get_rect()
        self.rect.topleft = pos


class Button(Display):
    def __init__(
        self,
        pos: tuple[int, int],
        callback: callable,
        img_path: str,
        size: tuple[int, int] = (80, 35),
    ):
        super().__init__(pos, img_path, size)
        self.on_click = callback


class Solitaire_Game:
    def __init__(self):
        # create solitaire game object
        self.solitaire = Solitaire()

        # create the game window
        pygame.init()
        self.screen = pygame.display.set_mode((960, 640))
        pygame.display.set_caption("Solitaire")
        pygame.display.set_icon(pygame.image.load(src_path["pics"]["icon"]))

        # pics
        self.cards_pics = [
            pygame.image.load(src_path["pics"]["cards"][i]) for i in range(0, 14)
        ]

        # snds
        self.sounds = {
            sound_name: pygame.mixer.Sound(src_path["sounds"][sound_name])
            for sound_name in ["complete", "deal", "done", "error", "pick", "undo"]
        }

        # variables
        self.from_idx: int | None = None
        self.to_idx: int | None = None
        self.mouse: tuple[int, int] = (0, 0)

        self.message: str = ""

        # create displays
        self.displays = {
            "done": Display(
                (12, 590),
                src_path["pics"]["displays"][self.solitaire.done_decks],
            ),
        }

        # create buttons
        self.btns = {
            "undo": Button(
                (872, 550),
                self.undo,
                src_path["pics"]["undo"],
            ),
            "deal": Button(
                (872, 590),
                self.deal_cards,
                src_path["pics"]["deals"][self.solitaire.remaining_heaps()],
            ),
        }

    def set_message(self, message: str):
        self.message = message

    def clear_message(self):
        self.message = ""

    def deal_cards(self):
        if self.solitaire.done_decks == 8:
            return
        if self.solitaire.remaining_heaps() == 0:
            return
        if self.solitaire.has_vacancies():
            self.set_message("Unable to deal cards when there are vacancies.")
            self.sounds["error"].play()
            return

        self.solitaire.deal()
        self.sounds["deal"].play()
        self.btns["deal"].img = pygame.image.load(
            src_path["pics"]["deals"][self.solitaire.remaining_heaps()]
        )

    def undo(self):
        if self.solitaire.done_decks == 8:
            return
        if self.solitaire.undo():
            self.clear_message()
            self.sounds["undo"].play()
            self.displays["done"].img = pygame.image.load(
                src_path["pics"]["displays"][self.solitaire.done_decks]
            )
            self.btns["deal"].img = pygame.image.load(
                src_path["pics"]["deals"][self.solitaire.remaining_heaps()]
            )

    def get_chosen_card_pos(self, mouse_pos: tuple[int, int]):
        for i, stack in enumerate(self.solitaire.stacks):
            for j in range(len(stack.cards) - 1, -1, -1):
                if pygame.Rect(96 * i + 8, 12 + 30 * j, 80, 35).collidepoint(mouse_pos):
                    return i, j
        return None

    def handle_events(self):
        for event in pygame.event.get():
            self.handle_quit(event)
            self.handle_btn(event)
            self.handle_remake(event)
            self.handle_drag(event)

    def handle_quit(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def handle_btn(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.btns.values():
                if btn.rect.collidepoint(event.pos):
                    btn.on_click()
                    break

    def handle_remake(self, event: pygame.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.solitaire = Solitaire()
                self.displays["done"].img = pygame.image.load(
                    src_path["pics"]["displays"][self.solitaire.done_decks]
                )
                self.btns["deal"].img = pygame.image.load(
                    src_path["pics"]["deals"][self.solitaire.remaining_heaps()]
                )
                self.clear_message()

    def handle_drag(self, event: pygame.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            chosen_card_pos = self.get_chosen_card_pos(event.pos)
            if chosen_card_pos is not None:
                self.clear_message()
                stack_idx, card_idx = chosen_card_pos
                self.from_idx = stack_idx
                if self.solitaire.hold_cards(self.from_idx, card_idx):
                    self.sounds["pick"].play()

        elif event.type == pygame.MOUSEBUTTONUP:
            target_stack_idx = event.pos[0] // 96
            if target_stack_idx < 0:
                target_stack_idx = 0
            if target_stack_idx > 9:
                target_stack_idx = 9
            self.to_idx = target_stack_idx

            if self.from_idx is not None and self.to_idx is not None:
                if self.solitaire.put_cards(self.to_idx, self.from_idx):
                    self.displays["done"].img = pygame.image.load(
                        src_path["pics"]["displays"][self.solitaire.done_decks]
                    )
                    if self.solitaire.done_decks < 8:
                        self.sounds["done"].play()
                    else:
                        self.set_message(
                            "Congratulations! You have completed the game!"
                        )
                        self.sounds["complete"].play()

        elif event.type == pygame.MOUSEMOTION:
            self.mouse = event.pos

    def update_display(self):
        """
        1. clear the screen
        2. draw the cards on the screen
        3. draw the displays and btns on the screen
        4. draw the holded card on the screen
        5. show the message on the screen
        """

        # 1.clear the screen
        self.screen.fill((0, 0, 0))

        # 2.draw the cards on the screen
        for i, stack in enumerate(self.solitaire.stacks):
            for j, card in enumerate(stack.cards):
                self.screen.blit(
                    self.cards_pics[card if j > stack.visible_index else 0],
                    (96 * i + 8, 12 + 30 * j),
                )

        # 3.draw the displays and btns on the screen
        for display in self.displays.values():
            self.screen.blit(display.img, display.rect)
        for btn in self.btns.values():
            self.screen.blit(btn.img, btn.rect)

        # 4.draw the holded card on the screen
        if self.solitaire.holdding:
            mouse_x, mouse_y = self.mouse
            for i, card in enumerate(self.solitaire.holdding):
                self.screen.blit(
                    self.cards_pics[card], (mouse_x - 40, mouse_y + 32 * i - 16)
                )

        # 5.show the message on the screen
        if self.message:
            font = pygame.font.Font(None, 32)
            text = font.render(self.message, True, (255, 0, 0))
            self.screen.blit(text, (248, 320))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update_display()


if __name__ == "__main__":
    Solitaire_Game().run()
