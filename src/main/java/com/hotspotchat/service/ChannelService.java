package com.hotspotchat.service;

import com.hotspotchat.model.*;
import com.hotspotchat.repository.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Business logic for channels, sub-channels, memberships, master admins, and sub-channel admins.
 */
@Service
public class ChannelService {

    private final ChannelRepository         channelRepository;
    private final SubChannelRepository      subChannelRepository;
    private final ChannelMemberRepository   memberRepository;
    private final UserRepository            userRepository;
    private final SubChannelAdminRepository subChannelAdminRepository;
    private final UserService               userService;

    @Autowired
    public ChannelService(ChannelRepository channelRepository,
                          SubChannelRepository subChannelRepository,
                          ChannelMemberRepository memberRepository,
                          UserRepository userRepository,
                          SubChannelAdminRepository subChannelAdminRepository,
                          UserService userService) {
        this.channelRepository         = channelRepository;
        this.subChannelRepository      = subChannelRepository;
        this.memberRepository          = memberRepository;
        this.userRepository            = userRepository;
        this.subChannelAdminRepository = subChannelAdminRepository;
        this.userService               = userService;
    }

    // ── Create ────────────────────────────────────────────────────────────────

    @Transactional
    public Channel createChannel(String name, String description,
                                 Channel.ChannelType type, String pin) {
        if (channelRepository.existsByName(name.trim())) {
            throw new IllegalArgumentException("A channel named \"" + name + "\" already exists.");
        }
        Channel ch = new Channel();
        ch.setName(name.trim());
        ch.setDescription(description);
        ch.setType(type);
        if (type == Channel.ChannelType.PRIVATE && pin != null && !pin.isBlank()) {
            ch.setPinHash(hashPin(pin.trim()));
        }
        return channelRepository.save(ch);
    }

    /**
     * Creates a sub-channel inside a Channel (both public and private supported).
     */
    @Transactional
    public SubChannel createSubChannel(Long channelId, String name, String description) {
        Channel parent = channelRepository.findById(channelId)
                .orElseThrow(() -> new IllegalArgumentException("Channel not found: " + channelId));
        SubChannel sub = new SubChannel(name.trim(), description, parent);
        return subChannelRepository.save(sub);
    }

    // ── Read ──────────────────────────────────────────────────────────────────

    public List<ChannelSummary> listChannels() {
        return channelRepository.findAllByOrderByCreatedAtAsc()
                .stream()
                .map(this::toSummary)
                .collect(Collectors.toList());
    }

    public List<SubChannelSummary> getSubChannels(Long channelId) {
        return subChannelRepository.findByChannelId(channelId)
                .stream()
                .map(s -> new SubChannelSummary(
                        s.getId(), s.getName(), s.getDescription(),
                        channelId, s.getCreatedAt()))
                .collect(Collectors.toList());
    }

    public List<MemberSummary> getMembers(Long channelId) {
        Channel ch = getChannelOrThrow(channelId);
        return memberRepository.findByChannel(ch)
                .stream()
                .map(m -> new MemberSummary(
                        m.getUser().getId(),
                        m.getUser().getEmail(),
                        m.getUser().getDisplayName(),
                        m.isAdmin(),
                        m.isBanned(),
                        m.getJoinedAt()))
                .collect(Collectors.toList());
    }

    public Optional<Channel> findById(Long id) { return channelRepository.findById(id); }

    public Optional<SubChannel> findSubChannelById(Long id) {
        return subChannelRepository.findById(id);
    }

    // ── Master Admin Management (Root Channel) ────────────────────────────────

    @Transactional
    public AdminSummary addChannelAdmin(Long channelId, String email) {
        Channel ch = getChannelOrThrow(channelId);
        User user = userService.findOrCreate(email.trim().toLowerCase());
        user.setRole(User.Role.ADMIN);
        userRepository.save(user);

        ChannelMember member = memberRepository.findByUserAndChannel(user, ch)
                .orElseGet(() -> new ChannelMember(user, ch, true));
        member.setAdmin(true);
        memberRepository.save(member);

        return new AdminSummary(user.getId(), user.getEmail(), user.getDisplayName());
    }

