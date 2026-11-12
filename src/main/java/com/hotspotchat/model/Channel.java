package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Represents a top-level channel created by the server admin.
 *
 * PUBLIC  → anyone on the network can see posts (read-only for regular users)
 * PRIVATE → requires a 4-digit PIN to join; has sub-channels inside
 */
@Entity
@Table(name = "channels")
public class Channel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true, length = 100)
    private String name;

    @Column(length = 500)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private ChannelType type = ChannelType.PUBLIC;

    /** SHA-256 hash of the 4-digit PIN; null for public channels */
    @Column(length = 64)
    private String pinHash;

    /** Which network subnet created this channel */
    @Column(length = 50)
    private String subnet;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @OneToMany(mappedBy = "channel", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<SubChannel> subChannels = new ArrayList<>();

    @OneToMany(mappedBy = "channel", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ChannelMember> members = new ArrayList<>();

    public enum ChannelType { PUBLIC, PRIVATE }

    public Channel() {}

    // Getters & Setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public ChannelType getType() { return type; }
    public void setType(ChannelType type) { this.type = type; }
    public String getPinHash() { return pinHash; }
    public void setPinHash(String pinHash) { this.pinHash = pinHash; }
    public String getSubnet() { return subnet; }
    public void setSubnet(String subnet) { this.subnet = subnet; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public List<SubChannel> getSubChannels() { return subChannels; }
    public List<ChannelMember> getMembers() { return members; }
}
