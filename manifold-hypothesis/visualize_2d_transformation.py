from manim import *
import colors
import numpy as np
import math
from modules import Grid

config.background_color = colors.WHITE


class VisualizeTransformation(Scene):
    def construct(self):
        self.linear_transfom()
        self.wait()

    def linear_transfom(self):
        grid = NumberPlane(
            y_length=8 * 3,
            y_range=[-8, 8, 0.5],
            x_length=14 * 3,
            x_range=[-14, 14, 0.5],
            background_line_style={
                "stroke_width": 1,
                "stroke_opacity": 0.75,
            },
            faded_line_ratio=1,
        ).set_stroke(color=colors.BLACK)
        fixed_grid = grid.copy().set_stroke(color=colors.DESERT)
        fixed_grid.axes.set_stroke(width=4, color=colors.BLACK)
        grid.axes.set_stroke(width=0)

        dot = Dot(fixed_grid.c2p(1, -1, 0)).set_opacity(0)

        def get_vector():
            vector = (
                Arrow(ORIGIN, dot.get_center(), buff=0)
                .set_stroke(width=4, color=colors.ORANGE)
                .set_fill(color=colors.ORANGE, opacity=1)
            )
            return vector

        vector = always_redraw(get_vector)

        self.play(Write(grid))
        self.add(fixed_grid)
        self.wait()

        self.play(Write(vector))

        A = np.array([[0.25, 0.75], [0.5, 0.25]])

        self.play(
            grid.animate.apply_matrix(A),
            dot.animate.move_to([*(A @ dot.get_center()[0:2]), 0]),
        )


class TanhGraph(Scene):
    def construct(self):
        self.build_tanh_graph()
        self.wait()
        self.show_squishing()
        self.wait()

    def build_tanh_graph(self):
        # build the tanh graph
        ax = Axes(
            x_range=[-6, 6, 2],
            y_range=[-1.5, 1.5, 0.5],
            tips=False,
            y_axis_config={
                "unit_size": 0.5,
                "numbers_to_include": np.arange(-1.0, 1.5, 0.5),
                "font_size": 20,
            },
            x_axis_config={
                "unit_size": 0.5,
                "numbers_to_include": np.arange(-4, 6, 2),
                "font_size": 20,
            },
        ).set_stroke(color=colors.BLACK)

        tanh_text = (
            MathTex(r"\tanh(x)", color=colors.BLACK)
            .set_stroke(width=1)
            .move_to(ax.get_corner(UL))
            .shift(DR + RIGHT * 0.5)
        )

        ax.get_axis(0).numbers.set_color(colors.BLACK).set_stroke(width=1)
        ax.get_axis(1).numbers.set_color(colors.BLACK).set_stroke(width=1)

        self.ax_border = Rectangle(width=ax.x_length, height=ax.y_length).set_stroke(
            color=colors.BLACK, width=4
        )
        graph = ax.plot(math.tanh, color=colors.PURPLE)
        labels = ax.get_axis_labels(x_label=Tex("x"), y_label=Tex("y"))

        t = ValueTracker(0)
        initial_point = [ax.c2p(t.get_value(), math.tanh(t.get_value()))]
        dot = Dot(point=initial_point, radius=0.04, color=colors.BLACK)

        dot.add_updater(
            lambda x: x.move_to(ax.c2p(t.get_value(), math.tanh(t.get_value())))
        )

        def get_dot_text():
            return Text(
                f"{math.tanh(t.get_value()):.2f}",
                color=colors.BLACK,
                font="Fira Code",
                weight=BOLD,
                font_size=15,
            )

        dot_text = always_redraw(get_dot_text)
        dot_text.add_updater(lambda x: x.next_to(dot, UR))

        full_graph = VGroup(ax, labels, graph, dot, tanh_text)

        self.play(Write(full_graph), Write(self.ax_border))
        self.play(Write(dot_text))
        full_graph.add(dot_text)
        self.play(t.animate.set_value(3), run_time=3)
        self.wait()
        self.play(t.animate.set_value(-3), run_time=3)
        self.wait()
        dot_text.clear_updaters()
        self.play(Unwrite(full_graph), Unwrite(dot_text))

    def show_squishing(self):

        fixed_grid = NumberPlane(
            y_length=self.ax_border.height,
            x_length=self.ax_border.width,
            y_range=[-2, 2, 0.5],
            x_range=[-3.5, 3.5, 0.5],
            background_line_style={
                "stroke_width": 1,
                "stroke_opacity": 0.75,
            },
            y_axis_config={
                "unit_size": 0.5,
                "include_numbers": True,
                "numbers_to_include": [-1, 1],
                "font_size": 20,
            },
            x_axis_config={
                "unit_size": 0.5,
                "include_numbers": True,
                "numbers_to_include": [-1, 1],
                "font_size": 20,
            },
            faded_line_ratio=1,
        ).set_stroke(color=colors.GRAY, width=1)

        fixed_grid.axes.set_color(colors.BLACK).set_stroke(width=2)

        grid = Grid(fixed_grid, [-3.5, 3.5, 0.5], [-3.5, 3.5, 0.5], lattice_radius=0.04)

        grid.set_color(colors.BLACK)
        grid.grid_lines.set_stroke(width=0.5)

        A = np.array(
            [
                [1, -1],
                [0, 1],
            ]
        )

        self.play(Write(fixed_grid))
        self.wait()
        self.play(Write(VGroup(grid.grid_lines, grid.submobjects)))
        self.wait()

        # applying the linear transformation to the grid
        grid.array = grid.array @ A.T
        new_grid = [
            dot.animate.move_to(fixed_grid.c2p(*pos))
            for dot, pos in zip(grid.submobjects, grid.array)
        ]
        self.play(*new_grid)
        self.wait()

        # applying the tanh function to the grid
        grid.array = np.tanh(grid.array)
        new_grid = [
            dot.animate.move_to(fixed_grid.c2p(*pos))
            for dot, pos in zip(grid.submobjects, grid.array)
        ]
        self.play(*new_grid)
        self.wait()

        grid.submobjects.clear_updaters()
        self.play(Unwrite(grid.submobjects), Unwrite(grid.grid_lines))
        self.play(Unwrite(fixed_grid))
        self.play(Unwrite(self.ax_border))


