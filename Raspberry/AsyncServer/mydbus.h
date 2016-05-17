#ifndef MYDBUS_H
#define MYDBUS_H

#include <QObject>
#include <QtDBus/QtDBus>

class MyDbus : public QObject
{
    Q_OBJECT
public:
    explicit MyDbus(QObject *parent = 0);

signals:

public slots:
    int test(QString str = "error");


};

#endif // MYDBUS_H
