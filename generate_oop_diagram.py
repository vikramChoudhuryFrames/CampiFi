import os
os.environ['MPLCONFIGDIR'] = '/tmp'
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_oop_diagram():
    fig = plt.figure(figsize=(15, 10), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background
    bg = patches.Rectangle((0, 0), 15, 10, facecolor='#F8FAFC', edgecolor='none')
    ax.add_patch(bg)

    # Title Banner
    banner = patches.FancyBboxPatch((0.5, 9.0), 14.0, 0.8, boxstyle="round,pad=0.1",
                                   facecolor='#1E3A8A', edgecolor='#0F172A', linewidth=1.5)
    ax.add_patch(banner)
    ax.text(7.5, 9.4, "CampiFi — Object-Oriented Programming (OOP) Architectural Implementation",
            ha='center', va='center', fontsize=14, fontweight='bold', color='white', fontfamily='sans-serif')

    # Subtitle
    ax.text(7.5, 9.1, "Demonstrating Classes, Objects, Encapsulation, Inheritance, Polymorphism, Abstraction & Interfaces",
            ha='center', va='center', fontsize=9.5, color='#93C5FD', fontfamily='sans-serif')

    # Card definitions: (title, subtitle, color, border, items, x, y, w, h)
    cards = [
        # 1. Classes & Objects (Top Left)
        {
            "num": "1",
            "title": "Classes & Objects",
            "concept": "Blueprint & Runtime Instantiation",
            "header_color": "#0284C7",
            "bg_color": "#F0F9FF",
            "border": "#38BDF8",
            "x": 0.6, "y": 4.8, "w": 4.3, "h": 3.9,
            "lines": [
                ("CLASS (Blueprint):", True, "#0369A1"),
                ("• User.java, Channel.java, SubChannel.java", False, "#1E293B"),
                ("• Defines state (attributes) and behavior (methods)", False, "#475569"),
                ("OBJECT (Instance):", True, "#0369A1"),
                ("• new User(\"admin@campifi.edu\", Role.ADMIN)", False, "#1E293B"),
                ("• Ephemeral SessionData records in memory", False, "#475569"),
                ("SPRING IoC CONTAINER:", True, "#0369A1"),
                ("• Manages singleton Bean objects (@Service, @Repository)", False, "#1E293B"),
                ("• Dependency Injection: UserService, ChannelService", False, "#475569")
            ]
        },
        # 2. Encapsulation (Top Center)
        {
            "num": "2",
            "title": "Encapsulation",
            "concept": "Data Hiding & State Protection",
            "header_color": "#16A34A",
            "bg_color": "#F0FDF4",
            "border": "#4ADE80",
            "x": 5.35, "y": 4.8, "w": 4.3, "h": 3.9,
            "lines": [
                ("PRIVATE DATA MEMBERS:", True, "#15803D"),
                ("• private Long id; private String email;", False, "#1E293B"),
                ("• private String pinHash; (Raw PIN never saved)", False, "#1E293B"),
                ("CONTROLLED ACCESSORS:", True, "#15803D"),
                ("• Public getters & validated setters", False, "#475569"),
                ("• Read-only fields: getId(), getCreatedAt() (No setters!)", False, "#1E293B"),
                ("STATE SHIELDING (SessionService):", True, "#15803D"),
                ("• private final ConcurrentHashMap sessions", False, "#1E293B"),
                ("• Callers cannot tamper; must use createSession()", False, "#475569")
            ]
        },
        # 3. Inheritance (Top Right)
        {
            "num": "3",
            "title": "Inheritance",
            "concept": "Code Reusability & Hierarchy",
            "header_color": "#9333EA",
            "bg_color": "#FAF5FF",
            "border": "#C084FC",
            "x": 10.1, "y": 4.8, "w": 4.3, "h": 3.9,
            "lines": [
                ("INTERFACE INHERITANCE (extends):", True, "#7E22CE"),
                ("• UserRepository extends JpaRepository<User, Long>", False, "#1E293B"),
                ("• ChannelRepository extends JpaRepository<Channel, Long>", False, "#1E293B"),
                ("INHERITED CAPABILITIES:", True, "#7E22CE"),
                ("• Inherits 30+ standardized CRUD operations:", False, "#475569"),
                ("  save(), findById(), findAll(), deleteById(), count()", False, "#1E293B"),
                ("HIERARCHICAL REUSE:", True, "#7E22CE"),
                ("• JpaRepository ➔ PagingAndSorting ➔ CrudRepository", False, "#1E293B"),
                ("• Zero duplicate database plumbing required", False, "#475569")
            ]
        },
        # 4. Polymorphism (Bottom Left)
        {
            "num": "4",
            "title": "Polymorphism",
            "concept": "Overloading & Dynamic Overriding",
            "header_color": "#D97706",
            "bg_color": "#FFFBEB",
            "border": "#FBBF24",
            "x": 0.6, "y": 0.6, "w": 4.3, "h": 3.9,
            "lines": [
                ("STATIC (Compile-Time / Overloading):", True, "#B45309"),
                ("• User() [Default] vs User(email, name, role) [Custom]", False, "#1E293B"),
                ("• ChatMessage() vs ChatMessage(type, sender, room)", False, "#1E293B"),
                ("DYNAMIC (Runtime / Overriding):", True, "#B45309"),
                ("• @Override run(String... args) in DataInitializer", False, "#1E293B"),
                ("• @Override configureMessageBroker() in WebSocketConfig", False, "#1E293B"),
                ("DYNAMIC DISPATCH (Interface Polymorphism):", True, "#B45309"),
                ("• userRepository.save(user) dispatches at runtime", False, "#475569"),
                ("  to Spring's SimpleJpaRepository proxy object", False, "#1E293B")
            ]
        },
        # 5. Abstraction (Bottom Center)
        {
            "num": "5",
            "title": "Abstraction",
            "concept": "Hiding Complex Internals",
            "header_color": "#EA580C",
            "bg_color": "#FFF7ED",
            "border": "#FB923C",
            "x": 5.35, "y": 0.6, "w": 4.3, "h": 3.9,
            "lines": [
                ("DATABASE ABSTRACTION (JPA):", True, "#C2410C"),
                ("• findByEmail(email) executes SQL without JDBC leaks", False, "#1E293B"),
                ("• Hides connection pools, statements & ResultSet", False, "#475569"),
                ("SERVICE LAYER ABSTRACTION:", True, "#C2410C"),
                ("• ChannelService.joinPrivateChannel() hides:", False, "#475569"),
                ("  SHA-256 PIN hashing, member lookups & commits", False, "#1E293B"),
                ("NETWORK UTILS ABSTRACTION:", True, "#C2410C"),
                ("• getClientIp(req) abstracts X-Forwarded headers,", False, "#1E293B"),
                ("  proxy hops & IPv6-to-IPv4 loopback conversions", False, "#475569")
            ]
        },
        # 6. Interfaces (Bottom Right)
        {
            "num": "6",
            "title": "Interfaces",
            "concept": "Pure Contracts & Decoupling",
            "header_color": "#0D9488",
            "bg_color": "#F0FDFA",
            "border": "#2DD4BF",
            "x": 10.1, "y": 0.6, "w": 4.3, "h": 3.9,
            "lines": [
                ("PURE CONTRACTS (What vs How):", True, "#0F766E"),
                ("• CommandLineRunner (Startup execution contract)", False, "#1E293B"),
                ("• WebSocketMessageBrokerConfigurer (STOMP contract)", False, "#1E293B"),
                ("• JpaRepository<T, ID> (Standardized data contract)", False, "#1E293B"),
                ("LOOSE COUPLING & INVERSION:", True, "#0F766E"),
                ("• Controllers depend on Services; Services depend", False, "#475569"),
                ("  on Repository Interfaces (not concrete classes)", False, "#1E293B"),
                ("• Enables seamless unit testing & database swaps", False, "#475569")
            ]
        }
    ]

    for c in cards:
        # Card outer frame
        card_box = patches.FancyBboxPatch((c["x"], c["y"]), c["w"], c["h"],
                                         boxstyle="round,pad=0.08",
                                         facecolor=c["bg_color"],
                                         edgecolor=c["border"],
                                         linewidth=1.4)
        ax.add_patch(card_box)

        # Card header bar
        header_h = 0.72
        header_box = patches.FancyBboxPatch((c["x"], c["y"] + c["h"] - header_h), c["w"], header_h,
                                           boxstyle="round,pad=0.06",
                                           facecolor=c["header_color"],
                                           edgecolor=c["header_color"])
        ax.add_patch(header_box)

        # Header Text
        ax.text(c["x"] + 0.25, c["y"] + c["h"] - 0.28,
                f"[{c['num']}]  {c['title']}",
                fontsize=11, fontweight='bold', color='white', fontfamily='sans-serif')
        ax.text(c["x"] + 0.25, c["y"] + c["h"] - 0.52,
                c["concept"],
                fontsize=8.5, fontstyle='italic', color='#E2E8F0', fontfamily='sans-serif')

        # Content lines
        curr_y = c["y"] + c["h"] - 0.95
        for text, is_header, color in c["lines"]:
            if is_header:
                curr_y -= 0.08
                ax.text(c["x"] + 0.2, curr_y, text,
                        fontsize=8.5, fontweight='bold', color=color, fontfamily='sans-serif')
                curr_y -= 0.24
            else:
                ax.text(c["x"] + 0.25, curr_y, text,
                        fontsize=7.8, color=color, fontfamily='sans-serif')
                curr_y -= 0.22

    # Central watermark / note at bottom
    ax.text(7.5, 0.2, "CampiFi Architectural Artifact — All concepts mapped directly to live production codebase (Spring Boot 3.2.5 + JPA + MySQL)",
            ha='center', va='center', fontsize=8.5, color='#64748B', fontstyle='italic', fontfamily='sans-serif')

    os.makedirs('/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams', exist_ok=True)
    out_path = '/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams/oop_concepts_architecture.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    plt.close()
    print(f"Diagram successfully generated at: {out_path}")

if __name__ == '__main__':
    generate_oop_diagram()
