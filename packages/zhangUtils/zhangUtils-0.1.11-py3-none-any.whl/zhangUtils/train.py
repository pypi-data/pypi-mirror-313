import torch
from tqdm import tqdm
import os
from torch import nn
from torch.utils.tensorboard import SummaryWriter


def test(model, testloader, criterion):

    model.eval()  # 将模型设置为评估模式
    criterion = criterion.cuda()
    
    sum_loss = 0

    loop = enumerate(testloader)

    with torch.no_grad():  
        for i, (data, targets) in (loop):
            # Get data to cuda if possible
            # forward
            scores = model(data)
            loss = criterion(scores, targets)

            sum_loss += loss.item()
    
    return sum_loss / (testloader.__len__())


## 可以考虑保存优化器
# 不实现gt 与 x 进行cuda(), 直接在Dataset中对gt进行.cuda()以实现更灵活的模型
def train(model, criterion, optimizer, trainloader, epochs, testloader, testEpoch, modelSavedPath='../data/model/', scheduler=None):

    if not os.path.exists(modelSavedPath):
        os.makedirs(modelSavedPath)
        writer = SummaryWriter(os.path.join(modelSavedPath, 'log/'))
        print(f'{modelSavedPath} mkdir success')

    model = model.cuda()
    criterion = criterion.cuda()

    test_min_loss = 9e9

    for epoch in range(epochs):

        loop = tqdm(enumerate(trainloader), total=(len(trainloader)))
        loop.set_description(f'Epoch [{epoch}/{epochs}]')

        sum_loss = 0
        count = 0

        for i, (data, targets) in loop:
            # forward
            scores = model(data)
            loss = criterion(scores, targets)

            sum_loss += loss.item()
            count += 1

            # backward
            optimizer.zero_grad()
            loss.backward()

            # gardient descent or adam step
            optimizer.step()

        print(f'train loss:{sum_loss / count}')

        if epoch % testEpoch == 0:

            test_loss = test(model, testloader, criterion)

            print(f'test loss:{test_loss}')

            if test_loss < test_min_loss:
                test_min_loss = test_loss

                torch.save(model.state_dict(), os.path.join(modelSavedPath, 'best_model.pkl'))
                print(f'{epoch}\'s model have saved to best_model.pkl')

        # test后再scheduler
        if scheduler != None:
            scheduler.step()
            
    torch.save(model.state_dict(), os.path.join(modelSavedPath, f'{epoch}_model.pkl'))
