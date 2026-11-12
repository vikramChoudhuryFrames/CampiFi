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
        self.drawString(54, 755, "CAMPIFI — Advanced Java Concepts, Concurrency & Security Guide")
        self.setFont("Helvetica", 8)
        self.drawRightString(558, 755, "Technical Evaluation & Viva Reference")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 747, 558, 747)

        # Bottom Running Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "CampiFi — Production Concurrency, Streams & Cryptography")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_str)
        self.restoreState()

def build_advanced_java_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    c_primary = colors.HexColor("#0F172A")
    c_blue = colors.HexColor("#0369A1")
    c_dark = colors.HexColor("#1E293B")
    c_muted = colors.HexColor("#475569")
    c_bg = colors.HexColor("#F8FAFC")
    c_border = colors.HexColor("#E2E8F0")

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
        textColor=c_dark,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=c_dark,
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
        hdr = Paragraph(f"<b>Code Reference: {title}</b>", ParagraphStyle('CodeHdr', fontName='Helvetica-Bold', fontSize=7.8, textColor=colors.HexColor("#0369A1")))
        body = Paragraph(code_text.replace('\n', '<br/>').replace(' ', '&nbsp;'), code_style)
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
    story.append(Paragraph("CampiFi — Advanced Java Concepts, Concurrency & Security Guide", title_style))
    story.append(Paragraph("Demonstrating Multithreading, Thread-Safe Collections, Generics, Java Streams, Exception Handling & Cryptography", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_primary, spaceBefore=0, spaceAfter=6))

    intro_p = Paragraph(
        "Modern enterprise software demands far more than basic object modeling. In <b>CampiFi</b>, an offline "
        "campus chat system operating under high-concurrency hotspot conditions, several <b>Advanced Java Concepts</b> "
        "and <b>Cutting-Edge Engineering Disciplines</b> are actively implemented: non-blocking concurrent data structures, "
        "declarative Java Streams with lambda pipelines, parametric Generics, multi-tier Exception Translation, and "
        "SHA-256 cryptographic security. Furthermore, while theoretical fields like AI/ML or Quantum are frequently discussed, "
        "this guide clarifies why CampiFi focuses on <b>Zero-Cloud Edge Resiliency</b> and how AI/ML and Post-Quantum Cryptography "
        "serve as natural future extensions.",
        body_style
    )
    story.append(intro_p)
    story.append(Spacer(1, 3))

    diag_path = os.path.join(DIAGRAMS_DIR, "advanced_java_architecture.png")
    if os.path.exists(diag_path):
        img = Image(diag_path, width=420, height=280)
        story.append(img)
        story.append(Paragraph("<b>Figure 1:</b> Architectural Mapping of Advanced Java Concepts across CampiFi's Concurrency Engine, Streams, Generics & Security.", caption_style))
    story.append(Spacer(1, 2))

    summary_table_data = [
        [
            Paragraph("<b>Advanced Concept</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Concrete Purpose in CampiFi</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Specific Java File & Reference</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white))
        ],
        [
            Paragraph("<b>1. Concurrency & Multithreading</b>", body_style),
            Paragraph("Lock-free concurrent session tracking across simultaneous HTTP threads", body_style),
            Paragraph("<code>ConcurrentHashMap</code> in <code>SessionService.java</code>", code_style)
        ],
        [
            Paragraph("<b>2. Collections Framework</b>", body_style),
            Paragraph("Thread-safe sets, dynamic array lists, and immutable modern Java maps", body_style),
            Paragraph("<code>ConcurrentHashMap.newKeySet()</code>, <code>Map.of()</code>", code_style)
        ],
        [
            Paragraph("<b>3. Generics & Type Safety</b>", body_style),
            Paragraph("Parametric type enforcement, monadic null-safety, and generic REST models", body_style),
            Paragraph("<code>JpaRepository&lt;T, ID&gt;</code>, <code>Optional&lt;User&gt;</code>", code_style)
        ],
        [
            Paragraph("<b>4. Java Streams & Lambdas</b>", body_style),
            Paragraph("Functional data transformations, method references, and monadic mapping", body_style),
            Paragraph("<code>.stream().map(this::toSummary).collect()</code>", code_style)
        ],
        [
            Paragraph("<b>5. Exception Handling</b>", body_style),
            Paragraph("Domain validation guards, checked-to-unchecked chaining, and HTTP 400/403 mapping", body_style),
            Paragraph("<code>ChannelService.java</code>, <code>AdminChannelController.java</code>", code_style)
        ],
        [
            Paragraph("<b>6. Security & Edge Computing</b>", body_style),
            Paragraph("SHA-256 PIN hashing, 128-bit UUID sessions, RBAC, and zero-cloud mesh", body_style),
            Paragraph("<code>MessageDigest</code>, <code>NetworkUtils.java</code>, <code>User.Role</code>", code_style)
        ]
    ]
    st_table = Table(summary_table_data, colWidths=[115, 235, 154])
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
    # SECTION 1: MULTITHREADING & CONCURRENCY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("1. Multithreading & Concurrency: High-Throughput Thread Safety", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Multithreading</b> is the capability of the Java Virtual Machine (JVM) to execute multiple "
        "concurrent threads of execution simultaneously. In CampiFi, hundreds of campus students connect to a single Wi-Fi "
        "hotspot at the same time. Each inbound HTTP request and WebSocket frame is handled on a separate thread, requiring "
        "careful thread-safe memory management to eliminate race conditions, thread starvation, and deadlocks.",
        body_style
    ))

    story.append(Paragraph("A. Lock-Free State Management: <code>ConcurrentHashMap</code>", h2_style))
    story.append(Paragraph(
        "In <code>SessionService.java</code>, active client login sessions are stored in an in-memory map. "
        "A standard <code>java.util.HashMap</code> is NOT thread-safe: if two threads write simultaneously during map resizing, "
        "it can cause corrupted pointers or infinite loops. Instead, CampiFi uses <code>ConcurrentHashMap</code>:",
        body_style
    ))

    code_concur = (
        "@Service\n"
        "public class SessionService {\n"
        "    // High-performance thread-safe storage using fine-grained lock striping & CAS operations\n"
        "    private final ConcurrentHashMap<String, SessionData> sessions = new ConcurrentHashMap<>();\n\n"
        "    public String createSession(User user) {\n"
        "        String token = UUID.randomUUID().toString();\n"
        "        // Thread-safe atomic insertion: safe across concurrent login requests\n"
        "        sessions.put(token, new SessionData(\n"
        "            user.getId(), user.getEmail(), user.getDisplayName(),\n"
        "            user.getRole(), LocalDateTime.now().plusHours(8)\n"
        "        ));\n"
        "        return token;\n"
        "    }\n\n"
        "    public Optional<SessionData> getSession(String token) {\n"
        "        if (token == null) return Optional.empty();\n"
        "        SessionData data = sessions.get(token); // Lock-free volatile read (zero blocking!)\n"
        "        if (data == null) return Optional.empty();\n"
        "        if (LocalDateTime.now().isAfter(data.expiresAt())) {\n"
        "            sessions.remove(token); // Thread-safe removal\n"
        "            return Optional.empty();\n"
        "        }\n"
        "        return Optional.of(data);\n"
        "    }\n"
        "}"
    )
    story.append(make_code_card("src/main/java/com/hotspotchat/service/SessionService.java", code_concur))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. The Multi-Threaded WebSocket Message Broker", h2_style))
    story.append(Paragraph(
        "Spring Boot's WebSocket engine (configured in <code>WebSocketConfig.java</code>) is fundamentally asynchronous. "
        "Inbound client messages over TCP sockets are processed by a dedicated thread pool managed by Spring's "
        "<code>ThreadPoolTaskExecutor</code>. When a student sends a chat message to <code>/app/chat.sendMessage</code>, "
        "the broker dispatches the message to all subscribed clients in parallel worker threads, achieving sub-5ms latency.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Embedded Tomcat Worker Thread Pool (NIO)", h2_style))
    story.append(Paragraph(
        "Spring Boot runs on an embedded Apache Tomcat web server using Non-Blocking I/O (NIO). "
        "Incoming HTTP requests are accepted by an acceptor thread and dispatched to a pool of worker threads "
        "(named <code>http-nio-8080-exec-1</code>, <code>http-nio-8080-exec-2</code>, etc.). This allows multiple clients "
        "to browse channels, verify PINs, and authenticate concurrently without blocking one another.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why did you use ConcurrentHashMap instead of a standard HashMap or Collections.synchronizedMap()?",
        "Standard HashMap is not thread-safe and suffers from race conditions and memory corruption under concurrent requests. Collections.synchronizedMap() wraps a map in a coarse, single global lock—meaning only one thread can read or write at any time, creating a severe performance bottleneck. In contrast, ConcurrentHashMap utilizes lock-striping and Compare-And-Swap (CAS) CPU primitives: reads are completely lock-free, and writes only lock the individual bucket being modified. This provides true parallel throughput for hundreds of concurrent hotspot users."
    ))

    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 2: COLLECTIONS FRAMEWORK
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("2. Collections Framework: Structure, Performance & Thread Safety", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> The <b>Java Collections Framework (JCF)</b> provides a unified architecture for storing, "
        "manipulating, and accessing groups of objects. CampiFi selectively uses diverse collections based on algorithmic "
        "complexity (O(1) vs O(N)), ordering guarantees, and thread-safety requirements:",
        body_style
    ))

    col_table_data = [
        [
            Paragraph("<b>Collection Type</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Concrete Class Used</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Thread Safety</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Usage in CampiFi</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white)),
            Paragraph("<b>Time Complexity</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.5, textColor=colors.white))
        ],
        [
            Paragraph("<code>java.util.List</code>", code_style),
            Paragraph("<code>ArrayList&lt;T&gt;</code>", code_style),
            Paragraph("Not Thread-Safe (Single thread/JPA)", body_style),
            Paragraph("<code>subChannels</code>, <code>members</code>, and <code>messages</code> inside JPA entities", body_style),
            Paragraph("O(1) append<br/>O(N) search", body_style)
        ],
        [
            Paragraph("<code>java.util.Set</code>", code_style),
            Paragraph("<code>ConcurrentHashMap.newKeySet()</code>", code_style),
            Paragraph("Fully Thread-Safe", body_style),
            Paragraph("Active connected members in <code>HotspotRoom.java</code> (guarantees uniqueness)", body_style),
            Paragraph("O(1) add / remove<br/>O(1) contains", body_style)
        ],
        [
            Paragraph("<code>java.util.Map</code>", code_style),
            Paragraph("<code>ConcurrentHashMap&lt;K, V&gt;</code>", code_style),
            Paragraph("Fully Thread-Safe", body_style),
            Paragraph("Global session repository in <code>SessionService.java</code>", body_style),
            Paragraph("O(1) get / put (lock-free read)", body_style)
        ],
        [
            Paragraph("<code>java.util.Map</code>", code_style),
            Paragraph("<code>Map.of(k, v, ...)</code>", code_style),
            Paragraph("Immutable (Thread-Safe)", body_style),
            Paragraph("JSON responses in <code>AdminChannelController.java</code>", body_style),
            Paragraph("O(1) lookup", body_style)
        ]
    ]

    c_table = Table(col_table_data, colWidths=[80, 120, 95, 135, 74])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284C7")),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(KeepTogether(c_table))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Modern Java Immutable Factory Methods: <code>Map.of()</code>", h2_style))
    story.append(Paragraph(
        "Throughout REST controllers (e.g., <code>AdminChannelController.java</code>), CampiFi constructs lightweight, "
        "unmodifiable JSON maps using modern Java factory methods: <code>Map.of(\"success\", true, \"channelId\", ch.getId())</code>. "
        "These immutable maps consume less memory than a traditional <code>new HashMap&lt;&gt;()</code> and cannot be modified by downstream code.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why do you use an ArrayList inside JPA entities but a ConcurrentHashMap for sessions?",
        "Inside JPA entities like Channel.java, the subChannels list is managed within a single database transaction and a single thread by Hibernate—so the lightweight, low-overhead ArrayList is optimal. However, SessionService is an application-wide singleton accessed concurrently by hundreds of HTTP request threads from different client devices at the same millisecond; it strictly requires the lock-free thread safety of ConcurrentHashMap."
    ))

    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 3: GENERICS & TYPE SAFETY
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("3. Generics: Parametric Polymorphism & Compile-Time Type Safety", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Generics</b> (Parametric Polymorphism) enable classes, interfaces, and methods to take types as parameters. "
        "Generics eliminate the need for dangerous runtime type casting (e.g. <code>(User) obj</code>) and allow bugs that would cause "
        "fatal <code>ClassCastException</code> crashes at runtime to be caught at compile-time.",
        body_style
    ))

    story.append(Paragraph("A. Generic Interface Contracts: <code>JpaRepository&lt;T, ID&gt;</code>", h2_style))
    story.append(Paragraph(
        "Every repository in CampiFi binds type arguments to Spring Data's generic interface:",
        body_style
    ))

    code_gen_repo = (
        "// Generic type parameters: T = Entity Type, ID = Primary Key Type\n"
        "public interface UserRepository extends JpaRepository<User, Long> {\n"
        "    // The compiler enforces that findByEmail returns Optional<User>, NOT an untyped Object\n"
        "    Optional<User> findByEmail(String email);\n"
        "}\n\n"
        "public interface ChannelRepository extends JpaRepository<Channel, Long> {}\n"
        "public interface MessageRepository extends JpaRepository<Message, Long> {}"
    )
    story.append(make_code_card("Generic Repositories in CampiFi", code_gen_repo))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Monadic Null-Safety with <code>Optional&lt;T&gt;</code>", h2_style))
    story.append(Paragraph(
        "Null pointer exceptions (NPE) are the #1 cause of runtime crashes in software. CampiFi eliminates NPEs "
        "by utilizing Java's generic <code>Optional&lt;T&gt;</code> container type for all operations that may not find a record:",
        body_style
    ))

    code_gen_opt = (
        "// In UserService.java: Explicit, type-safe handling of missing values\n"
        "public User findOrCreate(String email) {\n"
        "    return userRepository.findByEmail(email)\n"
        "            .orElseGet(() -> {\n"
        "                String displayName = extractDisplayName(email);\n"
        "                return userRepository.save(new User(email, displayName, User.Role.USER));\n"
        "            });\n"
        "}\n\n"
        "// In ChannelService.java: Type-safe exception throwing\n"
        "Channel ch = channelRepository.findById(channelId)\n"
        "        .orElseThrow(() -> new IllegalArgumentException(\"Channel not found: \" + channelId));"
    )
    story.append(make_code_card("Generic Optional<T> in UserService & ChannelService", code_gen_opt))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Generic HTTP Response Envelopes: <code>ResponseEntity&lt;T&gt;</code>", h2_style))
    story.append(Paragraph(
        "Controllers return <code>ResponseEntity&lt;List&lt;ChannelSummary&gt;&gt;</code> or <code>ResponseEntity&lt;Map&lt;String, Object&gt;&gt;</code>. "
        "This guarantees type-safe serialization to JSON without manual string concatenation or unsafe casting.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "How do Java Generics improve the safety and maintainability of your codebase?",
        "Generics provide compile-time type checking. Before Generics, collections and repositories returned generic 'Object' references, requiring explicit type casting like '(User) list.get(0)', which risked ClassCastException if the wrong type was stored. With JpaRepository<User, Long>, the compiler guarantees that findById() returns Optional<User> and findAll() returns List<User>. If a developer mistakenly tries to store a Channel in a UserRepository, the compiler halts immediately."
    ))

    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 4: JAVA STREAMS & LAMBDAS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("4. Java Streams & Functional Lambdas: Declarative Data Pipelines", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> Introduced in Java 8, the <b>Stream API</b> enables declarative, functional transformations "
        "on sequences of elements. Instead of writing imperative loops with manual counter variables and temporary lists, "
        "Streams express <i>what</i> transformation is required via composable pipelines comprising a <b>Source</b>, "
        "<b>Intermediate Operations</b>, and a <b>Terminal Operation</b>.",
        body_style
    ))

    story.append(Paragraph("A. Real Stream Pipeline in <code>ChannelService.java</code>", h2_style))
    story.append(Paragraph(
        "When clients query the list of available campus networks, <code>ChannelService.java</code> transforms database "
        "entities into lightweight presentation summaries using a Stream pipeline:",
        body_style
    ))

    code_stream = (
        "public List<ChannelSummary> listChannels() {\n"
        "    return channelRepository.findAllByOrderByCreatedAtAsc() // 1. Source (List<Channel>)\n"
        "            .stream()                                       // 2. Stream Initiation\n"
        "            .map(this::toSummary)                           // 3. Intermediate Transformation\n"
        "            .collect(Collectors.toList());                  // 4. Terminal Collection\n"
        "}\n\n"
        "public List<SubChannelSummary> getSubChannels(Long channelId) {\n"
        "    return subChannelRepository.findByChannelId(channelId)\n"
        "            .stream()\n"
        "            .map(s -> new SubChannelSummary(\n"
        "                    s.getId(), s.getName(), s.getDescription(),\n"
        "                    channelId, s.getCreatedAt()))           // Lambda Expression!\n"
        "            .collect(Collectors.toList());\n"
        "}"
    )
    story.append(make_code_card("Functional Streams in ChannelService.java (Lines 76-90)", code_stream))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Anatomy of a Stream Pipeline", h2_style))
    story.append(Paragraph("1. <b>Source:</b> The database query returns a <code>List&lt;Channel&gt;</code> from MySQL via Hibernate.", bullet_style))
    story.append(Paragraph("2. <b><code>.stream()</code>:</b> Creates a lazily-evaluated stream of elements.", bullet_style))
    story.append(Paragraph("3. <b><code>.map(this::toSummary)</code>:</b> A higher-order intermediate operation that transforms each <code>Channel</code> object into a <code>ChannelSummary</code> DTO using a <b>Method Reference</b> (<code>ClassName::methodName</code>).", bullet_style))
    story.append(Paragraph("4. <b><code>.collect(Collectors.toList())</code>:</b> The terminal operation that triggers pipeline execution, evaluates the lazy operations, and packages the result into a clean <code>List&lt;ChannelSummary&gt;</code>.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Monadic Functional Chaining on <code>Optional</code>", h2_style))
    story.append(Paragraph(
        "In <code>SessionService.java</code> (Lines 68-72), functional programming simplifies admin authorization checks into a single expression:",
        body_style
    ))
    code_opt_func = (
        "public boolean isAdmin(String token) {\n"
        "    return getSession(token)\n"
        "            .map(s -> s.role() == User.Role.ADMIN) // Transform SessionData -> Boolean\n"
        "            .orElse(false);                        // Fallback if token not found\n"
        "}"
    )
    story.append(make_code_card("Monadic Functional Mapping in SessionService.java", code_opt_func))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why use Java Streams instead of traditional for-loops, and what is a Method Reference?",
        "Traditional for-loops are imperative: they require initializing temporary accumulator lists, managing index variables, and explicitly mutating state (e.g. 'list.add(item)'), which increases boilerplate and off-by-one errors. Java Streams are declarative and functional: they specify the data transformation cleanly without side effects. A Method Reference (like 'this::toSummary') is a compact syntax for a lambda expression that simply calls an existing method, improving readability and eliminating redundant parameter boilerplate."
    ))

    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 5: EXCEPTION HANDLING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("5. Multi-Tier Exception Handling & Defensive Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Definition:</b> <b>Exception Handling</b> is Java's mechanism to handle runtime errors gracefully, "
        "ensuring normal program execution is maintained rather than crashing the JVM. CampiFi implements a "
        "<b>Defensive Multi-Tier Architecture</b>: domain services enforce invariants by throwing semantic exceptions, "
        "while REST controllers intercept those exceptions and translate them into standardized HTTP status codes.",
        body_style
    ))

    story.append(Paragraph("A. Domain-Level Validation Guards", h2_style))
    story.append(Paragraph(
        "In <code>ChannelService.java</code>, invalid client operations are rejected at the service layer by throwing "
        "standard unchecked exceptions with descriptive messages:",
        body_style
    ))

    code_exc_guard = (
        "// Duplicate channel prevention (IllegalArgumentException)\n"
        "if (channelRepository.existsByName(name.trim())) {\n"
        "    throw new IllegalArgumentException(\"A channel named \\\"\" + name + \"\\\" already exists.\");\n"
        "}\n\n"
        "// Channel access restriction for banned members (IllegalStateException)\n"
        "if (memberOpt.isPresent() && memberOpt.get().isBanned()) {\n"
        "    throw new IllegalStateException(\"You are banned from this channel.\");\n"
        "}\n\n"
        "// Entity lookup failure (orElseThrow idiom)\n"
        "Channel ch = channelRepository.findById(id)\n"
        "        .orElseThrow(() -> new IllegalArgumentException(\"Channel not found: \" + id));"
    )
    story.append(make_code_card("Domain Exceptions in ChannelService.java", code_exc_guard))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Checked-to-Unchecked Exception Translation & Chaining", h2_style))
    story.append(Paragraph(
        "In Java, checked exceptions (like <code>NoSuchAlgorithmException</code>) must be declared in method signatures, "
        "polluting callers. In <code>ChannelService.java</code>, CampiFi catches the checked exception and wraps it in an "
        "unchecked <code>RuntimeException</code>, preserving the original cause for debugging (<b>Exception Chaining</b>):",
        body_style
    ))

    code_exc_chain = (
        "private String hashPin(String pin) {\n"
        "    try {\n"
        "        MessageDigest digest = MessageDigest.getInstance(\"SHA-256\");\n"
        "        byte[] hash = digest.digest(pin.getBytes(StandardCharsets.UTF_8));\n"
        "        return bytesToHex(hash);\n"
        "    } catch (NoSuchAlgorithmException e) {\n"
        "        // Exception Translation: preserves root cause 'e' without checked signature leaks\n"
        "        throw new RuntimeException(\"SHA-256 not available\", e);\n"
        "    }\n"
        "}"
    )
    story.append(make_code_card("Exception Chaining in ChannelService.java (Lines 330-338)", code_exc_chain))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Controller HTTP Error Code Mapping", h2_style))
    story.append(Paragraph(
        "In <code>AdminChannelController.java</code> and <code>ChannelController.java</code>, exceptions are caught "
        "and mapped directly to semantic HTTP response codes:",
        body_style
    ))
    story.append(Paragraph("• <code><b>IllegalArgumentException</b></code> &rarr; Returns <b>HTTP 400 Bad Request</b> with JSON error: <code>ResponseEntity.badRequest().body(Map.of(\"error\", e.getMessage()))</code>", bullet_style))
    story.append(Paragraph("• <code><b>IllegalStateException</b></code> (e.g. banned user) &rarr; Returns <b>HTTP 403 Forbidden</b>: <code>ResponseEntity.status(403).body(...)</code>", bullet_style))
    story.append(Paragraph("• <code><b>SecurityException</b></code> (unauthorized admin access) &rarr; Returns <b>HTTP 401 Unauthorized</b>", bullet_style))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "Why do you wrap checked exceptions in RuntimeExceptions in your service layer?",
        "Checked exceptions like NoSuchAlgorithmException force every calling method to add 'throws NoSuchAlgorithmException' to its signature, violating encapsulation and leaking implementation details across architecture tiers. Wrapping the checked exception in an unchecked RuntimeException ('throw new RuntimeException(\"SHA-256 error\", e);') keeps service method signatures clean while preserving the original stack trace via Exception Chaining for logging and root-cause analysis."
    ))

    story.append(Spacer(1, 8))

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 6: SECURITY & CUTTING-EDGE FIELDS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("6. Security, Edge Computing & Cutting-Edge Disciplines", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "<b>Architectural Context:</b> Evaluators often ask about cutting-edge technologies like <b>Cybersecurity</b>, "
        "<b>Edge Computing</b>, <b>AI/ML</b>, and <b>Quantum</b>. It is vital to articulate what CampiFi actively implements, "
        "why certain technologies were chosen, and how advanced fields fit into future architecture.",
        body_style
    ))

    story.append(Paragraph("A. Cryptographic Security & Password Hashing (SHA-256)", h2_style))
    story.append(Paragraph(
        "In CampiFi, private channels are protected by a 4-digit PIN. Storing plain-text PINs is a severe security violation. "
        "CampiFi implements one-way cryptographic hashing using the <b>Secure Hash Algorithm (SHA-256)</b>:",
        body_style
    ))
    story.append(Paragraph("• <b>One-Way Hash Property:</b> It is computationally infeasible to invert a SHA-256 digest back into the original PIN.", bullet_style))
    story.append(Paragraph("• <b>Fixed 256-bit Output:</b> Every PIN generates a unique 64-character hexadecimal digest stored in MySQL.", bullet_style))
    story.append(Paragraph("• <b>Zero Plain-Text Footprint:</b> Even if an attacker dumps the MySQL database, they cannot read channel PINs.", bullet_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("B. Ephemeral Session Security & Memory Isolation", h2_style))
    story.append(Paragraph(
        "Instead of storing persistent authentication cookies on disk, CampiFi issues <b>128-bit cryptographically random UUID tokens</b> "
        "(<code>UUID.randomUUID().toString()</code>). These tokens exist only in volatile server RAM and auto-expire after 8 hours. "
        "If the campus server restarts, all sessions are immediately purged, preventing session hijacking or stale credential attacks.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("C. Zero-Cloud Edge Resiliency (The True Cutting-Edge Paradigm)", h2_style))
    story.append(Paragraph(
        "While modern software over-relies on centralized cloud vendors (AWS, Azure, Firebase), CampiFi implements "
        "<b>Local-First Edge Mesh Computing</b>. It requires <b>zero internet connection</b>, zero external DNS, and zero third-party APIs. "
        "During natural disasters, campus cellular blackouts, or remote field activities, CampiFi creates an instant, "
        "self-contained communication hub entirely over local Wi-Fi / hotspot radio frequencies.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("D. How to Answer Questions on AI/ML and Quantum Computing", h2_style))
    story.append(Paragraph(
        "Examiners may ask: <i>'Did you use AI/ML or Quantum in this project?'</i> Here is the exact, honest, and technically sound way to answer:",
        body_style
    ))
    story.append(Paragraph("• <b>Regarding AI/ML:</b> <i>'CampiFi intentionally does not use cloud AI/ML models because cloud connectivity violates our core requirement of functioning during zero-internet blackouts. However, as an immediate future enhancement, we plan to embed a lightweight, ONNX-based or TensorFlow Lite edge model running locally on the JVM to perform offline toxic message detection and automated priority alert filtering without needing internet access.'</i>", bullet_style))
    story.append(Paragraph("• <b>Regarding Quantum Computing:</b> <i>'Current quantum computers are experimental and not accessible in offline field environments. However, CampiFi's cryptographic architecture is modularly encapsulated: if quantum computing threatens SHA-256 in the future, our hashPin() method in ChannelService can be updated with Post-Quantum Cryptography (PQC) algorithms (such as NIST-approved CRYSTALS-Dilithium) without requiring any architectural changes to controllers or database schemas.'</i>", bullet_style))
    story.append(Spacer(1, 4))

    story.append(make_viva_card(
        "What cutting-edge paradigm does CampiFi represent if it doesn't use cloud AI?",
        "CampiFi represents Cutting-Edge Local-First Edge Resiliency. While industry software assumes continuous, high-speed cloud internet, CampiFi is engineered for crisis resilience, privacy, and zero-infrastructure environments (natural disasters, network outages, offline exams). Operating real-time WebSockets, in-memory concurrency, and cryptographic security entirely on local Wi-Fi radio frequencies without external cloud servers is the essence of modern decentralized edge computing."
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 7: MASTER MATRIX & CHEAT SHEET
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("7. Advanced Concepts Master Matrix & Viva Examination Defense", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_blue, spaceBefore=0, spaceAfter=5))

    story.append(Paragraph(
        "Use this master reference matrix during your project defense to immediately cite the exact file, "
        "line number, and architectural justification for every advanced Java and systems topic:",
        body_style
    ))

    master_matrix_data = [
        [
            Paragraph("<b>Topic</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white)),
            Paragraph("<b>Code File & Location</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white)),
            Paragraph("<b>Implementation Details in CampiFi</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white)),
            Paragraph("<b>Viva Examiner Talking Point</b>", ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.2, textColor=colors.white))
        ],
        [
            Paragraph("<b>Multithreading</b>", body_style),
            Paragraph("<code>service/SessionService.java</code><br/><code>config/WebSocketConfig.java</code>", code_style),
            Paragraph("<code>ConcurrentHashMap</code> lock-striping; Spring async WebSocket thread executor", body_style),
            Paragraph("Eliminates race conditions and global lock contention across concurrent hotspot users.", body_style)
        ],
        [
            Paragraph("<b>Collections</b>", body_style),
            Paragraph("<code>model/Channel.java</code><br/><code>service/SessionService.java</code>", code_style),
            Paragraph("<code>ArrayList</code> for entity collections; <code>ConcurrentHashMap.newKeySet()</code> for active members; <code>Map.of()</code> for immutability", body_style),
            Paragraph("Distinguishes single-threaded JPA lists from multi-threaded concurrent caches.", body_style)
        ],
        [
            Paragraph("<b>Generics</b>", body_style),
            Paragraph("<code>repository/UserRepository.java</code><br/><code>service/UserService.java</code>", code_style),
            Paragraph("<code>JpaRepository&lt;User, Long&gt;</code>; generic monadic <code>Optional&lt;User&gt;</code>; <code>ResponseEntity&lt;T&gt;</code>", body_style),
            Paragraph("Guarantees compile-time type safety and completely prevents <code>ClassCastException</code>.", body_style)
        ],
        [
            Paragraph("<b>Java Streams</b>", body_style),
            Paragraph("<code>service/ChannelService.java</code> (Lines 76-90, 145, 196)", code_style),
            Paragraph("<code>.stream().map(this::toSummary).collect(Collectors.toList())</code>; method references & lambdas", body_style),
            Paragraph("Declarative, side-effect-free data transformation replacing error-prone imperative loops.", body_style)
        ],
        [
            Paragraph("<b>Exception Handling</b>", body_style),
            Paragraph("<code>service/ChannelService.java</code><br/><code>AdminChannelController.java</code>", code_style),
            Paragraph("Domain validation (<code>IllegalArgumentException</code>); checked-to-unchecked chaining; HTTP 400/403 mapping", body_style),
            Paragraph("Preserves stack traces while shielding callers from checked exception clutter.", body_style)
        ],
        [
            Paragraph("<b>Security & Cryptography</b>", body_style),
            Paragraph("<code>service/ChannelService.java</code> (Line 330)<br/><code>service/NetworkUtils.java</code>", code_style),
            Paragraph("SHA-256 one-way hashing for channel PINs; 128-bit UUID sessions; proxy anti-spoofing", body_style),
            Paragraph("Zero plain-text secrets stored; ephemeral RAM sessions prevent data leakage.", body_style)
        ],
        [
            Paragraph("<b>Edge Computing (Future AI/Quantum)</b>", body_style),
            Paragraph("<code>service/ChannelService.java</code><br/>Overall Architecture", code_style),
            Paragraph("Zero-cloud offline mesh; modular design ready for on-device edge AI and Post-Quantum Cryptography (PQC)", body_style),
            Paragraph("Engineered for disaster recovery and offline campus autonomy, not cloud vendor lock-in.", body_style)
        ]
    ]

    m_table = Table(master_matrix_data, colWidths=[80, 130, 164, 130])
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
        Paragraph("<b>Top 4 'Golden Rules' to Remember for Your Advanced Java Defense</b>", h2_style),
        Paragraph("1. <b>Point out ConcurrentHashMap immediately:</b> When asked about multithreading, highlight that CampiFi's SessionService uses ConcurrentHashMap with non-blocking reads and CAS lock-striping to handle hundreds of simultaneous Wi-Fi clients.", bullet_style),
        Paragraph("2. <b>Walk through a Stream pipeline step-by-step:</b> When asked about Streams, explain the 4 stages: Source (JPA List), Stream creation (.stream()), Intermediate Transformation (.map(this::toSummary)), and Terminal Collection (.collect(Collectors.toList())).", bullet_style),
        Paragraph("3. <b>Highlight Exception Chaining:</b> Show how ChannelService catches NoSuchAlgorithmException and wraps it in a RuntimeException, explaining that this prevents polluting public method signatures while keeping the root cause intact.", bullet_style),
        Paragraph("4. <b>Be confident and honest about AI/ML & Quantum:</b> Proudly explain that CampiFi is built on <i>Cutting-Edge Offline Edge Resiliency</i> (zero internet dependency), and frame AI/ML and Quantum as on-device edge NLP and Post-Quantum cryptographic extensions.", bullet_style)
    ]
    story.append(KeepTogether(golden_rules))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Advanced Java Guide PDF successfully generated at: {filename}")

if __name__ == '__main__':
    target = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/CampiFi_Advanced_Java_and_Security_Guide.pdf"
    build_advanced_java_pdf(target)
