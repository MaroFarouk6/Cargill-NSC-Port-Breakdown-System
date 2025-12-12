# 🏭 Cargill Equipment Breakdown Management System (NSC Port)

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Production--Ready-success?style=for-the-badge)]()
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=for-the-badge&logo=windows)]()

## 📋 Project Overview

This desktop application was developed to digitize and streamline the maintenance tracking process for **Cargill (NSC Port)** operations. It replaces manual logging with a centralized, secure digital dashboard that tracks equipment failures, maintenance responses, and operational downtime in real-time.

The system features a **custom Dark Mode GUI** and implements **Role-Based Access Control (RBAC)** to distinguish between operational staff (logging issues) and engineering teams (resolving issues).

## 🚀 Key Features

### 🔐 Role-Based Access Control (RBAC)
* **Operator Mode (OPS):** Restricted access. Can only view status and log initial breakdowns.
* **Engineer Mode (ENG):** Full privileges. Can change equipment status to "Ready," "Planned Maintenance," or "Out of Service."
* **Secure Authentication:** SQLite-backed user management system with role assignment.

### 📊 Real-Time Dashboard
* **Live Status Tracking:** Uses `threading` to auto-refresh equipment status every 10 seconds without freezing the GUI.
* **Dynamic Visualization:** Color-coded cells (Green=Available, Red=Breakdown, Blue=Planned Maintenance) for instant visual assessment.
* **Log View:** Integrated `tksheet` widget to view historical logs directly within the app.

### 📑 Reporting & Data Export
* **Excel Export:** One-click generation of `.xlsx` reports using `XlsxWriter`.
* **Conditional Formatting:** Exported reports automatically apply color coding (Red/Green/Blue) to match the dashboard status.
* **Audit Trail:** Every action is logged with Timestamp, User, Role, and Status Change in a persistent SQLite database.

## 💻 Tech Stack

* **Language:** Python 3.10+
* **GUI Framework:** Tkinter (Custom Dark Theme)
* **Database:** SQLite3
* **Libraries:**
    * `tksheet` (Data Grid Display)
    * `XlsxWriter` (Reporting Engine)
    * `threading` (Concurrency)

## 📂 Project Structure

```text
Cargill-Breakdown-System/
├── assets/              # Icons (icons8-login-30.png, etc.)
├── main.py              # Application entry point (System Logic)
├── equipment.db         # SQLite Database (Auto-generated if missing)
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```
## 🔧 Installation and Setup

### 1.Clone the Repository
Download the project files to your local machine
```bash
git clone [https://github.com/yourusername/cargill-breakdown-system.git](https://github.com/yourusername/cargill-breakdown-system.git)
cd cargill-breakdown-system
```
### 2.Install Dependencies
This project requires specific libararies for the log grid (`tksheet`) and Escel reporting (`xlsxwriter`)
```bash
pip install -r requirements.txt
```
### 3.Verify Database & Assets
Ensure the following files are present in the root directory for the app to launch correctly:
   * `equipment.db` (The SQLite database file)
   * `icons8-login-30.png` (and other icon assets)
### 4.Run the Application
```bash
python main.py
```
## 🤝 Contribution
This project was a collaborative engineering effort designed to help in real-world industrial software 
#### Core Team
   * **[Omar Mohamed Farouk](https://www.linkedin.com/in/omar-amin-ejs/)**
   * **[Ibrahim Talal](https://www.linkedin.com/in/ibrahim-talal/)**