class ReLUGraph(Scene):
    def construct(self):
        self.build_relu_graph()
        self.wait()

    def build_relu_graph(self):
        # build the relu graph
        ax = Axes(
            x_range=[-6, 6, 2],
            y_range=[-6, 6, 2],
            tips=False,
            x_axis_config={
                "unit_size": 0.5,
                "numbers_to_include": np.arange(-4, 6, 2),
                "font_size": 20,
            },
            y_axis_config={
                "unit_size": 0.5,
                "numbers_to_include": np.arange(-4, 6, 2),
                "font_size": 20,
            },
        ).set_stroke(color=colors.BLACK)

        relu_text = (
            MathTex(r"\text{ReLU}(x)", color=colors.BLACK)
            .set_stroke(width=1)
            .move_to(ax.get_corner(UL))
            .shift(DR + RIGHT * 0.5)
        )

        ax.get_axis(0).numbers.set_color(colors.BLACK).set_stroke(width=1)
        ax.get_axis(1).numbers.set_color(colors.BLACK).set_stroke(width=1)

        self.ax_border = Rectangle(width=ax.x_length, height=ax.y_length).set_stroke(
            color=colors.BLACK, width=4
        )
        graph = ax.plot(lambda x: max(0, x), color=colors.PURPLE, use_smoothing=False)
        labels = ax.get_axis_labels(x_label=Tex("x"), y_label=Tex("y"))

        t = ValueTracker(0)
        initial_point = [ax.c2p(t.get_value(), max(0, t.get_value()))]
        dot = Dot(point=initial_point, radius=0.04, color=colors.BLACK)
        dot.add_updater(
            lambda x: x.move_to(ax.c2p(t.get_value(), max(0, t.get_value())))
        )

        def get_dot_text():
            return Text(
                f"{max(0, t.get_value()):.2f}",
                color=colors.BLACK,
                font="Fira Code",
                weight=BOLD,
                font_size=15,
            )

        dot_text = always_redraw(get_dot_text)
        dot_text.add_updater(lambda x: x.next_to(dot, UR))

        full_graph = VGroup(ax, labels, graph, dot, relu_text)

        self.play(Write(full_graph), Write(self.ax_border))
        self.play(Write(dot_text))
        full_graph.add(dot_text)
        self.play(t.animate.set_value(3), run_time=3)
        self.wait()
        self.play(t.animate.set_value(-3), run_time=3)
        self.wait()
        dot_text.clear_updaters()
        self.play(Unwrite(full_graph), Unwrite(dot_text))
