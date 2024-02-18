import pygame
import os
import sys

pygame.init()

# Global Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
MENU_FONT = pygame.font.SysFont("comicsans", 50, True)  # Font for menu text
RETRO_FONT = pygame.font.SysFont("frankgoth", 70, italic=True)  # Font for title
BACKGROUND_IMAGE = pygame.image.load('imgs/bg.jpg')  # Background image
F1_CAR_IMAGE = pygame.image.load('imgs/f1.png')  # F1 car image

class Menu:
    def __init__(self):
        # Initialize the game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racing Game Menu")
        # Options available in the menu
        self.menu_options = ["Play", "Settings", "Credits"]
        self.padding = 10  # Padding between buttons
        self.button_space = 20  # Space between buttons
        self.button_y_offset = 100  # Offset of buttons from the top of the screen
        self.button_color = WHITE  # Default button color

    def draw(self):
        # Render the menu screen
        self.screen.fill(WHITE)
        self._draw_background()
        self._draw_title()
        self._draw_menu_buttons()
        pygame.display.update()

    def _draw_background(self):
        # Draw the background image
        background_image = pygame.transform.scale(BACKGROUND_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background_image, (0, 0))

    def _draw_title(self):
        # Render and display the "RETRO" text
        retro_text = RETRO_FONT.render("RETRO", True, BLACK)

        # Resize the F1 car image to be 100 pixels tall
        f1_car_height = 100
        f1_car_width = int(F1_CAR_IMAGE.get_width() * (f1_car_height / F1_CAR_IMAGE.get_height()))
        f1_car_image = pygame.transform.scale(F1_CAR_IMAGE, (f1_car_width, f1_car_height))

        # Set y-coordinate to position both elements at the top of the screen
        y_position = 20  

        # Calculate the position to center the image on the x-axis
        f1_car_x = (SCREEN_WIDTH - f1_car_width - retro_text.get_width() - 10) // 2

        # Calculate the position to place the retro text right next to the F1 car image
        retro_text_x = f1_car_x + f1_car_width  

        self.screen.blit(f1_car_image, (f1_car_x, y_position))  # Display the F1 car image
        self.screen.blit(retro_text, (retro_text_x, y_position+10))  # Display the retro text

    def _draw_menu_buttons(self):
        # Draw the menu buttons on the screen
        max_option_width = max([MENU_FONT.size(option)[0] for option in self.menu_options])
        button_height = MENU_FONT.size(self.menu_options[0])[1] + 2 * self.padding
        start_y = SCREEN_HEIGHT // 2 - (
                    (len(self.menu_options) * button_height) + ((len(self.menu_options) - 1) * self.button_space)) // 2 + self.button_y_offset
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(self.menu_options):
            option_text = MENU_FONT.render(option, True, BLACK)
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - max_option_width // 2, start_y + i * (button_height + self.button_space),
                max_option_width, button_height)

            self._draw_button(button_rect, option_text, mouse_pos)

    def _draw_button(self, button_rect, option_text, mouse_pos):
        # Draw an individual button on the screen
        if button_rect.collidepoint(mouse_pos):
            border_color = BLACK
            button_color = WHITE  # Set button color to white on hover
        else:
            border_color = WHITE
            button_color = self.button_color  # Use the defined button color

        pygame.draw.rect(self.screen, border_color, button_rect)
        pygame.draw.rect(self.screen, button_color, button_rect.inflate(-4, -4))

        text_x = button_rect.centerx - option_text.get_width() // 2
        text_y = button_rect.centery - option_text.get_height() // 2
        self.screen.blit(option_text, (text_x, text_y))


