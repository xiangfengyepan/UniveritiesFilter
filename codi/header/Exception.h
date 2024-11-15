#pragma once
#include <exception>
#include <string>
#include <iostream>

using namespace std;

class Exception : public exception {
public:
  // Default constructor
  Exception() : exception(), mensaje("Unknown error") {}

  // Constructor with custom error message
  Exception(const string& msg) : exception(), mensaje(msg) {}

  // Override the what() function to return custom error message
  const char* what() const noexcept override {
    return mensaje.c_str();
  }

private:
  string mensaje;
};
