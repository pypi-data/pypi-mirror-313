# modified from https://blog.csdn.net/m0_51816252/article/details/130657443
import torch.nn as nn

class LeNet(nn.Module):
    def __init__(self, use_sigmoid=True):
        super(LeNet, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5),
            nn.Sigmoid() if use_sigmoid else nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(6, 16, 5),
            nn.Sigmoid() if use_sigmoid else nn.ReLU(),
            nn.MaxPool2d(2, 2)
        )
        self.fc = nn.Sequential(
            nn.Linear(16*4*4, 120),
            nn.Sigmoid() if use_sigmoid else nn.ReLU(),
            nn.Linear(120, 84),
            nn.Sigmoid() if use_sigmoid else nn.ReLU(),
            nn.Linear(84, 10)
        )

    def forward(self, x):
        feature = self.conv(x)
        output = self.fc(feature.view(x.shape[0], -1))
        return output


if __name__ =='__main__':
    import torch

    model = LeNet()
    input = torch.randn(8, 1, 28, 28)
    out = model(input)
    print(out.shape)
