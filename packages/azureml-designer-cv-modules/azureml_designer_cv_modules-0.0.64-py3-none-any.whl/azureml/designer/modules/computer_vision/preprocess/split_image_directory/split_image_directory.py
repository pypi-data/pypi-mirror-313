import fire
from sklearn.model_selection import train_test_split

from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.image_schema import ImageAnnotationTypeName
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError
from azureml.studio.internal.error_handler import error_handler
from azureml.designer.modules.computer_vision.package_info import PACKAGE_NAME, VERSION

STRATIFY_SPLIT_ANN_TYPE = {ImageAnnotationTypeName.CLASSIFICATION}


def random_split_to_idx(idx_list, fraction):
    train_idx, test_idx = train_test_split(idx_list, train_size=fraction, random_state=42)
    return train_idx, test_idx


def stratify_split_to_idx(idx_list, strats_list, fraction):
    train_idx, test_idx, _, _ = train_test_split(idx_list,
                                                 strats_list,
                                                 stratify=strats_list,
                                                 train_size=fraction,
                                                 random_state=42)
    return train_idx, test_idx


@error_handler
def split(src_path, tgt_train_path, tgt_test_path, fraction=0.9):
    # Add package version log
    logger.info(f'{PACKAGE_NAME} {VERSION}')

    loaded_dir = ImageDirectory.load(src_path)
    image_list = loaded_dir.image_list
    idx_list = list(range(len(image_list)))
    # validate image count
    image_cnt = len(idx_list)
    if image_cnt <= 1:
        ErrorMapping.throw(
            InvalidDatasetError(dataset1='Input image directory',
                                reason="no need to split for a dataset containing less than 2 images",
                                troubleshoot_hint="Remove the module from your graph."))

    # validate fraction
    ErrorMapping.verify_value_in_range(value=fraction,
                                       lower_bound=1.0 / image_cnt,
                                       upper_bound=1 - 1.0 / image_cnt,
                                       arg_name='Fraction')

    try:
        ann_type = loaded_dir.get_annotation_type()
        if ann_type in STRATIFY_SPLIT_ANN_TYPE:
            ann_col_name = loaded_dir.get_annotation_column()
            logger.info(f"For task {ann_type}, stratify split by annotation column '{ann_col_name}'.")
            ann_list = [item[ann_col_name] for item in image_list]
            train_idx, test_idx = stratify_split_to_idx(idx_list, ann_list, fraction)
        else:
            logger.info(f'For task {ann_type}, random split.')
            train_idx, test_idx = random_split_to_idx(idx_list, fraction)
    except ValueError as e:
        logger.warning(f'Got exception: {ErrorMapping.get_exception_message(e)} random split.')
        train_idx, test_idx = random_split_to_idx(idx_list, fraction)

    train_set_dir = loaded_dir.get_sub_dir(train_idx)
    test_set_dir = loaded_dir.get_sub_dir(test_idx)
    train_set_dir.dump(tgt_train_path)
    test_set_dir.dump(tgt_test_path)


if __name__ == '__main__':
    fire.Fire(split)
