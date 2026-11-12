import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
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
        self.drawString(54, 755, "CAMPIFI — System Architecture, UML & Technical Diagrams Guide")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 755, "Software Design & Engineering Models")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)

        # Bottom Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "CampiFi Project Evaluation Reference")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_architecture_pdf(filename):
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
    c_secondary = colors.HexColor("#3B82F6")
    c_dark = colors.HexColor("#0F172A")
    c_muted = colors.HexColor("#475569")
    c_bg = colors.HexColor("#F8FAFC")
    c_card_border = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=c_muted,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=c_muted,
        alignment=1,
        spaceAfter=8
    )

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # TITLE & INTRO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CampiFi — System Architecture & UML Diagrams Guide", title_style))
    story.append(Paragraph("Formal Software Engineering Diagrams, Class Relationships, Component Interactions & Network Models", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=10))

    intro_p = Paragraph(
        "This document provides the formal software architecture, UML class models, sequence flows, protocol interactions, "
        "and database ER diagrams for <b>CampiFi</b>. Each diagram represents key architectural decisions that enable off-grid, "
        "high-concurrency campus messaging with zero internet dependency.",
        body_style
    )
    story.append(intro_p)
    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 1: MULTI-TIER SYSTEM ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Multi-Tier Layered System Architecture", h1_style))
    story.append(Paragraph(
        "CampiFi follows a clean <b>5-Tier Architecture</b> designed for strict separation of concerns, maintainability, and security. "
        "Each layer only communicates with adjacent layers via defined interfaces and REST/WebSocket protocols.",
        body_style
    ))

    arch_img_path = os.path.join(DIAGRAMS_DIR, "system_architecture.png")
    if os.path.exists(arch_img_path):
        story.append(Image(arch_img_path, width=6.8*inch, height=5.5*inch))
        story.append(Paragraph("Figure 1: Multi-Tier Layered Architecture of CampiFi", caption_style))

    arch_breakdown = [
        ("Tier 1: Presentation Layer", "Browser-based client interface using HTML5, CSS3, and modern vanilla JavaScript. Connects to backend REST APIs using Fetch/XHR and establishes persistent full-duplex communication using SockJS and STOMP client libraries."),
        ("Tier 2: Network Gatekeeper", "Intercepts inbound HTTP connections. Validates client IP against the campus hotspot subnet (<code>10.0.0.0/8</code>) via <code>NetworkUtils</code>. Dynamically routes Host server traffic to <code>admin.html</code> and student devices to <code>index.html</code> via <code>PageController</code>."),
        ("Tier 3: Controller & Protocol Dispatcher", "Handles incoming HTTP REST endpoints (<code>AuthController</code>, <code>ChannelController</code>, <code>AdminChannelController</code>) and WebSocket frame mappings (<code>ChatController</code>). Validates input payloads and authenticates requests via <code>X-Session-Token</code> headers."),
        ("Tier 4: Service & Business Logic Layer", "Houses core application logic: user display-name extraction (<code>UserService</code>), in-memory session token lifecycle management (<code>SessionService</code>), SHA-256 PIN cryptography, and dual-tier admin promotion/revocation rules (<code>ChannelService</code>)."),
        ("Tier 5: Data Persistence Layer", "Spring Data JPA with Hibernate ORM translates repository operations into parameterized SQL statements executed via JDBC against a local MySQL 8.4 database running on port 3306.")
    ]

    for title, desc in arch_breakdown:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: UML DOMAIN CLASS DIAGRAM
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("2. UML Domain Entity Class Diagram", h1_style))
    story.append(Paragraph(
        "The object-oriented data model uses JPA entity mappings to define tables, attributes, primary/foreign keys, and cardinalities. "
        "Instead of unmanaged direct Many-to-Many collections, explicit association entities (<code>ChannelMember</code> and <code>SubChannelAdmin</code>) "
        "are used to store administrative flags, ban states, and metadata.",
        body_style
    ))

    uml_img_path = os.path.join(DIAGRAMS_DIR, "uml_class_diagram.png")
    if os.path.exists(uml_img_path):
        story.append(Image(uml_img_path, width=6.8*inch, height=5.4*inch))
        story.append(Paragraph("Figure 2: UML Class Diagram Representing Core Domain Entities & Relationships", caption_style))

    uml_explanations = [
        ("User (Entity)", "Represents a university student or faculty member. Identified by unique institutional email. Has a <code>Role</code> (<code>USER</code> or <code>ADMIN</code>). One User can belong to many channels through <code>ChannelMember</code> and administer multiple sub-channels through <code>SubChannelAdmin</code>."),
        ("Channel (Root Network Entity)", "Represents a primary campus network (e.g. <i>CSE Department</i>). Can be <code>PUBLIC</code> (open) or <code>PRIVATE</code> (protected by a 4-digit PIN stored as a SHA-256 hash in <code>pinHash</code>). Has a 1-to-Many composition relationship with <code>SubChannel</code>."),
        ("SubChannel (Entity)", "Nested rooms under a parent network (e.g. <i>Batch A</i>, <i>Faculty Lounge</i>). Contains a <code>@ManyToOne</code> foreign key back to parent <code>Channel</code>. Sub-channels allow granular discussions without polluting root channels."),
        ("ChannelMember (Association Entity)", "Resolves the Many-to-Many relationship between <code>User</code> and <code>Channel</code>. Holds attributes: <code>isAdmin</code> (marks the user as a Master Admin of the channel) and <code>isBanned</code> (restricts access)."),
        ("SubChannelAdmin (Association Entity)", "Explicit mapping that assigns a <code>User</code> as an administrator of a specific <code>SubChannel</code>. Enables professors or student leads to moderate individual class groups without granting them master privileges over the entire department.")
    ]

    for title, desc in uml_explanations:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: SEQUENCE DIAGRAM (PRIVATE NETWORK PIN AUTH)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Interaction Sequence Diagram: Private Channel Join Flow", h1_style))
    story.append(Paragraph(
        "This sequence diagram illustrates the lifecycle of a user attempting to access a PIN-protected private network. "
        "It details client-server interaction, cryptographic hashing, database queries, and response dispatch.",
        body_style
    ))

    seq_img_path = os.path.join(DIAGRAMS_DIR, "sequence_diagram_pin.png")
    if os.path.exists(seq_img_path):
        story.append(Image(seq_img_path, width=6.8*inch, height=5.2*inch))
        story.append(Paragraph("Figure 3: Sequence Diagram for Private Channel PIN Authentication & Join", caption_style))

    seq_steps = [
        ("1. User Input:", "User clicks a private network on <code>channels.html</code>. A 4-digit PIN prompt appears. Entering the PIN sends an AJAX <code>POST /api/channels/{id}/join</code> with payload <code>{ pin: '1234' }</code> and <code>X-Session-Token</code> header."),
        ("2. Controller Routing:", "<code>ChannelController</code> authenticates the session token via <code>SessionService</code>, extracts user details, and invokes <code>ChannelService.joinChannel()</code>."),
        ("3. Database Query:", "<code>ChannelService</code> fetches the channel record from <code>ChannelRepository</code> by ID, retrieving the stored <code>pinHash</code>."),
        ("4. Cryptographic Hashing:", "The service computes <code>SHA-256(inputPin)</code> and verifies if the resulting hex string exactly matches <code>channel.getPinHash()</code>. Plaintext PINs are never saved or compared directly."),
        ("5. Membership Persistence:", "Upon a valid hash match and verification that the user is not banned, a new <code>ChannelMember</code> record is persisted in MySQL via <code>ChannelMemberRepository.save()</code>."),
        ("6. Response Dispatch:", "The controller returns HTTP 200 OK with the child <code>subChannels</code> array. The frontend expands the channel accordion, enabling the 'Chat' button.")
    ]

    for title, desc in seq_steps:
        story.append(Paragraph(f"• <b>{title}</b> {desc}", bullet_style))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4: REAL-TIME WEBSOCKET & STOMP MESSAGING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Real-Time WebSocket & STOMP Protocol Architecture", h1_style))
    story.append(Paragraph(
        "Standard HTTP request-response architecture is inefficient for real-time group chat because it requires polling. "
        "CampiFi implements full-duplex TCP communication using <b>WebSockets</b> with <b>STOMP</b> framing and <b>SockJS</b> fallback.",
        body_style
    ))

    ws_img_path = os.path.join(DIAGRAMS_DIR, "websocket_architecture.png")
    if os.path.exists(ws_img_path):
        story.append(Image(ws_img_path, width=6.8*inch, height=5.0*inch))
        story.append(Paragraph("Figure 4: Full-Duplex WebSocket STOMP Publish-Subscribe Messaging Architecture", caption_style))

    ws_points = [
        ("SockJS Handshake (/ws):", "The client initiates an HTTP handshake at <code>/ws</code>. If supported, the connection upgrades to a persistent WebSocket TCP stream. If restricted by firewalls, SockJS automatically falls back to HTTP streaming or long-polling."),
        ("STOMP Over WebSocket:", "STOMP adds standard messaging semantics (<code>CONNECT</code>, <code>SUBSCRIBE</code>, <code>SEND</code>). Client A subscribes to <code>/topic/room/CSE Core</code>. Client B subscribes to the same topic."),
        ("In-Memory Message Broker:", "When Client A types a message and clicks Send, a STOMP <code>SEND</code> frame is dispatched to <code>/app/chat/CSE Core</code>. Spring's <code>ChatController</code> receives the payload, assigns a tamper-proof server timestamp, and publishes it to <code>/topic/room/CSE Core</code>."),
        ("Sub-10ms Latency:", "Spring's in-memory broker immediately fans out the message to all active subscribers. The message is rendered inside the chat bubble in real time without refreshing the page.")
    ]

    for title, desc in ws_points:
        story.append(Paragraph(f"• <b>{title}</b> {desc}", bullet_style))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5: DATABASE SCHEMA & ER DIAGRAM
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Relational Database Schema & Entity-Relationship (ER) Model", h1_style))
    story.append(Paragraph(
        "The relational database schema is normalized to Third Normal Form (3NF) to eliminate data redundancy and maintain "
        "referential integrity across users, channels, sub-channels, and roles.",
        body_style
    ))

    er_img_path = os.path.join(DIAGRAMS_DIR, "er_diagram.png")
    if os.path.exists(er_img_path):
        story.append(Image(er_img_path, width=6.8*inch, height=5.2*inch))
        story.append(Paragraph("Figure 5: Entity-Relationship (ER) Diagram of the MySQL Database Schema", caption_style))

    er_points = [
        ("Table 'users':", "Stores primary user identity. <code>id</code> is the Auto-Increment Primary Key. <code>email</code> has a UNIQUE constraint. <code>role</code> is stored as an ENUM (<code>'USER'</code>, <code>'ADMIN'</code>)."),
        ("Table 'channels':", "Stores root networks. <code>name</code> is UNIQUE. <code>type</code> is an ENUM (<code>'PUBLIC'</code>, <code>'PRIVATE'</code>). <code>pin_hash</code> stores the 64-character SHA-256 hash string."),
        ("Table 'sub_channels':", "Represents child channels. <code>channel_id</code> is a Foreign Key referencing <code>channels.id</code> with cascading delete options."),
        ("Table 'channel_members':", "Join table representing channel membership. <code>user_id</code> references <code>users.id</code>; <code>channel_id</code> references <code>channels.id</code>. <code>is_admin</code> designates Master Admins."),
        ("Table 'sub_channel_admins':", "Explicit admin mapping table. <code>user_id</code> references <code>users.id</code>; <code>sub_channel_id</code> references <code>sub_channels.id</code>. Supports clean role delegation and removal.")
    ]

    for title, desc in er_points:
        story.append(Paragraph(f"• <b>{title}</b> {desc}", bullet_style))

    story.append(Spacer(1, 10))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6: PHYSICAL NETWORK TOPOLOGY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Physical Network Deployment & Campus Hotspot Topology", h1_style))
    story.append(Paragraph(
        "CampiFi is physically deployed as an autonomous local edge system. The host computer acts as both the wireless router / access point "
        "and the application server, requiring no upstream internet gateway.",
        body_style
    ))

    topo_data = [
        [
            Paragraph("<b>Component</b>", ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
            Paragraph("<b>Network Configuration</b>", ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white)),
            Paragraph("<b>Role in CampiFi</b>", ParagraphStyle('TH', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.white))
        ],
        [
            Paragraph("<b>Host Machine (Server)</b>", body_style),
            Paragraph("IP: <code>10.5.4.55</code> (or <code>127.0.0.1</code>)<br/>Port: <code>8080</code> (Tomcat), <code>3306</code> (MySQL)", body_style),
            Paragraph("Runs Spring Boot, embedded Tomcat, MySQL server, and the <code>admin.html</code> management dashboard.", body_style)
        ],
        [
            Paragraph("<b>Campus Wi-Fi / Hotspot</b>", body_style),
            Paragraph("Subnet: <code>10.0.0.0/8</code> (Campus LAN)<br/>Broadcast: <code>10.255.255.255</code>", body_style),
            Paragraph("Provides local Layer 2 / Layer 3 connectivity without requiring WAN/Internet routing.", body_style)
        ],
        [
            Paragraph("<b>Student & Faculty Clients</b>", body_style),
            Paragraph("DHCP Range: <code>10.x.x.x</code><br/>Browser: Chrome, Safari, Firefox", body_style),
            Paragraph("Connects directly to <code>http://10.5.4.55:8080/</code>. Uses <code>index.html</code>, <code>channels.html</code>, and <code>chat.html</code>.", body_style)
        ]
    ]

    topo_table = Table(topo_data, colWidths=[130, 160, 214])
    topo_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('BOX', (0,0), (-1,-1), 1, c_card_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_card_border),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether(topo_table))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Architecture PDF generated at: {filename}")

if __name__ == "__main__":
    out_pdf = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/CampiFi_System_Architecture_and_UML_Diagrams.pdf"
    build_architecture_pdf(out_pdf)
