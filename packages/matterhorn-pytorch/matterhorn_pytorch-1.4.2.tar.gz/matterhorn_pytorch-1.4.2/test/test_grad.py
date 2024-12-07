import torch

def hook(grad: torch.Tensor):
    print(grad)

x = torch.tensor([-0.5, 0.0, 0.5, 1.0, 1.5]).requires_grad_()
x.register_hook(hook)
y = torch.clamp(x, 0.0, 1.0)

print(y)

y.sum().backward()