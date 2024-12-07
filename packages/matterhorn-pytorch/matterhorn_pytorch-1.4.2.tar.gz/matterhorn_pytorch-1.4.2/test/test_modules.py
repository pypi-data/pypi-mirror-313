import torch
import torch.nn as nn
import matterhorn_pytorch.snn as snn
import torch.nn.functional as F
from rich import print
from typing import Callable

class A:
    @property
    def b(self) -> Callable:
        return lambda x: x ** 2


def main():

    # x1 = nn.Flatten()
    # state_dict = x1.state_dict()
    # x1 = snn.Temporal(
    #     snn.Agent(
    #         x1
    #     )
    # )
    # x2 = snn.Flatten()
    # x2 = x2.multi_step_mode_()
    # x2.load_state_dict(state_dict)
    # print(x1)
    # print(x2)

    # i = torch.rand(4, 3, 3, 2, 2)
    # o1 = x1(i)
    # o2 = x2(i)
    # print(o1[1])
    # print(o2[1])
    # loss = F.mse_loss(o1, o2)
    # print(loss)
    a = A()
    print(a.b(2))

if __name__ == "__main__":
    main()