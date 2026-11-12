package com.hotspotchat.controller;

import com.hotspotchat.model.Channel;
import com.hotspotchat.model.SubChannel;
import com.hotspotchat.service.ChannelService;
import com.hotspotchat.service.ChannelService.AdminSummary;
import com.hotspotchat.service.ChannelService.SubChannelSummary;
import com.hotspotchat.service.NetworkUtils;
import com.hotspotchat.service.UserService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Server-laptop-only REST API for channel administration.
 * Every endpoint is guarded by NetworkUtils.isHostDevice().
 */
@RestController
@RequestMapping("/api/admin")
public class AdminChannelController {

    private final ChannelService channelService;
    private final NetworkUtils   networkUtils;
    private final UserService    userService;

    @Autowired
    public AdminChannelController(ChannelService channelService,
                                  NetworkUtils networkUtils,
                                  UserService userService) {
        this.channelService = channelService;
        this.networkUtils   = networkUtils;
        this.userService    = userService;
    }

    // ── Create Channel ────────────────────────────────────────────────────────

    @PostMapping("/channels")
    public ResponseEntity<Map<String, Object>> createChannel(
            @RequestBody Map<String, String> body,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        String name        = body.get("name");
        String description = body.getOrDefault("description", "");
        String typeStr     = body.getOrDefault("type", "PUBLIC").toUpperCase();
        String pin         = body.getOrDefault("pin", "");

        if (name == null || name.isBlank()) {
            return badRequest("Channel name is required.");
        }

        Channel.ChannelType type;
        try {
            type = Channel.ChannelType.valueOf(typeStr);
        } catch (IllegalArgumentException e) {
            return badRequest("Type must be PUBLIC or PRIVATE.");
        }

        if (type == Channel.ChannelType.PRIVATE && (pin.isBlank() || !pin.matches("\\d{4}"))) {
            return badRequest("A 4-digit numeric PIN is required for PRIVATE channels.");
        }

        try {
            Channel ch = channelService.createChannel(name, description, type, pin);
            Map<String, Object> resp = new HashMap<>();
            resp.put("status", "ok");
            resp.put("message", "Channel \"" + ch.getName() + "\" created.");
            resp.put("channelId", ch.getId());
            resp.put("channelName", ch.getName());
            resp.put("type", ch.getType().name());
            return ResponseEntity.ok(resp);
        } catch (IllegalArgumentException e) {
            return badRequest(e.getMessage());
        }
    }

    // ── Delete Channel ────────────────────────────────────────────────────────

