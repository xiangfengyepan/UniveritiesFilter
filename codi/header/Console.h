// #include <iostream>
// #include "./Degrees.h"
// using namespace std;

// Degrees degrees;

// string order;
// string _data;
// vector<string> v;
// double nota_max;
// double nota_min;

// void instruct() {
//   cout << "\033[2J\033[0;0H";
//   cout << "Instructions 😊" << endl << endl;

//   cout << "---to filter write first the comand {} and then a parameter []---"
//        << endl;
//   cout << "comand: {instruct} to view this at anytime" << endl;
//   cout << "comand: {clear} to go back to the original list" << endl << endl;
//   cout << "- {codi} [asc, des, or a llist]" << endl;
//   cout << "- {name} [asc, des, or a llist]" << endl;
//   cout << "- {space} [asc, des, or a llist]" << endl;
//   cout << "- {uni} [asc, des, or a llist]" << endl;
//   cout << "- {nota} [asc, des, interval]" << endl;
//   cout << "- {pond} [all, two]" << endl << endl;
//   cout << "!!!The llist must be separeted with spaces and ended with '-1' "
//           "note()!!!"
//        << endl
//        << endl;
//   cout << "---Diccionari---" << endl;
//   cout << "   - asc: ascendent" << endl;
//   cout << "   - des: descendent" << endl;
//   cout << "   - pond: ponderacions" << endl;
//   cout << endl;
// }

// void pond_instruct() {
//   cout << "\033[2J\033[0;0H";
//   cout << "Ponderacions Subjects 📖" << endl;
//   cout << "---write the numberd and finish with a '-1'---" << endl;
//   cout << " 0: Analisi Musical" << endl;
//   cout << " 1: Biologia" << endl;
//   cout << " 2: Ciencies de la Terra i del Medi Ambient" << endl;
//   cout << " 3: Cultura Audiovisual" << endl;
//   cout << " 4: Dibuix Artistic" << endl;
//   cout << " 5: Dibuix Tecnic" << endl;
//   cout << " 6: Disseny" << endl;
//   cout << " 7: Economia de l'Empresa" << endl;
//   cout << " 8: Electrotecnia" << endl;
//   cout << " 9: Fisica" << endl;
//   cout << "10: Fonaments de les Arts" << endl;
//   cout << "11: Geografia" << endl;
//   cout << "12: Grec" << endl;
//   cout << "13: Historia de la Filosofia" << endl;
//   cout << "14: Historia de l'Art" << endl;
//   cout << "15: Literatura Castellana" << endl;
//   cout << "16: Literatura Catalana" << endl;
//   cout << "17: Llati" << endl;
//   cout << "18: Matematiques" << endl;
//   cout << "19: Matematiques Aplicades a les CC.SS" << endl;
//   cout << "20: Quimica" << endl;
//   cout << "21: Tecnologia Industrial" << endl;
//   cout << endl;
// }

// string remove_leading_zeros(string &number) {
//   if (number[number.length() - 1] == '0' or
//       number[number.length() - 1] == '.') {
//     number.pop_back();
//     remove_leading_zeros(number);
//   }
//   return number;
// }

// void write(const vector<Degree> &degrees) {
//   // int name_max = 0;
//   // int uni_max = 0;
//   // int space_max = 0;
//   // for (const Degree &degree : degrees) {
//   //   name_max = max(name_max, int(degree.getName().size()));
//   //   uni_max = max(uni_max, int(degree.getName().size()));
//   //   space_max = max(space_max, int(degree.getName().size()));
//   // }

//   // ofstream w_file("./dades/filtre.txt");

//   // Label labels = {"Codi", "Name"};
//   // print_label(w_file, labels);

//   // myfile <<
//   // "┃00┃01┃02┃03┃04┃05┃06┃07┃08┃09┃10┃11┃12┃13┃14┃15┃16┃17┃18┃19┃20┃21┃" <<
//   // endl;

//   // for (int index = 0; index < size; ++index) {
//   //   Degree c = degrees[index];

//   //   myfile << c.getCode() << " ┃";

//   //   myfile << c.getName() << " ";
//   //   for (int i = c.getName().size(); i < name_max; ++i)
//   //     myfile << " ";

//   //   myfile << "┃";
//   //   myfile << c.getCity() << " ";
//   //   for (int i = c.getCity().size(); i < space_max; ++i)
//   //     myfile << " ";

//   //   myfile << "┃";
//   //   myfile << c.getUniversity() << " ";
//   //   for (int i = c.getUniversity().size(); i < uni_max; ++i)
//   //     myfile << " ";

