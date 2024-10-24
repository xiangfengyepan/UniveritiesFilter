#pragma once
#include <exception>

using namespace std;

class Exception : public exception {
public:
  Exception() : exception() {}
  Exception(const char *mot) : exception(), mensaje(mot) {}
  const char *what() const throw() {
    return mensaje;
  };

private:
  const char *mensaje;
};
