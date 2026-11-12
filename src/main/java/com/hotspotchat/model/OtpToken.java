package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Stores a one-time password (OTP) for admin login verification.
 * OTPs are 6-digit, expire after 5 minutes, and are single-use.
 */
@Entity
@Table(name = "otp_tokens")
public class OtpToken {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 255)
    private String email;

    @Column(nullable = false, length = 6)
    private String otp;

    @Column(nullable = false)
    private LocalDateTime expiresAt;

    @Column(nullable = false)
    private boolean used = false;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public OtpToken() {}

    public OtpToken(String email, String otp) {
        this.email = email;
        this.otp = otp;
        this.expiresAt = LocalDateTime.now().plusMinutes(5);
    }

    public boolean isExpired() {
        return LocalDateTime.now().isAfter(expiresAt);
    }

    public boolean isValid(String inputOtp) {
        return !used && !isExpired() && otp.equals(inputOtp);
    }

    // Getters & Setters
    public Long getId() { return id; }
    public String getEmail() { return email; }
    public String getOtp() { return otp; }
    public LocalDateTime getExpiresAt() { return expiresAt; }
    public boolean isUsed() { return used; }
    public void setUsed(boolean used) { this.used = used; }
    public LocalDateTime getCreatedAt() { return createdAt; }
}
