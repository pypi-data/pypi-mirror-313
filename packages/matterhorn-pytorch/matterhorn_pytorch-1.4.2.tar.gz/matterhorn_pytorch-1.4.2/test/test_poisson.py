import torch
import matterhorn_pytorch.snn as snn

def main():
    r = 0.99 + 0.01 * torch.rand(2, 3)
    print(r)
    p = snn.PoissonEncoder(
        time_steps = 8,
        count = True
    ).multi_step_mode_()
    l = snn.LIF()
    s = p(r)
    b = l(s, -0.5 * s)
    print(b)
    # print(s.shape, b.shape)

if __name__ == "__main__":
    main()