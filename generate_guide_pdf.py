import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

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
            return  # Suppress headers/footers on title/cover page

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Top Running Header
        self.drawString(54, 755, "CAMPIFI — Comprehensive System Architecture & Codebase Guide")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 755, "Spring Boot + WebSocket + MySQL")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)

        # Bottom Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Project Presentation & Viva Preparation Document")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    c_primary = colors.HexColor("#1E3A8A")   # Deep Navy
    c_secondary = colors.HexColor("#3B82F6") # Bright Blue
    c_dark = colors.HexColor("#0F172A")      # Slate 900
    c_muted = colors.HexColor("#475569")     # Slate 600
    c_accent = colors.HexColor("#0D9488")    # Teal 600
    c_bg = colors.HexColor("#F8FAFC")        # Slate 50
    c_card_border = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_muted,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=15,
        spaceAfter=3
    )

    code_title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=c_primary
    )

    code_desc_style = ParagraphStyle(
        'CodeDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # COVER / HEADER BLOCK
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 15))
    story.append(Paragraph("CampiFi — Complete System Architecture & Code Guide", title_style))
    story.append(Paragraph("A Step-by-Step Technical Reference of Every Class, File, Workflow, and Database Operation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceBefore=0, spaceAfter=12))

    # Meta summary table
    meta_data = [
        [
            Paragraph("<b>Project Domain:</b> Local Campus Network Chat", body_style),
            Paragraph("<b>Backend:</b> Spring Boot 3.2.5 (Java 17/21)", body_style)
        ],
        [
            Paragraph("<b>Protocol:</b> WebSockets + STOMP over SockJS", body_style),
            Paragraph("<b>Database:</b> MySQL 8.4 via Spring Data JPA / Hibernate", body_style)
        ],
        [
            Paragraph("<b>Network Scope:</b> Campus Subnet (10.0.0.0/8 / Hotspot)", body_style),
            Paragraph("<b>Security:</b> SHA-256 PIN Hashing + Dynamic Role RBAC", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[240, 264])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg),
        ('BOX', (0,0), (-1,-1), 1, c_card_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ══════════════════════════════════════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY & HOW IT ALL WORKS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Executive Summary & Runtime Flow", h1_style))
    story.append(Paragraph(
        "<b>CampiFi</b> is an off-grid campus communication platform engineered to function without external internet connectivity. "
        "It operates over the local Wi-Fi or mobile hotspot. Devices physically within the campus IP range can connect, communicate in real time, "
        "and organize into academic hierarchies without relying on commercial cloud messaging platforms like WhatsApp or Discord.",
        body_style
    ))
    story.append(Paragraph("<b>End-to-End Runtime Execution Order:</b>", h2_style))
    
    flow_steps = [
        "<b>Step 1: Application Boot:</b> Spring Boot starts, reads <code>application.properties</code>, connects to MySQL via JDBC, validates tables via Hibernate DDL-auto, and runs <code>DataInitializer</code> to auto-seed initial networks.",
        "<b>Step 2: Gatekeeper IP Check:</b> A device opens <code>http://&lt;server-ip&gt;:8080/</code>. <code>PageController</code> calls <code>NetworkUtils.isHostDevice()</code>. The host computer is routed to <code>admin.html</code>; other campus devices are routed to <code>index.html</code>.",
        "<b>Step 3: Frictionless Authentication:</b> The student enters their institutional email (e.g. <code>vikram_choudhury@srmap.edu.in</code>). <code>AuthController</code> calls <code>UserService.findOrCreate()</code> which parses the display name, creates a <code>User</code> entity, and stores an 8-hour UUID session in <code>SessionService</code>.",
        "<b>Step 4: Network Directory:</b> The client is redirected to <code>channels.html</code>. It fetches all root channels from <code>GET /api/channels</code>. Public networks can be viewed immediately; Private networks prompt for a 4-digit PIN.",
        "<b>Step 5: PIN Verification:</b> Submitting a 4-digit PIN triggers <code>POST /api/channels/{id}/verify-pin</code>. <code>ChannelService</code> hashes the PIN with <b>SHA-256</b> and compares it against the database hash. On success, the user is joined as a <code>ChannelMember</code>.",
        "<b>Step 6: Real-Time Chat Connection:</b> The user opens a channel or sub-channel (<code>chat.html?room=...</code>). The client creates a <b>SockJS + STOMP</b> WebSocket connection to <code>/ws</code>, subscribes to <code>/topic/room/{roomName}</code>, and broadcasts a <code>JOIN</code> message.",
        "<b>Step 7: Bi-Directional Messaging:</b> When any user types a message and clicks Send, it sends a STOMP payload to <code>/app/chat/{room}</code>. <code>ChatController</code> intercepts it, attaches server timestamps, and publishes it to all active subscribers via <code>/topic/room/{room}</code> instantaneously."
    ]
    for s in flow_steps:
        story.append(Paragraph("• " + s, bullet_style))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 2. APPLICATION BOOT & CONFIGURATION LAYER
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("2. Application Boot & Configuration Layer", h1_style))

    boot_classes = [
        ("HotspotChatApplication.java", "src/main/java/com/hotspotchat/HotspotChatApplication.java",
         "The entry point of the Spring Boot application. Decorated with <code>@SpringBootApplication</code> and <code>@EnableScheduling</code>. "
         "Initializes the Spring ApplicationContext, component scanning across all sub-packages, and launches the embedded Tomcat server on port 8080."),
        ("application.properties", "src/main/resources/application.properties",
         "Central configuration file. Configures server port (8080), network bind address (0.0.0.0 for LAN access), MySQL JDBC datasource URL "
         "(<code>jdbc:mysql://localhost:3306/campifi</code>), credentials (<code>campifi_user</code>/<code>campifi_pass</code>), Hibernate dialect, "
         "<code>spring.jpa.hibernate.ddl-auto=update</code> (auto-creates/updates tables without data loss), and upload size caps (50MB)."),
        ("DataInitializer.java", "src/main/java/com/hotspotchat/DataInitializer.java",
         "Implements <code>CommandLineRunner</code> to execute immediately after application startup. Checks if the database already has channels; "
         "if empty, it auto-seeds 4 standard networks: <i>University Announcements</i> (Public), <i>Campus Events & Sports</i> (Public), "
         "<i>Computer Science Dept</i> (Private, PIN 1234), and <i>Faculty Council</i> (Private, PIN 9999). Also pre-seeds sub-channels (e.g. 3rd Year Core, Lab Group A).")
    ]

    for name, path, desc in boot_classes:
        t_data = [[
            Paragraph(f"<b>Class / File:</b> {name}<br/><font color='#64748B'>Path: {path}</font>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 3. DATABASE SCHEMA & JPA ENTITIES (THE MODEL LAYER)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Database Schema & JPA Entity Layer", h1_style))
    story.append(Paragraph(
        "Spring Data JPA maps these Java classes directly to MySQL tables using annotations like <code>@Entity</code>, <code>@Table</code>, "
        "<code>@Id</code>, <code>@ManyToOne</code>, and <code>@OneToMany</code>. You do not need to write raw SQL table definitions; Hibernate generates them.",
        body_style
    ))

    entities = [
        ("User.java (Table: users)",
         "Represents a registered campus participant. Fields: <code>id</code> (Primary Key), <code>email</code> (unique index), "
         "<code>displayName</code> (derived from email), <code>role</code> (Enum: <code>USER</code> or <code>ADMIN</code>), <code>createdAt</code>. "
         "Drives privilege authorization across the entire platform."),
        ("Channel.java (Table: channels)",
         "Represents a root network. Fields: <code>id</code>, <code>name</code>, <code>description</code>, <code>type</code> (Enum: <code>PUBLIC</code> or <code>PRIVATE</code>), "
         "<code>pinHash</code> (stores the SHA-256 hash of the 4-digit PIN for private networks, null for public), <code>createdAt</code>. "
         "Has a <code>@OneToMany</code> relationship with <code>SubChannel</code> and <code>ChannelMember</code>."),
        ("SubChannel.java (Table: sub_channels)",
         "Represents nested sub-groups inside a channel. Fields: <code>id</code>, <code>name</code>, <code>description</code>, "
         "<code>channel</code> (<code>@ManyToOne</code> foreign key back to parent <code>Channel</code>). Allows dividing large departments into smaller batch/lab groups."),
        ("ChannelMember.java (Table: channel_members)",
         "Association entity representing channel membership. Fields: <code>id</code>, <code>user</code> (FK), <code>channel</code> (FK), "
         "<code>isAdmin</code> (boolean flag indicating if the member is a Master Admin of this channel), <code>isBanned</code> (boolean flag)."),
        ("SubChannelAdmin.java (Table: sub_channel_admins)",
         "Dedicated mapping entity that binds a specific <code>User</code> to a specific <code>SubChannel</code> as an administrator. "
         "Allows assigning faculty leads to individual sub-groups without making them global root channel admins."),
        ("ChatMessage.java (DTO Model)",
         "In-memory Data Transfer Object used by WebSockets (not mapped to DB). Fields: <code>type</code> (<code>CHAT</code>, <code>JOIN</code>, <code>LEAVE</code>), "
         "<code>sender</code>, <code>content</code>, <code>timestamp</code>, <code>room</code>.")
    ]

    for name, desc in entities:
        t_data = [[
            Paragraph(f"<b>{name}</b>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 4. DATA ACCESS LAYER (JPA REPOSITORIES)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Data Access Layer (Spring Data Repositories)", h1_style))
    story.append(Paragraph(
        "All repositories reside in <code>com.hotspotchat.repository</code> and extend <code>JpaRepository&lt;Entity, ID&gt;</code>. "
        "Spring dynamically generates optimized SQL queries from method names at runtime.",
        body_style
    ))

    repos = [
        ("UserRepository.java", "• <code>findByEmail(String email)</code>: Retrieves user by email.<br/>• <code>existsByEmail(String email)</code>: Fast existence verification."),
        ("ChannelRepository.java", "• <code>findByName(String name)</code>: Look up network by name.<br/>• <code>existsByName(String name)</code>: Validates unique channel naming."),
        ("SubChannelRepository.java", "• <code>findByChannelId(Long channelId)</code>: Returns all sub-channels under a specific root network.<br/>• <code>deleteByChannelId(Long id)</code>: Cascade deletion helper."),
        ("ChannelMemberRepository.java", "• <code>findByUserAndChannel(User, Channel)</code>: Checks user membership in a channel.<br/>• <code>existsByUserAndIsAdminTrue(User)</code>: Crucial for role demotion logic—checks if user is a Master Admin in <i>any</i> channel.<br/>• <code>findByChannelAndIsBannedFalse(Channel)</code>: Retrieves active non-banned members."),
        ("SubChannelAdminRepository.java", "• <code>findBySubChannelId(Long id)</code>: Retrieves all admins assigned to a sub-channel.<br/>• <code>existsByUserAndSubChannel(User, SubChannel)</code>: Checks specific admin assignment.<br/>• <code>existsByUser(User)</code>: Checks if a user is an admin of <i>any</i> sub-channel anywhere.")
    ]

    for name, desc in repos:
        t_data = [[
            Paragraph(f"<b>{name}</b>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 5. NETWORK SECURITY & AUTHENTICATION SERVICES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Network Gatekeeper, Authentication & Sessions", h1_style))

    security_classes = [
        ("NetworkUtils.java", "src/main/java/com/hotspotchat/service/NetworkUtils.java",
         "Validates the physical network location of connecting devices.<br/>"
         "• <code>isHostDevice(HttpServletRequest request)</code>: Inspects <code>request.getRemoteAddr()</code> against <code>127.0.0.1</code>, "
         "<code>::1</code>, and all local network interface addresses of the server. Only the physical computer running the Spring Boot server qualifies as the Host.<br/>"
         "• <code>isCampusIp(String ip)</code>: Verifies that the client IP starts with <code>10.</code> (campus <code>10.0.0.0/8</code> network) or is a local loopback."),
        ("PageController.java", "src/main/java/com/hotspotchat/controller/PageController.java",
         "The root HTTP router for <code>GET /</code>. Uses <code>NetworkUtils.isHostDevice()</code>. If accessed from the server machine itself, "
         "it redirects to <code>admin.html</code> (Network Management Dashboard). If accessed from any other client device on the Wi-Fi, it directs to <code>index.html</code> (User Login)."),
        ("UserService.java", "src/main/java/com/hotspotchat/service/UserService.java",
         "Handles user lifecycle.<br/>"
         "• <code>findOrCreate(email)</code>: Finds an existing user or creates a new one.<br/>"
         "• <code>parseDisplayName(email)</code>: Extracts human-readable names from institutional email addresses (e.g. <code>harsh.jha23@uni.edu</code> &rarr; <b>Harsh Jha</b>).<br/>"
         "• <code>promoteToAdmin(email)</code> and <code>demoteToUser(email)</code>: Toggles global user roles."),
        ("SessionService.java", "src/main/java/com/hotspotchat/service/SessionService.java",
         "High-performance in-memory session manager using a <code>ConcurrentHashMap&lt;String, SessionData&gt;</code>.<br/>"
         "• When a user logs in, generates a cryptographically random UUID token (e.g. <code>a7f8e3...</code>) returned to the client and stored in <code>sessionStorage</code>.<br/>"
         "• Each session stores <code>userId</code>, <code>email</code>, <code>displayName</code>, <code>role</code>, and an 8-hour expiry timestamp.<br/>"
         "• All REST APIs authenticate callers via the <code>X-Session-Token</code> HTTP header."),
        ("AuthController.java", "src/main/java/com/hotspotchat/controller/AuthController.java",
         "REST controller for user access.<br/>"
         "• <code>POST /api/auth/login</code>: Accepts <code>{ email }</code>, validates domain format, calls <code>findOrCreate()</code>, creates session token.<br/>"
         "• <code>GET /api/auth/check-session</code>: Validates token validity from <code>X-Session-Token</code> header.<br/>"
         "• <code>POST /api/auth/logout</code>: Invalidates the token.")
    ]

    for name, path, desc in security_classes:
        t_data = [[
            Paragraph(f"<b>{name}</b><br/><font color='#64748B'>Path: {path}</font>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 6. BUSINESS LOGIC & CHANNEL SERVICE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Channel & Admin Management Business Logic", h1_style))

    biz_classes = [
        ("ChannelService.java", "src/main/java/com/hotspotchat/service/ChannelService.java",
         "<b>The core business brain of CampiFi.</b> Manages all channel operations:<br/>"
         "• <code>createChannel(name, desc, type, pin)</code>: Creates root network. If type is <code>PRIVATE</code>, hashes the 4-digit PIN using SHA-256 before saving.<br/>"
         "• <code>hashPin(pin)</code>: Computes <code>MessageDigest.getInstance(\"SHA-256\")</code>. Raw PINs are never stored in the database.<br/>"
         "• <code>verifyPin(channelId, inputPin)</code>: Hashes input and compares it with <code>channel.getPinHash()</code>.<br/>"
         "• <code>joinChannel(channelId, user, pin)</code>: Validates PIN if private, ensures user is not banned, creates <code>ChannelMember</code>.<br/>"
         "• <code>addChannelAdmin(channelId, email)</code>: Promotes user to Master Admin for that channel and elevates global role to <code>ADMIN</code>.<br/>"
         "• <code>removeChannelAdmin(channelId, userId)</code>: Sets <code>ChannelMember.isAdmin = false</code> and triggers <code>downgradeRoleIfNoAdminRoles()</code>.<br/>"
         "• <code>addSubChannelAdmin(subChannelId, email)</code>: Saves <code>SubChannelAdmin</code> record, elevates user role to <code>ADMIN</code>.<br/>"
         "• <code>removeSubChannelAdmin(subChannelId, userId)</code>: Deletes admin record and triggers <code>downgradeRoleIfNoAdminRoles()</code>.<br/>"
         "• <b><code>downgradeRoleIfNoAdminRoles(User user)</code> (Critical Bugfix):</b> Verifies if user is still a Master Admin anywhere (<code>existsByUserAndIsAdminTrue</code>) "
         "OR still a sub-channel admin anywhere (<code>existsByUser</code>). If both are false, safely revokes global role back to <code>USER</code>."),
        ("AdminChannelController.java", "src/main/java/com/hotspotchat/controller/AdminChannelController.java",
         "Host-only REST endpoints under <code>/api/admin/**</code>. Every endpoint strictly checks <code>networkUtils.isHostDevice(request)</code>, "
         "returning HTTP 403 Forbidden to any client trying to call admin APIs remotely.<br/>"
         "• <code>POST /api/admin/channels</code>: Create network.<br/>"
         "• <code>DELETE /api/admin/channels/{id}</code>: Delete network.<br/>"
         "• <code>POST /api/admin/channels/{id}/sub-channels</code>: Create sub-channel.<br/>"
         "• <code>POST /api/admin/channels/{id}/admins</code>: Assign Master Admin.<br/>"
         "• <code>DELETE /api/admin/channels/{id}/admins/{uid}</code>: Remove Master Admin.<br/>"
         "• <code>POST /api/admin/sub-channels/{id}/admins</code>: Assign Sub-Channel Admin.<br/>"
         "• <code>DELETE /api/admin/sub-channels/{id}/admins/{uid}</code>: Remove Sub-Channel Admin."),
        ("ChannelController.java", "src/main/java/com/hotspotchat/controller/ChannelController.java",
         "Student/client REST endpoints under <code>/api/channels/**</code>. Requires valid <code>X-Session-Token</code> header.<br/>"
         "• <code>GET /api/channels</code>: Returns all network summaries.<br/>"
         "• <code>POST /api/channels/{id}/verify-pin</code>: Checks PIN.<br/>"
         "• <code>POST /api/channels/{id}/join</code>: Joins channel.<br/>"
         "• <code>GET /api/channels/{id}/sub-channels</code>: Returns sub-channels (verifies membership for private channels).<br/>"
         "• <code>POST /api/channels/{id}/leave</code>: Leaves channel.")
    ]

    for name, path, desc in biz_classes:
        t_data = [[
            Paragraph(f"<b>{name}</b><br/><font color='#64748B'>Path: {path}</font>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 7. REAL-TIME WEBSOCKET MESSAGING ENGINE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("7. Real-Time WebSocket & STOMP Messaging Engine", h1_style))

    ws_classes = [
        ("WebSocketConfig.java", "src/main/java/com/hotspotchat/config/WebSocketConfig.java",
         "Annotated with <code>@Configuration</code> and <code>@EnableWebSocketMessageBroker</code>. Implements <code>WebSocketMessageBrokerConfigurer</code>.<br/>"
         "• <code>configureMessageBroker()</code>: Enables an in-memory STOMP message broker on prefix <code>/topic</code>. Sets application destination prefix to <code>/app</code>.<br/>"
         "• <code>registerStompEndpoints()</code>: Registers the handshake endpoint <code>/ws</code>. Adds <code>.withSockJS()</code> so that if standard WebSockets are blocked "
         "by network firewalls or older browsers, it gracefully falls back to XHR streaming or long-polling."),
        ("ChatController.java", "src/main/java/com/hotspotchat/controller/ChatController.java",
         "WebSocket STOMP message handler.<br/>"
         "• <code>@MessageMapping(\"/chat/{room}\")</code>: Receives messages sent by clients to <code>/app/chat/{room}</code>.<br/>"
         "• <code>@SendTo(\"/topic/room/{room}\")</code>: Broadcasts the processed message to all clients subscribed to that room.<br/>"
         "• Attaches server-side timestamp formatted as <code>HH:mm:ss</code> to prevent client clock tampering.")
    ]

    for name, path, desc in ws_classes:
        t_data = [[
            Paragraph(f"<b>{name}</b><br/><font color='#64748B'>Path: {path}</font>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 8. FRONTEND ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("8. Frontend Architecture & User Interface", h1_style))

    fe_files = [
        ("index.html (Client Connect)", "Clean, modern entry page. Contains single institution email input field. On submit, calls <code>/api/auth/login</code>, "
         "stores the session token in <code>sessionStorage</code>, and redirects the student to <code>channels.html</code>."),
        ("channels.html (Network Directory)", "Displays responsive cards for all campus networks. Shows name, member count, public/private badge. "
         "Clicking a private network opens a 4-box PIN modal. Once joined, an accordion panel slides open displaying all available sub-networks with a 'Chat' launch button."),
        ("admin.html (Host Management Dashboard)", "Dedicated host server dashboard. Shows all networks with toggle arrows (▶/▼) expanding child sub-channels. "
         "Features 'Admins' button on each network and sub-channel opening an admin assignment modal to add/remove professors by institutional email."),
        ("chat.html (Live Chat Room)", "The real-time conversation screen. Features topbar with channel name and live member count, an active member presence strip, "
         "scrollable chat message container with distinct sender bubbles, and bottom text input."),
        ("app.js (Unified Client Logic)", "Drives all client behavior in ~900 lines of structured vanilla JS:<br/>"
         "• <code>initHomepage()</code>: Login form handling.<br/>"
         "• <code>initChannelsPage()</code>: Renders network cards, PIN modal logic, sub-channel expanders.<br/>"
         "• <code>initAdminDashboard()</code>: Network CRUD, accordion toggling, admin assignment modal.<br/>"
         "• <code>initChat(room, user)</code>: Connects SockJS + STOMP, subscribes to <code>/topic/room/{room}</code>, renders messages, tracks presence."),
        ("style.css (Design System)", "Comprehensive dark-mode stylesheet. Defines CSS variables for background (<code>#0d1117</code>), surface (<code>#161b22</code>), "
         "accent purple (<code>#8957e5</code>), green (<code>#238636</code>), and red (<code>#da3633</code>). Responsive grid layouts, keyframe animations, and modal overlays.")
    ]

    for name, desc in fe_files:
        t_data = [[
            Paragraph(f"<b>{name}</b>", code_title_style),
        ], [
            Paragraph(desc, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 5))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # 9. VIVA & PRESENTATION QUESTIONS & ANSWERS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("9. Key Technical Viva & Presentation Q&A", h1_style))

    qas = [
        ("Q1: Why use WebSockets instead of normal HTTP polling?",
         "<b>Answer:</b> HTTP polling creates massive overhead because the client must constantly send new HTTP request headers every few seconds. "
         "WebSockets establish a single persistent full-duplex TCP connection. Once the handshake is complete, messages travel with negligible header overhead (<6 bytes) "
         "and are pushed instantly from the server without waiting for client requests."),
        ("Q2: What is STOMP and why do we need it over raw WebSockets?",
         "<b>Answer:</b> Raw WebSockets only transmit raw strings or byte arrays; they don't define headers, message types, or routing. STOMP (Simple Text Oriented Messaging Protocol) "
         "adds a standardized framing layer (<code>CONNECT</code>, <code>SUBSCRIBE</code>, <code>SEND</code>, <code>MESSAGE</code>). This enables publish/subscribe topic channels "
         "(e.g. <code>/topic/room/{name}</code>) so multiple isolated chat rooms can run over one single WebSocket connection."),
        ("Q3: How does the system work without internet access?",
         "<b>Answer:</b> The server device runs an embedded Tomcat instance and MySQL locally on the campus Wi-Fi or mobile hotspot. The server machine has a local IP (e.g. <code>10.5.4.55</code>). "
         "Clients connect directly to this local IP via Wi-Fi. All assets (HTML, CSS, JS, SockJS, STOMP libraries) are stored locally in the project JAR, eliminating any external CDN calls."),
        ("Q4: How is private channel security enforced?",
         "<b>Answer:</b> Private channels use a 4-digit PIN hashed using <b>SHA-256</b>. The database never stores the plaintext PIN. When a user enters a PIN, the backend hashes the input "
         "and compares the hashes. Once verified, a <code>ChannelMember</code> record is created in MySQL, granting persistent access."),
        ("Q5: How does the dual-tier admin system prevent privilege leaks?",
         "<b>Answer:</b> When a Master Admin or Sub-Channel Admin is removed, the system calls <code>downgradeRoleIfNoAdminRoles()</code> in <code>ChannelService</code>. "
         "It checks if the user is still a Master Admin of any other channel (<code>existsByUserAndIsAdminTrue</code>) or Sub-Channel Admin of any other sub-channel (<code>existsByUser</code>). "
         "Only if both checks return false is their global <code>User.role</code> revoked back to standard <code>USER</code>.")
    ]

    for q, a in qas:
        t_data = [[
            Paragraph(f"<b>{q}</b>", ParagraphStyle('QStyle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=c_primary)),
        ], [
            Paragraph(a, code_desc_style)
        ]]
        t = Table(t_data, colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_bg),
            ('BOX', (0,0), (-1,-1), 1, c_card_border),
            ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(KeepTogether(t))
        story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == "__main__":
    out_path = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/CampiFi_Complete_Project_Guide.pdf"
    build_pdf(out_path)
