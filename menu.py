import pygame  # Import the pygame library for game development
import os  # Import the os module for interacting with the operating system
import sys  # Import the sys module for system-specific parameters and functions
from main import play_game  # Importing the play_game function from another module

# Global Constants
WHITE = (255, 255, 255)  # RGB color tuple for white
BLACK = (0, 0, 0)  # RGB color tuple for black
GRAY = (200, 200, 200)  # RGB color tuple for gray
RED = (255, 0, 0)  # RGB color tuple for red

# Fonts and Images
MENU_FONT = pygame.font.SysFont("comicsans", 50, True)  # Font for menu text
RETRO_FONT = pygame.font.SysFont("frankgoth", 70, italic=True)  # Font for title
BACKGROUND_IMAGE = pygame.image.load('imgs/bg.jpg')  # Background image
F1_CAR_IMAGE = pygame.image.load('imgs/f1.png')  # F1 car image
ARROW_IMAGE = pygame.image.load("imgs/arrow.png")  # Arrow image

# Menu Class
class Menu:
    def __init__(self, screen):
        self.screen = screen  # Initialize the screen attribute
        pygame.display.set_caption("Racing Game Menu")  # Set the window title
        self.menu_options = ["Play", "Controls", "Credits"]  # Options displayed in the menu
        self.padding = 10  # Padding for button rendering
        self.button_space = 20  # Space between buttons
        self.button_y_offset = 100  # Vertical offset for buttons
        self.button_color = WHITE  # Default button color

    # Draw the menu
    def draw(self):
        self.screen.fill(WHITE)  # Fill the screen with white
        self._draw_background()  # Draw the background image
        self._draw_title()  # Draw the game title
        self._draw_menu_buttons()  # Draw the menu buttons
        pygame.display.update()  # Update the display

    # Draw the background image
    def _draw_background(self):
        background_image = pygame.transform.scale(BACKGROUND_IMAGE, self.screen.get_size())  # Scale background image to screen size
        self.screen.blit(background_image, (0, 0))  # Draw background image on screen

    # Draw the game title
    def _draw_title(self):
        retro_text = RETRO_FONT.render("RETRO", True, BLACK)  # Render retro text
        f1_car_height = 100  # Height of F1 car image
        f1_car_width = int(F1_CAR_IMAGE.get_width() * (f1_car_height / F1_CAR_IMAGE.get_height()))  # Calculate width of F1 car image
        f1_car_image = pygame.transform.scale(F1_CAR_IMAGE, (f1_car_width, f1_car_height))  # Scale F1 car image
        y_position = 20  # Y position of the title
        f1_car_x = (self.screen.get_width() - f1_car_width - retro_text.get_width() - 10) // 2  # X position of F1 car image
        retro_text_x = f1_car_x + f1_car_width  # X position of retro text
        self.screen.blit(f1_car_image, (f1_car_x, y_position))  # Draw F1 car image on screen
        self.screen.blit(retro_text, (retro_text_x, y_position + 10))  # Draw retro text on screen

    # Draw the menu buttons
    def _draw_menu_buttons(self):
        max_option_width = max([MENU_FONT.size(option)[0] for option in self.menu_options])  # Get maximum width of menu options
        button_height = MENU_FONT.size(self.menu_options[0])[1] + 2 * self.padding  # Calculate button height
        start_y = self.screen.get_height() // 2 - (
                    (len(self.menu_options) * button_height) + ((len(self.menu_options) - 1) * self.button_space)) // 2 + self.button_y_offset  # Starting Y position for buttons
        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position

        for i, option in enumerate(self.menu_options):  # Iterate through menu options
            option_text = MENU_FONT.render(option, True, BLACK)  # Render menu option text
            button_rect = pygame.Rect(
                self.screen.get_width() // 2 - max_option_width // 2,
                start_y + i * (button_height + self.button_space),
                max_option_width, button_height)  # Create button rectangle

            self._draw_button(button_rect, option_text, mouse_pos)  # Draw button

    # Draw a button
    def _draw_button(self, button_rect, option_text, mouse_pos):
        if button_rect.collidepoint(mouse_pos):  # Check if mouse is over button
            border_color = BLACK  # Set border color to black
            button_color = WHITE  # Set button color to white
        else:
            border_color = WHITE  # Set border color to white
            button_color = self.button_color  # Set button color to default color

        pygame.draw.rect(self.screen, border_color, button_rect)  # Draw button border
        pygame.draw.rect(self.screen, button_color, button_rect.inflate(-4, -4))  # Draw button
        text_x = button_rect.centerx - option_text.get_width() // 2  # Calculate X position for text
        text_y = button_rect.centery - option_text.get_height() // 2  # Calculate Y position for text
        self.screen.blit(option_text, (text_x, text_y))  # Draw text on button

