package com.hotspotchat.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.net.URLConnection;
import java.nio.file.*;
import java.time.LocalDate;
import java.util.Locale;
import java.util.Map;
import java.util.Set;
import java.util.UUID;

/**
 * Handles file and photo uploads for the CampiFi chat.
 *
 * POST /api/upload
 *   - Accepts multipart "file"
 *   - Saves to <campifi.upload.dir>/<YYYY-MM>/<uuid>_<originalName>
 *   - Returns { status: "ok", url: "/files/...", name: "...", type: "image"|"file", size: ... }
 *
 * GET /files/{folder}/{filename:.+}
 *   - Serves uploaded pictures and documents inline
 */
@RestController
public class FileUploadController {

    @Value("${campifi.upload.dir:uploads}")
    private String uploadDir;

    private static final long MAX_BYTES = 50L * 1024 * 1024; // 50 MB

    private static final Set<String> IMAGE_EXTENSIONS = Set.of(
            "png", "jpg", "jpeg", "gif", "webp", "bmp", "svg"
    );

    @PostMapping("/api/upload")
    public ResponseEntity<?> upload(@RequestParam("file") MultipartFile file) {
        if (file == null || file.isEmpty()) {
            return ResponseEntity.badRequest().body(
                    Map.of("status", "error", "message", "No file received. Please select a file."));
        }
        if (file.getSize() > MAX_BYTES) {
            return ResponseEntity.badRequest().body(
                    Map.of("status", "error", "message", "File is too large. Maximum size is 50 MB."));
        }

        String originalName = sanitize(file.getOriginalFilename());
        String ext = getExtension(originalName);

        String mime = file.getContentType();
        if (mime == null || mime.isBlank() || mime.equals("application/octet-stream")) {
            mime = URLConnection.guessContentTypeFromName(originalName);
            if (mime == null) mime = "application/octet-stream";
        }

        boolean isImage = (mime != null && mime.toLowerCase(Locale.ROOT).startsWith("image/"))
                || IMAGE_EXTENSIONS.contains(ext);

        String attachType = isImage ? "image" : "file";

        try {
            String monthFolder = LocalDate.now().toString().substring(0, 7); // e.g. "2026-11"
            Path dir = Paths.get(uploadDir, monthFolder).toAbsolutePath().normalize();
            Files.createDirectories(dir);

            String uniquePrefix = UUID.randomUUID().toString().replace("-", "").substring(0, 10);
            String storedFileName = uniquePrefix + "_" + originalName;
            Path dest = dir.resolve(storedFileName);

            file.transferTo(dest.toFile());

            String fileUrl = "/files/" + monthFolder + "/" + storedFileName;
            System.out.println("[CampiFi] File uploaded: " + originalName + " -> " + fileUrl + " (" + attachType + ", " + file.getSize() + " bytes)");

            return ResponseEntity.ok(Map.of(
                    "status", "ok",
                    "url", fileUrl,
                    "name", originalName,
                    "type", attachType,
                    "size", file.getSize(),
                    "mime", mime
            ));
        } catch (IOException e) {
            System.err.println("[CampiFi] Upload error: " + e.getMessage());
            return ResponseEntity.internalServerError().body(
                    Map.of("status", "error", "message", "Server error saving file: " + e.getMessage()));
        }
    }

    /**
     * Directly streams uploaded pictures and documents to browsers.
     */
    @GetMapping("/files/{folder}/{filename:.+}")
    public ResponseEntity<Resource> serveFile(@PathVariable String folder, @PathVariable String filename) {
        try {
            Path filePath = Paths.get(uploadDir, folder, filename).toAbsolutePath().normalize();
            if (!Files.exists(filePath)) {
                return ResponseEntity.notFound().build();
            }

            Resource resource = new UrlResource(filePath.toUri());
            if (!resource.exists() || !resource.isReadable()) {
                return ResponseEntity.notFound().build();
            }

            String contentType = Files.probeContentType(filePath);
            if (contentType == null) {
                contentType = URLConnection.guessContentTypeFromName(filename);
            }
            if (contentType == null) {
                contentType = "application/octet-stream";
            }

            return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(contentType))
                    .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + filename + "\"")
                    .body(resource);
        } catch (Exception e) {
            return ResponseEntity.internalServerError().build();
        }
    }

    private static String getExtension(String filename) {
        if (filename == null) return "";
        int dot = filename.lastIndexOf('.');
        if (dot < 0 || dot >= filename.length() - 1) return "";
        return filename.substring(dot + 1).toLowerCase(Locale.ROOT);
    }

    private static String sanitize(String name) {
        if (name == null || name.isBlank()) return "attachment";
        String base = Paths.get(name).getFileName().toString();
        base = base.replaceAll("[^a-zA-Z0-9.\\-_]", "_");
        return base.length() > 100 ? base.substring(0, 100) : base;
    }
}
