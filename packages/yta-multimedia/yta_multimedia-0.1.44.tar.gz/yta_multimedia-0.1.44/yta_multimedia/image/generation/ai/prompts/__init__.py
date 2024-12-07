
class Prompt:
    """
    Class to encapsulate prompts
    """
    @classmethod
    def colouring_book_sketch(cls, element: str):
        """
        Returns a prompt to generate a colouring book or sketch
        image. This means the shape of the provided 'element' 
        with black borders, white filling and a chroma key green
        background to be able to remove the background of the
        image easily.
        """
        return 'Create a simple, child-friendly coloring page featuring a ' + element + '. The ' + element + ' should have crisp, clean black outlines with no shading or gradients. The interior of the ' + element + ' should be filled with pure white. Ensure that the black lines are distinct and well-defined. The background of the image should be a solid, intense green, like chroma key green, with no additional details or elements.'