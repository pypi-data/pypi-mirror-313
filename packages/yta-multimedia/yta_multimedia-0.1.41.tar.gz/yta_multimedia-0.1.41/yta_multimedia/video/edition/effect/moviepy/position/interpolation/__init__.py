"""
    Thanks to https://omaraflak.medium.com/b%C3%A9zier-interpolation-8033e9a262c2
    for interpolation explanation and code.

    Thanks to https://github.com/vmichals/python-algos/blob/master/catmull_rom_spline.py
    for the catmull-rom-spline interpolation code.
"""
from yta_general_utils.programming.parameter_validator import NumberValidator, PythonValidator
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from yta_multimedia.video.position import Position
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.math import Math
from scipy import interpolate
from typing import Callable, Union

import numpy as np
import matplotlib.pyplot as plt


# Here below are some functions to obtain the graphic
# between points
class InterpolationFormula:
    """
    Class to encapsulate interpolation formulas.
    """
    @staticmethod
    def catmull_rom_spline(spline_x: float, p0, p1, p2, p3):
        """
        Function to evaluate one spline of the Catmull-Rom
        between two points by using 4 control points.

        It returns the x,y point in the spline.

        Computes interpolated y-coord for given x-coord using
        Catmull-Rom. The 'spline_x' is the current position in
        the graphic interpolation between the points p0 and p1
        represented by a value between 0 and 1.

        Computes an interpolated y-coordinate for the given
        x-coordinate between the support points v1 and v2. The
        neighboring support points v0 and v3 are used by
        Catmull-Rom to ensure a smooth transition between the
        spline segments.
        """
        c1 = 1. * p1
        c2 = -.5 * p0 + .5 * p2
        c3 = 1. * p0 + -2.5 * p1 + 2. * p2 -.5 * p3
        c4 = -.5 * p0 + 1.5 * p1 + -1.5 * p2 + .5 * p3

        # TODO: We can apply a RateFunction here
        # in 'spline_x' to set the speed as
        # non-linear
        return (((c4 * spline_x + c3) * spline_x + c2) * spline_x + c1)
    
    @staticmethod
    def linear(spline_x: float, p0, p1):
        """
        Function to evaluate one spline of a linear function
        between two points.

        It returns the x,y point in the spline.

        Computes interpolated y-coord for given x-coord using
        linear function.
        """
        # TODO: We can apply a RateFunction here
        # in 'spline_x' to set the speed as
        # non-linear
        x = p0[0] + (p1[0] - p0[0]) * spline_x
        y = p0[1] + (p1[1] - p0[1]) * spline_x

        return (x, y)

