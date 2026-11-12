package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Represents a registered user (parsed from institution email).
 * Role USER  → regular participant
 * Role ADMIN → channel admin (can ban/remove, set via OTP flow)
 */
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 255)
    private String email;

    @Column(nullable = false, length = 100)
    private String displayName;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role = Role.USER;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public enum Role { USER, ADMIN }

    public User() {}

    public User(String email, String displayName, Role role) {
        this.email = email;
        this.displayName = displayName;
        this.role = role;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getDisplayName() { return displayName; }
    public void setDisplayName(String displayName) { this.displayName = displayName; }
    public Role getRole() { return role; }
    public void setRole(Role role) { this.role = role; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