# ControlsScreen Class
class ControlsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.transform.scale(BACKGROUND_IMAGE, self.screen.get_size())
        self.font = pygame.font.SysFont(None, 50)
        self.controls_text = ["Controls:", "W - Forward", "S - Backward", "A - Left", "D - Right"]
        self.back_button_text = "Back"
        self.back_button_font = pygame.font.SysFont(None, 40)
        self.back_button_rect = pygame.Rect(50, 50, 100, 50)

    def _draw_controls(self):
        # Display background image
        self.screen.blit(self.background_image, (0, 0))

        # Calculate the size of the white box based on the size of the controls text
        text_width = max([self.font.size(line)[0] for line in self.controls_text])
        text_height = len(self.controls_text) * self.font.get_linesize()
        padding = 50

        # Calculate position for the white box
        controls_background_rect = pygame.Rect(
            (self.screen.get_width() - text_width - padding) // 2,
            (self.screen.get_height() - text_height - padding) // 2,
            text_width + padding,
            text_height + padding
        )
        pygame.draw.rect(self.screen, WHITE, controls_background_rect)

        # Draw controls text
        controls_position = (self.screen.get_width() // 2, (self.screen.get_height() - text_height) // 2)
        for idx, line in enumerate(self.controls_text):
            controls_surface = self.font.render(line, True, BLACK)
            controls_rect = controls_surface.get_rect(center=(controls_position[0], controls_position[1] + idx * 50))
            self.screen.blit(controls_surface, controls_rect)

        # Draw back button
        pygame.draw.rect(self.screen, GRAY, self.back_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.back_button_rect, 3)
        back_text_surface = self.back_button_font.render(self.back_button_text, True, BLACK)
        back_text_rect = back_text_surface.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text_surface, back_text_rect)

    def is_back_button_clicked(self, pos):
        return self.back_button_rect.collidepoint(pos)


# CreditsScreen Class
class CreditsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.transform.scale(BACKGROUND_IMAGE, self.screen.get_size())
        self.font = pygame.font.SysFont(None, 50)
        self.credits_text = [
            "Credits: ",
        ]
        self.back_button_text = "Back"
        self.back_button_font = pygame.font.SysFont(None, 40)
        self.back_button_rect = pygame.Rect(50, 50, 100, 50)

    def _draw_credits(self):
        # Display background image
        self.screen.blit(self.background_image, (0, 0))

        # Calculate the size of the white box based on the size of the credits text
        text_width = max([self.font.size(line)[0] for line in self.credits_text])
        text_height = len(self.credits_text) * self.font.get_linesize()
        padding = 50

        # Calculate position for the white box
        credits_background_rect = pygame.Rect(
            (self.screen.get_width() - text_width - padding) // 2,
            (self.screen.get_height() - text_height - padding) // 2,
            text_width + padding,
            text_height + padding
        )
        pygame.draw.rect(self.screen, WHITE, credits_background_rect)

        # Draw credits text
        credits_position = (self.screen.get_width() // 2, (self.screen.get_height() - text_height) // 2)
        for idx, line in enumerate(self.credits_text):
            credits_surface = self.font.render(line, True, BLACK)
            credits_rect = credits_surface.get_rect(center=(credits_position[0], credits_position[1] + idx * 50))
            self.screen.blit(credits_surface, credits_rect)

        # Draw back button
        pygame.draw.rect(self.screen, GRAY, self.back_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.back_button_rect, 3)
        back_text_surface = self.back_button_font.render(self.back_button_text, True, BLACK)
        back_text_rect = back_text_surface.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text_surface, back_text_rect)

    def is_back_button_clicked(self, pos):
        return self.back_button_rect.collidepoint(pos)

