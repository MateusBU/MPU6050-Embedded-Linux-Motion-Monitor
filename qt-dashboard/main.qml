
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    id: window

    width: 640
    height: 480
    visible: true
    title: qsTr("MPU6050 Motion Monitor")

    property double roll: 0.0
    property double pitch: 0.0
    property bool isStarted: false

    // Simulates sensor readings for now
    function updateReadings() {
        roll = (Math.random() * 90 - 45).toFixed(2)
        pitch = (Math.random() * 90 - 45).toFixed(2)
    }

    Timer {
        id: periodicTimer
        interval: 500
        repeat: true

        onTriggered: {
            updateReadings()
        }
    }

    Label {
        id: titleLabel

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 50

        font.pixelSize: 28
        font.bold: true
        text: "MPU6050 Motion Monitor"
    }

    Row {
        id: readingsRow

        anchors.centerIn: parent
        spacing: 30

        // ROLL
        Rectangle {
            width: 220
            height: 130

            color: "transparent"
            border.color: "black"
            border.width: 2
            radius: 8

            Column {
                anchors.centerIn: parent
                spacing: 10

                Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "ROLL"
                    font.pixelSize: 22
                }

                Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: roll + "°"
                    font.pixelSize: 36
                    font.bold: true
                }
            }
        }

        // PITCH
        Rectangle {
            width: 220
            height: 130

            color: "transparent"
            border.color: "black"
            border.width: 2
            radius: 8

            Column {
                anchors.centerIn: parent
                spacing: 10

                Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "PITCH"
                    font.pixelSize: 22
                }

                Label {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: pitch + "°"
                    font.pixelSize: 36
                    font.bold: true
                }
            }
        }
    }

    Row {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: readingsRow.bottom
        anchors.topMargin: 40
        spacing: 30

        Button {
            text: isStarted ? "Stop" : "Start"
            font.pixelSize: 20

            onClicked: {
                if (!isStarted) {
                    isStarted = true
                    periodicTimer.start()
                    updateReadings()
                } else {
                    isStarted = false
                    periodicTimer.stop()

                    roll = 0
                    pitch = 0
                }
            }
        }

        Button {
            text: "Now"
            font.pixelSize: 20
            visible: !isStarted

            onClicked: {
                updateReadings()
            }
        }
    }

    Label {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20

        text: "Demo mode - simulated sensor values"
        font.pixelSize: 13
        color: "gray"
    }
}