    @DeleteMapping("/channels/{id}")
    public ResponseEntity<Map<String, Object>> deleteChannel(
            @PathVariable Long id,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        channelService.deleteChannel(id);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "Channel deleted."));
    }

    // ── Create Sub-Channel ────────────────────────────────────────────────────

    @PostMapping("/channels/{channelId}/sub-channels")
    public ResponseEntity<Map<String, Object>> createSubChannel(
            @PathVariable Long channelId,
            @RequestBody Map<String, String> body,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        String name        = body.get("name");
        String description = body.getOrDefault("description", "");

        if (name == null || name.isBlank()) {
            return badRequest("Sub-channel name is required.");
        }

        try {
            SubChannel sub = channelService.createSubChannel(channelId, name, description);
            Map<String, Object> resp = new HashMap<>();
            resp.put("status", "ok");
            resp.put("message", "Sub-channel \"" + sub.getName() + "\" created.");
            resp.put("subChannelId", sub.getId());
            resp.put("subChannelName", sub.getName());
            resp.put("parentChannelId", channelId);
            return ResponseEntity.ok(resp);
        } catch (IllegalArgumentException e) {
            return badRequest(e.getMessage());
        }
    }

    // ── Delete Sub-Channel ────────────────────────────────────────────────────

    @DeleteMapping("/sub-channels/{id}")
    public ResponseEntity<Map<String, Object>> deleteSubChannel(
            @PathVariable Long id,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        channelService.deleteSubChannel(id);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "Sub-channel deleted."));
    }

    // ── List Sub-Channels for Admin ───────────────────────────────────────────

    @GetMapping("/channels/{id}/sub-channels")
    public ResponseEntity<?> getSubChannels(
            @PathVariable Long id,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        List<SubChannelSummary> subs = channelService.getSubChannels(id);
        return ResponseEntity.ok(Map.of("status", "ok", "subChannels", subs));
    }

    // ── Channel Master Admins ─────────────────────────────────────────────────

    @GetMapping("/channels/{id}/admins")
    public ResponseEntity<?> getChannelAdmins(
            @PathVariable Long id,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        List<AdminSummary> admins = channelService.getChannelAdmins(id);
        return ResponseEntity.ok(Map.of("status", "ok", "admins", admins));
    }

    @PostMapping("/channels/{id}/admins")
    public ResponseEntity<?> addChannelAdmin(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        String email = body.get("email");
        if (email == null || !email.contains("@")) {
            return badRequest("Valid institution email required.");
        }

        try {
            AdminSummary admin = channelService.addChannelAdmin(id, email);
            return ResponseEntity.ok(Map.of(
                    "status", "ok",
                    "message", admin.displayName() + " added as Master Admin.",
                    "admin", admin));
        } catch (Exception e) {
            return badRequest(e.getMessage());
        }
    }

    @DeleteMapping("/channels/{channelId}/admins/{userId}")
    public ResponseEntity<?> removeChannelAdmin(
            @PathVariable Long channelId,
            @PathVariable Long userId,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        channelService.removeChannelAdmin(channelId, userId);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "Master Admin removed."));
    }

    // ── Sub-Channel Admins ────────────────────────────────────────────────────

    @GetMapping("/sub-channels/{id}/admins")
    public ResponseEntity<?> getSubChannelAdmins(
            @PathVariable Long id,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        List<AdminSummary> admins = channelService.getSubChannelAdmins(id);
        return ResponseEntity.ok(Map.of("status", "ok", "admins", admins));
    }

    @PostMapping("/sub-channels/{id}/admins")
    public ResponseEntity<?> addSubChannelAdmin(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        String email = body.get("email");
        if (email == null || !email.contains("@")) {
            return badRequest("Valid institution email required.");
        }

        try {
            AdminSummary admin = channelService.addSubChannelAdmin(id, email);
            return ResponseEntity.ok(Map.of(
                    "status", "ok",
                    "message", admin.displayName() + " added as Sub-Channel Admin.",
                    "admin", admin));
        } catch (Exception e) {
            return badRequest(e.getMessage());
        }
    }

    @DeleteMapping("/sub-channels/{subChannelId}/admins/{userId}")
    public ResponseEntity<?> removeSubChannelAdmin(
            @PathVariable Long subChannelId,
            @PathVariable Long userId,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        channelService.removeSubChannelAdmin(subChannelId, userId);
        return ResponseEntity.ok(Map.of("status", "ok", "message", "Sub-Channel Admin removed."));
    }

    // ── Promote / Demote Users ────────────────────────────────────────────────

    @PutMapping("/users/{email}/promote")
    public ResponseEntity<Map<String, Object>> promoteUser(
            @PathVariable String email,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        try {
            var user = userService.promoteToAdmin(email);
            return ResponseEntity.ok(Map.of(
                    "status", "ok",
                    "message", user.getDisplayName() + " is now an Admin.",
                    "email", user.getEmail(),
                    "role", user.getRole().name()));
        } catch (IllegalArgumentException e) {
            return badRequest(e.getMessage());
        }
    }

    @PutMapping("/users/{email}/demote")
    public ResponseEntity<Map<String, Object>> demoteUser(
            @PathVariable String email,
            HttpServletRequest request) {

        if (!networkUtils.isHostDevice(request)) return forbidden();

        try {
            var user = userService.demoteToUser(email);
            return ResponseEntity.ok(Map.of(
                    "status", "ok",
                    "message", user.getDisplayName() + " has been demoted to User.",
                    "email", user.getEmail(),
                    "role", user.getRole().name()));
        } catch (IllegalArgumentException e) {
            return badRequest(e.getMessage());
        }
    }

    // ── List all channels ─────────────────────────────────────────────────────

    @GetMapping("/channels")
    public ResponseEntity<?> listChannels(HttpServletRequest request) {
        if (!networkUtils.isHostDevice(request)) return forbidden();
        return ResponseEntity.ok(Map.of("status", "ok",
                "channels", channelService.listChannels()));
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    @SuppressWarnings("unchecked")
    private <T> ResponseEntity<T> forbidden() {
        return (ResponseEntity<T>) ResponseEntity.status(403).body(
                Map.of("status", "error",
                        "message", "This endpoint is only accessible from the server machine."));
    }

    @SuppressWarnings("unchecked")
    private <T> ResponseEntity<T> badRequest(String message) {
        return (ResponseEntity<T>) ResponseEntity.badRequest().body(
                Map.of("status", "error", "message", message));
    }
}