//   //   myfile << "┃";
//   //   myfile << c.getThreshold() << " ";

//   //   string num_str = to_string(c.getThreshold());
//   //   remove_leading_zeros(num_str);
//   //   for (int i = num_str.size(); i < 6; ++i)
//   //     myfile << " ";

//   //   myfile << "┃";
//   //   for (int i = 0; i < 22; ++i) {
//   //     if (c.getCoefficients()[i] == '2') {
//   //       if (i < 10)
//   //         myfile << "0";
//   //       myfile << i << "┃";
//   //     }
//   //   }
//   //   myfile << endl;
//   // }
//   // myfile.close();
//   // cout << "\033[2J\033[0;0H";
//   // cout << "find: " << size << "/" << degrees.size() << " degrees" << " 😨"
//   //      << endl;

//   // cout << order;
//   // if (_data != "-1") {
//   //   cout << " " << _data;
//   //   if (_data == "interval")
//   //     cout << " " << nota_max << " " << nota_min;
//   //   cout << endl;
//   // } else {
//   //   cout << " llist [";
//   //   for (int i = 0; i < v.size(); ++i) {
//   //     if (i != 0)
//   //       cout << " ";
//   //     cout << v[i];
//   //   }
//   //   cout << "]" << endl;
//   //   v.clear();
//   // }
// }

// bool cmp_codi_asc(const Degree &a, const Degree &b) {
//   return a.getCode() > b.getCode();
// }

// bool cmp_codi_des(const Degree &a, const Degree &b) {
//   return a.getCode() < b.getCode();
// }

// bool cmp_name_asc(const Degree &a, const Degree &b) {
//   return a.getName() > b.getName();
// }

// bool cmp_name_des(const Degree &a, const Degree &b) {
//   return a.getName() < b.getName();
// }

// bool cmp_space_asc(const Degree &a, const Degree &b) {
//   return a.getCity() > b.getCity();
// }

// bool cmp_space_des(const Degree &a, const Degree &b) {
//   return a.getCity() < b.getCity();
// }

// bool cmp_uni_asc(const Degree &a, const Degree &b) {
//   return a.getUniversity() > b.getUniversity();
// }

// bool cmp_uni_des(const Degree &a, const Degree &b) {
//   return a.getUniversity() < b.getUniversity();
// }

// bool cmp_nota_asc(const Degree &a, const Degree &b) {
//   return a.getThreshold() > b.getThreshold();
// }

// bool cmp_nota_des(const Degree &a, const Degree &b) {
//   return a.getThreshold() < b.getThreshold();
// }

// bool cmp_nota_max(const Degree &a, const Degree &b) {
//   if ((a.getThreshold() <= nota_max and a.getThreshold() >= nota_min) and
//       (b.getThreshold() <= nota_max and b.getThreshold() >= nota_min))
//     return a.getThreshold() > b.getThreshold();
//   if ((a.getThreshold() <= nota_max and a.getThreshold() >= nota_min) and
//       (b.getThreshold() > nota_max or b.getThreshold() < nota_min))
//     return true;
//   if ((a.getThreshold() > nota_max or a.getThreshold() < nota_min) and
//       (b.getThreshold() <= nota_max and b.getThreshold() >= nota_min))
//     return false;
//   return a.getThreshold() > b.getThreshold();
// }

// bool find_word(const string &a, const string &data) {
//   int size = a.size();
//   int i = 0;
//   for (int index = 0; index < size; ++index) {
//     if (data[i] == a[index])
//       ++i;
//     else
//       i = 0;
//     if (i == data.size())
//       return true;
//   }
//   return false;
// }

// bool find_in(const vector<Degree> &f, const Degree &c) {
//   for (int i = 0; i < f.size(); ++i) {
//     cout << "\033[2J\033[0;0H";
//     if (c.getCode() == f[i].getCode())
//       return true;
//   }
//   return false;
// }

// void filter(vector<Degree> &c, vector<string> &data, const string &order) {
//   vector<Degree> f;
//   string word;
//   int size = c.size();
//   for (int i = 0; i < size; ++i) {
//     if (order == "codi")
//       word = c[i].getCode();
//     else if (order == "name")
//       word = c[i].getName();
//     else if (order == "uni")
//       word = c[i].getUniversity();
//     else if (order == "space")
//       word = c[i].getCity();
//     for (int j = 0; j < data.size(); ++j) {
//       if (find_word(word, data[j]) and not find_in(f, c[i]))
//         f.push_back(c[i]);
//     }
//   }
//   c = f;
// }

