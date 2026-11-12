# CampiFi 📡
### Offline Campus Hotspot Real-Time Communication System

[![Java](https://img.shields.io/badge/Java-17-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.5-brightgreen.svg)](https://spring.io/projects/spring-boot)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-blue.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> **Air-Gapped, Zero-Cloud Local Communication Network for College Campuses**  
> Operates 100% offline over a local Wi-Fi hotspot without requiring active cellular data, SIM cards, or third-party cloud servers.

---

## 🌟 Why CampiFi?

Traditional campus messaging apps (WhatsApp, Telegram, Slack) require an active internet connection. During campus events, cellular dead zones (auditoriums, basement labs), or intentional internet restrictions (examinations), communication breaks down.

**CampiFi** solves this by turning any laptop running Java into a local communication server. A student or host enables a local Wi-Fi hotspot (`CampiFi-Campus`). Any peer connected to this hotspot can open their mobile or laptop browser to chat, join study channels, and receive campus broadcasts with **sub-35ms latency**.

---

## 🚀 Key Features

- **🌐 Zero-Internet Operation**: Runs entirely on local radio frequencies using standard Wi-Fi adapters.
- **⚡ Instant Real-Time Messaging**: Built on Java WebSockets & STOMP protocol for bi-directional live communication.
- **🔒 Public & Private Channels**:
  - *Public Channels*: Open campus-wide announcements (read-only for regular users, writable by admins).
  - *Private Channels*: Department or study team rooms secured by a 4-digit cryptographic PIN.
- **🛡️ Cryptographic Security**: Passwords and channel PINs are hashed using **SHA-256** via Java's `MessageDigest`. No plaintext passwords ever touch the database.
- **💾 Relational Database Persistence (JDBC)**: Full MySQL integration handling Create, Read, Update, and Delete (CRUD) operations with parameterized `PreparedStatement` to prevent SQL injection.
- **📱 Dual User Interface**:
  - *Zero-Install Mobile Web GUI*: Responsive HTML5/CSS/JavaScript interface accessible on any smartphone browser (iOS/Android).
  - *Native Java Swing Desktop Client*: Dedicated `JFrame` host administration console for desktop operators.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
|---|---|
| **Backend Language** | Java (JDK 17) |
| **Frameworks** | Spring Boot 3.2.5, Spring WebSocket, Spring Data JPA |
| **Database & Persistence** | MySQL 8.0, JDBC (`com.mysql.cj.jdbc.Driver`), HikariCP Connection Pooling |
| **Security** | SHA-256 MessageDigest, 128-bit UUID Ephemeral Sessions |
| **Frontend UI** | HTML5, Modern CSS Variables (Dark Theme), Vanilla JavaScript (ES6+), Java Swing (`javax.swing`) |
| **Build Tool** | Apache Maven |

---

## 🏛️ System Architecture

CampiFi follows a clean **4-Tier Architecture**:

```
+-----------------------------------------------------------------------+
|                       PRESENTATION TIER                               |
|   Student Smartphones & Laptops        Host Admin Laptop              |
|   (Web Browser: HTML5 / CSS / JS)     (Java Swing Desktop GUI)        |
+-----------------------------------+-----------------------------------+
                                    | Local Wi-Fi (Port 8080)
                                    v
+-----------------------------------------------------------------------+
|                    CONTROLLER & INGRESS TIER                          |
|   AuthController   ChannelController   ChatController   PageController|
+-----------------------------------+-----------------------------------+
                                    | Java Method Calls
                                    v
+-----------------------------------------------------------------------+
|                     SERVICE & SECURITY TIER                           |
|   SessionService        ChannelService            NetworkUtils        |
|   - ConcurrentHashMap   - SHA-256 PIN Hashing     - Subnet Detection  |
|   - UUID Session Token  - Streams & Filters       - Security Guards   |
+-----------------------------------+-----------------------------------+
                                    | Java Objects & Transactions
                                    v
+-----------------------------------------------------------------------+
|                   DATA ACCESS LAYER (JDBC / JPA)                      |
|   UserRepository       ChannelRepository      MessageRepository       |
|   - PreparedStatement  - SQL CRUD Operations  - ResultSet Mapping     |
+-----------------------------------+-----------------------------------+
                                    | TCP Port 3306
                                    v
+-----------------------------------------------------------------------+
|                         MYSQL DATABASE                                |
|   [users]   [channels]   [sub_channels]   [messages]   [members]      |
+-----------------------------------------------------------------------+
```

---

## 📂 Project Structure

```
hotspot-chat/
├── pom.xml                               # Maven project dependencies
├── README.md                             # Project documentation
├── CampiFi_Project_Report.md             # Complete academic report (12 rubric criteria)
├── diagrams/                             # Architecture, UML & ER diagrams
├── src/
│   ├── main/
│   │   ├── java/com/hotspotchat/
│   │   │   ├── HotspotChatApplication.java    # Application Entry Point
│   │   │   ├── DataInitializer.java           # Initial database seeding
│   │   │   ├── config/                        # WebSocket & static asset configuration
│   │   │   ├── controller/                    # REST & WebSocket endpoints
│   │   │   ├── model/                         # JPA domain entities (User, Channel, Message)
│   │   │   ├── repository/                    # Spring Data / JDBC DAOs
│   │   │   ├── service/                       # Business logic, SHA-256 hashing, sessions
│   │   │   └── gui/
│   │   │       └── CampiFiSwingClient.java    # Native Java Swing desktop UI
│   │   └── resources/
│   │       ├── application.properties         # Database and server configuration
│   │       └── static/                        # Web client assets (index, channels, chat, admin)
```

---

## ⚡ Quick Start & Setup

### 1. Prerequisites
- **Java Development Kit (JDK 17 or higher)**: `java -version`
- **Apache Maven 3.8+**: `mvn -version`
- **MySQL Server 8.0+**: Running locally on port `3306`

### 2. Configure MySQL Database
Open your MySQL prompt and create the database and user:
```sql
CREATE DATABASE campifi;
CREATE USER 'campifi_user'@'localhost' IDENTIFIED BY 'CampiFi#2026';
GRANT ALL PRIVILEGES ON campifi.* TO 'campifi_user'@'localhost';
FLUSH PRIVILEGES;
```

*(You can adjust credentials in `src/main/resources/application.properties` if needed).*

### 3. Build & Run the Application
In your project directory:
```bash
# Compile and package
mvn clean package

# Run the Spring Boot application
mvn spring-boot:run
```

Once started, the console will confirm:
```text
[CampiFi] System ready. Access at: http://localhost:8080
```

### 4. Connect to Hotspot
1. Turn on your laptop's **Wi-Fi Hotspot** (e.g., SSID: `CampiFi-Campus`).
2. Have students connect their phones/laptops to this Wi-Fi.
3. Open `http://<HOST_IP>:8080` (e.g., `http://192.168.43.1:8080`) in any browser.

---

## 👥 Authors & Team
- **V** – *System Flow & Network Architecture*
- **A** – *Object-Oriented Design & UML Modeling*
- **G** – *Java Concurrency, Thread Safety & Cryptography*
- **H** – *Database (JDBC), User Interface & Testing*

---
*Developed for Academic Project Submission & Technical Presentation.*