class GraphicRateFunction:
    """
    Class to simplify the way we work with rate functions
    being able to personalize a graphic that will allow us
    using it as a rate function to create our own effects.

    We receive a list of points that are coordinates of the
    graph we want to create as a rate function, and the 
    code will analyze it and obtain the function that allows
    us to determine the value of any 't' value between 0.0
    and 1.0.
    
    The 't' value provided is representing the distance in the
    graphic curve that has been generated with the points
    provided and the interpolation method applied. This curve
    is representing some effect, animation or transition
    duration, from 0 to 1. So, if the provided 't' is 0.20,
    that is representing the moment in which the 20% of the
    animation has been played, and will return the 'y' value
    that must be used in the animation for that specific 
    moment.

    We have a graphic representation of a function in which we
    use the 'x' and 'y' axis to represent it. There is another
    value that we call 't' and it is one point within the 
    graphic that has been generated with the provided points
    and the 'interpolation_formula'. This 't' is representing
    an instant during the execution of an animation or
    transition.
    """
    coordinates: list[Coordinate]
    """
    The list of coordinates to represent the graphic we
    want to represent.
    """
    interpolation_formula: Callable
    """
    The method to calculate the interpolation between each
    pair of points.

    TODO: By now it is the same for the whole graph but it
    could change in a near future and be specific for each
    pair of points. We should create an InterpolationStep
    or similar to include 2 coordinates and 1 interpolation
    formula, and receive a list of instances of that class
    as a parameter to be able to customize each type of
    interpolation.
    """

    def __init__(self, points: list[Coordinate, Position, tuple], interpolation_formula: Callable):
        if not PythonValidator.is_list(points) or len(points) < 4 or any(not PythonValidator.is_instance(point, [Coordinate, Position, tuple]) for point in points):
            raise Exception(f'The "points" parameter must be a list of Coordinate, Position with a minimum of 4 elements.')
    
        if not PythonValidator.is_class_staticmethod(InterpolationFormula, interpolation_formula):
            raise Exception('The provided "interpolation_formula" is not a valid InterpolationFormula class method.')

        # TODO: Maybe if less than 4 elements: add 2 in between those 2
        # TODO: Should I allow this below (?) If I'm trying to obtain a
        # path I think yes... I will be using a 't' that is actually the
        # distance in the graph once it's been built, so I don't care if
        # I am going back or not, because it is like if just have two 
        # points in that moment and we want to know the value in one 
        # specific point of the graph between those 2 points, so I think
        # I should accept going towards or backwards
        # if not all(points[i].x < points[i + 1].x for i in range(len(points) - 1)):
        #     raise Exception('Points must be consecutive, so the "x" value of each point must be greater than the previous one. Please, check the provided "points" parameter.')

        # Turn all points to coordinates, normalize them and
        # obtain the normalized x,y in the format we need
        coords = []
        for point in points:
            coord = point
            if PythonValidator.is_instance(point, Position):
                coord = point.as_video_position().coordinate
            elif PythonValidator.is_tuple(point):
                if len(point) != 2:
                    # TODO: Maybe apply the normalization limits as limits
                    # here for each position tuple element
                    raise Exception('Provided "position" is a tuple but does not have 2 values.')
                point = Coordinate(point[0], point[1])

            coord = coord.normalize()
            coords.append(coord)

        self.coordinates = coords
        self.interpolation_formula = interpolation_formula

    def get_coord(self, t: float):
        """
        Evaluate the function for the provided 'x' value and
        return the graphic coordinate corresponding to that
        't' value, that must be a normalized value (between
        0 and 1, both inclusive) that represents the distance
        in the generated graphic.

        A graphic with 5 coordinates will generate 4 splines
        of the same length. The start of each of those splines
        will be [t = 0, t = 0.25, t = 0.5, t = 0.75]. So, if
        you provide t = 0.20, the returned coordinate will be
        contained in the first spline because it is below 0.25.
        """
        if not NumberValidator.is_number_between(t, 0.0, 1.0):
            raise Exception('The provided "t" parameter "{str(t)}" must be  between 0 and 1, both inclusive.')

        num_of_splines = len(self.coordinates) - 1
        spline_size = 1
        if num_of_splines > 1:
            spline_size = 1 / num_of_splines

        if t == 1.0:
            spline_index = num_of_splines - 1
        else:
            # Check which spline we need to use
            spline_index = int(t // spline_size)

        # If we receive 0.28 => 0.28 - 0.25 = 0.03 / spline_size
        # A distance of 0.03 in the global graph is lower than the
        # real distance in any splice
        # 0.28 = 0.28 % (1 * 0.25) / 0.25 = 0.03 / 0.25 = 0.12
        previous_spline_size = spline_index * spline_size

        if previous_spline_size:
            t = t % (spline_index * spline_size) / spline_size
        else:
            t = t / spline_size

        if PythonValidator.is_class_staticmethod(InterpolationFormula, self.interpolation_formula, InterpolationFormula.catmull_rom_spline.__name__):
            numpy_coords = Coordinate.to_numpy(self.coordinates)

            if spline_index == 0: # First spline
                # We need to estimate the first point
                p0 = numpy_coords[0] - (numpy_coords[1] - numpy_coords[0])
                p1 = numpy_coords[0]
                p2 = numpy_coords[1]
                p3 = numpy_coords[2]
            elif spline_index == (num_of_splines - 1): # Last spline
                p0 = numpy_coords[spline_index - 1]
                p1 = numpy_coords[spline_index]
                p2 = numpy_coords[spline_index + 1]
                # We need to estimate the last point
                p3 = numpy_coords[spline_index + 1] + (numpy_coords[spline_index + 1] - numpy_coords[spline_index])
            else:
                p0 = numpy_coords[spline_index - 1]
                p1 = numpy_coords[spline_index]
                p2 = numpy_coords[spline_index + 1]
                p3 = numpy_coords[spline_index + 2]

            coord = self.interpolation_formula(t, p0, p1, p2, p3)
        elif PythonValidator.is_class_staticmethod(InterpolationFormula, self.interpolation_formula, InterpolationFormula.linear.__name__):
            p0 = numpy_coords[spline_index]
            p1 = numpy_coords[spline_index + 1]

            coord = self.interpolation_formula(t, p0, p1)
        
        # We maybe want the 'y' value as we are representing
        # something in a graphic, but we get the whole coord
        # at this point
        coord = Coordinate(coord[0], coord[1], self.coordinates[0].is_normalized)

        return coord
    
    def get_y(self, t: float):
        """
        Evaluate the function for the provided 't' value and
        return the graphic coordinate 'y' value corresponding
        to that 't' value that represents the distance in the
        generated graphic.

        A graphic with 5 coordinates will generate 4 splines
        of the same length. The start of each of those splines
        will be [t = 0, t = 0.25, t = 0.5, t = 0.75]. So, if
        you provide t = 0.20, the returned coordinate will be
        contained in the first spline because it is below 0.25.
        """
        return self.get_coord(t)[1]

    def plot(self, do_denormalize_values: bool = False):
        """
        This method is just for testing and shows the graphic
        using the matplotlib library.

        If you are plotting a path movement along the screen,
        set the 'do_denormalize_values' as True to make the
        plot show the real movement the video will do through
        the scene. If you are plotting a graph used for any
        other type of effect, keep the value as False.
        """
        if do_denormalize_values:
            # I denormalize values to be able to watch the path
            # movement properly
            self.coordinates = [coordinate.denormalize() for coordinate in self.coordinates]

        graph = np.array([self.get_coord(t).as_tuple() for t in np.linspace(0, 1, len(self.coordinates) * 100)])
        points = np.array([coordinate.as_tuple() for coordinate in self.coordinates])

        plt.plot(graph[:, 0], graph[:, 1], label = 'Graphic representation', color = 'blue')
        plt.scatter(points[:, 0], points[:, 1], color = 'red', label = 'Control points')
        plt.legend()
        plt.title('Graphic representation')
        plt.xlabel('x')
        plt.ylabel('y')

        if do_denormalize_values:
            # I invert the axis to see the graph as the video
            # movement because denormalization if because of
            # this
            plt.gca().invert_yaxis()
            
        plt.grid(True)
        plt.show()

    # TODO: If we want to apply one GraphicRateFunction to some
    # of our moviepy animations, we will be working with a 't'
    # value representing the time of the video, that can easily
    # be greater than 1, so we need to normalize it with the
    # video duration and use that normalized value to provide it
    # to this 'get_y()' or 'get_coord()' method.






class InterpolationMethod(Enum):
    """
    Enum class to include the available interpolation
    methods and to predict an 'y' value according to
    each specific method.

    This Enum class is pretended to be used with the
    InterpolatedPair class.
    """
    LINEAR = 'linear'
    QUADRATIC = 'quadratic'
    """
    This interpolation method needs 3 coordinates and
    x cannot be repeated.
    """
    CUBIC = 'cubic'
    """
    This interpolation method needs 4 coordinates and
    x cannot be repeated.
    """
    # TODO: Explain this above better, please

    def get_y_from_d(self, coordinate_a, coordinate_b, d: float):
        """
        Obtain the 'y' value by providing a 'd' distance that
        is the distance from one coordinate to another measured
        in normalized value between 0.0 and 1.0, representing
        the amount of distance traveled in the interpolation.
        """
        return self.get_coord_from_d(coordinate_a, coordinate_b, d)[1]

    def get_y_from_x(self, coordinate_a, coordinate_b, x: float):
        """
        Obtain the interpolated 'y' value for the given 'x'
        value, based on this interpolation method and the
        also given 'coordinate_a' and 'coordinate_b' coords.

        The 'x' parameter must be a normalized value (between
        0.0 and 1.0), representing an 'x' value in between the
        two provided coordinates.
        """
        return self.get_coord_from_x(coordinate_a, coordinate_b, x)[1]
    
    def get_coord_from_d(self, coordinate_a, coordinate_b, d: float):
        """
        Obtain the coordinate value by providing a 'd' distance
        that is the distance from one coordinate to another
        measured in normalized value between 0.0 and 1.0,
        representing the amount of distance traveled in the
        interpolation.
        """
        # TODO: Turn 'd' into x
        if not NumberValidator.is_number_between(d, 0.0, 1.0):
            raise Exception(f'The provided "d" parameter "{str(d)}" must be a value between 0.0 and 1.0.')
        
        # Calculate the 'x' according to the provided distance
        # 'd' traveled through the interpolation
        x = coordinate_a[0] + d * (coordinate_b[0] - coordinate_a[0])

        return self.get_coord_from_x(coordinate_a, coordinate_b, x)

    def get_coord_from_x(self, coordinate_a, coordinate_b, x: float):
        """
        Obtain the interpolated 'y' value for the given 'x'
        value, based on this interpolation method and the
        also given 'coordinate_a' and 'coordinate_b' coords.

        The 'x' parameter must be a normalized value (between
        0.0 and 1.0), representing an 'x' value in between the
        two provided coordinates.
        """
        # TODO: Move this code to 'get_coord_from_x' and call
        # it from here to obtain the y

        if not PythonValidator.is_tuple(coordinate_a) or len(coordinate_a) != 2 or not PythonValidator.is_tuple(coordinate_b) or len(coordinate_b) != 2:
            raise Exception('The provided "coordinate_a" or "coordinate_b" parameter is not a tuple of (x, y) values.')
        
        # Coordinates must be in order to be able to calculate
        # the interpolation. Don't worry, the interpolation will
        # be the same and the 'y' will be ok
        coordinates_in_order = sorted([coordinate_a, coordinate_b], key = lambda coord: coord[0])
        xs = [coordinates_in_order[0][0], coordinates_in_order[1][0]]
        ys = [coordinates_in_order[0][1], coordinates_in_order[1][1]]

        if not NumberValidator.is_number_between(x, xs[0], xs[1]):
            raise Exception(f'The provided "x" parameter "{str(x)}" is out of bounds (limits are [{str(xs[0])}, {str(xs[1])}]).')

        # TODO: Complete with all the interpolation methods
        if self == InterpolationMethod.LINEAR:
            # This method needs only 2 coordinates
            xs = [coordinate_a[0], coordinate_b[0]]
            ys = [coordinate_a[1], coordinate_b[1]]
            y = interpolate.interp1d(xs, ys, kind = InterpolationMethod.LINEAR.value)(x)
        elif self == InterpolationMethod.QUADRATIC:
            xs = [coordinate_a[0], coordinate_b[0]]
            ys = [coordinate_a[1], coordinate_b[1]]
            # We estimate a point in between the other two points
            xs.append((xs[0] + xs[1]) / 2)
            # We apply some randomness to the y of that point (or
            # it will become linear if we don't)
            # The more the distance between the points it is, the
            # more this value can be.
            randomness_factor = 0.95
            ys.append((ys[0] + ys[1]) / 2 * randomness_factor)
            y = interpolate.interp1d(xs, ys, kind = InterpolationMethod.QUADRATIC.value)(x)
        elif self == InterpolationMethod.CUBIC:
            # This method needs at least 4 coordinates
            #y = interpolate.interp1d(xs, ys, kind = 'linear')(x)
            # There is an 'assume_sorted' param as False, so it is
            # ok like this
            # TODO: Estimate other coords
            x0 = coordinate_a[0] - (coordinate_b[0] - coordinate_a[0])
            y0 = coordinate_a[1] - (coordinate_b[1] - coordinate_a[1])
            x3 = coordinate_b[0] + (coordinate_b[0] - coordinate_a[0])
            y3 = coordinate_b[1] + (coordinate_b[1] - coordinate_a[1])
            xs = [x0, coordinate_a[0], coordinate_b[0], x3]
            # TODO: This value, if random, has to be calculated
            # once for the whole interpolation, not for each y
            # value calculation or it will generate weird graphic
            #randomness_factor = randrangefloat(0.9, 1.1, 0.01)
            d = abs(x - coordinate_a[0]) / abs(coordinate_b[0] - coordinate_a[0])
            randomness_factor = 0.9
            ys = [y0 * randomness_factor, coordinate_a[1], coordinate_b[1], y3 * randomness_factor]
            y = interpolate.interp1d(xs, ys, kind = InterpolationMethod.CUBIC.value)(x)
        else:
            raise Exception(f'The "{self.name}" interpolation method has not been implemented yet.')
        # TODO: Implement more methods
        
        x = float(x)
        y = float(y)

        # TODO: If I invert, do I need to do a rest or something (?)

        return (x, y)
    
class InterpolatedPair:
    """
    A pair of coordinates connected by the provided interpolation
    method.
    """
    coordinate_a: Coordinate
    coordinate_b: Coordinate
    interpolation_method: InterpolationMethod
    _max_x: float = None
    _min_x: float = None

    @property
    def max_x(self):
        if not self._max_x:
            self._max_x = max([self.coordinate_a.x, self.coordinate_b.x], key = lambda coord: coord)

        return self._max_x
    
    @property
    def min_x(self):
        if not self._min_x:
            self._min_x = min([self.coordinate_a.x, self.coordinate_b.x], key = lambda coord: coord)

        return self._min_x

    def __init__(self, coordinate_a: Union[Coordinate, Position], coordinate_b: Union[Coordinate, Position], interpolation_method: InterpolationMethod = InterpolationMethod.LINEAR):
        if not PythonValidator.is_instance(coordinate_a, [Coordinate, Position]) or not PythonValidator.is_instance(coordinate_b, [Coordinate, Position]):
            raise Exception(f'The provided "coordinate_a" or "coordinate_b" is not a valid Coordinate or Position.')
        
        interpolation_method = InterpolationMethod.to_enum(interpolation_method)

        # Turn input parameters to Coordinate instances
        if PythonValidator.is_instance(coordinate_a, Position):
            coordinate_a = coordinate_a.get_moviepy_center_tuple()
            coordinate_a = Coordinate(coordinate_a[0], coordinate_a[1])

        if PythonValidator.is_instance(coordinate_b, Position):
            coordinate_b = coordinate_b.get_moviepy_center_tuple()
            coordinate_b = Coordinate(coordinate_b[0], coordinate_b[1])

        # We store them as normalized coordinates
        self.coordinate_a = coordinate_a.normalize()
        self.coordinate_b = coordinate_b.normalize()
        self.interpolation_method = interpolation_method

    def get_coord_from_x(self, x: float):
        """
        Get the coordinate that is in the provided 'x' 
        position (that must be a value between the two
        coordinate x axis we have).
        """
        # TODO: Maybe handle 'is_normalized' parameter
        # here also
        if not NumberValidator.is_number_between(x, self.min_x, self.max_x):
            raise Exception(f'The provided "d" parameter "{str(x)}" must be a value between 0.0 and 1.0.')
        
        y = self._get_y_from_x(x)

        return (x, y)

    def get_coord_from_distance(self, d: float):
        """
        Get the coordinate from the given distance 'd' that
        is the distance we will use to obtain the point in
        that distance between the two coordinates.
        """
        if not NumberValidator.is_number_between(d, 0.0, 1.0):
            raise Exception(f'The provided "d" parameter "{str(d)}" must be a value between 0.0 and 1.0.')
        
        # Calculate the 'x' according to the provided distance
        # 'd' traveled through the interpolation
        x = self.coordinate_a.x + d * (self.coordinate_b.x - self.coordinate_a.x)
        y = self._get_y_from_x(x)

        return (x, y)

    def _get_y_from_d(self, d: float):
        """
        Obtain the 'y' value by providing a 'd' distance that is
        the distance from one coordinate to another measured in
        normalized value between 0.0 and 1.0, representing the
        amount of distance traveled in the interpolation.
        """
        if not NumberValidator.is_number_between(d, 0.0, 1.0):
            raise Exception(f'The provided "d" parameter "{str(d)}" must be a value between 0.0 and 1.0.')
        
        x = self.coordinate_a.x + d * (self.coordinate_b.x - self.coordinate_a.x)

        return self._get_y_from_x(x)

    def _get_y_from_x(self, x: float):
        """
        Obtain the 'y' value by providing a 'x' value that is the
        x in value and must be in between the two coordinates.
        """
        if not NumberValidator.is_number_between(x, self.min_x, self.max_x):
            raise Exception(f'The provided "x" parameter "{str(x)}" must be a value between 0.0 and 1.0.')
        
        # TODO: What about non-consecutive (?)
        y = self.interpolation_method.get_y_from_x(self.coordinate_a.as_tuple(), self.coordinate_b.as_tuple(), x)

        return y

class GraphicInterpolation:
    """
    A graphic to represent points interpolated and to
    be able to calculate 'y' positions in those
    interpolations.
    """
    pairs_of_points: list[InterpolatedPair] = None
    _max_x: float = None
    _min_x: float = None
    _coordinates = None

    @property
    def max_x(self):
        if not self._max_x:
            self._max_x = max(self.coordinates, key = lambda coord: coord.x).x

        return self._max_x

    @property
    def min_x(self):
        if not self._min_x:
            self._min_x = min(self.coordinates, key = lambda coord: coord.x).x

        return self._min_x

    @property
    def coordinates(self):
        if not self._coordinates:
            coordinates = [pair_of_points.coordinate_a for pair_of_points in self.pairs_of_points]
            coordinates.append(self.pairs_of_points[-1].coordinate_b)

            self._coordinates = coordinates

        return self._coordinates

    def __init__(self, pairs_of_points: list[InterpolatedPair]):
        if not PythonValidator.is_list(pairs_of_points):
            if not PythonValidator.is_instance(pairs_of_points, InterpolatedPair):
                raise Exception('The provided "pairs_of_points" parameter is not a list of InterpolatedPair nor a single InterpolatedPair.')
            else:
                pairs_of_points = [pairs_of_points]

        for i in range(len(pairs_of_points) - 1):
            if pairs_of_points[i].coordinate_b.x != pairs_of_points[i + 1].coordinate_a.x or pairs_of_points[i].coordinate_b.y != pairs_of_points[i + 1].coordinate_a.y:
                raise Exception('The points must be consecutive, so the coordinate B of one point must be the coordinate A of the next one.')

        self.pairs_of_points = pairs_of_points

    def get_coord_from_x(self, x: float, is_normalized: bool = False, do_denormalize: bool = True):
        """
        Obtain the coordinate corresponding to the provided
        'x' in the whole graphic interpolation. This means 
        that the value will be interpolated with the pair of
        points that contains the provided 'x' in between.

        Use the 'do_denormalize' parameter to receive the
        coordinate denormalized or not.
        """
        # We are working with normalized coordinates, so if
        # the provided 'x' is not normalized, we need to do
        # it to be able to calculate
        if not is_normalized:
            # TODO: Really? Do we need the 'is_normalized' (?)
            x = Math.normalize(x, -10000, 10000)

        if not NumberValidator.is_number_between(x, self.min_x, self.max_x):
            raise Exception(f'The provided "x" parameter "{str(x)}" must be between {str(self.min_x)} and {str(self.max_x)}, both inclusive.')
        
        # We obtain the pair of points the 'x' belongs to
        # (it is in between of those 2 points)
        pair_of_points = next(pair_of_points for pair_of_points in self.pairs_of_points if pair_of_points.min_x <= x <= pair_of_points.max_x)

        coordinate = pair_of_points.get_coord_from_x(x)

        if do_denormalize:
            coordinate = Coordinate.denormalize_tuple((coordinate[0], coordinate[1]))

        return coordinate

    def get_coord_from_d(self, d: float, do_denormalize: bool = True):
        """
        Obtain the coordinate corresponding to the provided 
        distance 'd' in the whole graphic interpolation. This
        means that, if 5 pairs of points and 'd' is 0.3, it
        will return a coordinate located within the
        interpolation between the second pair of points.

        Consider 0.0 the start of the interpolation and 1.0 the
        end, and as we have 5 pair of points, the intervals 
        will be from [0, 0.2], [0.2, 0.4], [0.4, 0.6], 
        [0.6, 0.8], [0.8, 1.0]. As you can see, if 'd' is 0.3,
        the interval will be the second one.

        Use the 'do_denormalize' parameter to receive the
        coordinate denormalized or not.
        """
        if not NumberValidator.is_number_between(d, 0.0, 1.0):
            raise Exception(f'The provided "d" parameter "{str(d)}" must be between 0.0 and 1.0, both inclusive.')

        # 'd' is the distance within the whole graphic
        num_of_splines = len(self.pairs_of_points)
        spline_size = 1
        if num_of_splines > 1:
            spline_size = 1 / num_of_splines

        if d == 1.0:
            spline_index = num_of_splines - 1
        else:
            # Check which spline we need to use
            spline_index = int(d // spline_size)

        # If we receive 0.28 => 0.28 - 0.25 = 0.03 / spline_size
        # A distance of 0.03 in the global graph is lower than the
        # real distance in any splice
        # 0.28 = 0.28 % (1 * 0.25) / 0.25 = 0.03 / 0.25 = 0.12
        # so the 3% of the global graphic distance is actually a
        # 12% in spline distance because there are 4 splines
        if spline_index > 0:
            d = d % (spline_index * spline_size) / spline_size
        else:
            d = d / spline_size

        # spline_index is the coord, d is the percentage of
        # distance in the interpolation of the pair of coords
        pair_of_points = self.pairs_of_points[spline_index]

        # Obtain the corresponding x based on 'd' and points
        x = pair_of_points.coordinate_a.x + d * (pair_of_points.coordinate_b.x - pair_of_points.coordinate_a.x)

        coordinate = pair_of_points.get_coord_from_x(x)

        if do_denormalize:
            coordinate = Coordinate.denormalize_tuple((coordinate[0], coordinate[1]))

        return coordinate
    
    def plot(self, do_denormalize_values: bool = False):
        """
        This method is just for testing and shows the graphic
        using the matplotlib library.

        If you are plotting a path movement along the screen,
        set the 'do_denormalize_values' as True to make the
        plot show the real movement the video will do through
        the scene. If you are plotting a graph used for any
        other type of effect, keep the value as False.
        """
        # We draw 100 points per interpolation
        # TODO: Can I cast it as a tuple (?)
        graph = np.array([self.get_coord_from_d(d, False) for d in np.linspace(0, 1, len(self.coordinates) * 100)])
        points = np.array([coordinate.as_tuple() for coordinate in self.coordinates])

        if do_denormalize_values:
            # I denormalize values to be able to watch the path
            # movement properly
            # TODO: Import these min and max from constants
            graph = np.array([Coordinate.denormalize_tuple((graphi[0], graphi[1])) for graphi in graph])
            points = np.array([Coordinate.denormalize_tuple((pointi[0], pointi[1])) for pointi in points])

        plt.plot(graph[:, 0], graph[:, 1], label = 'Graphic representation', color = 'blue')
        plt.scatter(points[:, 0], points[:, 1], color = 'red', label = 'Control points')
        plt.legend()
        plt.title('Graphic representation')
        plt.xlabel('x')
        plt.ylabel('y')

        if do_denormalize_values:
            # I invert the axis to see the graph as the video
            # movement because denormalization if because of
            # this
            plt.gca().invert_yaxis()
            
        plt.grid(True)
        plt.show()


# TODO: Check moviepy.interpolation methods