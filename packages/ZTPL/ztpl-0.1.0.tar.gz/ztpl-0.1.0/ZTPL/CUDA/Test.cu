#include <torch/extension.h>
#include <torch/torch.h>
#include <vector>

// CUDA 核函数，计算两个张量的逐元素乘积
__global__ void multiply_kernel(
    torch::PackedTensorAccessor<float, 1, torch::RestrictPtrTraits, size_t> a,
    torch::PackedTensorAccessor<c10::complex<float>, 1, torch::RestrictPtrTraits, size_t> b,
    torch::PackedTensorAccessor<c10::complex<float>, 1, torch::RestrictPtrTraits, size_t> result,
    int n)
{
    const int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n)
        return;
    result[i] = a[i] * b[i];
}

// 封装函数，调用 CUDA 核函数
torch::Tensor T1(const torch::Tensor &a, const torch::Tensor &b)
{
    torch::Tensor result = torch::zeros_like(b);
    const dim3 threads(256, 1, 1);
    const dim3 blocks((a.size(0) + 256 - 1) / 256, 1, 1);

    multiply_kernel<<<blocks, threads>>>(
        a.packed_accessor<float, 1, torch::RestrictPtrTraits, size_t>(),
        b.packed_accessor<c10::complex<float>, 1, torch::RestrictPtrTraits, size_t>(),
        result.packed_accessor<c10::complex<float>, 1, torch::RestrictPtrTraits, size_t>(),
        a.size(0));
    return result;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m)
{
    m.def("T1", &T1, "Element-wise multiply");
}
