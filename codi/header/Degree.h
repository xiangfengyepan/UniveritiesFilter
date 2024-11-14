#pragma once

#include "../header/Exception.h"
#include <iomanip>
#include <iostream>
#include <set>
#include <vector>
using namespace std;

#define MAX_VALUE_COEFFICIENT 2
#define MAX_SIZE_COEFFICIENT 27

class Degree {
private:
  string code;
  string name;
  string university;
  set<string> branches;
  string city;
  string type;
  int capacity;
  int price;
  set<string> observations;
  float admission_threshold;
  vector<int> coefficients;

  string truncateString(const string &str, size_t width) const {
    if (str.length() > width)
      return str.substr(0, width - 3) + "...";
    return str;
  }

  string formatBranches() const {
    string result;
    for (const auto &branch : branches) {
      if (!result.empty())
        result += ",";
      result += branch;
    }
    return truncateString(result, 15);
  }

  string formatObservations() const {
    string result;
    for (const auto &obs : observations) {
      if (!result.empty())
        result += ",";
      result += obs;
    }
    return result;
  }

  string formatCoefficients() const {
    string result;
    for (size_t i = 0; i < coefficients.size(); ++i) {
      if (i > 0)
        result += ",";
      result += to_string(coefficients[i]);
    }
    return result;
  }

  const set<string> all_branches = {"AH", "C", "CS", "CSJ", "EA"};

public:
  Degree() {}

  Degree(const string &code, const string &name, const string &city,
         const string &university, const set<string> &branches,
         const string &type, int capacity, int price, float admission_threshold,
         const set<string> &observations)
      : code(code), name(name), university(university), branches(branches),
        city(city), type(type), capacity(capacity), price(price),
        admission_threshold(admission_threshold), observations(observations) {}

  string getCode() const { return code; }
  string getName() const { return name; }
  string getCity() const { return city; }
  string getUniversity() const { return university; }
  set<string> getBranches() const { return branches; }
  string getType() const { return type; }
  int getCapacity() const { return capacity; }
  int getPrice() const { return price; }
  double getThreshold() const { return admission_threshold; }
  set<string> getObservations() const { return observations; }
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
    if (withCoefficients) {
      for (int i = 0; i < MAX_SIZE_COEFFICIENT; ++i) {
        int coef;
        is >> coef;
        addCoefficient(coef);
      }
    }
  }
  void read(istream &is) { read(is, false); }

  void read_coefficients(istream &is) {
    string input;
    is >> input;
    while (all_branches.find(input) != all_branches.end()) {
      branches.insert(input);
      is >> input;
    }

    addCoefficient(stoi(input));
    for (int i = 0; i < MAX_SIZE_COEFFICIENT - 1; ++i) {
      int coef;
      is >> coef;
      addCoefficient(coef);
    }
  }

  void read_capacity(istream &is) {
    is >> type >> capacity;
    string price;
    is >> price;
    this->price = stoi(price);

    string observations;
    is >> observations;
    string observation;

    if (observations == "None")
      observation = observations;
    else {
      for (char c : observations) {
        if (c == '-')
          this->observations.insert(observation);

        observation += c;
      }
    }
    this->observations.insert(observation);
  }

  void display() const {
    cout << "Code: " << code << " ";
    cout << "Name: " << name << " ";
    cout << "University: " << university << " ";
    cout << "City: " << city << " ";
    cout << "Admission_threshold: " << admission_threshold << " ";
    cout << endl;
    cout << "Coefficients: ";
    for (int coeff : coefficients) {
      cout << coeff << " ";
    }
    cout << endl;
  }

  void printDetails(ostream &os, const string &sep) const {
    os << left << setw(5) << truncateString(code, 5) << sep << setw(20)
       << truncateString(name, 20) << sep << setw(10)
       << truncateString(city, 10) << sep << setw(10)
       << truncateString(university, 10) << sep << setw(10)
       << truncateString(formatBranches(), 10) << sep << setw(10)
       << truncateString(to_string(capacity), 10) << sep << setw(10)
       << truncateString(to_string(price), 10) << sep << setw(10)
       << truncateString(to_string(admission_threshold), 10) << sep
       << truncateString(formatObservations(), 10) << sep
       << truncateString(formatCoefficients(), 20) << endl;
  }

  static void printHeader(ostream &os, const string &sep) {
    os << left << setw(5) << "Code" << sep << setw(20) << "Name" << sep
       << setw(10) << "City" << sep << setw(10) << "University" << sep
       << setw(10) << "Branches" << sep << setw(10) << "Capacity" << sep
       << setw(10) << "Price" << sep << setw(10) << "Threshold" << sep
       << setw(10) << "Observations" << sep << "Coefficients" << endl;

    os << string(5 + 20 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 20 +
                     (9 * sep.length()),
                 '-')
       << endl;
  }
};
