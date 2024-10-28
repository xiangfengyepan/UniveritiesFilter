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

    os << code << SPACE << name << SPACE << city << SPACE << university << SPACE
       << capacity << SPACE << admission_threshold << SPACE;
    for (int coeff : coefficients)
      os << coeff << " ";
  }
  void write(ostream &os, const string &sep) const {

    os << code << sep << name << sep << city << sep << university << sep
       << capacity << sep << admission_threshold << sep;
    for (int coeff : coefficients)
      os << coeff << " ";
  }
    void write(ostream &os, const vector<string> &sep) const {
    int i = 0;
    os << code << sep[i++] << name << sep[i++] << city << sep[i++] << university << sep[i++]
       << capacity << sep[i++] << admission_threshold << sep[i++];
    for (int coeff : coefficients)
      os << coeff << " ";

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
