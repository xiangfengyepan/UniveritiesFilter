#pragma once

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <string>
using namespace std;

#define line(x) cout << x << endl;

class Interface {
private:
public:
  Interface() {}

  void read() {
    // fstream myfile;

    // myfile.open("./dades/spain.txt");
    // if (not myfile.is_open()) {
    //   perror("open");
    //   throw Exception();
    // }

    // int code;
    // myfile >> code;

    // while (code != "-1") {
    //   string name, city, university, capacity, admission_threshold;
    //   myfile >> name >> city >> university >> capacity >> admission_threshold;
    //   Degree degree(code, name, city, university, capacity,
    //                 admission_threshold);
    //   ceofficients = vector<int>(22) for (int i = 0; i < 22; ++i) {
    //     int coefficient;
    //     myfile >> coefficient;
    //     ceofficients.push(coefficient);
    //   }

    //   Degrees.push_back(degree);
    //   myfile >> degree.getCode();
    //   if (myfile.eof())
    //     break;
    // }
    // myfile.close();
  }
};
