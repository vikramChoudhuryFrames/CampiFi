import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas

DIAGRAMS_DIR = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Top Running Header
        self.drawString(54, 755, "CAMPIFI — Database Connectivity & JDBC Implementation Guide")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 755, "Persistence Architecture & CRUD Reference")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)

        # Bottom Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "CampiFi — MySQL, JDBC Driver, HikariCP & JPA")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_db_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#1E3A8A")
    c_blue = colors.HexColor("#0284C7")
    c_teal = colors.HexColor("#0D9488")
    c_dark = colors.HexColor("#0F172A")
    c_text = colors.HexColor("#1E293B")
    c_muted = colors.HexColor("#475569")
    c_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_primary,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_muted,
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        textColor=c_primary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=c_blue,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=c_text,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_text,
        leftIndent=10,
        spaceAfter=2.5
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=10,
        textColor=c_muted,
        alignment=1,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.8,
        textColor=colors.HexColor("#0F172A")
    )

    viva_q_style = ParagraphStyle(
        'VivaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.5,
        textColor=colors.HexColor("#9A3412")
    )

    viva_a_style = ParagraphStyle(
        'VivaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1E293B")
    )

    def make_code_card(title, code_text):
        hdr = Paragraph(f"<b>Database Architecture Reference: {title}</b>", ParagraphStyle('CodeHdr', fontName='Helvetica-Bold', fontSize=7.8, textColor=c_primary))
        safe_text = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace('\n', '<br/>').replace(' ', '&nbsp;')
        body = Paragraph(safe_text, code_style)
        t = Table([[hdr], [body]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        return KeepTogether(t)

    def make_viva_card(question, answer):
        q_p = Paragraph(f"<b>Examiner / Viva Question:</b> {question}", viva_q_style)
        a_p = Paragraph(f"<b>Ideal Presentation Answer:</b> {answer}", viva_a_style)
        t = Table([[q_p], [a_p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#FCD34D")),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor("#FDE68A")),
            ('TOPPADDING', (0, 0), (-1, -1), 3.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ]))
        return KeepTogether(t)

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE, FIGURE 1 & EXECUTIVE SUMMARY TABLE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CampiFi — Database Connectivity & JDBC Implementation Guide", title_style))
    story.append(Paragraph("Demonstrating MySQL Connectivity, JDBC Driver Mechanics, HikariCP Connection Pooling, and CRUD Operations", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_primary, spaceBefore=0, spaceAfter=6))

    intro_p = Paragraph(
        "A critical question in software engineering defense is: <i>'Did you use JDBC or JPA/Hibernate for database connectivity?'</i> "
        "The authoritative answer in <b>CampiFi</b> is: <b>Both! Spring Data JPA and Hibernate run directly on top of JDBC.</b> "
        "The low-level connection is managed by the official MySQL JDBC driver (<code>com.mysql.cj.jdbc.Driver</code>) across a TCP socket "
        "on port 3306, pooled via HikariCP, while Hibernate ORM translates high-level domain operations into parameterized JDBC "
        "<code>PreparedStatement</code> and <code>ResultSet</code> calls. This guide demystifies the entire persistence pipeline, "
        "proving exactly how Insertion, Retrieval, Updating, and Deletion are executed at both the repository and JDBC driver levels.",
        body_style
    )
    story.append(intro_p)
    story.append(Spacer(1, 3))

    diag_path = os.path.join(DIAGRAMS_DIR, "database_connectivity_architecture.png")
    if os.path.exists(diag_path):
        img = Image(diag_path, width=420, height=280)
        story.append(img)
        story.append(Paragraph("<b>Figure 1:</b> The 6-Stage Database Connectivity Pipeline and the Underlying JDBC Mechanics for the 4 CRUD Operations.", caption_style))
    story.append(Spacer(1, 2))

    summary_table_data = [
        [
            Paragraph("<b>Connectivity Layer</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Component / Class in CampiFi</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Specific Technical Function in Pipeline</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white))
        ],
        [
            Paragraph("<b>1. Domain Service Layer</b>", body_style),
            Paragraph("<code>ChannelService</code>, <code>UserService</code>", code_style),
            Paragraph("Enforces business rules and manages atomic transactions via <code>@Transactional</code>", body_style)
        ],
        [
            Paragraph("<b>2. Repository Layer</b>", body_style),
            Paragraph("<code>UserRepository</code>, <code>ChannelRepository</code>", code_style),
            Paragraph("High-level interface contracts extending <code>JpaRepository&lt;T, ID&gt;</code>", body_style)
        ],
        [
            Paragraph("<b>3. ORM Engine</b>", body_style),
            Paragraph("Hibernate 6.4 (JPA Provider)", code_style),
            Paragraph("Translates entity mutations into parameterized SQL & performs dirty checking", body_style)
        ],
        [
            Paragraph("<b>4. Connection Pool</b>", body_style),
            Paragraph("HikariCP (Default Spring Boot Pool)", code_style),
            Paragraph("Maintains warm TCP connection pool; reuses sockets in &lt;0.1ms without latency", body_style)
        ],
        [
            Paragraph("<b>5. JDBC Driver Layer</b>", body_style),
            Paragraph("<code>com.mysql.cj.jdbc.Driver</code>", code_style),
            Paragraph("Low-level JDBC driver issuing <code>PreparedStatement</code> & parsing <code>ResultSet</code>", body_style)
        ],
        [
            Paragraph("<b>6. Relational Database</b>", body_style),
            Paragraph("MySQL Server (Port 3306, DB: <code>campifi</code>)", code_style),
            Paragraph("Stores persistent relational tables in Third Normal Form (3NF) on disk", body_style)
        ]
    ]
    st_table = Table(summary_table_data, colWidths=[110, 160, 234])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(st_table)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2: THE DATABASE STACK & HIKARICP POOLING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. The Database Connection Stack & Connection Pooling", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Core Architecture:</b> Database connectivity in CampiFi is configured in <code>src/main/resources/application.properties</code>. "
        "When Spring Boot starts up, it reads the data source configuration and initializes the official MySQL Connector/J JDBC driver "
        "along with the HikariCP high-performance connection pool:",
        body_style
    ))

    code_db_props = (
        "# application.properties: Core JDBC Data Source Configuration\n"
        "spring.datasource.url=jdbc:mysql://localhost:3306/campifi?useSSL=false&serverTimezone=Asia/Kolkata&allowPublicKeyRetrieval=true\n"
        "spring.datasource.username=campifi_user\n"
        "spring.datasource.password=campifi_pass\n"
        "spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver\n\n"
        "# JPA / Hibernate Integration with MySQL Dialect\n"
        "spring.jpa.hibernate.ddl-auto=update\n"
        "spring.jpa.show-sql=false\n"
        "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect\n"
        "spring.jpa.properties.hibernate.format_sql=true"
    )
    story.append(make_code_card("Database Connection Properties (application.properties)", code_db_props))
    story.append(Spacer(1, 4))

    story.append(Paragraph("A. The Role of the JDBC Driver (com.mysql.cj.jdbc.Driver)", h2_style))
    story.append(Paragraph(
        "The <code>mysql-connector-j</code> dependency declared in <code>pom.xml</code> provides the actual Java Database Connectivity implementation. "
        "It acts as a <b>Type 4 Pure Java Driver</b>: it directly converts JDBC calls into the MySQL binary network protocol over TCP port 3306. "
        "Hibernate and Spring Data JPA cannot communicate with MySQL without this underlying JDBC driver.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Connection Pooling with HikariCP (Zero Connection Lag)", h2_style))
    story.append(Paragraph(
        "Opening a fresh TCP socket connection to MySQL involves a three-way TCP handshake, authentication exchange, "
        "and session initialization—taking <b>50ms to 120ms per connection</b>. If 200 campus hotspot users connected simultaneously, "
        "opening a new JDBC connection for every chat message would immediately crash the server.",
        body_style
    ))
    story.append(Paragraph(
        "CampiFi utilizes <b>HikariCP</b>, the fastest production JDBC connection pool in Java. "
        "On server startup, HikariCP establishes a warm pool of pre-authenticated TCP connections to MySQL. "
        "When a repository executes a query, it leases an existing connection from the pool in <b>under 0.05ms</b>, executes the query, "
        "and immediately returns it to the pool for reuse by other threads.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "What is HikariCP, and why do we need a connection pool instead of opening new JDBC connections?",
        "HikariCP is an ultra-fast, zero-overhead JDBC connection pool. Establishing a new raw TCP connection to MySQL via DriverManager.getConnection() takes 50-100ms and incurs substantial CPU and network overhead. Under high concurrency on a campus Wi-Fi hotspot, hundreds of simultaneous requests would exhaust MySQL's max_connections limit. HikariCP keeps a pool of warm, active database connections in RAM, leasing and reclaiming them in microseconds, eliminating connection latency entirely."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3: OPERATION 1 - INSERTION (CREATE)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("2. Operation 1: Insertion (Record Creation)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Insertion</b> is the process of adding new persistent records into the database. "
        "In CampiFi, insertion occurs when a new student connects (<code>User</code>), a channel is created (<code>Channel</code>), "
        "a sub-channel is defined (<code>SubChannel</code>), or a chat message is sent (<code>Message</code>).",
        body_style
    ))

    story.append(Paragraph("A. How Insertion Is Written in CampiFi Code", h2_style))
    story.append(Paragraph(
        "In <code>UserService.java</code> (Lines 35-42), when a new student logs in, a new <code>User</code> instance is created and saved:",
        body_style
    ))

    code_insert_jpa = (
        "// In UserService.java: High-level Insertion via JPA\n"
        "User newUser = new User(email, displayName, User.Role.USER);\n"
        "User savedUser = userRepository.save(newUser); // Insertion executed!\n"
        "Long generatedId = savedUser.getId();          // Auto-generated ID populated!"
    )
    story.append(make_code_card("High-Level JPA Insertion Call", code_insert_jpa))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Underlying Parameterized SQL & JDBC Driver Execution", h2_style))
    story.append(Paragraph(
        "Behind the <code>userRepository.save()</code> call, Hibernate generates a parameterized SQL <code>INSERT</code> statement "
        "and executes it using low-level JDBC driver interfaces:",
        body_style
    ))

    code_insert_jdbc = (
        "// 1. Parameterized SQL generated by Hibernate:\n"
        "INSERT INTO users (email, display_name, role, created_at) VALUES (?, ?, ?, ?);\n\n"
        "// 2. Underlying JDBC Driver execution (com.mysql.cj.jdbc.Driver):\n"
        "Connection conn = dataSource.getConnection(); // Leased from HikariCP\n"
        "PreparedStatement pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);\n"
        "pstmt.setString(1, user.getEmail());\n"
        "pstmt.setString(2, user.getDisplayName());\n"
        "pstmt.setString(3, user.getRole().name());\n"
        "pstmt.setTimestamp(4, Timestamp.valueOf(user.getCreatedAt()));\n"
        "pstmt.executeUpdate(); // Executes INSERT over TCP socket on port 3306\n\n"
        "// 3. Capturing MySQL AUTO_INCREMENT Generated Key via JDBC:\n"
        "ResultSet rs = pstmt.getGeneratedKeys();\n"
        "if (rs.next()) {\n"
        "    Long autoId = rs.getLong(1); // Maps MySQL AUTO_INCREMENT ID to Java field\n"
        "}"
    )
    story.append(make_code_card("Underlying JDBC Driver Execution (Insertion)", code_insert_jdbc))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "How does the application retrieve the auto-generated primary key after an INSERT operation?",
        "In User.java, the primary key is annotated with '@GeneratedValue(strategy = GenerationType.IDENTITY)', which maps to MySQL's AUTO_INCREMENT feature. When save() is called, Hibernate instructs the JDBC PreparedStatement using Statement.RETURN_GENERATED_KEYS. After executing the INSERT, Hibernate calls pstmt.getGeneratedKeys() to read the resulting JDBC ResultSet, extracts the newly assigned long integer from MySQL, and sets the private 'id' field on the User entity object via reflection."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4: OPERATION 2 - RETRIEVAL (READ)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Operation 2: Retrieval (Querying & Fetching Records)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Retrieval</b> is the querying and reading of existing records from MySQL tables into Java memory. "
        "In CampiFi, retrieval is performed to verify user credentials, check channel PIN hashes, populate chat histories, and display network lists.",
        body_style
    ))

    story.append(Paragraph("A. How Retrieval Is Written in CampiFi Code", h2_style))
    story.append(Paragraph(
        "In <code>UserRepository.java</code> and <code>ChannelRepository.java</code>, retrieval operations are declared via Spring Data derived methods:",
        body_style
    ))

    code_read_jpa = (
        "// 1. Single Entity Lookup via Email in UserRepository.java\n"
        "Optional<User> userOpt = userRepository.findByEmail(\"student@college.edu\");\n\n"
        "// 2. Sorted Collection Retrieval in ChannelRepository.java\n"
        "List<Channel> channels = channelRepository.findAllByOrderByCreatedAtAsc();\n\n"
        "// 3. Foreign-Key Relationship Retrieval in SubChannelRepository.java\n"
        "List<SubChannel> subChannels = subChannelRepository.findByChannelId(channelId);"
    )
    story.append(make_code_card("High-Level JPA Retrieval Calls", code_read_jpa))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Underlying Parameterized SQL & JDBC ResultSet Parsing", h2_style))
    story.append(Paragraph(
        "When <code>findByEmail()</code> is executed, the JDBC driver creates a prepared statement, transmits the query over TCP to MySQL, "
        "and parses the resulting binary table rows via <code>java.sql.ResultSet</code>:",
        body_style
    ))

    code_read_jdbc = (
        "// 1. Parameterized SQL Query generated by Hibernate:\n"
        "SELECT u.id, u.email, u.display_name, u.role, u.created_at\n"
        "FROM users u WHERE u.email = ? LIMIT 1;\n\n"
        "// 2. Underlying JDBC Driver execution (com.mysql.cj.jdbc.Driver):\n"
        "Connection conn = dataSource.getConnection();\n"
        "PreparedStatement pstmt = conn.prepareStatement(sql);\n"
        "pstmt.setString(1, email); // Safe binding prevents SQL injection!\n"
        "ResultSet rs = pstmt.executeQuery(); // Executes query\n\n"
        "// 3. Entity Hydration: Mapping JDBC ResultSet to Java Object\n"
        "User user = null;\n"
        "if (rs.next()) {\n"
        "    user = new User();\n"
        "    user.setEmail(rs.getString(\"email\"));\n"
        "    user.setDisplayName(rs.getString(\"display_name\"));\n"
        "    user.setRole(User.Role.valueOf(rs.getString(\"role\")));\n"
        "    // Reflection sets private id and createdAt\n"
        "}"
    )
    story.append(make_code_card("Underlying JDBC Driver Execution (Retrieval & ResultSet)", code_read_jdbc))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "What is the JDBC ResultSet, and how does Spring Data JPA prevent SQL Injection during retrieval?",
        "A JDBC ResultSet is a cursor-based tabular data structure returned by MySQL containing the rows and columns that match a SELECT query. Spring Data JPA completely prevents SQL injection vulnerabilities because it NEVER uses string concatenation (like 'SELECT * WHERE email = ' + email). Instead, it always generates parameterized SQL queries and binds user inputs through JDBC's PreparedStatement.setString(). The MySQL database engine treats the parameter strictly as literal data, making SQL injection mathematically impossible."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5: OPERATION 3 - UPDATING (UPDATE)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Operation 3: Updating (Record Modification & Dirty Checking)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Updating</b> is the modification of existing record attributes in the database. "
        "In CampiFi, updates occur when a student is promoted to Channel Admin, a user's display name is modified, "
        "or a participant's membership status is changed.",
        body_style
    ))

    story.append(Paragraph("A. How Updating Is Written in CampiFi Code", h2_style))
    story.append(Paragraph(
        "In <code>ChannelService.java</code> (Lines 115-126), when a user is granted Master Admin rights for a channel, "
        "the user's role is updated in the database:",
        body_style
    ))

    code_update_jpa = (
        "// In ChannelService.java: Updating User & ChannelMember\n"
        "@Transactional\n"
        "public AdminSummary addChannelAdmin(Long channelId, String email) {\n"
        "    Channel ch = getChannelOrThrow(channelId);\n"
        "    User user = userService.findOrCreate(email.trim().toLowerCase());\n"
        "    user.setRole(User.Role.ADMIN); // State modified in memory!\n"
        "    userRepository.save(user);     // Triggering database update\n\n"
        "    ChannelMember member = memberRepository.findByUserAndChannel(user, ch)\n"
        "            .orElseGet(() -> new ChannelMember(user, ch, true));\n"
        "    member.setAdmin(true);         // Member flag updated!\n"
        "    memberRepository.save(member);\n"
        "    return new AdminSummary(user.getId(), user.getEmail(), user.getDisplayName());\n"
        "}"
    )
    story.append(make_code_card("Entity Update Logic in ChannelService.java", code_update_jpa))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Hibernate Dirty Checking & Underlying JDBC UPDATE Execution", h2_style))
    story.append(Paragraph(
        "Hibernate features an intelligent mechanism called <b>Automatic Dirty Checking</b>. "
        "When an entity is loaded inside a <code>@Transactional</code> method, Hibernate keeps an internal snapshot of its original state. "
        "When the transaction commits, Hibernate compares the current entity state against the snapshot: if any field changed, "
        "it automatically generates and issues an optimized JDBC <code>UPDATE</code> statement:",
        body_style
    ))

    code_update_jdbc = (
        "// 1. Parameterized SQL UPDATE generated by Hibernate:\n"
        "UPDATE users SET role = ?, display_name = ? WHERE id = ?;\n\n"
        "// 2. Underlying JDBC Driver execution (com.mysql.cj.jdbc.Driver):\n"
        "Connection conn = dataSource.getConnection();\n"
        "PreparedStatement pstmt = conn.prepareStatement(sql);\n"
        "pstmt.setString(1, \"ADMIN\");\n"
        "pstmt.setString(2, user.getDisplayName());\n"
        "pstmt.setLong(3, user.getId()); // Primary Key in WHERE clause\n"
        "int rowsUpdated = pstmt.executeUpdate(); // Executes UPDATE on MySQL\n"
        "// rowsUpdated == 1 confirms successful modification"
    )
    story.append(make_code_card("Underlying JDBC Driver Execution (Update)", code_update_jdbc))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "What is Dirty Checking in Hibernate, and does it execute an UPDATE if no fields were changed?",
        "Dirty Checking is Hibernate's automated change-detection mechanism. Inside a @Transactional method, Hibernate stores an initial snapshot of each retrieved entity in its First-Level Cache (Persistence Context). At transaction commit, Hibernate compares the entity's current in-memory state against the snapshot. If no fields were modified, Hibernate smartly suppresses the query and executes ZERO JDBC UPDATE statements, saving database CPU and network bandwidth."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6: OPERATION 4 - DELETION (DELETE)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Operation 4: Deletion (Record Removal & Cascading)", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Deletion</b> is the permanent removal of records from MySQL tables. "
        "In CampiFi, deletion occurs when an admin revokes privileges, a sub-channel admin is unassigned, or a channel is removed.",
        body_style
    ))

    story.append(Paragraph("A. How Deletion Is Written in CampiFi Code", h2_style))
    story.append(Paragraph(
        "In <code>ChannelService.java</code> (Lines 183-191), when revoking Sub-Channel Admin authority, "
        "the corresponding relationship entity is removed from the database:",
        body_style
    ))

    code_delete_jpa = (
        "// In ChannelService.java: Explicit Deletion\n"
        "@Transactional\n"
        "public void removeSubChannelAdmin(Long subChannelId, Long userId) {\n"
        "    SubChannel sub = subChannelRepository.findById(subChannelId)\n"
        "            .orElseThrow(() -> new IllegalArgumentException(\"SubChannel not found: \" + subChannelId));\n"
        "    User user = getUserOrThrow(userId);\n"
        "    subChannelAdminRepository.findByUserAndSubChannel(user, sub)\n"
        "            .ifPresent(subChannelAdminRepository::delete); // Deletion executed!\n"
        "    downgradeRoleIfNoAdminRoles(user);\n"
        "}"
    )
    story.append(make_code_card("Entity Deletion in ChannelService.java", code_delete_jpa))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Underlying JDBC DELETE & Cascading Integrity", h2_style))
    story.append(Paragraph(
        "Hibernate translates the repository delete call into an SQL <code>DELETE</code> statement using JDBC:",
        body_style
    ))

    code_delete_jdbc = (
        "// 1. Parameterized SQL DELETE generated by Hibernate:\n"
        "DELETE FROM sub_channel_admins WHERE id = ?;\n\n"
        "// 2. Underlying JDBC Driver execution (com.mysql.cj.jdbc.Driver):\n"
        "Connection conn = dataSource.getConnection();\n"
        "PreparedStatement pstmt = conn.prepareStatement(sql);\n"
        "pstmt.setLong(1, subChannelAdminId);\n"
        "int rowsDeleted = pstmt.executeUpdate(); // Executes DELETE on MySQL\n\n"
        "// 3. Cascading Orphan Removal in Channel.java:\n"
        "// @OneToMany(mappedBy = \"channel\", cascade = CascadeType.ALL, orphanRemoval = true)\n"
        "// If a Channel is deleted, Hibernate automatically issues cascading JDBC DELETEs\n"
        "// for all child SubChannels and Messages, preventing orphan records!"
    )
    story.append(make_code_card("Underlying JDBC Driver Execution (Deletion & Cascades)", code_delete_jdbc))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "What happens to sub-channels and messages when a parent Channel is deleted?",
        "In Channel.java, the subChannels and members relationships are annotated with 'cascade = CascadeType.ALL, orphanRemoval = true'. When a parent channel is deleted, Hibernate automatically traverses the entity graph and issues cascading JDBC DELETE statements for all associated sub-channels, channel memberships, and messages. This guarantees referential integrity in MySQL and prevents orphan records without requiring manual deletion loops."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 7: TRANSACTION MANAGEMENT & RAW JDBC COMPARISON
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Transaction Management (@Transactional) & ACID Guarantees", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> In database connectivity, a <b>Transaction</b> is a single unit of work composed of multiple operations "
        "that must either all succeed together or all fail together. CampiFi manages transactions declaratively using Spring's <code>@Transactional</code>:",
        body_style
    ))

    story.append(Paragraph("A. How @Transactional Controls Underlying JDBC Transactions", h2_style))
    story.append(Paragraph("1. <b>Method Invocation:</b> Spring's transaction interceptor leases a JDBC connection from HikariCP and invokes <code>conn.setAutoCommit(false);</code>.", bullet_style))
    story.append(Paragraph("2. <b>Execution:</b> Multiple JPA repository operations execute their respective SQL statements across the shared JDBC connection.", bullet_style))
    story.append(Paragraph("3. <b>Success (Commit):</b> If the method completes normally, Spring calls <code>conn.commit();</code> to permanently persist all changes to MySQL.", bullet_style))
    story.append(Paragraph("4. <b>Failure (Rollback):</b> If an unhandled <code>RuntimeException</code> occurs (e.g. duplicate channel name), Spring intercepts the error and calls <code>conn.rollback();</code>, ensuring the database is never left in an inconsistent partial state.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Direct Comparison: Raw JDBC vs Spring Data JPA", h2_style))
    story.append(Paragraph(
        "Examiners frequently ask how modern JPA compares to manual, old-school raw JDBC. Here is the direct side-by-side comparison:",
        body_style
    ))

    code_comparison = (
        "// ── OLD-SCHOOL RAW JDBC (Manual Plumbing, Error-Prone) ───────────────────────────\n"
        "Connection conn = null;\n"
        "PreparedStatement pstmt = null;\n"
        "try {\n"
        "    conn = DriverManager.getConnection(\"jdbc:mysql://localhost:3306/campifi\", \"user\", \"pass\");\n"
        "    conn.setAutoCommit(false);\n"
        "    pstmt = conn.prepareStatement(\"INSERT INTO users (email, display_name) VALUES (?, ?)\");\n"
        "    pstmt.setString(1, email); pstmt.setString(2, name);\n"
        "    pstmt.executeUpdate();\n"
        "    conn.commit();\n"
        "} catch (SQLException e) { if (conn != null) conn.rollback(); } // 30+ lines of manual boilerplate!\n\n"
        "// ── MODERN CAMPIFI IMPLEMENTATION (Spring Data JPA + Hibernate) ──────────────────\n"
        "// The developer writes clean, type-safe, expressive domain code:\n"
        "@Transactional\n"
        "public User registerUser(String email, String name) {\n"
        "    return userRepository.save(new User(email, name, Role.USER)); // 3 clean lines!\n"
        "}"
    )
    story.append(make_code_card("Side-by-Side: Raw JDBC vs Modern Spring Data JPA", code_comparison))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why did you use Spring Data JPA instead of writing raw JDBC code for everything?",
        "Raw JDBC requires enormous amounts of repetitive boilerplate code: manual connection handling, explicit SQL authoring, manual parameter binding, tedious ResultSet-to-object parsing, and manual try-catch transaction rollbacks. Spring Data JPA eliminates 85% of boilerplate code, automates object-relational mapping, provides dirty checking, guarantees SQL injection safety via PreparedStatement binding, and manages connection pools via HikariCP—while still executing optimized JDBC statements underneath."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 8: MASTER DATABASE MATRIX & VIVA CHEAT SHEET
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("7. Database Connectivity Master Matrix & Viva Examination Defense", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "Use this master reference matrix during your project evaluation to immediately point examiners "
        "to the exact repository, method, generated SQL, and underlying JDBC API call for each operation:",
        body_style
    ))

    db_matrix_data = [
        [
            Paragraph("<b>CRUD Operation</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white)),
            Paragraph("<b>CampiFi Repository & Method</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white)),
            Paragraph("<b>Generated SQL Statement</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white)),
            Paragraph("<b>Underlying JDBC API Execution</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white))
        ],
        [
            Paragraph("<b>Create (Insertion)</b>", body_style),
            Paragraph("<code>userRepository.save(user)</code><br/><code>channelRepository.save(ch)</code>", code_style),
            Paragraph("<code>INSERT INTO users (email, display_name, role) VALUES (?, ?, ?)</code>", code_style),
            Paragraph("<code>PreparedStatement.executeUpdate()</code> followed by <code>getGeneratedKeys()</code> to fetch auto-assigned ID", body_style)
        ],
        [
            Paragraph("<b>Read (Retrieval)</b>", body_style),
            Paragraph("<code>userRepository.findByEmail(e)</code><br/><code>channelRepository.findById(id)</code>", code_style),
            Paragraph("<code>SELECT * FROM users WHERE email = ? LIMIT 1</code>", code_style),
            Paragraph("<code>PreparedStatement.executeQuery()</code> returning <code>ResultSet</code>; mapped to entity fields", body_style)
        ],
        [
            Paragraph("<b>Update (Updating)</b>", body_style),
            Paragraph("<code>user.setRole(Role.ADMIN)</code><br/><code>userRepository.save(user)</code>", code_style),
            Paragraph("<code>UPDATE users SET role = ?, display_name = ? WHERE id = ?</code>", code_style),
            Paragraph("Hibernate Dirty Checking compares entity against snapshot; calls <code>PreparedStatement.executeUpdate()</code>", body_style)
        ],
        [
            Paragraph("<b>Delete (Deletion)</b>", body_style),
            Paragraph("<code>subChannelAdminRepo.delete(a)</code><br/><code>channelRepo.deleteById(id)</code>", code_style),
            Paragraph("<code>DELETE FROM sub_channel_admins WHERE id = ?</code>", code_style),
            Paragraph("<code>PreparedStatement.executeUpdate()</code>; cascading child deletions via <code>orphanRemoval = true</code>", body_style)
        ],
        [
            Paragraph("<b>Connection Pool</b>", body_style),
            Paragraph("HikariCP Data Source<br/>(Spring Boot default)", code_style),
            Paragraph("TCP keep-alives over port 3306", code_style),
            Paragraph("<code>dataSource.getConnection()</code> leases warm connection in &lt;0.05ms without TCP handshake lag", body_style)
        ]
    ]

    m_table = Table(db_matrix_data, colWidths=[80, 135, 145, 144])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(KeepTogether(m_table))
    story.append(Spacer(1, 6))

    golden_rules = [
        Paragraph("<b>Top 4 'Golden Rules' to Remember for Your Database & JDBC Defense</b>", h2_style),
        Paragraph("1. <b>Clarify 'Both JDBC and JPA':</b> Never say 'we used JPA instead of JDBC'—say: <i>'We used Spring Data JPA with Hibernate, which runs directly on top of the MySQL JDBC driver (com.mysql.cj.jdbc.Driver). Hibernate generates parameterized SQL and executes it via JDBC PreparedStatement and ResultSet calls.'</i>", bullet_style),
        Paragraph("2. <b>Explain HikariCP Connection Pooling:</b> Highlight that HikariCP eliminates TCP connection latency by keeping warm connections open in RAM, serving requests in microseconds rather than 100ms per connection.", bullet_style),
        Paragraph("3. <b>Demonstrate SQL Injection Immunity:</b> Emphasize that all queries use JDBC PreparedStatement parameter binding ('?'), ensuring user inputs are treated as literal values, mathematically preventing SQL injection attacks.", bullet_style),
        Paragraph("4. <b>Highlight @Transactional Atomicity:</b> Explain that @Transactional controls the underlying JDBC connection's autoCommit flag, committing when all operations succeed and issuing a rollback if an error occurs.", bullet_style)
    ]
    story.append(KeepTogether(golden_rules))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Database Guide PDF successfully generated at: {filename}")

if __name__ == '__main__':
    target = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/CampiFi_Database_Connectivity_and_JDBC_Guide.pdf"
    build_db_pdf(target)
