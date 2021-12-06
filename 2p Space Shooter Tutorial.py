import arcade 
from os import path 

DIR = path.dirname(path.abspath(__file__))

SPRITE_SCALING_PLAYERS = 0.75
SPRITE_SCALING_LASERS = 0.75

P1_MAX_HEALTH = 3
P2_MAX_HEALTH = 3

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800 
SCREEN_TITLE = "2 Player Space Shooter"

PLAYER_SPEED = 5
LASER_SPEED = 10

winner = None 

class TitleView(arcade.View):
    """ View to show the title screen """

    def on_show(self):
        self.texture = arcade.load_texture(f"{DIR}\\space_shooter_title.png")

        # Reset the viewport, if necessary if we have a scrolling game and we need 
        # to reset the viewport back to the start so we can see what we draw
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw the view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

class GameOverView(arcade.View):
    """ View to show when the game is over """
     
    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()
        self.winner = None 
        arcade.set_background_color(arcade.color.BLACK)

        """ Reset the viewport"""
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render() 
        arcade.draw_text(
            f"GAME OVER\n{self.winner} WINS!\n(Press 'ENTER' to play again)",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            35,
            anchor_x='center',
            anchor_y='center',
            width = SCREEN_WIDTH,
            multiline = True,
            align='center'
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

class GameView(arcade.View):
    """ Main application class """
    
    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()

        # Variables that will hold sprite lists 
        self.player1_list = None 
        self.player2_list = None
        self.laser1_list = None 
        self.laser2_list = None 
        self.wall_list = None 

        # Set up the player info 
        self.player1_sprite = None 
        self.prayer2_sprite = None 

        self.p1_health = None 
        self.p2_health = None 

        # Background variable 
        self.background = None 

        # Don't show the mouse cursor 
        self.window.set_mouse_visible(False) 

    def setup(self):
        """ Set up the game and initialize variables """

        # Load the background image 
        self.background = arcade.load_texture(f"{DIR}\\space_free.png")

        # Sprite Lists
        self.player1_list = arcade.SpriteList()
        self.player2_list = arcade.SpriteList()
        self.laser1_list = arcade.SpriteList()
        self.laser2_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        # Set up the players 
        self.p1_health = P1_MAX_HEALTH
        self.p2_health = P2_MAX_HEALTH

        # Sprite images
        self.player1_sprite = arcade.Sprite(f"{DIR}\\blue_ship.png", SPRITE_SCALING_PLAYERS)
        self.player1_sprite.center_x = SCREEN_WIDTH / 2 
        self.player1_sprite.center_y = 35
        self.player1_list.append(self.player1_sprite)

        self.player2_sprite = arcade.Sprite(f"{DIR}\\red_ship.png", SPRITE_SCALING_PLAYERS, flipped_vertically=True)
        self.player2_sprite.center_x = SCREEN_WIDTH / 2 
        self.player2_sprite.center_y = SCREEN_HEIGHT - 35
        self.player2_list.append(self.player2_sprite)

        # Set the background color 
        arcade.set_background_color(arcade.color.BLACK)

        # Create the physics engine
        self.physics_engine1 = arcade.PhysicsEngineSimple(self.player1_sprite, self.wall_list)
        self.physics_engine2 = arcade.PhysicsEngineSimple(self.player2_sprite, self.wall_list)

    def on_draw(self):
        """ Render the screen """

        # This command has to happen before we start drawing to the screen
        arcade.start_render()

        # Draw the background image 
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background) 

        # Draw all the sprites 
        self.player1_list.draw()
        self.player2_list.draw()
        self.laser1_list.draw()
        self.laser2_list.draw()

        # Draw the player health
        p1_health_text = f"P1 Lives: {self.p1_health}"
        arcade.draw_text(p1_health_text, 10, 10, arcade.color.WHITE, 18)

        p2_health_text = f"P2 Lives: {self.p2_health}"
        arcade.draw_text(p2_health_text, 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player1_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player1_sprite.change_x = PLAYER_SPEED

        elif key == arcade.key.RSHIFT:
            laser = arcade.Sprite(f"{DIR}\\blue_laser.png", SPRITE_SCALING_LASERS)
            laser.center_x = self.player1_sprite.center_x
            laser.center_y = self.player1_sprite.center_y + 50
            laser.change_y = LASER_SPEED
            self.laser1_list.append(laser)
            
        if key == arcade.key.A:
            self.player2_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.E:
            self.player2_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.LSHIFT:
            laser = arcade.Sprite(f"{DIR}\\red_laser.png", SPRITE_SCALING_LASERS)
            laser.center_x = self.player2_sprite.center_x 
            laser.center_y = self.player2_sprite.center_y - 50
            laser.change_y = -LASER_SPEED
            self.laser2_list.append(laser)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player1_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player1_sprite.change_x = 0

        if key == arcade.key.A:
            self.player2_sprite.change_x = 0
        elif key == arcade.key.E:
            self.player2_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        self.physics_engine1.update()
        self.physics_engine2.update()

        # Call update on all sprites 
        self.laser1_list.update()
        self.laser2_list.update()

        # Loop through each player 1 laser 

        for laser in self.laser1_list:
            # Check to see if it hit player... 
            hit_list = arcade.check_for_collision_with_list(laser, self.player2_list)

            #...if it did, destroy the laser...
            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()

            #...and subtract one from player health
            for player in hit_list:
                self.p2_health -= 1
                if self.p2_health <= 0:
                    winner = "BLUE PLAYER"
                    player.remove_from_sprite_lists()
                    view = GameOverView()
                    view.winner = winner
                    self.window.show_view(view)

            # If the laser flies off screen, destroy it
            if laser.bottom > SCREEN_HEIGHT or laser.bottom < 0:
                laser.remove_from_sprite_lists()

        # Loop through each player 2 laser
        for laser in self.laser2_list:
            hit_list = arcade.check_for_collision_with_list(laser, self.player1_list)

            if len(hit_list) > 0:
                laser.remove_from_sprite_lists()

            for player in hit_list:
                self.p1_health -= 1
                if self.p1_health <= 0:
                    winner = "RED PLAYER"
                    player.remove_from_sprite_lists()
                    view = GameOverView()
                    view.winner = winner 
                    self.window.show_view(view)

            if laser.bottom > SCREEN_HEIGHT or laser.bottom < 0:
                laser.remove_from_sprite_lists()

        # Keep players in-bounds

        if self.player1_sprite.center_x >= SCREEN_WIDTH - 50:
            self.player1_sprite.center_x = SCREEN_WIDTH - 50
        if self.player1_sprite.center_x <= 50:
            self.player1_sprite.center_x = 50

        if self.player2_sprite.center_x >= SCREEN_WIDTH - 50:
            self.player2_sprite.center_x = SCREEN_WIDTH - 50
        if self.player2_sprite.center_x <= 50:
            self.player2_sprite.center_x = 50

        
            

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = TitleView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()