#include <QApplication>
#include "pni_pilot_core"

int main(int argc, char *argv[])
{
    // C++17 example: using a structured binding
    auto [appName, version] = std::make_pair("MyQt6App", "1.0.0");
    QApplication::setApplicationName(appName);
    QApplication::setApplicationVersion(version);
    
    QApplication a(argc, argv);

    // C++17 example: using a simple lambda with an 'if constexpr' internally
    MainWindow w;
    w.show();

    return a.exec();
}