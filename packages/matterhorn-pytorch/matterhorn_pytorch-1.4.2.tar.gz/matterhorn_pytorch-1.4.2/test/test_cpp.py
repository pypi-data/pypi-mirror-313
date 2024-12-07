import torch
from matterhorn_pytorch.snn.soma import LIF as LIF


def hook(model: torch.nn.Module, grad_output: torch.Tensor, grad_input: torch.Tensor) -> None:
    print(model)
    print(grad_output)


if __name__ == "__main__":
    import time
    ref_model = LIF(u_threshold = 1.0, u_rest = 0.0).multi_step_mode_()
    ref_model.register_full_backward_hook(hook)
    x = (torch.rand(4, 2, 2) * 2).requires_grad_()
    t2 = time.time()
    z = ref_model(x)
    t2 = time.time() - t2
    print("Forward: %.6f." % (t2))
    print(z)
    sz = z.sum()
    t4 = time.time()
    sz.backward()
    t4 = time.time() - t4
    print("Backward: %.6f." % (t4))