#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <vector>
#include <tuple>
#include <string>
#include <cassert>
#include <cstdlib>
#include <algorithm>
#include <iterator>
#include <numeric>
#include <limits>
#include <cstdint>
#include <stack>
#include <set>
#include <unordered_set>
#define _USE_MATH_DEFINES
#include <cmath>

using namespace std;

extern int rand_seed;

// --------------------------------------------------------------------------

// *Really* minimal PCG32 code / (c) 2014 M.E. O'Neill / pcg-random.org
// Licensed under Apache License 2.0 (NO WARRANTY, etc. see website)
typedef struct { uint64_t state;  uint64_t inc; } pcg32_random_t;

#define PCG32_INITIALIZER   { 0x853c49e6748fea9bULL, 0xda3e39cb94b95bdbULL }
static pcg32_random_t pcg32_global = PCG32_INITIALIZER;

uint32_t pcg32_random_r(pcg32_random_t* rng)
{
  uint64_t oldstate = rng->state;
  // Advance internal state
  rng->state = oldstate * 6364136223846793005ULL + (rng->inc|1);
  // Calculate output function (XSH RR), uses old state for max ILP
  uint32_t xorshifted = ((oldstate >> 18u) ^ oldstate) >> 27u;
  uint32_t rot = oldstate >> 59u;
  return (xorshifted >> rot) | (xorshifted << ((~rot + 1) & 31u));
}

uint32_t pcg32_random()
{
  return pcg32_random_r(&pcg32_global);
}

void pcg32_srandom_r(pcg32_random_t* rng, uint64_t initstate, uint64_t initseq)
{
  rng->state = 0U;
  rng->inc = (initseq << 1u) | 1u;
  pcg32_random_r(rng);
  rng->state += initstate;
  pcg32_random_r(rng);
}

void pcg32_srandom(uint64_t seed, uint64_t seq)
{
    pcg32_srandom_r(&pcg32_global, seed, seq);
}

//     Generate a uniformly distributed number, r, where 0 <= r < bound
uint32_t pcg32_boundedrand_r(pcg32_random_t* rng, uint32_t bound)
{
  uint32_t threshold = (0-bound) % bound;
  for (;;) {
    uint32_t r = pcg32_random_r(rng);
    if (r >= threshold)
      return r % bound;
  }
}

uint32_t pcg32_boundedrand(uint32_t bound)
{
  return pcg32_boundedrand_r(&pcg32_global, bound);
}

uint64_t pcg64_random()
{
  return (((uint64_t)pcg32_random()) << 32) | ((uint64_t)pcg32_random());
}

uint64_t pcg64_boundedrand(uint64_t bound)
{
  uint64_t threshold = (0-bound) % bound;
  for (;;) {
    uint64_t r = pcg64_random();
    if (r >= threshold)
      return r % bound;
  }
}

// --------------------------------------------------------------------------


int random_value(int i, int j) {
  return i + pcg32_boundedrand(j - i + 1);
}

long long random_value(long long i, long long j) {
  return i + pcg64_boundedrand(j - i + 1);
}

unsigned long random_value_ul(unsigned long i, unsigned long j) {
  return i + pcg32_boundedrand(j - i + 1);
}

unsigned long long random_value_ull(unsigned long long i, unsigned long long j) {
  return i + pcg64_boundedrand(j - i + 1);
}

double random_value(double i, double j) {
  double x = (double)pcg32_random() / (double)(numeric_limits<uint32_t>::max());
  return i + x * (j - i);
}

bool random_bool(int positive = 1, int total = 2) {
  return random_value(1, total) <= positive;
}

int random_around(int i, double percent = 0.2) {
  return random_value((int)round((1 - percent) * i),
		      (int)round((1 + percent) * i));
}

int random_around_up(int i, double percent = 0.2) {
  return random_value(i, (int)round((1 + percent) * i));
}

int random_around_down(int i, double percent = 0.2) {
  return random_value((int)round((1 - percent) * i), i);
}

int random_index(int n) {
  return random_value(0, n-1);
}

template <class T>
const T& random_element(const vector<T>& v) {
  return v[random_index(v.size())];
}

pair<int, int> random_pair(int i, int j, bool can_be_equal = false) {
  int a = random_value(i, j);
  int b;
  do {
    b = random_value(i, j);
  } while (!can_be_equal && a == b);
  return make_pair(a, b);
}

template <class T>
vector<T> random_array(int n, T min, T max) {
  vector<T> result(n);
  for (int i = 0; i < n; i++)
    result[i] = random_value(min, max);
  return result;
}

