
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Window {
    id: window

    width: 900
    height: 600
    minimumWidth: 700
    minimumHeight: 500
    visible: true
    title: "MPU6050 Motion Monitor"

    property double roll: 0.0
    property double pitch: 0.0

    property bool isStarted: false
    property bool apiConnected: false
    property bool darkTheme: true

    // Theme colors
    property color backgroundColor: darkTheme ? "#111827" : "#F3F6FA"
    property color panelColor: darkTheme ? "#1F2937" : "#FFFFFF"
    property color primaryText: darkTheme ? "#F9FAFB" : "#172033"
    property color secondaryText: darkTheme ? "#9CA3AF" : "#64748B"
    property color borderColor: darkTheme ? "#374151" : "#E2E8F0"
    property color accentColor: "#38BDF8"
    property color positiveColor: "#22C55E"
    property color negativeColor: "#EF4444"


    // Request sensor readings from Flask
    function updateReadings() {
        var request = new XMLHttpRequest()

        request.open("GET", "http://127.0.0.1:5000/")

        request.onreadystatechange = function() {
            if (request.readyState === XMLHttpRequest.DONE) {

                if (request.status === 200) {
                    try {
                        var response = JSON.parse(request.responseText)

                        roll = Number(response.roll)
                        pitch = Number(response.pitch)

                        apiConnected = true
                    } catch (error) {
                        apiConnected = false
                        console.log("Invalid API response:", error)
                    }
                } else {
                    apiConnected = false
                    console.log("API error:", request.status)
                }
            }
        }

        request.send()
    }

    Timer {
        id: periodicTimer
        interval: 300
        repeat: true

        onTriggered: window.updateReadings()
    }

    Rectangle {
        anchors.fill: parent
        color: window.backgroundColor

        Column {
            anchors.fill: parent
            anchors.margins: 32
            spacing: 28

            // HEADER
            Row {
                width: parent.width
                height: 65
                spacing: 12

                Column {
                    anchors.verticalCenter: parent.verticalCenter
                    spacing: 5

                    Label {
                        text: "MPU6050"
                        font.pixelSize: 27
                        font.bold: true
                        color: window.primaryText
                    }

                    Label {
                        text: "MOTION MONITOR"
                        font.pixelSize: 11
                        font.bold: true
                        font.letterSpacing: 2
                        color: window.secondaryText
                    }
                }

                Item {
                    width: parent.width - 340
                    height: 1
                }

                // API STATUS
                Rectangle {
                    width: 145
                    height: 38
                    radius: 19
                    color: window.panelColor
                    border.color: window.borderColor
                    anchors.verticalCenter: parent.verticalCenter

                    Row {
                        anchors.centerIn: parent
                        spacing: 8

                        Rectangle {
                            width: 9
                            height: 9
                            radius: 5
                            color: window.apiConnected
                                   ? window.positiveColor
                                   : window.negativeColor
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Label {
                            text: window.apiConnected
                                  ? "API Connected"
                                  : "API Offline"
                            color: window.primaryText
                            font.pixelSize: 12
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

                // THEME BUTTON
                Rectangle {
                    width: 44
                    height: 44
                    radius: 12
                    color: window.panelColor
                    border.color: window.borderColor
                    anchors.verticalCenter: parent.verticalCenter

                    Label {
                        anchors.centerIn: parent
                        text: window.darkTheme ? "☀" : "☾"
                        font.pixelSize: 22
                        color: window.primaryText
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor

                        onClicked: {
                            window.darkTheme = !window.darkTheme
                        }
                    }
                }
            }

            // DESCRIPTION
            Column {
                spacing: 6

                Label {
                    text: "Sensor Overview"
                    font.pixelSize: 21
                    font.bold: true
                    color: window.primaryText
                }

                Label {
                    text: "Real-time orientation measurements"
                    font.pixelSize: 13
                    color: window.secondaryText
                }
            }

            // SENSOR CARDS
            Row {
                width: parent.width
                height: 205
                spacing: 20

                // ROLL CARD
                Rectangle {
                    width: (parent.width - 20) / 2
                    height: 205
                    radius: 16
                    color: window.panelColor
                    border.color: window.borderColor

                    Column {
                        anchors.fill: parent
                        anchors.margins: 24
                        spacing: 12

                        Label {
                            text: "ROLL"
                            font.pixelSize: 13
                            font.bold: true
                            font.letterSpacing: 2
                            color: window.secondaryText
                        }

                        Label {
                            text: window.roll.toFixed(2) + "°"
                            font.pixelSize: 48
                            font.bold: true
                            color: window.accentColor
                        }

                        Label {
                            text: "Rotation around X-axis"
                            font.pixelSize: 12
                            color: window.secondaryText
                        }
                    }
                }

                // PITCH CARD
                Rectangle {
                    width: (parent.width - 20) / 2
                    height: 205
                    radius: 16
                    color: window.panelColor
                    border.color: window.borderColor

                    Column {
                        anchors.fill: parent
                        anchors.margins: 24
                        spacing: 12

                        Label {
                            text: "PITCH"
                            font.pixelSize: 13
                            font.bold: true
                            font.letterSpacing: 2
                            color: window.secondaryText
                        }

                        Label {
                            text: window.pitch.toFixed(2) + "°"
                            font.pixelSize: 48
                            font.bold: true
                            color: "#A78BFA"
                        }

                        Label {
                            text: "Rotation around Y-axis"
                            font.pixelSize: 12
                            color: window.secondaryText
                        }
                    }
                }
            }

            // CONTROLS
            Column {
                width: parent.width
                spacing: 15

                Label {
                    text: "CONTROLS"
                    font.pixelSize: 12
                    font.bold: true
                    font.letterSpacing: 2
                    color: window.secondaryText
                }

                Row {
                    spacing: 12

                    // START / STOP
                    Rectangle {
                        width: 125
                        height: 46
                        radius: 10
                        color: window.isStarted
                               ? window.negativeColor
                               : window.positiveColor

                        Label {
                            anchors.centerIn: parent
                            text: window.isStarted ? "Stop" : "Start"
                            font.pixelSize: 14
                            font.bold: true
                            color: "#FFFFFF"
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor

                            onClicked: {
                                if (!window.isStarted) {
                                    window.isStarted = true
                                    window.updateReadings()
                                    periodicTimer.start()
                                } else {
                                    window.isStarted = false
                                    periodicTimer.stop()
                                }
                            }
                        }
                    }

                    // NOW
                    Rectangle {
                        width: 100
                        height: 46
                        radius: 10
                        color: window.panelColor
                        border.color: window.borderColor
                        visible: !window.isStarted

                        Label {
                            anchors.centerIn: parent
                            text: "Refresh"
                            font.pixelSize: 14
                            color: window.primaryText
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            onClicked: window.updateReadings()
                        }
                    }

                    // RESET
                    Rectangle {
                        width: 100
                        height: 46
                        radius: 10
                        color: window.panelColor
                        border.color: window.borderColor
                        visible: !window.isStarted

                        Label {
                            anchors.centerIn: parent
                            text: "Reset"
                            font.pixelSize: 14
                            color: window.primaryText
                        }

                        MouseArea {
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor

                            onClicked: {
                                window.roll = 0
                                window.pitch = 0
                            }
                        }
                    }
                }
            }

            Item {
                width: 1
                height: 1
            }

            // FOOTER
            Label {
                width: parent.width
                text: "Embedded Linux  |  Raspberry Pi 4  |  MPU6050"
                font.pixelSize: 11
                color: window.secondaryText
                horizontalAlignment: Text.AlignHCenter
            }
        }
    }
}