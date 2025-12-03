#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton> // Example widget

// The Q_OBJECT macro is essential for Qt's signal/slot mechanism
// and requires the CMake property AUTOMOC ON.
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    // Example slot function declaration
    void handleButtonClick();

private:
    // A widget member
    QPushButton *m_button;
};

#endif // MAINWINDOW_H