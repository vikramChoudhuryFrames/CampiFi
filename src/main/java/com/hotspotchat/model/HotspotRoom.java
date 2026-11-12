package com.hotspotchat.model;

import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class HotspotRoom {
    private String name;
    private String subnet;
    private String networkMode; // "hotspot" (default) or "campus" or "public"
    private String creatorIp;
    private Set<String> members = ConcurrentHashMap.newKeySet();

    public HotspotRoom() {}

    public HotspotRoom(String name, String subnet, String networkMode, String creatorIp) {
        this.name = name;
        this.subnet = subnet;
        this.networkMode = networkMode != null ? networkMode : "hotspot";
        this.creatorIp = creatorIp;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getSubnet() { return subnet; }
    public void setSubnet(String subnet) { this.subnet = subnet; }

    public String getNetworkMode() { return networkMode; }
    public void setNetworkMode(String networkMode) { this.networkMode = networkMode; }

    public String getCreatorIp() { return creatorIp; }
    public void setCreatorIp(String creatorIp) { this.creatorIp = creatorIp; }

    public Set<String> getMembers() { return members; }
    public void setMembers(Set<String> members) { this.members = members; }

    public void addMember(String displayName) { this.members.add(displayName); }
    public void removeMember(String displayName) { this.members.remove(displayName); }
}
