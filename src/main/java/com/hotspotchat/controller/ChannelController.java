package com.hotspotchat.controller;

import com.hotspotchat.model.User;
import com.hotspotchat.service.ChannelService;
import com.hotspotchat.service.ChannelService.*;
import com.hotspotchat.service.SessionService;
import com.hotspotchat.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * REST API for channel operations available to any logged-in user.
 *
 * All endpoints require a valid X-Session-Token header (issued at login or OTP verify).
 *
 * Endpoints:
 *   GET  /api/channels                       → list all channels
 *   POST /api/channels/{id}/verify-pin       → check 4-digit PIN (before joining)
 *   POST /api/channels/{id}/join             → join a channel
 *   POST /api/channels/{id}/leave            → leave a channel
 *   GET  /api/channels/{id}/sub-channels     → list sub-channels (membership required for private)
 *   GET  /api/channels/{id}/members          → list members
 *   POST /api/channels/{id}/members/{uid}/ban  → ban user (ADMIN session required)
 *   POST /api/channels/{id}/members/{uid}/kick → kick user (ADMIN session required)
 */
@RestController
@RequestMapping("/api/channels")
public class ChannelController {

    private final ChannelService channelService;
    private final SessionService sessionService;
    private final UserService    userService;

    @Autowired
    public ChannelController(ChannelService channelService,
                             SessionService sessionService,
                             UserService userService) {
        this.channelService = channelService;
        this.sessionService = sessionService;
        this.userService    = userService;
    }

    // ── List all channels ────────────────────────────────────────────────────

    /** Returns the full channel directory. Requires any valid session. */
    @GetMapping
    public ResponseEntity<?> listChannels(HttpServletRequest request) {
        if (requireSession(request).isEmpty()) return unauthorized();

        List<ChannelSummary> channels = channelService.listChannels();
        return ResponseEntity.ok(Map.of("status", "ok", "channels", channels));
    }

    // ── PIN verification ─────────────────────────────────────────────────────

    /**
     * Verifies a 4-digit PIN for a PRIVATE channel.
     * The UI calls this before displaying sub-channels.
     * Body: { "pin": "1234" }
     */
    @PostMapping("/{id}/verify-pin")
    public ResponseEntity<Map<String, Object>> verifyPin(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            HttpServletRequest request) {

        if (requireSession(request).isEmpty()) return unauthorizedObj();

        String pin = body.getOrDefault("pin", "").trim();
        boolean ok = channelService.verifyPin(id, pin);

        Map<String, Object> resp = new HashMap<>();
        resp.put("status", ok ? "ok" : "error");
        resp.put("correct", ok);
        if (!ok) resp.put("message", "Incorrect PIN. Please try again.");
        return ok ? ResponseEntity.ok(resp) : ResponseEntity.status(401).body(resp);
    }

    // ── Join channel ─────────────────────────────────────────────────────────

    /**
     * Joins a channel. For PRIVATE channels, the PIN must be provided.
     * Body: { "pin": "1234" }  (optional for PUBLIC)
     */
    @PostMapping("/{id}/join")
    public ResponseEntity<Map<String, Object>> joinChannel(
            @PathVariable Long id,
            @RequestBody(required = false) Map<String, String> body,
            HttpServletRequest request) {

        Optional<SessionService.SessionData> session = requireSession(request);
        if (session.isEmpty()) return unauthorizedObj();

        User user = getUser(session.get());
        if (user == null) return unauthorizedObj();

        String pin = body != null ? body.getOrDefault("pin", "").trim() : "";

        Map<String, Object> resp = new HashMap<>();
        try {
            boolean joined = channelService.joinChannel(id, user, pin);
            if (joined) {
                resp.put("status", "ok");
                resp.put("message", "Joined channel successfully.");
                // Return sub-channels right away so the UI can show them
                resp.put("subChannels", channelService.getSubChannels(id));
            } else {
                resp.put("status", "error");
                resp.put("message", "Incorrect PIN.");
                return ResponseEntity.status(401).body(resp);
            }
        } catch (IllegalStateException e) {
            resp.put("status", "error");
            resp.put("message", e.getMessage());
            return ResponseEntity.status(403).body(resp);
        }
        return ResponseEntity.ok(resp);
    }

    // ── Leave channel ─────────────────────────────────────────────────────────

