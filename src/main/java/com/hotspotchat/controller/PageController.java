package com.hotspotchat.controller;

import com.hotspotchat.service.NetworkUtils;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

/**
 * Handles page-level routing.
 *
 * GET /       → host machine  : redirect to /admin
 *             → other devices : forward to index.html (join-only page)
 *
 * GET /admin  → host machine  : forward to admin.html (start + join)
 *             → other devices : redirect to / (access denied silently)
 */
@Controller
public class PageController {

    private final NetworkUtils networkUtils;

    public PageController(NetworkUtils networkUtils) {
        this.networkUtils = networkUtils;
    }

    @GetMapping("/")
    public String root(HttpServletRequest request) {
        if (networkUtils.isHostDevice(request)) {
            return "redirect:/admin";
        }
        return "forward:/index.html";
    }

    @GetMapping("/admin")
    public String admin(HttpServletRequest request) {
        if (!networkUtils.isHostDevice(request)) {
            // Silently redirect non-host devices back to the join page
            return "redirect:/";
        }
        return "forward:/admin.html";
    }
}
