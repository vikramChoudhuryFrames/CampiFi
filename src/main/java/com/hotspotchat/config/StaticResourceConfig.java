package com.hotspotchat.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import java.nio.file.Paths;

/**
 * Maps the on-disk uploads directory to the /files/** URL path so that
 * uploaded images and documents can be served directly by Spring Boot.
 *
 * Example:
 *   File on disk: uploads/2024-11/abc123_photo.png
 *   Served at:    http://<host>/files/2024-11/abc123_photo.png
 */
@Configuration
public class StaticResourceConfig implements WebMvcConfigurer {

    @Value("${campifi.upload.dir:uploads}")
    private String uploadDir;

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        // Resolve to an absolute path so Spring can serve files outside of the jar
        String absolutePath = Paths.get(uploadDir).toAbsolutePath().toString();

        registry.addResourceHandler("/files/**")
                .addResourceLocations("file:" + absolutePath + "/");
    }
}
