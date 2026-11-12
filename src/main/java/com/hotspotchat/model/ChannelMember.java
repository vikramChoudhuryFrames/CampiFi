package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Tracks a user's membership in a channel.
 * isAdmin → channel-level admin (set via OTP flow)
 * isBanned → user is blocked from this channel
 */
@Entity
@Table(name = "channel_members",
       uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "channel_id"}))
public class ChannelMember {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "channel_id", nullable = false)
    private Channel channel;

    @Column(nullable = false)
    private boolean isAdmin = false;

    @Column(nullable = false)
    private boolean isBanned = false;

    @Column(nullable = false)
    private LocalDateTime joinedAt = LocalDateTime.now();

    public ChannelMember() {}

    public ChannelMember(User user, Channel channel, boolean isAdmin) {
        this.user = user;
        this.channel = channel;
        this.isAdmin = isAdmin;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public Channel getChannel() { return channel; }
    public void setChannel(Channel channel) { this.channel = channel; }
    public boolean isAdmin() { return isAdmin; }
    public void setAdmin(boolean admin) { isAdmin = admin; }
    public boolean isBanned() { return isBanned; }
    public void setBanned(boolean banned) { isBanned = banned; }
    public LocalDateTime getJoinedAt() { return joinedAt; }
}
