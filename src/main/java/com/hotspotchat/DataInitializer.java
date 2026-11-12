package com.hotspotchat;

import com.hotspotchat.model.Channel;
import com.hotspotchat.repository.ChannelRepository;
import com.hotspotchat.service.ChannelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

/**
 * Seeds sample Networks (channels) into the database on first startup.
 * Runs only when the channels table is empty — safe to restart server without re-seeding.
 *
 * Sample data created:
 *   PUBLIC  — "University Announcements"   (broadcast, read-only for students)
 *   PUBLIC  — "Campus Events & Sports"     (broadcast, read-only)
 *   PRIVATE — "CSE Core A"        PIN: 1234
 *               └ Sub-network: Prof. Sharma — Data Structures
 *               └ Sub-network: Prof. Gupta — Operating Systems
 *               └ Sub-network: Prof. Mehta — DBMS
 *   PRIVATE — "ECE Batch 2021"    PIN: 5678
 *               └ Sub-network: Prof. Nair — Signals & Systems
 *               └ Sub-network: Prof. Rao  — Digital Electronics
 */
@Component
@Order(1)
public class DataInitializer implements CommandLineRunner {

    private final ChannelRepository channelRepository;
    private final ChannelService    channelService;

    @Autowired
    public DataInitializer(ChannelRepository channelRepository, ChannelService channelService) {
        this.channelRepository = channelRepository;
        this.channelService    = channelService;
    }

    @Override
    public void run(String... args) {
        // Skip if networks already exist (prevents re-seeding on restart)
        if (channelRepository.count() > 0) {
            System.out.println("[CampiFi] Networks already exist — skipping seed.");
            return;
        }

        System.out.println("[CampiFi] Seeding sample Networks...");

        // ── Public Channels ──────────────────────────────────────────────────
        channelService.createChannel(
                "University Announcements",
                "Official notices from administration, exam schedules, and circulars.",
                Channel.ChannelType.PUBLIC,
                null
        );

        channelService.createChannel(
                "Campus Events & Sports",
                "Event schedules, sports results, club notices, and fest updates.",
                Channel.ChannelType.PUBLIC,
                null
        );

        // ── CSE Core A (Private) ─────────────────────────────────────────────
        Channel cseA = channelService.createChannel(
                "CSE Core A",
                "Core subjects for the CSE Batch 2021. PIN: 1234",
                Channel.ChannelType.PRIVATE,
                "1234"
        );
        channelService.createSubChannel(cseA.getId(),
                "Prof. Sharma — Data Structures",
                "Arrays, Trees, Graphs and Algorithm Design");
        channelService.createSubChannel(cseA.getId(),
                "Prof. Gupta — Operating Systems",
                "Process management, memory, file systems");
        channelService.createSubChannel(cseA.getId(),
                "Prof. Mehta — DBMS",
                "Relational models, SQL, normalization and transactions");

        // ── ECE Batch 2021 (Private) ──────────────────────────────────────────
        Channel ece = channelService.createChannel(
                "ECE Batch 2021",
                "Electronics & Communication core subjects. PIN: 5678",
                Channel.ChannelType.PRIVATE,
                "5678"
        );
        channelService.createSubChannel(ece.getId(),
                "Prof. Nair — Signals & Systems",
                "Fourier analysis, Laplace transform, signal processing");
        channelService.createSubChannel(ece.getId(),
                "Prof. Rao — Digital Electronics",
                "Logic gates, flip-flops, counters and digital circuits");

        System.out.println("[CampiFi] Sample Networks seeded successfully!");
        System.out.println("[CampiFi]   CSE Core A   PIN: 1234");
        System.out.println("[CampiFi]   ECE Batch    PIN: 5678");
    }
}