    @Transactional
    public void removeChannelAdmin(Long channelId, Long userId) {
        Channel ch = getChannelOrThrow(channelId);
        User user = getUserOrThrow(userId);
        memberRepository.findByUserAndChannel(user, ch).ifPresent(m -> {
            m.setAdmin(false);
            memberRepository.save(m);
        });
        // Downgrade global role if no longer admin anywhere
        downgradeRoleIfNoAdminRoles(user);
    }


    public List<AdminSummary> getChannelAdmins(Long channelId) {
        Channel ch = getChannelOrThrow(channelId);
        return memberRepository.findByChannelAndIsAdminTrue(ch)
                .stream()
                .map(m -> new AdminSummary(m.getUser().getId(), m.getUser().getEmail(), m.getUser().getDisplayName()))
                .collect(Collectors.toList());
    }

    public boolean isChannelAdmin(Long channelId, User user) {
        if (user == null) return false;
        Channel ch = channelRepository.findById(channelId).orElse(null);
        if (ch == null) return false;
        return memberRepository.findByUserAndChannel(user, ch)
                .map(ChannelMember::isAdmin)
                .orElse(false);
    }

    // ── Sub-Channel Admin Management ──────────────────────────────────────────

    @Transactional
    public AdminSummary addSubChannelAdmin(Long subChannelId, String email) {
        SubChannel sub = subChannelRepository.findById(subChannelId)
                .orElseThrow(() -> new IllegalArgumentException("SubChannel not found: " + subChannelId));
        User user = userService.findOrCreate(email.trim().toLowerCase());
        user.setRole(User.Role.ADMIN);
        userRepository.save(user);

        if (!subChannelAdminRepository.existsByUserAndSubChannel(user, sub)) {
            subChannelAdminRepository.save(new SubChannelAdmin(user, sub));
        }

        // Also ensure user is in parent channel member list
        Channel parent = sub.getChannel();
        if (memberRepository.findByUserAndChannel(user, parent).isEmpty()) {
            memberRepository.save(new ChannelMember(user, parent, false));
        }

        return new AdminSummary(user.getId(), user.getEmail(), user.getDisplayName());
    }

    @Transactional
    public void removeSubChannelAdmin(Long subChannelId, Long userId) {
        SubChannel sub = subChannelRepository.findById(subChannelId)
                .orElseThrow(() -> new IllegalArgumentException("SubChannel not found: " + subChannelId));
        User user = getUserOrThrow(userId);
        subChannelAdminRepository.findByUserAndSubChannel(user, sub)
                .ifPresent(subChannelAdminRepository::delete);
        // Downgrade global role if no longer admin anywhere
        downgradeRoleIfNoAdminRoles(user);
    }


    public List<AdminSummary> getSubChannelAdmins(Long subChannelId) {
        return subChannelAdminRepository.findBySubChannelId(subChannelId)
                .stream()
                .map(sca -> new AdminSummary(sca.getUser().getId(), sca.getUser().getEmail(), sca.getUser().getDisplayName()))
                .collect(Collectors.toList());
    }

    /**
     * Checks if a user is admin of a sub-channel:
     * - Returns true if user is Master Admin of parent channel
     * - Returns true if user is specifically assigned admin of this sub-channel
     */
    public boolean isSubChannelAdmin(Long subChannelId, User user) {
        if (user == null) return false;
        SubChannel sub = subChannelRepository.findById(subChannelId).orElse(null);
        if (sub == null) return false;

        // Check if user is Master Admin of root channel
        if (isChannelAdmin(sub.getChannel().getId(), user)) return true;

        // Check if user is assigned admin of this specific sub-channel
        return subChannelAdminRepository.existsByUserAndSubChannel(user, sub);
    }

    // ── Membership ────────────────────────────────────────────────────────────

    public boolean verifyPin(Long channelId, String pin) {
        Channel ch = getChannelOrThrow(channelId);
        if (ch.getType() == Channel.ChannelType.PUBLIC) return true;
        if (ch.getPinHash() == null) return true;
        return hashPin(pin.trim()).equals(ch.getPinHash());
    }

