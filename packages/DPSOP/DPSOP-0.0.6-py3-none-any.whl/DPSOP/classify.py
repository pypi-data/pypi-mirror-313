"""
分类
"""

import torch
from torch.utils.tensorboard import SummaryWriter

class ClassifySop(object):
    def __init__(self,model,train_loader,val_loader,device="cpu",tensorboard_logs_dir="runs"):
        super(ClassifySop, self).__init__()
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.device = device
        self.tensorboard_logs_dir = tensorboard_logs_dir
        self.model.to(self.device)

        self.train_losses = []
        self.val_losses = []
        self.train_accs = []
        self.val_accs = []

    def __train_model(self,loss_fn,optimizer):
        '''
        模型训练
        :param loss_fn:  损失函数
        :param optimizer: 优化器
        :return: loss 和 acc
        '''

        self.model.train() # 切换到训练模式

        size = len(self.train_loader.dataset) # 训练数据的总个数
        batch_size = len(self.train_loader)  # 训练批次

        losses,accs = 0,0 # 损失值和正确个数

        for X,y in self.train_loader:
            X = X.to(self.device) # 训练数据
            y = y.to(self.device) # 真实值

            pred = self.model(X) # 预测值
            loss = loss_fn(pred,y)

            # 反向传播
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            # 统计损失和正确个数
            losses += loss.item()
            accs += (pred.argmax(1)==y).type(torch.float).sum().item()

        # 返回平均损失和正确个数
        losses /= batch_size
        accs /= size

        return losses, accs

    def __validate_model(self,loss_fn,optimizer):
        '''
        模型验证
        :param loss_fn:
        :param optimizer:
        :return:
        '''

        self.model.eval() # 切换模式

        size = len(self.val_loader.dataset)
        batch_size = len(self.val_loader)

        losses,accs = 0,0

        for X,y in self.val_loader:
            X = X.to(self.device)
            y = y.to(self.device)

            pred = self.model(X)
            loss = loss_fn(pred,y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            losses += loss.item()
            accs += (pred.argmax(1)==y).type(torch.float).sum().item()

        losses /= batch_size
        accs /= size

        return losses, accs

    def train(self,epochs,loss_fn,optimizer,clear_history=True):
        '''
        模型训练
        :param epochs: 训练周期
        :param loss_fn: 损失函数
        :param optimizer: 优化器
        :return:
        '''

        if clear_history:
            self.train_accs = []
            self.train_losses = []
            self.val_accs = []
            self.val_losses = []


        for epoch in range(epochs):
            # 训练模型
            train_loss, train_acc = self.__train_model(loss_fn,optimizer)
            self.train_losses.append(train_loss)
            self.train_accs.append(train_acc)

            # 模型验证
            val_loss, val_acc = self.__validate_model(loss_fn,optimizer)
            self.val_losses.append(val_loss)
            self.val_accs.append(val_acc)

            print(f"周期：{epoch+1}/{epochs} 训练损失：{train_loss:.4f} 训练正确率：{train_acc*100:.2f}% 验证损失：{val_loss:.4f} 验证正确率：{val_acc*100:.2f}%")


    def show_tensorboard(self,example_input):
        '''

        :param example_input: 输入示例
        :return:
        '''
        writer = SummaryWriter(self.tensorboard_logs_dir)

        for i,loss in enumerate(self.train_losses):
            writer.add_scalar('训练 Loss', loss, i)

        for i,acc in enumerate(self.train_accs):
            writer.add_scalar("训练 Accuracy", acc, i)

        for i,loss in enumerate(self.val_losses):
            writer.add_scalar("验证 Loss", loss, i)

        for i,acc in enumerate(self.val_accs):
            writer.add_scalar("验证 Accuracy", acc, i)

        writer.add_graph(self.model,input_to_model=example_input.to(self.device),verbose=True)
        writer.close()






