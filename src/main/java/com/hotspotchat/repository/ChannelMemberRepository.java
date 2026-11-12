package com.hotspotchat.repository;

import com.hotspotchat.model.Channel;
import com.hotspotchat.model.ChannelMember;
import com.hotspotchat.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface ChannelMemberRepository extends JpaRepository<ChannelMember, Long> {
    Optional<ChannelMember> findByUserAndChannel(User user, Channel channel);
    List<ChannelMember> findByChannel(Channel channel);
    List<ChannelMember> findByChannelAndIsBannedFalse(Channel channel);
    boolean existsByUserAndChannelAndIsBannedFalse(User user, Channel channel);
    List<ChannelMember> findByChannelAndIsAdminTrue(Channel channel);
    List<ChannelMember> findByChannelIdAndIsAdminTrue(Long channelId);
    boolean existsByUserAndIsAdminTrue(User user);
}

