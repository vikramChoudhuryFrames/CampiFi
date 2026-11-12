package com.hotspotchat.service;

import com.hotspotchat.model.HotspotRoom;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class HotspotService {

    private final ConcurrentHashMap<String, HotspotRoom> rooms = new ConcurrentHashMap<>();
    private final NetworkUtils networkUtils;

    public HotspotService(NetworkUtils networkUtils) {
        this.networkUtils = networkUtils;
    }

    /**
     * Creates a new room. Network subnet is the sole membership key — no password.
     */
    public synchronized String createRoom(String name, String creatorIp, String displayName, String networkMode) {
        if (rooms.containsKey(name.toLowerCase())) {
            return "ROOM_EXISTS";
        }
        String mode = (networkMode != null && !networkMode.isBlank()) ? networkMode.toLowerCase() : "hotspot";
        String subnet = networkUtils.extractNetworkIdentifier(creatorIp, mode);
        HotspotRoom room = new HotspotRoom(name.toLowerCase(), subnet, mode, creatorIp);
        room.addMember(displayName);
        rooms.put(name.toLowerCase(), room);
        return "OK";
    }

    /**
     * Joins an existing room. Validates only that the joiner is on the same network subnet.
     */
    public String joinRoom(String name, String joinerIp, String displayName) {
        HotspotRoom room = rooms.get(name.toLowerCase());
        if (room == null) {
            return "ROOM_NOT_FOUND";
        }
        // Check network — compare joiner's subnet to the room's stored subnet
        String mode = room.getNetworkMode() != null ? room.getNetworkMode() : "hotspot";
        String joinerSubnet = networkUtils.extractNetworkIdentifier(joinerIp, mode);
        if (!room.getSubnet().equals(joinerSubnet)) {
            return "DIFFERENT_NETWORK";
        }
        room.addMember(displayName);
        return "OK";
    }

    public Set<String> getMembers(String roomName) {
        HotspotRoom room = rooms.get(roomName.toLowerCase());
        if (room == null) return Collections.emptySet();
        return room.getMembers();
    }

    public void removeMember(String roomName, String displayName) {
        HotspotRoom room = rooms.get(roomName.toLowerCase());
        if (room != null) {
            room.removeMember(displayName);
        }
    }

    public boolean roomExists(String name) {
        return rooms.containsKey(name.toLowerCase());
    }

    public Map<String, Object> getRoomInfo(String name) {
        HotspotRoom room = rooms.get(name.toLowerCase());
        if (room == null) return null;
        Map<String, Object> info = new HashMap<>();
        info.put("name", room.getName());
        info.put("subnet", room.getSubnet());
        info.put("networkMode", room.getNetworkMode());
        info.put("memberCount", room.getMembers().size());
        info.put("members", new ArrayList<>(room.getMembers()));
        return info;
    }
}
