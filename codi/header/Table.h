#pragma once

#include <exception>
#include <fstream>
#include <iostream>
#include <vector>
using namespace std;

#define MAX_WINDOW_WIDTH 200
#define MAX_WINDOW_HEIGHT 30

template <typename T> using List = vector<T>;

template <typename T> using Matrix = vector<List<T>>;

struct Pos {
  int x;
  int y;

  // Constructors
  Pos() : x(0), y(0) {}
  Pos(int x, int y) : x(x), y(y) {}

  // Arithmetic operators
  Pos operator+(const Pos &other) const {
    return Pos(x + other.x, y + other.y);
  }
  Pos operator-(const Pos &other) const {
    return Pos(x - other.x, y - other.y);
  }

  Pos operator*(int scalar) const { return Pos(x * scalar, y * scalar); }
  Pos operator/(int scalar) const {
    if (scalar == 0)
      throw invalid_argument("Division by zero");
    return Pos(x / scalar, y / scalar);
  }

  // Compound assignment operators (one-liners)
  Pos &operator+=(const Pos &other) {
    x += other.x;
    y += other.y;
    return *this;
  }
  Pos &operator-=(const Pos &other) {
    x -= other.x;
    y -= other.y;
    return *this;
  }
  Pos &operator*=(int scalar) {
    x *= scalar;
    y *= scalar;
    return *this;
  }
  Pos &operator/=(int scalar) {
    if (scalar == 0)
      throw invalid_argument("Division by zero");
    x /= scalar;
    y /= scalar;
    return *this;
  }

  // Comparison operators
  bool operator==(const Pos &other) const {
    return x == other.x && y == other.y;
  }
  bool operator!=(const Pos &other) const { return !(*this == other); }
  bool operator<(const Pos &other) const {
    return (x < other.x) || (x == other.x && y < other.y);
  }
  bool operator<=(const Pos &other) const {
    return *this < other || *this == other;
  }
  bool operator>(const Pos &other) const { return !(*this <= other); }
  bool operator>=(const Pos &other) const { return !(*this < other); }

  bool check(int width, int height) const {
    return 0 <= y && y < height && 0 <= x && x < width;
  }

  // Stream operators
  friend ostream &operator<<(ostream &os, const Pos &pos) {
    os << "(" << pos.x << ", " << pos.y << ")";
    return os;
  }

  friend istream &operator>>(istream &is, Pos &pos) {
    is >> pos.x >> pos.y;
    return is;
  }
};

class Table {
private:
  Matrix<char> table;
  Pos pointer;

public:
  Table()
      : table(MAX_WINDOW_HEIGHT, List<char>(MAX_WINDOW_WIDTH, 'X')),
        pointer(Pos()) {};

  Table(int width, int height)
      : table(height, List<char>(width, 'X')), pointer(Pos()) {};

  Pos getPointer() { return pointer; }
  Matrix<char> getTable() { return table; }
  void checkPointer() {
    if (!pointer.check(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT))
      throw Exception("pointer out");
  }

  void validPointer() {
    if (pointer.x < 0)
      pointer = Pos(MAX_WINDOW_WIDTH - 1, pointer.y - 1);
    if (pointer.x >= MAX_WINDOW_WIDTH)
      pointer = Pos(0, pointer.y + 1);
    checkPointer();
  }

  void setPointer(Pos &pos) {
    pointer = pos;
    validPointer();
  }

  void moveRight(int steps) {
    for (int i = 0; i < steps; ++i) {
      pointer.x++;
      validPointer();
    }
  }

  void moveLeft(int steps) {
    for (int i = 0; i < steps; ++i) {
      pointer.x--;
      validPointer();
    }
  }

  void moveDown(int steps) {
    for (int i = 0; i < steps; ++i) {
      pointer.y++;
      validPointer();
    }
  }

  void moveUp(int steps) {
    for (int i = 0; i < steps; ++i) {
      pointer.y--;
      validPointer();
    }
  }

  void moveRight() { moveRight(1); }

  void moveLeft() { moveLeft(1); }

  void moveDown() { moveDown(1); }

  void moveUp() { moveUp(1); }

  void moveStartLine() { pointer.x = 0; }

  void enter() {
    moveDown();
    moveStartLine();
  }

  void read(ifstream &is) {
    while (!is.eof()) {
      if (pointer.check(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT)) {
        is >> table[pointer.y][pointer.x];
        moveRight();
      } else
        enter();
    }
  }

  void print(ostream &os) const {
    for (const List<char> &list : table) {
      for (char element : list)
        os << element;
      os << endl;
    }
  }

  void write(const string &value) {
    for (char character : value) {
      table[pointer.y][pointer.x] = character;
      moveRight();
    }
  }
};
