#include <QDebug>
//#include <QTimer>
//#include <QPoint>
//#include <QHoverEvent>
#include "myqframe.h"
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "json.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    ui->TurretFrame->setRange(  ui->horizontalSlider_TurretH->minimum(),
                                ui->horizontalSlider_TurretH->maximum(),
                                ui->verticalSlider_TurretV->minimum(),
                                ui->verticalSlider_TurretV->maximum());

    connect(ui->checkBox_autonomous,SIGNAL(toggled(bool)),this,SLOT(changeMode(bool)));

    connect(ui->verticalSlider_left,SIGNAL(valueChanged(int)),this,SLOT(leftChanged(int)));
    connect(ui->verticalSlider_right,SIGNAL(valueChanged(int)),this,SLOT(rightChanged(int)));
    connect(ui->verticalSlider_speed,SIGNAL(valueChanged(int)),this,SLOT(speedChanged(int)));
    connect(ui->dial,SIGNAL(valueChanged(int)),this,SLOT(dialChanged(int)));
    connect(ui->pushButton_flipLaser,SIGNAL(clicked(bool)),this,SLOT(flipLaser(bool)));
    connect(ui->pushButton_resetSpeed,SIGNAL(clicked(bool)),this,SLOT(resetSpeed(bool)));
    connect(ui->pushButton_Straight,SIGNAL(clicked(bool)),this,SLOT(goStraight(bool)));
    connect(ui->TurretFrame,SIGNAL(mouseMoved(int,int)),this,SLOT(turretAngle(int,int)));
    connect(ui->pushButton_fireSingleT1,SIGNAL(clicked(bool)),this,SLOT(fireSingleT1(bool)));
    connect(ui->pushButton_fireSingleT2,SIGNAL(clicked(bool)),this,SLOT(fireSingleT2(bool)));
    connect(ui->pushButton_fireAllT1,SIGNAL(clicked(bool)),this,SLOT(fireAllT1(bool)));
    connect(ui->pushButton_fireAllT2,SIGNAL(clicked(bool)),this,SLOT(fireAllT2(bool)));
    connect(ui->pushButton_Nuke,SIGNAL(clicked(bool)),this,SLOT(fireAllT12(bool)));

    connect(ui->checkBox_Mode,SIGNAL(toggled(bool)),this,SLOT(verboseChanged(bool)));
    connect(ui->checkBox_Motor,SIGNAL(toggled(bool)),this,SLOT(verboseChanged(bool)));
    connect(ui->checkBox_turretAngle,SIGNAL(toggled(bool)),this,SLOT(verboseChanged(bool)));
    connect(ui->checkBox_laser,SIGNAL(toggled(bool)),this,SLOT(verboseChanged(bool)));
    connect(ui->checkBox_missile,SIGNAL(toggled(bool)),this,SLOT(verboseChanged(bool)));

    connect(ui->verticalSlider_TurretV,SIGNAL(valueChanged(int)),this,SLOT(turretVChanged(int)));
    connect(ui->horizontalSlider_TurretH,SIGNAL(valueChanged(int)),this,SLOT(turretHChanged(int)));

    socket = new MySocket(this);
    connect(ui->pushButton_Connect,SIGNAL(clicked(bool)),this,SLOT(connectToPi(bool)));
    connect(socket->socket,SIGNAL(connected()),this,SLOT(connected()));
    connect(socket,SIGNAL(receivedData(QByteArray)),this,SLOT(dumpData(QByteArray)));
    connect(socket,SIGNAL(disconnectSignal()),this,SLOT(socketDisconnected()));

    QList<QWidget*> widgets = findChildren<QWidget*>();
    foreach (QWidget* widget, widgets)
        widget->installEventFilter(this);
}

