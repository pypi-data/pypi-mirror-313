from yta_multimedia.video.position import Position


# TODO: Remove this
class MoviepyPosition:
    """
    Enum class to encapsulate and simplify the way we work with
    positions in the moviepy video scene system. This is just a
    shortcut to using directly a Position Enum class and its
    moviepy methods.
    """
    @staticmethod
    def get_position(position: Position, video, background_video):
        """
        This method will calculate the (x, y) tuple position for the provided
        'video' over the also provided 'background_video' that would be,
        hypothetically, a 1920x1080 black color background static image. The
        provided 'position' will be transformed into the (x, y) tuple according
        to our own definitions.
        """
        position = Position.to_enum(position)

        return position.get_moviepy_position(video, background_video)

# TODO: Import all effects to have them here available (?)