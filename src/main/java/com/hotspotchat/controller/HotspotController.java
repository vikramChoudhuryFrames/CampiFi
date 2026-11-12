package com.hotspotchat.controller;

import com.hotspotchat.model.JoinRequest;
import com.hotspotchat.service.HotspotService;
import com.hotspotchat.service.NetworkUtils;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/hotspot")
public class HotspotController {

    private final HotspotService hotspotService;
    private final NetworkUtils networkUtils;

    public HotspotController(HotspotService hotspotService, NetworkUtils networkUtils) {
        this.hotspotService = hotspotService;
        this.networkUtils = networkUtils;
    }

    @PostMapping("/create")
    public ResponseEntity<Map<String, String>> createRoom(
            @RequestBody JoinRequest request,
            HttpServletRequest httpRequest) {

        String clientIp = networkUtils.getClientIp(httpRequest);
        String networkMode = (request.getNetworkMode() != null && !request.getNetworkMode().isBlank())
                ? request.getNetworkMode().toLowerCase()
                : "campus";

        Map<String, String> response = new HashMap<>();

        String result = hotspotService.createRoom(
                request.getHotspotName(),
                clientIp,
                request.getDisplayName(),
                networkMode);

        if ("ROOM_EXISTS".equals(result)) {
            response.put("status", "error");
            response.put("message", "A network with this name already exists. Try connecting instead.");
            return ResponseEntity.badRequest().body(response);
        }

        response.put("status", "ok");
        response.put("message", "Network started. Others on your network can now connect.");
        response.put("room", request.getHotspotName().toLowerCase());
        return ResponseEntity.ok(response);
    }

    @PostMapping("/join")
    public ResponseEntity<Map<String, String>> joinRoom(
            @RequestBody JoinRequest request,
            HttpServletRequest httpRequest) {

        String clientIp = networkUtils.getClientIp(httpRequest);

        Map<String, String> response = new HashMap<>();

        String result = hotspotService.joinRoom(
                request.getHotspotName(),
                clientIp,
                request.getDisplayName());

        switch (result) {
            case "ROOM_NOT_FOUND":
                response.put("status", "error");
                response.put("message", "No network found with that name. Check the name or start a new one.");
                return ResponseEntity.badRequest().body(response);
            case "DIFFERENT_NETWORK":
                Map<String, Object> roomInfo = hotspotService.getRoomInfo(request.getHotspotName());
                String roomSubnet = roomInfo != null ? String.valueOf(roomInfo.get("subnet")) : "unknown";
                String roomMode = roomInfo != null ? String.valueOf(roomInfo.get("networkMode")) : "campus";
                response.put("status", "error");
                response.put("message", "You are not on the same network as this room.\n" +
                        "Your IP: " + clientIp + "\n" +
                        "Mode: " + roomMode + "  Expected subnet: " + roomSubnet + ".*\n" +
                        "Your subnet: " + networkUtils.extractNetworkIdentifier(clientIp, roomMode) + ".*");
                return ResponseEntity.status(403).body(response);
            default:
                response.put("status", "ok");
                response.put("message", "Connected successfully.");
                response.put("room", request.getHotspotName().toLowerCase());
                return ResponseEntity.ok(response);
        }
    }

    @GetMapping("/members/{room}")
    public ResponseEntity<Map<String, Object>> getMembers(@PathVariable String room) {
        Map<String, Object> info = hotspotService.getRoomInfo(room);
        if (info == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(info);
    }

    @GetMapping("/myip")
    public ResponseEntity<Map<String, String>> getMyIp(HttpServletRequest httpRequest) {
        String clientIp = networkUtils.getClientIp(httpRequest);
        Map<String, String> response = new HashMap<>();
        response.put("ip", clientIp);
        response.put("subnet", networkUtils.extractSubnet(clientIp));
        return ResponseEntity.ok(response);
    }
}
