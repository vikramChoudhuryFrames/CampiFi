package com.hotspotchat.repository;

import com.hotspotchat.model.Channel;
import com.hotspotchat.model.Message;
import com.hotspotchat.model.SubChannel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MessageRepository extends JpaRepository<Message, Long> {
    /** All messages in a public channel (direct posts), oldest first */
    List<Message> findByChannelOrderBySentAtAsc(Channel channel);

    /** All messages in a sub-channel, oldest first */
    List<Message> findBySubChannelOrderBySentAtAsc(SubChannel subChannel);

    /** Last N messages in a sub-channel for pagination (Task 5) */
    List<Message> findTop50BySubChannelOrderBySentAtDesc(SubChannel subChannel);
}
