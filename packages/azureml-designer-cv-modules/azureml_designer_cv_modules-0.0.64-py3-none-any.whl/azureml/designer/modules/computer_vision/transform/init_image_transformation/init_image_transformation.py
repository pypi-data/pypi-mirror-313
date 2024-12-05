import fire

from azureml.studio.core.io.transformation_directory import ImageTransformationDirectory
from azureml.studio.core.logger import logger
from azureml.studio.internal.error_handler import error_handler
from azureml.designer.modules.computer_vision.package_info import PACKAGE_NAME, VERSION


def init_transform(
        resize=False,
        size=256,
        center_crop=False,
        crop_size=224,
        pad=False,
        padding=0,
        color_jitter=False,
        grayscale=False,
        random_resized_crop=False,
        random_resized_crop_size=256,
        random_crop=False,
        random_crop_size=224,
        random_horizontal_flip=False,
        random_vertical_flip=False,
        random_rotation=False,
        random_rotation_degrees=0,
        random_affine=False,
        random_affine_degrees=0,
        random_grayscale=False,
        random_perspective=False):
    """Construct transform operations.
    Refer to https://pytorch.org/docs/stable/torchvision/transforms.html for parameter meanings. Note:
    1. Exclude 'Five/Ten crops' because they returns a tuple of images and there may be a mismatch in the number of
    inputs and targets dataset returns.
    2. Exclude tensor transfoms like 'ToTensor' and 'Random erasing' because they are tensor transforms
    not image.
    3. Should add required paras for ops 'Resize', 'Center crop', 'Pad', 'Random resized crop', 'Random crop',
    'Random rotation', 'Random affine'.

    :return: ImageTransformationDirectory
    """
    img_trans_dir = ImageTransformationDirectory.create()
    if resize:
        img_trans_dir.append('Resize', size)

    if center_crop:
        img_trans_dir.append('CenterCrop', crop_size)

    if pad:
        img_trans_dir.append('Pad', padding)

    if color_jitter:
        img_trans_dir.append('ColorJitter')

    # Known limitation: comment out grayscale transform because default normalization in both deploy service
    # and train pipeline requires RGB images, single-channel image is unsupported.
    # if grayscale:
    #     img_trans_dir.append('Grayscale')

    if random_resized_crop:
        img_trans_dir.append('RandomResizedCrop', random_resized_crop_size)

    if random_crop:
        img_trans_dir.append('RandomCrop', random_crop_size)

    if random_horizontal_flip:
        img_trans_dir.append('RandomHorizontalFlip')

    if random_vertical_flip:
        img_trans_dir.append('RandomVerticalFlip')

    if random_rotation:
        img_trans_dir.append('RandomRotation', random_rotation_degrees)

    if random_affine:
        img_trans_dir.append('RandomAffine', random_affine_degrees)

    # if random_grayscale:
    #     img_trans_dir.append('RandomGrayscale')

    if random_perspective:
        img_trans_dir.append('RandomPerspective')

    logger.info(f'Constructed image transforms: {img_trans_dir.transforms}')
    return img_trans_dir


@error_handler
def entrance(output_path, **kwargs):
    # Add package version log
    logger.info(f'{PACKAGE_NAME} {VERSION}')

    transform_dir = init_transform(**kwargs)
    transform_dir.dump(output_path)


if __name__ == '__main__':
    fire.Fire(entrance)
