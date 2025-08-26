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
        title.arrange(RIGHT)
        title.to_edge(UP)

        # Make the angle tracker follow the theta value
        theta_value_text.add_updater(lambda m: m.set_value(theta_tracker.get_value()))

        self.add(axes, cube)
        self.add_fixed_in_frame_mobjects(title_static_part, theta_value_text) # .renderer.camera.
        # self.add(title_static_part, theta_value_text)

        self.wait()

        self.play(
            Rotate(cube, angle=90 * DEGREES, axis=OUT, about_point=ORIGIN, run_time=4),
            theta_tracker.animate.set_value(90),
            rate_func=linear
        )
        self.wait()
