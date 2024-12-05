from multiprocessing import cpu_count
import time

import torch
from azureml.core.run import Run
from azureml.designer.modules.dl.pytorch.common.pytorch_utils import raise_error
from azureml.designer.modules.dl.pytorch.train.trainer.trainer_utils import (AverageMeter, accuracy, calc_ips,
                                                                             get_padding_batch,
                                                                             get_polynomial_decay_schedule_with_warmup,
                                                                             is_first_rank, reduce_tensor,
                                                                             safe_default_collate)
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import ErrorMapping


class ClassificationTrainer:
    def __init__(self, model):
        self.model = model
        self.padding_batch = None
        self.run = Run.get_context()
        self.lr_init = 0.0001
        # Increasing worker num accelerates training obviously. 5 is good enough and can not be faster if larger than 5.
        # The cpu count threshold 10 is just an empirical value, and may help avoid OOM.
        self.num_workers = 5 if cpu_count() >= 10 else 0

    def fit(self,
            train_set,
            train_sampler,
            valid_set,
            valid_sampler,
            epochs=1,
            batch_size=2,
            num_warmup_steps=10,
            lr=0.001,
            wd=0.0001,
            momentum=0.9,
            random_seed=None,
            patience=10,
            print_freq=100):
        ErrorMapping.verify_less_than_or_equal_to(value=batch_size,
                                                  b=len(train_set),
                                                  arg_name='Batch size',
                                                  b_name='train data count')
        logger.info('Torch cuda random seed setting.')
        # Torch cuda random seed setting
        if random_seed is not None:
            if torch.cuda.is_available():
                if torch.cuda.device_count() > 1:
                    torch.cuda.manual_seed_all(random_seed)
                else:
                    torch.cuda.manual_seed(random_seed)
            else:
                torch.manual_seed(random_seed)

        logger.info("Data start loading.")
        # Set data loader
        train_loader = torch.utils.data.DataLoader(train_set,
                                                   batch_size=batch_size,
                                                   shuffle=(train_sampler is None),
                                                   sampler=train_sampler,
                                                   collate_fn=safe_default_collate,
                                                   pin_memory=(torch.cuda.is_available()),
                                                   num_workers=self.num_workers,
                                                   drop_last=True)
        valid_loader = torch.utils.data.DataLoader(valid_set,
                                                   batch_size=batch_size,
                                                   shuffle=False,
                                                   sampler=valid_sampler,
                                                   collate_fn=safe_default_collate,
                                                   pin_memory=(torch.cuda.is_available()),
                                                   num_workers=self.num_workers)
        # Use padding batch when reading image failed in a certain batch.
        try:
            self.padding_batch = get_padding_batch(train_loader)
        except Exception as e:
            raise_error(e)

        if torch.cuda.is_available():
            self.model = self.model.cuda()

        if torch.distributed.is_initialized():
            try:
                local_rank = torch.distributed.get_rank() % torch.cuda.device_count()
                self.model = torch.nn.parallel.DistributedDataParallel(self.model, device_ids=[local_rank])
            except Exception as e:
                raise_error(e)

        optimizer = torch.optim.SGD(self.model.parameters(),
                                    lr=self.lr_init,
                                    momentum=momentum,
                                    nesterov=True,
                                    weight_decay=wd)
        lr_warmup = lr * (torch.distributed.get_world_size() if torch.distributed.is_initialized() else 1)
        scheduler = get_polynomial_decay_schedule_with_warmup(optimizer,
                                                              num_warmup_steps,
                                                              epochs,
                                                              lr_warmup,
                                                              lr_init=self.lr_init,
                                                              power=2)
        # this zero gradient update is needed to avoid a warning message.
        optimizer.zero_grad()
        logger.info('Start training epochs.')
        best_top1_acc = 1
        counter = 0
        last_epoch_valid_loss = -1
        best_model = self.model
        for epoch in range(epochs):
            if torch.distributed.is_initialized():
                train_sampler.set_epoch(epoch)
            try:
                train_ips, train_loss, train_error = self.train_one_epoch(loader=train_loader,
                                                                          optimizer=optimizer,
                                                                          scheduler=scheduler,
                                                                          epoch=epoch,
                                                                          epochs=epochs,
                                                                          print_freq=print_freq)
            except Exception as e:
                raise_error(e, batch_size=batch_size)

            try:
                valid_loss, top1_acc, top5_acc = self.evaluate(loader=valid_loader)
            except Exception as e:
                raise_error(e, mode='Validation')

            # Determine if model is the best
            if top1_acc > best_top1_acc:
                is_best = True
                best_top1_acc = top1_acc
            else:
                is_best = False

            # Early stop
            if epoch == 0:
                last_epoch_valid_loss = valid_loss
            else:
                if valid_loss >= last_epoch_valid_loss:
                    counter += 1
                else:
                    counter = 0
                last_epoch_valid_loss = valid_loss

            if is_first_rank():
                self.run.log_row('learning rate', epoch=epoch + 1, lr=optimizer.param_groups[0]['lr'])
                self.run.log_row('Train images per second', epoch=epoch + 1, train_ips=train_ips)
                self.run.log_row('Train loss', epoch=epoch + 1, train_loss=train_loss)
                self.run.log_row('Train error', epoch=epoch + 1, train_error=train_error)
                self.run.log_row('Valid loss', epoch=epoch + 1, valid_loss=valid_loss)
                self.run.log_row('Top-1 validation accuracy', epoch=epoch + 1, top1_acc=top1_acc)
                self.run.log_row('Top-5 validation accuracy', epoch=epoch + 1, top5_acc=top5_acc)

            # TODO: save checkpoint files, but removed now to increase web service deployment efficiency.
            logger.info(','.join([
                f'Epoch {epoch + 1:d}', f'train_ips {train_ips:.2f}', f'train_loss {train_loss:.6f}',
                f'train_error {train_error:.6f}', f'valid_loss {valid_loss:.5f}', f'top1 acc {top1_acc:.5f}',
                f'top5 acc {top5_acc:.5f}'
            ]))
            if is_best:
                logger.info(f'Get better top1 accuracy: {top1_acc:.4f}, best checkpoint will be updated.')
                best_model = self.model

            early_stop = True if counter >= patience else False
            if early_stop:
                logger.info("Early stopped.")
                break

            scheduler.step()

        return best_model

    def train_one_epoch(self, loader, optimizer, scheduler, epoch, epochs, print_freq=100):
        """Training process every epoch.

        :param self:
        :param loader: torch.utils.data.DataLoader
        :param optimizer: torch.optim
        :param epoch: int
        :param epochs: int
        :param print_freq: int
        :return average batch_time, loss, error: float, float, float
        """
        batch_time = AverageMeter()
        losses = AverageMeter()
        errors = AverageMeter()
        ips = AverageMeter()
        # Model on train mode
        self.model.train()
        end = time.time()
        batches = len(loader)
        for batch_idx, item in enumerate(loader):
            # use padding batch.
            (input, target) = self.padding_batch if len(item) == 0 else item
            # Create variables
            if torch.cuda.is_available():
                input = input.cuda()
                target = target.cuda()

            # Compute output
            output = self.model(input)
            loss = torch.nn.functional.cross_entropy(output, target)
            # Measure accuracy and record loss
            batch_size = target.size(0)
            reduced_loss = reduce_tensor(loss.data)
            top1_acc = reduce_tensor(accuracy(output.data, target)[0])
            errors.update(1 - top1_acc.item(), batch_size)
            losses.update(reduced_loss.item(), batch_size)
            # Measure elapsed time
            elapsed_time = time.time() - end
            batch_time.update(elapsed_time, batch_size)
            ips.update(calc_ips(batch_size, elapsed_time), batch_size)
            end = time.time()
            if batch_idx % print_freq == 0 and is_first_rank():
                res = '\t'.join([
                    f'Epoch: [{epoch + 1}/{epochs}]',
                    f'Iter: [{batch_idx + 1}/{batches}]',
                    f'Avg_Time_Batch/Avg_Time_Epoch(s): {batch_time.val:.3f}/{batch_time.avg:.3f}',
                    f'Avg_Ips_Batch/Avg_Ips_Epoch(img/s): {ips.val:.4f}/{ips.avg:.4f}',
                    f'Avg_Loss_Batch/Avg_Loss_Epoch: {losses.val:.4f}/{losses.avg:.4f}',
                    f'Avg_Error_Batch/Avg_Error_Epoch: {errors.val:.4f}/{errors.avg:.4f}',
                ])
                logger.info(res)

            # Compute gradient and do SGD step
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            if torch.cuda.is_available():
                torch.cuda.synchronize()

        # Return summary statistics
        return ips.avg, losses.avg, errors.avg

    def evaluate(self, loader, print_freq=1):
        batch_time = AverageMeter()
        losses = AverageMeter()
        top1_accs = AverageMeter()
        top5_accs = AverageMeter()
        # Model on eval mode
        self.model.eval()
        end = time.time()
        # Disabling gradient calculation for inference, which will reduce memory consumption for computations.
        with torch.no_grad():
            for batch_idx, item in enumerate(loader):
                # use padding batch.
                (input, target) = self.padding_batch if len(item) == 0 else item
                # Create variables
                if torch.cuda.is_available():
                    input = input.cuda()
                    target = target.cuda()
                # compute output
                output = self.model(input)
                loss = torch.nn.functional.cross_entropy(output, target)
                # measure accuracy and record loss
                batch_size = target.size(0)
                top1_acc, top5_acc = accuracy(output.data, target, topk=(1, 5))
                loss = reduce_tensor(loss.data)
                top1_acc = reduce_tensor(top1_acc)
                top5_acc = reduce_tensor(top5_acc)

                if torch.cuda.is_available():
                    torch.cuda.synchronize()

                top1_accs.update(top1_acc.item(), batch_size)
                top5_accs.update(top5_acc.item(), batch_size)
                losses.update(loss.item(), batch_size)
                # measure elapsed time
                batch_time.update(time.time() - end)
                end = time.time()

        # Return summary statistics
        return losses.avg, top1_accs.avg, top5_accs.avg
