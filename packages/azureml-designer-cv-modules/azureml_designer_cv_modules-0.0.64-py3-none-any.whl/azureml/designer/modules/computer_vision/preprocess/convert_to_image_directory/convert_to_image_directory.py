import itertools
import tarfile
from pathlib import Path
import shutil
from tempfile import mkdtemp
from urllib.error import URLError
from zipfile import BadZipFile

import fire

# zipfile37 is a backport of the zipfile module from Python 3.7, which contains some improvements.
# However, this package could meet a compliance issue as it is personal. so copy it here from
# https://github.com/markus1978/zipfile37 to add support for ZIP files with disks set to 0.
# Such files are commonly created by builtin tools on Windows when use ZIP64 extension.
# See details in https://github.com/python/cpython/pull/5985.
# TODO: revert to use zipfile when we upgrade python to version above 3.7.
import azureml.designer.modules.computer_vision.preprocess.convert_to_image_directory.zipfile37 as zipfile
from azureml.studio.core.io.any_directory import _META_FILE_PATH
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.error import _OPEN_SUPPORT_TICKET_HINT
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError, ModuleOutOfMemoryError
from azureml.studio.internal.error_handler import error_handler
from azureml.designer.modules.computer_vision.package_info import PACKAGE_NAME, VERSION

# This mapping is used for handling compressed files
COMPRESSED_EXT_TO_METHOD = {
    '.zip': zipfile.ZipFile,
    # do not use class 'tarfile.TarFile' directly but tarfile.open() instead
    # based on https://docs.python.org/3/library/tarfile.html
    '.tar': tarfile.open,
    '.gz': tarfile.open,
    '.bz2': tarfile.open,
}
# Useless metadata created across different os, which may break original directory structure.
USELESS_METADATA_SET = {'__MACOSX'}


def _remove_useless_metadata(input_dir: Path):
    '''Remove useless metadata like "__MACOSX" folder. This folder is created when compressing file on Mac but
    useless outside Mac. And it may break original directory structure, which will be used in image classification
    task to detect labels if the input directory follows torchvision ImageFolder structure.
    '''
    for file_name in USELESS_METADATA_SET:
        file_path = input_dir / file_name
        if file_path.is_dir():
            shutil.rmtree(file_path)
            logger.info(f"Removed useless metadata folder '{file_path}'.")
        elif file_path.is_file():
            file_path.unlink()
            logger.info(f"Removed useless metadata file '{file_path}'.")


def detect_base_dir_in_uncompressed(uncompressed_dir: Path):
    """Detect the real base directory containing images in an uncompressed directory.
    Set uncompressed_dir as root and recursively search if current directory contains only one directory.
    For example,
    root/xx.yaml => root
    root/aaa/xx.yaml => root/aaa
    In case of one-class torchvision ImageFolder (category is saved as subfolder name),
    returns parent path of the final detected directory during the recursion. For example,
    root/dog/*.png => root
    Noted, cannot return root parent path in case including extra unexpected files. For example,
    root/*.png => root
    """
    def first_n_files(path, file_num=2):
        return list(itertools.islice(Path(path).iterdir(), file_num))

    def get_sub_dir_cnt(path):
        return len([x for x in path.iterdir() if x.is_dir()])

    base_dir = uncompressed_dir
    _remove_useless_metadata(base_dir)
    while True:
        files = first_n_files(base_dir)
        if not files:
            ErrorMapping.throw(
                InvalidDatasetError(dataset1=base_dir.name,
                                    reason=f"no file is found in '{base_dir}'",
                                    troubleshoot_hint="Please input a non-empty compressed file."))

        sub_dir_cnt = get_sub_dir_cnt(base_dir)
        logger.info(f"{sub_dir_cnt} subfolder(s) in current directory '{base_dir}'. List some files: {files}.")
        # in case of one-class torchvision image folder.
        if sub_dir_cnt == 0 and not (base_dir / _META_FILE_PATH).exists() and base_dir != uncompressed_dir:
            logger.info(f"Detected as a one-class torchvision ImageFolder. Use parent path '{base_dir.parent}'"
                        " as base directory for sake of annotation.")
            return base_dir.parent

        if len(files) == 1 and files[0].is_dir():
            logger.info(f"Only 1 folder is found in '{base_dir}', start searching the subfolder '{files[0]}'.")
            base_dir = files[0]
        else:
            logger.info(f"Detected real base directory path '{base_dir}'.")
            return base_dir


