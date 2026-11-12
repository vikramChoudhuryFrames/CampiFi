package com.hotspotchat.model;

public class JoinRequest {
    private String hotspotName;
    private String displayName;
    private String networkMode; // "hotspot" (default) or "campus"

    public JoinRequest() {}

    public JoinRequest(String hotspotName, String displayName) {
        this.hotspotName = hotspotName;
        this.displayName = displayName;
        this.networkMode = "hotspot";
    }

    public JoinRequest(String hotspotName, String displayName, String networkMode) {
        this.hotspotName = hotspotName;
        this.displayName = displayName;
        this.networkMode = networkMode != null ? networkMode : "hotspot";
    }

    public String getHotspotName() { return hotspotName; }
    public void setHotspotName(String hotspotName) { this.hotspotName = hotspotName; }

    public String getDisplayName() { return displayName; }
    public void setDisplayName(String displayName) { this.displayName = displayName; }

    public String getNetworkMode() { return networkMode; }
    public void setNetworkMode(String networkMode) { this.networkMode = networkMode; }
}
