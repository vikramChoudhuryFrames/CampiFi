package com.hotspotchat.service;

import com.hotspotchat.model.User;
import com.hotspotchat.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

/**
 * Manages User records in the database.
 *
 * Display-name parsing mirrors the logic in app.js parseEmailToName():
 *   john.doe@uni.edu   → "John Doe"
 *   alice_smith@ac.in  → "Alice Smith"
 *   2021cs01@iit.ac.in → "Cs" (numeric roll numbers stripped)
 */
@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Looks up a user by email. Creates one with USER role if they don't exist yet.
     * Display name is auto-parsed from the email local part.
     */
    @Transactional
    public User findOrCreate(String email) {
        return userRepository.findByEmail(email.toLowerCase())
                .orElseGet(() -> {
                    User u = new User(email.toLowerCase(), parseDisplayName(email), User.Role.USER);
                    return userRepository.save(u);
                });
    }

    /**
     * Returns the user by email if present.
     */
    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email.toLowerCase());
    }

    /**
     * Promotes an existing user to ADMIN role. Called from the server-side admin panel (Task 8).
     */
    @Transactional
    public User promoteToAdmin(String email) {
        User user = userRepository.findByEmail(email.toLowerCase())
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + email));
        user.setRole(User.Role.ADMIN);
        return userRepository.save(user);
    }

    /**
     * Demotes an ADMIN back to USER role.
     */
    @Transactional
    public User demoteToUser(String email) {
        User user = userRepository.findByEmail(email.toLowerCase())
                .orElseThrow(() -> new IllegalArgumentException("User not found: " + email));
        user.setRole(User.Role.USER);
        return userRepository.save(user);
    }

    // ── Static helper ─────────────────────────────────────────────────────────

    /**
     * Parses the display name from an institution email address.
     * Mirrors the parseEmailToName() function in app.js.
     *
     * Examples:
     *   john.doe@university.edu   → "John Doe"
     *   alice_smith@college.ac.in → "Alice Smith"
     *   rahul-kumar@campus.edu    → "Rahul Kumar"
     *   2021cs042@iit.ac.in       → "Cs"
     */
    public static String parseDisplayName(String email) {
        if (email == null || !email.contains("@")) return email;

        // Take local part (before @)
        String local = email.split("@")[0].toLowerCase();

        // Split on delimiters: dot, underscore, hyphen
        String[] parts = local.split("[._\\-]+");

        java.util.List<String> cleaned = new java.util.ArrayList<>();
        for (String part : parts) {
            // Strip leading/trailing digits, keep only letters
            String clean = part.replaceAll("^\\d+|\\d+$", "").replaceAll("[^a-z]", "");
            if (!clean.isEmpty()) {
                // Capitalize first letter
                cleaned.add(Character.toUpperCase(clean.charAt(0)) + clean.substring(1));
            }
        }

        if (cleaned.isEmpty()) {
            // Fallback: strip all non-letters from the local part
            String letters = local.replaceAll("[^a-z]", "");
            if (!letters.isEmpty()) {
                return Character.toUpperCase(letters.charAt(0)) + letters.substring(1);
            }
            return "User";
        }

        if (cleaned.size() == 1) return cleaned.get(0);

        // First + Last (ignore middle tokens like roll-number fragments)
        return cleaned.get(0) + " " + cleaned.get(cleaned.size() - 1);
    }
}
