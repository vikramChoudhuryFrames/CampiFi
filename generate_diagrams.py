import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = "/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def draw_system_architecture():
    fig, ax = plt.subplots(figsize=(10.5, 8.5), dpi=220)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 9.0)
    ax.axis('off')

    ax.text(5.25, 8.6, "CampiFi — Multi-Tier System Architecture", ha='center', va='center',
            fontsize=16, fontweight='bold', color='#1E3A8A')

    layers = [
        ("1. Presentation Tier (Client Web Browsers)", 7.1, 1.1, '#EFF6FF', '#3B82F6', [
            ("index.html\n(Email Login)", 1.8),
            ("channels.html\n(Network Directory)", 4.1),
            ("admin.html\n(Host Dashboard)", 6.4),
            ("chat.html\n(Live WebSocket Chat)", 8.7)
        ]),
        ("2. Network Gatekeeper & Security Tier", 5.6, 1.0, '#F0FDF4', '#10B981', [
            ("NetworkUtils\n(Campus Subnet 10.0.0.0/8 Check)", 3.4),
            ("PageController\n(Host Device vs Student Routing)", 7.1)
        ]),
        ("3. Controller & Protocol Dispatcher Tier", 4.1, 1.0, '#FAF5FF', '#8B5CF6', [
            ("AuthController\n(/api/auth)", 1.8),
            ("ChannelController\n(/api/channels)", 4.1),
            ("AdminChannelController\n(/api/admin)", 6.4),
            ("ChatController\n(WebSocket/STOMP)", 8.7)
        ]),
        ("4. Service & Business Logic Tier", 2.6, 1.0, '#FFFBEB', '#D97706', [
            ("UserService\n(User Parsing & Roles)", 2.4),
            ("SessionService\n(In-Memory UUID Session Store)", 5.25),
            ("ChannelService\n(Channels, PIN SHA-256, Admins)", 8.1)
        ]),
        ("5. Data Persistence Tier (Spring Data JPA & MySQL)", 1.1, 1.0, '#FEF2F2', '#DC2626', [
            ("Spring Data JPA Repositories\n(Hibernate ORM Layer)", 3.4),
            ("MySQL 8.4 Relational Database\n(Port 3306 @ campifi DB)", 7.1)
        ])
    ]

    for title, y, h, bg_col, border_col, components in layers:
        rect = patches.FancyBboxPatch((0.5, y), 9.5, h, boxstyle="round,pad=0.08",
                                      fc=bg_col, ec=border_col, lw=1.5)
        ax.add_patch(rect)
        ax.text(0.7, y + h - 0.22, title, fontsize=9.5, fontweight='bold', color=border_col)

        for comp_name, cx in components:
            w_box = 2.1
            box = patches.FancyBboxPatch((cx - w_box/2, y + 0.1), w_box, h - 0.42,
                                         boxstyle="round,pad=0.05", fc='white', ec=border_col, lw=1)
            ax.add_patch(box)
            ax.text(cx, y + 0.1 + (h - 0.42)/2, comp_name, ha='center', va='center',
                    fontsize=7.5, color='#0F172A', multialignment='center')

    # Side flow arrows
    for y_top in [7.1, 5.6, 4.1, 2.6]:
        ax.annotate("", xy=(10.15, y_top), xytext=(10.15, y_top + 0.4),
                    arrowprops=dict(arrowstyle="->", lw=2, color='#64748B'))
        ax.annotate("", xy=(0.35, y_top), xytext=(0.35, y_top + 0.4),
                    arrowprops=dict(arrowstyle="->", lw=2, color='#64748B'))

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "system_architecture.png")
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

