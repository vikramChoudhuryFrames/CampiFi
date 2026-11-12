import os
os.environ['MPLCONFIGDIR'] = '/tmp'
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_db_diagram():
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
    ax.text(7.5, 9.42, "CampiFi — Database Connectivity & JDBC Architecture Pipeline",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='white', fontfamily='sans-serif')
    ax.text(7.5, 9.15, "Connecting Spring Data JPA, Hibernate ORM, HikariCP Connection Pool, and MySQL JDBC Driver",
            ha='center', va='center', fontsize=9.2, color='#93C5FD', fontfamily='sans-serif')

    # Top Half: 6-Stage Connectivity Pipeline (Flowchart from Application to MySQL)
    pipeline_y = 6.6
    pipe_h = 1.8
    stages = [
        ("1. Business Service", "ChannelService\nUserService\n@Transactional", "#0284C7", 0.6, 2.1),
        ("2. JPA Repository", "UserRepository\nChannelRepository\n(Interface Contract)", "#0D9488", 3.0, 2.1),
        ("3. Hibernate ORM", "SQL Generation\nEntity Hydration\nDirty Checking", "#7C3AED", 5.4, 2.1),
        ("4. HikariCP Pool", "TCP Connection Pool\nMin: 10 / Max: 20\nZero Connection Lag", "#D97706", 7.8, 2.1),
        ("5. MySQL JDBC Driver", "com.mysql.cj.jdbc.Driver\nPreparedStatement\njava.sql.ResultSet", "#B91C1C", 10.2, 2.1),
        ("6. MySQL Database", "Port: 3306\nSchema: campifi\nInnoDB 3NF Tables", "#15803D", 12.6, 1.8),
    ]

    for title, desc, color, x, w in stages:
        box = patches.FancyBboxPatch((x, pipeline_y), w, pipe_h,
                                    boxstyle="round,pad=0.08",
                                    facecolor='white',
                                    edgecolor=color,
                                    linewidth=1.5)
        ax.add_patch(box)

        # Header bar
        hdr = patches.FancyBboxPatch((x, pipeline_y + pipe_h - 0.45), w, 0.45,
                                    boxstyle="round,pad=0.04",
                                    facecolor=color,
                                    edgecolor=color)
        ax.add_patch(hdr)
        ax.text(x + w/2, pipeline_y + pipe_h - 0.23, title,
                ha='center', va='center', fontsize=7.8, fontweight='bold', color='white', fontfamily='sans-serif')

        # Desc
        ax.text(x + w/2, pipeline_y + 0.65, desc,
                ha='center', va='center', fontsize=7.2, color='#334155', fontfamily='sans-serif')

    # Connecting Arrows between pipeline stages
    arrow_points = [(2.7, 7.5), (5.1, 7.5), (7.5, 7.5), (9.9, 7.5), (12.3, 7.5)]
    for ax_pt, ay_pt in arrow_points:
        ax.annotate("", xy=(ax_pt + 0.3, ay_pt), xytext=(ax_pt, ay_pt),
                    arrowprops=dict(arrowstyle="->", color="#1E3A8A", lw=2, mutation_scale=15))

    # Sub-label for pipeline
    ax.text(7.5, 6.2, "Figure 1A: End-to-End Database Connectivity Execution Pipeline (High-Level Request Flow)",
            ha='center', va='center', fontsize=8.2, fontstyle='italic', color='#475569', fontfamily='sans-serif')

    # Bottom Half: The 4 Fundamental CRUD Operations (Cards 1 to 4)
    crud_cards = [
        # 1. Create (Insertion)
        {
            "num": "C",
            "title": "INSERTION (Create)",
            "hdr_color": "#0284C7",
            "bg_color": "#F0F9FF",
            "border": "#38BDF8",
            "x": 0.6, "y": 0.6, "w": 3.3, "h": 5.2,
            "jpa_call": "userRepository.save(new User(...));",
            "sql_stmt": "INSERT INTO users\n(email, display_name, role,\n created_at)\nVALUES (?, ?, ?, ?);",
            "jdbc_under": "• conn.prepareStatement(sql, ...)\n• stmt.setString(1, email)\n• stmt.executeUpdate()\n• rs = stmt.getGeneratedKeys()\n• user.setId(rs.getLong(1))",
            "viva_point": "Auto-generates Primary Key\nvia MySQL IDENTITY column."
        },
        # 2. Read (Retrieval)
        {
            "num": "R",
            "title": "RETRIEVAL (Read)",
            "hdr_color": "#0D9488",
            "bg_color": "#F0FDFA",
            "border": "#2DD4BF",
            "x": 4.15, "y": 0.6, "w": 3.3, "h": 5.2,
            "jpa_call": "userRepository.findByEmail(email);",
            "sql_stmt": "SELECT id, email,\n       display_name, role,\n       created_at\nFROM users WHERE email = ?;",
            "jdbc_under": "• stmt = conn.prepareStatement(sql)\n• stmt.setString(1, email)\n• ResultSet rs = stmt.executeQuery()\n• while (rs.next()) { ... }\n• Entity mapped from columns",
            "viva_point": "Wrapped in Optional<User>\nto guarantee null-safety."
        },
        # 3. Update (Updating)
        {
            "num": "U",
            "title": "UPDATING (Update)",
            "hdr_color": "#D97706",
            "bg_color": "#FFFBEB",
            "border": "#FBBF24",
            "x": 7.7, "y": 0.6, "w": 3.3, "h": 5.2,
            "jpa_call": "user.setRole(Role.ADMIN);\nuserRepository.save(user);",
            "sql_stmt": "UPDATE users\nSET role = ?, display_name = ?\nWHERE id = ?;",
            "jdbc_under": "• Hibernate Dirty Checking\n• Detects field mutation in RAM\n• PreparedStatement prepared\n• stmt.setString(1, 'ADMIN')\n• stmt.setLong(3, userId)",
            "viva_point": "Scoped within @Transactional\nfor automatic atomic commit."
        },
        # 4. Delete (Deletion)
        {
            "num": "D",
            "title": "DELETION (Delete)",
            "hdr_color": "#B91C1C",
            "bg_color": "#FEF2F2",
            "border": "#F87171",
            "x": 11.25, "y": 0.6, "w": 3.15, "h": 5.2,
            "jpa_call": "adminRepo.delete(admin);\nchannelRepo.deleteById(id);",
            "sql_stmt": "DELETE FROM sub_channel_admins\nWHERE id = ?;",
            "jdbc_under": "• stmt = conn.prepareStatement(sql)\n• stmt.setLong(1, adminId)\n• stmt.executeUpdate()\n• CascadeType.ALL triggers\n  cascading deletes for orphans",
            "viva_point": "Referential integrity enforced\nvia MySQL Foreign Keys."
        }
    ]

    for c in crud_cards:
        # Box frame
        box = patches.FancyBboxPatch((c["x"], c["y"]), c["w"], c["h"],
                                    boxstyle="round,pad=0.08",
                                    facecolor=c["bg_color"],
                                    edgecolor=c["border"],
                                    linewidth=1.3)
        ax.add_patch(box)

        # Header bar
        header_h = 0.55
        hdr = patches.FancyBboxPatch((c["x"], c["y"] + c["h"] - header_h), c["w"], header_h,
                                    boxstyle="round,pad=0.04",
                                    facecolor=c["hdr_color"],
                                    edgecolor=c["hdr_color"])
        ax.add_patch(hdr)
        ax.text(c["x"] + c["w"]/2, c["y"] + c["h"] - 0.28,
                f"[{c['num']}]  {c['title']}",
                ha='center', va='center', fontsize=9.2, fontweight='bold', color='white', fontfamily='sans-serif')

        # 1. Spring Data JPA Code
        curr_y = c["y"] + c["h"] - 0.8
        ax.text(c["x"] + 0.15, curr_y, "1. Spring Data JPA Operation:", fontsize=7.5, fontweight='bold', color=c["hdr_color"])
        curr_y -= 0.22
        jpa_box = patches.Rectangle((c["x"] + 0.15, curr_y - 0.35), c["w"] - 0.3, 0.5, facecolor='white', edgecolor='#CBD5E1', linewidth=0.6)
        ax.add_patch(jpa_box)
        ax.text(c["x"] + 0.25, curr_y - 0.12, c["jpa_call"], fontsize=6.8, fontfamily='monospace', color='#0F172A')

        # 2. Generated SQL
        curr_y -= 0.65
        ax.text(c["x"] + 0.15, curr_y, "2. Generated SQL Query:", fontsize=7.5, fontweight='bold', color=c["hdr_color"])
        curr_y -= 0.22
        sql_box = patches.Rectangle((c["x"] + 0.15, curr_y - 0.65), c["w"] - 0.3, 0.8, facecolor='#1E293B', edgecolor='none')
        ax.add_patch(sql_box)
        ax.text(c["x"] + 0.25, curr_y - 0.25, c["sql_stmt"], fontsize=6.3, fontfamily='monospace', color='#38BDF8')

        # 3. Underlying JDBC Operations
        curr_y -= 0.95
        ax.text(c["x"] + 0.15, curr_y, "3. Underlying JDBC Execution:", fontsize=7.5, fontweight='bold', color=c["hdr_color"])
        curr_y -= 0.22
        ax.text(c["x"] + 0.2, curr_y - 0.45, c["jdbc_under"], fontsize=6.8, color='#334155', fontfamily='sans-serif')

        # 4. Viva Tip
        curr_y -= 1.15
        tip_box = patches.Rectangle((c["x"] + 0.15, curr_y - 0.4), c["w"] - 0.3, 0.5, facecolor='#FEF3C7', edgecolor='#F59E0B', linewidth=0.6)
        ax.add_patch(tip_box)
        ax.text(c["x"] + 0.22, curr_y - 0.18, "Viva Highlight:\n" + c["viva_point"], fontsize=6.5, color='#92400E', fontfamily='sans-serif')

    ax.text(7.5, 0.2, "CampiFi Database Architecture Artifact — 100% Parameterized JDBC Queries via Hibernate ORM & HikariCP",
            ha='center', va='center', fontsize=8.2, color='#64748B', fontstyle='italic', fontfamily='sans-serif')

    os.makedirs('/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams', exist_ok=True)
    out_path = '/run/media/moxienox/New Volume/javaProj/hotspot-chat/diagrams/database_connectivity_architecture.png'
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='#F8FAFC', bbox_inches='tight')
    plt.close()
    print(f"Database diagram successfully generated at: {out_path}")

if __name__ == '__main__':
    generate_db_diagram()
