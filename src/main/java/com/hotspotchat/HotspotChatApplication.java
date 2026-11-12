package com.hotspotchat;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling   // needed for periodic OTP cleanup job in OtpService
public class HotspotChatApplication {
    public static void main(String[] args) {
        SpringApplication.run(HotspotChatApplication.class, args);
    }
}
