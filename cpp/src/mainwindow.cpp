#include "mainwindow.hpp"
#include <QVBoxLayout>
#include <QWidget>
#include <QDebug> // For simple C++ style output

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
{
    // Set up the central widget and layout
    QWidget *centralWidget = new QWidget(this);
    QVBoxLayout *layout = new QVBoxLayout(centralWidget);

    // Initialize the button
    m_button = new QPushButton("Click Me (C++17 & Qt6)", centralWidget);
    layout->addWidget(m_button);
    
    setCentralWidget(centralWidget);
    setWindowTitle("Qt 6 C++17 App");
    
    // Connect the button's clicked signal to a custom slot
    // C++17/Qt 5.7+ connect syntax is often preferred:
    connect(m_button, &QPushButton::clicked, this, &MainWindow::handleButtonClick);
}

MainWindow::~MainWindow()
{
    // No need to explicitly delete m_button here, as it's a child of
    // centralWidget, which is automatically deleted when MainWindow is.
}

void MainWindow::handleButtonClick()
{
    // C++17 example: using an 'if' statement with an initializer
    if (int result = 42; result == 42) {
        qDebug() << "Button clicked! The C++17 magic number is:" << result;
    }

    // Qt's standard message box would be used in a real app
    m_button->setText("Thanks!");
}