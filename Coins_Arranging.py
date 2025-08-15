# --- Full Animation Script: Coin.py (with 2.5D Elliptical Coins) ---

from manim import *
import numpy as np

# (Paste the improved 2.5D Coin class from above right here)
class Coin(VGroup):
    """
    A customizable, 2.5D-looking coin Mobject with a perspective angle.
    It's a VGroup that uses two ellipses to simulate a coin viewed
    from an angle, giving it a sense of thickness and perspective.
    """
    def __init__(
        self,
        radius: float = 0.4,
        thickness: float = 0.1,
        perspective_angle: float = 70,
        color: ManimColor = GOLD,
        edge_darkness: float = 0.6,
        **kwargs
    ):
        super().__init__(**kwargs)
        if not (0 <= perspective_angle <= 90):
            raise ValueError("perspective_angle must be between 0 and 90 degrees.")
        angle_rad = np.deg2rad(perspective_angle)
        ellipse_width = 2 * radius
        ellipse_height = 2 * radius * np.sin(angle_rad)
        edge_color = color.darker(edge_darkness)
        self.edge = Ellipse(width=ellipse_width, height=ellipse_height, color=edge_color, fill_opacity=1, stroke_width=0)
        self.face = Ellipse(width=ellipse_width, height=ellipse_height, color=color, fill_opacity=1, stroke_width=2.5, stroke_color=edge_color)
        self.add(self.edge, self.face)
        self.face.move_to(self.edge.get_center() + UP * thickness)


class ArrangeCoinsScene(Scene):
    def construct(self):
        # --- CONFIGURATION ---
        N_COINS = 18+7+8+9+7
        COIN_RADIUS = 0.35
        COIN_THICKNESS = 0.08
        PERSPECTIVE_ANGLE = 30 # The new angle for our 2.5D view!
        START_POS = UP * 2.5

        # --- CALCULATE SPACING based on ellipse dimensions ---
        coin_width = 2 * COIN_RADIUS
        coin_height = 2 * COIN_RADIUS * np.sin(np.deg2rad(PERSPECTIVE_ANGLE))

        # Spacing is now based on the coin's apparent width and height
        x_spacing = coin_width * 1.15
        y_spacing = coin_height * 1.25

        # --- SETUP ---
        title = Tex("Arranging Coins", font_size=48).to_edge(UP)
        self.play(Write(title))

        tracker_text = VGroup(
            Tex("Total Coins:", font_size=36),
            Integer(N_COINS, font_size=42).set_color(YELLOW),
            Tex("Full Rows:", font_size=36),
            Integer(0, font_size=42).set_color(GREEN)
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN)

        self.play(FadeIn(tracker_text))
        self.wait(0.5)

        # --- ANIMATION LOGIC ---
        coins_remaining = N_COINS
        rows_built = 0
        current_row_num = 1

        all_placed_coins = VGroup()

        while coins_remaining >= current_row_num:
            row_coins = VGroup()
            for i in range(current_row_num):
                coin = Coin(
                    radius=COIN_RADIUS,
                    thickness=COIN_THICKNESS,
                    perspective_angle=PERSPECTIVE_ANGLE
                )

                # Calculate position using our new spacing values
                y_pos = START_POS[1] - (rows_built * y_spacing)
                x_pos = (i - (current_row_num - 1) / 2) * x_spacing

                coin.move_to([x_pos, y_pos, 0])
                row_coins.add(coin)

            self.play(Create(row_coins, lag_ratio=0.2))
            all_placed_coins.add(row_coins)

            # Update state and tracker
            coins_remaining -= current_row_num
            rows_built += 1

            self.play(
                tracker_text[1].animate.set_value(coins_remaining),
                tracker_text[3].animate.set_value(rows_built)
            )
            self.wait(0.5)

            current_row_num += 1

        # --- FINAL STEP: Show remaining coins ---
        if coins_remaining > 0:
            remaining_text = Tex(f"Cannot form the next row of {current_row_num}", font_size=32).next_to(all_placed_coins, DOWN, buff=0.17)
            self.play(Write(remaining_text))

            leftover_coins = VGroup()
            for i in range(coins_remaining):
                coin = Coin(
                    radius=COIN_RADIUS,
                    thickness=COIN_THICKNESS,
                    perspective_angle=PERSPECTIVE_ANGLE,
                    color=RED_C
                )
                leftover_coins.add(coin)

            self.play(FadeIn(leftover_coins.arrange(RIGHT, buff=0.1).next_to(remaining_text, DOWN), shift=UP))

        self.wait(2)

        # Final result box
        final_box = SurroundingRectangle(tracker_text[2:], corner_radius=0.1, buff=0.2, color=GREEN)
        final_text = Tex(f"Final Answer: {rows_built} full rows", font_size=40).next_to(leftover_coins, DOWN, buff=0.13).set_color(GREEN)
        self.play(Create(final_box), Write(final_text))
        self.wait(3)
