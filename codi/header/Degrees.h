#pragma once

#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <string>

#include "Degree.h"
#include "Exception.h"
using namespace std;

class Degrees {
private:
  vector<Degree> degrees;

public:
  Degrees() {}

  vector<Degree> getVector()
  {
    return degrees;
  }

  vector<Degree> read(const string &path) {
    line("opening file" + path);
    ifstream r_file;
    r_file.open(path);
    if (not r_file.is_open()) {
      perror("open");
      throw Exception("can not open file");
    }
    
    line("reading file...");
    vector<Degree> degrees;
    while (not r_file.eof()) {
      Degree degree;
      degree.read(r_file);
      degrees.push_back(degree);
    }

    r_file.close();
    line("done");
    return degrees;
  }

  void write(ostream& os)
  {
    for (const Degree& degree : degrees)
      degree.write(os);
  }
};
