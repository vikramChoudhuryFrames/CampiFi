package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * Sub-channel nested inside a PRIVATE Channel.
 * e.g., "CSE Core A" → sub-channels: "Prof. Sharma", "Prof. Gupta"
 * Users chat inside sub-channels, not the parent channel directly.
 */
@Entity
@Table(name = "sub_channels")
public class SubChannel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(length = 500)
    private String description;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "channel_id", nullable = false)
    private Channel channel;

    @Column(nullable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @OneToMany(mappedBy = "subChannel", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Message> messages = new ArrayList<>();

    public SubChannel() {}

    public SubChannel(String name, String description, Channel channel) {
        this.name = name;
        this.description = description;
        this.channel = channel;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Channel getChannel() { return channel; }
    public void setChannel(Channel channel) { this.channel = channel; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public List<Message> getMessages() { return messages; }
}