vector<unsigned long> random_array_ull(int n, unsigned long min, unsigned long max) {
  vector<unsigned long> result(n);
  for (int i = 0; i < n; i++)
    result[i] = random_value_ul(min, max);
  return result;
}

vector<unsigned long long> random_array_ull(int n, unsigned long long min, unsigned long long max) {
  vector<unsigned long long> result(n);
  for (int i = 0; i < n; i++)
    result[i] = random_value_ull(min, max);
  return result;
}

vector<int> random_sorted_array(int n, int min, int dmin, int dmax) {
  vector<int> result(n);
  result[0] = min;
  for (int i = 1; i < n; i++)
    result[i] = result[i-1] + random_value(dmin, dmax);
  return result;
}

vector<double> random_sorted_array(int n, double min, double dmin, double dmax) {
  vector<double> result(n);
  result[0] = min;
  for (int i = 1; i < n; i++)
    result[i] = result[i-1] + random_value(dmin, dmax);
  return result;
}

string random_string_alpha_(int from, int to, int numLetters = 26) {
  int n = random_value(from, to);
  string rez(n, ' ');
  for (int i = 0; i < n; i++)
    rez[i] = (random_value(0, 1) ? 'a' : 'A') + random_value(0, numLetters - 1);
  return rez;
}

string random_string_alpha(int n, int numLetters = 26) {
  return random_string_alpha_(n, n, numLetters);
}

string random_string_lower(int n, int numLetters = 26) {
  string rez(n, ' ');
  for (int i = 0; i < n; i++)
    rez[i] = 'a' + random_value(0, numLetters - 1);
  return rez;
}

string random_string_upper(int n, int numLetters = 26) {
  string rez(n, ' ');
  for (int i = 0; i < n; i++)
    rez[i] = 'A' + random_value(0, numLetters - 1);
  return rez;
}

string random_string_digits(int n, int numLetters = 10) {
  string rez(n, ' ');
  rez[0] = '0' + random_value(1, numLetters - 1);
  for (int i = 1; i < n; i++)
    rez[i] = '0' + random_value(0, numLetters - 1);
  return rez;
}

string random_sentence(int words_from = 2, int words_to = 10,
                       int word_length_from = 1, int word_length_to = 10) {
  int num_words = random_value(words_from, words_to);
  string rez;
  for (int i = 0; i < num_words; i++) {
    string word = random_string_lower(random_value(word_length_from, word_length_to));
    if (i == 0 || random_value(1, 4) == 1)
      word[0] = toupper(word[0]);
    rez += word;
    if (i == num_words - 1) {
      string interp = ".!?";
      rez += interp[random_value(0, 2)];
    } else {
      if (random_value(1, 5) == 1)
        rez += ",";
      rez += " ";
    }
  }
  return rez;
}

// random m-element subset of interval [a, b]
vector<int> random_subset(int m, int a, int b, bool sorted=false) {
  int n = b - a + 1;
  assert(0 <= m && m <= n);
  if (m < n/2) {
    unordered_set<int> included;
    while (included.size() < m) {
      int x;
      do {
        x = random_value(a, b);
      } while (included.count(x) > 0);
      included.insert(x);
    }
    vector<int> result(begin(included), end(included));
    if (!sorted)
      random_shuffle(begin(result), end(result), random_index);
    return result;
  } else {
    unordered_set<int> excluded;
    while (excluded.size() + m < n) {
      int x;
      do {
        x = random_value(a, b);
      } while (excluded.count(x) > 0);
      excluded.insert(x);
    }
    vector<int> result;
    result.reserve(m);
    for (int i = a; i <= b; i++)
      if (excluded.count(i) == 0)
        result.push_back(i);
    if (!sorted)
      random_shuffle(begin(result), end(result), random_index);
    return result;
  }
}


tuple<int, int, int> random_time() {
  return make_tuple(random_value(0, 23),
                    random_value(0, 59),
                    random_value(0, 59));
}

// provera da li je data godina prestupna
bool isLeap(int year) {
  // year je prestupna ako je deljiva sa 4 i nije deljiva sa 100,
  // ili ako je deljiva sa 400
  return (year % 4 == 0 && year % 100 != 0) || (year % 400) == 0;
}

// broj dana u datom mesecu date godine
int daysInMonth(int month, int year) {
  switch (month) {
    // januar, mart, maj, jul, avgust, oktobar, decembar
  case 1: case 3: case 5: case 7: case 8: case 10: case 12:
    return 31;
    // april, jun, septembar, novembar
  case 4: case 6: case 9: case 11:
    return 30;
    // februar
  case 2:
    return isLeap(year) ? 29 : 28;
  }
  return 0;
}

