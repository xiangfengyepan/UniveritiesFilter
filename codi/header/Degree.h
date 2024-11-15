#pragma once

#include "../header/Exception.h"
#include <iomanip>
#include <iostream>
#include <regex>
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
  string capacity;
  string price;
  set<string> observations;
  string admission_threshold;
  vector<string> coefficients;

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
        result += " ";
      result += obs;
    }
    return result;
  }

  string formatCoefficients() const {
    string result;
    for (size_t i = 0; i < coefficients.size(); ++i) {
      if (i > 0)
        result += ",";
      result += coefficients[i];
    }
    return result;
  }

  const set<string> all_branches = {"AH", "C", "CS", "CSJ", "EA"};

public:
  Degree() {}

  Degree(const string &code, const string &name, const string &city,
         const string &university, const set<string> &branches,
         const string &type, const string &capacity, const string &price,
         const string &admission_threshold, const set<string> &observations,
         const vector<string> &coefficients)
      : code(code), name(name), university(university), branches(branches),
        city(city), type(type), capacity(capacity), price(price),
        admission_threshold(admission_threshold), observations(observations),
        coefficients(coefficients) {}

  string getCode() const { return code; }
  string getName() const { return name; }
  string getCity() const { return city; }
  string getUniversity() const { return university; }
  set<string> getBranches() const { return branches; }
  string getType() const { return type; }
  string getCapacity() const { return capacity; }
  string getPrice() const { return price; }
  string getThreshold() const { return admission_threshold; }
  set<string> getObservations() const { return observations; }
  vector<string> getCoefficients() const { return coefficients; }

  void setCode(const string &code) { this->code = code; }

  void setName(const string &name) { this->name = name; }

  void setCity(const string &city) { this->city = city; }

  void setUniversity(const string &university) {
    this->university = university;
  }

  void setBranches(const set<string> &branches) { this->branches = branches; }
  void setType(const string &type) { this->type = type; }
  void setCapacity(const string &capacity) { this->capacity = capacity; }
  void setPrice(const string &price) { this->price = price; }
  void setAdmissionThreshold(const string &threshold) {
    this->admission_threshold = threshold;
  }
  void setObservations(const set<string> &observations) {
    this->observations = observations;
  }
  void setCoefficients(const vector<string> &coefficients) {
    this->coefficients = coefficients;
  }

  void addCoefficient(const string &coefficient) {
    if (coefficients.size() == MAX_SIZE_COEFFICIENT)
      throw Exception("too many coefficients");
    coefficients.push_back(coefficient);
  }

  static bool isValidCode(const string &code) {
    return code.size() == 5 and all_of(code.begin(), code.end(), ::isdigit);
  }

  static bool isValidNameOrCityOrType(const string &str) {
    const std::set<char> validSpecialChars = {
        '\'', '_', '-', '"', '(', ')',
        '/',  ',', '+', '*', ':', '.'}; // Added slash to valid characters

    return all_of(str.begin(), str.end(), [&validSpecialChars](char c) {
      return isalpha(c) or isdigit(c) or
             validSpecialChars.find(c) !=
                 validSpecialChars
                     .end(); // Check if the character is alphabetic or in the
                             // set of special characters
    });
  }

  static bool isValidNumeric(const string &str) {
    return all_of(str.begin(), str.end(),
                  [](char c) { return isdigit(c) or c == '.'; });
  }

  static bool isValidAdmissionThreshold(const string &str) {
    try {
      float value = stof(str);
      return (value >= 0 and value <= 14);
    } catch (...) {
      return false;
    }
  }

  static bool isValidPrice(const string &price) {
    regex pricePattern(R"(^\d+(\.\d{1,3})?$)");
    return regex_match(price, pricePattern);
  }

  static bool isValidCoefficient(const string &coef) {
    // Implement your validation rules here
    // For example, checking if the coefficient is a valid number or matches
    // specific criteria
    return coef.size() > 0 && coef.size() <= MAX_VALUE_COEFFICIENT;
  }

  static Degree read(istream &is, bool withCoefficients) {
    Degree degree;
    string code, name, university, city, admission_threshold;
    vector<string> coefficients;

    is >> code;
    if (code == "")
      return degree;
    is >> name >> university >> city >> admission_threshold;

    if (!isValidCode(code))
      throw Exception("Invalid code: " + code);
    if (!isValidNameOrCityOrType(name))
      throw Exception("Invalid name: " + code + " " + name);
    if (!isValidNameOrCityOrType(university))
      throw Exception("Invalid university: " + code + " " + university);
    if (!isValidNameOrCityOrType(city))
      throw Exception("Invalid city: " + code + " " + city);
    if (!isValidAdmissionThreshold(admission_threshold))
      throw Exception("Invalid admission threshold.");

    degree.code = code;
    degree.name = name;
    degree.university = university;
    degree.city = city;
    degree.admission_threshold = admission_threshold;

    if (withCoefficients) {
      for (int i = 0; i < MAX_SIZE_COEFFICIENT; ++i) {
        string coef;
        is >> coef;
        coefficients.push_back(coef);
      }
      degree.coefficients = coefficients;
    }

    return degree;
  }

  static Degree read(istream &is) { return read(is, false); }

  void read_capacity(istream &is) {
    string type, capacity, price;
    set<string> observations;

    is >> type >> capacity >> price;

    if (!isValidNameOrCityOrType(type)) {
      throw Exception("Invalid type: " + type);
    }
    if (!isValidNumeric(capacity)) {
      throw Exception("Invalid capacity: " + capacity);
    }
    if (!isValidPrice(price)) {
      throw Exception("Invalid price: " + price);
    }

    string obs;
    is >> obs;

    if (obs == "None") {
      observations.insert("None");
    } else {
      string observation;
      for (char c : obs) {
        if (c == '-') {
          if (!observation.empty()) {
            observations.insert(observation);
          }
        } else {
          observation += c;
        }
      }

      if (!observation.empty()) {
        observations.insert(observation);
      }
    }

    this->type = type;
    this->capacity = capacity;
    this->price = price;
    this->observations = observations;
  }

  void read_coefficients(istream &is) {
    set<string> branches;
    vector<string> coefficients;
    string input;

    is >> input;
    while (all_branches.find(input) != all_branches.end()) {
      branches.insert(input);
      is >> input;
    }

    if (branches.empty()) {
      throw Exception("No valid branches found.");
    }

    coefficients.push_back(input);

    for (int i = 0; i < MAX_SIZE_COEFFICIENT - 1; ++i) {
      string coef;
      is >> coef;

      if (isValidCoefficient(coef)) {
        coefficients.push_back(coef);
      } else {
        throw Exception("Invalid coefficient: " + coef);
      }
    }

    if (coefficients.size() > MAX_SIZE_COEFFICIENT) {
      throw Exception("Too many coefficients.");
    }

    this->branches = branches;
    this->coefficients = coefficients;
  }

  void display() const {
    cout << "Code: " << code << " ";
    cout << "Name: " << name << " ";
    cout << "University: " << university << " ";
    cout << "City: " << city << " ";
    cout << "Type: " << type << " ";
    cout << "Capacity: " << capacity << " ";
    cout << "Price: " << price << " ";
    cout << "Admission Threshold: " << admission_threshold << " ";

    cout << "Branches: ";
    for (const auto &branch : branches) {
      cout << branch << " ";
    }
    cout << " ";

    cout << "Observations: ";
    for (const auto &obs : observations) {
      cout << obs << " ";
    }
    cout << " ";

    cout << "Coefficients: ";
    for (const auto &coeff : coefficients) {
      cout << coeff << " ";
    }
    cout << endl;
  }
  void printDetails(ostream &os, const string &sep) const {
    string formatted_name = name;
    // Replace underscores with spaces in the name
    replace(formatted_name.begin(), formatted_name.end(), '_', ' ');

    os << left << setw(SETW_CODE) << truncateString(code, SETW_CODE) << sep
       << setw(SETW_NAME) << truncateString(formatted_name, SETW_NAME) << sep
       << setw(SETW_CITY) << truncateString(city, SETW_CITY) << sep
       << setw(SETW_UNIVERSITY) << truncateString(university, SETW_UNIVERSITY)
       << sep << setw(SETW_BRANCHES)
       << truncateString(formatBranches(), SETW_BRANCHES) << sep
       << setw(SETW_CAPACITY) << truncateString(capacity, SETW_CAPACITY) << sep
       << setw(SETW_PRICE) << truncateString(price, SETW_PRICE) << sep
       << setw(SETW_THRESHOLD)
       << truncateString(admission_threshold, SETW_THRESHOLD) << sep
       << setw(SETW_OBSERVATIONS)
       << truncateString(formatObservations(), SETW_OBSERVATIONS) << sep
       << setw(SETW_COEFFICIENTS)
       << truncateString(formatCoefficients(), SETW_COEFFICIENTS) << endl;
  }

  static void printHeader(ostream &os, const string &sep) {
    os << left << setw(SETW_CODE) << "Code" << sep << setw(SETW_NAME) << "Name"
       << sep << setw(SETW_CITY) << "City" << sep << setw(SETW_UNIVERSITY)
       << "University" << sep << setw(SETW_BRANCHES) << "Branches" << sep
       << setw(SETW_CAPACITY) << "Capacity" << sep << setw(SETW_PRICE)
       << "Price" << sep << setw(SETW_THRESHOLD) << "Threshold" << sep
       << setw(SETW_OBSERVATIONS) << "Observations" << sep << "Coefficients"
       << endl;

    os << string(SETW_CODE + SETW_NAME + SETW_CITY + SETW_UNIVERSITY +
                     SETW_BRANCHES + SETW_CAPACITY + SETW_PRICE +
                     SETW_THRESHOLD + SETW_OBSERVATIONS + SETW_COEFFICIENTS +
                     (9 * sep.length()),
                 '-')
       << endl;
  }
};
