"""
    There is some code here below that is generating a
    video moving throw the scene by the path defined in
    the GraphicInterpolation, and that is resized and
    the movement is recalculated based on the resized 
    so it is actually being resized while moving with
    no error.
"""
from yta_multimedia.video.edition.effect.moviepy.position.interpolation import GraphicInterpolation, InterpolationMethod, InterpolatedPair
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyWithPrecalculated
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.position.objects.coordinate import Coordinate
from moviepy import VideoFileClip


def test():
    # Create 3 consecutive pairs
    p1 = InterpolatedPair(Position.HALF_LEFT, Position.HALF_TOP, InterpolationMethod.LINEAR)
    p2 = InterpolatedPair(Position.HALF_TOP, Position.HALF_RIGHT, InterpolationMethod.LINEAR)
    p3 = InterpolatedPair(Position.HALF_RIGHT, Position.HALF_BOTTOM, InterpolationMethod.LINEAR)

    graph = GraphicInterpolation([p1, p2, p3])

    video = VideoFileClip('prueba.mp4').with_subclip(0, 1)
    #video = video.resized(0.5)
    fd = 1 / video.fps  # frame duration

    resizes = [1 - 0.7 * f * fd / video.duration for f in range(int(video.fps * video.duration))]
    # Obtain the position for each frame duration
    positions = [graph.get_coord_from_d(f * fd / video.duration) for f in range(int(video.fps * video.duration))]
    # The position above has been calculated for a video of
    # 1920x1080 over an scene of also 1920x1080, so adapt it to
    # our video

    # Transform center position to upper left corner
    for i, _ in enumerate(positions):
        positions[i] = Coordinate(positions[i][0], positions[i][1]).get_moviepy_upper_left_corner_tuple((video.w * resizes[i], video.h * resizes[i]))

    # TODO: I think we need to accept GraphicInterpolation as
    # a MoviepyWith parameter to be able to calculate the
    # positions for each frame and apply them considering the
    # also provided 'resizes'.
    # MoviepyWith is considering the 'resize' while moving, so
    # If i allow GraphicInterpolation to be accepted and adapt
    # the code to make the calculations, this example will be
    # working by itself just passing the GraphicInterpolation
    MoviepyWithPrecalculated.apply(video, with_position_list = positions, resized_list = resizes).write_videofile('a_test_precalculated.mp4')