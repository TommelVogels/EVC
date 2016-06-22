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

    void MotorSignal(bool left, bool right, int l = 0, int r = 0);
    void TurretAngleSignal(bool horizontal, bool vertical, int h = 0, int v = 0);
    void MissileSignal(bool t1, bool t2, bool all = false);
    void LaserSignal(bool on);

public slots:
    Q_SCRIPTABLE void push(const QByteArray &arg, const quint8 &commandID);
    Q_SCRIPTABLE QByteArray pop(void);

    Q_SCRIPTABLE void SetMotor(const bool &left, const bool &right, const int &l, const int &r);
    Q_SCRIPTABLE void setTurretAngle(const bool &horizontal, const bool &vertical, const int &h, const int &v);
    Q_SCRIPTABLE void fireMissile(const bool &t1, const bool &t2, const bool &all);
    Q_SCRIPTABLE void setLaser(const bool &on);

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
