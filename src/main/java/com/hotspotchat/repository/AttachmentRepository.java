package com.hotspotchat.repository;

import com.hotspotchat.model.Attachment;
import com.hotspotchat.model.Message;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AttachmentRepository extends JpaRepository<Attachment, Long> {
    List<Attachment> findByMessage(Message message);
}
