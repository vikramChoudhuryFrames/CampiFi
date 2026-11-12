package com.hotspotchat.controller;

import com.hotspotchat.model.User;
import com.hotspotchat.service.OtpService;
import com.hotspotchat.service.SessionService;
import com.hotspotchat.service.SessionService.SessionData;
import com.hotspotchat.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * REST endpoints for the Admin OTP login flow.
 *
 * Flow:
 *   1. Client: POST /api/auth/request-otp  { email }
 *      Server: generates OTP → saves to DB → sends to email (or prints to console)
 *      Response: { status: "ok", message: "OTP sent to ..." }
 *
 *   2. Client: POST /api/auth/verify-otp   { email, otp }
 *      Server: validates OTP → marks used → creates session token
 *      Response: { status: "ok", token, displayName, email, role }
 *
 *   3. Client stores token in sessionStorage, sends it as "X-Session-Token" header.
 *
 *   4. Client: GET  /api/auth/check-session   (header: X-Session-Token)
 *      Response: { valid: true/false, displayName, role }
 *
 *   5. Client: POST /api/auth/logout          (header: X-Session-Token)
 *      Response: { status: "ok" }
 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final OtpService otpService;
    private final UserService userService;
    private final SessionService sessionService;

    @Autowired
    public AuthController(OtpService otpService,
                          UserService userService,
                          SessionService sessionService) {
        this.otpService = otpService;
        this.userService = userService;
        this.sessionService = sessionService;
    }

    // ── 1. Request OTP ────────────────────────────────────────────────────────

    /**
     * Generates and sends a 6-digit OTP to the institution email.
     * Also ensures the user record exists in the database.
     */
    @PostMapping("/request-otp")
    public ResponseEntity<Map<String, String>> requestOtp(
            @RequestBody Map<String, String> body) {

        String email = body.get("email");
        if (email == null || !email.contains("@")) {
            return ResponseEntity.badRequest().body(
                    error("Please provide a valid institution email address."));
        }

        email = email.trim().toLowerCase();

        // Ensure user exists in DB
        userService.findOrCreate(email);

        // Generate OTP, save, send (or print to console)
        otpService.generateAndSend(email);

        Map<String, String> resp = new HashMap<>();
        resp.put("status", "ok");
        resp.put("message", "OTP sent to " + email + ". Check your inbox (or the server console for local testing).");
        return ResponseEntity.ok(resp);
    }

    // ── 2. Verify OTP ─────────────────────────────────────────────────────────

    /**
     * Validates the OTP submitted by the admin candidate.
     * On success: creates a session and returns role information.
     */
    @PostMapping("/verify-otp")
    public ResponseEntity<Map<String, Object>> verifyOtp(
            @RequestBody Map<String, String> body) {

        String email = body.get("email");
        String otp   = body.get("otp");

        if (email == null || otp == null) {
            return ResponseEntity.badRequest().body(
                    errorObj("Email and OTP are required."));
        }

        email = email.trim().toLowerCase();
        otp   = otp.trim();

        if (!otpService.verify(email, otp)) {
            return ResponseEntity.status(401).body(
                    errorObj("Invalid or expired OTP. Please request a new one."));
        }

        // Fetch the user (they were created during request-otp)
        User user = userService.findOrCreate(email);

        // Create session
        String token = sessionService.createSession(user);

        Map<String, Object> resp = new HashMap<>();
        resp.put("status", "ok");
        resp.put("token", token);
        resp.put("displayName", user.getDisplayName());
        resp.put("email", user.getEmail());
        resp.put("role", user.getRole().name()); // "USER" or "ADMIN"
        return ResponseEntity.ok(resp);
    }

    // ── 3. Check session ──────────────────────────────────────────────────────

    /**
     * Validates a session token. Used by the frontend on page load to
     * restore the session without re-authenticating.
     */
    @GetMapping("/check-session")
    public ResponseEntity<Map<String, Object>> checkSession(HttpServletRequest request) {
        String token = request.getHeader("X-Session-Token");
        Optional<SessionData> session = sessionService.getSession(token);

        Map<String, Object> resp = new HashMap<>();
        if (session.isEmpty()) {
            resp.put("valid", false);
            return ResponseEntity.ok(resp);
        }

        SessionData s = session.get();
        resp.put("valid", true);
        resp.put("displayName", s.displayName());
        resp.put("email", s.email());
        resp.put("role", s.role().name());
        return ResponseEntity.ok(resp);
    }

    // ── 4. Logout ─────────────────────────────────────────────────────────────

    /**
     * Invalidates the session token (logout).
     */
    @PostMapping("/logout")
    public ResponseEntity<Map<String, String>> logout(HttpServletRequest request) {
        String token = request.getHeader("X-Session-Token");
        sessionService.invalidate(token);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "Logged out."));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private Map<String, String> error(String message) {
        Map<String, String> m = new HashMap<>();
        m.put("status", "error");
        m.put("message", message);
        return m;
    }

    private Map<String, Object> errorObj(String message) {
        Map<String, Object> m = new HashMap<>();
        m.put("status", "error");
        m.put("message", message);
        return m;
    }

    // ── 5. Regular user login (no OTP needed) ─────────────────────────────────

    /**
     * Creates a session for regular (non-admin) users connecting via the Connect form.
     * No OTP is required — network subnet verification is the sole auth mechanism.
     *
     * Body: { "email": "student@uni.edu" }
     * Response: { status, token, displayName, email, role }
     *
     * This endpoint is called by Task 5's updated Connect form
     * so that regular users also get a session token for the channel browser.
     */
    @PostMapping("/login")
    public ResponseEntity<Map<String, Object>> userLogin(
            @RequestBody Map<String, String> body) {

        String email = body.get("email");
        if (email == null || !email.contains("@")) {
            return ResponseEntity.badRequest().body(
                    errorObj("Please provide a valid institution email address."));
        }

        email = email.trim().toLowerCase();

        User user = userService.findOrCreate(email);
        String token = sessionService.createSession(user);

        Map<String, Object> resp = new HashMap<>();
        resp.put("status", "ok");
        resp.put("token", token);
        resp.put("displayName", user.getDisplayName());
        resp.put("email", user.getEmail());
        resp.put("role", user.getRole().name());
        return ResponseEntity.ok(resp);
    }
}

