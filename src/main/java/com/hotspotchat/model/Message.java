package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * A chat message sent in a sub-channel (private) or directly in a
 * public channel (read-only posts).
 *
 * TEXT   → plain text
 * IMAGE  → image upload
 * FILE   → document / file upload
 */
@Entity
@Table(name = "messages")
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "TEXT")
    private String content;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sender_id", nullable = false)
    private User sender;

    /** Set when the message belongs to a public channel directly */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "channel_id")
    private Channel channel;

    /** Set when the message belongs to a sub-channel of a private channel */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "sub_channel_id")
    private SubChannel subChannel;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private MessageType type = MessageType.TEXT;

    @Column(nullable = false)
    private LocalDateTime sentAt = LocalDateTime.now();

    @OneToMany(mappedBy = "message", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Attachment> attachments = new ArrayList<>();

    public enum MessageType { TEXT, IMAGE, FILE }

    public Message() {}

    // Getters & Setters
    public Long getId() { return id; }
    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }
    public User getSender() { return sender; }
    public void setSender(User sender) { this.sender = sender; }
    public Channel getChannel() { return channel; }
    public void setChannel(Channel channel) { this.channel = channel; }
    public SubChannel getSubChannel() { return subChannel; }
    public void setSubChannel(SubChannel subChannel) { this.subChannel = subChannel; }
    public MessageType getType() { return type; }
    public void setType(MessageType type) { this.type = type; }
    public LocalDateTime getSentAt() { return sentAt; }
    public List<Attachment> getAttachments() { return attachments; }
}
