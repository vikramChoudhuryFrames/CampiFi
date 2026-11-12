package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Tracks an administrator assigned specifically to a sub-channel.
 * Created by the server host from the "Manage Networks" dashboard.
 */
@Entity
@Table(name = "sub_channel_admins",
       uniqueConstraints = @UniqueConstraint(columnNames = {"user_id", "sub_channel_id"}))
public class SubChannelAdmin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sub_channel_id", nullable = false)
    private SubChannel subChannel;

    @Column(nullable = false)
    private LocalDateTime assignedAt = LocalDateTime.now();

    public SubChannelAdmin() {}

    public SubChannelAdmin(User user, SubChannel subChannel) {
        this.user = user;
        this.subChannel = subChannel;
    }

    public Long getId() { return id; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    public SubChannel getSubChannel() { return subChannel; }
    public void setSubChannel(SubChannel subChannel) { this.subChannel = subChannel; }
    public LocalDateTime getAssignedAt() { return assignedAt; }
}