// bool find_all_pond(const vector<int> &pond, const vector<int> &llist) {
//   for (int i = 0; i < llist.size(); ++i) {
//     cout << "\033[2J\033[0;0H";
//     if (pond[llist[i]] != '2')
//       return false;
//   }
//   return true;
// }

// bool find_two_pond(const vector<int> &pond, const vector<int> &llist) {
//   int count = 0;
//   for (int i = 0; i < llist.size(); ++i) {
//     cout << "\033[2J\033[0;0H";
//     if (pond[llist[i]] == '2')
//       ++count;
//     if (llist.size() == 1)
//       return count == 1;
//     else if (count == 2)
//       return true;
//   }
//   return false;
// }

// void filter_pond(vector<Degree> &degree, const string &data) {
//   pond_instruct();
//   cout << "data: " << data << endl;

//   vector<int> llist;
//   int pos;
//   cin >> pos;
//   while (pos != -1) {
//     llist.push_back(pos);
//     cout << endl;
//     cout << "it must finish witn '-1'😊" << endl;
//     cin >> pos;
//   }

//   vector<Degree> f;
//   for (int index = 0; index < degrees.getVector().size(); ++index) {
//     const Degree& c = degrees.getVector()[index];
//     if (find_all_pond(c.getCoefficients(), llist) and data == "all")
//       f.push_back(c);
//     else if (find_two_pond(c.getCoefficients(), llist) and data == "two")
//       f.push_back(c);
//   }
//   // cambi
//   // degrees = Degrees();
// }

// void console(vector<Degree> &c) {
//   instruct();
//   while (cin >> order) {
//     instruct();

//     cout << order << " ";
//     if (order == "instruct") {
//       instruct();
//       pond_instruct();
//     } else if (order == "clear") {
//       // write(degrees);
//       // c = degrees;
//     } else if (order == "codi" or order == "name" or order == "space" or
//                order == "uni") {
//       cin >> _data;
//       if (_data != "asc" and _data != "des") {
//         while (_data != "-1") {
//           v.push_back(_data);
//           cout << endl;
//           cout << "it must finish witn '-1'😊" << endl;
//           cin >> _data;
//         }
//         cout << "\033[2J\033[0;0H";
//         cout << order << " llist: ";
//         for (int i = 0; i < v.size(); ++i)
//           cout << v[i] << " ";
//         cout << endl;
//       }
//       if (_data == "asc" or _data == "des")
//         cout << _data << " " << endl;
//       if (order == "codi") {
//         if (_data == "asc")
//           sort(c.begin(), c.end(), cmp_codi_asc);
//         else if (_data == "des")
//           sort(c.begin(), c.end(), cmp_codi_des);
//         else
//           filter(c, v, order);
//       } else if (order == "name") {
//         if (_data == "asc")
//           sort(c.begin(), c.end(), cmp_name_asc);
//         else if (_data == "des")
//           sort(c.begin(), c.end(), cmp_name_des);
//         else
//           filter(c, v, order);
//       } else if (order == "space") {
//         if (_data == "asc")
//           sort(c.begin(), c.end(), cmp_space_asc);
//         else if (_data == "des")
//           sort(c.begin(), c.end(), cmp_space_des);
//         else
//           filter(c, v, order);
//       } else if (order == "uni") {
//         if (_data == "asc")
//           sort(c.begin(), c.end(), cmp_uni_asc);
//         else if (_data == "des")
//           sort(c.begin(), c.end(), cmp_uni_des);
//         else
//           filter(c, v, order);
//       }
//       write(c);
//     } else if (order == "pond") {
//       cin >> _data;
//       if (_data == "all" or _data == "two") {
//         filter_pond(c, _data);
//         write(c);
//       } else {
//         instruct();
//         cout << order << " " << _data << endl;
//         cout << "error data!" << endl;
//       }
//     } else if (order == "nota") {
//       cin >> _data;
//       if (_data == "asc")
//         sort(c.begin(), c.end(), cmp_nota_asc);
//       else if (_data == "des")
//         sort(c.begin(), c.end(), cmp_nota_des);
//       else if (_data == "interval") {
//         cout << endl;
//         cout << "max? min?" << endl;
//         cin >> nota_max >> nota_min;
//         sort(c.begin(), c.end(), cmp_nota_max);
//       }
//       if (_data == "asc" or _data == "des" or _data == "interval")
//         write(c);
//       else {
//         instruct();
//         cout << order << " " << _data << endl;
//         cout << "error data!" << endl;
//       }
//     } else {
//       instruct();
//       cout << order << endl;
//       cout << "error order!" << endl;
//     }
//   }
// }