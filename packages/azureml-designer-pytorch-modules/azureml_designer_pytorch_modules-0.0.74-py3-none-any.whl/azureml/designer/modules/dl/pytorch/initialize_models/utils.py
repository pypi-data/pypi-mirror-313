import time
from functools import partial
from urllib.error import URLError

import torch
from azureml.studio.internal.error import ErrorMapping, FailedToDownloadFilesError
from azureml.studio.core.logger import logger


def _retry_internal(f, exceptions=Exception, tries=0, delay=0):
    """Executes a function and retries it if it failed.

    :param f: the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: 0.
    :param delay: initial delay between attempts. default: 0.
    :returns: the result of the f function.
    """
    _tries, _delay = tries, delay
    for i in range(_tries):
        try:
            return f()
        except exceptions as e:
            logger.warning(f'{e}, retrying in {_delay} seconds...')
            time.sleep(_delay)
    return f()


def retry_call(f, fargs=None, fkwargs=None, exceptions=Exception, tries=0, delay=0):
    """Calls a function and re-executes it if it failed.

    :param f: the function to execute.
    :param fargs: the positional arguments of the function to execute.
    :param fkwargs: the named arguments of the function to execute.
    :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
    :param tries: the maximum number of attempts. default: 0.
    :param delay: initial delay between attempts. default: 0.
    :returns: the result of the f function.
    """
    args = fargs if fargs else list()
    kwargs = fkwargs if fkwargs else dict()
    return _retry_internal(partial(f, *args, **kwargs), exceptions, tries, delay)


def load_pretrained_model_from_url(model_url):
    if model_url is None:
        raise ValueError(f"Invalid model url '{model_url}'.")

    try:
        retry_call(torch.hub.load_state_dict_from_url,
                   fargs=[model_url],
                   exceptions=URLError,
                   tries=3,
                   delay=3)
    except URLError as e:
        ErrorMapping.rethrow(e, FailedToDownloadFilesError(file_names=model_url))
