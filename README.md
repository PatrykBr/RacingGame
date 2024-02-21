# Instructions:

**explenation of code:**
- username input has validation
- select different sponsors in menu and you get a different car depending on sponsor.
- npc car follow predetermined path and each time you win the npc car gets faster
- there is 10 levels and if you win all 10 then you win

find these lines in the code and then explain in doc. you can un-comment it and then play the game and ss the result. when screenshotting code remove most of the comments and keep only important ones

this shows the mask(hitbox) of the cars:

```python
#WIN.blit(self.mask.to_surface(), self.mask_rect.topleft)
```
\
this shows the mask(hitbox) of the track border and finish:

```python
#WIN.blit(TRACK_BORDER_MASK.to_surface(), (track_border_x, track_border_y))
#WIN.blit(FINISH_MASK.to_surface(), FINISH_POSITION)
```
\
displaying the npc path points:
```python
# def draw_points(self, win):
	# for point in self.path:
	# pygame.draw.circle(win, (255, 0, 0), point, 5)
  
# def draw(self, win):
	# super().draw(win)
	# self.draw_points(win)

# if event.type == pygame.MOUSEBUTTONDOWN:
	# pos = pygame.mouse.get_pos()
	# computer_car.path.append(pos)

#print(computer_car.path)
```
make sure to click on the screen and then press any button on keyboard to display the path points
