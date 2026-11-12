import os
os.environ['MPLCONFIGDIR'] = '/tmp'
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_gui_diagram():
    fig = plt.figure(figsize=(15, 10), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background
    bg = patches.Rectangle((0, 0), 15, 10, facecolor='#0D1117', edgecolor='none')
    ax.add_patch(bg)

    # Title Banner
    banner = patches.FancyBboxPatch((0.5, 9.0), 14.0, 0.8, boxstyle="round,pad=0.1",
                                   facecolor='#161B22', edgecolor='#30363D', linewidth=1.5)
    ax.add_patch(banner)
    ax.text(7.5, 9.42, "CampiFi — Graphical User Interface (GUI) Architecture & Screen Wireframes",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#E6EDF3', fontfamily='sans-serif')
    ax.text(7.5, 9.15, "Zero-Cloud Offline UI: Semantic HTML5, CSS3 Variables, Vanilla JS ES6+, SockJS & STOMP.js",
            ha='center', va='center', fontsize=9.2, color='#58A6FF', fontfamily='sans-serif')

    # 4 GUI Screen Panels (2x2 Grid)
    screens = [
        # Screen 1: Client Connect / Auth View (Top Left)
        {
            "num": "1",
            "title": "Client Connect View (index.html)",
            "subtitle": "Zero-Friction Institution Authentication",
            "tag": "Entry Screen",
            "tag_color": "#238636",
            "x": 0.6, "y": 4.8, "w": 6.6, "h": 3.9,
            "mockup_type": "auth",
            "features": [
                "• Lightweight single-column card layout (max-width: 420px)",
                "• Auto-validating email input (@college.edu / @domain)",
                "• In-memory session token storage (sessionStorage)",
                "• Dynamic inline error banners (no disruptive popups)",
                "• Auto-redirects to /channels.html upon instant verification"
            ]
        },
        # Screen 2: Networks & PIN Modal (Top Right)
        {
            "num": "2",
            "title": "Network & Sub-Network Browser (channels.html)",
            "subtitle": "Network Directory with 4-Digit PIN Security",
            "tag": "Directory & PIN",
            "tag_color": "#1F6FEB",
            "x": 7.8, "y": 4.8, "w": 6.6, "h": 3.9,
            "mockup_type": "channels",
            "features": [
                "• Responsive CSS Grid displaying Public & Private networks",
                "• Color-coded badges: Green for PUBLIC, Amber for PRIVATE",
                "• Interactive 4-digit PIN Modal with auto-focus digit hopping",
                "• Hierarchical Sub-Network accordion drilldown (CSE Core A ➔ Prof. Sharma)",
                "• Live user role badge (Student vs Admin) in sticky navigation"
            ]
        },
        # Screen 3: Real-Time Chat Screen (Bottom Left)
        {
            "num": "3",
            "title": "Real-Time Hotspot Chat Interface (chat.html)",
            "subtitle": "Full-Duplex WhatsApp-Style Chat Experience",
            "tag": "Core Chat UI",
            "tag_color": "#2EA043",
            "x": 0.6, "y": 0.6, "w": 6.6, "h": 3.9,
            "mockup_type": "chat",
            "features": [
                "• Top App Bar: Channel label, back navigation & active member count",
                "• Online presence strip: Real-time active user pill tags",
                "• Distinct message bubbles: Dark-green for sent, Slate for received",
                "• Paperclip attachment trigger with drag-and-drop file upload",
                "• Auto-scrolling message viewport & WebSocket connection status"
            ]
        },
        # Screen 4: Server Admin Dashboard (Bottom Right)
        {
            "num": "4",
            "title": "Server Admin & Network Management (admin.html)",
            "subtitle": "Privileged Network & Access Control Dashboard",
            "tag": "Management Panel",
            "tag_color": "#8957E5",
            "x": 7.8, "y": 0.6, "w": 6.6, "h": 3.9,
            "mockup_type": "admin",
            "features": [
                "• Split Admin Layout: Left sidebar navigation + Main content area",
                "• Dynamic Network Creator: Toggle Public broadcast vs Private PIN",
                "• Collapsible Sub-Channel hierarchy tree (▶/▼ dropdown toggle)",
                "• Admin Delegation Modals: Assign Master Admins & Sub-Channel Admins",
                "• Participant moderation controls: View members, remove, and ban"
            ]
        }
    ]

    for s in screens:
        # Card outer border
        card = patches.FancyBboxPatch((s["x"], s["y"]), s["w"], s["h"],
                                     boxstyle="round,pad=0.08",
                                     facecolor='#161B22',
                                     edgecolor='#30363D',
                                     linewidth=1.3)
        ax.add_patch(card)

        # Card header bar
        header_h = 0.65
        hdr = patches.FancyBboxPatch((s["x"], s["y"] + s["h"] - header_h), s["w"], header_h,
                                    boxstyle="round,pad=0.05",
                                    facecolor='#21262D',
                                    edgecolor='#30363D')
        ax.add_patch(hdr)

        # Title & Subtitle
        ax.text(s["x"] + 0.2, s["y"] + s["h"] - 0.25,
                f"[{s['num']}]  {s['title']}",
                fontsize=9.8, fontweight='bold', color='#E6EDF3', fontfamily='sans-serif')
        ax.text(s["x"] + 0.2, s["y"] + s["h"] - 0.48,
                s["subtitle"],
                fontsize=8.0, fontstyle='italic', color='#8B949E', fontfamily='sans-serif')

        # Tag pill
        tag_w = 1.35
        tag_box = patches.FancyBboxPatch((s["x"] + s["w"] - tag_w - 0.2, s["y"] + s["h"] - 0.48), tag_w, 0.32,
                                        boxstyle="round,pad=0.04",
                                        facecolor=s["tag_color"], edgecolor='none')
        ax.add_patch(tag_box)
        ax.text(s["x"] + s["w"] - (tag_w/2) - 0.2, s["y"] + s["h"] - 0.32,
                s["tag"],
                ha='center', va='center', fontsize=7.2, fontweight='bold', color='white', fontfamily='sans-serif')

        # Visual Wireframe Box (Left side of card)
        wire_w = 2.4
        wire_h = 2.85
        wire_x = s["x"] + 0.2
        wire_y = s["y"] + 0.25
        wire_box = patches.Rectangle((wire_x, wire_y), wire_w, wire_h,
                                    facecolor='#0D1117', edgecolor='#30363D', linewidth=0.8)
        ax.add_patch(wire_box)

        # Draw mini UI wireframe based on mockup_type
        if s["mockup_type"] == "auth":
            # Header
            ax.text(wire_x + 1.2, wire_y + 2.5, "CampiFi", ha='center', fontsize=8, fontweight='bold', color='#58A6FF')
            ax.text(wire_x + 1.2, wire_y + 2.3, "CAMPUS CHAT", ha='center', fontsize=5, color='#8B949E')
            # Box
            box = patches.Rectangle((wire_x + 0.25, wire_y + 1.2), 1.9, 0.9, facecolor='#161B22', edgecolor='#30363D')
            ax.add_patch(box)
            ax.text(wire_x + 1.2, wire_y + 1.85, "Connect", ha='center', fontsize=6.5, fontweight='bold', color='#E6EDF3')
            # Input
            inp = patches.Rectangle((wire_x + 0.4, wire_y + 1.5), 1.6, 0.22, facecolor='#0D1117', edgecolor='#30363D')
            ax.add_patch(inp)
            ax.text(wire_x + 0.5, wire_y + 1.61, "email@college.edu", fontsize=5, color='#7D8590')
            # Button
            btn = patches.Rectangle((wire_x + 0.4, wire_y + 1.25), 1.6, 0.2, facecolor='#1F6FEB', edgecolor='none')
            ax.add_patch(btn)
            ax.text(wire_x + 1.2, wire_y + 1.35, "Connect", ha='center', va='center', fontsize=5.5, fontweight='bold', color='white')

        elif s["mockup_type"] == "channels":
            # Topbar
            top = patches.Rectangle((wire_x, wire_y + 2.55), wire_w, 0.3, facecolor='#161B22', edgecolor='none')
            ax.add_patch(top)
            ax.text(wire_x + 0.15, wire_y + 2.7, "CampiFi", fontsize=6, fontweight='bold', color='#58A6FF')
            # Network Cards
            c1 = patches.Rectangle((wire_x + 0.15, wire_y + 1.65), 2.1, 0.75, facecolor='#161B22', edgecolor='#238636', linewidth=0.8)
            ax.add_patch(c1)
            ax.text(wire_x + 0.25, wire_y + 2.22, "Announcements", fontsize=5.5, fontweight='bold', color='#E6EDF3')
            ax.text(wire_x + 0.25, wire_y + 2.05, "PUBLIC BROADCAST", fontsize=4.2, color='#2EA043')

            c2 = patches.Rectangle((wire_x + 0.15, wire_y + 0.75), 2.1, 0.75, facecolor='#161B22', edgecolor='#D29922', linewidth=0.8)
            ax.add_patch(c2)
            ax.text(wire_x + 0.25, wire_y + 1.32, "CSE Core A", fontsize=5.5, fontweight='bold', color='#E6EDF3')
            ax.text(wire_x + 0.25, wire_y + 1.15, "PRIVATE • PIN [LOCK]", fontsize=4.2, color='#D29922')

            # PIN Modal overlay
            modal = patches.Rectangle((wire_x + 0.35, wire_y + 0.1), 1.7, 0.55, facecolor='#21262D', edgecolor='#58A6FF', linewidth=0.8)
            ax.add_patch(modal)
            ax.text(wire_x + 1.2, wire_y + 0.48, "PIN: [ 1 ][ 2 ][ 3 ][ 4 ]", ha='center', fontsize=4.8, color='#58A6FF')

        elif s["mockup_type"] == "chat":
            # Header
            top = patches.Rectangle((wire_x, wire_y + 2.55), wire_w, 0.3, facecolor='#161B22', edgecolor='none')
            ax.add_patch(top)
            ax.text(wire_x + 0.15, wire_y + 2.7, "← Prof. Sharma", fontsize=5.5, fontweight='bold', color='#E6EDF3')
            ax.text(wire_x + 2.25, wire_y + 2.7, "3 online", ha='right', fontsize=4.5, color='#7EE787')
            # Messages
            m1 = patches.Rectangle((wire_x + 0.15, wire_y + 1.95), 1.5, 0.45, facecolor='#161B22', edgecolor='#30363D')
            ax.add_patch(m1)
            ax.text(wire_x + 0.25, wire_y + 2.25, "Prof. Sharma:", fontsize=4.5, fontweight='bold', color='#58A6FF')
            ax.text(wire_x + 0.25, wire_y + 2.07, "Class starts in 5 mins", fontsize=4.5, color='#E6EDF3')

            m2 = patches.Rectangle((wire_x + 0.75, wire_y + 1.35), 1.5, 0.45, facecolor='#238636', edgecolor='none')
            ax.add_patch(m2)
            ax.text(wire_x + 0.85, wire_y + 1.65, "You:", fontsize=4.5, fontweight='bold', color='white')
            ax.text(wire_x + 0.85, wire_y + 1.47, "Understood, joining!", fontsize=4.5, color='white')

            # Composer
            comp = patches.Rectangle((wire_x + 0.1, wire_y + 0.1), 2.2, 0.35, facecolor='#161B22', edgecolor='#30363D')
            ax.add_patch(comp)
            ax.text(wire_x + 0.25, wire_y + 0.27, "[+] Type message...", fontsize=4.8, color='#7D8590')
            send_btn = patches.Rectangle((wire_x + 1.85, wire_y + 0.15), 0.4, 0.25, facecolor='#1F6FEB', edgecolor='none')
            ax.add_patch(send_btn)
            ax.text(wire_x + 2.05, wire_y + 0.27, ">", ha='center', va='center', fontsize=5.5, color='white')

        elif s["mockup_type"] == "admin":
            # Sidebar + Content
            side = patches.Rectangle((wire_x, wire_y), 0.7, wire_h, facecolor='#161B22', edgecolor='none')
            ax.add_patch(side)
            ax.text(wire_x + 0.35, wire_y + 2.65, "Admin", ha='center', fontsize=5, fontweight='bold', color='#BC8CFF')
            ax.text(wire_x + 0.35, wire_y + 2.35, "• Networks", ha='center', fontsize=4.5, color='#58A6FF')
            ax.text(wire_x + 0.35, wire_y + 2.15, "• Users", ha='center', fontsize=4.5, color='#8B949E')

            # Main content area
            main_b = patches.Rectangle((wire_x + 0.75, wire_y + 1.7), 1.55, 1.05, facecolor='#161B22', edgecolor='#30363D')
            ax.add_patch(main_b)
            ax.text(wire_x + 0.85, wire_y + 2.55, "Manage Networks", fontsize=5.2, fontweight='bold', color='#E6EDF3')
            ax.text(wire_x + 0.85, wire_y + 2.32, "▼ CSE Core A", fontsize=4.8, color='#58A6FF')
            ax.text(wire_x + 1.05, wire_y + 2.15, "• Prof. Sharma", fontsize=4.2, color='#8B949E')
            ax.text(wire_x + 1.05, wire_y + 1.98, "• Prof. Gupta", fontsize=4.2, color='#8B949E')

            create_b = patches.Rectangle((wire_x + 0.75, wire_y + 0.5), 1.55, 0.9, facecolor='#161B22', edgecolor='#238636', linewidth=0.8)
            ax.add_patch(create_b)
            ax.text(wire_x + 0.85, wire_y + 1.2, "+ New Network", fontsize=5, fontweight='bold', color='#2EA043')
            ax.text(wire_x + 0.85, wire_y + 0.95, "[ Network Name ]", fontsize=4.2, color='#7D8590')
            ax.text(wire_x + 0.85, wire_y + 0.75, "[ Public / Private ]", fontsize=4.2, color='#7D8590')

        # Feature bullet points on Right side of card
        fx = s["x"] + wire_w + 0.4
        fy = s["y"] + s["h"] - 0.9
        for f in s["features"]:
            ax.text(fx, fy, f, fontsize=7.3, color='#C9D1D9', fontfamily='sans-serif')
            fy -= 0.5

    # Bottom Footer
    ax.text(7.5, 0.2, "CampiFi GUI Architecture — Lightweight, High-Performance, Zero-Internet Offline Web UI Engine",
            ha='center', va='center', fontsize=8.5, color='#8B949E', fontstyle='italic', fontfamily='sans-serif')

    os.makedirs('/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams', exist_ok=True)
    out_path = '/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams/gui_architecture.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='#0D1117', bbox_inches='tight')
    plt.close()
    print(f"GUI Diagram successfully generated at: {out_path}")

if __name__ == '__main__':
    generate_gui_diagram()
