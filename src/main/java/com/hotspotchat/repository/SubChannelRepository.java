package com.hotspotchat.repository;

import com.hotspotchat.model.Channel;
import com.hotspotchat.model.SubChannel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SubChannelRepository extends JpaRepository<SubChannel, Long> {
    List<SubChannel> findByChannelOrderByCreatedAtAsc(Channel channel);
    List<SubChannel> findByChannelId(Long channelId);
}
