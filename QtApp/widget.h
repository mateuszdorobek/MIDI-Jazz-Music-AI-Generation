#ifndef WIDGET_H
#define WIDGET_H

#include <QtWidgets>

class Widget : public QWidget
{
    Q_OBJECT

public:
    Widget(QWidget *parent = 0);
    ~Widget();
    QSize sizeHint() const;
    void setPixmap(const QPixmap &px);
    void setPosition(double p, double d);
protected:
    void paintEvent(QPaintEvent*);
private:
    QPixmap m_px;
    double m_pos = 0.0;
    double m_dur = 0.0;
};

#endif // WIDGET_H
