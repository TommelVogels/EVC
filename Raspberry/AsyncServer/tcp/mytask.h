#ifndef MYTASK_H
#define MYTASK_H

#include <QDebug>
#include <QObject>
#include <QRunnable>
#include "json.h"
#include "globaldefines.h"

class MyTask : public QObject, public QRunnable
{
    Q_OBJECT

public:
    MyTask(QString received, SystemState sysState);

signals:
    void Result(QByteArray rData);
    void UARTsend(QByteArray data, uint function = 0);
    void Verbose(uint level);
    void ChangeMode(uint mode);

    void MotorSignal(bool left, bool right, int l = 0, int r = 0);
    void TurretAngleSignal(bool horizontal, bool vertical, int h = 0, int v = 0);
    void MissileSignal(bool t1, bool t2, bool all = false);
    void LaserSignal(bool on);

protected:
    void run();

private:
    QVariantMap JSONcall;
    bool answer;
    SystemState system;

    void getError(uint error, QVariantMap &result);

    void processCall(QVariantMap json, QVariantMap &result);
    void getMethods(QVariantMap &result);
    void setMode(QVariantMap &params, QVariantMap &result);
    void busWrite(QVariantMap &params, QVariantMap &result);
    void setVerbose(QVariantList &params, QVariantMap &result);
    void getMode(QVariantMap &result);
    void setMotor(QVariantMap &params, QVariantMap &result);
    void setTurretAngle(QVariantMap &params, QVariantMap &result);
    void fireMissile(QVariantMap &params, QVariantMap &result);
    void setLaser(QVariantMap &params, QVariantMap &result);
    void finalize(QVariantMap &params, QVariantMap &result);
};

#endif // MYTASK_H
