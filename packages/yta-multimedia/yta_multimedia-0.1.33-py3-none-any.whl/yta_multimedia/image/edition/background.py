from subprocess import run


def remove_image_background(image_filename, output_filename):
    """
    Removes the background of the provided 'image_filename' by using the 
    'backgroundremover' open library that is included in a comment.
    """
    # It uses (https://github.com/nadermx/backgroundremover?referral=top-free-background-removal-tools-apis-and-open-source-models)
    # That uses U2Net (https://medium.com/axinc-ai/u2net-a-machine-learning-model-that-performs-object-cropping-in-a-single-shot-48adfc158483)
    # TODO: Please, use this as python library not as command, ty
    command_parameters = ['backgroundremover', '-i', image_filename, '-o', output_filename]
    run(command_parameters)

    """ # Problem with Circular import
    from backgroundremover.bg import remove as remove_background
    r = lambda image_filename: image_filename.buffer.read() if hasattr(image_filename, "buffer") else image_filename.read()
    w = lambda o, data: o.buffer.write(data) if hasattr(o, "buffer") else o.write(data)

    # These below are default values
    x = remove_background(
        r(image_filename),
        model_name = 'u2net',
        alpha_matting = False,
        alpha_matting_foreground_threshold = 240,
        alpha_matting_background_threshold = 10,
        alpha_matting_erode_structure_size = 10,
        alpha_matting_base_size = 1000
    )
    w(output_filename, x)
    """

    

    # TODO: This below seems to work (as shown in this 
    # commit https://github.com/nadermx/backgroundremover/commit/c590858de4c7e75805af9b8ecdd22baf03a1368f)
    """
    from backgroundremover.bg import remove
    def remove_bg(src_img_path, out_img_path):
        model_choices = ["u2net", "u2net_human_seg", "u2netp"]
        f = open(src_img_path, "rb")
        data = f.read()
        img = remove(data, model_name=model_choices[0],
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_structure_size=10,
                    alpha_matting_base_size=1000)
        f.close()
        f = open(out_img_path, "wb")
        f.write(img)
        f.close()
    """
