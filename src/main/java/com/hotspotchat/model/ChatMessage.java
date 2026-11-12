package com.hotspotchat.model;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ChatMessage {

    public enum MessageType {
        CHAT, JOIN, LEAVE, FILE
    }

    private MessageType type;
    private String sender;
    private String content;
    private String timestamp;
    private String room;

    // ── Attachment fields (populated for FILE messages) ──────────────────────
    private String attachmentUrl;    // e.g. /files/2024/abc123_photo.png
    private String attachmentName;   // original file name shown to users
    private String attachmentType;   // "image" or "file"
    private Long   attachmentSize;   // bytes, for display

    public ChatMessage() {}

    public ChatMessage(MessageType type, String sender, String content, String room) {
        this.type = type;
        this.sender = sender;
        this.content = content;
        this.room = room;
        this.timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("HH:mm"));
    }

    public MessageType getType() { return type; }
    public void setType(MessageType type) { this.type = type; }

    public String getSender() { return sender; }
    public void setSender(String sender) { this.sender = sender; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getTimestamp() { return timestamp; }
    public void setTimestamp(String timestamp) { this.timestamp = timestamp; }

    public String getRoom() { return room; }
    public void setRoom(String room) { this.room = room; }

    public String getAttachmentUrl()  { return attachmentUrl; }
    public void setAttachmentUrl(String attachmentUrl)   { this.attachmentUrl = attachmentUrl; }

    public String getAttachmentName() { return attachmentName; }
    public void setAttachmentName(String attachmentName) { this.attachmentName = attachmentName; }

    public String getAttachmentType() { return attachmentType; }
    public void setAttachmentType(String attachmentType) { this.attachmentType = attachmentType; }

    public Long getAttachmentSize()   { return attachmentSize; }
    public void setAttachmentSize(Long attachmentSize)   { this.attachmentSize = attachmentSize; }
}

