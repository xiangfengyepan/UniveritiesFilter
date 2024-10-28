#pragma once

#include <cstdlib>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

#include "Degree.h"
#include "Exception.h"
#include "utilities.h"

typedef vector<string> Label;
typedef vector<int> Lengths;

using namespace std;

class Degrees {
private:
  vector<Degree> degrees;

public:
  Degrees() {}

  vector<Degree> getVector() { return degrees; }

  void filter() {
    //
  }

  void read(const string &path) {
    line("opening file" + path);
    ifstream r_file;
    r_file.open(path);
    if (not r_file.is_open()) {
      perror("open");
      throw Exception("can not open file");
    }

    line("reading file...");
    while (not r_file.eof()) {
      Degree degree;
      degree.read(r_file);
      degrees.push_back(degree);
    }

    r_file.close();
    line("done");
  }
  void write(ostream &os) {
    for (const Degree &degree : degrees) {
      degree.write(os);
      os << endl;
    }
    os << endl;
  }

  void write(ostream &os, const string &sep) {
    for (const Degree &degree : degrees) {
      degree.write(os, sep);
      os << endl;
    }
    os << endl;
  }

  void print_label(ostream &os, const Label &labels,
                   const Lengths &labels_length) {
    int index = 0;
    int size = labels.size();
    if (size != labels_length.size())
      throw Exception("wrong label size");
    for (int i = 0; i < labels.size(); ++i) {
      string label = labels[i];
      int length = labels_length[i] - label.size();
      os << label;
      print_times(os, SPACE, length);
      print_times(os, VERTICAL_BAR, 1);
    }
    os << endl;
    print_times(os, HORIZONTAL_BAR,
                add_all_size(labels) + add_all_value(labels_length) + size - 1);
    print_times(os, VERTICAL_BAR, 1);
    os << endl;
  }

  void write(const string &path) {
    line("writing in " + path);
    ofstream w_file(path);

    int name_max = 0;
    int uni_max = 0;
    int city_max = 0;
    for (const Degree &degree : degrees) {
      name_max = max(name_max, int(degree.getName().size()));
      city_max = max(city_max, int(degree.getCity().size()));
      uni_max = max(uni_max, int(degree.getUniversity().size()));
    }

    Label labels = {"Codi",     "Name", "City",        "Uni",
                    "Capacity", "AT",   "Coefficients"};
    Lengths labels_length = {5, name_max, city_max, uni_max, 4, 3, 0};
    print_label(w_file, labels, labels_length);

    Lengths word_length = {5, name_max, city_max, uni_max, 4, 3, 0};

    write(w_file, string(SPACE) + string(VERTICAL_BAR));

    w_file.close();
    line("done");
  }
};