def extract_compressed_file_to_dir(compressed_file: Path):
    ext = compressed_file.suffix
    target_dir = Path(mkdtemp())
    try:
        with COMPRESSED_EXT_TO_METHOD[ext](compressed_file) as zf:
            zf.extractall(target_dir)
    except BadZipFile as e:
        if 'zipfiles that span multiple disks are not supported' in str(e.args):
            ErrorMapping.rethrow(e, InvalidDatasetError(
                dataset1=compressed_file,
                reason=f"Got exception when extracting the file: {ErrorMapping.get_exception_message(e)}",
                troubleshoot_hint="Please unpack the file and repack it on a single disk."))
        else:
            raise e
    except OSError as e:
        if 'No space left on device' in str(e.args):
            ErrorMapping.rethrow(e, ModuleOutOfMemoryError('Cannot allocate more memory. Please upgrade VM Sku.'))
        else:
            raise e
    except tarfile.ReadError as e:
        if 'file could not be opened successfully' in str(e.args):
            ErrorMapping.rethrow(e, InvalidDatasetError(
                dataset1=compressed_file,
                reason=f"Got exception when extracting the file: {ErrorMapping.get_exception_message(e)}",
                troubleshoot_hint="Please use the right pack way to prepare the compressed file, "
                                  "compatible with the file extension."))
        else:
            raise e
    except RuntimeError as e:
        if 'ipynb' in str(e.args).lower():
            ErrorMapping.rethrow(e, InvalidDatasetError(
                dataset1=compressed_file,
                reason=f"Got exception when extracting the file: {ErrorMapping.get_exception_message(e)}",
                troubleshoot_hint="Please remove non-image files from the compressed file. see "
                                  "https://aka.ms/aml/convert-to-image-directory for input image dataset requirement."))
        else:
            raise e

    logger.info(f"Extract compressed file to path '{target_dir}'.")
    target_dir = detect_base_dir_in_uncompressed(target_dir)
    return target_dir


def detect_image_directory_path(input_path: Path):
    """Detect target image directory path when walking through input path.

    :param input_path: Path
    :return: Path
    """
    target_dir = input_path
    # Fix bug 971294. `Path.is_file()` could return False if the path doesn't exist or is a broken symlink.
    # See https://docs.python.org/3/library/pathlib.html. And there is a known issue that dataset may not be
    # fully downloaded until iterated, because dataset team loads the dataset to local machine in a lazy way.
    if not input_path.exists():
        ErrorMapping.throw(InvalidDatasetError(
            dataset1=input_path.name,
            reason=f"input path '{str(input_path)}' doesn't exist",
            troubleshoot_hint=f"Please retry as this may be a transient issue. {_OPEN_SUPPORT_TICKET_HINT}"))

    if input_path.is_file():
        if input_path.suffix in COMPRESSED_EXT_TO_METHOD:
            logger.info(f"Input is a compressed file. Loading from {input_path}.")
            target_dir = extract_compressed_file_to_dir(input_path)
        else:
            ErrorMapping.throw(
                InvalidDatasetError(dataset1=input_path.name,
                                    reason=f"file extension '{input_path.suffix}' is not allowed",
                                    troubleshoot_hint="Please input a compressed file with allowed extensions: "
                                    f"{set(COMPRESSED_EXT_TO_METHOD.keys())}."))
    else:
        # load from any valid compressed file in first layer of current directory.
        compressed_file_paths = list(
            itertools.islice((path for path in input_path.iterdir() if path.suffix in COMPRESSED_EXT_TO_METHOD), 1))
        if len(compressed_file_paths) > 0:
            logger.info(f"Found {len(compressed_file_paths)} compressed file(s) in current directory. "
                        f"Pick 1 file to load: '{compressed_file_paths[0]}'.")
            target_dir = extract_compressed_file_to_dir(compressed_file_paths[0])
        else:
            # try to load from current directory.
            logger.info(f"Loading from directory {input_path}.")
            _remove_useless_metadata(input_path)

    return target_dir


@error_handler
def convert(input_path, output_path):
    # Add package version log
    logger.info(f'{PACKAGE_NAME} {VERSION}')

    input_path = Path(input_path)
    target_dir = detect_image_directory_path(input_path)
    try:
        loader_dir = ImageDirectory.load(target_dir)
        loader_dir.dump(output_path)
    except (FileNotFoundError, ValueError) as e:
        ErrorMapping.rethrow(
            e,
            InvalidDatasetError(dataset1=input_path.name,
                                reason=f"Got exception when loading: {ErrorMapping.get_exception_message(e)}",
                                troubleshoot_hint="Please make sure all images in input dataset are valid, see "
                                "https://aka.ms/aml/convert-to-image-directory for input image dataset requirement."))
    except URLError as e:
        ErrorMapping.rethrow(
            e,
            InvalidDatasetError(
                dataset1=input_path.name,
                reason=f"Got exception when dumping: {ErrorMapping.get_exception_message(e)}",
                troubleshoot_hint="Please check if could download image from your input image url, and fix the url"
                " protocol, see https://aka.ms/aml/convert-to-image-directory for input image dataset requirement."))


if __name__ == '__main__':
    fire.Fire(convert)