tuple<int, int, int> random_date(int yearFrom = 1900, int yearTo = 2100) {
  int y = random_value(yearFrom, yearTo);
  int m = random_value(1, 12);
  int d = random_value(1, daysInMonth(m, y));
  return make_tuple(y, m, d);
}

tuple<int, int, int> random_angle() {
  return make_tuple(random_value(0, 359),
                    random_value(0, 59),
                    random_value(0, 59));
}

////////////////////////////////////////////////////////////////////////////////

template <class T>
void print_array(const vector<T>& a, ostream& tin, bool doNotPrintSize = false) {
  if (!doNotPrintSize)
    tin << a.size() << endl;
  for (auto x : a)
    tin << x << endl;
}

void print_array(const vector<double>& a, ostream& tin, bool doNotPrintSize, int prec) {
  if (!doNotPrintSize)
    tin << a.size() << endl;
  for (int i = 0; i < a.size(); i++)
    tin << setprecision(prec) << fixed << showpoint << a[i] << endl;
}


template <class T>
void print_array_inline(const vector<T>& a, ostream& tin, bool doNotPrintSize = false) {
  if (!doNotPrintSize)
    tin << a.size() << endl;
  for (int i = 0; i < a.size(); i++) {
    tin << a[i];
    if (i != a.size() - 1)
      tin << " ";
  }
  tin << endl;
}

void print_array_inline(const vector<double>& a, ostream& tin, bool doNotPrintSize, int prec) {
  if (!doNotPrintSize)
    tin << a.size() << endl;
  for (int i = 0; i < a.size(); i++) {
    tin << setprecision(prec) << fixed << showpoint << a[i];
    if (i != a.size() - 1)
      tin << " ";
  }
  tin << endl;
}

////////////////////////////////////////////////////////////////////////////////

vector<int> sizes(int num_OK, int OK_size,
		  int num_TLE, int TLE_size) {
  vector<int> result;
  result.reserve(num_OK + num_TLE);
  for (int i = 0; i < num_OK; i++)
    result.push_back(random_around(OK_size, 0.2));
  for (int i = 0; i < num_TLE; i++)
    result.push_back(random_around_up(TLE_size, 0.2));
  return result;
}

vector<int> sizes_n(int num_OK, int num_TLE) {
  const int OK_size = 100;
  const int TLE_size = 20000;
  return sizes(num_OK, OK_size, num_TLE, TLE_size);
}

vector<int> sizes_n2(int num_OK, int num_TLE) {
  const int OK_size = 50;
  const int TLE_size = 2000;
  return sizes(num_OK, OK_size, num_TLE, TLE_size);
}

vector<int> sizes_n3(int num_OK, int num_TLE) {
  const int OK_size = 10;
  const int TLE_size = 100;
  return sizes(num_OK, OK_size, num_TLE, TLE_size);
}

vector<int> sizes_nlogn(int num_OK, int num_TLE) {
  const int OK_size = 100;
  const int TLE_size = 20000;
  return sizes(num_OK, OK_size, num_TLE, TLE_size);
}

////////////////////////////////////////////////////////////////////////////////

extern int test_count;

void gen_test(int i, ostream &tin); 

void gen_tests(const string& tests_name, const string& testcase_dir, int test_count, bool print_info) {
  for (int test_num = 1; test_num <= test_count; test_num++) {
    ofstream tin;
    stringstream buf;
    buf << setw(2) << setfill('0') << test_num;
    string file = testcase_dir + "/" + tests_name + "_" + buf.str();
    string inFile =  file + ".in";
    tin.open(inFile.c_str());
    if (print_info)
      cout << "INFO: generating test input " << test_num << "..." << endl;
    gen_test(test_num, tin);
    tin.close();
  }
}

// usage ./<tgen.exe> tests_name testcase_dir print_info
// generates:
//    testcase_dir/tests_name_01.in
//    ...
//    testcase_dir/tests_name_09.in
int main(int argc, char* argv[]) {
  ios_base::sync_with_stdio(false);
  pcg32_srandom(rand_seed, 12345);

  // default testcase_dir
  string testcase_dir = ".";
  // default tests_name is "test_01.in", "test_02.in", ...
  string tests_name = "test";
  // no info messages are printed by default
  bool print_info = false;
  
  if (argc > 1)
    tests_name = argv[1];
  if (argc > 2)
    testcase_dir = argv[2];
  if (argc > 3)
    print_info = true;

  gen_tests(tests_name, testcase_dir, test_count, print_info);
}