    @Transactional
    public boolean joinChannel(Long channelId, User user, String pin) {
        Channel ch = getChannelOrThrow(channelId);

        Optional<ChannelMember> existing = memberRepository.findByUserAndChannel(user, ch);
        if (existing.isPresent()) {
            if (existing.get().isBanned()) {
                throw new IllegalStateException("You are banned from this channel.");
            }
            return true;
        }

        if (ch.getType() == Channel.ChannelType.PRIVATE) {
            if (pin == null || !hashPin(pin.trim()).equals(ch.getPinHash())) {
                return false;
            }
        }

        memberRepository.save(new ChannelMember(user, ch, false));
        return true;
    }

    @Transactional
    public void leaveChannel(Long channelId, User user) {
        Channel ch = getChannelOrThrow(channelId);
        memberRepository.findByUserAndChannel(user, ch)
                .ifPresent(memberRepository::delete);
    }

    public boolean isMember(Long channelId, User user) {
        Channel ch = channelRepository.findById(channelId).orElse(null);
        if (ch == null) return false;
        return memberRepository.existsByUserAndChannelAndIsBannedFalse(user, ch);
    }

    // ── Moderation ────────────────────────────────────────────────────────────

    @Transactional
    public void banUser(Long channelId, Long targetUserId) {
        Channel ch     = getChannelOrThrow(channelId);
        User    target = getUserOrThrow(targetUserId);

        ChannelMember member = memberRepository.findByUserAndChannel(target, ch)
                .orElseGet(() -> new ChannelMember(target, ch, false));
        member.setBanned(true);
        memberRepository.save(member);
    }

    @Transactional
    public void kickUser(Long channelId, Long targetUserId) {
        Channel ch     = getChannelOrThrow(channelId);
        User    target = getUserOrThrow(targetUserId);
        memberRepository.findByUserAndChannel(target, ch)
                .ifPresent(memberRepository::delete);
    }

    // ── Delete ────────────────────────────────────────────────────────────────

    @Transactional
    public void deleteChannel(Long channelId) {
        channelRepository.deleteById(channelId);
    }

    @Transactional
    public void deleteSubChannel(Long subChannelId) {
        subChannelRepository.deleteById(subChannelId);
    }

    // ── Private helpers ───────────────────────────────────────────────────────

    private Channel getChannelOrThrow(Long id) {
        return channelRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Channel not found: " + id));
    }

    private User getUserOrThrow(Long id) {
        return userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + id));
    }

    /**
     * Revokes User.Role → USER when the user no longer holds any admin position:
     *   - Not a Master Admin (ChannelMember.isAdmin = true) in any channel
     *   - Not a Sub-Channel Admin (SubChannelAdmin record) in any sub-channel
     *
     * Called immediately after removing an admin from a channel or sub-channel.
     * If the user is still an admin somewhere else, their role is left untouched.
     */
    private void downgradeRoleIfNoAdminRoles(User user) {
        boolean stillChannelAdmin    = memberRepository.existsByUserAndIsAdminTrue(user);
        boolean stillSubChannelAdmin = subChannelAdminRepository.existsByUser(user);

        if (!stillChannelAdmin && !stillSubChannelAdmin) {
            user.setRole(User.Role.USER);
            userRepository.save(user);
            System.out.println("[CampiFi] Admin privileges revoked for: " + user.getEmail());
        }
    }


    private String hashPin(String pin) {
        try {
            byte[] hash = MessageDigest.getInstance("SHA-256")
                    .digest(pin.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hash) sb.append(String.format("%02x", b));
            return sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
    }

    private ChannelSummary toSummary(Channel ch) {
        int members     = memberRepository.findByChannelAndIsBannedFalse(ch).size();
        int subChannels = subChannelRepository.findByChannelId(ch.getId()).size();
        return new ChannelSummary(
                ch.getId(), ch.getName(), ch.getDescription(),
                ch.getType().name(), members, subChannels,
                ch.getPinHash() != null, ch.getCreatedAt());
    }

    // ── DTOs ──────────────────────────────────────────────────────────────────

    public record ChannelSummary(
            Long id, String name, String description, String type,
            int memberCount, int subChannelCount, boolean hasPin,
            LocalDateTime createdAt) {}

    public record SubChannelSummary(
            Long id, String name, String description,
            Long parentChannelId, LocalDateTime createdAt) {}

    public record MemberSummary(
            Long userId, String email, String displayName,
            boolean isAdmin, boolean isBanned, LocalDateTime joinedAt) {}

    public record AdminSummary(
            Long userId, String email, String displayName) {}
}
