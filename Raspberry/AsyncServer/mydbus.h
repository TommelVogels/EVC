#ifndef MYDBUS_H
#define MYDBUS_H

#include <QObject>
#include <QtDBus/QtDBus>
#include "globaldefines.h"

class Dbus_ext: public QObject
{
    Q_OBJECT
public slots:
    Q_SCRIPTABLE QString push(const QString &arg);
    Q_SCRIPTABLE QString pop(const QString &arg);
};

class MyDbus : public QObject
{
    Q_OBJECT
public:
    explicit MyDbus(QObject *parent = 0);

signals:

public slots:
    int test(QString str = "error");

protected:
    Dbus_ext ext;


};

#endif // MYDBUS_H