bool MainWindow::eventFilter( QObject *, QEvent *e )
{
    if ( e->type() == QEvent::KeyPress ) {
        // special processing for key press
        QKeyEvent *k = (QKeyEvent *)e;

        if(!socket->connected)
            return false;

        switch(k->key())
        {
        case Qt::Key_Space:
            goStraight(true);
            return true;
        case Qt::Key_W:
            ui->verticalSlider_speed->setValue(
                        ui->verticalSlider_speed->value()+5);
            return true;
        case Qt::Key_A:
            ui->dial->setValue(
                        ui->dial->value()-30);
            return true;
        case Qt::Key_S:
            ui->verticalSlider_speed->setValue(
                        ui->verticalSlider_speed->value()-5);
            return true;
        case Qt::Key_D:
            ui->dial->setValue(
                        ui->dial->value()+30);
            return true;
        case Qt::Key_Up:
            ui->verticalSlider_TurretV->setValue(
                    ui->verticalSlider_TurretV->value()+5);
            return true;
        case Qt::Key_Left:
            ui->horizontalSlider_TurretH->setValue(
                    ui->horizontalSlider_TurretH->value()-5);
            return true;
        case Qt::Key_Down:
            ui->verticalSlider_TurretV->setValue(
                    ui->verticalSlider_TurretV->value()-5);
            return true;
        case Qt::Key_Right:
            ui->horizontalSlider_TurretH->setValue(
                    ui->horizontalSlider_TurretH->value()+5);
            return true;
        default:
            return false;
        }
    } else {
        // standard event processing
        return false;
    }
}

void MainWindow::turretAngle(int h, int v)
{
    ui->horizontalSlider_TurretH->blockSignals(true);
    ui->verticalSlider_TurretV->blockSignals(true);
    ui->horizontalSlider_TurretH->setValue(h);
    ui->verticalSlider_TurretV->setValue(v);
    ui->horizontalSlider_TurretH->blockSignals(false);
    ui->verticalSlider_TurretV->blockSignals(false);

    turretDataChanged(true, true);
}

void MainWindow::turretHChanged(int)
{
    turretDataChanged(true, false);
}

void MainWindow::turretVChanged(int)
{
    turretDataChanged(false, true);
}

