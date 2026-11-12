import os
os.environ['MPLCONFIGDIR'] = '/tmp'
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_advanced_java_diagram():
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
                                   facecolor='#0F172A', edgecolor='#1E293B', linewidth=1.5)
    ax.add_patch(banner)
    ax.text(7.5, 9.42, "CampiFi — Advanced Java & Edge Security Architecture",
            ha='center', va='center', fontsize=14, fontweight='bold', color='white', fontfamily='sans-serif')
    ax.text(7.5, 9.15, "Concurrency, Functional Streams, Generics, Robust Exception Handling & Cryptographic Security",
            ha='center', va='center', fontsize=9.5, color='#38BDF8', fontfamily='sans-serif')

    cards = [
        # 1. Multithreading & Concurrency (Top Left)
        {
            "num": "1",
            "title": "Multithreading & Concurrency",
            "concept": "Thread-Safety & Non-Blocking State",
            "header_color": "#0369A1",
            "bg_color": "#F0F9FF",
            "border": "#38BDF8",
            "x": 0.6, "y": 4.8, "w": 4.3, "h": 3.9,
            "lines": [
                ("LOCK-FREE CONCURRENT MAP:", True, "#0284C7"),
                ("• ConcurrentHashMap<String, SessionData>", False, "#1E293B"),
                ("• Lock-striping & CAS operations prevent", False, "#475569"),
                ("  race conditions across concurrent HTTP threads", False, "#1E293B"),
                ("SPRING ASYNC WEBSOCKET BROKER:", True, "#0284C7"),
                ("• ThreadPoolTaskExecutor handles STOMP frames", False, "#1E293B"),
                ("• Dedicated worker threads per connected client", False, "#475569"),
                ("TOMCAT NIO THREAD POOL:", True, "#0284C7"),
                ("• http-nio-8080-exec-* workers handle incoming", False, "#1E293B"),
                ("  campus requests in parallel without blocking", False, "#475569")
            ]
        },
        # 2. Functional Java Streams (Top Center)
        {
            "num": "2",
            "title": "Java Streams & Lambdas",
            "concept": "Declarative Data Transformation",
            "header_color": "#047857",
            "bg_color": "#F0FDF4",
            "border": "#34D399",
            "x": 5.35, "y": 4.8, "w": 4.3, "h": 3.9,
            "lines": [
                ("DECLARATIVE STREAM PIPELINES:", True, "#059669"),
                ("• channelRepository.findAllByOrderByCreatedAtAsc()", False, "#1E293B"),
                ("  .stream().map(this::toSummary).collect(...)", False, "#047857"),
                ("METHOD REFERENCES (ClassName::method):", True, "#059669"),
                ("• this::toSummary, ChannelMember::isAdmin", False, "#1E293B"),
                ("• Concise, clean, and null-safe execution", False, "#475569"),
                ("MONADIC OPTIONAL PIPELINES:", True, "#059669"),
                ("• .map(s -> s.role() == Role.ADMIN).orElse(false)", False, "#1E293B"),
                ("• Eliminates risky procedural null checks", False, "#475569")
            ]
        },
        # 3. Generics & Type Safety (Top Right)
        {
            "num": "3",
            "title": "Generics & Type Safety",
            "concept": "Parametric Polymorphism",
            "header_color": "#6D28D9",
            "bg_color": "#FAF5FF",
            "border": "#A855F7",
            "x": 10.1, "y": 4.8, "w": 4.3, "h": 3.9,
            "lines": [
                ("GENERIC REPOSITORY CONTRACTS:", True, "#7C3AED"),
                ("• JpaRepository<User, Long>", False, "#1E293B"),
                ("• JpaRepository<Channel, Long>", False, "#1E293B"),
                ("• Enforces compile-time type verification", False, "#475569"),
                ("GENERIC MONADIC CONTAINERS:", True, "#7C3AED"),
                ("• Optional<User>, Optional<SessionData>", False, "#1E293B"),
                ("• Eliminates ClassCastException & NullPointer", False, "#475569"),
                ("GENERIC HTTP RESPONSES:", True, "#7C3AED"),
                ("• ResponseEntity<Map<String, Object>>", False, "#1E293B"),
                ("• Strongly-typed REST payloads", False, "#475569")
            ]
        },
        # 4. Multi-Tier Exception Handling (Bottom Left)
        {
            "num": "4",
            "title": "Exception Handling",
            "concept": "Defensive Architecture & Error Mapping",
            "header_color": "#B45309",
            "bg_color": "#FFFBEB",
            "border": "#FBBF24",
            "x": 0.6, "y": 0.6, "w": 4.3, "h": 3.9,
            "lines": [
                ("DOMAIN-LEVEL GUARDS:", True, "#D97706"),
                ("• throw new IllegalArgumentException(\"Name taken\")", False, "#1E293B"),
                ("• throw new IllegalStateException(\"Banned user\")", False, "#1E293B"),
                ("CHECKED-TO-UNCHECKED TRANSLATION:", True, "#D97706"),
                ("• catch (NoSuchAlgorithmException e) {", False, "#1E293B"),
                ("    throw new RuntimeException(\"SHA-256 error\", e); }", False, "#475569"),
                ("HTTP CONTROLLER ERROR MAPPING:", True, "#D97706"),
                ("• catch (IllegalArgumentException e) ➔ 400 Bad Req", False, "#1E293B"),
                ("• catch (IllegalStateException e) ➔ 403 Forbidden", False, "#1E293B")
            ]
        },
        # 5. Cryptography & Security (Bottom Center)
        {
            "num": "5",
            "title": "Security & Cryptography",
            "concept": "SHA-256, RBAC & Subnet Defense",
            "header_color": "#BE123C",
            "bg_color": "#FFF1F2",
            "border": "#FB7185",
            "x": 5.35, "y": 0.6, "w": 4.3, "h": 3.9,
            "lines": [
                ("SHA-256 CRYPTOGRAPHIC HASHING:", True, "#E11D48"),
                ("• Private channel 4-digit PINs hashed with", False, "#1E293B"),
                ("  MessageDigest before storage (Zero plain PINs)", False, "#475569"),
                ("EPHEMERAL SESSION TOKENS:", True, "#E11D48"),
                ("• UUID.randomUUID() 128-bit entropy tokens", False, "#1E293B"),
                ("• 8-hour auto-expiry in RAM (No disk leaks)", False, "#475569"),
                ("ROLE-BASED ACCESS CONTROL (RBAC):", True, "#E11D48"),
                ("• USER vs ADMIN roles; Sub-channel admin checks", False, "#1E293B"),
                ("• NetworkUtils: X-Forwarded-For anti-spoofing", False, "#475569")
            ]
        },
        # 6. Edge & Resilient Computing (Bottom Right)
        {
            "num": "6",
            "title": "Cutting-Edge Edge System",
            "concept": "Zero-Cloud Offline Hotspot Mesh",
            "header_color": "#0F766E",
            "bg_color": "#F0FDFA",
            "border": "#2DD4BF",
            "x": 10.1, "y": 0.6, "w": 4.3, "h": 3.9,
            "lines": [
                ("ZERO-CLOUD RESILIENCY:", True, "#0D9488"),
                ("• Functions during internet blackouts & crises", False, "#1E293B"),
                ("• Local Wi-Fi Direct / Hotspot AP routing", False, "#475569"),
                ("AI/ML FUTURE SCOPE (VIVA TOPIC):", True, "#0D9488"),
                ("• On-device lightweight NLP content moderation", False, "#1E293B"),
                ("  (e.g., ONNX / TensorFlow Lite without cloud API)", False, "#475569"),
                ("QUANTUM DEFENSE READINESS:", True, "#0D9488"),
                ("• Modular cryptography enables drop-in Post-Quantum", False, "#1E293B"),
                ("  algorithms (PQC Dilithium/Kyber) in ChannelService", False, "#475569")
            ]
        }
    ]

    for c in cards:
        card_box = patches.FancyBboxPatch((c["x"], c["y"]), c["w"], c["h"],
                                         boxstyle="round,pad=0.08",
                                         facecolor=c["bg_color"],
                                         edgecolor=c["border"],
                                         linewidth=1.4)
        ax.add_patch(card_box)

        header_h = 0.72
        header_box = patches.FancyBboxPatch((c["x"], c["y"] + c["h"] - header_h), c["w"], header_h,
                                           boxstyle="round,pad=0.06",
                                           facecolor=c["header_color"],
                                           edgecolor=c["header_color"])
        ax.add_patch(header_box)

        ax.text(c["x"] + 0.25, c["y"] + c["h"] - 0.28,
                f"[{c['num']}]  {c['title']}",
                fontsize=10.5, fontweight='bold', color='white', fontfamily='sans-serif')
        ax.text(c["x"] + 0.25, c["y"] + c["h"] - 0.52,
                c["concept"],
                fontsize=8.5, fontstyle='italic', color='#E2E8F0', fontfamily='sans-serif')

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

    ax.text(7.5, 0.2, "CampiFi Architectural Artifact — Production Advanced Java 17, Concurrency, Cryptography & Edge Systems",
            ha='center', va='center', fontsize=8.5, color='#64748B', fontstyle='italic', fontfamily='sans-serif')

    os.makedirs('/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams', exist_ok=True)
    out_path = '/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams/advanced_java_architecture.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    plt.close()
    print(f"Diagram successfully generated at: {out_path}")

if __name__ == '__main__':
    generate_advanced_java_diagram()
