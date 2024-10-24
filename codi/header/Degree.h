#pragma once

#include "../header/Exception.h"
#include <iostream>
#include <vector>
using namespace std;

#define MAX_VALUE_COEFFICIENT 3
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
  Degree() {}

  // Degree(const string &code, const string &name, const string &city,
  //        const string &university, int capacity, float admission_threshold)
  //     : code(code), name(name), university(university), city(city),
  //       capacity(capacity), admission_threshold(admission_threshold) {}
  Degree(const string &code, const string &name, const string &city,
         const string &university, int capacity, float admission_threshold) {
    this->code = code;
  }

  string getCode() const { return code; }

  string getName() const { return name; }

  string getCity() const { return city; }

  string getUniversity() const { return university; }

  int getCapacity() const { return capacity; }

  double getThreshold() const { return admission_threshold; }

  vector<int> getCoefficients() const { return coefficients; }

  void addCoefficient(int coefficient) {
    if (not(0 <= coefficient and coefficient <= MAX_VALUE_COEFFICIENT))
      throw Exception("wrong value coefficient");
    if (coefficients.size() == MAX_SIZE_COEFFICIENT)
      throw Exception("too many coefficients");
    coefficients.push_back(coefficient);
  }

  void read(istream &is) {
    is >> code >> name >> university >> city >> capacity >> admission_threshold;

    for (int i = 0; i < MAX_SIZE_COEFFICIENT; ++i) {
      int coef;
      is >> coef;
      addCoefficient(coef);
    }
  }

  void write(ostream &os) const {
    os << "Code: " << code << endl;
    os << "Name: " << name << endl;
    os << "City: " << city << endl;
    os << "University: " << university << endl;
    os << "Capacity: " << to_string(capacity) << endl;
    os << "Admission_threshold: " << admission_threshold << endl;
    os << "Coefficients: ";
    for (int coeff : coefficients)
      os << coeff << " ";
    os << endl;
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
