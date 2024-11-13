#include <iostream>
#include <algorithm>
#include <vector>
#include <cstdlib>

#include "../header/Character.h"
#include "../header/Degree.h"
#include "../header/Degrees.h"
#include "../header/Exception.h"
#include "../header/Console.h"
using namespace std;

int main() {
  srand(time(0));
  cout.setf(ios::fixed);
  cout.precision(1);

  string op;
  while (op != "exit") {
    try {
      cin >> op;
      Degrees degrees;
      degrees.read("./dades/spain.txt");
      degrees.write("./filter/filter.txt");

      // // console(Filtro);
    } catch (const invalid_argument &error) { // More specific exception first
      cerr << error.what() << endl;
    } catch (const exception &error) { // General exception catch-all
      cerr << error.what() << endl;
    }
  }
}