# PlayScreen Class
class PlayScreen:
    def __init__(self, screen):
        self.screen = screen
        pygame.display.set_caption("Sponsor Viewer")
        self.sponsor_info = self._load_sponsors()
        self.sponsors = [pygame.image.load(os.path.join('imgs/sponsors', name + extension)) for name, extension in self.sponsor_info]
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
        self.back_button_text = "Back"
        self.back_button_font = pygame.font.SysFont(None, 40)
        self.back_button_rect = pygame.Rect(50, 50, 100, 50)

    # Run the play screen
    def run(self):
        running = True
        while running:  # Main game loop
            self.screen.fill(WHITE)  # Fill the screen with white
            self._draw_back_button()  # Draw back button
            for event in pygame.event.get():  # Check events
                if event.type == pygame.QUIT:  # Check if user wants to quit
                    pygame.quit()  # Quit pygame
                    sys.exit()  # Exit the program
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Check if mouse button is clicked
                    self._handle_mouse_click(event)  # Handle mouse click event
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_back_button_clicked(mouse_pos):
                        running = False  # Exit the play screen loop
                elif event.type == pygame.KEYDOWN:  # Check if key is pressed
                    self._handle_key_press(event)  # Handle key press event
                elif event.type == pygame.VIDEORESIZE:  # Check if window is resized
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)  # Resize the window

            self._draw_background()  # Draw the background
            self._draw_back_button()
            self._draw_username_input()  # Draw username input field
            self._draw_select_sponsor_text()  # Draw text for selecting sponsor
            self._draw_sponsor_selection()  # Draw sponsor selection
            self._draw_play_button()  # Draw play button
            self._draw_error_message()  # Draw error message
            pygame.display.flip()  # Update the display

    # Draw the background
    def _draw_background(self):
        background_image = pygame.transform.scale(BACKGROUND_IMAGE, self.screen.get_size())  # Scale background image to screen size
        self.screen.blit(background_image, (0, 0))  # Draw background image on screen        

    # Draw the text for selecting sponsor
    def _draw_select_sponsor_text(self):
        select_sponsor_surface = self.font.render(self.select_sponsor_text, True, WHITE)  # Render text for selecting sponsor
        select_sponsor_rect = select_sponsor_surface.get_rect()  # Get rectangle for text
        select_sponsor_rect.midtop = (self.screen.get_width() // 2, self.screen.get_height() // 2.8)  # Position text
        self.screen.blit(select_sponsor_surface, select_sponsor_rect)  # Draw text on screen

    # Load sponsor names and extensions
    def _load_sponsors(self):
        sponsor_dir = "imgs/sponsors"  # Directory containing sponsor images
        sponsor_files = os.listdir(sponsor_dir)  # List files in sponsor directory
        sponsors = [(os.path.splitext(file)[0], os.path.splitext(file)[1]) for file in sponsor_files]  # Create tuples of name and extension
        return sponsors  # Return sponsor information

    # Validate username
    def _validate_username(self):
        if len(self.username) < 3:  # Check if username is too short
            self.error_message = "Username must be at least 3 characters long"  # Set error message
            return False  # Return False
        elif len(self.username) > 20:  # Check if username is too long
            self.error_message = "Username must be at most 20 characters long"  # Set error message
            return False  # Return False
        else:
            self.error_message = ""  # Clear error message
            return True  # Return True

    # Draw error message
    def _draw_error_message(self):
        if self.error_message:  # Check if there is an error message
            error_surface = self.font.render(self.error_message, True, RED)  # Render error message
            error_rect = error_surface.get_rect(center=(self.screen.get_width() // 2, self.input_rect.bottom + 20))  # Get rectangle for error message
            self.screen.blit(error_surface, error_rect)  # Draw error message on screen

    # Handle mouse click events
    def _handle_mouse_click(self, event):
        mouse_pos = pygame.mouse.get_pos()  # Get current mouse position
        play_button_rect = pygame.Rect(
            (self.screen.get_width() - 200) // 2,
            self.screen.get_height() // 1.3,
            200,
            50
        )  # Rectangle for play button

        if play_button_rect.collidepoint(mouse_pos):  # Check if play button is clicked
            if self._validate_username():  # Check if username is valid
                main(self.username, self.sponsor_info[self.current_sponsor_index])  # Call main function with username and sponsor info
        else:
            if self.input_rect.collidepoint(mouse_pos):  # Check if mouse is over username input field
                self.input_active = True  # Activate username input field
            else:
                self.input_active = False  # Deactivate username input field

            left_arrow_rect, right_arrow_rect = self._draw_arrow((self.screen.get_width() - 100) // 2,
                                                                 (self.screen.get_height() - 100) // 2)  # Draw arrow buttons

            if left_arrow_rect.collidepoint(mouse_pos):  # Check if left arrow is clicked
                self.current_sponsor_index = (self.current_sponsor_index - 1) % len(self.sponsors)  # Change current sponsor index
            elif right_arrow_rect.collidepoint(mouse_pos):  # Check if right arrow is clicked
                self.current_sponsor_index = (self.current_sponsor_index + 1) % len(self.sponsors)  # Change current sponsor index

    # Handle key press events
    def _handle_key_press(self, event):
        if self.input_active:  # Check if username input field is active
            if event.key == pygame.K_RETURN:  # Check if Enter key is pressed
                self.input_active = False  # Deactivate username input field
                self.text_color = BLACK  # Change text color to black
            elif event.key == pygame.K_BACKSPACE:  # Check if Backspace key is pressed
                self.username = self.username[:-1]  # Remove last character from username
            else:
                self.username += event.unicode  # Add pressed character to username

    # Draw username input field
    def _draw_username_input(self):
        input_rect_width = self.screen.get_width() // 3  # Width of input field rectangle
        input_rect_height = 50  # Height of input field rectangle
        input_rect_x = (self.screen.get_width() - input_rect_width) // 2  # X position of input field rectangle
        input_rect_y = self.screen.get_height() // 6  # Y position of input field rectangle

        self.input_rect = pygame.Rect(input_rect_x, input_rect_y, input_rect_width, input_rect_height)  # Set input field rectangle

        pygame.draw.rect(self.screen, self.text_color, self.input_rect, 2)  # Draw input field rectangle
        if not self.username and not self.input_active:  # Check if username is empty and input field is not active
            placeholder_surface = self.font.render(self.placeholder_text, True, GRAY)  # Render placeholder text
            placeholder_rect = placeholder_surface.get_rect(center=self.input_rect.center)  # Get rectangle for placeholder text
            self.screen.blit(placeholder_surface, placeholder_rect.topleft)  # Draw placeholder text on screen
        else:
            text_surface = self.font.render(self.username, True, self.text_color)  # Render username text
            text_rect = text_surface.get_rect(center=self.input_rect.center)  # Get rectangle for username text
            self.screen.blit(text_surface, text_rect.topleft)  # Draw username text on screen

    # Draw sponsor selection
    def _draw_sponsor_selection(self):
        sponsor_x = (self.screen.get_width() - 100) // 2  # X position for sponsor selection
        sponsor_y = (self.screen.get_height() - 100) // 2  # Y position for sponsor selection
        sponsor_img = pygame.transform.scale(self.sponsors[self.current_sponsor_index], (100, 100))  # Scale sponsor image
        self.screen.blit(sponsor_img, (sponsor_x, sponsor_y))  # Draw sponsor image on screen
        self._draw_arrow(sponsor_x, sponsor_y)  # Draw arrow buttons

    # Draw arrow buttons for sponsor selection
    def _draw_arrow(self, sponsor_x, sponsor_y):
        arrow_size = (50, 70)  # Size of arrow buttons

        left_arrow_rect = pygame.Rect(sponsor_x - arrow_size[0] - 10, sponsor_y + arrow_size[0] / 2, arrow_size[0], arrow_size[1])  # Rectangle for left arrow
        right_arrow_rect = pygame.Rect(sponsor_x + arrow_size[1] + 20, sponsor_y + arrow_size[0] / 2, arrow_size[0], arrow_size[1])  # Rectangle for right arrow

        left_arrow_rotated = pygame.transform.scale(ARROW_IMAGE, arrow_size)  # Scale left arrow image
        left_arrow_rotated = pygame.transform.rotate(left_arrow_rotated, -90)  # Rotate left arrow
        self.screen.blit(left_arrow_rotated, (sponsor_x - arrow_size[0] - 10, sponsor_y + arrow_size[0] / 2))  # Draw left arrow on screen

        right_arrow_rotated = pygame.transform.scale(ARROW_IMAGE, arrow_size)  # Scale right arrow image
        right_arrow_rotated = pygame.transform.rotate(right_arrow_rotated, 90)  # Rotate right arrow
        self.screen.blit(right_arrow_rotated, (sponsor_x + arrow_size[1] + 20, sponsor_y + arrow_size[0] / 2))  # Draw right arrow on screen

        return left_arrow_rect, right_arrow_rect  # Return rectangles for arrow buttons

    # Draw the play button
    def _draw_play_button(self):
        button_width = 200  # Width of play button
        button_height = 50  # Height of play button
        button_x = (self.screen.get_width() - button_width) // 2  # X position of play button
        button_y = self.screen.get_height() // 1.3  # Y position of play button

        pygame.draw.rect(self.screen, GRAY, (button_x, button_y, button_width, button_height), 0)  # Draw play button
        pygame.draw.rect(self.screen, WHITE, (button_x, button_y, button_width, button_height), 3)  # Draw play button border
        play_text = self.font.render("Play Game", True, BLACK)  # Render text for play button
        text_x = button_x + (button_width - play_text.get_width()) // 2  # X position for play button text
        text_y = button_y + (button_height - play_text.get_height()) // 2  # Y position for play button text
        self.screen.blit(play_text, (text_x, text_y))  # Draw play button text on screen

    def _draw_back_button(self):
        # Draw back button
        pygame.draw.rect(self.screen, GRAY, self.back_button_rect)
        pygame.draw.rect(self.screen, WHITE, self.back_button_rect, 3)
        back_text_surface = self.back_button_font.render(self.back_button_text, True, BLACK)
        back_text_rect = back_text_surface.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text_surface, back_text_rect)

    def is_back_button_clicked(self, pos):
        return self.back_button_rect.collidepoint(pos)


# Main function to start the game
def main(username, sponsor_info):
    sponsor_name, extension = sponsor_info  # Get sponsor name and extension
    sponsor_filename = sponsor_name + extension  # Concatenate sponsor name and extension
    play_game(username, sponsor_filename)  # Call play_game function with username and sponsor filename


def main_menu():
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    menu = Menu(screen)
    controls_screen = ControlsScreen(screen)
    credits_screen = CreditsScreen(screen)
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
                        elif option == "Controls":
                            controls_screen._draw_controls()
                            pygame.display.flip()
                            waiting_for_back = True
                            while waiting_for_back:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if controls_screen.is_back_button_clicked(event.pos):
                                            waiting_for_back = False
                                            screen.fill(WHITE)
                                            menu.draw()
                                            pygame.display.flip()
                                            break
                        elif option == "Credits":
                            credits_screen._draw_credits()
                            pygame.display.flip()
                            waiting_for_back = True
                            while waiting_for_back:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if credits_screen.is_back_button_clicked(event.pos):
                                            waiting_for_back = False
                                            screen.fill(WHITE)
                                            menu.draw()
                                            pygame.display.flip()
                                            break

if __name__ == "__main__":
    main_menu()