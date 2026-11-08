SHELL := /bin/bash
.ONESHELL:

.PHONY: run-backend build-qt run-qt run clean

QT_DIR := qt-dashboard
QT_BUILD_DIR := $(QT_DIR)/build
QT_APP := $(QT_BUILD_DIR)/mpu6050_dashboard

# Start the sensor reader and Flask API
run-backend:
	@echo "Starting MPU6050 backend..."
	python3 read_mpu6050.py &
	SENSOR_PID=$$!
	python3 app.py &
	FLASK_PID=$$!

	cleanup() {
		echo "Stopping backend..."
		kill $$FLASK_PID $$SENSOR_PID 2>/dev/null || true
		wait $$FLASK_PID $$SENSOR_PID 2>/dev/null || true
	}
	trap cleanup EXIT INT TERM

	wait $$FLASK_PID

# Build Qt dashboard
build-qt:
	cmake -S $(QT_DIR) -B $(QT_BUILD_DIR)
	cmake --build $(QT_BUILD_DIR) -j$$(nproc)

# Run only Qt dashboard
run-qt: build-qt
	$(QT_APP)

# Run backend and Qt dashboard together
run: build-qt
	@echo "Starting MPU6050 backend and Qt dashboard..."

	python3 read_mpu6050.py &
	SENSOR_PID=$$!

	python3 app.py &
	FLASK_PID=$$!

	cleanup() {
		echo "Stopping project..."
		kill $$QT_PID $$FLASK_PID $$SENSOR_PID 2>/dev/null || true
		wait $$QT_PID $$FLASK_PID $$SENSOR_PID 2>/dev/null || true
	}
	trap cleanup EXIT INT TERM

	sleep 1

	$(QT_APP) &
	QT_PID=$$!

	wait $$QT_PID

# Remove Qt build files
clean:
	rm -rf $(QT_BUILD_DIR)