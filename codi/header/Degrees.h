#pragma once

#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

#include "Degree.h"
#include "Exception.h"

typedef vector<string> Label;
typedef vector<int> Lengths;

using namespace std;

class Degrees {
private:
  vector<Degree> degrees;

public:
  Degrees() {}

  vector<Degree> getVector() { return degrees; }

  Degree &get(const string &code) {
    for (Degree &degree : degrees) {
      if (degree.getCode() == code)
        return degree;
    }
    throw Exception("No code found");
  }

  void filter() {
    //
  }

  void read(const string &path) {
    line("opening file " + path);
    ifstream r_file;
    r_file.open(path);
    if (not r_file.is_open()) {
      perror("open");
      throw Exception("can not open file");
    }

    line("reading file...");
    while (not r_file.eof()) {
      Degree degree = Degree::read(r_file);
      degrees.push_back(degree);
    }

    r_file.close();
    line("done");
  }

  void read_coefficients(const string &path) {
    line("opening file " + path);
    ifstream r_file;
    r_file.open(path);
    if (not r_file.is_open()) {
      perror("open");
      throw Exception("can not open file");
    }

    line("reading file...");
    while (not r_file.eof()) {
      string code;
      r_file >> code;
      if (code.size() == 0)
        break;
      Degree &degree = get(code);
      degree.read_coefficients(r_file);
    }

    r_file.close();
    line("done");
  }

  void read_capacity(const string &path) {
    line("opening file " + path);
    ifstream r_file;
    r_file.open(path);
    if (not r_file.is_open()) {
      perror("open");
      throw Exception("can not open file");
    }

    line("reading file...");
    while (not r_file.eof()) {
      string code;
      r_file >> code;
      if (code.size() == 0)
        break;

      Degree &degree = get(code);
      degree.read_capacity(r_file);
    }

    r_file.close();
    line("done");
  }

  void write(ostream &os, const string &sep) {
    for (const Degree &degree : degrees) {
      degree.printDetails(os, sep);
      os << endl;
    }
    os << endl;
  }

  void write(ostream &os) { write(os, " "); }

  void write(const string &path) {
    line("writing in " + path);
    ofstream w_file(path);

    string sep = string(SPACE) + string(VERTICAL_BAR);
    Degree::printHeader(w_file, sep);
    write(w_file, sep);

    w_file.close();
    line("done");
  }
};
