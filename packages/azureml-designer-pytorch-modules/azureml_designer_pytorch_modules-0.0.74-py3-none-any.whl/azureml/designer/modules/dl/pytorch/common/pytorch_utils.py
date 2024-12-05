import torch
from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError, ModuleOutOfMemoryError, TimeoutOccuredError


def raise_error(e, mode='Training', batch_size=None):
    ex_msg = str(e.args).lower()
    if isinstance(e, RuntimeError):
        if any(error_keywords in ex_msg
               for error_keywords in ["sizes of tensors must match", "stack expects each tensor to be equal size"]):
            ErrorMapping.rethrow(
                e,
                InvalidDatasetError(
                    dataset1=f"{mode} dataset",
                    reason=f"Got exception when {mode.lower()}: {ErrorMapping.get_exception_message(e)}",
                    troubleshoot_hint="Please transform input images to have the same size, see "
                                      "https://aka.ms/aml/init-image-transformation."))

        if any(error_keywords in ex_msg for error_keywords in [
                "out of memory", "can't allocate memory", "out of shared memory", "cudnn_status_internal_error",
                "cublas_status_alloc_failed", "unable to find a valid cudnn algorithm",
                "cudnn_status_execution_failed"]):
            ErrorMapping.rethrow(
                e,
                ModuleOutOfMemoryError(f"Cannot allocate more memory because {ErrorMapping.get_exception_message(e)}, "
                                       f"and cuda math lib might run into issue on old gpu. Please upgrade VM Sku or "
                                       f"reduce hyper-parameter 'Batch size'."))

        if any(error_keywords in ex_msg for error_keywords in
               ["timed out", "nccl error: unhandled system error", "nccl communicator was aborted"]):
            ErrorMapping.rethrow(e, TimeoutOccuredError)

    if isinstance(e, ValueError):
        if 'expected more than 1 value per channel when training' in ex_msg:
            ErrorMapping.verify_greater_than_or_equal_to(
                value=batch_size,
                # The error is most likely thrown during training small size images and if the current batch only
                # contains a single sample. For large size images, training with batch size 1 is acceptable.
                b=2 * torch.cuda.device_count() if torch.cuda.is_available() else 2,
                arg_name='Batch size')

    raise e
