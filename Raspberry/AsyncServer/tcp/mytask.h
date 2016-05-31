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
    MyTask(QString received, uint mode);

signals:
    void Result(QByteArray rData);
    void UARTsend(QByteArray data, uint function = 0);
    void Verbose(uint level);
    void Mode(uint mode);

protected:
    void run();

private:
    QVariantMap JSONcall;
    bool answer;
    uint mode;

    void processCall(QVariantMap json, QVariantMap &result);
    void getMethods(QVariantMap &result);
    void setMode(QVariantMap &params, QVariantMap &result);
    void busWrite(QVariantMap &params, QVariantMap &result);
    void setVerbose(QVariantMap &params, QVariantMap &result);
    void getCurrent(QVariantMap &result);
    void getMode(QVariantMap &result);
    void setMotor(QVariantMap &params, QVariantMap &result);
    void setTurretAngle(QVariantMap &params, QVariantMap &result);
    void fireMissile(QVariantMap &params, QVariantMap &result);
    void setLaser(QVariantMap &params, QVariantMap &result);
    void finalize(QVariantMap &params, QVariantMap &result);
};

#endif // MYTASK_H
