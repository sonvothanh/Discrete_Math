from manim import *

class RotationAnimation(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES, zoom=0.8)

        # --- Create Axes ---
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )

        # --- Create a cube ---
        cube = Cube(side_length=2, fill_opacity=0.1, stroke_color=BLUE_D, stroke_width=2)

        # --- Theta Tracker and Title ---
        theta_tracker = ValueTracker(0)
        theta_value_text = DecimalNumber(
            theta_tracker.get_value(),
            num_decimal_places=2,
            show_ellipsis=False,
            group_with_commas=False,
            unit="^{\\circ}"
        )

        title_static_part = MathTex(r"\text{Rotation angle } \theta = ")
        title_static_part.to_edge(UP)
        title = VGroup(title_static_part, theta_value_text)
        
        def update_title(group):
            group[1].next_to(group[0],RIGHT)
            group[1].set_value(theta_tracker.get_value())
            self.add_fixed_in_frame_mobjects(group)
        
        title.add_updater(update_title)
        self.add(title,axes, cube)
        self.play(
            Rotate(cube, angle=90 * DEGREES, axis=OUT, about_point=ORIGIN, run_time=4),
            theta_tracker.animate.set_value(90),
            rate_func=linear
        )
        self.wait()
