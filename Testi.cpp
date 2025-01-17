#include <iostream>

int main() {

    const int maara = 5;

    double lampo[maara];

    double yhteensa = 0.0;

    std::cout << "Anna 5 lämpöarvoa:\n";

    for (int i = 0; i < maara; ++i) {

        std::cout << "Lämpötila " << (i + 1) << ": ";

        std::cin >> lampo[i];

        yhteensa += lampo[i];
    }

    double keskiarvo = yhteensa / maara;

    std::cout << "Keskiarvo: " << keskiarvo << std::endl;

    return 0;
}