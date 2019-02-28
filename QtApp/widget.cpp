#include "widget.h"
#include <QPainter>

Widget::Widget(QWidget *parent)
    : QWidget(parent)
{
}

Widget::~Widget()
{

}

QSize Widget::sizeHint() const {
    return m_px.size();

}

void Widget::setPixmap(const QPixmap &px) {
    m_px = px;
    updateGeometry();
}

void Widget::setPosition(double p, double d)
{
    m_pos = p;
    m_dur = d;
    update();
}

void Widget::paintEvent(QPaintEvent *) {
    std::printf("%f",m_pos);
    QPainter p(this);
    p.drawPixmap(0, 0, m_px);
    if (m_dur >= 0) {
        p.setPen(Qt::green);
        const auto offset = m_pos / m_dur * width();
        p.drawLine(int(offset), 0, int(offset), height());
    }
}
