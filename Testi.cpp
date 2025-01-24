//Markus Koski, Frans-Emil Vuori, Miika Musta

// muutos ja tämmä vikaa muutos testausta varten

#include <SFML/Graphics.hpp>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "2D Roguelike");

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();
        }

        window.clear();
        // Render game objects here
        window.display();
    }

    return 0;
}
