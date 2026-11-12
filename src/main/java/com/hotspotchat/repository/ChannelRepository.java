package com.hotspotchat.repository;

import com.hotspotchat.model.Channel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ChannelRepository extends JpaRepository<Channel, Long> {
    Optional<Channel> findByName(String name);
    boolean existsByName(String name);
    List<Channel> findAllByOrderByCreatedAtAsc();
    List<Channel> findByType(Channel.ChannelType type);
}
