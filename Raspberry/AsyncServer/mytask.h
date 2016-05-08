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
    MyTask(QString received);

signals:
    void Result(QByteArray rData);
    void UARTsend(QByteArray data);

protected:
    void run();

private:
    QVariantMap JSONcall;
    QVariantMap JSONresult;
    QVariantMap paramsJSON;
    QVariantMap robjJSON;
    bool answer;

    void processCall();
    void setMode();
    QVariantMap busWrite();
    void setVerbose();
    QVariantMap getCurrent();
    void getMode();
    void setMotor();
    void setTurretAngle();
    void fireMissile();
    void setLaser();
    void finalize();
};

#endif // MYTASK_H
