import torch
import torch.nn as nn
from matterhorn_pytorch.snn import Agent


class Core:
    def c(self):
        return "5"


class DemoModel(nn.Module):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.core = Core()

    def __getattr__(self, name: str) -> torch.Any:
        print(name)
        return getattr(self.core, name)

    def forward(self, x: torch.Tensor, y: int):
        print(x.shape, y)
        return torch.zeros_like(x), y


if __name__ == "__main__":
    a = Agent(DemoModel()).multi_step_mode_()
    data = torch.rand(3, 4, 4)
    res, _ = a(data, 3)
    print(res, _)
    print(a.c())