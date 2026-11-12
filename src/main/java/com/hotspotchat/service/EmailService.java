package com.hotspotchat.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

/**
 * Sends OTP emails via SMTP.
 *
 * If SMTP is not yet configured (default stub values in application.properties),
 * it PRINTS the OTP to the server console so you can test without real email.
 */
@Service
public class EmailService {

    // Injected as optional — app still starts even if mail auto-config fails
    @Autowired(required = false)
    private JavaMailSender mailSender;

    @Value("${spring.mail.username:not-configured}")
    private String fromAddress;

    /**
     * Sends a 6-digit OTP to the given email address.
     * Always logs to console regardless of SMTP status.
     */
    public void sendOtpEmail(String to, String otp) {
        // Always print to server console — handy for local testing
        System.out.println("\n========================================");
        System.out.println("  CAMPIFI ADMIN OTP");
        System.out.println("  To      : " + to);
        System.out.println("  OTP     : " + otp);
        System.out.println("  Valid   : 5 minutes");
        System.out.println("========================================\n");

        if (!isMailConfigured()) {
            // SMTP not configured — OTP visible in terminal only
            return;
        }

        try {
            SimpleMailMessage msg = new SimpleMailMessage();
            msg.setFrom(fromAddress);
            msg.setTo(to);
            msg.setSubject("CampiFi Admin Verification Code");
            msg.setText(
                    "Hello,\n\n" +
                    "Your CampiFi admin verification code is:\n\n" +
                    "   " + otp + "\n\n" +
                    "This code is valid for 5 minutes. Do not share it with anyone.\n\n" +
                    "— CampiFi"
            );
            mailSender.send(msg);
        } catch (Exception e) {
            System.err.println("[EmailService] Email delivery failed: " + e.getMessage());
            System.err.println("[EmailService] OTP is still printed above in the console.");
        }
    }

    private boolean isMailConfigured() {
        return mailSender != null
                && fromAddress != null
                && !fromAddress.equals("not-configured")
                && !fromAddress.startsWith("your-");
    }
}
