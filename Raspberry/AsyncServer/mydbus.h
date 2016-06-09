#ifndef MYDBUS_H
#define MYDBUS_H

#include <QObject>
#include <QtDBus/QtDBus>
#include "globaldefines.h"

class Dbus_ext: public QObject
{
    Q_OBJECT
signals:
    void busWrite(QByteArray data, uint function = 0);
    void busRead(QByteArray data);
public slots:
    Q_SCRIPTABLE QByteArray push(const QByteArray &arg, const QByteArray &commandID);
    Q_SCRIPTABLE QByteArray pop(void);
};

class MyDbus : public QObject
{
    Q_OBJECT
public:
    explicit MyDbus(QObject *parent = 0);
    Dbus_ext ext;

public slots:
};

#endif // MYDBUS_H
