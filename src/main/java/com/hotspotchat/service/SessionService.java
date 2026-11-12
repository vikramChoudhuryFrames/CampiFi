package com.hotspotchat.service;

import com.hotspotchat.model.User;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Lightweight in-memory session manager.
 *
 * After a successful OTP verification, the client receives a UUID session token.
 * The client stores this in sessionStorage and sends it as the
 * "X-Session-Token" header on protected requests.
 *
 * Sessions are lost on server restart (intentional — campus sessions are ephemeral).
 * Sessions auto-expire after 8 hours of inactivity.
 */
@Service
public class SessionService {

    /** Session lifetime: 8 hours */
    private static final long SESSION_HOURS = 8;

    private final ConcurrentHashMap<String, SessionData> sessions = new ConcurrentHashMap<>();

    /**
     * Creates a new session for the given user and returns the session token.
     */
    public String createSession(User user) {
        String token = UUID.randomUUID().toString();
        sessions.put(token, new SessionData(
                user.getId(),
                user.getEmail(),
                user.getDisplayName(),
                user.getRole(),
                LocalDateTime.now().plusHours(SESSION_HOURS)
        ));
        return token;
    }

    /**
     * Looks up a session. Returns empty if token doesn't exist or is expired.
     */
    public Optional<SessionData> getSession(String token) {
        if (token == null) return Optional.empty();
        SessionData data = sessions.get(token);
        if (data == null) return Optional.empty();
        if (LocalDateTime.now().isAfter(data.expiresAt())) {
            sessions.remove(token);
            return Optional.empty();
        }
        return Optional.of(data);
    }

    /**
     * Invalidates (logs out) a session.
     */
    public void invalidate(String token) {
        if (token != null) sessions.remove(token);
    }

    /**
     * Checks whether the session has ADMIN role.
     */
    public boolean isAdmin(String token) {
        return getSession(token)
                .map(s -> s.role() == User.Role.ADMIN)
                .orElse(false);
    }

    // ── Data record ───────────────────────────────────────────────────────────

    public record SessionData(
            Long userId,
            String email,
            String displayName,
            User.Role role,
            LocalDateTime expiresAt
    ) {}
}
