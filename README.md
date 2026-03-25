# Airbag-Triggering-System

This project presents the development and validation of a functional prototype for an airbag-triggering system. By using a triaxial **accelerometer (ADXL345)**, combined with an **ESP32 microcontroller**, the system reliably detects collisions in real time, distinguishing between frontal and lateral collisions, rollovers, and free falls.

Sensor data is processed and transmitted to a LabVIEW interface for real-time visualization, and also stored for later evaluation.

This project demonstrates the feasibility of low-cost, efficient automotive safety systems, with potential applications in autonomous vehicles, personal protection, and industrial monitoring.

This project was developed collaboratively with **Arnaldo Rodrigues** and **Gustavo Agostinho** at the University of Porto, Portugal, during the course 'Project (EFIS3001)'. My individual contributions are highlighted in the "My Contribution" section.

---

## Overview

The system measures real-time acceleration in three axes and triggers simulated crash events when thresholds are exceeded, distinguishing between frontal and lateral collisions, rollovers, and free fall scenarios.

The prototype built is wireless, powered by a battery of 5,000 mAh, and tightly packed in protective layers to avoid damaging the equipment. The prototype was tested in two stages.

First, we prepared different crash scenarios and analyzed the sensor data without applying any airbag-triggering thresholds. Then, the experimental data was thoroughly analyzed to determine reliable thresholds.

Secondly, we repeated the crash scenarios with the relevant airbag-triggering thresholds and analyzed the system's ability to reliably detect crash events. These steps were repeated several times to tune the threshold parameters.

Data analysis was conducted in Python.

---

## My Contribution

- Conducted data analysis to study the system's response time, reliability, and its ability to distinguish between crash events
- Developed LabVIEW interface for real-time sensor data visualization
- Implemented the TCP protocol for communication between ESP32 microcontroller and LabVIEW interface (collaboratively with Arnaldo Rodrigues)
- Conducted testing with the prototype in different crash scenarios (collaboratively with other team members)
- Defined relevant thresholds for crash detection based on experimental data (collaboratively with other members)

---

## References

[1] Espressif Systems, *ESP32 Technical Reference Manual*. [Online]. Available: https://documentation.espressif.com/esp32_technical_reference_manual_en.pdf. [Accessed: Mar. 25, 2026].

[2] Analog Devices, *ADXL345: Digital Accelerometer Datasheet*. [Online]. Available: https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf. [Accessed: Mar. 25, 2026].

[3] MicroPython, *ESP32 Quick Reference*. [Online]. Available: https://docs.micropython.org/en/latest/esp32/quickref.html. [Accessed: Mar. 25, 2026].

[4] National Instruments, *LabVIEW User Manual*. [Online]. Available: https://download.ni.com/support/manuals/320999b.pdf. [Accessed: Mar. 25, 2026].

[5] H. C. Gabler and J. Hinch, “Evaluation of advanced air bag deployment algorithm performance using event data recorders,” *Annals of Advances in Automotive Medicine*, vol. 52, pp. 175–184, Oct. 2008.

[6] Seeed Studio / reichelt elektronik, *Grove‑Button Module Datasheet (A300/101020003_01)*. [Online]. Available: https://cdn-reichelt.de/documents/datenblatt/A300/101020003_01.pdf. [Accessed: Mar. 25, 2026].