import datetime
import os

import torch
from azureml.studio.core.logger import logger
from mpi4py import MPI
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data.dataloader import default_collate

_MPI_MASTER_NODE_ENV_NAME = 'AZ_BATCHAI_MPI_MASTER_NODE'
_DEFAULT_PORT = ':23456'
# No below env var if mpi run is activated on single node although multiple processes.
_MASTER_NODE_ENV_NAME = 'AZ_BATCH_MASTER_NODE'


def get_rank():
    # If no mpi run is triggered, rank will be 0.
    return MPI.COMM_WORLD.Get_rank()


def get_world_size():
    # If no mpi run is triggered, world size will be 1.
    return MPI.COMM_WORLD.Get_size()


class DistributedConfig():
    def __init__(self, master_node_ip):
        self.master_node_ip = master_node_ip
        # If no mpi run is triggered, rank will be 0, world_size 1.
        self.rank = get_rank()
        self.world_size = get_world_size()
        print(f'rank {self.rank}, world_size {self.world_size}')
        # Fix bug 1369468: require world_size greater than 1 for dist training in case env var
        # "AZ_BATCHAI_MPI_MASTER_NODE" value changes.
        self.distributed = self.master_node_ip is not None and self.world_size > 1 and torch.cuda.is_available()
        self.local_rank = self.rank % torch.cuda.device_count() if self.distributed else -1
        self.dist_url = f'tcp://{self.master_node_ip}' if self.distributed else None

    @classmethod
    def create(cls):
        print(f'os env {os.environ}')
        mpi_master_node_env_val = os.environ.get(_MPI_MASTER_NODE_ENV_NAME, None)
        master_node_ip = os.environ.get(
            _MASTER_NODE_ENV_NAME,
            None if mpi_master_node_env_val is None else f'{mpi_master_node_env_val}{_DEFAULT_PORT}')
        return cls(master_node_ip)


def init_distributed_mode(rank, world_size, local_rank, dist_url):
    torch.cuda.set_device(local_rank)
    logger.info(f'Distributed init (rank {rank}, local_rank {local_rank}): {dist_url}.')
    os.environ['NCCL_BLOCKING_WAIT'] = '1'
    torch.distributed.init_process_group(backend='nccl',
                                         init_method=dist_url,
                                         world_size=world_size,
                                         rank=rank,
                                         timeout=datetime.timedelta(seconds=600))
    # Synchronizes all processes to ensure process group is ready.
    torch.distributed.barrier()


def is_first_rank():
    # Use torch.distributed.get_rank to check first due to no env var available in pytest to trigger dist train.
    if torch.distributed.is_initialized():
        return torch.distributed.get_rank() == 0
    else:
        return get_rank() == 0


def accuracy(output, target, topk=(1, )):
    """Computes the top k accuracy"""
    maxk = min(max(topk), output.shape[1])
    size = target.size(0)
    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.reshape(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
        res.append(correct_k / size)
    return res


def reduce_tensor(tensor):
    rt = tensor.clone()
    if torch.distributed.is_initialized():
        torch.distributed.all_reduce(rt, op=torch.distributed.ReduceOp.SUM)

    rt /= torch.distributed.get_world_size() if torch.distributed.is_initialized() else 1
    return rt


def calc_ips(batch_size, time):
    """Training throughput. Calculate images per second."""
    world_size = torch.distributed.get_world_size() if torch.distributed.is_initialized() else 1
    tbs = world_size * batch_size
    return tbs / time


def safe_default_collate(batch):
    filtered_batch = [x for x in batch if x is not None]
    if len(filtered_batch) == 0:
        return []
    return default_collate(filtered_batch)


def get_padding_batch(loader):
    padding_batch = None
    for batch in loader:
        if len(batch) > 0:
            padding_batch = batch
            break
    # TODO: raise error if padding batch is None
    return padding_batch


class AverageMeter(object):
    """Computes and stores the average and current value
    Copied from: https://github.com/pytorch/examples/blob/master/imagenet/main.py
    """
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def get_polynomial_decay_schedule_with_warmup(optimizer,
                                              num_warmup_steps,
                                              num_training_steps,
                                              lr_warmup,
                                              lr_init=0.0001,
                                              lr_end=1e-7,
                                              power=1.0,
                                              last_epoch=-1):
    """Create a schedule with a learning rate that decreases as a polynomial decay from the initial lr set in the
    optimizer to end lr defined by `lr_end`, after a warmup period during which it increases linearly from 0 to the
    initial lr set in the optimizer.

    :param optimizer:class: torch.optim.Optimizer. The optimizer for which to schedule the learning rate.
    :param num_warmup_steps: int. The number of steps for the warmup phase.
    :param num_training_steps: int. The total number of training steps.
    :param lr_warmup: float. The learning rate at the end of warmup.
    :param lr_init: float. The initial learning rate.
    :param lr_end: float. The end learning rate.
    :param power: float. Power factor.
    :param last_epoch: int. The index of the last epoch when resuming training.
    Note: `power` defaults to 1.0 as in the fairseq implementation, which in turn is based on the original BERT
    implementation at
    https://github.com/google-research/bert/blob/f39e881b169b9d53bea03d2d341b31707a6c052b/optimization.py#L37
    :return: torch.optim.lr_scheduler.LambdaLR.
    """
    def lr_lambda(current_step: int):
        if current_step < num_warmup_steps:
            cur_lr = lr_init + (lr_warmup - lr_init) * current_step / num_warmup_steps
        else:
            lr_range = lr_warmup - lr_end
            decay_steps = num_training_steps - num_warmup_steps
            pct_remaining = 1 - (current_step - num_warmup_steps) / decay_steps
            cur_lr = lr_range * pct_remaining**power + lr_end

        return cur_lr / lr_init  # as LambdaLR multiplies by lr_init

    return LambdaLR(optimizer, lr_lambda, last_epoch)