def draw_uml_class_diagram():
    fig, ax = plt.subplots(figsize=(11.5, 9.2), dpi=220)
    ax.set_xlim(0, 11.5)
    ax.set_ylim(0, 9.5)
    ax.axis('off')

    ax.text(5.75, 9.15, "CampiFi — UML Domain Entity Class Diagram", ha='center', va='center',
            fontsize=16, fontweight='bold', color='#1E3A8A')

    classes = [
        ("User", 1.2, 5.8, 3.0, 2.7, [
            "+ id : Long {PK}",
            "+ email : String {Unique}",
            "+ displayName : String",
            "+ role : Role {USER, ADMIN}",
            "+ createdAt : LocalDateTime"
        ], [
            "+ getId() : Long",
            "+ getRole() : Role",
            "+ setRole(Role) : void"
        ]),
        ("Channel", 7.3, 5.8, 3.0, 2.7, [
            "+ id : Long {PK}",
            "+ name : String {Unique}",
            "+ description : String",
            "+ type : ChannelType",
            "+ pinHash : String",
            "+ createdAt : LocalDateTime"
        ], [
            "+ getType() : ChannelType",
            "+ getPinHash() : String"
        ]),
        ("SubChannel", 7.3, 2.1, 3.0, 2.4, [
            "+ id : Long {PK}",
            "+ name : String",
            "+ description : String",
            "+ channel : Channel {FK}"
        ], [
            "+ getChannel() : Channel"
        ]),
        ("ChannelMember", 4.3, 4.3, 2.9, 2.5, [
            "+ id : Long {PK}",
            "+ user : User {FK}",
            "+ channel : Channel {FK}",
            "+ isAdmin : boolean",
            "+ isBanned : boolean"
        ], [
            "+ isAdmin() : boolean",
            "+ setAdmin(boolean) : void"
        ]),
        ("SubChannelAdmin", 1.2, 2.1, 3.0, 2.4, [
            "+ id : Long {PK}",
            "+ user : User {FK}",
            "+ subChannel : SubChannel {FK}"
        ], [
            "+ getUser() : User",
            "+ getSubChannel() : SubChannel"
        ])
    ]

    for name, x, y, w, h, attrs, methods in classes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc='#F8FAFC', ec='#1E3A8A', lw=1.5)
        ax.add_patch(rect)
        header = patches.Rectangle((x, y + h - 0.4), w, 0.4, fc='#1E3A8A', ec='#1E3A8A')
        ax.add_patch(header)
        ax.text(x + w/2, y + h - 0.2, name, ha='center', va='center', fontsize=10, fontweight='bold', color='white')

        curr_y = y + h - 0.65
        for attr in attrs:
            ax.text(x + 0.12, curr_y, attr, fontsize=7.8, color='#0F172A', va='center')
            curr_y -= 0.25

        ax.plot([x, x + w], [curr_y + 0.1, curr_y + 0.1], color='#CBD5E1', lw=0.75)
        curr_y -= 0.15

        for m in methods:
            ax.text(x + 0.12, curr_y, m, fontsize=7.8, color='#475569', va='center')
            curr_y -= 0.25

    # Relationships
    # User -> ChannelMember (1 to N)
    ax.annotate("", xy=(4.3, 5.6), xytext=(4.2, 6.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1E3A8A'))
    ax.text(3.9, 6.8, "1", fontsize=8.5, color='#1E3A8A', fontweight='bold')
    ax.text(4.1, 5.7, "0..*", fontsize=8.5, color='#1E3A8A', fontweight='bold')

    # Channel -> ChannelMember (1 to N)
    ax.annotate("", xy=(7.2, 5.6), xytext=(7.3, 6.7), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1E3A8A'))
    ax.text(7.4, 6.8, "1", fontsize=8.5, color='#1E3A8A', fontweight='bold')
    ax.text(7.0, 5.7, "0..*", fontsize=8.5, color='#1E3A8A', fontweight='bold')

    # Channel -> SubChannel (1 to N)
    ax.annotate("", xy=(8.8, 4.5), xytext=(8.8, 5.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1E3A8A'))
    ax.text(8.9, 5.5, "1", fontsize=8.5, color='#1E3A8A', fontweight='bold')
    ax.text(8.9, 4.6, "0..*", fontsize=8.5, color='#1E3A8A', fontweight='bold')

    # User -> SubChannelAdmin (1 to N)
    ax.annotate("", xy=(2.7, 4.5), xytext=(2.7, 5.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1E3A8A'))
    ax.text(2.8, 5.5, "1", fontsize=8.5, color='#1E3A8A', fontweight='bold')
    ax.text(2.8, 4.6, "0..*", fontsize=8.5, color='#1E3A8A', fontweight='bold')

    # SubChannel -> SubChannelAdmin (1 to N)
    ax.annotate("", xy=(4.2, 3.2), xytext=(7.3, 3.2), arrowprops=dict(arrowstyle="->", lw=1.5, color='#1E3A8A'))
    ax.text(7.0, 3.35, "1", fontsize=8.5, color='#1E3A8A', fontweight='bold')
    ax.text(4.4, 3.35, "0..*", fontsize=8.5, color='#1E3A8A', fontweight='bold')

    # Enums Box
    enum_box = patches.FancyBboxPatch((4.2, 0.4), 3.1, 1.4, boxstyle="round,pad=0.08", fc='#EFF6FF', ec='#3B82F6', lw=1.2)
    ax.add_patch(enum_box)
    ax.text(5.75, 1.55, "<<Enumerations>>", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E3A8A')
    ax.text(4.4, 1.2, "• Role: USER, ADMIN", fontsize=8, color='#0F172A')
    ax.text(4.4, 0.9, "• ChannelType: PUBLIC, PRIVATE", fontsize=8, color='#0F172A')
    ax.text(4.4, 0.6, "• MessageType: CHAT, JOIN, LEAVE", fontsize=8, color='#0F172A')

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "uml_class_diagram.png")
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

def draw_websocket_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 7.2), dpi=220)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    ax.text(5.25, 7.8, "CampiFi — WebSocket & STOMP Real-Time Messaging Architecture",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E3A8A')

    # Client A Box
    boxA = patches.FancyBboxPatch((0.5, 3.8), 2.2, 3.2, boxstyle="round,pad=0.08", fc='#EFF6FF', ec='#3B82F6', lw=1.5)
    ax.add_patch(boxA)
    ax.text(1.6, 6.6, "Client A (Sender)", ha='center', fontsize=10, fontweight='bold', color='#1E3A8A')
    ax.text(1.6, 5.3, "• SockJS('/ws')\n• Stomp.over(socket)\n• Room: 'CSE Core'\n• User: 'Vikram'\n• Types message &\n  clicks 'Send'",
            ha='center', fontsize=8, color='#0F172A')

    # Server Box
    boxS = patches.FancyBboxPatch((3.7, 2.5), 3.1, 4.6, boxstyle="round,pad=0.08", fc='#FAF5FF', ec='#8B5CF6', lw=1.5)
    ax.add_patch(boxS)
    ax.text(5.25, 6.8, "Spring Boot Server", ha='center', fontsize=11, fontweight='bold', color='#6D28D9')
    ax.text(5.25, 6.4, "Embedded Tomcat @ Port 8080", ha='center', fontsize=8, color='#64748B')

    # In-memory STOMP Broker sub-box
    broker = patches.FancyBboxPatch((3.9, 2.8), 2.7, 3.3, boxstyle="round,pad=0.05", fc='white', ec='#8B5CF6', lw=1)
    ax.add_patch(broker)
    ax.text(5.25, 5.8, "STOMP Message Broker", ha='center', fontsize=9, fontweight='bold', color='#6D28D9')
    ax.text(5.25, 4.4, "@MessageMapping\n'/app/chat/{room}'\n\nAttaches Timestamp\n(HH:mm:ss)\n\n@SendTo\n'/topic/room/{room}'",
            ha='center', fontsize=8, color='#0F172A')

    # Client B Box
    boxB = patches.FancyBboxPatch((7.8, 3.8), 2.2, 3.2, boxstyle="round,pad=0.08", fc='#EFF6FF', ec='#3B82F6', lw=1.5)
    ax.add_patch(boxB)
    ax.text(8.9, 6.6, "Client B (Receiver)", ha='center', fontsize=10, fontweight='bold', color='#1E3A8A')
    ax.text(8.9, 5.3, "• SockJS('/ws')\n• Subscribed to\n  '/topic/room/CSE Core'\n• Receives payload\n• Renders incoming\n  bubble instantly",
            ha='center', fontsize=8, color='#0F172A')

    # Arrows
    ax.annotate("STOMP SEND\n/app/chat/CSE Core", xy=(3.7, 5.0), xytext=(2.7, 5.0),
                arrowprops=dict(arrowstyle="->", lw=1.8, color='#3B82F6'),
                fontsize=7.8, ha='center', va='bottom', color='#1E3A8A')

    ax.annotate("STOMP MESSAGE\n/topic/room/CSE Core", xy=(7.8, 5.0), xytext=(6.8, 5.0),
                arrowprops=dict(arrowstyle="->", lw=1.8, color='#10B981'),
                fontsize=7.8, ha='center', va='bottom', color='#065F46')

    # Summary box
    sum_box = patches.FancyBboxPatch((1.0, 0.8), 8.5, 1.3, boxstyle="round,pad=0.08", fc='#F8FAFC', ec='#CBD5E1', lw=1)
    ax.add_patch(sum_box)
    ax.text(5.25, 1.7, "Key Advantage: True Full-Duplex TCP Connection", ha='center', fontsize=9.5, fontweight='bold', color='#0F172A')
    ax.text(5.25, 1.2, "No HTTP polling overhead: Messages travel over a persistent TCP socket with <6 bytes overhead, arriving in <10ms.",
            ha='center', fontsize=8.5, color='#475569')

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "websocket_architecture.png")
    plt.savefig(out, bbox_inches='tight')
    plt.close()
    print("Saved:", out)

if __name__ == "__main__":
    draw_system_architecture()
    draw_uml_class_diagram()
    draw_websocket_diagram()
    print("Regenerated cleanly!")
