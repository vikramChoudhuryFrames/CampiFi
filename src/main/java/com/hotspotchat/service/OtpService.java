package com.hotspotchat.service;

import com.hotspotchat.model.OtpToken;
import com.hotspotchat.repository.OtpTokenRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.security.SecureRandom;
import java.time.LocalDateTime;
import java.util.Optional;

/**
 * Generates, stores, and verifies 6-digit OTP codes for admin login.
 *
 * Each OTP:
 *  - Is 6 digits (000000 – 999999, zero-padded)
 *  - Expires exactly 5 minutes after creation
 *  - Is single-use (marked 'used' immediately after successful verification)
 *
 * Expired tokens are cleaned up every 15 minutes via @Scheduled.
 */
@Service
public class OtpService {

    private final OtpTokenRepository otpTokenRepository;
    private final EmailService emailService;
    private final SecureRandom secureRandom = new SecureRandom();

    @Autowired
    public OtpService(OtpTokenRepository otpTokenRepository, EmailService emailService) {
        this.otpTokenRepository = otpTokenRepository;
        this.emailService = emailService;
    }

    /**
     * Generates a new OTP for the given email, saves it, and sends it.
     * Any previous unused OTPs for this email are superseded (they still expire naturally).
     */
    @Transactional
    public void generateAndSend(String email) {
        // Generate a 6-digit zero-padded OTP
        String otp = String.format("%06d", secureRandom.nextInt(1_000_000));

        OtpToken token = new OtpToken(email, otp);
        otpTokenRepository.save(token);

        emailService.sendOtpEmail(email, otp);
    }

    /**
     * Verifies the submitted OTP for the given email.
     *
     * @return true if valid (correct, unused, not expired); false otherwise
     */
    @Transactional
    public boolean verify(String email, String submittedOtp) {
        Optional<OtpToken> tokenOpt = otpTokenRepository
                .findTopByEmailAndUsedFalseAndExpiresAtAfterOrderByCreatedAtDesc(
                        email, LocalDateTime.now());

        if (tokenOpt.isEmpty()) return false;

        OtpToken token = tokenOpt.get();
        if (!token.isValid(submittedOtp)) return false;

        // Mark as used immediately — single-use enforcement
        token.setUsed(true);
        otpTokenRepository.save(token);
        return true;
    }

    /**
     * Runs every 15 minutes to delete expired OTP tokens and keep the table clean.
     */
    @Scheduled(cron = "0 */15 * * * *")
    @Transactional
    public void cleanupExpiredTokens() {
        otpTokenRepository.deleteExpiredTokens(LocalDateTime.now());
    }
}