void MainWindow::verboseChanged(bool)
{
    if(!socket->connected)
        return;

    qDebug() << "going to send the verbosity";

    QVariantMap json;
    QVariantList params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "System.SetVerbose";

    if(ui->checkBox_Mode->checkState()) params.append("mode");
    if(ui->checkBox_Motor->checkState()) params.append("motorSpeed");
    if(ui->checkBox_missile->checkState()) params.append("turretMissile");
    if(ui->checkBox_turretAngle->checkState()) params.append("turretAngle");
    if(ui->checkBox_laser->checkState()) params.append("laser");

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::changeMode(bool val)
{
    QVariantMap json;
    QVariantMap params;
    json["jsonrpc"] = "2.0";
    json["id"] = "mode";
    json["method"] = "System.SetMode";
    params["mode"] = val ? "autonomous" : "manual";
    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::connected()
{
    ui->verticalSlider_TurretV->setEnabled(true);
    ui->horizontalSlider_TurretH->setEnabled(true);
    ui->TurretFrame->setEnabled(true);
    ui->checkBox_autonomous->setEnabled(true);
    ui->pushButton_fireAllT1->setEnabled(true);
    ui->pushButton_fireAllT2->setEnabled(true);
    ui->pushButton_fireSingleT1->setEnabled(true);
    ui->pushButton_fireSingleT2->setEnabled(true);
    ui->pushButton_flipLaser->setEnabled(true);
    ui->pushButton_Nuke->setEnabled(true);
    ui->pushButton_resetSpeed->setEnabled(true);
    ui->pushButton_Straight->setEnabled(true);
    ui->pushButton_Connect->setEnabled(false);
    ui->lineEdit_ipaddress->setEnabled(false);
    ui->lineEdit_port->setEnabled(false);

    socket->connected = true;
    verboseChanged(true);

    QVariantMap json;
    json["jsonrpc"] = "2.0";
    json["id"] = "mode";
    json["method"] = "System.GetMode";

    socket->writeBytes(QtJson::serialize(json));
}

void MainWindow::motorDataChanged(bool left, bool right)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Motor.SetMotor";

    if(left)  params["left"] = this->left;
    if(right) params["right"] = this->right;

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::turretDataChanged(bool h, bool v)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.SetAngle";

    if(h) params["horizontal"] = ui->horizontalSlider_TurretH->value();
    if(v) params["vertical"] = ui->verticalSlider_TurretV->value();

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setSteeringEnabled(bool enabled)
{
    ui->verticalSlider_left->setEnabled(enabled);
    ui->verticalSlider_right->setEnabled(enabled);
    ui->verticalSlider_speed->setEnabled(enabled);
    ui->dial->setEnabled(enabled);

    ui->checkBox_autonomous->blockSignals(true);
    ui->checkBox_autonomous->setChecked(!enabled);
    ui->checkBox_autonomous->blockSignals(false);
}

void MainWindow::connectToPi(bool)
{
    socket->connectToPi(ui->lineEdit_ipaddress->text(),
                        ui->lineEdit_port->text().toInt());
}

void MainWindow::leftChanged(int left)
{
    int diff = left - right;
    int tot = left + right;

    ui->dial->blockSignals(true);
    ui->verticalSlider_speed->blockSignals(true);
    ui->dial->setValue(diff);
    ui->verticalSlider_speed->setValue(tot);
    ui->dial->blockSignals(false);
    ui->verticalSlider_speed->blockSignals(false);

    this->left = left;
    this->dial = diff;
    this->speed = tot;

    motorDataChanged(true, false);
}

void MainWindow::rightChanged(int right)
{
    qDebug() << "R";
    int diff = left - right;
    int tot = left + right;

    ui->dial->blockSignals(true);
    ui->verticalSlider_speed->blockSignals(true);
    ui->dial->setValue(diff);
    ui->verticalSlider_speed->setValue(tot);
    ui->dial->blockSignals(false);
    ui->verticalSlider_speed->blockSignals(false);

    this->right = right;
    this->dial = diff;
    this->speed = tot;

    motorDataChanged(false, true);
}

void MainWindow::speedChanged(int speed)
{
    qDebug() << "S";
    // new values: left + right = new speed
    //             left - right = old dial

    int newLeft = (speed + dial)/2;
    int newRight = (speed - dial)/2;

    if  (newLeft  >  255 ||
         newLeft  < -255 ||
         newRight >  255 ||
         newRight < -255)
    {
        ui->verticalSlider_speed->setValue(this->speed);
        return;
    }

    ui->verticalSlider_left->blockSignals(true);
    ui->verticalSlider_right->blockSignals(true);
    ui->verticalSlider_left->setValue(newLeft);
    ui->verticalSlider_right->setValue(newRight);
    ui->verticalSlider_left->blockSignals(false);
    ui->verticalSlider_right->blockSignals(false);

    this->left = newLeft;
    this->right = newRight;
    this->speed = speed;

    motorDataChanged(true,true);
}

void MainWindow::dialChanged(int dial)
{
    // new values: left + right = old speed
    //             left - right = new dial

    int newLeft = (speed + dial)/2;
    int newRight = (speed - dial)/2;

    if  (newLeft  >  255 ||
         newLeft  < -255 ||
         newRight >  255 ||
         newRight < -255)
    {
        ui->dial->setValue(this->dial);
        return;
    }

    ui->verticalSlider_left->blockSignals(true);
    ui->verticalSlider_right->blockSignals(true);
    ui->verticalSlider_left->setValue(newLeft);
    ui->verticalSlider_right->setValue(newRight);
    ui->verticalSlider_left->blockSignals(false);
    ui->verticalSlider_right->blockSignals(false);

    this->left = newLeft;
    this->right = newRight;
    this->dial = dial;

    motorDataChanged(true,true);
}

void MainWindow::resetSpeed(bool)
{
    ui->verticalSlider_left->blockSignals(true);
    ui->verticalSlider_right->blockSignals(true);
    ui->verticalSlider_speed->blockSignals(true);
    ui->dial->blockSignals(true);
    ui->verticalSlider_left->setValue(0);
    ui->verticalSlider_right->setValue(0);
    ui->verticalSlider_speed->setValue(0);
    ui->dial->setValue(0);

    this->left = 0;
    this->right = 0;
    this->speed = 0;
    this->dial = 0;

    ui->verticalSlider_left->blockSignals(false);
    ui->verticalSlider_right->blockSignals(false);
    ui->verticalSlider_speed->blockSignals(false);
    ui->dial->blockSignals(false);

    motorDataChanged(true,true);
}

void MainWindow::goStraight(bool)
{
    ui->verticalSlider_left->blockSignals(true);
    ui->verticalSlider_right->blockSignals(true);
    ui->verticalSlider_speed->blockSignals(true);
    ui->dial->blockSignals(true);

    qDebug() << this->speed << floor(this->speed/2);

    int newVal = floor(this->speed/2);

    ui->verticalSlider_left->setValue(newVal);
    ui->verticalSlider_right->setValue(newVal);
    ui->dial->setValue(0);

    this->left = newVal;
    this->right = newVal;
    this->dial = 0;

    ui->verticalSlider_left->blockSignals(false);
    ui->verticalSlider_right->blockSignals(false);
    ui->verticalSlider_speed->blockSignals(false);
    ui->dial->blockSignals(false);

    motorDataChanged(true,true);
}

void MainWindow::fireSingleT1(bool)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.FireMissile";

    params["turret"] = 1;
    params["amount"] = "one";

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::fireSingleT2(bool)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.FireMissile";

    params["turret"] = 2;
    params["amount"] = "one";

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::fireAllT1(bool)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.FireMissile";

    params["turret"] = 1;
    params["amount"] = "all";

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::fireAllT2(bool)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.FireMissile";

    params["turret"] = 2;
    params["amount"] = "all";

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::fireAllT12(bool)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.FireMissile";

    params["turret"] = 12;
    params["amount"] = "all";

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

bool laser = false;
void MainWindow::flipLaser(bool)
{
    QVariantMap json, params;
    json["jsonrpc"] = "2.0";
    json["id"] = "-";
    json["method"] = "Turret.SetLaser";

    if(laser)  params["on"] = "true";
    else params["on"] = "false";

    laser = !laser;

    json["params"] = params;
    bool success;
    socket->writeBytes(QtJson::serialize(json,success));
}

void MainWindow::socketDisconnected()
{
    ui->TurretFrame->setEnabled(false);
    ui->verticalSlider_TurretV->setEnabled(false);
    ui->horizontalSlider_TurretH->setEnabled(false);
    ui->verticalSlider_left->setEnabled(false);
    ui->verticalSlider_right->setEnabled(false);
    ui->verticalSlider_speed->setEnabled(false);
    ui->dial->setEnabled(false);
    ui->verticalSlider_TurretV->setEnabled(false);
    ui->horizontalSlider_TurretH->setEnabled(false);
    ui->checkBox_autonomous->setEnabled(false);
    ui->pushButton_fireAllT1->setEnabled(false);
    ui->pushButton_fireAllT2->setEnabled(false);
    ui->pushButton_fireSingleT1->setEnabled(false);
    ui->pushButton_fireSingleT2->setEnabled(false);
    ui->pushButton_flipLaser->setEnabled(false);
    ui->pushButton_Nuke->setEnabled(false);
    ui->pushButton_resetSpeed->setEnabled(false);
    ui->pushButton_Straight->setEnabled(false);
    ui->pushButton_Connect->setEnabled(true);
    ui->lineEdit_ipaddress->setEnabled(true);
    ui->lineEdit_port->setEnabled(true);
}

void MainWindow::dumpData(QByteArray data)
{
    qDebug() << "data:" << data;

    QVariantMap json = QtJson::parse(data).toMap();
    QString source = json["source"].toString();

    if(json["id"].toString() == "mode")
    {
        if(json["result"].toString() == "manual")
        {
            qDebug() << "manual";
            setSteeringEnabled(true);
        }
        else if(json["result"].toString() == "autonomous")
        {
            qDebug() << "auto";
            setSteeringEnabled(false);
        }
        return;
    }

    QString id = json["id"].toString();
    if(id.isEmpty() || id.isNull())
    {
        qDebug() << "notification:" << data;
        QString method = json["method"].toString();
        if(method == "System.SetMode")
        {
            if(json["mode"].toString() == "manual")
            {
                setSteeringEnabled(true);
            }
            else if(json["mode"].toString() == "autonomous")
            {
                setSteeringEnabled(false);
            }
        }
        else if(method == "Motor.SetMotor")
        {
            QString ls = json["left"].toString();
            QString rs = json["right"].toString();

            ui->verticalSlider_left->blockSignals(true);
            ui->verticalSlider_right->blockSignals(true);
            ui->dial->blockSignals(true);
            ui->verticalSlider_speed->blockSignals(true);

            if(!ls.isEmpty())
            {
                this->left = ls.toInt();
                ui->verticalSlider_left->setValue(this->left);
            }
            if(!rs.isEmpty())
            {
                this->right = rs.toInt();
                ui->verticalSlider_right->setValue(this->right);
            }

            this->dial = left - right;
            this->speed = left + right;
            ui->dial->setValue(this->dial);
            ui->verticalSlider_speed->setValue(this->speed);

            ui->dial->blockSignals(false);
            ui->verticalSlider_speed->blockSignals(false);
            ui->verticalSlider_left->blockSignals(false);
            ui->verticalSlider_right->blockSignals(false);

            qDebug() << "speeds:" << ls << rs;

        }
        else if(method == "Turret.SetAngle")
        {
            QString hs = json["horizontal"].toString();
            QString vs = json["vertical"].toString();

            ui->verticalSlider_TurretV->blockSignals(true);
            ui->horizontalSlider_TurretH->blockSignals(true);

            if(!hs.isEmpty()) ui->horizontalSlider_TurretH->setValue(hs.toInt());
            if(!vs.isEmpty()) ui->verticalSlider_TurretV->setValue(vs.toInt());

            ui->verticalSlider_TurretV->blockSignals(false);
            ui->horizontalSlider_TurretH->blockSignals(false);
        }
    }

    if(source.isEmpty() || source.isNull())
        return;

    if(source == "UART")
    {
        QString direction = json["direction"].toString();

        ui->textEdit->moveCursor (QTextCursor::End);
        ui->textEdit->insertHtml("<b><u>UART<\\u><\\b>");
        ui->textEdit->insertHtml(":");
        ui->textEdit->insertPlainText("\t");
        if(direction == "RA")
        {
            ui->textEdit->insertHtml("<b>Direction<\\b>");
            ui->textEdit->insertHtml(": ");
            ui->textEdit->insertHtml("<i>R <\\i>");
            ui->textEdit->insertHtml(" --> A");
            ui->textEdit->insertPlainText("\t");
            ui->textEdit->insertHtml("<b>Method: <\\b>");
            ui->textEdit->insertHtml(json["method"].toString());
            ui->textEdit->insertPlainText("\t");
            ui->textEdit->insertHtml("<b>Data: <\\b>");
            ui->textEdit->insertHtml(json["data"].toString());
        }
        else if(direction == "AR") ui->textEdit->insertHtml("<b>Direction: A<\\b> --> R");
        ui->textEdit->insertPlainText("\n");
        ui->textEdit->moveCursor (QTextCursor::End);
    }
}