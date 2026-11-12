package com.hotspotchat.controller;

import com.hotspotchat.model.ChatMessage;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Controller
public class ChatController {

    @MessageMapping("/chat/{room}")
    @SendTo("/topic/room/{room}")
    public ChatMessage sendMessage(@DestinationVariable String room, ChatMessage message) {
        message.setRoom(room);
        message.setTimestamp(LocalDateTime.now().format(DateTimeFormatter.ofPattern("HH:mm:ss")));
        return message;
    }
}
