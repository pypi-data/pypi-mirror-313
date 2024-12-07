import torch
import matterhorn_pytorch.snn as snn
import matterhorn_pytorch.snn.functional as SF


if __name__ == "__main__":
    s = torch.randint(0, 2, (4, 2, 2, 4, 4))
    s = s.to(torch.half)
    s.requires_grad_()
    print(s)
    p = snn.AvgPool2d(2).multi_step_mode_()
    d = p(s)
    print(d)
    s = d.sum()
    print(s)
    s.backward()
