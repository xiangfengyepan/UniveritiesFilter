#pragma once

#include "../header/Exception.h"
#include <iomanip>
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

  string truncateString(const string &str, size_t width) const {
    if (str.length() > width)
      return str.substr(0, width - 3) + "...";
    return str;
  }

public:
  Degree() {}

  Degree(const string &code, const string &name, const string &city,
         const string &university, int capacity, float admission_threshold)
      : code(code), name(name), university(university), city(city),
        capacity(capacity), admission_threshold(admission_threshold) {}

  void printDetails(ostream &os, const string &sep) const {
    os << left << setw(5) << truncateString(code, 5) << sep << setw(100)
       << truncateString(name, 100) << sep << setw(15)
       << truncateString(city, 15) << sep << setw(20)
       << truncateString(university, 20) << sep << setw(10) << capacity << sep
       << setw(5) << admission_threshold << endl;
  }

  static void printHeader(ostream &os, const string &sep) {
    os << left << setw(5) << "Code" << sep << setw(100) << "Name" << sep
       << setw(15) << "City" << sep << setw(20) << "University" << sep
       << setw(10) << "Capacity" << sep << setw(5) << "Threshold" << endl;

    os << string(5 + 100 + 15 + 20 + 10 + 5 + (6 * sep.length()), '-') << endl;
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

  void read(istream &is, bool withCoefficients) {

    is >> code >> name >> university >> city >> admission_threshold;
    if (code == "11001" or code == "21152")
      display();
    if (withCoefficients) {
      for (int i = 0; i < MAX_SIZE_COEFFICIENT; ++i) {
        int coef;
        is >> coef;
        addCoefficient(coef);
      }
    }
  }

  void read(istream &is) { read(is, false); }

  void display() const {
    cout << "Code: " << code << " ";
    cout << "Name: " << name << " ";
    cout << "University: " << university << " ";
    cout << "City: " << city << " ";
    cout << "Admission_threshold: " << admission_threshold << " ";
    cout << "Coefficients: ";
    for (int coeff : coefficients) {
      cout << coeff << " ";
    }
    cout << endl;
  }
};
