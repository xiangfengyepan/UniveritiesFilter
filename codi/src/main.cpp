#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <vector>

#include "../header/Character.h"
#include "../header/Console.h"
#include "../header/Degree.h"
#include "../header/Degrees.h"
#include "../header/Exception.h"
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
      degrees.read("./dades/2024/notes.txt");
      degrees.read_coefficients("./dades/2024/coefficients.txt");
      degrees.read_capacity("./dades/2024/capacity.txt");

      degrees.write("./filter/filter.txt");

      // // console(Filtro);
    } catch (const std::bad_alloc &e) {
      std::cout << "Memory allocation failed: " << e.what() << std::endl;
    } catch (const invalid_argument &error) { // More specific exception first
      cerr << error.what() << endl;
    } catch (const exception &error) { // General exception catch-all
      cerr << error.what() << endl;
    }
  }
}