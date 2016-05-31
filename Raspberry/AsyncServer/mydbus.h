#ifndef MYDBUS_H
#define MYDBUS_H

#include <QObject>
#include <QtDBus/QtDBus>
#include "globaldefines.h"

class Dbus_ext: public QObject
{
    Q_OBJECT
signals:
    void busWrite(QByteArray data, int function = 0);
    void busRead(QByteArray data);
public slots:
    Q_SCRIPTABLE QString push(const QString &arg);
    Q_SCRIPTABLE QString pop(const QString &arg);
};

class MyDbus : public QObject
{
    Q_OBJECT
public:
    explicit MyDbus(QObject *parent = 0);
    void push(QByteArray &data);

    Dbus_ext ext;

public slots:
    int test(QString str = "error");
};

#endif // MYDBUS_H
