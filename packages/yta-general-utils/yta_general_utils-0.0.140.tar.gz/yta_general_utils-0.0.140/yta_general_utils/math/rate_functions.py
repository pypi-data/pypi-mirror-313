"""
This is an adaption of the rate functions found in manim
library for the moviepy library. I have to use lambda t
functions with the current frame time to be able to resize
or reposition a video, so I have adapted the manim rate
functions to be able to return a factor that, with specific
moviepy functions, will make a change with the factor that
has been calculated with the corresponding rate function.

You can see 'manim/utils/rate_functions.py'.

This is the way I have found to make it work and to be able
to build smoother animations. As manim docummentation says,
the rate functions have been inspired by the ones listed in
this web page: https://easings.net/
"""
from yta_general_utils.math import Math
from math import pow, sqrt
from typing import Callable, Iterable

import numpy as np


class RateFunction:
    """
    Class to simplify and encapsulate the functionality related
    to normalized bezier and rate functions.

    For any case the 'n' value must be a normalized value 
    between 0 and 1 to work as expected. You can apply the 
    result to a variation you want to make in some of your
    functions.

    If you want to make a linear zoom of a 20%, you will use
    a progressive zoom by applying the formula '1 + 0.2 * 
    linear(t)' (where t is the normalized time moment of the
    zoom animation).

    This is based on the manim library and this web page 
    https://easings.net/.
    """
    @staticmethod
    def linear(n: float) -> float:
        return n
    
    @staticmethod
    def slow_into(n: float) -> float:
        return np.sqrt(1 - (1 - n) * (1 - n))

    @staticmethod
    def smooth(n: float, inflection: float = 10.0) -> float:
        error = Math.sigmoid(-inflection / 2)

        return min(
            max((Math.sigmoid(inflection * (n - 0.5)) - error) / (1 - 2 * error), 0),
            1,
        )
    
    @staticmethod
    def smoothstep(n: float) -> float:
        """
        Implementation of the 1st order SmoothStep sigmoid function.
        The 1st derivative (speed) is zero at the endpoints.
        https://en.wikipedia.org/wiki/Smoothstep
        """
        return 0 if n <= 0 else 3 * n**2 - 2 * n**3 if n < 1 else 1
    
    @staticmethod
    def smootherstep(n: float) -> float:
        """
        Implementation of the 2nd order SmoothStep sigmoid function.
        The 1st and 2nd derivatives (speed and acceleration) are zero at the endpoints.
        https://en.wikipedia.org/wiki/Smoothstep
        """
        return 0 if n <= 0 else 6 * n**5 - 15 * n**4 + 10 * n**3 if n < 1 else 1
    
    @staticmethod
    def smoothererstep(n: float) -> float:
        """
        Implementation of the 3rd order SmoothStep sigmoid function.
        The 1st, 2nd and 3rd derivatives (speed, acceleration and jerk) are zero at the endpoints.
        https://en.wikipedia.org/wiki/Smoothstep
        """
        alpha = 0
        if 0 < n < 1:
            alpha = 35 * n**4 - 84 * n**5 + 70 * n**6 - 20 * n**7
        elif n >= 1:
            alpha = 1
        return alpha
    
    @staticmethod
    def rush_into(n: float, inflection: float = 10.0) -> float:
        return 2 * RateFunction.smooth(n / 2.0, inflection)

    @staticmethod
    def rush_from(n: float, inflection: float = 10.0) -> float:
        return 2 * RateFunction.smooth(n / 2.0 + 0.5, inflection) - 1
    
    @staticmethod
    def double_smooth(n: float) -> float:
        if n < 0.5:
            return 0.5 * RateFunction.smooth(2 * n)
        else:
            return 0.5 * (1 + RateFunction.smooth(2 * n - 1))
        
    @staticmethod
    def there_and_back(n: float, inflection: float = 10.0) -> float:
        if n < 0.5:
            n = 2 * n
        else:
            n = 2 * (1 - n)

        return RateFunction.smooth(n, inflection)
    
    @staticmethod
    def there_and_back_with_pause(n: float, pause_ratio: float = 1.0 / 3) -> float:
        a = 1.0 / pause_ratio
        if n < 0.5 - pause_ratio / 2:
            return RateFunction.smooth(a * n)
        elif n < 0.5 + pause_ratio / 2:
            return 1
        else:
            return RateFunction.smooth(a - a * n)
        
    @staticmethod
    def running_start(n: float, pull_factor: float = -0.5) -> Iterable: # what is func return type?
        # TODO: This is being taken from manim, maybe copy (?)
        from manim.utils.bezier import bezier

        return bezier([0, 0, pull_factor, pull_factor, 1, 1, 1])(n)
    
    @staticmethod
    def wiggle(n: float, wiggles: float = 2) -> float:
        # TODO: Manim says 'not_quite_there' function is not working
        return RateFunction.there_and_back(n) * np.sin(wiggles * np.pi * n)
    
    @staticmethod
    def ease_in_cubic(n: float) -> float:
        return n * n * n
    
    @staticmethod
    def ease_out_cubic(n: float) -> float:
        return 1 - pow(1 - n, 3)
    
    @staticmethod
    def squish_rate_func(func: Callable[[float], float], a: float = 0.4, b: float = 0.6) -> Callable[[float], float]:
        def result(n: float):
            if a == b:
                return a

            if n < a:
                return func(0)
            elif n > b:
                return func(1)
            else:
                return func((n - a) / (b - a))

        return result
    
    @staticmethod
    def lingering(n: float) -> float:
        return RateFunction.squish_rate_func(lambda n: n, 0, 0.8)(n)
    
    @staticmethod
    def exponential_decay(n: float, half_life: float = 0.1) -> float:
        # The half-life should be rather small to minimize
        # the cut-off error at the end
        return 1 - np.exp(-n / half_life)

    @staticmethod
    def ease_in_sine(n: float) -> float:
        return 1 - np.cos((n * np.pi) / 2)
    
    @staticmethod
    def ease_out_sine(n: float) -> float:
        return np.sin((n * np.pi) / 2)
    
    @staticmethod
    def ease_in_out_sine(n: float) -> float:
        return -(np.cos(np.pi * n) - 1) / 2

    @staticmethod
    def ease_in_quad(n: float) -> float:
        return n * n
    
    @staticmethod
    def ease_out_quad(n: float) -> float:
        return 1 - (1 - n) * (1 - n)

    @staticmethod
    def ease_in_out_quad(n: float) -> float:
        return 2 * n * n if n < 0.5 else 1 - pow(-2 * n + 2, 2) / 2
    
    @staticmethod
    def ease_in_out_cubic(n: float) -> float:
        return 4 * n * n * n if n < 0.5 else 1 - pow(-2 * n + 2, 3) / 2

    @staticmethod
    def ease_in_quart(n: float) -> float:
        return n * n * n * n
    
    @staticmethod
    def ease_out_quart(n: float) -> float:
        return 1 - pow(1 - n, 4)

    @staticmethod
    def ease_in_out_quart(n: float) -> float:
        return 8 * n * n * n * n if n < 0.5 else 1 - pow(-2 * n + 2, 4) / 2
    
    @staticmethod
    def ease_in_quint(n: float) -> float:
        return n * n * n * n * n

    @staticmethod
    def ease_out_quint(n: float) -> float:
        return 1 - pow(1 - n, 5)
    
    @staticmethod
    def ease_in_out_quint(n: float) -> float:
        return 16 * n * n * n * n * n if n < 0.5 else 1 - pow(-2 * n + 2, 5) / 2

    @staticmethod
    def ease_in_expo(n: float) -> float:
        return 0 if n == 0 else pow(2, 10 * n - 10)
    
    @staticmethod
    def ease_out_expo(n: float) -> float:
        return 1 if n == 1 else 1 - pow(2, -10 * n)
    
    @staticmethod
    def ease_in_out_expo(n: float) -> float:
        if n == 0:
            return 0
        elif n == 1:
            return 1
        elif n < 0.5:
            return pow(2, 20 * n - 10) / 2
        else:
            return (2 - pow(2, -20 * n + 10)) / 2
        
    @staticmethod
    def ease_in_circ(n: float) -> float:
        return 1 - sqrt(1 - pow(n, 2))
    
    @staticmethod
    def ease_out_circ(n: float) -> float:
        return sqrt(1 - pow(n - 1, 2))
    
    @staticmethod
    def ease_in_out_circ(n: float) -> float:
        return (
            (1 - sqrt(1 - pow(2 * n, 2))) / 2
            if n < 0.5
            else (sqrt(1 - pow(-2 * n + 2, 2)) + 1) / 2
        )

    @staticmethod
    def ease_in_back(n: float) -> float:
        c1 = 1.70158
        c3 = c1 + 1

        return c3 * n * n * n - c1 * n * n

    @staticmethod
    def ease_out_back(n: float) -> float:
        c1 = 1.70158
        c3 = c1 + 1

        return 1 + c3 * pow(n - 1, 3) + c1 * pow(n - 1, 2)
    
    @staticmethod
    def ease_in_out_back(n: float) -> float:
        c1 = 1.70158
        c2 = c1 * 1.525

        return (
            (pow(2 * n, 2) * ((c2 + 1) * 2 * n - c2)) / 2
            if n < 0.5
            else (pow(2 * n - 2, 2) * ((c2 + 1) * (n * 2 - 2) + c2) + 2) / 2
        )
    
    @staticmethod
    def ease_in_elastic(n: float) -> float:
        c4 = (2 * np.pi) / 3
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return -pow(2, 10 * n - 10) * np.sin((n * 10 - 10.75) * c4)
        
    @staticmethod
    def ease_out_elastic(n: float) -> float:
        c4 = (2 * np.pi) / 3
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            return pow(2, -10 * n) * np.sin((n * 10 - 0.75) * c4) + 1

    @staticmethod
    def ease_in_out_elastic(n: float) -> float:
        c5 = (2 * np.pi) / 4.5
        if n == 0:
            return 0
        elif n == 1:
            return 1
        elif n < 0.5:
            return -(pow(2, 20 * n - 10) * np.sin((20 * n - 11.125) * c5)) / 2
        else:
            return (pow(2, -20 * n + 10) * np.sin((20 * n - 11.125) * c5)) / 2 + 1

    @staticmethod
    def ease_in_bounce(n: float) -> float:
        return 1 - RateFunction.ease_out_bounce(1 - n)
    
    @staticmethod
    def ease_out_bounce(n: float) -> float:
        n1 = 7.5625
        d1 = 2.75

        if n < 1 / d1:
            return n1 * n * n
        elif n < 2 / d1:
            return n1 * (n - 1.5 / d1) * (n - 1.5 / d1) + 0.75
        elif n < 2.5 / d1:
            return n1 * (n - 2.25 / d1) * (n - 2.25 / d1) + 0.9375
        else:
            return n1 * (n - 2.625 / d1) * (n - 2.625 / d1) + 0.984375
        
    @staticmethod
    def ease_in_out_bounce(n: float) -> float:
        if n < 0.5:
            return (1 - RateFunction.ease_out_bounce(1 - 2 * n)) / 2
        else:
            return (1 + RateFunction.ease_out_bounce(2 * n - 1)) / 2

# TODO: I can create my own curves by setting nodes with
# different values (as speed curves in a famous video
# editor) to make my own animations