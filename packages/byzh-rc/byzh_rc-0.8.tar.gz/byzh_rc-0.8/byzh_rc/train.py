import os
import time

import numpy as np
import torch
# import tqdm
from torch import nn
from pathlib import Path
from .progressBar import bProgressBar
from .log import bLogger
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

class bTrainer:
    def __init__(self, model, train_loader, val_loader, optimizer, criterion, device,
                 lrScheduler=None,
                 isBinaryCls=False, isParallel=False, isSpikingjelly=False):
        '''

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
        self.log = None

        self.model.to(self.device)

        if self.isParallel:
            print(f"当前GPU数量:{torch.cuda.device_count()}")
            if torch.cuda.device_count() > 1:
                print("使用多GPU训练")
                self.model = nn.DataParallel(self.model)

    def train_eval_s(self, epochs, log_path=None):
        '''
        :param epochs:
        :param log_path: 若提供, 则生成log文件
        :return:
        '''
        # 日志
        if log_path != None:
            self.log = bLogger(log_path, ifTime=True)

        for epoch in range(epochs):
            train_acc, current_lr = self.__train_once(epoch, epochs)
            val_acc = self.__eval_once()
            # 日志
            if self.log != None:
                self.log.toFile(f'Epoch [{epoch}/{epochs}], lr: {current_lr:.2e},'
                                f' train_acc: {train_acc:.2f}, val_acc: {val_acc:.2f}')

    def calculate_model(self, dataloader=None, model=None):
        '''
        如果不指定, 则用类内的
        :param dataloader: 默认self.train_loader
        :param model: 默认self.model
        :return:
        '''
        if dataloader==None:
            dataloader = self.train_loader
        if model==None:
            model = self.model
        model.eval()
        correct = 0
        total = 0
        y_true = []
        y_pred = []
        with torch.no_grad():
            for inputs, labels in dataloader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                outputs = model(inputs)
                _, predicted = torch.max(outputs, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()
                y_true.extend(labels.cpu().numpy())
                y_pred.extend(predicted.cpu().numpy())
                if self.isSpikingjelly:
                    from spikingjelly.activation_based import functional
                    functional.reset_net(model)
            # 记录accuracy
            accuracy = correct / total
            print('[测试]: accuracy:', accuracy)
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

    def save_model(self, path):
        parent_path = Path(path).parent
        os.makedirs(parent_path, exist_ok=True)
        torch.save(self.model.state_dict(), path)

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
                       prefix=f"{BLUE}Epoch [{epoch}/{epochs}]",
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