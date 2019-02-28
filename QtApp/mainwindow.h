#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QtWidgets>
#include <QtCore>
#include <QtMultimedia>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_sliderProgress_sliderMoved(int position);

    void on_sliderVolume_sliderMoved(int position);

    void on_buttonPlay_clicked();

    void on_buttonStop_clicked();

    void on_positionChanged(qint64 position);

    void on_durationChanged(qint64 position);

    void onListWidgetItemClicked(QListWidgetItem* item);

private:
    Ui::MainWindow *ui;
    QTimeLine *tl;
    QMediaPlayer *player;
    QStringList imageNames;
    QStringList musicNames;
    QString currPath;
    void load_file_names();
    void fillWidgetList();
};

#endif // MAINWINDOW_H
