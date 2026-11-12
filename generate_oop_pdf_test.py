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
        self.drawString(54, 755, "CAMPIFI — Object-Oriented Programming (OOP) Implementation Guide")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 755, "Academic Viva & Technical Evaluation")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)

        # Bottom Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "CampiFi — Java & Spring Boot OOP Reference")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_oop_pdf(filename):
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
    c_secondary = colors.HexColor("#2563EB")
    c_dark = colors.HexColor("#0F172A")
    c_muted = colors.HexColor("#475569")
    c_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=c_primary,
        spaceAfter=5
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14.5,
        textColor=c_muted,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=c_primary,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=c_dark,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=12,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=3
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10.5,
        textColor=c_muted,
        alignment=1,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=10.2,
        textColor=colors.HexColor("#1E293B")
    )

    viva_q_style = ParagraphStyle(
        'VivaQ',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#9A3412")
    )

    viva_a_style = ParagraphStyle(
        'VivaA',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#1E293B")
    )

    def make_code_card(title, code_text):
        hdr = Paragraph(f"<b>Code File: {title}</b>", ParagraphStyle('CodeHdr', fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor("#1E3A8A")))
        body = Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
        t = Table([[hdr], [body]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 7),
            ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ]))
        return t

    def make_viva_card(question, answer):
        q_p = Paragraph(f"<b>Examiner / Viva Question:</b> {question}", viva_q_style)
        a_p = Paragraph(f"<b>How to Answer:</b> {answer}", viva_a_style)
        t = Table([[q_p], [a_p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFBEB")),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#FCD34D")),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor("#FDE68A")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    story = []

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1: TITLE & EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("CampiFi — Implementation of Object-Oriented Programming (OOP) Concepts", title_style))
    story.append(Paragraph("Demonstrating Classes, Objects, Encapsulation, Inheritance, Polymorphism, Abstraction & Interfaces in Java & Spring Boot", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=0, spaceAfter=8))

    intro_p = Paragraph(
        "<b>Object-Oriented Programming (OOP)</b> is the foundational paradigm of the <b>CampiFi</b> architecture. "
        "Rather than treating software as a sequence of procedural steps, CampiFi models its offline campus network "
        "around real-world domain entities (<i>Users</i>, <i>Channels</i>, <i>SubChannels</i>, <i>Messages</i>, and <i>Sessions</i>). "
        "This guide provides an academic and practical breakdown of how every core OOP principle is implemented "
        "in the live codebase, connecting theoretical computer science concepts with production Java 17 and Spring Boot design patterns.",
        body_style
    )
    story.append(intro_p)
    story.append(Spacer(1, 4))

    # Architecture Diagram on Page 1
    diag_path = os.path.join(DIAGRAMS_DIR, "oop_concepts_architecture.png")
    if os.path.exists(diag_path):
        img = Image(diag_path, width=504, height=336)
        story.append(img)
        story.append(Paragraph("<b>Figure 1:</b> Architectural Mapping of the 6 OOP Pillars across CampiFi's Java Domain Model, Service Layer, and Repositories.", caption_style))
    story.append(Spacer(1, 4))

    summary_table_data = [
        [
            Paragraph("<b>OOP Concept</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Core Purpose in CampiFi</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Concrete Java File & Reference</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))
        ],
        [
            Paragraph("<b>1. Classes & Objects</b>", body_style),
            Paragraph("Blueprints defining domain state & dynamic runtime memory allocations", body_style),
            Paragraph("<code>User.java</code>, <code>Channel.java</code>, <code>SessionData</code>", code_style)
        ],
        [
            Paragraph("<b>2. Encapsulation</b>", body_style),
            Paragraph("Data hiding via private members, controlled getters, and immutable IDs", body_style),
            Paragraph("<code>User.java</code> (no ID setter), <code>SessionService.java</code>", code_style)
        ],
        [
            Paragraph("<b>3. Inheritance</b>", body_style),
            Paragraph("Code reusability via generic interface inheritance (30+ CRUD ops)", body_style),
            Paragraph("<code>UserRepository extends JpaRepository&lt;User, Long&gt;</code>", code_style)
        ],
        [
            Paragraph("<b>4. Polymorphism</b>", body_style),
            Paragraph("Compile-time constructor overloading & runtime interface method overriding", body_style),
            Paragraph("<code>WebSocketConfig.java</code>, <code>DataInitializer.java</code>", code_style)
        ],
        [
            Paragraph("<b>5. Abstraction</b>", body_style),
            Paragraph("Hiding SQL statements, network headers & hashing behind clean APIs", body_style),
            Paragraph("<code>ChannelService.java</code>, <code>NetworkUtils.java</code>", code_style)
        ],
        [
            Paragraph("<b>6. Interfaces</b>", body_style),
            Paragraph("Pure contracts enabling loose coupling and Dependency Injection (IoC)", body_style),
            Paragraph("<code>CommandLineRunner</code>, <code>WebSocketMessageBroker...</code>", code_style)
        ]
    ]
    st_table = Table(summary_table_data, colWidths=[110, 244, 150])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(st_table)

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2: CLASSES & OBJECTS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Classes and Objects: The Building Blocks of CampiFi", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>Definition:</b> A <b>Class</b> is a user-defined template or blueprint that defines the structure, attributes (state), "
        "and behaviors (methods) common to all entities of its type. An <b>Object</b> is a concrete instance of a class "
        "created in memory at runtime that holds actual state values.",
        body_style
    ))

    story.append(Paragraph("A. Entity Class Blueprint: <code>User.java</code>", h2_style))
    story.append(Paragraph(
        "In CampiFi, <code>User.java</code> serves as the class blueprint representing participants on the offline hotspot. "
        "It defines persistent attributes mapped to the MySQL database via Jakarta Persistence annotations:",
        body_style
    ))

    code_user = (
        "@Entity\n"
        "@Table(name = \"users\")\n"
        "public class User {\n"
        "    @Id\n"
        "    @GeneratedValue(strategy = GenerationType.IDENTITY)\n"
        "    private Long id;\n\n"
        "    @Column(nullable = false, unique = true, length = 255)\n"
        "    private String email;\n\n"
        "    @Column(nullable = false, length = 100)\n"
        "    private String displayName;\n\n"
        "    @Enumerated(EnumType.STRING)\n"
        "    @Column(nullable = false)\n"
        "    private Role role = Role.USER;\n\n"
        "    @Column(nullable = false)\n"
        "    private LocalDateTime createdAt = LocalDateTime.now();\n\n"
        "    public User() {} // Required by JPA\n"
        "    public User(String email, String displayName, Role role) {\n"
        "        this.email = email;\n"
        "        this.displayName = displayName;\n"
        "        this.role = role;\n"
        "    }\n"
        "    // Getters and Setters omitted for brevity\n"
        "}"
    )
    story.append(make_code_card("src/main/java/com/hotspotchat/model/User.java", code_user))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Object Instantiation in Memory", h2_style))
    story.append(Paragraph(
        "Objects are actively created at runtime in two distinct ways throughout the application lifecycle:",
        body_style
    ))
    story.append(Paragraph("• <b>Explicit Manual Instantiation (Heap Memory):</b> Using the <code>new</code> keyword to create domain entities and transfer records. For example, in <code>DataInitializer.java</code>, startup objects are instantiated and populated into the database:", bullet_style))
    story.append(Paragraph("<code>User admin = new User(\"admin@campifi.edu\", \"Master Admin\", User.Role.ADMIN);</code>", code_style))
    story.append(Paragraph("<code>SubChannel sub = new SubChannel(\"Prof. Sharma\", \"Data Structures\", parentChannel);</code>", code_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph("• <b>Spring IoC Managed Objects (Spring Beans):</b> The Spring ApplicationContext manages singleton lifecycle instances of classes annotated with <code>@Service</code>, <code>@Repository</code>, and <code>@RestController</code>. Classes such as <code>UserService</code>, <code>ChannelService</code>, and <code>SessionService</code> are instantiated once by Spring's Inversion of Control (IoC) container and injected where needed via Dependency Injection.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Modern Java 17 Records as Immutable Objects: <code>SessionData</code>", h2_style))
    story.append(Paragraph(
        "Inside <code>SessionService.java</code>, CampiFi uses a modern Java 17 <b>record</b> as an immutable data carrier object:",
        body_style
    ))
    code_record = (
        "public record SessionData(\n"
        "    Long userId,\n"
        "    String email,\n"
        "    String displayName,\n"
        "    User.Role role,\n"
        "    LocalDateTime expiresAt\n"
        ") {}"
    )
    story.append(make_code_card("src/main/java/com/hotspotchat/service/SessionService.java (Lines 76-82)", code_record))
    story.append(Spacer(1, 5))

    story.append(make_viva_card(
        "What is the difference between a class and an object in CampiFi, and who instantiates the Service classes?",
        "A class (e.g., User.java) is the compile-time blueprint defining fields and methods. An object is the runtime instance occupying RAM (e.g., an individual student logged in). While entity objects like User and Channel are created using the 'new' operator as data arrives, Service classes (UserService, ChannelService) are singleton Beans instantiated and managed automatically by the Spring Inversion of Control (IoC) Container."
    ))

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3: ENCAPSULATION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("2. Encapsulation: Information Hiding and State Protection", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Encapsulation</b> is the principle of bundling the internal data (fields) and the code (methods) "
        "that operates on that data into a single protective unit, while strictly restricting direct external access to internal state. "
        "Encapsulation guarantees data integrity, prevents unintended side effects, and allows internal logic to change without breaking calling code.",
        body_style
    ))

    story.append(Paragraph("A. Defensive Field Access & The 'No-Setter' Principle", h2_style))
    story.append(Paragraph(
        "In <code>User.java</code>, all instance variables are declared <code>private</code>. Outside classes cannot directly "
        "read or mutate fields (e.g., <code>user.email = \"fake\"</code> produces a compiler error). Access is mediated exclusively "
        "through public getter and setter methods:",
        body_style
    ))

    code_encap_user = (
        "public class User {\n"
        "    private Long id;                  // Primary Key — managed by MySQL\n"
        "    private String email;             // Institution email\n"
        "    private LocalDateTime createdAt;  // Audit timestamp\n\n"
        "    // Controlled Access: Getters allow external reading\n"
        "    public Long getId() { return id; }\n"
        "    public String getEmail() { return email; }\n"
        "    public LocalDateTime getCreatedAt() { return createdAt; }\n\n"
        "    // Validated Modification: Only email can be updated\n"
        "    public void setEmail(String email) { this.email = email; }\n\n"
        "    // CRITICAL ENCAPSULATION DESIGN:\n"
        "    // Notice: There is NO public setId(Long id) or setCreatedAt(...)!\n"
        "    // Preventing external classes from corrupting DB keys or history.\n"
        "}"
    )
    story.append(make_code_card("Encapsulation in User.java", code_encap_user))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Sensitive State Protection: Channel PIN Hashing", h2_style))
    story.append(Paragraph(
        "Encapsulation protects sensitive security credentials in <code>Channel.java</code> and <code>ChannelService.java</code>. "
        "The raw 4-digit numeric PIN is never exposed, logged, or saved to the database. Instead, internal business logic "
        "encapsulates cryptographic hashing behind service boundaries:",
        body_style
    ))

    code_encap_pin = (
        "// In Channel.java: Encapsulated private field\n"
        "private String pinHash; // Stores 64-character SHA-256 hex string\n\n"
        "// In ChannelService.java: Business logic encapsulation\n"
        "if (type == Channel.ChannelType.PRIVATE && pin != null && !pin.isBlank()) {\n"
        "    ch.setPinHash(hashPin(pin.trim())); // Encapsulated SHA-256 routine\n"
        "}\n\n"
        "private String hashPin(String pin) {\n"
        "    MessageDigest digest = MessageDigest.getInstance(\"SHA-256\");\n"
        "    byte[] hash = digest.digest(pin.getBytes(StandardCharsets.UTF_8));\n"
        "    return bytesToHex(hash); // Internal helper remains private!\n"
        "}"
    )
    story.append(make_code_card("State Protection & Cryptographic Encapsulation", code_encap_pin))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Shielding Concurrency State in <code>SessionService.java</code>", h2_style))
    story.append(Paragraph(
        "In <code>SessionService.java</code>, the internal active session table is a <code>private final ConcurrentHashMap</code>. "
        "No outside controller can directly access, iterate over, or wipe the map. All operations must flow through "
        "encapsulated public API methods: <code>createSession()</code>, <code>getSession()</code>, and <code>invalidate()</code>.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why did you deliberately omit setter methods for 'id' and 'createdAt' in your User entity class?",
        "To enforce strict encapsulation and protect data integrity. The 'id' is a database surrogate primary key generated automatically by MySQL (IDENTITY). Allowing external code to invoke setId() could cause primary key collisions or hijack existing records. Similarly, 'createdAt' represents an immutable audit timestamp recording when the account was registered; omitting its setter guarantees audit trail tamper-resistance."
    ))

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4: INHERITANCE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Inheritance: Code Reusability & Architectural Hierarchy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Inheritance</b> is the mechanism by which one class or interface acquires the properties "
        "and behaviors (methods) of another class or interface using the <code>extends</code> keyword. "
        "Inheritance promotes massive code reuse, enforces structural consistency, and establishes an 'IS-A' relationship.",
        body_style
    ))

    story.append(Paragraph("A. Generic Interface Inheritance: <code>JpaRepository</code>", h2_style))
    story.append(Paragraph(
        "In CampiFi, all persistence repositories implement <b>Interface Inheritance</b> by extending Spring Data's "
        "<code>JpaRepository&lt;T, ID&gt;</code> interface. Look at how <code>UserRepository.java</code> is declared:",
        body_style
    ))

    code_inh_repo = (
        "@Repository\n"
        "public interface UserRepository extends JpaRepository<User, Long> {\n"
        "    // Custom query method declared via Spring Data derived naming\n"
        "    Optional<User> findByEmail(String email);\n"
        "    boolean existsByEmail(String email);\n"
        "}"
    )
    story.append(make_code_card("src/main/java/com/hotspotchat/repository/UserRepository.java", code_inh_repo))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. The Multi-Level Inheritance Hierarchy in Spring Data", h2_style))
    story.append(Paragraph(
        "By extending <code>JpaRepository&lt;User, Long&gt;</code>, the <code>UserRepository</code> interface inherits from an extensive "
        "hierarchy of standard Java interfaces without writing a single line of redundant code:",
        body_style
    ))

    story.append(Paragraph("1. <code><b>Repository&lt;T, ID&gt;</b></code> — Marker interface indicating a data access component.", bullet_style))
    story.append(Paragraph("2. <code><b>CrudRepository&lt;T, ID&gt;</b></code> (extends Repository) — Supplies core CRUD operations: <code>save()</code>, <code>findById()</code>, <code>existsById()</code>, <code>findAll()</code>, <code>deleteById()</code>, <code>count()</code>.", bullet_style))
    story.append(Paragraph("3. <code><b>PagingAndSortingRepository&lt;T, ID&gt;</b></code> (extends CrudRepository) — Adds paginated and sorted querying methods: <code>findAll(Sort)</code>, <code>findAll(Pageable)</code>.", bullet_style))
    story.append(Paragraph("4. <code><b>ListPagingAndSortingRepository&lt;T, ID&gt;</b></code> (extends PagingAndSortingRepository) — Refines return types to <code>java.util.List</code>.", bullet_style))
    story.append(Paragraph("5. <code><b>JpaRepository&lt;T, ID&gt;</b></code> (extends ListPagingAndSortingRepository) — Adds JPA-specific batching and flush operations: <code>flush()</code>, <code>saveAndFlush()</code>, <code>deleteAllInBatch()</code>.", bullet_style))
    story.append(Paragraph("6. <code><b>UserRepository</b></code> (extends JpaRepository) — Inherits all 30+ methods above for the <code>User</code> entity!", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Inheritance across All 7 Domain Repositories", h2_style))
    story.append(Paragraph(
        "CampiFi reuses this identical inheritance structure across all entity components in the application:",
        body_style
    ))

    repo_table_data = [
        [
            Paragraph("<b>Repository Interface</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Parent Interface Extended</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white)),
            Paragraph("<b>Inherited Generic Types & Key Inherited Methods</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=8, textColor=colors.white))
        ],
        [
            Paragraph("<code>UserRepository</code>", code_style),
            Paragraph("<code>JpaRepository&lt;User, Long&gt;</code>", code_style),
            Paragraph("Inherits <code>save(User)</code>, <code>findById(Long)</code>, <code>deleteById(Long)</code>", body_style)
        ],
        [
            Paragraph("<code>ChannelRepository</code>", code_style),
            Paragraph("<code>JpaRepository&lt;Channel, Long&gt;</code>", code_style),
            Paragraph("Inherits <code>count()</code>, <code>save(Channel)</code>, <code>findAll()</code>", body_style)
        ],
        [
            Paragraph("<code>SubChannelRepository</code>", code_style),
            Paragraph("<code>JpaRepository&lt;SubChannel, Long&gt;</code>", code_style),
            Paragraph("Inherits <code>save(SubChannel)</code>, <code>findById(Long)</code>", body_style)
        ],
        [
            Paragraph("<code>MessageRepository</code>", code_style),
            Paragraph("<code>JpaRepository&lt;Message, Long&gt;</code>", code_style),
            Paragraph("Inherits batching, pagination, and persistence operations", body_style)
        ]
    ]
    r_table = Table(repo_table_data, colWidths=[130, 160, 214])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#7E22CE")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(r_table)
    story.append(Spacer(1, 5))

    story.append(make_viva_card(
        "Does Java support multiple inheritance of classes? How does your project achieve multiple inheritance?",
        "Java does NOT support multiple inheritance of classes (to prevent the famous 'Diamond Problem' of conflicting method implementations). However, Java explicitly supports MULTIPLE INHERITANCE OF INTERFACES using the 'implements' keyword or by having an interface 'extend' multiple parent interfaces. In CampiFi, JpaRepository inherits from both ListCrudRepository and ListPagingAndSortingRepository, cleanly combining multiple behavioral contracts without method conflicts."
    ))

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 5: POLYMORPHISM
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Polymorphism: Compile-Time Overloading & Runtime Dynamic Overriding", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Polymorphism</b> (Greek for 'many forms') allows a single interface, method, or object "
        "to execute different behaviors depending on how it is invoked. Java implements polymorphism in two primary flavors: "
        "<b>Compile-time (Static) Polymorphism</b> via Method/Constructor Overloading, and "
        "<b>Runtime (Dynamic) Polymorphism</b> via Method Overriding and Interface Dynamic Dispatch.",
        body_style
    ))

    story.append(Paragraph("A. Compile-Time Polymorphism: Constructor Overloading", h2_style))
    story.append(Paragraph(
        "In <code>User.java</code>, multiple constructors exist with the same name but distinct parameter signatures. "
        "The Java compiler determines which constructor to invoke at compile time based on the argument list:",
        body_style
    ))

    code_poly_overload = (
        "public class User {\n"
        "    // Form 1: Default No-Argument Constructor (Required by Hibernate JPA via reflection)\n"
        "    public User() {}\n\n"
        "    // Form 2: Parameterized Constructor (Used by application code during user registration)\n"
        "    public User(String email, String displayName, Role role) {\n"
        "        this.email = email;\n"
        "        this.displayName = displayName;\n"
        "        this.role = role;\n"
        "    }\n"
        "}"
    )
    story.append(make_code_card("Constructor Overloading in User.java", code_poly_overload))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Runtime Polymorphism: Method Overriding (<code>@Override</code>)", h2_style))
    story.append(Paragraph(
        "In <b>Runtime Polymorphism</b>, a class implements an interface method, providing its own custom behavior. "
        "The Java Virtual Machine (JVM) determines which implementation to execute dynamically at runtime. "
        "Two prominent examples in CampiFi are:",
        body_style
    ))

    code_poly_override = (
        "// Example 1: Overriding WebSocket Broker Configuration\n"
        "@Configuration\n"
        "@EnableWebSocketMessageBroker\n"
        "public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {\n"
        "    @Override\n"
        "    public void configureMessageBroker(MessageBrokerRegistry config) {\n"
        "        config.enableSimpleBroker(\"/topic\");\n"
        "        config.setApplicationDestinationPrefixes(\"/app\");\n"
        "    }\n\n"
        "    @Override\n"
        "    public void registerStompEndpoints(StompEndpointRegistry registry) {\n"
        "        registry.addEndpoint(\"/ws\").setAllowedOriginPatterns(\"*\").withSockJS();\n"
        "    }\n"
        "}\n\n"
        "// Example 2: Overriding Spring Boot Startup Hook\n"
        "@Component\n"
        "public class DataInitializer implements CommandLineRunner {\n"
        "    @Override\n"
        "    public void run(String... args) {\n"
        "        // Custom startup seeding logic executed dynamically by Spring Boot\n"
        "        if (channelRepository.count() > 0) return;\n"
        "        seedDefaultCampusNetworks();\n"
        "    }\n"
        "}"
    )
    story.append(make_code_card("Dynamic Method Overriding in WebSocketConfig & DataInitializer", code_poly_override))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Dynamic Dispatch via Interface References", h2_style))
    story.append(Paragraph(
        "In <code>ChannelService.java</code>, dependencies are declared using <b>interface types</b> rather than concrete classes:",
        body_style
    ))
    story.append(Paragraph("<code>private final UserRepository userRepository; // Interface reference type</code>", code_style))
    story.append(Paragraph(
        "When <code>userRepository.save(user)</code> is called, the JVM does not execute code inside an interface (which has none). "
        "Instead, it dynamically dispatches the call to the runtime proxy instance generated by Spring (<code>SimpleJpaRepository</code>). "
        "This dynamic polymorphism enables loose coupling and makes swapping implementations seamless.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "What is the difference between Method Overloading and Method Overriding in CampiFi?",
        "Method Overloading (Compile-Time / Static) occurs when two methods in the same class share the same name but have different parameter lists (e.g., User() vs User(email, name, role)); the compiler resolves which method to invoke. Method Overriding (Runtime / Dynamic) occurs when a subclass or implementing class provides its own specific implementation of an inherited or interface method using the @Override annotation (e.g., WebSocketConfig overriding configureMessageBroker()); the JVM resolves the exact method at runtime via dynamic dispatch."
    ))

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 6: ABSTRACTION
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Abstraction: Hiding Complexity and Exposing Essentials", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Abstraction</b> is the principle of hiding complex, low-level implementation details "
        "and exposing only the essential, high-level features and operations to the caller. Abstraction allows developers "
        "to work with intuitive domain operations without getting bogged down by low-level networking, database protocols, or memory buffers.",
        body_style
    ))

    story.append(Paragraph("A. Persistence Abstraction via Spring Data JPA", h2_style))
    story.append(Paragraph(
        "Consider this single line in <code>UserRepository.java</code>:",
        body_style
    ))
    story.append(Paragraph("<code>Optional&lt;User&gt; findByEmail(String email);</code>", code_style))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "This concise method declaration is a masterclass in abstraction. Behind this single method call, Spring Data JPA and Hibernate "
        "abstract away dozens of low-level procedural steps:",
        body_style
    ))
    story.append(Paragraph("1. Opening a raw TCP socket connection to MySQL on port 3306 via the HikariCP connection pool.", bullet_style))
    story.append(Paragraph("2. Preparing the parameterized SQL statement: <code>SELECT * FROM users WHERE email = ? LIMIT 1</code>.", bullet_style))
    story.append(Paragraph("3. Binding the Java String parameter to prevent SQL injection vulnerabilities.", bullet_style))
    story.append(Paragraph("4. Executing the query across the network and reading the raw byte stream from MySQL.", bullet_style))
    story.append(Paragraph("5. Parsing the JDBC <code>ResultSet</code> rows and columns into Java primitive types.", bullet_style))
    story.append(Paragraph("6. Instantiating a new <code>User</code> entity object and populating its fields via Java reflection.", bullet_style))
    story.append(Paragraph("7. Wrapping the result in a modern Java <code>Optional&lt;User&gt;</code> container to eliminate null pointer risks.", bullet_style))
    story.append(Paragraph("The service layer simply invokes <code>userRepository.findByEmail(email)</code> without ever knowing raw SQL exists!", body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Service Layer Business Abstraction: <code>ChannelService</code>", h2_style))
    story.append(Paragraph(
        "Controllers never directly query the database or perform raw cryptographic operations. "
        "Instead, <code>ChannelService.java</code> provides high-level business abstraction methods:",
        body_style
    ))

    code_abs_service = (
        "@Transactional\n"
        "public Channel createChannel(String name, String description, Channel.ChannelType type, String pin) {\n"
        "    if (channelRepository.existsByName(name.trim())) {\n"
        "        throw new IllegalArgumentException(\"Channel name already exists.\");\n"
        "    }\n"
        "    Channel ch = new Channel();\n"
        "    ch.setName(name.trim());\n"
        "    ch.setDescription(description);\n"
        "    ch.setType(type);\n"
        "    if (type == Channel.ChannelType.PRIVATE && pin != null && !pin.isBlank()) {\n"
        "        ch.setPinHash(hashPin(pin.trim())); // PIN hashing abstracted!\n"
        "    }\n"
        "    return channelRepository.save(ch); // Transaction boundary abstracted!\n"
        "}"
    )
    story.append(make_code_card("Business Logic Abstraction in ChannelService.java", code_abs_service))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Network Hardware & IP Abstraction: <code>NetworkUtils.java</code>", h2_style))
    story.append(Paragraph(
        "Handling client IP addresses on an offline Wi-Fi hotspot involves handling reverse proxies, forwarded headers, "
        "and IPv6 loopback edge cases. <code>NetworkUtils.java</code> completely abstracts this complexity:",
        body_style
    ))

    code_abs_net = (
        "@Component\n"
        "public class NetworkUtils {\n"
        "    public String getClientIp(HttpServletRequest request) {\n"
        "        String ip = request.getHeader(\"X-Forwarded-For\");\n"
        "        if (ip != null && !ip.isEmpty() && !\"unknown\".equalsIgnoreCase(ip)) {\n"
        "            ip = ip.split(\",\")[0].trim(); // Extract first proxy hop\n"
        "        } else {\n"
        "            ip = request.getHeader(\"X-Real-IP\");\n"
        "        }\n"
        "        if (ip == null || ip.isEmpty() || \"unknown\".equalsIgnoreCase(ip)) {\n"
        "            ip = request.getRemoteAddr(); // Direct socket connection\n"
        "        }\n"
        "        if (\"::1\".equals(ip) || \"0:0:0:0:0:0:0:1\".equals(ip)) ip = \"127.0.0.1\";\n"
        "        return ip; // Caller receives a clean, normalized IPv4 address!\n"
        "    }\n"
        "}"
    )
    story.append(make_code_card("Hardware & Socket Abstraction in NetworkUtils.java", code_abs_net))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "How does Spring Data JPA demonstrate abstraction in your persistence layer?",
        "Spring Data JPA abstracts the entire database interaction. In UserRepository, we write 'Optional<User> findByEmail(String email);' without any SQL or JDBC code. Spring automatically abstracts away connection pool management, parameterized SQL generation, statement execution, JDBC ResultSet parsing, and object-relational mapping. The caller works strictly with domain objects, completely shielded from low-level database mechanics."
    ))

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 7: INTERFACES & DECOUPLING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Interfaces: Pure Contracts and Architectural Decoupling", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "<b>Definition:</b> An <b>Interface</b> in Java is a completely abstract type that acts as a pure contract, "
        "specifying <i>what</i> behaviors a class must implement without defining <i>how</i> they must be implemented. "
        "Interfaces enable loose coupling, modularity, multiple inheritance of type, and adherence to the Dependency Inversion Principle (DIP).",
        body_style
    ))

    story.append(Paragraph("A. Core Interfaces Used Across CampiFi", h2_style))
    story.append(Paragraph(
        "CampiFi leverages three fundamental interface contracts to structure its architecture:",
        body_style
    ))

    story.append(Paragraph("• <code><b>CommandLineRunner</b></code> (Spring Framework): A functional interface containing exactly one contract method: <code>void run(String... args)</code>. Any Spring Bean implementing this interface is guaranteed to execute immediately after the application context loads. Used in <code>DataInitializer.java</code> to automatically seed campus channels.", bullet_style))
    story.append(Paragraph("• <code><b>WebSocketMessageBrokerConfigurer</b></code> (Spring Messaging): An interface defining callback hooks for configuring STOMP endpoints and real-time message routing. Used in <code>WebSocketConfig.java</code>.", bullet_style))
    story.append(Paragraph("• <code><b>JpaRepository&lt;T, ID&gt;</b></code> (Spring Data): A generic contract defining standardized database operations. Implemented by all 7 repository interfaces in CampiFi.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. The Dependency Inversion Principle (DIP) in Action", h2_style))
    story.append(Paragraph(
        "One of the most important software engineering reasons for using interfaces is the <b>Dependency Inversion Principle</b> "
        "(the 'D' in SOLID): <i>High-level modules should not depend on low-level modules; both should depend on abstractions (interfaces).</i>",
        body_style
    ))

    code_dip = (
        "@Service\n"
        "public class ChannelService {\n"
        "    // DEPENDENCY INVERSION: The service depends on the INTERFACE,\n"
        "    // NOT on a concrete database implementation class!\n"
        "    private final ChannelRepository channelRepository;\n"
        "    private final UserRepository    userRepository;\n\n"
        "    @Autowired\n"
        "    public ChannelService(ChannelRepository channelRepository,\n"
        "                          UserRepository userRepository) {\n"
        "        this.channelRepository = channelRepository;\n"
        "        this.userRepository    = userRepository;\n"
        "    }\n"
        "}"
    )
    story.append(make_code_card("Dependency Inversion in ChannelService.java", code_dip))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Why this interface-driven architecture is critical for enterprise software:", body_style))
    story.append(Paragraph("1. <b>Loose Coupling:</b> <code>ChannelService</code> does not know or care whether the repository is backed by MySQL, PostgreSQL, or an in-memory H2 database.", bullet_style))
    story.append(Paragraph("2. <b>Unit Testing with Mockito:</b> In unit tests, developers can easily inject a mock repository interface (e.g., <code>Mockito.mock(UserRepository.class)</code>) to test business logic in isolation without requiring a live MySQL server running.", bullet_style))
    story.append(Paragraph("3. <b>Zero Boilerplate:</b> Interfaces eliminate thousands of lines of handwritten SQL and JDBC plumbing code.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why did you write UserRepository as an interface instead of a regular class?",
        "Because UserRepository follows the interface contract pattern of Spring Data JPA. By declaring an interface that extends JpaRepository<User, Long>, we specify WHAT database operations are needed, not HOW to implement them. At runtime, Spring dynamically generates a proxy class implementing the interface. Furthermore, depending on an interface adheres to the Dependency Inversion Principle (SOLID), decoupling our business services from database specifics and enabling effortless unit testing with mock objects."
    ))

    # story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 8: QUICK-REFERENCE MATRIX & VIVA CHEAT SHEET
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("7. OOP Master Matrix & Viva Examination Defense", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceBefore=0, spaceAfter=6))

    story.append(Paragraph(
        "Use this master reference matrix during your project evaluation to immediately point examiners "
        "to the exact file, line number, and technical justification for each OOP concept:",
        body_style
    ))

    master_matrix_data = [
        [
            Paragraph("<b>OOP Concept</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Code File & Exact Location</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Implementation Details in CampiFi</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Examiner Viva Talking Point</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white))
        ],
        [
            Paragraph("<b>Classes & Objects</b>", body_style),
            Paragraph("<code>model/User.java</code><br/><code>service/SessionService.java</code>", code_style),
            Paragraph("Domain entity blueprint; <code>SessionData</code> record; runtime instantiation via <code>new</code> & Spring Beans", body_style),
            Paragraph("Separation of compile-time structure (class) from runtime heap state (object).", body_style)
        ],
        [
            Paragraph("<b>Encapsulation</b>", body_style),
            Paragraph("<code>model/User.java</code><br/><code>model/Channel.java</code>", code_style),
            Paragraph("Private instance variables, public getters/setters, deliberate omission of <code>setId()</code> & <code>setCreatedAt()</code>", body_style),
            Paragraph("Protects database keys and audit timestamps from accidental tampering.", body_style)
        ],
        [
            Paragraph("<b>Inheritance</b>", body_style),
            Paragraph("<code>repository/UserRepository.java</code><br/><code>repository/ChannelRepository.java</code>", code_style),
            Paragraph("<code>extends JpaRepository&lt;T, ID&gt;</code> inheriting 30+ CRUD and paging methods without duplication", body_style),
            Paragraph("Multi-level interface inheritance hierarchy (Repository &rarr; CrudRepository &rarr; JpaRepository).", body_style)
        ],
        [
            Paragraph("<b>Polymorphism (Static)</b>", body_style),
            Paragraph("<code>model/User.java</code><br/><code>model/ChatMessage.java</code>", code_style),
            Paragraph("Constructor overloading: <code>User()</code> (JPA reflection) vs <code>User(email, name, role)</code> (custom)", body_style),
            Paragraph("Compile-time polymorphism resolved by the compiler via parameter signature matching.", body_style)
        ],
        [
            Paragraph("<b>Polymorphism (Dynamic)</b>", body_style),
            Paragraph("<code>config/WebSocketConfig.java</code><br/><code>DataInitializer.java</code>", code_style),
            Paragraph("Method overriding via <code>@Override configureMessageBroker()</code> and <code>@Override run()</code>", body_style),
            Paragraph("Runtime polymorphism resolved dynamically by the JVM via dynamic dispatch.", body_style)
        ],
        [
            Paragraph("<b>Abstraction</b>", body_style),
            Paragraph("<code>repository/UserRepository.java</code><br/><code>service/NetworkUtils.java</code>", code_style),
            Paragraph("<code>findByEmail()</code> hides raw SQL, JDBC & socket pools; <code>getClientIp()</code> hides HTTP proxies", body_style),
            Paragraph("Hides low-level complexity behind clean, intuitive domain interfaces.", body_style)
        ],
        [
            Paragraph("<b>Interfaces</b>", body_style),
            Paragraph("<code>CommandLineRunner</code><br/><code>WebSocketMessageBroker...</code>", code_style),
            Paragraph("Pure contracts implemented by service components; enables Dependency Inversion (DIP)", body_style),
            Paragraph("Enables loose coupling and seamless unit testing with mock objects.", body_style)
        ]
    ]

    m_table = Table(master_matrix_data, colWidths=[90, 130, 154, 130])
    m_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(m_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("Top 4 'Golden Rules' to Remember for Your Project Defense", h2_style))
    story.append(Paragraph("1. <b>Always pair the concept with a specific file:</b> Never just say 'we used encapsulation'—say <i>'We implemented encapsulation in User.java by declaring all fields private and deliberately omitting setId() to prevent database key tampering.'</i>", bullet_style))
    story.append(Paragraph("2. <b>Distinguish Compile-Time from Runtime:</b> When asked about polymorphism, immediately clarify that CampiFi uses BOTH: constructor overloading at compile time, and interface method overriding (WebSocketConfig) at runtime.", bullet_style))
    story.append(Paragraph("3. <b>Emphasize Abstraction vs Encapsulation:</b> <i>Encapsulation</i> is about <b>data protection</b> (hiding state inside a class). <i>Abstraction</i> is about <b>complexity reduction</b> (hiding how a feature is implemented behind a simple method like findByEmail).", bullet_style))
    story.append(Paragraph("4. <b>Highlight the Dependency Inversion Principle:</b> Show that your service classes inject repository <i>interfaces</i>, not concrete classes, proving clean architectural decoupling.", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"OOP Guide PDF successfully generated at: {filename}")

if __name__ == '__main__':
    target = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/CampiFi_OOP_Concepts_Implementation_Guide.pdf"
    build_oop_pdf(target)
