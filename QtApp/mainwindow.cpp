#include "widget.h"
#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    tl(new QTimeLine()),
    player(new QMediaPlayer(this))
{
    ui->setupUi(this);
    currPath = QDir::current().path();
//    qDebug() << currPath;
    load_file_names();
    fillWidgetList();

    tl->setCurveShape(QTimeLine::LinearCurve);
    QObject::connect(tl, &QTimeLine::valueChanged, [&](double v) {
        ui->imageWidget->setPosition(v*tl->duration(), tl->duration());
    });
    connect(player, &QMediaPlayer::positionChanged, this, &MainWindow::on_positionChanged);
    connect(player, &QMediaPlayer::durationChanged, this, &MainWindow::on_durationChanged);

    player->setNotifyInterval(6);
}

MainWindow::~MainWindow()
{
    delete ui;
    delete tl;
}

void MainWindow::load_file_names()
{
    QDir directory(currPath + "/images");
    imageNames = directory.entryList(QStringList() << "*.png", QDir::Files);
    directory.setPath(currPath + "/music");
    musicNames = directory.entryList(QStringList() << "*.mp3", QDir::Files);
}

void MainWindow::fillWidgetList()
{
    connect(ui->listWidget, SIGNAL(itemClicked(QListWidgetItem*)),
                this, SLOT(onListWidgetItemClicked(QListWidgetItem*)));

    if(imageNames.size() != musicNames.size())
        qDebug() << "image library size is not equal music library size";
    for(int i = 0; i < imageNames.size(); i++){
        QString url = currPath + "/images/" + imageNames[i];
        QPixmap px(url);
        QListWidgetItem *item = new QListWidgetItem(QIcon(px.scaled(120,120)),musicNames[i]);
        QVariant v;
        v.setValue(i);
        item->setData(Qt::UserRole, v);
        v = item->data(Qt::UserRole);
        ui->listWidget->addItem(item);
    }
    ui->listWidget->setIconSize(QSize(120,120));
}

void MainWindow::onListWidgetItemClicked(QListWidgetItem *item)
{
    on_buttonStop_clicked();
    QVariant v = item->data(Qt::UserRole);
    int fileNr = v.value<int>();
    QString url = currPath + "/images/" + imageNames[fileNr];
    QPixmap px(url);
    ui->imageWidget->setPixmap(px.scaled(400,400));
    player->setMedia(QUrl::fromLocalFile(currPath + "/music/" + musicNames[fileNr]));
    ui->imageWidget->update();

}

void MainWindow::on_sliderProgress_sliderMoved(int position)
{
    player->setPosition(position);
    tl->setPaused(true);
    tl->setCurrentTime(int(position));
    tl->setPaused(false);
}

void MainWindow::on_sliderVolume_sliderMoved(int position)
{
    player->setVolume(position);
}

void MainWindow::on_buttonPlay_clicked()
{
    tl->setDuration(int(player->duration()));
    player->play();
    tl->start();
//    qDebug() << player->errorString();
}

void MainWindow::on_buttonStop_clicked()
{
    player->stop();
    tl->stop();
    tl->setCurrentTime(0);
}

void MainWindow::on_positionChanged(qint64 position)
{
    ui->sliderProgress->setValue(int(position));
}

void MainWindow::on_durationChanged(qint64 position)
{
    ui->sliderProgress->setMaximum(int(position));
}

