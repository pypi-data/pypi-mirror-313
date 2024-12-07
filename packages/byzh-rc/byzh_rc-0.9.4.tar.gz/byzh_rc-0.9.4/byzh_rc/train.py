import os
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn
from .progressBar import bProgressBar
from .log import bLogger

class _COLOR:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

class _stopByAcc:
    def __init__(self, rounds):
        self.rounds = rounds
        self.cnt = 0
    def __call__(self, train_acc, val_acc, max_val_acc, delta=0.01):
        if val_acc < train_acc-delta:
            self.cnt += 1
        if val_acc > train_acc or val_acc == max_val_acc:
            self.cnt = 0
        if self.cnt > self.rounds:
            return True
        return False

class _saveDuringTrain:
    def __init__(self, path, rounds):
        self.path = path
        self.rounds = rounds
        self.cnt = 0
    def __call__(self):
        self.cnt += 1
        if self.cnt > self.rounds:
            self.cnt = 0
            return True
        return False

class bTrainer:
    def __init__(self, model, train_loader, val_loader, optimizer, criterion, device,
                 lrScheduler=None,
                 isBinaryCls=False, isParallel=False, isSpikingjelly=False):
        '''
        训练:\n
        train_eval_s\n
        训练前函数:\n
        load_model, load_optimizer, load_lrScheduler, set_logger, set_stop_by_acc\n
        训练后函数:\n
        save_latest_checkpoint, save_best_checkpoint, calculate_model
        :param model:
        :param train_loader:
        :param val_loader:
        :param optimizer:
        :param criterion:
        :param device:
        :param lrScheduler:
        :param isBinaryCls: 若是二分类, 则输出额外信息
        :param isParallel: 是否多GPU
        :param isSpikingjelly: 是否为SNN
        '''
        self.train_loss_lst = []
        self.train_acc_lst = []
        self.val_acc_lst = []
        self.val_f1_lst = []
        self.val_L0_True_lst = []
        self.val_L1_True_lst = []

        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.lrScheduler = lrScheduler
        self.isBinaryCls = isBinaryCls
        self.isParallel = isParallel
        self.isSpikingjelly = isSpikingjelly

        self.__isTraining = False
        self.__save_during_train = None
        self.__log = None
        self.__stop_by_acc = None
        self.__best_acc = 0
        self.__best_net_state_dict = None
        self.__best_optimizer_state_dict = None
        self.__best_lrScheduler_state_dict = None


        self.model.to(self.device)

        if self.isParallel:
            print(f"当前GPU数量:{torch.cuda.device_count()}")
            if torch.cuda.device_count() > 1:
                print("使用多GPU训练")
                self.model = nn.DataParallel(self.model)

    def train_eval_s(self, epochs):
        '''
        :param epochs:
        :return:
        '''
        self.__isTraining = True

        for epoch in range(epochs):
            train_acc, current_lr = self.__train_once(epoch, epochs)
            val_acc = self.__eval_once()
            # 日志
            if self.__log != None:
                self.__log.toFile(f'Epoch [{epoch}/{epochs}], lr: {current_lr:.2e},'
                                  f' train_acc: {train_acc:.3f}, val_acc: {val_acc:.3f}')
            # 保存模型
            if self.__save_during_train != None:
                if self.__save_during_train():
                    self.save_best_checkpoint(self.__save_during_train.path)
            # 早停
            if self.__stop_by_acc != None:
                if self.__stop_by_acc(train_acc, val_acc, max(self.val_acc_lst)):
                    print(f'模型在连续{self.__stop_by_acc.rounds}个epoch内停滞, 触发stop_by_acc')
                    break

    def calculate_model(self, dataloader=None, model=None):
        '''
        如果不指定, 则用类内的
        :param dataloader: 默认self.val_loader
        :param model: 默认self.model
        :return:
        '''
        if dataloader==None:
            dataloader = self.val_loader
        if model==None:
            model = self.model
        model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        inference_time = []
        with torch.no_grad():
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                start_time = time.time()
                outputs = model(inputs)
                end_time = time.time()
                _, predicted = torch.max(outputs, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())
                inference_time.append(end_time - start_time)
                if self.isSpikingjelly:
                    from spikingjelly.activation_based import functional
                    functional.reset_net(model)
            # 平均推理时间
            inference_time = sum(inference_time) / len(inference_time)
            # 精确度
            accuracy = correct / total
            # 参数量
            params = sum(p.numel() for p in model.parameters())
            info = f'[calculate] accuracy: {accuracy:.3f}, inference_time: {inference_time:.2e}s, params: {params/1e3}K'
            print(info)
            if self.__log:
                self.__log.toFile(info)
            if self.isBinaryCls:
                from sklearn.metrics import confusion_matrix
                mat = confusion_matrix(y_true, y_pred)
                print('mat:\n', mat)

                TN, FP, FN, TP = mat.ravel()

                f1 = self.__get_f1(TP, FP, FN)
                print('f1:', f1)

                L0_True = self.__get_L0_True(TN, FP)
                print('L0_True:', L0_True)

                L1_True = self.__get_L1_True(FN, TP)
                print('L1_True:', L1_True)

    def save_latest_checkpoint(self, path):
        '''
        字典checkpoint包含net, optimizer, lrScheduler
        '''
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)

        checkpoint = {
            'net': self.model.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'lrScheduler': self.lrScheduler.state_dict()
        }
        torch.save(checkpoint, path)
        print(f"最新checkpoint已保存到{path}")

    def save_best_checkpoint(self, path):
        '''
        字典checkpoint包含net, optimizer, lrScheduler
        '''
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)

        checkpoint = {
            'net': self.__best_net_state_dict,
            'optimizer': self.__best_optimizer_state_dict,
            'lrScheduler': self.__best_lrScheduler_state_dict
        }
        torch.save(checkpoint, path)
        print(f"最佳checkpoint已保存到{path}")
    def load_model(self, path):
        checkpoint = torch.load(path)
        self.model.load_state_dict(checkpoint['net'])
        print(f"model已从{path}加载")
    def load_optimizer(self, path):
        checkpoint = torch.load(path)
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        print(f"optimizer已从{path}加载")
    def load_lrScheduler(self, path):
        checkpoint = torch.load(path)
        self.lrScheduler.load_state_dict(checkpoint['lrScheduler'])
        print(f"lrScheduler已从{path}加载")

    def set_logger(self, logPath, mode='a'):
        '''
        请在训练前设置set_logger
        :param logPath:
        :param mode: 'a', 'w'
        :return:
        '''
        self.__log = bLogger(logPath, ifTime=True)
        if mode == 'a':
            pass
        if mode == 'w':
            self.__log.clearFile()

        self.__log.toFile("model="+str(self.model), ifTime=False)
        if self.lrScheduler is not None:
            self.__log.toFile("lrScheduler="+str(self.lrScheduler.__class__.__name__), ifTime=False)
        print(f'日志将保存到{logPath}')
    def set_save_during_train(self, path, rounds=10):
        '''
        请在训练前设置set_save_during_train
        '''
        self.__save_during_train = _saveDuringTrain(path, rounds)
    def set_stop_by_acc(self, rounds=10):
        '''
        请在训练前设置set_stop_by_acc
        :param rounds: 连续rounds次过拟合且val_acc不上升
        :return:
        '''
        self.__stop_by_acc = _stopByAcc(rounds=rounds)

    def draw(self, jpgPath, isShow=False):
        parent_path = Path(jpgPath).parent
        os.makedirs(parent_path, exist_ok=True)

        import matplotlib.pyplot as plt
        plt.figure(figsize=(8, 8))

        plt.subplot(3, 1, 1)
        # 每十个画一次(防止点多卡顿)
        temp = [x for i, x in enumerate(self.train_loss_lst) if (i + 1) % 10 == 0]
        plt.plot(temp, color="red", label="train_loss")
        plt.xlabel("awa")
        plt.ylabel("loss")
        plt.legend(loc='upper right')

        plt.subplot(3, 1, 2)
        plt.plot(self.train_acc_lst, color="red", label="train_acc")
        plt.plot(self.val_acc_lst, color="blue", label="val_acc")
        plt.xlabel("epoch")
        plt.ylabel("acc")
        plt.ylim(-0.05, 1.05)
        plt.legend(loc='lower right')

        if self.isBinaryCls:
            plt.subplot(3, 1, 3)
            plt.plot(self.val_f1_lst, color="red", label="f1")
            plt.plot(self.val_L0_True_lst, color="blue", label="L0_True")
            plt.plot(self.val_L1_True_lst, color="green", label="L1_True")
            plt.xlabel("epoch")
            plt.ylabel("score")
            plt.ylim(-0.05, 1.05)
            plt.legend(loc='lower right')

        plt.savefig(jpgPath)
        if isShow:
            plt.show()
        plt.close()

    def __train_once(self, epoch, epochs):
        bar = bProgressBar(total=len(self.train_loader))
        current_lr = self.optimizer.param_groups[0]['lr']

        self.model.train()
        correct = 0
        total = 0
        for iter, (inputs, labels) in enumerate(self.train_loader):
            # 基本训练
            inputs, labels = inputs.to(self.device), labels.to(self.device)
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            self.optimizer.zero_grad()  # 清零梯度
            loss.backward()  # 计算梯度
            self.optimizer.step()  # 更新参数
            # SNN
            if self.isSpikingjelly:
                from spikingjelly.activation_based import functional
                functional.reset_net(self.model)
            # 进度条
            bar.update(1,
                       prefix=f"{_COLOR.BLUE}Epoch [{epoch}/{epochs}]",
                       suffix=f"lr: {current_lr:.2e}, loss: {loss.item():.2f}")
            # 数据记录
            self.train_loss_lst.append(loss.item())
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        accuracy = correct / total
        print(f'Epoch [{epoch}/{epochs}], train_Acc: {accuracy:.4f}', end='')
        self.train_acc_lst.append(accuracy)

        # 更新学习率
        if self.lrScheduler:
            self.lrScheduler.step()

        return accuracy, current_lr

    def __eval_once(self):
        self.model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        with torch.no_grad():
            for inputs, labels in self.val_loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs, 1)

                if self.isSpikingjelly:
                    from spikingjelly.activation_based import functional
                    functional.reset_net(self.model)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

            # 记录accuracy
            accuracy = correct / total
            # print('Epoch [{}/{}], val_Acc: {:.4f}'.format(epoch, epochs, accuracy))
            print(f', val_Acc: {accuracy:.4f}')
            self.val_acc_lst.append(accuracy)
            # 保存最优模型
            if accuracy > self.__best_acc:
                self.__best_acc = accuracy
                self.__best_net_state_dict = self.model.state_dict()
                self.__best_optimizer_state_dict = self.optimizer.state_dict()
                self.__best_lrScheduler_state_dict = self.lrScheduler.state_dict() if self.lrScheduler else None

            if self.isBinaryCls:
                from sklearn.metrics import confusion_matrix
                TN, FP, FN, TP = confusion_matrix(y_true, y_pred).ravel()

                f1 = self.__get_f1(TP, FP, FN)
                self.val_f1_lst.append(f1)

                L0_True = self.__get_L0_True(TN, FP)
                self.val_L0_True_lst.append(L0_True)

                L1_True = self.__get_L1_True(FN, TP)
                self.val_L1_True_lst.append(L1_True)

        return accuracy

    def __get_precision(self, TP, FP):
        if TP + FP == 0:
            return np.nan
        return TP / (self, TP + FP)

    def __get_recall(self, TP, FN):
        return TP / (TP + FN)

    def __get_f1(self, TP, FP, FN):
        precision = self.__get_precision(TP, FP)
        recall = self.__get_recall(TP, FN)
        if np.isnan(precision):
            return np.nan
        f1 = 2 * precision * recall / (precision + recall)
        return f1

    def __get_L0_True(self, TN, FP):
        return TN / (TN + FP)

    def __get_L1_True(self, FN, TP):
        return TP / (TP + FN)