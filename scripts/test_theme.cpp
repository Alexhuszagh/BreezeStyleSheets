/**
 *  Example to test our theme detection works at the C++ level.
*/

#include <iostream>
#include "../example/detect/system_theme.hpp"

int main()
{
    std::cout << "Theme: " << static_cast<int>(breeze_stylesheets::get_theme()) << std::endl;
    std::cout << "Is Dark: " << breeze_stylesheets::is_dark() << std::endl;
    std::cout << "Is Light: " << breeze_stylesheets::is_light() << std::endl;

    return 0;
}
