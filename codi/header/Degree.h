#pragma once

#include "../header/Exception.h"
#include <iostream>
#include <vector>
using namespace std;

#define MAX_VALUE_COEFFICIENT 2
#define MAX_SIZE_COEFFICIENT 22

class Degree {
private:
  string code;
  string name;
  string city;
  string university;
  int capacity;
  float admission_threshold;
  vector<int> coefficients;

public:
  Degree(const string& code, const string &name, const string &city,
         const string &university, int capacity, float admission_threshold)
      : code(code), name(name), city(city), university(university),
        capacity(capacity), admission_threshold(admission_threshold) {}

  string getCode() const { return code; }

  string getName() const { return name; }

  string getCity() const { return city; }

  string getUniversity() const { return university; }

  int getCapacity() const { return capacity; }

  double getThreshold() const { return admission_threshold; }

  vector<int> getCoefficients() const { return coefficients; }

  void addCoefficient(int coefficient) {
    if (not(0 <= coefficient and coefficient <= MAX_VALUE_COEFFICIENT))
      throw Exception("wrong value ceofficinet");
    if (coefficients.size() == MAX_SIZE_COEFFICIENT)
      throw Exception("too many coefficients");
    coefficients.push_back(coefficient);
  }

  void display() const {
    cout << "Code: " << code << endl;
    cout << "Name: " << name << endl;
    cout << "City: " << city << endl;
    cout << "University: " << university << endl;
    cout << "Capacity: " << to_string(capacity) << endl;
    cout << "Admission_threshold: " << admission_threshold << endl;
    cout << "Coefficients: ";
    for (int coeff : coefficients) {
      cout << coeff << " ";
    }
    cout << endl;
  }
};
