#include "mainwindow.h"
#include "widget.h"
#include <QtWidgets>
#include <QtCore>

int main(int argc, char *argv[])
{
    QCoreApplication::addLibraryPath("./");
    QApplication app(argc, argv);
    MainWindow mainWindow;
    mainWindow.show();
    return app.exec();
}
