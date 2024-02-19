import pygame
import os
import sys
from game import play_game  # Importing the play_game function from another module

# Global Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Fonts and Images
MENU_FONT = pygame.font.SysFont("comicsans", 50, True)  # Font for menu text
RETRO_FONT = pygame.font.SysFont("frankgoth", 70, italic=True)  # Font for title
BACKGROUND_IMAGE = pygame.image.load('imgs/bg.jpg')  # Background image
F1_CAR_IMAGE = pygame.image.load('imgs/f1.png')  # F1 car image
ARROW_IMAGE = pygame.image.load("imgs/arrow.png")  # Arrow image

# Menu Class
class Menu:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption("Racing Game Menu")
        self.menu_options = ["Play", "Settings", "Credits"]  # Options displayed in the menu
        self.padding = 10  # Padding for button rendering
        self.button_space = 20  # Space between buttons
        self.button_y_offset = 100  # Vertical offset for buttons
        self.button_color = WHITE  # Default button color

    # Draw the menu
    def draw(self):
        self.screen.fill(WHITE)
        self._draw_background()
        self._draw_title()
        self._draw_menu_buttons()
        pygame.display.update()

    # Draw the background image
    def _draw_background(self):
        background_image = pygame.transform.scale(BACKGROUND_IMAGE, self.screen.get_size())
        self.screen.blit(background_image, (0, 0))

    # Draw the game title
    def _draw_title(self):
        retro_text = RETRO_FONT.render("RETRO", True, BLACK)
        f1_car_height = 100
        f1_car_width = int(F1_CAR_IMAGE.get_width() * (f1_car_height / F1_CAR_IMAGE.get_height()))
        f1_car_image = pygame.transform.scale(F1_CAR_IMAGE, (f1_car_width, f1_car_height))
        y_position = 20
        f1_car_x = (self.screen.get_width() - f1_car_width - retro_text.get_width() - 10) // 2
        retro_text_x = f1_car_x + f1_car_width
        self.screen.blit(f1_car_image, (f1_car_x, y_position))
        self.screen.blit(retro_text, (retro_text_x, y_position + 10))

    # Draw the menu buttons
    def _draw_menu_buttons(self):
        max_option_width = max([MENU_FONT.size(option)[0] for option in self.menu_options])
        button_height = MENU_FONT.size(self.menu_options[0])[1] + 2 * self.padding
        start_y = self.screen.get_height() // 2 - (
                    (len(self.menu_options) * button_height) + ((len(self.menu_options) - 1) * self.button_space)) // 2 + self.button_y_offset
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(self.menu_options):
            option_text = MENU_FONT.render(option, True, BLACK)
            button_rect = pygame.Rect(
                self.screen.get_width() // 2 - max_option_width // 2,
                start_y + i * (button_height + self.button_space),
                max_option_width, button_height)

            self._draw_button(button_rect, option_text, mouse_pos)

    # Draw a button
    def _draw_button(self, button_rect, option_text, mouse_pos):
        if button_rect.collidepoint(mouse_pos):
            border_color = BLACK
            button_color = WHITE
        else:
            border_color = WHITE
            button_color = self.button_color

        pygame.draw.rect(self.screen, border_color, button_rect)
        pygame.draw.rect(self.screen, button_color, button_rect.inflate(-4, -4))

        text_x = button_rect.centerx - option_text.get_width() // 2
        text_y = button_rect.centery - option_text.get_height() // 2
        self.screen.blit(option_text, (text_x, text_y))


