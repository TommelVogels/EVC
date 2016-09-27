#ifndef MYQFRAME_H
#define MYQFRAME_H

#include <QObject>
#include <QFrame>
#include <QDebug>
#include <QMouseEvent>

struct range{
    int min;
    int max;
};

class MyQFrame : public QFrame
{
    Q_OBJECT
public:
    explicit MyQFrame(QWidget *parent = 0);
    void mouseMoveEvent(QMouseEvent *ev);
    void setEnabled(bool en);
    void setRange(int hmin, int hmax, int vmin, int vmax);

private:
    range vrange;
    range hrange;

signals:
    void mouseMoved(int x, int y);
    void verticalChanged(int v);
    void horizontalChanged(int h);



public slots:
};

#endif // MYQFRAME_H
