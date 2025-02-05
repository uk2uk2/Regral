#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib>
#include <cmath>

// DataPoint structure: x is the time index (or day number), y is the price.
struct DataPoint {
    double x;
    double y;
};

// Read CSV file and return a vector of DataPoint objects.
// The CSV is expected to have a header, then rows of the form: Date,Price,...
std::vector<DataPoint> readCSV(const std::string& filename) {
    std::vector<DataPoint> data;
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening CSV file: " << filename << std::endl;
        exit(1);
    }
    std::string line;
    // Skip header line.
    std::getline(file, line);
    while (std::getline(file, line)) {
        std::stringstream ss(line);
        std::string date, priceStr;
        if (std::getline(ss, date, ',') && std::getline(ss, priceStr, ',')) {
            try {
                double price = std::stod(priceStr);
                DataPoint dp;
                dp.y = price;
                // x will be assigned later as the sequential index.
                data.push_back(dp);
            } catch (const std::exception& e) {
                // Ignore bad lines.
                continue;
            }
        }
    }
    return data;
}

// Assign sequential x-indices (starting at 1) to each DataPoint.
void assignXIndices(std::vector<DataPoint>& data) {
    for (size_t i = 0; i < data.size(); ++i) {
        data[i].x = static_cast<double>(i + 1);
    }
}

// Compute the linear regression coefficients (slope, intercept)
// for the given data points.
std::pair<double, double> linearRegression(const std::vector<DataPoint>& data) {
    double n = static_cast<double>(data.size());
    double sumX = 0.0, sumY = 0.0, sumXY = 0.0, sumXX = 0.0;
    for (const auto& dp : data) {
        sumX += dp.x;
        sumY += dp.y;
        sumXY += dp.x * dp.y;
        sumXX += dp.x * dp.x;
    }
    double denominator = n * sumXX - sumX * sumX;
    if (denominator == 0) {
        std::cerr << "Error: denominator is zero in linear regression calculation." << std::endl;
        exit(1);
    }
    double slope = (n * sumXY - sumX * sumY) / denominator;
    double intercept = (sumY - slope * sumX) / n;
    return {slope, intercept};
}

// Given regression coefficients and an x-value, predict the y-value.
double predict(const std::pair<double, double>& coeff, double x) {
    return coeff.first * x + coeff.second;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: ./regression <csv_file>" << std::endl;
        return 1;
    }
    std::string filename = argv[1];
    auto data = readCSV(filename);
    if (data.empty()) {
        std::cerr << "No valid data found in CSV." << std::endl;
        return 1;
    }
    assignXIndices(data);
    auto coeff = linearRegression(data);
    std::cout << "Linear Regression Coefficients:" << std::endl;
    std::cout << "Slope: " << coeff.first << std::endl;
    std::cout << "Intercept: " << coeff.second << std::endl;
    
    // Predict the next day's price (x = number of data points + 1)
    double nextX = static_cast<double>(data.size() + 1);
    double predictedPrice = predict(coeff, nextX);
    std::cout << "Predicted value for day " << nextX << ": " << predictedPrice << std::endl;
    return 0;
}