    /** Removes the user's membership from the channel. */
    @PostMapping("/{id}/leave")
    public ResponseEntity<Map<String, String>> leaveChannel(
            @PathVariable Long id,
            HttpServletRequest request) {

        Optional<SessionService.SessionData> session = requireSession(request);
        if (session.isEmpty()) return unauthorized();

        User user = getUser(session.get());
        if (user == null) return unauthorized();

        channelService.leaveChannel(id, user);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "Left channel."));
    }

    // ── Sub-channels ──────────────────────────────────────────────────────────

    /**
     * Returns sub-channels of a channel.
     * For PRIVATE channels, the user must already be a member.
     */
    @GetMapping("/{id}/sub-channels")
    public ResponseEntity<?> getSubChannels(
            @PathVariable Long id,
            HttpServletRequest request) {

        Optional<SessionService.SessionData> session = requireSession(request);
        if (session.isEmpty()) return unauthorized();

        User user = getUser(session.get());

        // For private channels, verify membership
        Optional<com.hotspotchat.model.Channel> chOpt = channelService.findById(id);
        if (chOpt.isPresent()) {
            com.hotspotchat.model.Channel ch = chOpt.get();
            if (ch.getType() == com.hotspotchat.model.Channel.ChannelType.PRIVATE
                    && user != null && !channelService.isMember(id, user)) {
                return ResponseEntity.status(403).body(
                        Map.of("status", "error", "message", "Join the channel first."));
            }
        }

        List<SubChannelSummary> subs = channelService.getSubChannels(id);
        return ResponseEntity.ok(Map.of("status", "ok", "subChannels", subs));
    }

    // ── Members ───────────────────────────────────────────────────────────────

    /** Returns the full member list. Used by the channel info panel. */
    @GetMapping("/{id}/members")
    public ResponseEntity<?> getMembers(
            @PathVariable Long id,
            HttpServletRequest request) {

        if (requireSession(request).isEmpty()) return unauthorized();

        List<MemberSummary> members = channelService.getMembers(id);
        return ResponseEntity.ok(Map.of("status", "ok", "members", members));
    }

    // ── Ban ───────────────────────────────────────────────────────────────────

    /**
     * Permanently bans a user from a channel.
     * Requires an ADMIN-role session (professor / channel manager).
     */
    @PostMapping("/{channelId}/members/{userId}/ban")
    public ResponseEntity<Map<String, String>> banUser(
            @PathVariable Long channelId,
            @PathVariable Long userId,
            HttpServletRequest request) {

        Optional<SessionService.SessionData> session = requireSession(request);
        if (session.isEmpty()) return unauthorized();
        if (session.get().role() != com.hotspotchat.model.User.Role.ADMIN) {
            return ResponseEntity.status(403).body(
                    Map.of("status", "error", "message", "Admin access required."));
        }

        channelService.banUser(channelId, userId);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "User banned from channel."));
    }

    // ── Kick ──────────────────────────────────────────────────────────────────

    /**
     * Removes a user from a channel (can re-join later).
     * Requires an ADMIN-role session.
     */
    @PostMapping("/{channelId}/members/{userId}/kick")
    public ResponseEntity<Map<String, String>> kickUser(
            @PathVariable Long channelId,
            @PathVariable Long userId,
            HttpServletRequest request) {

        Optional<SessionService.SessionData> session = requireSession(request);
        if (session.isEmpty()) return unauthorized();
        if (session.get().role() != com.hotspotchat.model.User.Role.ADMIN) {
            return ResponseEntity.status(403).body(
                    Map.of("status", "error", "message", "Admin access required."));
        }

        channelService.kickUser(channelId, userId);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "User removed from channel."));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    private Optional<SessionService.SessionData> requireSession(HttpServletRequest request) {
        return sessionService.getSession(request.getHeader("X-Session-Token"));
    }

    private User getUser(SessionService.SessionData session) {
        return userService.findByEmail(session.email()).orElse(null);
    }

    @SuppressWarnings("unchecked")
    private <T> ResponseEntity<T> unauthorized() {
        return (ResponseEntity<T>) ResponseEntity.status(401)
                .body(Map.of("status", "error", "message", "Session required. Please log in."));
    }

    @SuppressWarnings("unchecked")
    private <T> ResponseEntity<T> unauthorizedObj() {
        return (ResponseEntity<T>) ResponseEntity.status(401)
                .body(Map.of("status", "error", "message", "Session required. Please log in."));
    }
}
