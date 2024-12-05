/**
    Damping kernel used in the Fourier-Wavelets sinogram destriping method.
*/
__global__ void kern_fourierwavelets(float2* sinoF, int Nx, int Ny, float wsigma) {
    int gidx = threadIdx.x + blockIdx.x*blockDim.x;
    int gidy = threadIdx.y + blockIdx.y*blockDim.y;
    int Nfft = Ny/2+1;
    if (gidx >= Nx || gidy >= Nfft) return;

    float m = gidy/wsigma;
    float factor = 1.0f - expf(-(m * m)/2);

    int tid = gidy*Nx + gidx;
    // do not forget the scale factor (here Ny)
    sinoF[tid].x *= factor;
    sinoF[tid].y *= factor;
}