# PlayScreen Class
class PlayScreen:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption("Sponsor Viewer")
        self.sponsor_paths = self._load_sponsors()
        self.sponsors = [pygame.image.load(path) for path in self.sponsor_paths]
        self.current_sponsor_index = 0
        self.font = pygame.font.SysFont(None, 40)
        self.username = ""
        self.placeholder_text = "Enter your username"
        self.input_rect = pygame.Rect(200, 100, 400, 50)
        self.input_active = False
        self.text_color = BLACK
        self.select_sponsor_text = "Select a sponsor"
        self.error_message = ""
        self.arrow_left_rect = pygame.Rect((self.screen.get_width() - 200) // 2 - 70,
                                           (self.screen.get_height() - 100) // 2 + 25, 50, 50)
        self.arrow_right_rect = pygame.Rect((self.screen.get_width() - 200) // 2 + 200 + 20,
                                            (self.screen.get_height() - 100) // 2 + 25, 50, 50)

    # Run the play screen
    def run(self):
        running = True
        while running:
            self.screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event)
                elif event.type == pygame.KEYDOWN:
                    self._handle_key_press(event)
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            self._draw_background()
            self._draw_username_input()
            self._draw_select_sponsor_text()
            self._draw_sponsor_selection()
            self._draw_play_button()
            self._draw_error_message()

            pygame.display.flip()

    # Draw the background
    def _draw_background(self):
        background_image = pygame.transform.scale(BACKGROUND_IMAGE, self.screen.get_size())
        self.screen.blit(background_image, (0, 0))

    # Draw the text for selecting sponsor
    def _draw_select_sponsor_text(self):
        select_sponsor_surface = self.font.render(self.select_sponsor_text, True, WHITE)
        select_sponsor_rect = select_sponsor_surface.get_rect()
        select_sponsor_rect.midtop = (self.screen.get_width() // 2, self.screen.get_height() // 2.8)
        self.screen.blit(select_sponsor_surface, select_sponsor_rect)

    # Load sponsor images
    def _load_sponsors(self):
        sponsor_dir = "imgs/sponsors"
        sponsor_files = os.listdir(sponsor_dir)
        sponsors = [os.path.join(sponsor_dir, file) for file in sponsor_files]
        return sponsors

    # Validate username
    def _validate_username(self):
        if len(self.username) < 3:
            self.error_message = "Username must be at least 3 characters long"
            return False
        elif len(self.username) > 20:
            self.error_message = "Username must be at most 20 characters long"
            return False
        else:
            self.error_message = ""
            return True

    # Draw error message
    def _draw_error_message(self):
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, RED)
            error_rect = error_surface.get_rect(center=(self.screen.get_width() // 2, self.input_rect.bottom + 20))
            self.screen.blit(error_surface, error_rect)

    # Handle mouse click events
    def _handle_mouse_click(self, event):
        mouse_pos = pygame.mouse.get_pos()
        play_button_rect = pygame.Rect(
            (self.screen.get_width() - 200) // 2,
            self.screen.get_height() // 1.3,
            200,
            50
        )

        if play_button_rect.collidepoint(mouse_pos):
            if self._validate_username():
                main(self.username, self.sponsor_paths[self.current_sponsor_index])
        else:
            if self.input_rect.collidepoint(mouse_pos):
                self.input_active = True
            else:
                self.input_active = False

            left_arrow_rect, right_arrow_rect = self._draw_arrow((self.screen.get_width() - 100) // 2,
                                                                 (self.screen.get_height() - 100) // 2)

            if left_arrow_rect.collidepoint(mouse_pos):
                self.current_sponsor_index = (self.current_sponsor_index - 1) % len(self.sponsors)
            elif right_arrow_rect.collidepoint(mouse_pos):
                self.current_sponsor_index = (self.current_sponsor_index + 1) % len(self.sponsors)

    # Handle key press events
    def _handle_key_press(self, event):
        if self.input_active:
            if event.key == pygame.K_RETURN:
                self.input_active = False
                self.text_color = BLACK
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            else:
                self.username += event.unicode

    # Draw username input field
    def _draw_username_input(self):
        input_rect_width = self.screen.get_width() // 3
        input_rect_height = 50
        input_rect_x = (self.screen.get_width() - input_rect_width) // 2
        input_rect_y = self.screen.get_height() // 6

        self.input_rect = pygame.Rect(input_rect_x, input_rect_y, input_rect_width, input_rect_height)

        pygame.draw.rect(self.screen, self.text_color, self.input_rect, 2)
        if not self.username and not self.input_active:
            placeholder_surface = self.font.render(self.placeholder_text, True, GRAY)
            placeholder_rect = placeholder_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(placeholder_surface, placeholder_rect.topleft)
        else:
            text_surface = self.font.render(self.username, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(text_surface, text_rect.topleft)

    # Draw sponsor selection
    def _draw_sponsor_selection(self):
        sponsor_x = (self.screen.get_width() - 100) // 2
        sponsor_y = (self.screen.get_height() - 100) // 2
        sponsor_img = pygame.transform.scale(self.sponsors[self.current_sponsor_index], (100, 100))
        self.screen.blit(sponsor_img, (sponsor_x, sponsor_y))
        self._draw_arrow(sponsor_x, sponsor_y)

    # Draw arrow buttons for sponsor selection
    def _draw_arrow(self, sponsor_x, sponsor_y):
        arrow_size = (50, 70)

        left_arrow_rect = pygame.Rect(sponsor_x - arrow_size[0] - 10, sponsor_y + arrow_size[0] / 2, arrow_size[0], arrow_size[1])
        right_arrow_rect = pygame.Rect(sponsor_x + arrow_size[1] + 20, sponsor_y + arrow_size[0] / 2, arrow_size[0], arrow_size[1])

        left_arrow_rotated = pygame.transform.scale(ARROW_IMAGE, arrow_size)
        left_arrow_rotated = pygame.transform.rotate(left_arrow_rotated, -90)
        self.screen.blit(left_arrow_rotated, (sponsor_x - arrow_size[0] - 10, sponsor_y + arrow_size[0] / 2))

        right_arrow_rotated = pygame.transform.scale(ARROW_IMAGE, arrow_size)
        right_arrow_rotated = pygame.transform.rotate(right_arrow_rotated, 90)
        self.screen.blit(right_arrow_rotated, (sponsor_x + arrow_size[1] + 20, sponsor_y + arrow_size[0] / 2))

        return left_arrow_rect, right_arrow_rect

    # Draw the play button
    def _draw_play_button(self):
        button_width = 200
        button_height = 50
        button_x = (self.screen.get_width() - button_width) // 2
        button_y = self.screen.get_height() // 1.3

        pygame.draw.rect(self.screen, GRAY, (button_x, button_y, button_width, button_height), 0)
        pygame.draw.rect(self.screen, WHITE, (button_x, button_y, button_width, button_height), 3)
        play_text = self.font.render("Play Game", True, BLACK)
        text_x = button_x + (button_width - play_text.get_width()) // 2
        text_y = button_y + (button_height - play_text.get_height()) // 2
        self.screen.blit(play_text, (text_x, text_y))


# Main function to start the game
def main(username, sponsor_name):
    play_game(username, sponsor_name)


# Main menu function
def main_menu():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    menu = Menu(screen)
    clock = pygame.time.Clock()
    run_menu = True

    while run_menu:
        clock.tick(60)
        menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(menu.menu_options):
                    max_option_width = max([MENU_FONT.size(option)[0] for option in menu.menu_options])
                    button_height = MENU_FONT.size(menu.menu_options[0])[1] + 2 * menu.padding
                    button_rect = pygame.Rect(
                        screen.get_width() // 2 - max_option_width // 2,
                        screen.get_height() // 2 - (
                                (len(menu.menu_options) * button_height) + (
                                    (len(menu.menu_options) - 1) * menu.button_space)) // 2 + i * (
                                        button_height + menu.button_space) + menu.button_y_offset,
                        max_option_width,
                        button_height,
                    )
                    if button_rect.collidepoint(mouse_pos):
                        if option == "Play":
                            play_screen = PlayScreen(screen)
                            play_screen.run()


if __name__ == "__main__":
    main_menu()
