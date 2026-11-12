package com.hotspotchat.repository;

import com.hotspotchat.model.SubChannel;
import com.hotspotchat.model.SubChannelAdmin;
import com.hotspotchat.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface SubChannelAdminRepository extends JpaRepository<SubChannelAdmin, Long> {
    List<SubChannelAdmin> findBySubChannel(SubChannel subChannel);
    List<SubChannelAdmin> findBySubChannelId(Long subChannelId);
    Optional<SubChannelAdmin> findByUserAndSubChannel(User user, SubChannel subChannel);
    boolean existsByUserAndSubChannel(User user, SubChannel subChannel);
    void deleteByUserAndSubChannel(User user, SubChannel subChannel);
    boolean existsByUser(User user);
}