class UsernameEntry:
    def __init__(self):
        # Initialize the username entry screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sponsor Viewer")
        # Load paths to sponsor images
        self.sponsor_paths = self._load_sponsors()
        # Load sponsor images
        self.sponsors = [pygame.image.load(path) for path in self.sponsor_paths]
        self.current_sponsor_index = 0  # Index of the currently selected sponsor
        self.font = pygame.font.SysFont(None, 40)
        self.username = ""  # Store the entered username
        self.placeholder_text = "Enter your username"  # Placeholder text for the input field
        self.input_rect = pygame.Rect(200, 100, 400, 50)  # Rectangle for username input
        self.input_active = False  # Flag to track whether the input field is active
        self.text_color = BLACK

    def _load_sponsors(self):
        # Load paths to sponsor images from a directory
        sponsor_dir = "imgs/sponsors"
        sponsor_files = os.listdir(sponsor_dir)
        sponsors = [os.path.join(sponsor_dir, file) for file in sponsor_files]
        return sponsors

    def run(self):
        # Run the username entry screen
        running = True
        while running:
            self.screen.fill(WHITE)
            self._handle_events()

            self._draw_username_input()
            self._draw_sponsor_selection()
            self._draw_play_button()

            pygame.display.flip()

    def _handle_events(self):
        # Handle events such as mouse clicks and key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)
            elif event.type == pygame.KEYDOWN:
                self._handle_key_press(event)

    def _handle_mouse_click(self, event):
        # Handle mouse clicks on the screen
        if self.input_rect.collidepoint(event.pos):
            self.input_active = True
        else:
            self.input_active = False

        if 300 <= event.pos[0] <= 500 and 450 <= event.pos[1] <= 500:
            main(self.username, self.sponsor_paths[self.current_sponsor_index])  # Pass the path
        elif SCREEN_WIDTH // 2 - 150 <= event.pos[0] <= SCREEN_WIDTH // 2 - 50 and SCREEN_HEIGHT // 2 - 50 <= event.pos[
            1] <= SCREEN_HEIGHT // 2 + 50:
            self.current_sponsor_index = (self.current_sponsor_index - 1) % len(self.sponsors)
        elif SCREEN_WIDTH // 2 + 50 <= event.pos[0] <= SCREEN_WIDTH // 2 + 150 and SCREEN_HEIGHT // 2 - 50 <= event.pos[
            1] <= SCREEN_HEIGHT // 2 + 50:
            self.current_sponsor_index = (self.current_sponsor_index + 1) % len(self.sponsors)

    def _handle_key_press(self, event):
        # Handle key presses for entering the username
        if self.input_active:
            if event.key == pygame.K_RETURN:
                self.input_active = False
                self.text_color = BLACK
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            else:
                self.username += event.unicode

    def _draw_username_input(self):
        # Draw the username input field on the screen
        pygame.draw.rect(self.screen, self.text_color, self.input_rect, 2)
        if not self.username and not self.input_active:
            placeholder_surface = self.font.render(self.placeholder_text, True, GRAY)
            placeholder_rect = placeholder_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(placeholder_surface, placeholder_rect.topleft)
        else:
            text_surface = self.font.render(self.username, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.input_rect.center)
            self.screen.blit(text_surface, text_rect.topleft)

    def _draw_sponsor_selection(self):
        # Draw the sponsor selection area on the screen
        sponsor_x = (SCREEN_WIDTH - 100) // 2
        sponsor_y = (SCREEN_HEIGHT - 100) // 2
        sponsor_img = pygame.transform.scale(self.sponsors[self.current_sponsor_index], (100, 100))
        self.screen.blit(sponsor_img, (sponsor_x, sponsor_y))
        self._draw_arrow(sponsor_x, sponsor_y)

    def _draw_arrow(self, sponsor_x, sponsor_y):
        # Draw arrows to navigate through sponsors
        arrow_img = pygame.image.load("imgs/arrow.png")
        arrow_size = (100, 100)

        left_arrow_rotated = pygame.transform.scale(arrow_img, arrow_size)
        left_arrow_rotated = pygame.transform.rotate(left_arrow_rotated, -90)
        self.screen.blit(left_arrow_rotated, (sponsor_x - arrow_size[0] - 10, sponsor_y))

        right_arrow_rotated = pygame.transform.scale(arrow_img, arrow_size)
        right_arrow_rotated = pygame.transform.rotate(right_arrow_rotated, 90)
        self.screen.blit(right_arrow_rotated, (sponsor_x + 100 + 10, sponsor_y))

    def _draw_play_button(self):
        # Draw the play button on the screen
        pygame.draw.rect(self.screen, GRAY, (300, 450, 200, 50), 0)
        pygame.draw.rect(self.screen, WHITE, (300, 450, 200, 50), 3)
        play_text = self.font.render("Play Game", True, BLACK)
        self.screen.blit(play_text, (330, 460))


def main(username, sponsor_name):
    # Main function to start the game
    print("Running main() with username:", username)
    print("Sponsor:", sponsor_name)


def main_menu():
    # Main menu function to display the menu screen
    pygame.init()
    menu = Menu()  # Create a Menu object
    clock = pygame.time.Clock()  # Clock object to control frame rate
    run_menu = True

    while run_menu:
        clock.tick(60)  # Cap the frame rate at 60 FPS
        menu.draw()  # Draw the menu screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(menu.menu_options):
                    max_option_width = max([MENU_FONT.size(option)[0] for option in menu.menu_options])
                    button_height = MENU_FONT.size(menu.menu_options[0])[1] + 2 * menu.padding
                    button_rect = pygame.Rect(
                        SCREEN_WIDTH // 2 - max_option_width // 2,
                        SCREEN_HEIGHT // 2 - (
                                    (len(menu.menu_options) * button_height) + (
                                        (len(menu.menu_options) - 1) * menu.button_space)) // 2 + i * (
                                            button_height + menu.button_space) + menu.button_y_offset,
                        max_option_width,
                        button_height,
                    )
                    if button_rect.collidepoint(mouse_pos):
                        if option == "Play":
                            username_entry = UsernameEntry()
                            username_entry.run()


if __name__ == "__main__":
    main_menu()  # Run the main menu function when the script is executed
