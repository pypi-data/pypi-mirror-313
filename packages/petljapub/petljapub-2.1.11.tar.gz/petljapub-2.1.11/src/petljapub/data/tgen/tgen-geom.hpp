// tacka je zadata svojim dvema koordinatama
struct Tacka {
  int x, y;
  Tacka(int x_ = 0, int y_ = 0) {
    x = x_; y = y_;
  }
};

enum Orijentacija { POZITIVNA, NEGATIVNA, KOLINEARNE };

Orijentacija orijentacija(const Tacka& t0, const Tacka& t1, const Tacka& t2) {
  long long d = (long long)(t1.x-t0.x)*(long long)(t2.y-t0.y) - (long long)(t2.x-t0.x)*(long long)(t1.y-t0.y);
  if (d > 0)
    return POZITIVNA;
  else if (d < 0)
    return NEGATIVNA;
  else
    return KOLINEARNE;
}

long long kvadratRastojanja(const Tacka& t1, const Tacka& t2) {
  int dx = t1.x - t2.x, dy = t1.y - t2.y;
  return dx*dx + dy*dy;
}

void prostMnogougao(vector<Tacka>& tacke) {
  // trazimo tacku sa maksimalnom x koordinatom,
  // u slucaju da ima vise tacaka sa maksimalnom x koordinatom
  // biramo onu sa najmanjom y koordinatom
  auto max = max_element(begin(tacke), end(tacke),
                         [](const Tacka& t1, const Tacka& t2) {
                           return t1.x < t2.x ||
                                  (t1.x == t2.x && t1.y > t2.y);
                         });
  // dovodimo je na početak niza - ona predstavlja centar kruga
  swap(*begin(tacke), *max);
  const Tacka& t0 = tacke[0];

  // sortiramo ostatak niza (tačke sortiramo na osnovu ugla koji
  // zaklapaju u odnosu vertikalnu polupravu koja polazi naviše iz
  // centra kruga), a kolinearne na osnovu rastojanja od centra kruga
  sort(next(begin(tacke)), end(tacke),
       [t0](const Tacka& t1, const Tacka& t2) {
         Orijentacija o = orijentacija(t0, t1, t2);
         if (o == KOLINEARNE)
           return kvadratRastojanja(t0, t1) <= kvadratRastojanja(t0, t2);
         return o == POZITIVNA;
       });

  // obrcemo redosled tacaka na poslednjoj pravoj
  auto it = prev(end(tacke));
  while (orijentacija(*prev(it), *it, t0) == KOLINEARNE)
    it = prev(it);
  reverse(it, end(tacke));
}

void konveksniOmotac(vector<Tacka>& tacke,
                     vector<Tacka>& omotac) {
  prostMnogougao(tacke);
  omotac.push_back(tacke[0]);
  omotac.push_back(tacke[1]);
  for (int i = 2; i < tacke.size(); i++) {
    while (omotac.size() >= 2 &&
           orijentacija(omotac[omotac.size()-2], omotac[omotac.size()-1], tacke[i]) != POZITIVNA) {
      omotac.pop_back();
    }
    omotac.push_back(tacke[i]);
  }
}
