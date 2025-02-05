#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cuda_runtime.h>

// ------------------------------------------------------
// CUDA Kernel Example: Compute Daily Returns
// For an array of prices: returns[i] = (price[i+1] - price[i]) / price[i]
// ------------------------------------------------------
__global__
void dailyReturnsKernel(const float* prices, float* returns, int n)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < n - 1) {
        float pToday = prices[idx];
        float pTomorrow = prices[idx + 1];
        // Basic daily return formula (watch out for dividing by zero in real usage).
        returns[idx] = (pTomorrow - pToday) / pToday;
    }
}

int main(int argc, char* argv[])
{
    if (argc < 2) {
        std::cerr << "Usage: ./cuda_finance <csv_file>" << std::endl;
        return 1;
    }
    std::string filename = argv[1];

    // ------------------------------------------------------
    // Step 1: Read CSV into Host Vector
    // ------------------------------------------------------
    std::vector<float> prices;
    {
        std::ifstream file(filename);
        if (!file.is_open()) {
            std::cerr << "Could not open file: " << filename << std::endl;
            return 1;
        }

        // Example: CSV with a single column of prices or 
        // possibly more columns where the 2nd col is price. 
        // For demonstration, assume 1st row is a header we skip.
        std::string line;
        bool skipHeader = true;
        while (std::getline(file, line)) {
            if (skipHeader) {
                skipHeader = false;
                continue;
            }
            std::stringstream ss(line);
            std::string valStr;
            // Here, assume each line has at least one numeric field we want
            if (std::getline(ss, valStr, ',')) {
                try {
                    float price = std::stof(valStr);
                    prices.push_back(price);
                } catch (...) {
                    // If parsing fails, skip or handle error
                }
            }
        }
        file.close();
    }
    int n = prices.size();
    if (n < 2) {
        std::cerr << "Not enough price data to compute returns." << std::endl;
        return 1;
    }
    std::cout << "Loaded " << n << " price entries from CSV." << std::endl;

    // ------------------------------------------------------
    // Step 2: Allocate Device Memory for Prices and Returns
    // ------------------------------------------------------
    float *d_prices = nullptr;
    float *d_returns = nullptr;
    cudaMalloc((void**)&d_prices, n * sizeof(float));
    cudaMalloc((void**)&d_returns, n * sizeof(float));  // same length, though last is not used

    // ------------------------------------------------------
    // Step 3: Copy Data from Host to Device
    // ------------------------------------------------------
    cudaMemcpy(d_prices, prices.data(), n * sizeof(float), cudaMemcpyHostToDevice);

    // ------------------------------------------------------
    // Step 4: Launch Kernel to Process Data in Parallel
    // ------------------------------------------------------
    int blockSize = 256;
    int gridSize = (n + blockSize - 1) / blockSize;
    dailyReturnsKernel<<<gridSize, blockSize>>>(d_prices, d_returns, n);
    cudaDeviceSynchronize();

    // ------------------------------------------------------
    // Step 5: Copy Results Back to Host
    // ------------------------------------------------------
    std::vector<float> returns(n);
    cudaMemcpy(returns.data(), d_returns, n * sizeof(float), cudaMemcpyDeviceToHost);

    // (Optional) Print some sample outputs
    std::cout << "Sample computed returns (first 5):" << std::endl;
    for (int i = 0; i < 5 && i < n - 1; i++) {
        std::cout << "Day " << i << " -> " << returns[i] << std::endl;
    }

    // ------------------------------------------------------
    // Cleanup
    // ------------------------------------------------------
    cudaFree(d_prices);
    cudaFree(d_returns);

    return 0;
}
