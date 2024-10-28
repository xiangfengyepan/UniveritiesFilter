#pragma once

template <typename T>
void print_times(ostream &os, const T &thing, int times) {
  for (int i = 0; i < times; ++i)
    os << thing;
}

template <typename T>
T add_all_value(const vector<T>& vector)
{
  T result;
  for (const T& element : vector)
    result += element;
  return result;
}

template <typename T>
int add_all_size(const vector<T>& vector)
{
  int result;
  for (const T& element : vector)
    result += element.size();
  return result;
}
