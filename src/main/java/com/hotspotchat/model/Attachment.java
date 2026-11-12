package com.hotspotchat.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

/**
 * Stores metadata for a file/image attached to a message.
 * Actual file bytes are stored on disk under campifi.upload.dir.
 */
@Entity
@Table(name = "attachments")
public class Attachment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "message_id", nullable = false)
    private Message message;

    /** Original file name as uploaded by the client */
    @Column(nullable = false, length = 255)
    private String originalName;

    /** Path on disk relative to campifi.upload.dir */
    @Column(nullable = false, length = 500)
    private String storedPath;

    /** MIME type, e.g. image/png, application/pdf */
    @Column(nullable = false, length = 100)
    private String mimeType;

    /** File size in bytes */
    private Long fileSize;

    @Column(nullable = false)
    private LocalDateTime uploadedAt = LocalDateTime.now();

    public Attachment() {}

    public Attachment(Message message, String originalName, String storedPath,
                      String mimeType, Long fileSize) {
        this.message = message;
        this.originalName = originalName;
        this.storedPath = storedPath;
        this.mimeType = mimeType;
        this.fileSize = fileSize;
    }

    // Getters & Setters
    public Long getId() { return id; }
    public Message getMessage() { return message; }
    public void setMessage(Message message) { this.message = message; }
    public String getOriginalName() { return originalName; }
    public void setOriginalName(String originalName) { this.originalName = originalName; }
    public String getStoredPath() { return storedPath; }
    public void setStoredPath(String storedPath) { this.storedPath = storedPath; }
    public String getMimeType() { return mimeType; }
    public void setMimeType(String mimeType) { this.mimeType = mimeType; }
    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long fileSize) { this.fileSize = fileSize; }
    public LocalDateTime getUploadedAt() { return uploadedAt; }
}
