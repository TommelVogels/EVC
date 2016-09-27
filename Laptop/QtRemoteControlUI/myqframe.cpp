#include "myqframe.h"

MyQFrame::MyQFrame(QWidget *parent) : QFrame(parent)
{
    qDebug() << "hello there";
    vrange = {0, 90};
    hrange = {0, 180};
}

void MyQFrame::setEnabled(bool en)
{
    QFrame::setEnabled(en);
    QPalette p = this->palette();
    QColor c = p.color(QPalette::Background);

    c.setAlpha((en?255:100));

    p.setColor(QPalette::Background,c);
    this->setPalette(p);

}

void MyQFrame::setRange(int hmin, int hmax, int vmin, int vmax)
{
    vrange = {vmin,vmax};
    hrange = {hmin, hmax};
}

void MyQFrame::mouseMoveEvent(QMouseEvent *ev)
{
    int evx = ev->x();
    int evy = ev->y();
    int width = this->width();
    int height = this->height();

    if(evx < 0 || evy < 0 || evx > width || evy > height)
        return;

    float revx = evx/(float)width;
    float revy = evy/(float)height;

    // horizontal
    int a_h = hrange.max - hrange.min;
    int b_h = hrange.min;
    int horizontal = revx*a_h + b_h;
    emit horizontalChanged(horizontal);

    // vertical
    int a_v = vrange.max - vrange.min;
    int b_v = vrange.min;
    int vertical = vrange.max - revy*a_v + b_v;
    emit verticalChanged(vertical);

    // horizontal & vertical
    emit mouseMoved(horizontal,vertical);
}
